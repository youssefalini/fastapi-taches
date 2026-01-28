# def calculer_total(articles:list[float], remise:bool)-> float:
#     total = sum(articles)
#     if remise:
#         total = total * 0.9  # 10% de réduction
#     return total

# prix_panier = [12.5, 9.99, 45.0]
# resultat = calculer_total(prix_panier, True)
# print(resultat)
# prix_sales : list[str] = ["$10.50", "$5.00", "ERREUR", "$33.20", "N/A"]
# prix_propres : list[float] = [  float(prix[1:]) for prix in prix_sales if (prix.startswith("$"))]
# print(prix_propres)


# Pour les decorateurs
# ---> EXO 1 : Créez un décorateur "timer" qui mesure le temps d'exécution d'une fonction.
# import time
# from typing import Callable


# # --- VOTRE DÉCORATEUR ---
# def timer(func: Callable):
#     # On définit le wrapper interne. *args et **kwargs servent à accepter n'importe quels arguments
#     def wrapper(*args, **kwargs):
#         # TODO 1 : Lancez le chrono (start_time = time.time())
#         start_time = time.time()
#         result = func(*args, **kwargs)  # On exécute la vraie fonction
#         # TODO 2 : Arrêtez le chrono (end_time = ...)
#         end_time = time.time()
#         # TODO 3 : Calculez la différence et affichez "Temps d'exécution : X secondes"
#         result_time = end_time - start_time
#         return result

#     return wrapper
# # --- L'UTILISATION ---
# @timer
# def traitement_long():
#     print("Traitement en cours...")
#     time.sleep(2)  # On fait dormir le code 2 secondes
#     print("Fini !")
# # --- TEST ---
# traitement_long()
# ---> EXO 2 : Créez un décorateur "logger" qui enregistre dans un fichier le nom de la fonction appelée et ses arguments.
# USER_ROLE = "admin"
# def admin_required (func:Callable):
#     def wrapper(*args , **kwargs) :
#         # TODO 1 : Vérifiez si USER_ROLE est égal à "admin"
#         if USER_ROLE == "admin":
#         # TODO 2 : Si oui, exécutez la fonction 'func' et retournez son résultat
#             return func(*args,**kwargs)
#         else :
#         # TODO 3 : Si non, affichez un message d'erreur et ne lancez PAS la fonction
#             print("Erreur : Acces refuse")
#     return wrapper
# # --- L'UTILISATION ---
# @admin_required
# def detruire_base_de_donnees():
#     print("Base de données détruite !")
# # --- TEST ---
# print(f"Tentative d'action avec le rôle : {USER_ROLE}")
# detruire_base_de_donnees()

## Pour gestion des erreurs et les fichiers json
# import json
# import os
# file = "data.json"
# def charger_file () -> int :
#     try :
#         with open (file,"r") as f :
#             data = json.load(f)
#             return data
#     except FileNotFoundError :
#         print ("Erreur : Le fichier n'existe pas.")
#         return 0
#     except json.JSONDecodeError :
#         print ("Erreur : Le fichier n'est pas un JSON valide.")
#         return 0

# # 1. Test de chargement (devrait afficher 0 si pas de fichier)
# score = charger_file()
# print(f"Score actuel du joueur : {score}")

# # 2. Simulation : Le joueur gagne des points
# score += 50
# print(f"Le joueur gagne 50 points. Nouveau score : {score}")
# print("Sauvegarde en cours...")
# with open('NOM_FICHIER', "w") as f:
#     json.dump(score,f)

## Projet finale de la semaine 1
# import json
# import os

# file = "tasks.json"


# def charger_file() -> list[str]:
#     try:
#         with open(file, "r") as f:
#             data = json.load(f)
#             return data
#     except FileNotFoundError as e:
#         print("File doesn't exists", e)
#         return []
#     except json.JSONDecodeError as e:
#         print("File invalid")
#         return []


# def ajouter_tache(tache: str, liste_taches: list[str]) -> None:
#     tache = tache.lower()
#     if tache not in liste_taches:
#         liste_taches.append(
#             tache
#         )  # ajoute tous ces éléments à liste_taches en une seule fois
#     with open(file, "w") as f:
#         json.dump(
#             liste_taches, f, indent=4
#         )  # indent=4 rend le JSON lisible par un humain)
#     print(f"Tâche '{tache}' ajoutée avec succès.")


# def afficher_taches(liste_taches: list[str]) -> None:
#     if not liste_taches:
#         print("Aucune tâche dans la liste.")
#         return
#     for i, t in enumerate(liste_taches, start=1):
#         print(f"{i} - {t}")


# def mettre_a_jour_tache(ancienne: str, nouvelle: str, liste_taches: list[str]) -> bool:
#     """Remplace une tâche par une autre."""
#     ancienne = ancienne.lower()
#     nouvelle = nouvelle.lower()

#     # 1. On cherche l'index (la position) de l'ancienne tâche
#     if ancienne in liste_taches:
#         index = liste_taches.index(ancienne)

#         # 2. On remplace la valeur à cet index
#         liste_taches[index] = nouvelle

#         # 3. On sauvegarde
#         with open(file, "w") as f:
#             json.dump(liste_taches, f, indent=4)

#         print(f"🔄 Tâche '{ancienne}' modifiée en '{nouvelle}'.")
#         return True

#     return False


# def supprimer_tache(tache: str, liste_taches: list[str]) -> bool:
#     """Supprime une tâche si elle existe. Retourne True si succès, False sinon."""
#     tache = tache.lower()  # On gère la casse comme pour l'ajout

#     if tache in liste_taches:
#         liste_taches.remove(tache)  # La méthode .remove() enlève l'élément

#         # On sauvegarde le changement
#         with open(file, "w") as f:
#             json.dump(liste_taches, f, indent=4)
#         print(f"🗑️ Tâche '{tache}' supprimée.")
#         return True

#     print(f"⚠️ Tâche '{tache}' introuvable.")
#     return False


# def quitter() -> None:
#     print("Au revoir !")
#     exit()


# def menu() -> None:
#     liste_taches = charger_file()
#     while True:
#         print("\nMenu :")
#         print("1. Ajouter une tâche")
#         print("2. Afficher les tâches")
#         print("3. Quitter")
#         print("4. Mettre à jour une tâche")
#         print("5. Supprimer une tâche")
#         choix = input("Choisissez une option (1-3) : ")
#         if choix == "1":
#             tache = input("Entrez la tâche à ajouter : ")
#             if not tache.strip() == "":
#                 ajouter_tache(tache, liste_taches)
#         elif choix == "2":
#             afficher_taches(liste_taches)
#         elif choix == "3":
#             quitter()
#         elif choix == "4":
#             ancienne = input("Entrez la tâche à mettre à jour : ")
#             nouvelle = input("Entrez la nouvelle tâche : ")
#             if not mettre_a_jour_tache(ancienne, nouvelle, liste_taches):
#                 print(f"Tâche '{ancienne}' non trouvée.")
#         elif choix == "5":
#             tache = input("Entrez la tâche à supprimer : ")
#             if not supprimer_tache(tache, liste_taches):
#                 print(f"Tâche '{tache}' non trouvée.")
#         else:
#             print("Option invalide. Veuillez réessayer.")


# if __name__ == "__main__":
#     menu()


#                           SEMAINE 3 :
import sqlite3

# Plus de fichier JSON ! On pointe vers la DB.
DB_NAME = "todo.db"


def get_db_connection():
    """Crée une connexion et la renvoie."""
    conn = sqlite3.connect(DB_NAME)
    return conn


def charger_file() -> list[str]:
    """Récupère tous les TITRES des tâches depuis la base de données."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT titre FROM tasks")
    rows = cursor.fetchall()  # Renvoie [(titre1,), (titre2,), ...]

    conn.close()

    # On transforme la liste de tuples en liste de chaines simples
    # [("Manger",), ("Dormir",)]  --->  ["Manger", "Dormir"]
    liste_propre = [row[0] for row in rows]
    return liste_propre


def ajouter_tache(
    tache: str,
) -> None:
    """Ajoute une tâche dans la base SQL."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # On insère juste le titre (l'ID est automatique)
    cursor.execute("INSERT INTO tasks (titre) VALUES (?)", (tache,))

    conn.commit()  # Très important pour sauvegarder !
    conn.close()
    print(f"✅ Tâche '{tache}' sauvegardée en base de données.")


def supprimer_tache(tache: str) -> bool:
    """Supprime une tâche par son nom (Attention : supprime toutes celles qui ont ce nom)."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # On vérifie d'abord si elle existe
    cursor.execute("SELECT * FROM tasks WHERE titre = ?", (tache,))
    if cursor.fetchone() is None:
        conn.close()
        return False  # Pas trouvé

    # Si elle existe, on supprime
    cursor.execute("DELETE FROM tasks WHERE titre = ?", (tache,))
    conn.commit()
    conn.close()
    print(f"🗑️ Tâche '{tache}' supprimée de la base.")
    return True


# Pour l'instant, on ignore 'mettre_a_jour' pour ne pas compliquer,
# car cela demande de gérer les IDs, ce qu'on fera lundi.
def menu():
    while True:
        print("\n--- MENU SQL ---")
        print("1. Voir")
        print("2. Ajouter")
        print("3. Supprimer")
        print("4. Quitter")
        choix = input("Choix : ")

        if choix == "1":
            print(charger_file())
        elif choix == "2":
            t = input("Tâche : ")
            ajouter_tache(t)  # Plus besoin du 2ème argument !
        elif choix == "3":
            t = input("Tâche à supprimer : ")
            supprimer_tache(t)  # Plus besoin du 2ème argument !
        elif choix == "4":
            break


if __name__ == "__main__":
    menu()
