from django.urls import path,include
from django.contrib.auth import views as auth_views
from .views import * 




app_name = 'opt_module'
urlpatterns = [
    path('validate_user_account',otp_account_validation.as_view(),name="otp_account_validation"),
    path('validate_client_account',otp_client_account_validation.as_view(),name="otp_client_account_validation"),
    path('validate_deposit',otp_deposit_validation.as_view(),name="otp_deposit_validation"),
    path('validate_levantament',otp_levantament_validation.as_view(),name="otp_levantament_validation"),
    path('validate_transferenc',otp_transferenc_validation.as_view(),name="otp_transferenc_validation"),
    path('getall/tempagent',getAllTempAgent,name="getAllTempAgent"),
    path('getall/tempclient',getAllTempClient,name="getAllTempClient"),
    path('getall/tempconta',getAllTempConta,name="getAllTempConta"),
    path('getall/tempdeposito',getAllTempDeposito,name="getAllTempDeposito"),
    path('getall/templevantamento',getAllTempLevantamento,name="getAllTempLevantamento"),
    path('getall/temptransferencia',getAllTempTransferencia,name="getAllTempTransferencia"),
    path('getall/operacaootp',getAlloperacaoOPT,name="getAlloperacaoOPT"),
    path('getall/accountvalidationotp',getAllaccontValidationOTP,name="getAllaccontValidationOTP"),                
]