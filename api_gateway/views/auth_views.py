
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
import json
from address_book_app_be.settings import AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_DOMAIN


@csrf_exempt
def login(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

    body = json.loads(request.body)
    email = body.get('email')
    password = body.get('password')

    myobj = {
        "grant_type":"password",
        "client_id":AUTH0_CLIENT_ID,
        "client_secret":AUTH0_CLIENT_SECRET,
        "username": email,
        "password": password,
        "scope":"openid profile email name"
    }
    url = f'https://{AUTH0_DOMAIN}/oauth/token'
    x = requests.post(url, json = myobj)
    return JsonResponse({'data': x.json()})

@csrf_exempt
def signup(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

    body = json.loads(request.body)
    email = body.get('email')
    password = body.get('password')

    myobj = {
        "client_id":AUTH0_CLIENT_ID,
        "email": email,
        "password": password,
        "connection":"Username-Password-Authentication"
    }
    url = f'https://{AUTH0_DOMAIN}/dbconnections/signup'
    x = requests.post(url, json = myobj)
    return JsonResponse({'data': x.json()})

@csrf_exempt
def change_password(request): 
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

    body = json.loads(request.body)
    email = body.get('email')
    password = body.get('password')

    myobj = {
        "client_id":AUTH0_CLIENT_ID,
        "email": email,
        "password": password,
        "connection":"Username-Password-Authentication"
    }
    url = f'https://{AUTH0_DOMAIN}/dbconnections/change_password'
    x = requests.post(url, json = myobj)
    return JsonResponse({'status': 'success', 'data': x.json()})