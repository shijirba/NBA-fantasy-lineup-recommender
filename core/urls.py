from django.urls import path
from .views import player_list, find, player_compare

urlpatterns = [
    path('', player_list, name='home'),
    path('compare', player_compare, name='compare'), 
    path('find', find, name='find'), 
]