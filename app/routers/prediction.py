from fastapi import APIRouter, HTTPException
import numpy as np
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

#Récupérer les informations d'un pokémon
@router.get("/get_pokemon_details/{pokemon_name}")
def get_pokemon_details(pokemon_name: str):

    pokemon_data = df_pokemons[df_pokemons['name'] == pokemon_name.lower()]

    if not pokemon_data.empty:
        def convert_numpy_types(value):
            if isinstance(value, np.int64):
                return int(value)
            return value

        pokemon_details = {
            "Name": pokemon_data.iloc[0]['name'],
            "Type 1": pokemon_data.iloc[0]['type1'],
            "HP": convert_numpy_types(pokemon_data.iloc[0]['hp']),
            "Attack": convert_numpy_types(pokemon_data.iloc[0]['atk']),
            "Defense": convert_numpy_types(pokemon_data.iloc[0]['def']),
            "Special Attack": convert_numpy_types(pokemon_data.iloc[0]['spatk']),
            "Special Defense": convert_numpy_types(pokemon_data.iloc[0]['spdef']),
            "Speed": convert_numpy_types(pokemon_data.iloc[0]['speed']),
            "Height": convert_numpy_types(pokemon_data.iloc[0]['height']),
            "Weight": convert_numpy_types(pokemon_data.iloc[0]['weight']),
            "Abilities": convert_numpy_types(pokemon_data.iloc[0]['abilities']),
            "Description": convert_numpy_types(pokemon_data.iloc[0]['desc'])
        }

        return {"pokemon_details": pokemon_details}
    else:
        raise HTTPException(status_code=404, detail=f"Pokémon not found: {pokemon_name}")

@router.post("/send_prediction_result")
def send_selected_pokemons(data: dict):
    type1 = data.get("type1")
    type2 = data.get("type2")

    result = compare_pokemons(type1, type2)
    return {"message": f"Types sélectionnés : {type1}, {type2}", "result": result.get("message", "")}

def compare_pokemons(type1: str, type2: str):

    type1 = type1.lower()
    type2 = type2.lower()

    pokemon1_data = df_pokemons[df_pokemons['name'] == type1]
    pokemon2_data = df_pokemons[df_pokemons['name'] == type2]

    if not pokemon1_data.empty and not pokemon2_data.empty:
        total_pokemon1 = pokemon1_data.iloc[0]['total']
        total_pokemon2 = pokemon2_data.iloc[0]['total']

        if total_pokemon1 > total_pokemon2:
            message = f"{type1} est potentiellement plus fort que {type2}"
        elif total_pokemon1 < total_pokemon2:
            message = f"{type2} est potentiellement plus fort que {type1}"
        else:
            message = f"{type1} et {type2} sont potentiellement égaux en termes de force"

        return {"message": message}
    else:
        return {"message": f"Données pour {type1} ou {type2} introuvables. Vérifiez les noms des Pokémon."}
