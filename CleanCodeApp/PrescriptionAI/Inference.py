import torch

from . import ModelToolKit
'''
-each doctor will have their own model, so save model weights locally
-fine tune on new diagnosis and symptoms
-adaptive learning, learns new drugs/brands are assigns meaning in fine tuning process

'''

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
'''
from ModelToolKit import GenerateModel
load = GenerateModel()
load.generate(101)
'''

'''
from ModelToolKit import LoadModel
from Inference import Infer
load = LoadModel(101)

(tokenizer, model)= load.load()
pipeline = Infer(tokenizer,model)
print(pipeline.generate_medical_response("Symptoms: Cold, Runny Nose, Sneezing. Prescriptions only:"))

'''

class Infer():
    def __init__(self,tokenizer,model):
        self.tokenizer = tokenizer
        self.model = model

        
    #optimised presets
    def generate_medical_response(self,prompt, max_new_tokens=30):
        
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            padding=False,
            truncation=True,
            return_attention_mask=True
        ).to(device)

        output_ids = self.model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"], 
            max_new_tokens=max_new_tokens,
            do_sample=True,
            top_k=41,
            top_p=0.14,
            temperature=0.8,
            repetition_penalty=1.176
        )

        return self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
    




#print(generate_medical_response(query))



