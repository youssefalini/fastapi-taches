from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship  # <--- L'outil magique de liaison
from database import Base


# # Cette classe Python = La table SQL "tasks"
# class TacheModel(Base):
#     __tablename__ = "tasks"  # Le nom de la table dans la DB


#     # Voici les colonnes
#     id = Column(Integer, primary_key=True, index=True)
#     titre = Column(String, index=True)
#     # On ajoute un petit bonus pour le futur : savoir si c'est fini ou pas
#     est_fini = Column(Boolean, default=False)
class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(
        String, unique=True, index=True
    )  # unique=True : Interdit les doublons d'email
    hashed_password = Column(
        String
    )  # On stockera le mot de passe ici (crypté plus tard)

    # La Relation : "Mes tâches sont..."
    # back_populates="owner" signifie : "Regarde la variable 'owner' dans l'autre table pour comprendre"
    tasks = relationship("TacheModel", back_populates="owner")


# --- LA TABLE TÂCHE MODIFIÉE ---
class TacheModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String, index=True)
    est_fini = Column(Boolean, default=False)

    # 1. La Clé Étrangère (Le Badge)
    # Elle stocke l'ID de l'utilisateur (ex: 1, 42, 99)
    # "users.id" fait référence à la table "users", colonne "id"
    owner_id = Column(Integer, ForeignKey("users.id"))

    # 2. La Relation (L'Objet)
    # Permet d'accéder à l'objet utilisateur complet via 'tache.owner'
    owner = relationship("UserModel", back_populates="tasks")
