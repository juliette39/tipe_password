# Création base de données rainbow table

import time
import sqlite3
from ArcEnCiel import *

def table(datas : ArcEnCiel) -> None:
    """Création table Arc en ciel si AEC, Classique sinon
    Si perfect est True : table parfaite : pas de fusion
    Renvoie une base de donnée d'une table arc en ciel :
    Colonne 1 : indice d'origine
    Colonne 2 : indice t fois de l'indice d'origine
    Table ordonnée suivant la dernière colonne
    """

    start_time = time.time()
    tableName = datas.type
    conn = sqlite3.connect(datas.database)
    cur = conn.cursor()

    for l in range(datas.l):

        print("Table {}".format(l+1))
        tableNamel = tableName + str(l)

        try:
            cur.execute("""DROP TABLE {}""".format(tableNamel))
        except sqlite3.OperationalError:
            pass

        cur.execute("""CREATE TABLE {}(
            i_0 INT,
            i_t INT);""".format(tableNamel))

        for m in range(datas.m):
            i_0 = datas.ialea(tableName, l)
            i_t = i_0

            for t in range(datas.t):
                if tableName != 'ArcEnCiel':
                    t = l
                i_t = datas.i2i(i_t, t)

            cur.execute("""
                INSERT INTO {}
                (i_0, i_t)
                VALUES(?, ?);""".format(tableNamel), (i_0, i_t))
            conn.commit()

            if m % 200 == 0:
                print("{} secondes pour {} lignes".format(round(time.time() - start_time), m))

    conn.commit()
    conn.close

# Générer table

def creer():
    start_time = time.time()
    table(datas) # Création table AEC
    tableName = datas.type
    print("Création table {} : {} secondes\n".format(tableName, time.time() - start_time))

# creer()