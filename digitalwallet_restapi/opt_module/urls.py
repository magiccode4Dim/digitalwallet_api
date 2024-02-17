from django.urls import path,include
from django.contrib.auth import views as auth_views
from .views import * 


app_name = 'opt_module'
urlpatterns = [
    path('validate_user_account',otp_account_validation.as_view(),name="otp_account_validation"),
    path('validate_client_account',otp_client_account_validation.as_view(),name="otp_client_account_validation"),
    path('validate_deposit',otp_deposit_validation.as_view(),name="otp_deposit_validation"),      
]