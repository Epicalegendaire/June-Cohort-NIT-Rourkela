from transformers import AutoTokenizer, AutoModelForCausalLM
from torch.utils.data import Dataset
from transformers import Trainer, TrainingArguments
import re
from transformers import BitsAndBytesConfig
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from peft import prepare_model_for_kbit_training, LoraConfig, get_peft_model
import torch
from peft import PeftModel


'''
-each doctor will have their own model, so save model weights locally
-fine tune on new diagnosis and symptoms
'''
class QLoRAtools():
    def __init__(self):
        self.bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
        )      
        self.lora_config = LoraConfig(
            r=8,
            lora_alpha=32,
            target_modules=["c_attn"],  # GPT-2-specific target layer
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM",
        )

    
class LoadModel():
    def __init__(self,doctor_id):
        self.doctor_id = doctor_id
        print('Loading personalised precription agent....')
        qt =  QLoRAtools()
        self.bnb_config = qt.bnb_config
        self.lora_config = qt.lora_config

    def load(self):
        
        tokenizer = AutoTokenizer.from_pretrained(f"./personalised/{self.doctor_id}")
        model = AutoModelForCausalLM.from_pretrained('./base-Locutusque-medical',quantization_config =self.bnb_config,device_map = "auto")
        model = prepare_model_for_kbit_training(model)
        model = get_peft_model(model, self.lora_config)

        #add peft wrapper using LoRA adapter
        pmodel = PeftModel.from_pretrained(model, f"./personalised/{self.doctor_id}")
        return (tokenizer, pmodel)
    

class GenerateModel():
    def __init__(self):
        
        print('Loading Locutusque gpt2 medical base model....')
        self.qt = QLoRAtools()

        #since gpt 2 models like locutusque, do not have a pad token and for training we need one

        
    def download_base(self):
        model_name = "Locutusque/gpt2-large-medical"
        
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        tokenizer.add_special_tokens({'pad_token': '[PAD]'})
        model.resize_token_embeddings(len(self.tokenizer))
        model.save_pretrained('./base-Locutusque-medical')
        tokenizer.save_pretrained("./base-Locutusque-medical")

    def generate(self,doctor_id):
        try:

            #if base locutuque medical exists, otherwise download
            tokenizer = AutoTokenizer.from_pretrained('./base-Locutusque-medical')
            model = AutoModelForCausalLM.from_pretrained('./base-Locutusque-medical',quantization_config =self.qt.bnb_config,device_map = "auto")
            model = prepare_model_for_kbit_training(model)
            model = get_peft_model(model, self.qt.lora_config)
            #basic finetuning
            symp = 'Cold, Runny Nose, Sneezing'
            presc = 'Cetcip-L, Sinarest'
            FineTuneModel(model,tokenizer,doctor_id,symp=symp,presc=presc)
            #we also have to generate the lora adapter, for the first time
        except:
            print('Base Model does not exist or is corrupted, generating a new model.')
            self.download_base()
    

class TrainDataset(Dataset):
    def __init__(self, texts, tokenizer, max_length=30):
        self.tokenizer = tokenizer
        self.inputs = tokenizer(texts, truncation=True, padding='max_length', max_length=max_length, return_tensors='pt')

    def __len__(self):
        return self.inputs.input_ids.shape[0]

    def __getitem__(self, idx):
        return {
            "input_ids": self.inputs.input_ids[idx],
            "attention_mask": self.inputs.attention_mask[idx],
            "labels": self.inputs.input_ids[idx]
        }


class FineTuneModel():
    
    def __init__(self, model, tokenizer, doctor_id,symp,presc):
        self.doctor_id = doctor_id
        (self.tokenizer, self.model) = (tokenizer, model)
        
        print('updating preferences...')
        self.symp = symp
        self.presc = presc

        self.training_args = TrainingArguments(
            output_dir=f"./personalised/{doctor_id}",
            evaluation_strategy="no",
            num_train_epochs=3,
            per_device_train_batch_size=1,
            logging_dir="./logs",
            save_strategy="epoch",
            save_total_limit=2,
            learning_rate=5e-5,
            fp16=False,
            push_to_hub=False
        )

        self.add_new_tokens()
        

    def add_new_tokens(self):
        new_names = re.split(r"[ ,.]+", self.presc)
        
        print(new_names)
        no_added_tokens = self.tokenizer.add_tokens(new_names)
        print(f"Added {no_added_tokens} new tokens.")
        self.model.resize_token_embeddings(len(self.tokenizer))
        

    def create_prompt(self,symp, presc):
        return f"Symptoms: {symp}. Prescriptions only: {presc}."
    

    def train(self):
        prompt = self.create_prompt(self.symp,self.presc)
        dataset = TrainDataset(prompt, self.tokenizer)

        trainer = Trainer(
            model=self.model,
            args=self.training_args,
            train_dataset=dataset,
            tokenizer=self.tokenizer,
            data_collator=DataCollatorForLanguageModeling(self.tokenizer, mlm=False)

        )
        trainer.train()

        #save the LoRA adapters
        self.model.save_pretrained(f"./personalised/{self.doctor_id}")
        self.tokenizer.save_pretrained(f"./personalised/{self.doctor_id}")

