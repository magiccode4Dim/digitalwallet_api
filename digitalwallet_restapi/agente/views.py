from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Agente
from .serializer import AgenteSerializer

# Create your views here.
@api_view(['GET'])
def getAll(request):
    data = Agente.objects.all()
    serializer = AgenteSerializer(data, many=True)
    return Response(serializer.data)