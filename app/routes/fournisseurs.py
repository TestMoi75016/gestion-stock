from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import Fournisseur

router = APIRouter(prefix="/fournisseurs", tags=["Fournisseurs"])


# ---route creer un fournisseur -
@router.post("", response_model=Fournisseur)
def creer_fournisseur(fournisseur: Fournisseur, session: Session = Depends(get_session)):
    session.add(fournisseur)
    session.commit()
    session.refresh(fournisseur)
    return fournisseur


# ---route lister tous les fournisseurs -
@router.get("", response_model=list[Fournisseur])
def lister_fournisseurs(session: Session = Depends(get_session)):
    fournisseurs = session.exec(select(Fournisseur)).all()
    return fournisseurs


# ---route lister un fournisseur en particulier -
@router.get("/{fournisseur_id}", response_model=Fournisseur)
def lire_fournisseur(fournisseur_id: int, session: Session = Depends(get_session)):
    fournisseur = session.get(Fournisseur, fournisseur_id)
    if fournisseur is None:
        raise HTTPException(status_code=404, detail="Fournisseur introuvable")
    return fournisseur


# ---route modifier un fournisseur en particulier -
@router.put("/{fournisseur_id}", response_model=Fournisseur)
def modifier_fournisseur(
    fournisseur_id: int, fournisseur_maj: Fournisseur, session: Session = Depends(get_session)
):
    fournisseur = session.get(Fournisseur, fournisseur_id)
    if fournisseur is None:
        raise HTTPException(status_code=404, detail="Fournisseur introuvable")
    donnees = fournisseur_maj.model_dump(exclude_unset=True)
    fournisseur.sqlmodel_update(donnees)
    session.add(fournisseur)
    session.commit()
    session.refresh(fournisseur)
    return fournisseur


# ---route supprimer un fournisseur en particulier -
@router.delete("/{fournisseur_id}")
def supprimer_fournisseur(fournisseur_id: int, session: Session = Depends(get_session)):
    fournisseur = session.get(Fournisseur, fournisseur_id)
    if fournisseur is None:
        raise HTTPException(status_code=404, detail="Fournisseur introuvable")
    session.delete(fournisseur)
    session.commit()
    return {"ok": True}
