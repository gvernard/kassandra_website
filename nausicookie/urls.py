from django.urls import path
from nausicookie import views

urlpatterns = [
    path('', views.hello_nausicookie,name='hello_nausicookie'),
]

