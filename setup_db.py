import sqlite3

connection = sqlite3.connect(
    "todo.db"
)  # 1. Connexion (ou création ;Si le fichier "todo.db" n'existe pas, Python le crée pour nous. ) de la base de données
cursur = (
    connection.cursor()
)  # 2. Création d'un curseur pour exécuter des commandes SQL (C'est notre "stylo" pour écrire du SQL)
# 3. Création de la table "tasks" si elle n'existe pas déjà
sql_instruction = """CREATE TABLE IF NOT EXISTS TASKS  (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL);"""
cursur.execute(sql_instruction)
connection.commit()  # 4. Sauvegarde des modifications dans la base de données
connection.close()  # 5. Fermeture de la connexion à la base de données
print("✅ Base de données et table 'tasks' créées avec succès !")
