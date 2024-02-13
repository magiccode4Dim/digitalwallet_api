from django.urls import path,include
from django.contrib.auth import views as auth_views
from .views import * 


app_name = 'cliente'

urlpatterns = [
    path('register',Register.as_view(),name="RegisterClient")
]