import sqlite3
import hashlib

database = "./Mots.sqlite"

def hachage(mot):
    """hash mot avec md5"""
    return hashlib.new('md5', mot.encode('utf-8')).hexdigest()

def recherche(hash):

    conn = sqlite3.connect(database)
    cur = conn.cursor()

    cur.execute("""SELECT ortho FROM MOTS ORDER BY freqlemfilms DESC""")
    liste = cur.fetchall()
    for mot in liste:
        mot = mot[0]
        if mot is not None and hachage(mot) == hash:
            return mot

mot = "mot"
print(recherche(hachage(mot)))
