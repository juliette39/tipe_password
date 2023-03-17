# -*- coding: utf8 -*-

# MD5, SHA1, SHA224, SHA256, SHA384, SHA512

# Implémentation manuelle des fonctions de hachages très utilisées : SHA1 et SHA256
# Plus long que les fonctions de python
# Tous est fait sur des entiers sauf la normalisation qui travaille sur les nombres en binaire

# Fonctions utiles pour les fonctions de hachage :

# Spécifique à SHA1 et MD5 :

def ROTL(x, n):
    """Utile pour SHA1 et MD5
    Opération de rotation binaire vers la gauche"""

    return (x << n) | x >> (32 - n)

def normalisation2(mot):
    """Utile pour MD5
    Normalise mot :
    - Le converti en bits
    - Lui ajoute 1
    - Ajoute le nombre minimal de 0 pour atteindre un multiple de 512-64
    - Ajoute la longueur de self d'origine représenté sur 64 bits"""

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

# Spécifiques à SHA256 :

def ROTR(x, n):
    """Utile pour SHA256
    Opération de rotation binaire vers la droite"""

    return (x >> n) | x << (32 - n)


def Ch(x, y, z):
    """Utile pour SHA256"""

    return (x & y) ^ (~x & z)


def Maj(x, y, z):
    """Utile pour SHA256"""

    return (x & y) ^ (x & z) ^ (y & z)


def SIGMA0(x):
    """Utile pour SHA256"""

    return ROTR(x, 2) ^ ROTR(x, 13) ^ ROTR(x, 22)


def SIGMA1(x):
    """Utile pour SHA256"""

    return ROTR(x, 6) ^ ROTR(x, 11) ^ ROTR(x, 25)


def sigma0(x):
    """Utile pour SHA256"""

    return ROTR(x, 7) ^ ROTR(x, 18) ^ (x >> 3)


def sigma1(x):
    """Utile pour SHA256"""

    return ROTR(x, 17) ^ ROTR(x, 19) ^ (x >> 10)


# Commune aux fonctions :

def decomposition(l, n):
    """Utile pour SHA1 et SHA256
    décomposition de l en une liste de str de longueur n"""

    return [int(l[i:i+n], 2) for i in range(0, len(l), n)]

def normalisation(mot):
    """Utile pour SHA1 et SHA256
    Normalise mot :
    - Le converti en bits
    - Lui ajoute 1
    - Ajoute le nombre minimal de 0 pour atteindre un multiple de 512-64
    - Ajoute la longueur de self d'origine représenté sur 64 bits"""

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
    # Ajout longueur
    x += format(lon,'064b')
    return x


import math

def toHex(value):
    """Utile pour MD5
    Converti un entier en hexadécimal à l'envers"""

    value = hex(value)
    diff = len(value) - 8
    value = value[diff:]
    return ''.join([value[i*2:(i+1)*2] for i in reversed(range(len(value)//2))])


def md5(mot):
    """ Fonction MD5, fonction de hachage
    Utilise les fonctions:
    - normalisation2
    - ROTL
    - wordToHex
    """

    r = [7, 12, 17, 22] * 4 + [5, 9, 14, 20] * 4 + [4, 11, 16, 23] * 4 + [6, 10, 15, 21] * 4
    K = [int(abs((2**32) * math.sin(i + 1))) for i in range(64)]

    x = decomposition(normalisation2(mot), 32)

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


def sha1(mot):
    """ Fonction SHA1, fonction de hachage
    Utilise les fonctions:
    - normalisation
    - decomposition
    - ROTL
    NE MARCHE PAS
    """

    # Valeurs initiales
    A, B, C, D, E = 0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0

    x = normalisation(mot)

    for M in decomposition(x, 512):

        W = [i for i in decomposition(M, 32)]

        for i in range(16, 80):
            W.append(ROTL((W[i-3] ^ W[i-8] ^ W[i-14] ^ W[i-16]), 1))

        a, b, c, d, e = A, B, C, D, E

        for t in range(80):

            if t >= 0 and t < 20:
                f = (B & C) | ((~B) & D)
                K = 0x5A827999
            elif t >= 20 and t < 40:
                f = B ^ C ^ D
                K = 0x6ED9EBA1
            elif t >= 40 and t < 60:
                f = (B & C) | (B & D) | (C & D)
                K = 0x8F1BBCDC
            elif t >= 60 and t < 80:
                f = B ^ C ^ D
                K = 0xCA62C1D6

            T = (ROTL(A, 5) + f + E + K + W[t]) % 2**32
            E = D
            D = C
            C = ROTL(B, 30)
            B = A
            A = T

        A = (a + A) % 2**32
        B = (b + B) % 2**32
        C = (c + C) % 2**32
        D = (d + D) % 2**32
        E = (e + E) % 2**32

    return '%08x%08x%08x%08x%08x'%(A, B, C, D, E)


def sha256(mot):
    """ Fonction SHA256, fonction de hachage
    Utilise les fonctions:
    - normalisation
    - decomposition
    - ROTR
    - sigma0
    - sigma1
    - SIGMA0
    - SIGMA1
    - Ch
    - Maj
    """

    # Valeurs initiales
    A, B, C, D, E, F, G, H = 0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19

    # Constante K
    K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
         0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
         0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
         0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
         0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
         0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
         0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
         0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
         0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
         0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
         0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
         0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
         0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
         0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
         0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
         0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]

    x = normalisation(mot)

    for M in decomposition(x, 512):

        W = [i for i in decomposition(M, 32)]

        for i in range(16, 64):
            W.append((sigma1(W[i - 2]) + W[i - 7] + sigma0(W[i - 15]) + W[i - 16]) % 2**32)

        (a, b, c, d, e, f, g, h) = (A, B, C, D, E, F, G, H)

        for i in range(64):

            t1 = (H + SIGMA1(E) + Ch(E, F, G) + K[i] + W[i]) % 2**32
            t2 = (SIGMA0(A) + Maj(A, B, C)) % 2**32
            H = G
            G = F
            F = E
            E = (D + t1) % 2**32
            D = C
            C = B
            B = A
            A = (t1 + t2) % 2**32

        A = (A + a) % 2**32
        B = (B + b) % 2**32
        C = (C + c) % 2**32
        D = (D + d) % 2**32
        E = (E + e) % 2**32
        F = (F + f) % 2**32
        G = (G + g) % 2**32
        H = (H + h) % 2**32

    return '%08x%08x%08x%08x%08x%08x%08x%08x'%(A, B, C, D, E, F, G, H)

mot = "e"

print(md5(mot))

import hashlib
print(hashlib.md5(mot.encode('utf-8')).hexdigest())