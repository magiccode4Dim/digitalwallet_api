"""digitalwallet_restapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('agente/', include('agente.urls')),
    path('cliente/', include('cliente.urls')),
    path('conta/', include('conta.urls')),
    path('deposito/', include('deposito.urls')),
    path('levantamento/', include('levantamento.urls')),
    path('operacao/', include('operacao.urls')),
    path('transferencia/', include('transferencia.urls')),
    path('utilizador/', include('utilizador.urls')),
    path('otp/', include('opt_module.urls')),
    path('docs/', TemplateView.as_view(
        template_name='docs.html',
        extra_context={'schema_url':'api_schema'}
        ), name='swagger-ui'),
    path('api_schema/', get_schema_view(
        title='DOCUMENTAÇÃO DA API',
        description='Aqui estão os detalhes de todas urls da aplicação.'
    ), name='api_schema')
]
