from django.urls import path
from .views import player_list, find, compare, compare_player, rank, prediction

urlpatterns = [
    path('', player_list, name='home'),
    path('compare', compare, name='compare'), 
    path('compare-player', compare_player, name='compare-player'), 
    path('find', find, name='find'), 
    path('rank', rank, name='rank'), 
    path('prediction', prediction, name='prediction'), 
]
