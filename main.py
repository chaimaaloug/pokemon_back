from fastapi import FastAPI

app = FastAPI()

@app.post("/predict")
def predict(data: dict):
    # Here, you handle POST requests
    # ...

    prediction = {"result": "La prédiction de Pokémon"}
    return prediction

@app.get("/get_predict")
def get_prediction():
 
    return {"message": "Get prédiction de Pokémon"}
