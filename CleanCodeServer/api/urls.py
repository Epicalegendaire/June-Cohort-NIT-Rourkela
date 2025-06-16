
from django.urls import path
from .views import load_model, generate_prescription

urlpatterns = [
    path('load-model/', load_model),
    path('prescribe/', generate_prescription),
]
