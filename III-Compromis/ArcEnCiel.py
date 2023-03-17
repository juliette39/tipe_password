"""
Classe ArcEnciel

Contient * les données pour les tables de compromis temps-mémoires
         * les fonctions pour générer une table ou rechercher un mot dedans
TIPE
"""

import hashlib
import random as rd
import sqlite3
import numpy as np

__version__ = "1.1.1"
__author__ = "Juliette Debono"

class ArcEnCiel:
    """Classe pour générer une table de compromis temps-mémoires
    Objet avec attributs : informations nécéssaires pour créer la table
    Fonctions : fonctions de base pour créer la table
    """

    def __init__(self, m : int, t : int, l : int, t_min : int, t_max : int, carac : str, type : bool, database : str, hachage : 'function') -> None:
        """Création d'un objet contenant les informations :
        ** Informations directements transmises :
        * m : Nombre de lignes de la base de données
        * t : Nombre de fois qu'on applique la réduction
        * l : Nombre de tables
        * t_min : longueur minimale des mots de passe possibles
        * t_max : longueur maximale des mots de passe possibles
        * carac : Liste des caractères possibles
        * type : Type de la table : ArcEnCiel ou Classique
        * database : Nom de la base de données
        * hachage : Fonction de hachage utilisée
        ** Généré à partir des autres valeurs :
        * N : nombre de mots possible avec les caractéristiques données
              (nombre de caractère et longueur des mots de passe)
        * nblettres : Nombre de caractères dans la chaine carac
        * couverture : Pourcentage de succès qu'un mot soit dans la table
        """

        nblettres = len(carac)
        N = sum([nblettres**i for i in range(t_min, t_max+1)])

        self._m = m
        self._t = t
        self._l = l
        self._type = type
        self._t_min = t_min
        self._t_max = t_max
        self._carac = carac
        self._database = database
        self._hachage = hachage
        self._N = N
        self._nblettres = nblettres
        self._couverture = self.couv()


    def __repr__(self) -> str:
        """Montrer l'objet"""
        return """N : {}
t : {}
m : {}
l : {}
lettre entre {} et {}
couverture = {}
database : {}
carac : {}
hachage : {}
nblettres : {}""".format(self.N, self.t, self.m, self.l, self.t_min, self.t_max, self.couverture, self.database, self.carac, self.hachage, self.nblettres)

    def _impossible(self, *args):
        """Empêche de supprimer / modifier un attribut"""
        print("Impossible")

    def _get_m(self):
        """Retourne m"""
        return self._m

    def _set_m(self, m):
        """Modifie m"""
        self._m = m
        self._couverture = self.couv()

    m = property(_get_m, _set_m, _impossible)


    def _get_t(self):
        """Retourne t"""
        return self._t

    def _set_t(self, t):
        """Modifie t"""
        self._t = t
        self._couverture = self.couv()

    t = property(_get_t, _set_t, _impossible)


    def _get_l(self):
        """Retourne l"""
        return self._l

    def _set_l(self, l):
        """Modifie T"""
        self._l = l

    l = property(_get_l, _set_l, _impossible)


    def _get_t_min(self):
        """Retourne t_min de mots de passe possibles"""
        return self._t_min

    def _set_t_min(self, t_min):
        """Modifie t_min"""
        self._t_min = t_min
        self._N = sum([self.nblettres**i for i in range(self._t_min, self._t_max+1)])
        self._couverture = self.couv()

    t_min = property(_get_t_min, _set_t_min, _impossible)


    def _get_t_max(self):
        """Retourne les tailles de mots de passe possibles"""
        return self._t_max

    def _set_t_max(self, t_max):
        """Modifie taille"""
        self._t_max = t_max
        self._N = sum([self.nblettres**i for i in range(self._t_min, self._t_max+1)])
        self._couverture = self.couv()

    t_max = property(_get_t_max, _set_t_max, _impossible)

    def _get_type(self):
        """Retourne type"""
        return self._type

    def _set_type(self, type):
        """Modifie type"""
        self._type = type
        self._couverture = self.couv()
        self._database = "/Users/juliettedebono/Documents/MP*/TIPE/III- Compromis/III- {5}) {0}/Tables/{0} t = {1} m = {2} l = {3} len = {4}.sqlite".format("{0}", self._t, self._m, self._l, self._t_max, lettre(type))


    type = property(_get_type, _set_type, _impossible)


    def _get_carac(self):
        """Retourne les caractères possibles"""
        return self._carac

    def _set_carac(self, carac):
        """Modifie carac"""
        self._carac = carac
        self._nblettres = len(carac)
        self._N = sum([self.nblettres**i for i in range(self._t_min, self._t_max+1)])

    carac = property(_get_carac, _set_carac, _impossible)


    def _get_database(self):
        """Retourne le nom de la base de données"""
        return self._database.format(self.type)

    def _set_database(self, database):
        """Modifie database"""
        self._database = database

    database = property(_get_database, _set_database, _impossible)


    def _get_hachage(self):
        """Retourne la fonction de hachage"""
        return self._hachage

    def _set_hachage(self, hachage):
        """Modifie la fonction de hachage"""
        self._hachage = hachage

    hachage = property(_get_hachage, _set_hachage, _impossible)

    def _get_couverture(self):
        """Retourne la valeur de la couverture"""
        return self._couverture

    couverture = property(_get_couverture, _impossible, _impossible)


    def _get_N(self):
        """Retourne N"""
        return self._N

    N = property(_get_N, _impossible, _impossible)


    def _get_nblettres(self):
        """Retourne le nombre de lettres"""
        return self._nblettres

    nblettres = property(_get_nblettres, _impossible, _impossible)


    def couv(self):
        """Renvoie la couverture de datas : le pourcentage de valeur contenue dans la table type"""

        if self.type == 'ArcEnCiel':
            m = self.m
            v = 1.0
            for _ in range(self.t):
                v *= (1 - m / self.N)
                m = self.N * (1 - np.exp(-m/self.N))
            p = (1 - (v**self.l))
            return round(100 * p, 2)
        else:
            if self.m * (self.t**2) < 10 * self.N:
                p = (self.m*self.t*self.l)/self.N
                return round(100 * p, 2)
            else:
                p = 0.8 * ((self.m*self.t*self.l)/self.N)
                return round(100 * p, 2)


    def ialea(self, tableName, l) -> int:
        """Indice aléatoire de départ d'une ligne"""

        conn = sqlite3.connect(self.database.format(tableName))
        cur = conn.cursor()
        i = 0

        def inter(cur, conn, tableNamel, l, i):
            """Choisi indice aleatoire qui n'est pas dans la table : si il y est : récursion"""
            i_0 = rd.randint(0, self.N - 1)

            cur.execute("""SELECT * FROM {}{} WHERE i_0 = ?""".format(tableName, l),(i_0,))

            if cur.fetchone() is None:
                return i_0
            else:
                i += 1
                try:
                    return inter(cur, conn, tableName, l, i)
                except RecursionError:
                    return rd.randint(0, self.N)

        i_0 = inter(cur, conn, tableName, l, i)
        conn.close
        return i_0


    def i2c(self, i : int) -> str:
        """Convertit i en base 10 en x en base len(carac) avec la liste de caractères carac"""

        l = self.nblettres
        N = sum([l**i for i in range(1, self.t_min)])
        i += N

        result = self.carac[i % l]
        i = (i//l) - 1

        while i > -1 and len(result) < self.t_max+1:
            i, result = (i // l) - 1, self.carac[i % l] + result

        return result


    def h(self, c : str) -> str:
        """hash c avec une fonction de hachage de nom hachage[0] et d'encodage hachage[1]"""

        return hashlib.new(self.hachage[0], c.encode(self.hachage[1])).hexdigest()


    def h2i(self, h : str, t : int) -> int :
        """Transforme un hash en indice"""

        h = str(h)
        return (int(h, 16) + t) % self.N


    def h2h(self, h1 : int, t : int) -> str:
        """Passe d'un hash au suivant et renvoie le clair et le hash"""

        i2 = self.h2i(h1, t)
        c2 = self.i2c(i2)
        h2 = self.h(c2)
        return c2, h2


    def i2i(self, i1 : int, t : int) -> int:
        """Réalise la génération de l'indice d'après avec les fonctions préalablement établies"""

        c1 = self.i2c(i1)
        h1 = self.h(c1)
        i2 = self.h2i(h1, t)
        return i2


    def pick(self) -> str:
        """Choisi un hash stocké dans la table aléatoirement"""

        conn = sqlite3.connect(self.database)
        cur = conn.cursor()

        l = rd.randint(0, self.l - 1)

        cur.execute("""SELECT i_0 FROM {}{} ORDER BY RANDOM()""".format(self.type, l))

        a = cur.fetchone()[0]
        conn.close
        for i in range(rd.randint(1, self.t - 1)):
            if self.type != "ArcEnCiel":
                i = l
            else:
                i += 1
            a = self.i2i(a, i)
        return self.i2c(a)

# Informations :

carac = 'abcdefghijklmnopqrstuvwxyz'+'abcdefghijklmnopqrstuvwxyz'.upper() + '0123456789'
t_min = 4
t_max = t_min
t = 1000
m = 100000
l = 1
type = "ArcEnCiel"

hachage = 'md5', 'utf-8' # md5

lettre = lambda a : "b" if a == 'ArcEnCiel' else "a"

database = "/Users/juliettedebono/Documents/MP*/TIPE/III- Compromis/III- {5}) {0}/Tables/{0} t = {1} m = {2} l = {3} len = {4}.sqlite".format("{0}", t, m, l, t_max, lettre(type))

datas = ArcEnCiel(m, t, l, t_min, t_max, carac, type, database, hachage) # Objet contenant les informations
del carac, type, t, m, l, hachage, database, t_min, t_max # Suppression valeurs inutiles
print(datas)