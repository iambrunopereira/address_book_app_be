import os
from django.test import TestCase, override_settings
from django.http import HttpRequest, JsonResponse
import requests_mock
from address_book_app_be.settings import AUTH0_DOMAIN
from api_gateway.middleware.auth_middleware import AuthorizationCheckMiddleware
@override_settings(AUTH0_DOMAIN=f'https://{AUTH0_DOMAIN}/')
class AuthorizationCheckMiddlewareTests(TestCase):

    def setUp(self):
        self.middleware = AuthorizationCheckMiddleware(get_response=lambda request: JsonResponse({'message': 'success'}))
        self.request = HttpRequest()

    def test_path_exclusion(self):
        self.request.path = '/api/auth/somepath'
        response = self.middleware(self.request)
        self.assertEqual(response.status_code, 200)  # Assuming successful processing

    @override_settings(DJANGO_TESTING='True')
    def test_environment_variable_for_testing(self):
        response = self.middleware(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.request.user['name'], 'testuser')

    def test_missing_authorization_header(self):
        os.environ['DJANGO_TESTING'] = 'False'
        self.request.path = '/some/other/path'
        response = self.middleware(self.request)
        self.assertEqual(response.status_code, 401)
        os.environ['DJANGO_TESTING'] = 'True'
 
    def test_invalid_authorization_header(self):
        os.environ['DJANGO_TESTING'] = 'False'
        print(os.environ.get('DJANGO_TESTING'))
        with requests_mock.Mocker() as m:
            # Mock the Auth0 request to return a 401 status code
            m.get(f'https://{AUTH0_DOMAIN}/userinfo', status_code=401)

            print(f'https://{AUTH0_DOMAIN}/userinfo')
            print(f"Mocked URL: {m.last_request}")

            # Set up the request with an invalid authorization header
            self.request.META['HTTP_AUTHORIZATION'] = 'Bearer InvalidToken'
            self.request.path = '/api/search'
            print(f"Request Authorization Header: {self.request.META['HTTP_AUTHORIZATION']}")
            # Process the request through the middleware
            response = self.middleware(self.request)
            print(f"Response Status Code: {response.status_code}")
            # Assert that a 401 Unauthorized response is returned
            self.assertEqual(response.status_code, 401)
            os.environ['DJANGO_TESTING'] = 'True'
