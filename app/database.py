from sqlmodel import SQLModel, create_engine, Session

# force Python à lire models.py, ce qui inscrit les classes dans le registre SQLModel.metadata:
from app.models import Categorie, Fournisseur, Produit, Mouvement

fichier_base = "database.db"
url_base = f"sqlite:///{fichier_base}"

engine = create_engine(url_base, echo=True, connect_args={"check_same_thread": False})


def creer_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
