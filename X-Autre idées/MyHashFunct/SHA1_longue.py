import hashlib

class MonException(Exception):
    """Exception levée dans un certain contexte… qui reste à définir"""
    def __init__(self, message):
        """On se contente de stocker le message d'erreur"""
        self.message = message
    def __str__(self):
        """On renvoie le message"""
        return self.message

class byte:
    """Classe byte : représente des bits avec des opérations associées
    Sert pour hachage SHA 1"""


    def __init__(self, value = "", nbbits = None):
        """Initialisation d'un byte"""

        if type(value) == type(0):
            # On lui donne un entier en base 10
            str = bin(value)
            str = str[2:]
            lon = len(str)
            if nbbits is not None and nbbits > lon:
                str = "0" * (nbbits - lon) + str
            elif nbbits is not None and nbbits < lon:
                str = str[-32:]
            self._str = str
            self._int = value

        elif type(value) == type(""):
            # On lui donne un str
            if value.replace(" ", "").replace("0", "").replace("1", "") == "":
                # C'est un str d'un nombre binaire
                self._str = value
                self._int = int(self._str, 2)
            else:
                # C'est un str d'un mot : converti en binaire
                bits = ""
                for n in range(len(value)):
                    bits += '{0:08b}'.format(ord(value[n]))
                self._str = bits
                self._int = int(self._str, 2)

        elif type(value) == type(b''):
            # On lui donne un nombre en binaire (type bytes)
            binaire = ""
            for i in value:
                binaire += bin(i)[2:]
            self._str = byte(value.decode('utf-8'))._str
            self._int = int(self._str, 2)

        elif type(value) == type(byte("")):
            # On lui bonne un byte
            self._str = value._str
            self._int = int(self._str, 2)


    def _get_str(self):
        """Montre le byte"""

        return self._str


    def _set_str(self, type):
        """Modifie le byte"""

        self._str = type

    def _del_str(self):
        """Empêche de supprimer le str du byte"""

        print("Vous ne pouvez pas supprimer le str de la liste")

    str = property(_get_str, _set_str, _del_str)


    def __len__(self):
        """Return len(self)"""

        return len(self.str.replace(" ", ""))


    def __repr__(self):
        """Return self"""

        return self.str


    def __add__(self, value):
        """Return self + value"""

        if type(value) == type(""):
            self.str = self.str + value
            return self
        elif type(value) == type(self):
            self.str = self.str + value.str
            return self
        else:
            raise ValueError("Value n'est pas du type byte ou str")


    def __iadd__(self, value):
        """Return self += value"""

        if type(value) == type(""):
            self.str = self.str + value
            return self
        elif type(value) == type(self):
            self.str = self.str + value.str
            return self
        else:
            raise ValueError("value n'est pas du type byte ou str")


    def __and__(self, value):
        """Return self & value"""

        result = byte(self._int & value._int, len(self))
        return result

    def __eq__(self, value):
        """Return self == value"""

        return self.str.replace(" ", "") == value.str.replace(" ", "")


    def __invert__(self):
        """Return ~self"""

        result = byte(~self._int, len(self))
        return result


    def __or__(self, value):
        """Return self | value"""

        result = byte(self._int | value._int, len(self))
        return result


    def __xor__(self, value):
        """Return self ^ value"""

        result = byte(self._int ^ value._int, len(self))
        return result


    def __rshift__(self, value):
        """Return self>>value"""

        result = byte(self.int() >> value, len(self))
        return result


    def __lshift__(self, value):
        """Return self<<value"""

        result = byte(self.int() << value, len(self))
        return result


    def add(self, *value):
        """Addition mod 2**32 des entiers qui correspondent aux mots de 32 bits"""
        intlist = [self._int]
        for i in value:
            intlist.append(i._int)
        result = byte(sum(intlist) , 32)
        return result


    def hexa(self):
        """Converti self en hexadecimal"""

        str = self.str.replace(" ", "")
        a = hex(int(str,2))[2:]
        lon = len(a)
        a = "0" * (40 - lon) + a
        return a


    def normalisation(self):
        """Normalise self :
        - Lui ajoute 1
        - Ajoute le nombre minimal de 0 pour atteindre un multiple de 512-64
        - Ajoute la longueur de self d'origine représenté sur 64 bits"""

        lon = len(self)
        self += "1" + ("0" * (512 - 64 - lon - 1)) + byte(lon, 64).str
        return None


    def find_n(self):
        """Trouve le nombre bits de 512 dans self"""

        if len(self) % 512 != 0:
            raise MonException('len(bit) non multiple de 512 !')
        return len(self) // 512


    def decomposition(self, n):
        """Retourne une liste de str de longueur n du str"""
        return [byte(self.str[i:i+n]) for i in range(0, len(self), n)]


    def int(self):
        return int(self.str, 2)


def S(w, k):
    """Décalage à gauche de k bits
    en permutation circulaire"""

    return byte((w.int() << k) | (w.int() >> (32 - k)), 32)


def f(B, C, D, t):
    """Définition fonction f qui dépend de t, et prend 3 bytes en argument"""

    if t >= 0 and t <= 19:
        return (B & C) | ((~B) & D)
    elif t >= 20 and t <= 39:
        return B ^ C ^ D
    elif t >= 40 and t <= 59:
        return (B & C) | (B & D) | (C & D)
    elif t >= 60 and t <= 79:
        return B ^ C ^ D

def K(t):
    """Définition de la constante K en fonction de t"""

    if t >= 0 and t <= 19:
        return byte(0x5A827999, 32)

    elif t >= 20 and t <= 39:
        return byte(0x6ED9EBA1, 32)

    elif t >= 40 and t <= 59:
        return byte(0x8F1BBCDC, 32)

    elif t >= 60 and t <= 79:
        return byte(0xCA62C1D6, 32)


def sha1(bits):
    """Code bits avec la méthode SHA1"""

    # Initialisation des H
    H = [byte(0x67452301, 32), byte(0xEFCDAB89, 32), byte(0x98BADCFE, 32), byte(0x10325476, 32), byte(0xC3D2E1F0, 32)]
    bits = byte(bits)
    bits.normalisation()
    n = bits.find_n()
    M = bits.decomposition(512)
    for i in range(n):
        W = M[i].decomposition(32)
        for t in range(16, 80):
            W.append(S((W[t-3] ^ W[t-8] ^ W[t-14] ^ W[t-16]), 1))

        [A, B, C, D, E] = H
        for t in range(80):

            T = S(A, 5).add(f(B, C, D, t), E, W[t], K(t))
            E = D
            D = C
            C = S(B, 30)
            B = A
            A = T
        H[0] = H[0].add(A)
        H[1] = H[1].add(B)
        H[2] = H[2].add(C)
        H[3] = H[3].add(D)
        H[4] = H[4].add(E)
    # print(H)
    result = H[0] + H[1] + H[2] + H[3] + H[4]
    return result

passWord = "MotDePasse"

boucle = 1000

import time
start_time = time.time()
for i in range(boucle):
    a = hashlib.sha1(passWord.encode()).hexdigest()
print(a)
print("Temps d'execution fonction test : {}".format(str(time.time() - start_time)))

start_time = time.time()
for i in range(boucle):
    a = sha1(passWord)
print("Temps d'execution ma fonction :{}s".format(str(time.time() - start_time)))
print(a)
