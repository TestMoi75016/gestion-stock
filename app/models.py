from datetime import datetime, timezone
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship


# class TypeMouvement qui n'est pas une table. (pas de table=True)
class TypeMouvement(str, Enum):
    entree = "entree"
    sortie = "sortie"


# --- Table "Categories" ---
class Categorie(SQLModel, table=True):
    __tablename__ = "categories"  # sinon la table s'appellerait "categorie"

    id: int | None = Field(default=None, primary_key=True)
    nom: str
    produits: list["Produit"] = Relationship(
        back_populates="categorie"
    )  # list["Produit"] ça veut pour Python: tkt la table "Produit" n'est pas crée mais fait moi confiance ça arrive juste en dessous


# --- Table "fournisseurs" ---
class Fournisseur(SQLModel, table=True):
    __tablename__ = "fournisseurs"

    id: int | None = Field(default=None, primary_key=True)
    nom: str
    email: str | None = None  # optionnel

    produits: list["Produit"] = Relationship(
        back_populates="fournisseur"
    )  # list["Produit"] ça veut pour Python: tkt la table "Produit" n'est pas crée mais fait moi confiance ça arrive juste en dessous


# --- Table "produits" ---
class Produit(SQLModel, table=True):
    __tablename__ = "produits"

    id: int | None = Field(default=None, primary_key=True)
    nom: str
    sku: str = Field(index=True, unique=True)  # référence unique du produit
    seuil_alerte: int = Field(default=0)  # niveau bas déclenchant l'alerte

    # Clés étrangères : chaque produit pointe vers UNE catégorie, UN fournisseur.
    categorie_id: int | None = Field(default=None, foreign_key="categories.id")
    fournisseur_id: int | None = Field(default=None, foreign_key="fournisseurs.id")

    # Raccourcis seulement pour Python : depuis un produit, aller chercher
    # sa catégorie et son fournisseur sans écrire de requête.
    # Ne crée aucune colonne — s'appuie sur categorie_id / fournisseur_id.
    categorie: Categorie | None = Relationship(back_populates="produits")
    fournisseur: Fournisseur | None = Relationship(back_populates="produits")

    # Navigation vers les enfants : un produit a plusieurs mouvements.
    mouvements: list["Mouvement"] = Relationship(
        back_populates="produit"
    )  # list["Mouvement"] ça veut pour Python: tkt la table "Mouvement" n'est pas crée mais fait moi confiance ça arrive juste en dessous


# --- Table "mouvements" ---
class Mouvement(SQLModel, table=True):
    __tablename__ = "mouvements"

    id: int | None = Field(default=None, primary_key=True)
    produit_id: int = Field(foreign_key="produits.id")  # obligatoire
    type: TypeMouvement  # "entree" ou "sortie"
    quantite: int
    # default_factory (pas default !) : fonction appelée À CHAQUE création,
    # donc chaque mouvement reçoit l'heure de SON insertion.
    date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    note: str | None = None  # commentaire libre, optionnel

    produit: Produit | None = Relationship(back_populates="mouvements")
