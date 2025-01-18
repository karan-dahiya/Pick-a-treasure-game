#
# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path('create/', views.create_game, name='create_game'),
#     path('pick/<str:player_name>/<int:row>/<int:col>/', views.pick_treasure, name='pick_treasure'),
# ]

# game/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_game, name='create_game'),  # Create and initialize the game
    path('game/', views.game_board, name='game_board'),  # Display game board and player scores
    path('game/player/<str:player_name>/', views.player_score, name='player_score'),  # Display individual player score
    path('game/pick/<str:player_name>/<int:row>/<int:col>/', views.pick_treasure, name='pick_treasure'),  # Handle player's move
]
