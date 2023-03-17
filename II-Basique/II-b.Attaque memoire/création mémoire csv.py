# Liste de tous les caractères possibles dans le mot de passe :
caracteres = 'abcdefghijklmnopqrstuvwxyz'


# Création base de données avec tout d'une certaine longueur et de certains caractères
# Temps de création, temps de recherche

import sqlite3
import hashlib
import time

def dec2base(i, caracteres):
    """Convertit i en base 10 en result en base len(caracteres) avec la liste de caractères caracteres"""

    l = len(caracteres)
    result = caracteres[i % l]
    i = (i//l) - 1

    while i > -1:
        i, result = (i // l) - 1, caracteres[i % l] + result
    return result


def forceBrute(mini = 1, maxi = 10, caracteres = caracteres):
    """Test par force brute jusqu'à ce que la valeur vaille mdp"""

    liste = []
    l = len(caracteres)
    cherche = sum([l**i for i in range(1, mini)])

    mot = dec2base(cherche, caracteres)

    while len(mot) <= maxi:
        mot = dec2base(cherche, caracteres)
        liste.append([mot, hachage(mot)])
        cherche += 1

    return liste[:-1]

def hachage(mot):
    """hash mot avec une fonction de hachage"""

    return hashlib.md5(mot.encode('utf8')).hexdigest()

def creation(database, liste):
    with open(database, "w") as f:
        for i in liste:
            f.write(",".join(i) + "\n")

def creer_table(n):
    database = "/Users/juliettedebono/Documents/MP*/TIPE/II- Basique/II- b) Attaque memoire/Memoire{}.csv".format(n)
    liste = forceBrute(n, n, caracteres)
    creation(database, liste)


creer_table(4)



# 0 0.0002338886260986328
# 1 0.0005590915679931641
# 2 0.004124879837036133
# 3 0.0750572681427002
# 4 2.241652011871338