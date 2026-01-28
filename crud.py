# from sqlalchemy.orm import Session
# import models  # On importe la définition de la table


# # 1. LIRE (SELECT)
# def get_taches(db: Session):
#     # Traduction : "Dans la DB, cherche dans la table TacheModel et prends tout (.all())"
#     return db.query(models.TacheModel).all()


# # 2. CRÉER (INSERT)
# def create_tache(db: Session, texte_tache: str):
#     # On crée un OBJET Python
#     nouvelle_tache = models.TacheModel(titre=texte_tache)

#     # On l'ajoute au panier
#     db.add(nouvelle_tache)
#     # On valide (Transaction)
#     db.commit()
#     # On rafraîchit l'objet pour récupérer son ID tout neuf
#     db.refresh(nouvelle_tache)
#     return nouvelle_tache


# # 3. SUPPRIMER (DELETE)
# def delete_tache(db: Session, nom_tache: str):
#     # On cherche d'abord la tâche
#     tache = (
#         db.query(models.TacheModel).filter(models.TacheModel.titre == nom_tache).first()
#     )

#     if tache:
#         db.delete(tache)
#         db.commit()
#         return True
#     return False


# # 4. METTRE À JOUR (UPDATE)
# def update_tache(db: Session, task_id: int, fini: bool):
#     # On dit explicitement : "Je te promets que 'tache' est un modèle TacheModel"
#     tache: models.TacheModel = (
#         db.query(models.TacheModel).filter(models.TacheModel.id == task_id).first()
#     )

#     if tache:
#         # On modifie la valeur
#         tache.est_fini = fini
#         # On valide la transaction
#         db.commit()
#         # On rafraîchit pour être sûr d'avoir la version à jour
#         db.refresh(tache)
#         return tache
#     return None


# # Filtration des taches finies
# def get_taches_finies(db: Session):
#     # On ajoute .filter(Condition)
#     return db.query(models.TacheModel).filter(models.TacheModel.est_fini == True).all()

from sqlalchemy.orm import Session
import models
from security import get_password_hash


# --- GESTION DES UTILISATEURS ---
def get_user(db: Session, user_id: int):
    # SQLAlchemy va chercher l'utilisateur.
    # Grâce à la relation définie dans models.py, il chargera aussi ses tâches si on lui demande.
    return db.query(models.UserModel).filter(models.UserModel.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    # Utile pour vérifier si l'email existe déjà
    return db.query(models.UserModel).filter(models.UserModel.email == email).first()


def create_user(db: Session, user: "UserCreate"):
    # 1. On transforme le mot de passe "123" en "$2b$12$..."
    mot_de_passe_crypte = get_password_hash(user.password)

    # 2. On enregistre UNIQUEMENT la version cryptée dans la base
    db_user = models.UserModel(email=user.email, hashed_password=mot_de_passe_crypte)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# --- GESTION DES TÂCHES ---


def get_taches(db: Session):
    return db.query(models.TacheModel).all()


# ⚠️ MODIFICATION MAJEURE ICI : On ajoute 'user_id'
# def create_tache(db: Session, tache: "NouvelleTache", user_id: int):
def create_tache(db: Session, tache, user_id: int):
    # On crée la tâche en précisant qui est le PROPRIÉTAIRE (owner_id)
    db_tache = models.TacheModel(titre=tache.texte, owner_id=user_id)

    db.add(db_tache)
    db.commit()
    db.refresh(db_tache)
    return db_tache


def delete_tache(db: Session, nom_tache: str):
    tache = (
        db.query(models.TacheModel).filter(models.TacheModel.titre == nom_tache).first()
    )
    if tache:
        db.delete(tache)
        db.commit()
        return True
    return False
