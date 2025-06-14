
from django.urls import path
from .views import generate_prescription, load_model

urlpatterns = [
    path('prescribe/', generate_prescription, name='generate_prescription'),
    path('load_model/', load_model),
]
