
from django.urls import path
from .views import load_model, generate_prescription

urlpatterns = [
    path('load-model/', load_model, name='load_model'),
    path('generate-prescription/', generate_prescription, name='generate_prescription'),
]
