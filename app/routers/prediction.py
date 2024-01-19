from fastapi import APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

router = APIRouter()

#Lire et charger les types des pokémons
df_types = pd.read_csv("app/data/pokemon-types.csv")
types_pokemon = df_types.columns[1:].tolist()
types_pokemon = [type.capitalize() for type in types_pokemon]

#Lire et charger les noms des pokémons
df_pokemons = pd.read_csv("app/data/pokemons.csv")
pokemon_names = df_pokemons["name"].tolist()
pokemon_names = [name.capitalize() for name in pokemon_names]

@router.get("/get_pokemon_types")
def get_pokemon_types():
    return {"pokemon_types": types_pokemon}

@router.get("/get_pokemon_names")
def get_pokemon_names():
    return {"pokemon_names": pokemon_names}

@router.post("/send_prediction_result")
def send_selected_pokemons(data: dict):
    type1 = data.get("type1")
    type2 = data.get("type2")

    # Appeler la fonction pour comparer les Pokémon
    result = compare_pokemons(type1, type2)

    # Retourner la propriété 'result' dans la réponse
    return {"message": f"Types sélectionnés : {type1}, {type2}", "result": result.get("message", "")}


def compare_pokemons(type1: str, type2: str):
    # Convertir les noms de Pokémon en minuscules
    type1 = type1.lower()
    type2 = type2.lower()

    # Sélectionner les données noms des deux Pokémon
    pokemon1_data = df_pokemons[df_pokemons['name'] == type1]
    pokemon2_data = df_pokemons[df_pokemons['name'] == type2]

    if not pokemon1_data.empty and not pokemon2_data.empty:
        # Extraire les caractéristiques pertinentes pour la comparaison
        total_pokemon1 = pokemon1_data.iloc[0]['total']
        total_pokemon2 = pokemon2_data.iloc[0]['total']

        # Comparaison des caractéristiques
        if total_pokemon1 > total_pokemon2:
            message = f"{type1} est potentiellement plus fort que {type2}"
        elif total_pokemon1 < total_pokemon2:
            message = f"{type2} est potentiellement plus fort que {type1}"
        else:
            message = f"{type1} et {type2} sont potentiellement égaux en termes de force"

        return {"message": message}
    else:
        return {"message": f"Données pour {type1} ou {type2} introuvables. Vérifiez les noms des Pokémon."}
