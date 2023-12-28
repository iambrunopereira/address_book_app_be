from django.urls import path, include

from api_gateway.views import user_views
from api_gateway.views import auth_views



urlpatterns = [
    path('user', user_views.fetch_user),
    path('search', user_views.search_and_fetch),
    path('user/add', user_views.add_to_favorites),
    path('user/remove', user_views.remove_from_favorites),
    path('user/favorites', user_views.get_favorites),
    path('auth/login', auth_views.login),
    path('auth/signup', auth_views.signup),
    path('auth/change-password', auth_views.change_password),
]