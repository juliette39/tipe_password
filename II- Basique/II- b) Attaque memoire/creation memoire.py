# Liste de tous les caractères possibles dans le mot de passe :
caracteres = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

# Création base de données avec tout d'une certaine longueur et de certains caractères

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
    dic = {}
    l = len(caracteres)
    cherche = sum([l**i for i in range(1, mini)])

    mot = dec2base(cherche, caracteres)

    while len(mot) <= maxi:
        mot = dec2base(cherche, caracteres)
        liste.append([mot, hachage(mot)])
        cherche += 1

    return liste

def hachage(mot):
    """hash mot avec une fonction de hachage"""
    return hashlib.md5(mot.encode('utf8')).hexdigest()


def creation(database, dic):
    conn = sqlite3.connect(database)
    cur = conn.cursor()

    cur.execute("""CREATE TABLE Memoire (mot CHARACTER, hash CHARACTER) """)

    for mot in dic:
        cur.execute("""Insert Into Memoire (mot, hash) VALUES (?, ?)""", mot)
    conn.commit()
    conn.close

def creer_table(n):
    database = "./Memoire{}.sqlite".format(n)
    dic = forceBrute(n, n, caracteres)
    creation(database, dic)

t = time.time()
creer_table(4)
print("Temps pour créer table mémoire : {} secondes".format(time.time() - t))

# 0 0.0039310455322265625
# 1 0.009385108947753906
# 2 0.026437997817993164
# 3 0.5101959705352783
# 4 11.037984132766724
# 5 266.90790915489197