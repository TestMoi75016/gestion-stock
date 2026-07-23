from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import creer_tables


@asynccontextmanager  # décorateur
async def lifespan(app: FastAPI):
    # Avant le yield : au démarrage du serveur
    creer_tables()
    yield
    # Après le yield : à l'extinction du serveur (rien à faire ici)


app = FastAPI(title="Gestion de stock", lifespan=lifespan)


@app.get("/")
async def racine():
    return {"message": "API de gestion de stock opérationnelle"}
