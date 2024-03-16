from django.urls import path,include
from django.contrib.auth import views as auth_views
from .views import * 


app_name = 'utilizador'

urlpatterns = [
    path('login',Login.as_view(),name="Login"),
    path('register',Register.as_view(),name="RegisterUser"),
    path('get/<int:id_user_to_get>',get,name="get"),
    path('delete/<int:id_user_to_delete>',delete,name="delete"),
    path('update',update,name="update"),
    path('getall',getAll,name="getall"),
]