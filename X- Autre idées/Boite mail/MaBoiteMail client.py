# Pseudo-boite mail avec utilisateur : Database : prenom, nom, email, mdp

# Différence client - serveur : Permet de bien voir les différence entre ce à quoi chaque personne à accès

# Le client voit son mot de passe mais jamais la base de donnée

# Le serveur a accès à la base de donnée, mais ne voit jamais le mot de passe

import tkinter as tk
from tkinter import font
import sqlite3
from hashlib import sha256
import re
import socket
import signal
import sys

encodage = 'utf-8' # Encodage des informations à faire transiter
terminaisonMail = "@tipemail.fr" # Fin de l'adresse email

def fermer_programme(signal, frame):
    """Fonction appelée quand vient l'heure de fermer notre programme"""

    print("Fermeture de la connexion")
    connexion_avec_serveur.send(b"fin".encode(encodage))
    connexion_avec_serveur.close()
    sys.exit(1)

# Connexion du signal à notre fonction
signal.signal(signal.SIGINT, fermer_programme)

hote = "localhost"
port = 12800

connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:

    # On tente une connexion au serveur
    connexion_avec_serveur.connect((hote, port))
except ConnectionRefusedError:

    # Le serveur n'est pas ouvert
    serveur = False
else:

    # Le serveur est ouvert
    print("Connexion établie avec le serveur sur le port {}".format(port))
    serveur = True


def connexion():
    """Lors de appui bouton Login
    Vérifie que mail existe dans la base de donnée
    Et que le mot de passe haché et salé corresponde à la base de donnée"""

    global serveur
    if serveur:
        mail = mailEntry.get()
        pass1 = passWordEntry.get()
        connexion_avec_serveur.send(("0$%s"%mail).encode(encodage))
        prenom_nom = connexion_avec_serveur.recv(1024).decode(encodage)
        if prenom_nom is None:
            infoVar.set("Le serveur n'est pas ouvert")
            serveur = False
            return None
        elif prenom_nom == "Vous n'existez pas\ndans la base de donnée":
            infoVar.set(prenom_nom)
            return None
        passWh = sha256((pass1 + prenom_nom).encode(encodage)).hexdigest()
        try:
            connexion_avec_serveur.send((("1${}${}".format(mail, passWh)).encode(encodage)))
        except:
            infoVar.set("Le serveur n'est pas ouvert")
            serveur = False
            return None
        else:
            msg_recu = connexion_avec_serveur.recv(1024).decode(encodage)
            if msg_recu is None:
                infoVar.set("Le serveur n'est pas ouvert")
                serveur = False
            elif msg_recu == "Mauvais mot de passe, désolé":
                infoVar.set(msg_recu)
            else:
                infoVar.set("Bienvenue, {}".format(msg_recu))
            return None
    else:
        infoVar.set("Le serveur n'est pas ouvert")
        return None

def inscription():
    """Lors de appui bouton inscription
    Montrer la fenêtre d'inscritpion, ou la créer si elle a été supprimée"""

    global serveur
    global reg
    if serveur:
        try:
            reg.deiconify()
        except tk.TclError:
            reg = tk.Toplevel(root)
            reg.title("Inscription")

            prenomLabel = tk.Label(reg, text = "Entrez votre prenom", font = police)
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

            infoVar2 = tk.StringVar()
            infoLabel2 = tk.Label(reg, textvariable = infoVar2, font = police)

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
            infoLabel2.grid(column = 0, row = 12)
        return None
    else:
        infoVar.set("Le serveur n'est pas ouvert")
        return None

def confirmer():
    """Lors de appui bouton confirmer
    Enregistre nouvel utilisateur dans la base de donnée
    le mot de passe est salé et haché
    on vérifie que les 2 mots de passe correspondent, et que le mail et unique"""

    global serveur
    if serveur:
        prenom = prenomEntry.get()
        nom = nomEntry.get()
        mail = mailEntry2.get() + terminaisonMail
        pass1 = passWordEntry2.get()
        pass2 = passWordEntry3.get()
        if re.match(r"^([a-z0-9]*[_.-]?)*(@tipemail.fr){1}", mail) is None:
            infoVar2.set("{} ne convient pas :\nlettres_minuscules.ou-12390@tipemail.fr)".format(mail))
        elif pass1 != pass2:
            infoVar2.set("Les mots de passe\nne correspondent pas")
        elif len(pass1) < 6 or pass1.lower() == pass1 or pass1.upper() == pass1:
            infoVar2.set("Votre mot de passe\nn'est pas assez sécurisé")
        else:
            passWh = sha256((pass1 + prenom + nom).encode(encodage)).hexdigest()
            try:
                connexion_avec_serveur.send(("2${}${}${}${}".format(prenom, nom, mail, passWh)).encode(encodage))
                msg_recu = connexion_avec_serveur.recv(1024).decode(encodage)
            except:
                infoVar2.set("Le serveur n'est pas ouvert")
                serveur = False
                return None
            else:
                if msg_recu == "Votre adresse email existe déja":
                    infoVar2.set(msg_recu)
                elif msg_recu == prenom + " " + nom:
                    infoVar2.set("Bienvenue, {}".format(msg_recu))
                else:
                    infoVar2.set("Le serveur n'est pas ouvert")
                    serveur = False
                    return None
        return None
    else:
        infoVar.set("Le serveur n'est pas ouvert")
        return None

def modifier():
    """Lors de appui bouton confirmer
    Enregistre nouvel utilisateur dans la base de donnée
    le mot de passe est salé et haché
    on vérifie que les 2 mots de passe correspondent, et que le mail et unique"""

    global serveur
    if serveur:
        prenom = prenomEntry2.get()
        nom = nomEntry2.get()
        mail = mailEntry4.get() + terminaisonMail
        pass1 = passWordEntry4.get()
        pass2 = passWordEntry5.get()
        if pass1 != pass2:
            infoVar3.set("Les mots de passe\nne correspondent pas")
        elif len(pass1) < 6 or pass1.lower() == pass1 or pass1.upper() == pass1:
            infoVar2.set("Votre mot de passe\nn'est pas assez sécurisé")
        else:
            passWh = sha256((pass1 + prenom + nom).encode(encodage)).hexdigest()
            try:
                connexion_avec_serveur.send(("3${}${}${}${}".format(prenom, nom, mail, passWh)).encode(encodage))
                msg_recu = connexion_avec_serveur.recv(1024).decode(encodage)
            except:
                infoVar3.set("Le serveur n'est pas ouvert")
                serveur = False
                return None
            else:
                if msg_recu == "Vous n'existez pas\ndans la base de donnée":
                    print("lol")
                    infoVar3.set(msg_recu)
                elif msg_recu == prenom + " " + nom:
                    infoVar3.set("Mot de passe modifié, {}".format(msg_recu))
                else:
                    infoVar3.set("Le serveur n'est pas ouvert")
                    serveur = False
                    return None
        return None
    else:
        infoVar.set("Le serveur n'est pas ouvert")
        return None

def oubli():
    global serveur
    global oops
    if serveur:
        try:
            oops.deiconify()
        except tk.TclError:
            oops = tk.Toplevel(root)
            oops.title("Modification")

            prenomLabel2 = tk.Label(oops, text = "Entrez votre prenom", font = police)
            prenomEntry2 = tk.Entry(oops, font = police)

            nomLabel2 = tk.Label(oops, text = "Entrez votre nom", font = police)
            nomEntry2 = tk.Entry(oops, font = police)

            mailLabel4 = tk.Label(oops, text = "Entrez votre mail", font = police)
            mailEntry4 = tk.Entry(oops, font = police)
            mailLabel5 = tk.Label(oops, text = terminaisonMail, font = police)

            passWordLabel4 = tk.Label(oops, text = "Entrez votre nouveau mot de passe", font = police)
            passWordEntry4 = tk.Entry(oops, show="*", font = police)

            passWordLabel5 = tk.Label(oops, text = "Vérifiez votre nouveau mot de passe", font = police)
            passWordEntry5 = tk.Entry(oops, show="*", font = police)

            modifBouton = tk.Button(oops, text = 'Modifier', command = modifier, font = police)

            infoVar3 = tk.StringVar()
            infoLabel3 = tk.Label(oops, textvariable = infoVar3, font = police)

            prenomLabel2.grid(column = 0, row = 1)
            prenomEntry2.grid(column = 0, row = 2)
            nomLabel2.grid(column = 0, row = 3)
            nomEntry2.grid(column = 0, row = 4)
            mailLabel4.grid(column = 0, row = 5)
            mailEntry4.grid(column = 0, row = 6)
            mailLabel5.grid(column = 1, row = 6)
            passWordLabel4.grid(column = 0, row = 7)
            passWordEntry4.grid(column = 0, row = 8)
            passWordLabel5.grid(column = 0, row = 9)
            passWordEntry5.grid(column = 0, row = 10)
            modifBouton.grid(column = 0, row = 11)
            infoLabel3.grid(column = 0, row = 12)
        return None
    else:
        infoVar.set("Le serveur n'est pas ouvert")
        return None

if serveur:

    # Alors le serveur est toujours ouvert

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
    oubliBouton = tk.Button(root, text = 'Mot de passe oublié', command = oubli, font = police)

    infoVar = tk.StringVar()
    infoLabel = tk.Label(root, textvariable = infoVar, font = police)

    mailLabel.grid(column = 0, row = 1)
    mailEntry.grid(column = 0, row = 2)
    passWordLabel.grid(column = 0, row = 3)
    passWordEntry.grid(column = 0, row = 4)
    connectBouton.grid(column = 0, row = 5)
    inscriBouton.grid(column = 0, row = 6)
    oubliBouton.grid(column = 0, row = 7)
    infoLabel.grid(column = 0, row = 8)


    # Fenêtre d'enregistrement

    reg = tk.Toplevel(root)
    reg.title("Inscription")

    prenomLabel = tk.Label(reg, text = "Entrez votre prenom", font = police)
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

    infoVar2 = tk.StringVar()
    infoLabel2 = tk.Label(reg, textvariable = infoVar2, font = police)

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
    infoLabel2.grid(column = 0, row = 12)

    reg.withdraw()

    # Fenêtre d'oubli

    oops = tk.Toplevel(root)
    oops.title("Modification")

    prenomLabel2 = tk.Label(oops, text = "Entrez votre prenom", font = police)
    prenomEntry2 = tk.Entry(oops, font = police)

    nomLabel2 = tk.Label(oops, text = "Entrez votre nom", font = police)
    nomEntry2 = tk.Entry(oops, font = police)

    mailLabel4 = tk.Label(oops, text = "Entrez votre mail", font = police)
    mailEntry4 = tk.Entry(oops, font = police)
    mailLabel5 = tk.Label(oops, text = terminaisonMail, font = police)

    passWordLabel4 = tk.Label(oops, text = "Entrez votre nouveau mot de passe", font = police)
    passWordEntry4 = tk.Entry(oops, show="*", font = police)

    passWordLabel5 = tk.Label(oops, text = "Vérifiez votre nouveau mot de passe", font = police)
    passWordEntry5 = tk.Entry(oops, show="*", font = police)

    modifBouton = tk.Button(oops, text = 'Modifier', command = modifier, font = police)

    infoVar3 = tk.StringVar()
    infoLabel3 = tk.Label(oops, textvariable = infoVar3, font = police)

    prenomLabel2.grid(column = 0, row = 1)
    prenomEntry2.grid(column = 0, row = 2)
    nomLabel2.grid(column = 0, row = 3)
    nomEntry2.grid(column = 0, row = 4)
    mailLabel4.grid(column = 0, row = 5)
    mailEntry4.grid(column = 0, row = 6)
    mailLabel5.grid(column = 1, row = 6)
    passWordLabel4.grid(column = 0, row = 7)
    passWordEntry4.grid(column = 0, row = 8)
    passWordLabel5.grid(column = 0, row = 9)
    passWordEntry5.grid(column = 0, row = 10)
    modifBouton.grid(column = 0, row = 11)
    infoLabel3.grid(column = 0, row = 12)

    oops.withdraw()

    root.mainloop()

    connexion_avec_serveur.send("fin".encode(encodage))
    print("Fermeture de la connexion")
    connexion_avec_serveur.close()

else:

    # Alors le serveur n'est pas ouvert

    print("Le serveur n'est pas ouvert")
    print("Contactez le responsable du serveur pour plus d'informations")