
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .model_loader import load_doctor_model, get_model_for_doctor

@api_view(["POST"])
def load_model(request):
    doctor_id = request.data.get("doctor_id")
    model_name = request.data.get("model_name", "gpt2")

    if not doctor_id:
        return Response({"error": "doctor_id is required"}, status=400)

    try:
        msg = load_doctor_model(doctor_id, model_name)
        return Response({"message": msg})
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
@api_view(["POST"])
def generate_prescription(request):
    doctor_id = request.data.get("doctor_id")
    symptoms = request.data.get("symptoms", [])

    if not doctor_id or not symptoms:
        return Response({"error": "doctor_id and symptoms are required"}, status=400)

    pipe = get_model_for_doctor(doctor_id)
    if pipe is None:
        return Response({"error": f"No model loaded for doctor {doctor_id}"}, status=404)

    prompt = "Patient reports: " + ", ".join(symptoms) + ". Prescribe appropriate medicine."
    result = pipe(prompt, max_length=100, num_return_sequences=1)
    return Response({"prescription": result[0]['generated_text']})