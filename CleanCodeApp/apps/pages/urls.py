from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('patients/', views.patients_view, name='patients'),
    path('appointments/', views.appointments, name='appointments'),
    
]
