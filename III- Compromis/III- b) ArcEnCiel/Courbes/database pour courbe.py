from creationtable import table
import ArcEnCiel
import time
import sqlite3

carac = 'abcdefghijklmnopqrstuvwxyz'
t_min, t_max = 4, 4
database = "./T M temps EnCours.sqlite"
hachage = 'md5', 'utf-8' # md5
type = 'ArcEnCiel'
datas = ArcEnCiel.ArcEnCiel(1, 1, 1, t_min, t_max, carac, type, database, hachage) # Objet contenant les informations

database = "./T M temps T = 9000 M = 12000 Pas = 1000.sqlite"
conn = sqlite3.connect(database)
cur = conn.cursor()
try:
    cur.execute("""CREATE TABLE Temps(
        M INT,
        T INT,
        temps INT);""")
except sqlite3.OperationalError:
    pass
else:
    print("Nouvelle Table")

for T in range(3000, 9001, 500):
    for M in range(3000, 12001, 500):
        cur.execute("""SELECT * FROM Temps WHERE T = ? AND M = ?""",(T, M))

        if cur.fetchone() is None:
            # T et M n'a pas encore été calculé : on le calcule

            print("T :", T, ", M :", M)

            datas.t = T
            datas.m = M

            temps = time.time()

            text = table(datas)

            temps = time.time() - temps

            cur.execute("""
            INSERT INTO Temps
            (M, T, temps)
            VALUES(?, ?, ?);""",(M, T, temps))

            conn.commit()

            print("Création table arc en ciel T : {} , M : {} : {} secondes\n".format(T, M, temps))

        else:
            print(T, M, "Déjà dans la table")

conn.close