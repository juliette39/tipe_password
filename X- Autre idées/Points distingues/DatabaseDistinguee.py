# Création base de données de table distinguée (Rivest)

import time
import sqlite3
from ArcEnCiel import *

fichierPath = "/Users/juliettedebono/Desktop/fichier.csv"

def condition(h):
    lon = 3
    bit = bin(int(h, 16))[-lon:]
    return bit == '0' * lon

def table(datas : ArcEnCiel) -> None:
    """Création table distinguées
    Si perfect est True : table parfaite : pas de fusion
    Renvoie une base de donnée d'une table arc en ciel :
    Colonne 1 : indice d'origine
    Colonne 2 : indice t fois de l'indice d'origine
    Table ordonnée suivant la dernière colonne
    """

    conn = sqlite3.connect(datas.database)
    cur = conn.cursor()
    start_time = time.time()
    fichier = open(fichierPath, 'w')
    fichier.write("m;t\n")
    bool = True

    for l in range(datas.l):

        print(l, "lignes")

        try:
            cur.execute("""DROP TABLE Distinguee{}""".format(l))

        except sqlite3.OperationalError:
            pass

        cur.execute("""CREATE TABLE Distinguee{}(
        i_0 INT,
        i_t INT);""".format(l))
        m = 0
        while m < datas.m:

            i_0 = datas.ialea(datas.AEC, l)
            i_t = i_0

            count = 0

            while count < datas.t and not condition(datas.h(datas.i2c(i_t))):
                i_t = datas.i2i(i_t, l)
                count += 1

            if count != datas.t:
                # print(count)

                cur.execute("""SELECT i_t FROM Distinguee{} WHERE i_t = {}""".format(l, i_t))
                result = cur.fetchone()
                if result is None:

                    cur.execute("""
                    INSERT INTO Distinguee{}
                    (i_0, i_t)
                    VALUES(?, ?);""".format(l), (i_0, i_t))
                    print(m)
                    m += 1

            conn.commit()

            if m % 10 == 0:
                if bool == True:
                    fichier.write("{};{}\n".format(m, str(time.time() - start_time).replace(".", ",")))
                    bool = False
            else:
                bool = True

    conn.commit()
    conn.close

    return None

# Générer table

def creer():
    """Créer une table"""

    start_time = time.time()
    print(datas.database)
    table(datas) # Création table AEC
    print("Création table distinguées {} secondes\n".format(time.time() - start_time))

creer()