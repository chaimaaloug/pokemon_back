from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.routers import prediction
app = FastAPI()

app.include_router(prediction.router)

#------ Enable CORS for all origins --------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
def predict(data: dict):
    prediction = {"result": "La prédiction de Pokémon"}
    return prediction

@app.get("/get_predict")
def get_prediction():
    return {"message": "Get prédiction de Pokémon"}

