from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Enable CORS for all origins
app = FastAPI()

@app.post("/predict")
def predict(data: dict):
    prediction = {"result": "La prédiction de Pokémon"}
    return prediction

@app.get("/get_predict")
def get_prediction():
    return {"message": "Get prédiction de Pokémon"}
