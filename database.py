# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base

# # 1. L'adresse de la base de données
# # C'est la même qu'avant, mais avec un préfixe spécial pour SQLAlchemy
# SQLALCHEMY_DATABASE_URL = "sqlite:///./todo.db"

# # 2. Création du Moteur (The Engine)
# # connect_args={"check_same_thread": False} est nécessaire uniquement pour SQLite
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

# # 3. La Session (L'usine à connexions)
# # Chaque fois qu'on voudra parler à la base, on demandera une "Session" à cette usine.
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # 4. La Base (Le patron)
# # Toutes nos futures tables (Tâches, Utilisateurs...) hériteront de cette classe.
# Base = declarative_base()
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

# 1. On charge le fichier .env (s'il existe, donc sur ton PC)
load_dotenv()
# 2. On récupère la variable sécurisée.
# Si on est sur Koyeb, il la trouvera dans ses réglages.
# Si on est sur PC, il la trouvera dans le fichier .env
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Petit filet de sécurité : si la variable est vide, on prévient
if not SQLALCHEMY_DATABASE_URL:
    raise ValueError(
        "Pas de DATABASE_URL trouvée ! Vérifiez vos variables d'environnement."
    )
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
