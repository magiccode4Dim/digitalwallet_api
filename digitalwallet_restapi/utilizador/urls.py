from django.urls import path,include
from django.contrib.auth import views as auth_views
from .views import * 


app_name = 'utilizador'

urlpatterns = [
    path('login',Login.as_view(),name="Login"),
    path('register',Register.as_view(),name="Register"),
]