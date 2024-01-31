from django.urls import path,include
from django.contrib.auth import views as auth_views
from .views import * 


app_name = 'agente'

urlpatterns = [
    path('getall',getAll,name="getall"),
    path('register',Register.as_view(),name="RegisterAgent"),   
]