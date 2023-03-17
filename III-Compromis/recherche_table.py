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

    for t in range(1, i):
        if h == hash:
            return c
        if datas.type != 'ArcEnCiel':
            t = l
        c, h = datas.h2h(h, t)
    if h == hash:
        return c
    return False

def inter(ligne : tuple, l : int, i : int, hash : str, datas : ArcEnCiel):
    if ligne is not None:
        for id in ligne:
            c1 = datas.i2c(id[0])
            h1 = datas.h(c1)
            if h1 == hash:
                return c1
            else:
                result = recherche(h1, hash, l, i, datas)
                if result:
                    return result # c'est la bonne ligne
    return False


def inverse(hash : str, datas : ArcEnCiel) -> str:
    """Cherche le mot de passe d'origine ayant hash comme image hachée"""

    tableName = datas.type

    conn = sqlite3.connect(datas.database)
    cur = conn.cursor()

    if datas.type == 'ArcEnCiel':
        for i in reversed(range(datas.t + 1)):
            indice = datas.h2i(hash, i)
            for t in range(i, datas.t):
                t +=1
                indice = datas.i2i(indice, t)

            for l in range(datas.l):
                # On récupère les dernières lignes lorsque i_t est dans colonne dans toutes les l tables
                tableNamel = tableName + str(l)
                cur.execute("""SELECT i_0 FROM {} WHERE i_t = ?""".format(tableNamel), (indice,))
                # t = time.time()
                result = inter(cur.fetchall(), l, i, hash, datas)
                # print(time.time() - t)
                if result:
                    return result

            if i % 100 == 0:
                print("Colonne {}".format(i))

    else:
        for l in range(datas.l):
            print("Table {}".format(l))
            # Dans chaque table
            indice = datas.h2i(hash, l)
            tableNamel = tableName + str(l)
            for t in range(datas.t):
                indice = datas.i2i(indice, l)
                cur.execute("""SELECT i_0 FROM {} WHERE i_t = ?""".format(tableNamel), (indice,))
                result = inter(cur.fetchall(), l, t, hash, datas)
                if result:
                    return result

                if t % 100 == 0:
                    print("Colonne {}".format(t))

    conn.close
    return "Pas dans la table"


def testValidite(mot : str, hach : str, datas : ArcEnCiel) -> bool :
    """Renvoie si mot est bien l'antécédent de hash avec la fonction du hachage de datas"""

    return datas.h(mot) == hach


def alea(datas : ArcEnCiel):
    """Génère un mot aléatoire suivant les caractéristiques de la table"""

    result = ""

    for _ in range(rd.randint(datas.t_min, datas.t_max)):
        result += rd.choice(datas.carac)
    return result


# result = datas.pick() # Choisi aléatoirement un hach qui est dans la base de données
# result = alea(datas) # Choisi aléatoirement un mot qui pourrait être dans la base de données

# result = "TiP3" # Mot imposé

# hach = datas.h(result) # Hache le mot choisi
# print(hach, result) # Affiche le hach du mot cherché

# t = time.time() # Démare le compteur de temps

# mot = inverse(hach, datas) # Cherche l'antécédent du hach

# print(mot) # Affice le mot de passe trouvé
# print(testValidite(mot, hach, datas)) # Vérifie que c'est le bon mot
# print("Temps pour recherche table {} : {} secondes".format(datas.type, time.time() - t))