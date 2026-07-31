from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.models import Produit, Mouvement

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
