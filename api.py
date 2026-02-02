# # from fastapi import FastAPI, HTTPException
# # from pydantic import BaseModel  # <--- Nouveau ! Sert à valider les données

# # # On importe la fonction 'charger_file' depuis notre fichier tasks.py
# # # (Assurez-vous que tasks.py est bien dans le même dossier)
# # from tasks import charger_file, ajouter_tache, supprimer_tache

# # app = FastAPI()


# # @app.get("/")
# # def home():
# #     return {"message": "Bienvenue sur mon API ! 🚀"}


# # # @app.get("/bonjour")
# # # def dire_bonjour(nom: str = "Inconnu"):
# # #     return {"message": f"Bonjour, {nom} !"}
# # # C'est notre "contrat". Le client DOIT envoyer un JSON avec un champ "texte"
# # class NouvelleTache(BaseModel):
# #     texte: str


# # # ROUTE POUR LA LECTURE
# # # @app.get("/tasks")
# # # def get_tasks():
# # #     # 1. On appelle la fonction de tasks.py pour lire le JSON
# # #     # liste = charger_file()

# # #     # 2. On renvoie simplement la liste.
# # #     # FastAPI va automatiquement la convertir en JSON propre.
# # #     return {"tasks": liste}


# # # ROUTE POUR L'ÉCRITURE
# # @app.post("/tasks")
# # def post_task(nouvelle_tache: NouvelleTache):
# #     # 1. On charge la liste actuelle des tâches
# #     # liste = charger_file() : on n'en a plus besoin ici, car on ajoute directement dans la base de données

# #     # 2. On ajoute la nouvelle tâche à la liste
# #     ajouter_tache(
# #         nouvelle_tache.texte
# #     )  # tache.texte contient ce que l'utilisateur a envoyé

# #     # 3. On confirme que c'est fait
# #     return {"message": f"Tâche '{nouvelle_tache.texte}' ajoutée !"}


# # # ROUTE POUR LA MISE À JOUR
# # # @app.put("/tasks/{ancienne_tache}")
# # # def update_task(ancienne_tache: str, nouvelle_tache: NouvelleTache):
# # #     # 1. On charge la liste actuelle des tâches
# # #     liste = charger_file()

# # #     # 2. On met à jour la tâche
# # #     if mettre_a_jour_tache(ancienne_tache, nouvelle_tache.texte, liste):
# # #         return {
# # #             "message": f"Tâche '{ancienne_tache}' mise à jour en '{nouvelle_tache.texte}'."
# # #         }
# # #     else:
# # #         return {"message": f"Tâche '{ancienne_tache}' non trouvée."}


# # # ROUTE POUR LA SUPPRESSION
# # # Remarquez les accolades {nom_tache}. C'est une variable DANS l'URL.
# # @app.delete("/tasks/{nom_tache}")
# # def delete_task(nom_tache: str):
# #     # liste = charger_file()

# #     # On tente de supprimer
# #     succes = supprimer_tache(nom_tache)

# #     if succes:
# #         return {"message": f"La tâche '{nom_tache}' a été supprimée."}
# #     else:
# #         # Code 404 (Rouge) : Erreur, resource non trouvée !
# #         raise HTTPException(status_code=404, detail="Tâche introuvable")
# from fastapi import FastAPI, HTTPException, Depends
# from sqlalchemy.orm import Session
# from pydantic import BaseModel

# # On importe nos outils
# import models
# import crud
# from database import SessionLocal, engine

# # Création des tables (Au cas où)
# models.Base.metadata.create_all(bind=engine)

# app = FastAPI()


# # --- LA DÉPENDANCE (La magie de FastAPI) ---
# # Cette fonction donne une connexion à la route et la ferme après
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# # --- LE CONTRAT DE DONNÉES (Pydantic) ---
# class NouvelleTache(BaseModel):
#     texte: str


# # Contrat pour la mise à jour (Juste le statut fini/pas fini)
# class TacheUpdate(BaseModel):
#     est_fini: bool


# # --- LES ROUTES ---


# @app.get("/tasks")
# def read_tasks(db: Session = Depends(get_db)):
#     # On demande au CRUD de chercher les tâches avec la session 'db'
#     taches = crud.get_taches(db)
#     return taches


# @app.post("/tasks")
# def create_task(tache: NouvelleTache, db: Session = Depends(get_db)):
#     crud.create_tache(db=db, texte_tache=tache.texte)
#     return {"message": f"Tâche '{tache.texte}' ajoutée !"}


# # route pour obtenir les tâches finies
# @app.get("/tasks/finished")
# def read_finished_tasks(db: Session = Depends(get_db)):
#     taches = crud.get_taches_finies(db)
#     return taches


# @app.delete("/tasks/{nom_tache}")
# def delete_task(nom_tache: str, db: Session = Depends(get_db)):
#     succes = crud.delete_tache(db=db, nom_tache=nom_tache)
#     if not succes:
#         raise HTTPException(status_code=404, detail="Tâche introuvable")
#     return {"message": f"Tâche '{nom_tache}' supprimée."}


# @app.put("/tasks/{task_id}")
# def update_task(task_id: int, tache_maj: TacheUpdate, db: Session = Depends(get_db)):
#     # On appelle le CRUD avec l'ID et la nouvelle valeur (True ou False)
#     tache_mise_a_jour = crud.update_tache(
#         db=db, task_id=task_id, fini=tache_maj.est_fini
#     )

#     if tache_mise_a_jour is None:
#         raise HTTPException(status_code=404, detail="Tâche introuvable")

#     return tache_mise_a_jour
from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
import crud
from database import SessionLocal, engine
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

# On importe nos outils de sécurité
from security import verify_password, create_access_token, SECRET_KEY, ALGORITHM

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# --- DÉBUT DU BLOC CORS ---
# On définit qui a le droit d'entrer.
# "*" veut dire "Tout le monde". C'est bien pour le développement.
# En vraie prod, on mettrait ["https://mon-site.com"]
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Autorise tout : GET, POST, DELETE...
    allow_headers=["*"],  # Autorise tous les types de contenu
)
# --- FIN DU BLOC CORS ---

# --- CONFIGURATION SÉCURITÉ ---
# On dit à FastAPI que l'URL pour se connecter est "/token"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- LE GARDIEN (Vérifie le Token) ---
# Cette fonction sera appelée à chaque fois qu'on veut protéger une route.
# Elle lit le token, le décrypte, et retrouve l'utilisateur.
async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    exception_auth = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalide ou expiré",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 1. On décrypte le token avec la clé secrète
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")  # On récupère l'email caché dedans
        if email is None:
            raise exception_auth
    except JWTError:
        raise exception_auth

    # 2. On vérifie que l'utilisateur existe bien dans la base
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise exception_auth

    return user  # Si tout est bon, on renvoie l'utilisateur connecté !


# --- LES CONTRATS (Pydantic) ---


# 1. Le Schéma pour LIRE une Tâche (ce que l'API renvoie au client)
class TacheSchema(BaseModel):
    id: int
    titre: str
    est_fini: bool
    owner_id: int

    # Cette configuration est OBLIGATOIRE pour lire des données depuis SQLAlchemy
    class Config:
        from_attributes = True


# 2. Le Schéma pour CRÉER une Tâche (ce que le client envoie)
class NouvelleTache(BaseModel):
    texte: str


# 3. Le Schéma pour CRÉER un Utilisateur
class UserCreate(BaseModel):
    email: str
    password: str


# 4. Le Schéma pour LIRE un Utilisateur (Le plus magique !)
class UserSchema(BaseModel):
    id: int
    email: str
    # C'est ici que la magie opère : L'utilisateur contient une LISTE de tâches
    tasks: list[TacheSchema] = []

    class Config:
        from_attributes = True


# --- LES ROUTES ---


# Route A : Créer un Utilisateur
@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # On vérifie si l'email existe déjà
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Cet email est déjà pris.")
    return crud.create_user(db=db, user=user)


# 2. LOGIN (La porte d'entrée)
# Swagger va afficher un petit cadenas grâce à "OAuth2PasswordRequestForm"
@app.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    # Note : form_data.username contient l'email
    user = crud.get_user_by_email(db, form_data.username)

    # On vérifie le mot de passe
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Email ou mot de passe incorrect")

    # Si c'est bon, on génère le token
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# 3. QUI SUIS-JE ? (Route protégée)
# Remarquez : current_user = Depends(get_current_user)
@app.get("/users/me", response_model=UserSchema)
def read_users_me(current_user: models.UserModel = Depends(get_current_user)):
    return current_user


# Route B : Créer une tâche POUR un utilisateur spécifique
# Regardez bien l'URL : on précise l'ID du chef dans l'adresse
# @app.post("/users/{user_id}/tasks/")
# def create_task_for_user(
#     user_id: int, tache: NouvelleTache, db: Session = Depends(get_db)
# ):
#     return crud.create_tache(db=db, tache=tache,  =user_id)


# 4. CRÉER UNE TÂCHE (Version Sécurisée)
# On n'a plus besoin de passer {user_id} dans l'URL ! L'API sait qui on est.
@app.post("/tasks/")
def create_task(
    tache: NouvelleTache,
    db: Session = Depends(get_db),
    current_user: models.UserModel = Depends(get_current_user),
):
    return crud.create_tache(db=db, tache=tache, user_id=current_user.id)


# Route C : Lire toutes les tâches (pour vérifier)
# @app.get("/tasks/")
# def read_tasks(db: Session = Depends(get_db)):
#     return crud.get_taches(db)


# 5. LIRE MES TÂCHES
@app.get("/tasks/")
def read_my_tasks(
    db: Session = Depends(get_db),
    current_user: models.UserModel = Depends(get_current_user),
):
    # On renvoie seulement les tâches de l'utilisateur connecté
    # (Il faudra peut-être adapter crud.get_taches pour filtrer, mais testons déjà ça)
    return current_user.tasks


# Remarquez 'response_model=UserSchema'.
# On dit à FastAPI : "Utilise le moule UserSchema pour formater la réponse".
# C'est ce moule qui va inclure la liste des tâches.
# @app.get("/users/{user_id}", response_model=UserSchema)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="Utilisateur introuvable")
#     return db_user
