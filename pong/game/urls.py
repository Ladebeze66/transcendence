# /pong/game/urls.py

from django.urls import path, include
from . import views
from .views import player_list, tournoi_list, match_list
from rest_framework.routers import DefaultRouter
from .views import match_list_json
from .views import player_list_json



urlpatterns = [
    path('', views.index, name='index'),
    path('check_user_exists/', views.check_user_exists, name='check_user_exists'),
    path('register_user/', views.register_user, name='register_user'),
    path('authenticate_user/', views.authenticate_user, name='authenticate_user'),
    path('players/', player_list, name='player_list'),
    path('matches/', match_list, name='match_list'),
    path('tournois/', tournoi_list, name='tournoi_list'),
    path('api/match_list/', match_list_json, name='match_list_json'),
    path('api/player_list/', player_list_json, name='player_list_json'),
]
