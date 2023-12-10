from rest_framework import viewsets
import requests
from django.http import JsonResponse



def hello_world(request):
    return JsonResponse({"message": "Hello World"})