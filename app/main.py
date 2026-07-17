from fastapi import FastAPI

app = FastAPI(title="Gestion de stock")


@app.get("/")
async def racine():
    return {"message": "API de gestion de stock opérationnelle"}
