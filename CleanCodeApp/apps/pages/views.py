from django.http import HttpResponse
from apps.pages.models import Appointment, Patient
# Create your views here.
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm


def index(request):

    # Page from the theme 
    return render(request, 'pages/dashboard.html')

def prescribe_view(request):
    
    return render(request, 'pages/prescribe.html')

def patients_view(request):
    context = {
        'segment': 'patients',
        # optionally pass data like: 'patients': Patient.objects.all()
    }
    return render(request, 'pages/patients.html', context)

def appointments(request):

    return render(request, 'pages/appoinments.html')