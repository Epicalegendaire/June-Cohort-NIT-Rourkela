
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .model_loader import load_doctor_model, get_model_for_doctor
from PrescriptionAI.Inference import Infer

@api_view(["POST"])
def load_model(request):
    doctor_id = request.data.get("doctor_id")

    if not doctor_id:
        return Response({"error": "doctor_id is required"}, status=400)

    try:
        msg = load_doctor_model(doctor_id)
        return Response({"message": msg})
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
@api_view(["POST"])
def generate_prescription(request):
    doctor_id = request.data.get("doctor_id")
    symptoms = request.data.get("symptoms", [])

    if not doctor_id or not symptoms:
        return Response({"error": "doctor_id and symptoms are required"}, status=400)

    (tokenizer,model) = get_model_for_doctor(doctor_id)
    
    if not model or not tokenizer:
        return Response({"error": f"Model not loaded for doctor_id {doctor_id}"}, status=404)
    
   
    symptom_text = ', '.join(symptoms) if isinstance(symptoms, list) else symptoms
    #incase symptoms is passed on as a list
    query = f"Symptoms: {symptom_text}. Prescriptions only:"
    
    try:
        result = Infer(tokenizer, model).generate_medical_response(query)
    except Exception as e:
        return Response({"error": f"Inference failed: {str(e)}"}, status=500)
        
    return Response({"prescription": result})
