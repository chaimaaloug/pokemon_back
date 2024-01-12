# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('compare/<str:pokemon_name_1>/<str:pokemon_name_2>/', views.compare_pokemons, name='compare_pokemons'),
    # Ajoutez d'autres URLs ici
]
