from django.urls import path
from predict import views

urlpatterns = [
    path('', views.predict,name='predict'),
    path('test_predictor/', views.test_predictor,name='test_predictor'),
    path('get_latest_ips/', views.get_latest_ips,name='get_latest_ips'),
    path('get_countries_and_regions/', views.get_countries_and_regions,name='get_countries_and_regions'),
    path('get_model_colors/', views.get_model_colors,name='get_model_colors'),
]

