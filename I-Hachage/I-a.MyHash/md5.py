# -*- coding: utf8 -*-

# MD5

# Implémentation manuelle d'une fonctions de hachages très utilisée : MD5
# Plus long que la fonction de python
# Tous est fait sur des entiers sauf la normalisation qui travaille sur les nombres en binaire

import math

def ROTL(x, n):
    """Opération de rotation binaire vers la gauche"""

    return (x << n) | x >> (32 - n)

def decomposition(l, n):
    """Décomposition de l en une liste d'entier de longueur n"""

    return [int(l[i:i+n], 2) for i in range(0, len(l), n)]

def normalisation(mot):
    """Normalise mot :
    - Le converti en bits
    - Lui ajoute 1
    - Ajoute le nombre minimal de 0 pour atteindre un multiple de 512-64
    - Retourne les bits pour être en little endian
    - Ajoute la longueur de self d'origine représenté sur 64 bits codé en little endian"""

    # Conversion en bits
    x = ""
    for n in range(len(mot)):
        x += format(ord(mot[n]),'08b')
    lon = len(x)
    # Ajout 1
    x += "1"
    # Ajout nb 0
    while len(x) % 512 != 448:
        x += "0"
    x2 = ""
    a = 32
    # Retourner les bits en little endian
    for i in range(0, len(x), a):
        a, b, c, d, e = i, i+8, i+16, i+24, i+32
        x2 += x[d : e] + x[c : d] + x[b : c] + x[a : b]
    # Ajout longueur
    l = format(lon,'064b')
    x2 += l[32:] + l[:32]
    return x2

def toHex(value):
    """Converti un entier en hexadécimal en l'inversant"""

    value = hex(value)
    diff = len(value) - 8
    value = value[diff:]
    return ''.join([value[i*2:(i+1)*2] for i in reversed(range(len(value)//2))])

def md5(mot):
    """ Fonction MD5"""

    r = [7, 12, 17, 22] * 4 + [5, 9, 14, 20] * 4 + [4, 11, 16, 23] * 4 + [6, 10, 15, 21] * 4
    K = [int(abs((2**32) * math.sin(i + 1))) for i in range(64)]

    x = normalisation(mot)
    x = decomposition(x, 32)

    A, B, C, D = 0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476

    for j in range(0, len(x), 16):
        a, b, c, d = A, B, C, D

        for t in range(64):
            if t >= 0 and t < 16:
                f = (B & C) | ((~B) & D)
                g = t
            elif t >= 16 and t < 32:
                f = (B & D) | (C & (~D))
                g = (5 * t + 1) % 16
            elif t >= 32 and t < 48:
                f = B ^ C ^ D
                g = (3 * t + 5) % 16
            elif t >= 48 and t < 64:
                f = C ^ (B | (~D))
                g = (7 * t) % 16

            new_B = (A + f + x[j + g] + K[t]) % 2**32
            new_B = (ROTL(new_B, r[t]) % 2**32) + B

            A, B, C, D = D, new_B, B, C

        A = (a + A) % 2**32
        B = (b + B) % 2**32
        C = (c + C) % 2**32
        D = (d + D) % 2**32

    return toHex(A) + toHex(B) + toHex(C) + toHex(D)

mot = "Demain"

print(md5(mot)) # b3a46a9f4cbf9bd55c64602ae9b70476

import hashlib
print(hashlib.md5(mot.encode('utf-8')).hexdigest()) # b3a46a9f4cbf9bd55c64602ae9b70476