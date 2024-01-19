from fastapi import APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

router = APIRouter()

#Lire et charger les types des pokémons
df = pd.read_csv("app/data/pokemon-types.csv")
types_pokemon = df.columns[1:].tolist()
types_pokemon = [type.capitalize() for type in types_pokemon]

#Lire et charger les noms des pokémons
df = pd.read_csv("app/data/pokemons.csv")
pokemon_names = df["name"].tolist()

@router.get("/get_pokemon_types")
def get_pokemon_types():
    return {"pokemon_types": types_pokemon}

@router.get("/get_pokemon_names")
def get_pokemon_types():
    return {"pokemon_names": pokemon_names}

@router.post("/send_selected_pokemons")
def valider_pokemon(data: dict):
    type1 = data.get("type1")
    type2 = data.get("type2")

    return {"message": f"Types sélectionnés : {type1}, {type2}"}