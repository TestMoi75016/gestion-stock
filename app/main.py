from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import creer_tables
from app.routes import produits


@asynccontextmanager  # décorateur: transforme la fonction en gestionnaire de cycle de vie (démarrage/arrêt de l'application)
async def lifespan(app: FastAPI):
    # Avant le yield : au démarrage du serveur: code exécuté au démarrage (ici creer_tables() crée les tables si elles n'existent pas).
    creer_tables()
    yield  # indique à FastAPI de démarrer l'application et de traiter les requêtes
    # Après yield : code exécuté à l'arrêt du serveur (ici il n'y en a pas)


app = FastAPI(title="Gestion de stock", lifespan=lifespan)

# accroche le porte-routes à l'application. C'est la ligne qui « active » mes trois routes.
app.include_router(produits.router)


@app.get("/")
async def racine():
    return {"message": "API de gestion de stock opérationnelle"}
