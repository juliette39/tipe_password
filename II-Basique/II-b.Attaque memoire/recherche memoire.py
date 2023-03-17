import sqlite3
import hashlib
import time

def est_bon_mot(mot_de_passe, mot_haché):
    """Renvoie si mot_de_passe est bien l'antécédent de mot_haché avec la fonction du hachage"""
    return hachage(mot_de_passe) == mot_haché

def hachage(mot):
    """hash mot avec une fonction de hachage"""

    return hashlib.md5(mot.encode('utf8')).hexdigest()

def rechercheM(database, hash):
    conn = sqlite3.connect(database)
    cur = conn.cursor()

    cur.execute("""SELECT mot FROM Memoire WHERE hash = '{}'""".format(hash))
    mot = cur.fetchone()[0]
    conn.close
    return mot

# caracteres = 'abcdefghijklmnopqrstuvwxyz'
# mot = "TiP3"
# mothash = hachage(mot)

# longueur = 4
# database = "/Users/juliettedebono/Documents/MP*/TIPE/II- Basique/II- b) Attaque memoire/Memoire{}.sqlite".format(longueur)

# t = time.time()
# print(rechercheM(database, mothash))
# print("Temps pour recherche dans table mémoire : {} secondes".format(time.time() - t))