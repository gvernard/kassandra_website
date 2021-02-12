from django.urls import path
from prescribe import views

urlpatterns = [
    path('', views.prescribe,name='prescribe'),
]

