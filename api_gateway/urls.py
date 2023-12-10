from django.urls import path, include
from .views import hello_world
from .views import fetch_random_user

urlpatterns = [
    path('hello/', hello_world),
    path('user/', fetch_random_user),
]