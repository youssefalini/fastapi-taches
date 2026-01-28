from passlib.context import CryptContext

# On configure le "Hacheur" pour utiliser l'algorithme bcrypt (le standard actuel)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Fonction 1 : Créer le Hash (Faire le smoothie)
# On l'utilise quand l'utilisateur s'inscrit
def get_password_hash(password: str):
    return pwd_context.hash(password)


# Fonction 2 : Vérifier le mot de passe (Goûter le smoothie)
# On l'utilise quand l'utilisateur se connecte (Login)
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


from datetime import datetime, timedelta
from jose import jwt

# 1. La Clé Secrète (La signature du bracelet)
# Seul le serveur la connaît. Si un pirate essaie de fabriquer un faux token, ça ne marchera pas.
SECRET_KEY = "mon_super_secret_indevinable"  # Dans la vraie vie, c'est une longue chaîne aléatoire
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Le token est valable 30 minutes


# Fonction 3 : Créer le Token (Fabriquer le bracelet)
def create_access_token(data: dict):
    to_encode = data.copy()

    # On définit la date d'expiration
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # On encode le tout avec la clé secrète
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
