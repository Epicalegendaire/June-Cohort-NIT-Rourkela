
from PrescriptionAI.ModelToolKit import LoadModel
from PrescriptionAI.ModelToolKit import GenerateModel
# Keep track of doctor-specific models
model_registry = {}

def load_doctor_model(doctor_id):
    """
    Load model/tokenizer for the given doctor ID.
    """
    load = LoadModel(doctor_id)
    (tokenizer,model) = load.load()
    if tokenizer is not None and model is not None:
        print("Model and tokenizer loaded successfully.")
        model_registry[doctor_id] = (tokenizer,model)
    else:
        print("Error: Model or tokenizer is None, generating a model..")
        gen = GenerateModel()
        gen.generate(doctor_id)
        load_doctor_model(doctor_id)
    
    
    return f"Personalied Model loaded for doctor {doctor_id}"

def get_model_for_doctor(doctor_id):
    return model_registry.get(doctor_id)
