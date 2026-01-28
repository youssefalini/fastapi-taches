import sqlite3

connection = sqlite3.connect("todo.db")
cursor = connection.cursor()

# L'ordre SQL pour tout récupérer
cursor.execute("SELECT * FROM tasks")

# On demande à Python de récupérer le résultat ("Fetch All" = Tout attraper)
toutes_les_taches = cursor.fetchall()

print("--- Voici ce que la base renvoie ---")
print(toutes_les_taches)
print("\n--- Affichage propre ---")
for tache in toutes_les_taches:
    # tache est un "Tuple" : (id, titre)
    # tache[0] c'est l'ID
    # tache[1] c'est le TITRE
    print(f"ID: {tache[0]} | Titre: {tache[1]}")

connection.close()
