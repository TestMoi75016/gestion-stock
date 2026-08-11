from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import case, func
from sqlmodel import Session, select

from app.database import get_session
from app.models import Mouvement, Produit, TypeMouvement

router = APIRouter(prefix="/rapports", tags=["Rapports"])


# ---route calculer la valeur totale du stock -
@router.get("/valeur-stock")
def lire_valeur_stock(session: Session = Depends(get_session)):
    signe = case(
        (Mouvement.type == TypeMouvement.entree, Mouvement.quantite),
        (Mouvement.type == TypeMouvement.sortie, -Mouvement.quantite),
        else_=0,
    )
    valeur_totale = func.coalesce(func.sum(Produit.prix * signe), 0)
    statement = select(valeur_totale).join(
        Mouvement, Mouvement.produit_id == Produit.id, isouter=True
    )
    resultat = session.exec(statement).one()
    return {"valeur_totale": resultat}


# ---route lister les mouvements sur une période -
@router.get(
    "/mouvements",
    responses={
        400: {
            "description": "La date de début doit être antérieure ou égale à la date de fin."
        }
    },
)
def lire_mouvements(
    debut: datetime, fin: datetime, session: Session = Depends(get_session)
):
    if debut > fin:
        raise HTTPException(
            status_code=400,
            detail="La date de début doit être antérieure ou égale à la date de fin.",
        )
    statement = (
        select(
            Mouvement
        )  # Mouvement (majuscule) = la classe (le moule), importée en haut du fichier : from app.models import Mouvement
        .where(Mouvement.date >= debut, Mouvement.date <= fin)
        .order_by(Mouvement.date)
    )
    mouvements = session.exec(statement).all()
    return mouvements
