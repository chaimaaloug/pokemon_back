# views.py

from django.http import JsonResponse
from .models import Pokemon, PokemonType
from django.shortcuts import render


# def compare_pokemons(request, pokemon_name_1, pokemon_name_2):
#     try:
#         # Récupérer les objets Pokémon en fonction des noms
#         pokemon1 = Pokemon.objects.get(name__iexact=pokemon_name_1)
#         pokemon2 = Pokemon.objects.get(name__iexact=pokemon_name_2)
        
#         # Ici, vous pouvez ajouter votre logique de comparaison, par exemple :
#         # comparer les statistiques totales de chaque Pokémon
#         total_stats_comparison = pokemon1.total_stats > pokemon2.total_stats
        
#         # Construire le dictionnaire de données pour la réponse JSON
#         data = {
#             'pokemon1': {
#                 'name': pokemon1.name,
#                 'total_stats': pokemon1.total_stats,
#             },
#             'pokemon2': {
#                 'name': pokemon2.name,
#                 'total_stats': pokemon2.total_stats,
#             },
#             'comparison_result': total_stats_comparison
#         }
        
#         # Retourner les résultats en JSON
#         return JsonResponse(data)
    
#     except Pokemon.DoesNotExist:
#         # Si l'un des Pokémon n'est pas trouvé, retourner une erreur
#         return JsonResponse({'error': 'L\'un des Pokémon n\'a pas été trouvé.'}, status=404)


def prediction(request):
    context = {'pokemon_types': PokemonType.objects.all()}  # Ajoutez ceci pour passer les types de Pokémon
    if request.method == 'POST':
        type1_name = request.POST.get('type1')
        type2_name = request.POST.get('type2')
        type1 = PokemonType.objects.get(name=type1_name)
        type2 = PokemonType.objects.get(name=type2_name)

        if type2 in type1.strong_against.all():
            context['result'] = f"{type1_name} gagne contre {type2_name}"
        elif type1 in type2.strong_against.all():
            context['result'] = f"{type2_name} gagne contre {type1_name}"
        else:
            context['result'] = "C'est un match nul"

    return render(request, 'prediction.html', context)