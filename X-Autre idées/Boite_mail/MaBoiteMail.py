# Pseudo-boite mail avec utilisateur : Database : prenom, nom, email, mdp

import tkinter as tk
from tkinter import font
import sqlite3
from hashlib import sha256
import re

database = "MaBoiteMail.db"
terminaisonMail = "@tipemail.fr" # Fin de l'adresse email

def creerDataBase():
    """Créer un base de donnée pour stocker les mots de passe vide"""

    cur.execute(
    """
    CREATE TABLE "utilisateur" (
        "id" INTEGER NOT NULL UNIQUE,
        "prenom" TEXT NOT NULL,
        "nom" TEXT NOT NULL,
        "email" TEXT NOT NULL UNIQUE,
        "mdp" TEXT NOT NULL UNIQUE,
        PRIMARY KEY("id" AUTOINCREMENT));
    """)
    conn.commit()
    cur.execute(
    """
    CREATE TRIGGER validate_email_before_insert_utilisateur
    BEFORE INSERT ON utilisateur
    BEGIN
    SELECT
        CASE
        WHEN NEW.email NOT LIKE '%_@tipemail.fr' THEN
        RAISE (ABORT,'Invalid email address')
        END;
    END;""")
    conn.commit()
    return None

# Connexion base de donnée
conn = sqlite3.connect(database)
cur = conn.cursor()

# Création base de donnée si n'existe pas déja
try:
    cur.execute("""
        INSERT INTO
        utilisateur
        (prenom, nom, email, mdp)
        VALUES(?, ?, ?, ?);""",("prenom", "nom" , "email" , "mdp"))
except sqlite3.OperationalError:
    creerDataBase()
except sqlite3.IntegrityError:
    None

def connexion():
    """Lors de appui bouton Login
    Vérifie que mail existe dans la base de donnée
    Et que le mot de passe haché et salé corresponde à la base de donnée"""

    mail = mailEntry.get()
    pass1 = passWordEntry.get()
    cur.execute("""SELECT prenom, nom FROM utilisateur WHERE email = ?""", (mail,))
    count = 0
    for i in cur.fetchall():
        name = i[0] + " " + i[1]
        count += 1
    if count != 1:
        print("Vous n'existez pas dans la base de donnée")
        return None
    passWh = sha256((pass1 + name).encode('utf-8')).hexdigest()
    cur.execute("""SELECT prenom, nom FROM utilisateur WHERE email = ? and mdp = ?""", (mail, passWh))
    gus = cur.fetchall()
    if len(gus) == 1:
        for name in gus:
            name = name[0] + " " + name[1]
            print("Bienvenue, {}".format(name))
    else:
        print("Mauvais mot de passe, désolé")


def inscription():
    """Lors de appui bouton inscription
    Montrer la fenêtre d'inscritpion, ou la créer si elle a été supprimée"""

    global reg

    try:
        reg.deiconify()

    except tk.TclError:

        reg = tk.Toplevel(root)
        reg.title("Inscription")

        prenomLabel = tk.Label(reg, text = "Entrez votre prénom", font = police)
        prenomEntry = tk.Entry(reg, font = police)

        nomLabel = tk.Label(reg, text = "Entrez votre nom", font = police)
        nomEntry = tk.Entry(reg, font = police)

        mailLabel2 = tk.Label(reg, text = "Entrez votre mail", font = police)
        mailEntry2 = tk.Entry(reg, font = police)
        mailLabel3 = tk.Label(reg, text = terminaisonMail, font = police)

        passWordLabel2 = tk.Label(reg, text = "Entrez votre mot de passe", font = police)
        passWordEntry2 = tk.Entry(reg, show="*", font = police)

        passWordLabel3 = tk.Label(reg, text = "Vérifiez votre mot de passe", font = police)
        passWordEntry3 = tk.Entry(reg, show="*", font = police)

        confirmBouton = tk.Button(reg, text = 'Confirmez', command = confirmer, font = police)

        prenomLabel.grid(column = 0, row = 1)
        prenomEntry.grid(column = 0, row = 2)
        nomLabel.grid(column = 0, row = 3)
        nomEntry.grid(column = 0, row = 4)
        mailLabel2.grid(column = 0, row = 5)
        mailEntry2.grid(column = 0, row = 6)
        mailLabel3.grid(column = 1, row = 6)
        passWordLabel2.grid(column = 0, row = 7)
        passWordEntry2.grid(column = 0, row = 8)
        passWordLabel3.grid(column = 0, row = 9)
        passWordEntry3.grid(column = 0, row = 10)
        confirmBouton.grid(column = 0, row = 11)


def confirmer():
    """Lors de appui bouton confirmer
    Enregistre nouvel utilisateur dans la base de donnée
    le mot de passe est salé et haché
    on vérifie que les 2 mots de passe correspondent, et que le mail et unique"""

    prenom = prenomEntry.get()
    nom = nomEntry.get()
    mail = mailEntry2.get() + terminaisonMail
    pass1 = passWordEntry2.get()
    pass2 = passWordEntry3.get()
    if re.match(r"^([a-z0-9]*[_.-]?)*(@tipemail.fr){1}", mail) is None:
        print("L'adresse email ne convient pas :\nlettre_minuscules.ou-12390@tipemail.fr)")
    elif pass1 != pass2:
        print("Les mots de passe ne correspondent pas")
    elif len(pass1) < 6 or pass1.lower() == pass1 or pass1.upper() == pass1:
        print("Votre mot de passe n'est pas assez sécurisé")
    else:
        passWh = sha256((pass1 + name).encode('utf-8')).hexdigest()
        cur.execute("""SELECT count(*) FROM utilisateur WHERE email = ?""", (mail,))
        gus = cur.fetchall()
        for name2 in gus:
            lon = name2[0]
        if lon == 0:
            cur.execute("""
                INSERT INTO
                utilisateur
                (prenom, nom, email, password)
                VALUES(?, ?, ?, ?);""",(prenom, nom , mail , passWh))
            conn.commit()

            print("Bienvenue, {}".format(prenom + " " + nom))
        else:
            print("Votre adresse email existe déja")
    return None

# Création fenêtre visuelle

root=tk.Tk()
root.title("Connexion")

police = font.Font(root, size = 20, family = 'Arial')


mailLabel = tk.Label(root, text = "Entrez votre mail", font = police)
mailEntry = tk.Entry(root, font = police)

passWordLabel = tk.Label(root, text = "Entrez votre mot de passe", font = police)
passWordEntry = tk.Entry(root, show="*", font = police)

connectBouton = tk.Button(root, text = "Connexion", command = connexion, font = police)
inscriBouton = tk.Button(root, text = "Inscription", command = inscription, font = police)

mailLabel.grid(column = 0, row = 1)
mailEntry.grid(column = 0, row = 2)
passWordLabel.grid(column = 0, row = 3)
passWordEntry.grid(column = 0, row = 4)
connectBouton.grid(column = 0, row = 5)
inscriBouton.grid(column = 0, row = 6)

# Fenêtre d'enregistrement (caché au début)
reg = tk.Toplevel(root)
reg.title("Inscription")

prenomLabel = tk.Label(reg, text = "Entrez votre prénom", font = police)
prenomEntry = tk.Entry(reg, font = police)

nomLabel = tk.Label(reg, text = "Entrez votre nom", font = police)
nomEntry = tk.Entry(reg, font = police)

mailLabel2 = tk.Label(reg, text = "Entrez votre mail", font = police)
mailEntry2 = tk.Entry(reg, font = police)
mailLabel3 = tk.Label(reg, text = terminaisonMail, font = police)

passWordLabel2 = tk.Label(reg, text = "Entrez votre mot de passe", font = police)
passWordEntry2 = tk.Entry(reg, show="*", font = police)

passWordLabel3 = tk.Label(reg, text = "Vérifiez votre mot de passe", font = police)
passWordEntry3 = tk.Entry(reg, show="*", font = police)

confirmBouton = tk.Button(reg, text = 'Confirmez', command = confirmer, font = police)

prenomLabel.grid(column = 0, row = 1)
prenomEntry.grid(column = 0, row = 2)
nomLabel.grid(column = 0, row = 3)
nomEntry.grid(column = 0, row = 4)
mailLabel2.grid(column = 0, row = 5)
mailEntry2.grid(column = 0, row = 6)
mailLabel3.grid(column = 1, row = 6)
passWordLabel2.grid(column = 0, row = 7)
passWordEntry2.grid(column = 0, row = 8)
passWordLabel3.grid(column = 0, row = 9)
passWordEntry3.grid(column = 0, row = 10)
confirmBouton.grid(column = 0, row = 11)

reg.withdraw()

root.mainloop()

conn.commit()
conn.close