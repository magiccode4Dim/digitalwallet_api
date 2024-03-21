from django.urls import path,include
from django.contrib.auth import views as auth_views
from .views import * 


app_name = 'levantamento'

urlpatterns = [
    path('register',Register.as_view(),name="RegisterDeposito"),
    path('getall/<int:id_conta>',getAll,name="getAll"),
    path('getall',getAllAgent,name="getAllAgent"),
      
]