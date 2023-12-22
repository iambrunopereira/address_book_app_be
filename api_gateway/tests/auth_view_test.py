from django.test import TestCase, Client
from unittest.mock import patch
import json

class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('requests.post')
    def test_login_success(self, mock_post):

        mock_response = {
            "access_token": "some_access_token",
            "id_token": "some_id_token"
        }
        mock_post.return_value.json.return_value = mock_response
        mock_post.return_value.status_code = 200

        data = {
            "email": "user@example.com",
            "password": "password123"
        }

        response = self.client.post('/api/auth/login', json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'data': mock_response})

    @patch('requests.post')
    def test_login_failure(self, mock_post):

        mock_post.return_value.json.return_value = {"error": "invalid_grant"}
        mock_post.return_value.status_code = 401

        data = {
            "email": "user@example.com",
            "password": "wrong_password"
        }

        response = self.client.post('/api/auth/login', json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn("error", response.json()['data'])
