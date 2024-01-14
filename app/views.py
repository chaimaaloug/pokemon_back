# views.py

from django.http import JsonResponse
from .models import Pokemon, PokemonType

def compare_pokemons(request, pokemon_name_1, pokemon_name_2):
    try:
        # Récupérer les objets Pokémon en fonction des noms
        pokemon1 = Pokemon.objects.get(name__iexact=pokemon_name_1)
        pokemon2 = Pokemon.objects.get(name__iexact=pokemon_name_2)
        
        # Ici, vous pouvez ajouter votre logique de comparaison, par exemple :
        # comparer les statistiques totales de chaque Pokémon
        total_stats_comparison = pokemon1.total_stats > pokemon2.total_stats
        
        # Construire le dictionnaire de données pour la réponse JSON
        data = {
            'pokemon1': {
                'name': pokemon1.name,
                'total_stats': pokemon1.total_stats,
            },
            'pokemon2': {
                'name': pokemon2.name,
                'total_stats': pokemon2.total_stats,
            },
            'comparison_result': total_stats_comparison
        }
        
        # Retourner les résultats en JSON
        return JsonResponse(data)
    
    except Pokemon.DoesNotExist:
        # Si l'un des Pokémon n'est pas trouvé, retourner une erreur
        return JsonResponse({'error': 'L\'un des Pokémon n\'a pas été trouvé.'}, status=404)
