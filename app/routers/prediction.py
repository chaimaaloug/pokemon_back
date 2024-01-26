from fastapi import APIRouter, HTTPException
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from fastapi.responses import FileResponse
import os

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
            "Type1": pokemon_data.iloc[0]['type1'],
            "Type2": convert_numpy_types(pokemon_data.iloc[0]['type2']) if not pd.isnull(pokemon_data.iloc[0]['type2']) else "",
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
            message = f"{type1} est potentiellement plus fort que {type2} de { total_pokemon1 - total_pokemon2 } points"
        elif total_pokemon1 < total_pokemon2:
            message = f"{type2} est potentiellement plus fort que {type1} de { total_pokemon2 - total_pokemon1 } points"
        else:
            message = f"{type1} et {type2} sont potentiellement égaux en termes de force"

        return {"message": message}
    else:
        return {"message": f"Données pour {type1} ou {type2} introuvables. Vérifiez les noms des Pokémon."}

# Supposez que df_pokemons contient toutes les données des Pokémon
def get_pokemon_stats(pokemon_name):
    pokemon_data = df_pokemons[df_pokemons['name'] == pokemon_name.lower()]

    if not pokemon_data.empty:
        stats_data = {
            "HP": int(pokemon_data.iloc[0]['hp']),
            "Attack": int(pokemon_data.iloc[0]['atk']),
            "Defense": int(pokemon_data.iloc[0]['def']),
            "Special Attack": int(pokemon_data.iloc[0]['spatk']),
            "Special Defense": int(pokemon_data.iloc[0]['spdef']),
            "Speed": int(pokemon_data.iloc[0]['speed']),
        }
        return stats_data
    else:
        raise HTTPException(status_code=404, detail=f"Pokémon not found: {pokemon_name}")


@router.get("/get_stats_chart/{pokemon_name}")
def get_stats_chart(pokemon_name: str):

    stats_data = get_pokemon_stats(pokemon_name)

    # Créer le graphique avec Matplotlib
    labels = ['HP', 'Attaque', 'Défense', 'Vitesse']
    values = [stats_data['HP'], stats_data['Attack'], stats_data['Defense'], stats_data['Speed']]

    # Définir des couleurs spécifiques pour chaque statistique
    colors = ['#159F8D', '#EC7147', '#5DB9FF', '#FBD643']

    fig, ax = plt.subplots()
    bars = ax.bar(labels, values, color=colors)

    # Ajouter les valeurs à l'intérieur de chaque barre
    for bar, value in zip(bars, values):
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, yval, round(value, 2), ha='center', va='bottom')

    save_directory = 'static/media'
    
    try:
        os.makedirs(save_directory, exist_ok=True)
    except OSError as e:
        print(f"Error creating directory: {e}")

    image_path = f'{save_directory}/{pokemon_name}_stats_chart.png'
    fig.savefig(image_path)
    
    plt.close()

    # Renvoyer l'image au frontend
    return FileResponse(image_path, media_type="image/png")


@router.get("/get_stats_radar_chart/{pokemon_name}")
async def get_stats_chart(pokemon_name: str):
    pokemon_data = df_pokemons[df_pokemons['name'] == pokemon_name.lower()]

    pokemon_stats = {
        "HP": int(pokemon_data.iloc[0]['hp']),
        "Attack": int(pokemon_data.iloc[0]['atk']),
        "Defense": int(pokemon_data.iloc[0]['def']),
        "Special Attack": int(pokemon_data.iloc[0]['spatk']),
        "Special Defense": int(pokemon_data.iloc[0]['spdef']),
        "Speed": int(pokemon_data.iloc[0]['speed']),
    }

    labels = list(pokemon_stats.keys())
    values = list(pokemon_stats.values())
    num_stats = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_stats, endpoint=False).tolist()

    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='red', alpha=0.25)

    # labels and title
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    save_directory = 'static/media'
    try:
        os.makedirs(save_directory, exist_ok=True)
    except OSError as e:
        print(f"Erreur: {e}")

    image_path = f'{save_directory}/{pokemon_name}_stats_radar_chart.png'
    fig.savefig(image_path)
    plt.close()

    return FileResponse(image_path, media_type="image/png")