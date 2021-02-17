from django.urls import path
from home import views

urlpatterns = [
    path('', views.home,name='home'),
    path('get_global_new_cases/', views.get_global_new_cases,name='get_global_new_cases'),
]


