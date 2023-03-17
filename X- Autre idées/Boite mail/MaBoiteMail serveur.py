# Pseudo-boite mail avec utilisateur : Database : prenom, nom, email, mdp

# Différence client - seerveur : Permet de bien voir les différence entre ce à quoi chaque personne à accès

# Le serveur a accès à la base de donnée, mais ne voit jamais le mot de passe

# Le client voit son mot de passe mais jamais la base de donnée

import tkinter as tk
import sqlite3
from hashlib import sha256
import socket
import select
import signal
import sys

encodage = 'utf-8' # Encodage des informations à faire transiter
database = "MaBoiteMail.db" # Nom de la base de donnée

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

def fermer_programme(signal, frame):
    """Fonction appelée quand vient l'heure de fermer notre programme"""

    print("Fermeture des connexions")
    conn.commit()
    conn.close
    for client in clients_connectes:
        client.close()
        client.send("fin".encode(encodage))

    connexion_principale.close()
    sys.exit(1)

# Connexion du signal à notre fonction
signal.signal(signal.SIGINT, fermer_programme)

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

hote = ''
port = 12800

connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_principale.bind((hote, port))
connexion_principale.listen(5)
print("Le serveur écoute à présent sur le port {}".format(port))

serveur_lance = True
clients_connectes = []
while serveur_lance:
    # On va vérifier que de nouveaux clients ne demandent pas à se connecter
    # Pour cela, on écoute la connexion_principale en lecture
    # On attend maximum 50ms
    connexions_demandees, wlist, xlist = select.select([connexion_principale],
        [], [], 0.05)

    for connexion in connexions_demandees:
        connexion_avec_client, infos_connexion = connexion.accept()
        # On ajoute le socket connecté à la liste des clients
        clients_connectes.append(connexion_avec_client)

    # Maintenant, on écoute la liste des clients connectés
    # Les clients renvoyés par select sont ceux devant être lus (recv)
    # On attend là encore 50ms maximum
    # On enferme l'appel à select.select dans un bloc try
    # En effet, si la liste de clients connectés est vide, une exception
    # Peut être levée
    clients_a_lire = []
    try:
        clients_a_lire, wlist, xlist = select.select(clients_connectes, [], [], 0.05)
    except select.error:
        pass
    else:
        # On parcourt la liste des clients à lire
        for client in range(len(clients_a_lire)):
            msg_recu = clients_a_lire[client].recv(1024)
            msg_recu = msg_recu.decode(encodage).split("$")
            # msg_recu est une liste contenant tout les messages envoyés pas le client
            print("Reçu {}".format(str(msg_recu)))
            if msg_recu[0] == "0":
                # Test mail existe dans la base de donnée
                cur.execute("""SELECT nom, prenom FROM utilisateur WHERE email = ?""", (msg_recu[1],))
                count = 0
                prenom = None
                for i in cur.fetchall():
                    nom = i[0]
                    prenom = i[1]
                    count += 1
                if prenom is None:
                    # Mail non présent dans la base de donnée
                    print("pas là")
                    clients_a_lire[client].send("Vous n'existez pas\ndans la base de donnée".encode(encodage))
                else:
                    # Mail present dans la base de donnée : le renvoie au client
                    clients_a_lire[client].send((prenom + nom).encode(encodage))

            elif msg_recu[0] == "1":
                # Test mot de passe correspond à l'utilisateur
                # Il ne recoit pas le mot de passe en clair, mais seulement le mot de passe haché/salé
                cur.execute("""SELECT nom, prenom FROM utilisateur WHERE email = ? and mdp = ?""", (msg_recu[1], msg_recu[2]))
                gus = cur.fetchall()
                if len(gus) == 1:
                    # Il existe un unique utilisateur avec cette adresse email et ce mot de passe
                    # On renvoie le nom d'utilisateur de la personne
                    for name in gus:
                        nom = name[0]
                        prenom = name[1]
                    clients_a_lire[client].send((prenom + " " + nom).encode(encodage))
                else:
                    # Les informations ne correspondent a aucun utilisateur
                    # On envoie un message d'erreur
                    clients_a_lire[client].send("Mauvais mot de passe, désolé".encode(encodage))

            elif msg_recu[0] == "2":
                # Inscription
                # On vérifie que l'adresse email n'existe pas déjà
                [truc, prenom, nom, mail, passWh] = msg_recu
                cur.execute("""SELECT count(*) FROM utilisateur WHERE email = ?""", (mail,))
                gus = cur.fetchone()
                for lon in gus:
                    lon = lon
                if lon == 0:
                    # Mail unique : on créer le nouvel utilisateur avec les informations données
                    # Mot de passe déjà haché et salé : le serveur ne voit pas en clair le mot de passe
                    cur.execute("""
                        INSERT INTO
                        utilisateur
                        (prenom, nom, email, mdp)
                        VALUES(?, ?, ?, ?);""",(prenom, nom , mail , passWh))
                    conn.commit()
                    clients_a_lire[client].send((prenom + " " + nom).encode(encodage))

            elif msg_recu[0] == "3":
                # Modification mot de passe
                # On vérifie que l'utilisateur existe
                [truc, prenom, nom, mail, passWh] = msg_recu
                cur.execute("""SELECT count(*) FROM utilisateur WHERE email = ? AND prenom = ? and nom = ?""", (mail, prenom, nom))
                gus = cur.fetchone()
                for lon in gus:
                    lon = lon
                if lon == 1:
                    # Utilisateur existe : on modifie son mot de passe
                    # Mot de passe déjà haché et salé : le serveur ne voit pas en clair le mot de passe
                    # Bien sur en vrai, il n'est pas aussi facile de modifier son mot de passe
                    # Le site vérifie que nous sommes la bonne personne avec d'autres moyens de confirmations
                    cur.execute("""
                        UPDATE utilisateur
                        SET mdp = ?
                        WHERE prenom = ? AND nom = ? AND email = ?;""",
                        (passWh, prenom, nom , mail))
                    conn.commit()
                    print("modif effectuée")
                    clients_a_lire[client].send((prenom + " " + nom).encode(encodage))
                else:
                    # Email n'existe pas déjà dans base de donnée
                    print("modif pas effectuée")
                    clients_a_lire[client].send("Vous n'existez pas\ndans la base de donnée".encode(encodage))

            if msg_recu == ["fin"]:
                # Client se déconnecte
                clients_a_lire[client].close()
                del clients_connectes[client]

conn.commit()
conn.close