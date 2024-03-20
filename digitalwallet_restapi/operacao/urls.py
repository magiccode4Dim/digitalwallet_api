from django.urls import path,include
from django.contrib.auth import views as auth_views
from .views import * 


app_name = 'operacao'
getAllByContID
urlpatterns = [
    path('register',Register.as_view(),name="RegisterOperacao"),
    path('getall',getAll,name="getall"),
    path('getall/<int:id_conta>',getAllByContID,name="getAllByContID"),
    path('get/<int:id_operacao>',getByOperationID,name="getByOperationID"),     
]