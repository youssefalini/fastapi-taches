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
import time
from typing import Callable


# --- VOTRE DÉCORATEUR ---
def timer(func: Callable):
    # On définit le wrapper interne. *args et **kwargs servent à accepter n'importe quels arguments
    def wrapper(*args, **kwargs):
        # TODO 1 : Lancez le chrono (start_time = time.time())
        start_time = time.time()
        result = func(*args, **kwargs)  # On exécute la vraie fonction
        # TODO 2 : Arrêtez le chrono (end_time = ...)
        end_time = time.time()
        # TODO 3 : Calculez la différence et affichez "Temps d'exécution : X secondes"
        result_time = end_time - start_time
        return result

    return wrapper


# --- L'UTILISATION ---
@timer
def traitement_long():
    print("Traitement en cours...")
    time.sleep(2)  # On fait dormir le code 2 secondes
    print("Fini !")


# --- TEST ---
traitement_long()
