from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import Categorie

router = APIRouter(prefix="/categories", tags=["Categories"])


# ---route creer une categorie -
@router.post("", response_model=Categorie)
def creer_categorie(categorie: Categorie, session: Session = Depends(get_session)):
    session.add(categorie)
    session.commit()
    session.refresh(categorie)
    return categorie


# ---route lister toutes les categories -
@router.get("", response_model=list[Categorie])
def lister_categories(session: Session = Depends(get_session)):
    categories = session.exec(select(Categorie)).all()
    return categories


# ---route lister une categorie en particulier -
@router.get("/{categorie_id}", response_model=Categorie)
def lire_categorie(categorie_id: int, session: Session = Depends(get_session)):
    categorie = session.get(Categorie, categorie_id)
    if categorie is None:
        raise HTTPException(status_code=404, detail="Categorie introuvable")
    return categorie


# ---route modifier une categorie en particulier -
@router.put("/{categorie_id}", response_model=Categorie)
def modifier_categorie(
    categorie_id: int, categorie_maj: Categorie, session: Session = Depends(get_session)
):
    categorie = session.get(Categorie, categorie_id)
    if categorie is None:
        raise HTTPException(status_code=404, detail="Categorie introuvable")
    donnees = categorie_maj.model_dump(exclude_unset=True)
    categorie.sqlmodel_update(donnees)
    session.add(categorie)
    session.commit()
    session.refresh(categorie)
    return categorie


# ---route supprimer une categorie en particulier -
@router.delete("/{categorie_id}")
def supprimer_categorie(categorie_id: int, session: Session = Depends(get_session)):
    categorie = session.get(Categorie, categorie_id)
    if categorie is None:
        raise HTTPException(status_code=404, detail="Categorie introuvable")
    session.delete(categorie)
    session.commit()
    return {"ok": True}
