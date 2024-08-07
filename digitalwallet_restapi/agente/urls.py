from django.urls import path,include
from django.contrib.auth import views as auth_views
from .views import * 


app_name = 'agente'

urlpatterns = [
    path('getall',getAll,name="getall"),
    path('register',Register.as_view(),name="RegisterAgent"),
    path('get/<int:id_agent>',get,name="get"),
    path('get',getMy,name="getMy"),
    path('update',update,name="update"),
    path('addsaldo',addAgentSaldo,name="addAgentSaldo"),         
]