from django.urls import path,include
from django.contrib.auth import views as auth_views
from .views import * 


app_name = 'conta'

urlpatterns = [
    path('getall',getAll,name="getall"),
    path('delete/<int:id>',delete,name="delete"),
    path('getall/<str:number>',getAllByNumero,name="getAllByNumero"), #PESQUISAR COM BASE NO NUMERO DE CONTA
    path('register',Register.as_view(),name="RegisterConta"),
    path('extract/<int:id_conta>',getExtratoConta,name="getExtratoConta")    
]