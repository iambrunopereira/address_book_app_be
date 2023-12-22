""" from django.test import TestCase
from unittest.mock import patch

from api_gateway.views.user_views import fetch_random_users

class FetchRandomUsersTests(TestCase):
    @patch('requests.get')
    def test_fetch_random_users_successful(self, mock_get):
        # Setup mock
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": [{"name": "John Doe"}]}

        # Call the function
        response_data = fetch_random_users(1)
        
        # Assertions
        self.assertEqual(response_data, [{"name": "John Doe"}]) """


from django.core.cache import cache
from django.http import JsonResponse

from django.test import TestCase, override_settings
from django.core.cache import cache
import requests_mock
import time

from api_gateway.views.user_views import fetch_random_users

@override_settings(CACHES={
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
})
class FetchRandomUsersTests(TestCase):
    def test_fetch_random_users_returns_data_from_cache(self):
        # Setup: Pre-populate cache with expected data
        expected_data = {'some': 'data'}
        cache.set('random_users_page_1', expected_data, 86400)


        result = fetch_random_users(1)


        self.assertEqual(result, expected_data)
    def test_fetch_random_users_api_call_and_caching_on_cache_miss(self):

        expected_data = {'results': [{'user': 'data'}]}
        with requests_mock.Mocker() as m:
            m.get('https://randomuser.me/api/?results=50&seed=addressbookApp&page=1', json=expected_data)

            result = fetch_random_users(1)

            self.assertEqual(result, expected_data['results'])

            cached_data = cache.get('random_users_page_1')
            self.assertEqual(cached_data, expected_data['results'])

