
from fastapi import FastAPI, Query, HTTPException
import requests

app = FastAPI()

url = "https://guilhermeonrails.github.io/api-restaurantes/restaurantes.json"


@app.get("/api/hello")
def hello_world():
    return {"Hello": "World"}


@app.get("/api/restaurantes/")
def get_restaurantes(restaurante: str | None = Query(default=None)):
    response = requests.get(url, timeout=30)

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail="Não foi possível buscar os dados dos restaurantes."
        )

    dados_json = response.json()

    if restaurante is None:
        return {"Dados": dados_json}

    dados_restaurante = []

    for item in dados_json:
        if item["Company"].casefold() == restaurante.casefold():
            dados_restaurante.append({
                "item": item["Item"],
                "price": item["price"],
                "description": item["description"]
            })

    if not dados_restaurante:
        raise HTTPException(
            status_code=404,
            detail="Restaurante não encontrado."
        )

    return {"Restaurante": restaurante, "Cardapio": dados_restaurante}
