from transformers import AutoTokenizer, AutoModelForCausalLM
import pandas as pd
from torch.utils.data import Dataset
from transformers import Trainer, TrainingArguments
import re

'''
-each doctor will have their own model, so save model weights locally
-fine tune on new diagnosis and symptoms
'''

class LoadModel():
    def __init__(self,doctor_id):
        self.doctor_id = doctor_id
        print('Loading personalised precription agent....')
        
    def load(self):
        tokenizer = AutoTokenizer.from_pretrained(f'./personalised/{self.doctor_id}')
        model = AutoModelForCausalLM.from_pretrained(f'./personalised/{self.doctor_id}')
        return (tokenizer, model)

class GenerateModel():
    def __init__(self,doctor_id):
        self.doctor_id = doctor_id
        print('Loading Locutusque gpt2 medical base model....')
        model_name = "Locutusque/gpt2-large-medical"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        
    def generate(self):
        self.model.save_pretrained(f'./personalised/{self.doctor_id}')
        self.tokenizer.save_pretrained(f"./personalised/{self.doctor_id}")

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
    
    def __init__(self,doctor_id,symp,presc):
        self.doctor_id = doctor_id
        (self.tokenizer, self.model) = LoadModel(doctor_id).load()
        #since gpt 2 models like locutusque, do not have a pad token and for training we need one
        self.tokenizer.pad_token = self.tokenizer.eos_token
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
        self.tokenizer.save_pretrained(f"./personalised/{self.doctor_id}")

    def create_prompt(self,symp, presc):
        return f"Symptoms: {symp}. Prescriptions only: {presc}."
    
    def train(self):
        prompt = self.create_prompt(self.symp,self.presc)
        dataset = TrainDataset(prompt, self.tokenizer)
        trainer = Trainer(
            model=self.model,
            args=self.training_args,
            train_dataset=dataset,
            tokenizer=self.tokenizer
        )
        trainer.train()

