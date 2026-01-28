from database import engine, Base
import models  # On importe nos modèles pour que SQLAlchemy les connaisse

print("Création des tables...")
# Cette ligne magique transforme vos classes Python en vraies tables SQL
Base.metadata.create_all(bind=engine)
print("Tables créées avec succès ! (Si elles n'existaient pas déjà)")
