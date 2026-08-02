from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import case, func
from sqlmodel import Session, select
from app.database import get_session
from app.models import Produit, Mouvement, TypeMouvement

router = APIRouter(prefix="/produits", tags=["Mouvements"])


# -- l'URL dit : « crée un mouvement pour le produit {produit_id} --
@router.post("/{produit_id}/mouvements", response_model=Mouvement)
def creer_mouvement(
    produit_id: int,
    mouvement: Mouvement,
    session: Session = Depends(get_session),
):
    produit = session.get(Produit, produit_id)
    if produit is None:
        raise HTTPException(status_code=404, detail="Produit introuvable")

    if mouvement.quantite <= 0:
        raise HTTPException(status_code=400, detail="La quantité doit être positive")

    mouvement.produit_id = produit_id  # l'URL fait foi
    session.add(mouvement)
    session.commit()
    session.refresh(mouvement)
    return mouvement


# -- l'URL dit : « donne le stock courant du produit {produit_id} --
@router.get("/{produit_id}/stock")
def lire_stock(produit_id: int, session: Session = Depends(get_session)):
    produit = session.get(Produit, produit_id)
    if produit is None:
        raise HTTPException(status_code=404, detail="Produit introuvable")

    # +quantite pour une entrée, -quantite pour une sortie, sommés en SQL.
    signe = case(
        (Mouvement.type == TypeMouvement.entree, Mouvement.quantite),
        (Mouvement.type == TypeMouvement.sortie, -Mouvement.quantite),
        else_=0,
    )
    statement = select(func.sum(signe)).where(Mouvement.produit_id == produit_id)
    stock = session.exec(statement).one()

    return {"produit_id": produit_id, "stock": stock or 0}
