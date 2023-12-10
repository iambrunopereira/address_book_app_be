from rest_framework import viewsets
import requests
from django.http import JsonResponse



def hello_world(request):
    return JsonResponse({"message": "Hello World"})

def fetch_random_user(request):
    response = requests.get('https://randomuser.me/api/')
    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Failed to fetch data'}, status=500)