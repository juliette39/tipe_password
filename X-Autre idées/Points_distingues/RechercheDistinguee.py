# Recherche mot à partir de base de données de table distinguée (Rivest)

import time
import random as rd
from ArcEnCiel import *


def recherche(h : int, hash : str, l : int, i : int, datas : ArcEnCiel) -> str:
    """
    * On donne le hash qu'on cherche et le premier hash de la ligne de notre table où est situé le mot
    * Applique l'algo jusqu'à ce que le hash i fois :
        - Si c'est le bon : renvoie la valeur avant hachage
        - Sinon renvoie False
    """

    for _ in range(1, i):
        if h == hash:
            return c
        c, h = datas.h2h(h, l)
    if h == hash:
        return c
    return False


def inverse(hash : str, datas : ArcEnCiel) -> str:
    """Cherche le mot de passe d'origine ayant hash comme image hachée"""

    conn = sqlite3.connect(datas.database)
    cur = conn.cursor()

    for l in range(datas.l):
        # Dans chaque table
        indice = datas.h2i(hash, l)
        for t in range(datas.t):
            # print(t)

            indice = datas.i2i(indice, l)
            cur.execute("""SELECT i_0 FROM {}{} WHERE i_t = ?""".format(datas.AEC, l), (indice,))
            id = cur.fetchone()

            if id is not None:
                c1 = datas.i2c(id[0])
                h1 = datas.h(c1)
                if h1 == hash:
                    return c1
                else:
                    result = recherche(h1, hash, l, t, datas)
                    if result:
                        return result # c'est la bonne ligne
    conn.close
    return "Pas dans la table"


def testValidite(mot : str, hach : str, datas : ArcEnCiel) -> bool :
    """Renvoie si mot est bien l'antécédent de hash avec la fonction du hachage de datas"""

    return datas.h(mot) == hach


def alea(datas : ArcEnCiel):
    """Génère un mot aléatoire suivant les caractéristiques de la table"""

    result = ""
    for _ in range(datas.tailles[rd.randint(0, len(datas.tailles) - 1)]):
        result += rd.choice(datas.carac)
    return result


# result = datas.pick() # Choisi aléatoirement un hash qui est dans la base de données
# result = "truc" # Mot imposé
# result = alea(datas) # Choisi aléatoirement un mot qui pourrait être dans la base de données
result = "wisy"
hash = datas.h(result) # Hache le mot choisi

start_time = time.time() # Démare le compteur de temps

print(hash, result) # Affiche le hash du mot cherché

mot = inverse(hash, datas) # Cherche l'antécédent du hash

print(mot) # Affice le mot de passe trouvé
print(testValidite(mot, hash, datas)) # Vérifie que c'est le bon mot

print("\nTemps : {} secondes".format(time.time() - start_time)) # Temps nécéssaire
