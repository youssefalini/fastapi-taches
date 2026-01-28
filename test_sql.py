import sqlite3

# 1. On se connecte
connection = sqlite3.connect("todo.db")
cursur = connection.cursor()
# 2. On prépare la donnée
nouvelle_tache = "Apprendre le SQL"
cursur.execute(
    "INSERT INTO TASKS (titre) VALUES (?) ", (nouvelle_tache,)
)  # Remarquez le (?) -> C'est une sécurité. On ne colle jamais le texte directement.
# On dit à Python : "Remplace le point d'interrogation par ma variable".
# 3. On sauvegarde
connection.commit()
print("✅ Tâche ajoutée en base de données !")
# 4. On ferme la connexion
connection.close()
