from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Keep track of doctor-specific models
model_registry = {}

def load_doctor_model(doctor_id):
    """
    Load model/tokenizer/pipeline for the given doctor ID.
    """
    tokenizer = AutoTokenizer.from_pretrained('./base-Locutusque-medical')
    model = AutoModelForCausalLM.from_pretrained('./base-Locutusque-medical')
    pipe = pipeline("prescription-generation", model=model, tokenizer=tokenizer)

    model_registry[doctor_id] = pipe
    return f"Model {model_name} loaded for doctor {doctor_id}"

def get_model_for_doctor(doctor_id):
    return model_registry.get(doctor_id)
