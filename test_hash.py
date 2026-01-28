from security import get_password_hash, verify_password

mot_de_passe = "secret123"

# 1. On crypte
le_hash = get_password_hash(mot_de_passe)
print(f"Mot de passe en clair : {mot_de_passe}")
print(f"Mot de passe haché    : {le_hash}")

# 2. On vérifie (Le bon)
resultat_bon = verify_password("secret123", le_hash)
print(f"Est-ce que 'secret123' est bon ? -> {resultat_bon}")

# 3. On vérifie (Le mauvais)
resultat_faux = verify_password("toto", le_hash)
print(f"Est-ce que 'toto' est bon ?      -> {resultat_faux}")
