from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import Produit

router = APIRouter(prefix="/produits", tags=["Produits"])


# ---route creer un produit -
@router.post("", response_model=Produit)
def creer_produit(produit: Produit, session: Session = Depends(get_session)):
    session.add(produit)
    session.commit()
    session.refresh(produit)
    return produit


# ---route lister tous les produits -
@router.get("", response_model=list[Produit])
def lister_produits(session: Session = Depends(get_session)):
    produits = session.exec(select(Produit)).all()
    return produits


# ---route lister un produit en particulier -
@router.get("/{produit_id}", response_model=Produit)
def lire_produit(produit_id: int, session: Session = Depends(get_session)):
    produit = session.get(Produit, produit_id)
    if produit is None:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    return produit


# ---route modifier un produit en particulier -
@router.put("/{produit_id}", response_model=Produit)
def modifier_produit(
    produit_id: int, produit_maj: Produit, session: Session = Depends(get_session)
):
    produit = session.get(Produit, produit_id)
    if produit is None:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    donnees = produit_maj.model_dump(exclude_unset=True)
    produit.sqlmodel_update(donnees)
    session.add(produit)
    session.commit()
    session.refresh(produit)
    return produit


# ---route supprimer un produit en particulier -
@router.delete("/{produit_id}")
def supprimer_produit(produit_id: int, session: Session = Depends(get_session)):
    produit = session.get(Produit, produit_id)
    if produit is None:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    session.delete(produit)
    session.commit()
    return {"ok": True}
