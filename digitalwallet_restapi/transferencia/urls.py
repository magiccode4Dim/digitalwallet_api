from django.urls import path,include
from django.contrib.auth import views as auth_views
from .views import * 


app_name = 'transferencia'

urlpatterns = [
    path('register',Register.as_view(),name="RegisterTransferencia") 
]