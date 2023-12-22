import os
from django.test import RequestFactory, TestCase
from django.urls import reverse
from unittest.mock import patch
from django.contrib.sessions.middleware import SessionMiddleware
from api_gateway.views.user_views import search_and_fetch


class SearchAndFetchTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def add_session_to_request(self, request):
        """Add a session to a test request."""
        middleware = SessionMiddleware(lambda x: x)
        middleware.process_request(request)
        request.session.save()

    def test_search_and_fetch_with_no_parameters(self):
        request = self.factory.get('/search')
        self.add_session_to_request(request)  # Add a session to the request
        response = search_and_fetch(request)
        self.assertEqual(response.status_code, 200)

    @patch('api_gateway.views.user_views.fetch_random_users')
    def test_search_and_fetch(self, mock_fetch_random_users):
        # Setup mock
        
        mock_fetch_random_users.return_value = [{
            "gender": "male",
            "name": {
                "title": "Mr",
                "first": "Danilo",
                "last": "Naydich"
            },
            "location": {
                "street": {
                    "number": 8187,
                    "name": "Kazanska"
                },
                "city": "Derazhnya",
                "state": "Volinska",
                "country": "Ukraine",
                "postcode": 40619,
                "coordinates": {
                    "latitude": "79.5008",
                    "longitude": "-20.0728"
                },
                "timezone": {
                    "offset": "-12:00",
                    "description": "Eniwetok, Kwajalein"
                }
            },
            "email": "danilo.naydich@example.com",
            "login": {
                "uuid": "490d6415-fe0c-423b-8953-f95fa3999596",
                "username": "goldendog962",
                "password": "mahler",
                "salt": "73cVkoSU",
                "md5": "eb8dc4baeeb761141296e8f56f7206d8",
                "sha1": "ea36831d13994b531ccbc4cf4c8df184ebf48820",
                "sha256": "188da84294cc30e6264f4151bda63634184e9e4701ac21bbc1fc71b690bdd27d"
            },
            "dob": {
                "date": "1977-10-03T10:21:02.812Z",
                "age": 46
            },
            "registered": {
                "date": "2009-09-25T16:13:57.468Z",
                "age": 14
            },
            "phone": "(097) F56-5364",
            "cell": "(066) L97-3206",
            "id": {
                "name": "",
                "value": "NULL"
            },
            "picture": {
                "large": "https://randomuser.me/api/portraits/men/98.jpg",
                "medium": "https://randomuser.me/api/portraits/med/men/98.jpg",
                "thumbnail": "https://randomuser.me/api/portraits/thumb/men/98.jpg"
            },
            "nat": "UA"
        }]

        # Make a GET request to the view
        response = self.client.get('/api/search', {'name': 'Danilo Naydich', 'gender': 'male', 'nat': 'ua', 'nextPage': 20})
        
        self.maxDiff = None
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'data': [{
            "id": "490d6415-fe0c-423b-8953-f95fa3999596",
            "picture": "https://randomuser.me/api/portraits/thumb/men/98.jpg",
            "fullName": "Danilo Naydich",
            "username": "goldendog962",
            "firstName": "Danilo",
            "lastName": "Naydich",
            "email": "danilo.naydich@example.com",
            "phone": "(097) F56-5364",
            "cell": "(066) L97-3206",
            "gender": "male",
            "address": {
                "street": 8187,
                "city": "Derazhnya",
                "state": "Volinska",
                "country": "Ukraine",
                "postcode": 40619
            },
            "nat": "UA"
        }], "total": 1, "moreData": False, "nextPage": 1})
        mock_fetch_random_users.assert_called_once_with(20)

