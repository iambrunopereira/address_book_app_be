import os
import requests
from django.http import JsonResponse
from django.core.cache import cache
from address_book_app_be.settings import AUTH0_DOMAIN

class AuthorizationCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/auth'):
            return self.get_response(request)
        
        if os.environ.get('DJANGO_TESTING') == 'False':
            if 'Authorization' not in request.headers:
                print("Authorization header missing")
                return JsonResponse({'error': 'Unauthorized - No Authorization header'}, status=401)
            

            headers = {"Authorization": "Bearer "+request.headers['Authorization']}
            url = f'https://{AUTH0_DOMAIN}/userinfo'
            validateToken = requests.get(url, headers = headers)
            print(f"Auth0 response status: {validateToken.status_code}")
            if validateToken.status_code != 200:
                print("Invalid token detected")
                return JsonResponse({'error': 'Unauthorized - Invalid Token'}, status=401)
            

            userData = validateToken.json()

            request.user = {'id': userData['sub'], 'email': userData['email'], 'name': userData['name']}
        else:
            request.user = {'id': 'testuser', 'email': 'testuser@test.com', 'name': 'testuser'}
        # Continue processing the request if the header is present
        response = self.get_response(request) 
        
        return response
