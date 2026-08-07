from fastapi import APIRouter, Depends
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
