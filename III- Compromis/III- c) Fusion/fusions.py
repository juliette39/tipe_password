# Fusion
# On cherche un mot dans la table : on regarde dans combien de lignes il apparait

import time
import random as rd
from ArcEnCiel import *

def recherche(h : int, hash : str, l : int, i : int, datas : ArcEnCiel) -> str:
    """
    * On donne le hash qu'on cherche et le premier hash de la ligne de notre table où est situé le motj
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
    count = 0

    if datas.type == 'ArcEnCiel':

        for i in reversed(range(datas.t + 1)):
            indice = datas.h2i(hash, i)
            for t in range(i, datas.t):
                indice = datas.i2i(indice, t)

            indiceList = []
            for l in range(datas.l):
                # On récupère les dernières lignes lorsque i_t est dans colonne dans toutes les l tables
                tableNamel = tableName + str(l)
                cur.execute("""SELECT i_0 FROM {} WHERE i_t = ?""".format(tableNamel), (indice,))
                result = inter(cur.fetchall(), l, i, hash, datas)
                if result:
                    count += 1
    else:
        for l in range(datas.l):
            # Dans chaque table
            indice = datas.h2i(hash, l)
            tableNamel = tableName + str(l)
            for t in range(datas.t):
                indice = datas.i2i(indice, l)
                cur.execute("""SELECT i_0 FROM {} WHERE i_t = ?""".format(tableNamel), (indice,))

                result = inter(cur.fetchall(), l, t, hash, datas)
                if result:
                    count += 1
    conn.close
    return count

def alea(datas : ArcEnCiel):
    """Génère un mot aléatoire suivant les caractéristiques de la table"""

    result = ""
    for _ in range(datas.tailles[rd.randint(0, len(datas.tailles) - 1)]):
        result += rd.choice(datas.carac)
    return result

def fusions(datas):

    listeClassic = []
    listeAEC = []
    listeMot = []

    for i in range(10):

        datas.type = "Classique"

        mot = datas.pick()

        listeMot.append(mot)

        hash = datas.h(mot)

        listeClassic.append(inverse(hash, datas))

        datas.type = 'ArcEnCiel'

        listeAEC.append(inverse(hash, datas))

        print("ET DE {}".format(i+1))
        print(listeClassic, listeAEC)

    return listeClassic, listeAEC, listeMot

listeClassic, listeAEC, listeMot = fusions(datas)

print(listeClassic, listeAEC, listeMot)


"""
t = 1000
m = 5000
l = 1
N = 456976

listeMot = ['hlzw', 'mlcb', 'eesr', 'bgko', 'nqon', 'qtpx', 'qcvx', 'vutc', 'hiai', 'wnbz']
listeClassic = [343, 686, 681, 838, 687, 716, 663, 737, 839, 841]
listeAEC = [11, 4, 11, 2, 3, 4, 3, 6, 5, 9]
"""