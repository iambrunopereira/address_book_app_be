
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from api_gateway.models.favorites import Favorite

from api_gateway.utils.data_fetcher import process_user_data

api_url = f'https://randomuser.me/api/?results=50&seed=addressbookApp'

@csrf_exempt
def fetch_random_users(page_number):

    cache_key = f'random_users_page_{page_number}'
    cache_time = 86400  


    data = cache.get(cache_key)

    
    if not data:

        response = requests.get(api_url + f'&page={page_number}')
        if response.status_code == 200:
            data = response.json().get('results', [])


            cache.set(cache_key, data, cache_time)
        else:
            return JsonResponse({'error': 'Failed to fetch data'}, status=response.status_code)
   
    return data

@csrf_exempt
def search_and_fetch(request):

    search_term = request.GET.get('name', '').lower()
    gender = request.GET.get('gender', '')
    nat_params = request.GET.get('nat', '').split(',')
    page = int(request.GET.get('nextPage', 1))
    nat_filters = sorted([nat.upper() for nat in nat_params if nat])
    

    current_search_params = f"{search_term}-{gender}-{''.join(nat_filters)}"


    if current_search_params != request.session.get('last_search_params', ''):

        request.session['last_page'] = 1
        request.session['last_position'] = 0


    request.session['last_search_params'] = current_search_params
    request.session['last_search_term'] = search_term
    request.session['last_gender'] = gender

    last_position = request.session.get('last_position', 0)
    accumulated_results = []
    
    
    while len(accumulated_results) < 50:

        if page > 20:

            return JsonResponse({'data': accumulated_results, "total": len(accumulated_results), "moreData": False, "nextPage": 1 })
        

        users = fetch_random_users(page)
        
        with ThreadPoolExecutor(max_workers=100) as executor:
                future_to_user = {executor.submit(process_user_data, user, search_term, gender, nat_filters): user for user in users}
                for future in as_completed(future_to_user):
                    result = future.result()
                    if result:
                        accumulated_results.append(result)
                    if len(accumulated_results) >= 50:
                        break

        
        page += 1
        last_position = 0  

    request.session['last_page'] = page
    request.session['last_position'] = 0  
    return JsonResponse({'data': accumulated_results, "total": len(accumulated_results), "moreData": True, "nextPage": page})

def handle_fetch_user(listUserIds):

        page = 1
        accumulated_results = []
        print(listUserIds)

        while len(accumulated_results) < len(listUserIds):

            if page > 20:
                return {'data': accumulated_results, "total": len(accumulated_results) }
          
            users = fetch_random_users(page)

            for i, user in enumerate(users):
                id_matches = user['login']['uuid'] in listUserIds if listUserIds else True
                if id_matches:
                    user_info = {
                        "id": user['login']['uuid'],
                        "picture": user['picture']['thumbnail'],
                        "fullName": f"{user['name']['first']} {user['name']['last']}",
                        "firstName": user['name']['first'],
                        "lastName": user['name']['last'],
                        "email": user['email'],
                        "phone": user['phone'],
                        "cell": user['cell'],
                        "gender": user['gender'],
                        "address": {
                            "street": user['location']['street']['number'],
                            "city": user['location']['city'],
                            "state": user['location']['state'],
                            "country": user['location']['country'],
                            "postcode": user['location']['postcode'],
                        },
                        "nat": user['nat']
                    }
                    accumulated_results.append(user_info)

                if len(accumulated_results) == len(listUserIds):
                    return {'data': accumulated_results, "total": len(accumulated_results) }

            page += 1
            
        return {'error': 'No favorites available'}

@csrf_exempt
def get_favorites(request):
    account_id = request.user.get('id')

    user_uuids = Favorite.get_favorite_user_uuids(account_id)
    users_data = handle_fetch_user(user_uuids)

    return JsonResponse(users_data)


def fetch_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        listUserIds = data.get('ids')
        
        response = handle_fetch_user(listUserIds)
            
        return JsonResponse(response)
    

@csrf_exempt
def add_to_favorites(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

    body = json.loads(request.body)
    print(body)
    user_id = body.get('user_id')
    account_id = request.user.get('id')

    print(account_id, user_id)


    if Favorite.objects.filter(account_id=account_id, user_id=user_id).exists():
        return JsonResponse({'status': 'error', 'message': 'Favorite already exists'})

    Favorite.objects.create(account_id=account_id, user_id=user_id)
    return JsonResponse({'status': 'success', 'message': 'Favorite added'})

@csrf_exempt
def remove_from_favorites(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

    body = json.loads(request.body)
    user_id = body.get('user_id')
    account_id = request.user.get('id')


    favorite = Favorite.objects.filter(account_id=account_id, user_id=user_id)
    if not favorite.exists():
        return JsonResponse({'status': 'error', 'message': 'Favorite not found'})


    favorite.delete()
    return JsonResponse({'status': 'success', 'message': 'Favorite removed'})
