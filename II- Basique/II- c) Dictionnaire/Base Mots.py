import sqlite3
import pandas
import os

database = "./Mots.sqlite"
lexiqueFile = "/Users/juliettedebono/Documents/MPSI_2/Info_TC/TP/Projet/Lexique383/Lexique383.tsv"
motFile = "./MOTS.csv"

def creation_DbSimple():
    """Créer une base nommée Mots.sqlite avec la table MOTS pour le TIPE et génere un fichier csv MOTS qui convient"""

    conn = sqlite3.connect(database)
    cur = conn.cursor()

    cur.execute("""CREATE TABLE MOTS(
        id INTEGER,
        ortho VARCHAR(79),
        cgram VARCHAR(79),
        freqlemfilms REAL,
        freqlemlivres REAL,
        freqfilms REAL,
        freqlivres REAL,
        PRIMARY KEY(id));""")

    # Création liste base de donnée à partir de fichier texte
    base = []
    with open(lexiqueFile,"r") as f :
        f.readline()
        i = 0
        ligne = f.readline()
        inter = ligne.strip("\n").split("\t")
        listeinter = [inter[0], inter[3], inter[6], inter[7], inter[8], inter[9]]
        while ligne != "":
            inter = ligne.strip("\n").split("\t")
            listeinter = [inter[0], inter[3], inter[6], inter[7], inter[8], inter[9]]
            base.append(listeinter)
            i += 1
            ligne = f.readline()

    # Ecriture dans nouveau fichier de la nouvelle base
    with open(motFile, "w") as f:
        f.write("id\tortho\tcgram\tfreqlemfilms\tfreqlemlivres\tfreqfilms\tfreqlivres\n")
        for i in range(len(base)):
            f.write(str(i+1) + '\t' + '\t'.join(base[i]) + "\n")

    pandas.read_csv(motFile, delimiter ="\t").to_sql("MOTS", conn, if_exists='append', index=False)

    os.popen("rm " + motFile) # Supprimer fichier MOTS.csv

    conn.commit()
    conn.close

creation_DbSimple()