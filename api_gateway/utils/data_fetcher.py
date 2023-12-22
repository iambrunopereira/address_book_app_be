def process_user_data(user, search_term, gender, nat_filters):
    name_matches = True  
    if search_term:
        name_matches = search_term in f"{user['name']['first']} {user['name']['last']}".lower()
    
    if gender:
        gender = gender.lower()
        gender_matches = True if gender == 'all' else gender == user['gender']
    else:
        gender_matches = True

    nationality_matches = user['nat'] in nat_filters if nat_filters else True

    if name_matches and gender_matches and nationality_matches:
        return {
                    "id": user['login']['uuid'],
                    "picture": user['picture']['thumbnail'],
                    "fullName": f"{user['name']['first']} {user['name']['last']}",
                    "username": user['login']['username'],
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
    return None
