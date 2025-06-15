from PrescriptionAI.ModelToolKit import LoadModel

# Keep track of doctor-specific models
model_registry = {}

def load_doctor_model(doctor_id):
    """
    Load model/tokenizer/pipeline for the given doctor ID.
    """
    load = LoadModel(doctor_id)
    (tokenizer,model) = load.load()
    model_registry[doctor_id] = (tokenizer,model)
    
    return f"Personalied Model loaded for doctor {doctor_id}"

def get_model_for_doctor(doctor_id):
    return model_registry.get(doctor_id)
