from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. L'adresse de la base de données
# C'est la même qu'avant, mais avec un préfixe spécial pour SQLAlchemy
SQLALCHEMY_DATABASE_URL = "sqlite:///./todo.db"

# 2. Création du Moteur (The Engine)
# connect_args={"check_same_thread": False} est nécessaire uniquement pour SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. La Session (L'usine à connexions)
# Chaque fois qu'on voudra parler à la base, on demandera une "Session" à cette usine.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. La Base (Le patron)
# Toutes nos futures tables (Tâches, Utilisateurs...) hériteront de cette classe.
Base = declarative_base()
