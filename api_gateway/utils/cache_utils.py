from django.http import JsonResponse
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def invalidate_cache():
    page_number = 1
    while int(page_number) <= 21:
        cache_key = f'random_users_page_{page_number}'
        cache.delete(cache_key)
        page_number += 1
    JsonResponse({'message': "cache cleared" })