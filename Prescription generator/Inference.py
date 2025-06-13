import torch
import ModelToolKit
'''
-each doctor will have their own model, so save model weights locally
-fine tune on new diagnosis and symptoms
-adaptive learning, learns new drugs/brands are assigns meaning in fine tuning process

'''

''' test out the fine tuning feature
load = ModelToolKit.FineTuneModel(doctor_id=101,symp='Fever, Headache, Body Pain',presc='Dolo 650, Flexon')
load.train()
exit()
'''


doctor_id = 101

(tokenizer, model) = ModelToolKit.LoadModel(doctor_id).load()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

#optimised presets
def generate_medical_response(prompt, max_new_tokens=30):
    input_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)
    output_ids = model.generate(
        input_ids,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        top_k=41,
        top_p=0.14,
        temperature=0.8,
        repetition_penalty=1.176
    )
    return tokenizer.decode(output_ids[0], skip_special_tokens=True)


symp = 'chest pain and shortness of breath'

query = f"Symptoms: {symp}. Prescriptions only:"


print(generate_medical_response(query))


