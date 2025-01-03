from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('set-api-key/', views.set_api_key, name='set_api_key'),
    path('get-response/', views.get_response, name='get_response'),
]
