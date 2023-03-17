import math

def convertToWordArray(string):

    n = len(string)
    inter = n + 8
    lon = (((inter - (inter % 64)) // 64) + 1) * 16
    liste = [0] * (lon - 1)
    pos = 0

    for i in range(n):

        inter = (i-(i%4)) // 4
        pos = (i%4) * 8
        liste[inter] = (liste[inter]|(ord(string[i])<<pos))
    i = n

    inter = (i-(i%4)) // 4
    pos = (i%4) * 8
    liste[inter] = liste[inter] | (0x80 << pos)
    liste[lon-2] = n << 3
    liste.append(n >> 29)
    return liste

def ROTL(x, n):
    """Utile pour SHA1 et MD5
    Opération de rotation binaire vers la gauche"""

    return (x << n) | x >> (32 - n)

def wordToHex(value):
    value = hex(value)
    diff = len(value) - 8
    value = value[diff:]
    return ''.join([value[i*2:(i+1)*2] for i in reversed(range(len(value)//2))])

def md5(message):

    r = [7, 12, 17, 22] * 4 + [5, 9, 14, 20] * 4 + [4, 11, 16, 23] * 4 + [6, 10, 15, 21] * 4
    K = [int(abs((2**32) * math.sin(i + 1))) for i in range(64)]


    x = convertToWordArray(message)

    A = 0x67452301
    B = 0xEFCDAB89
    C = 0x98BADCFE
    D = 0x10325476

    print(len(x))
    x = x + x

    for j in range(0, len(x), 16):
        a = A
        b = B
        c = C
        d = D

        for t in range(64):
            if t >= 0 and t < 16:
                f = (B & C) | ((~B) & D) # OK
                g = t # OK
            elif t >= 16 and t < 32:
                f = (B & D) | (C & (~D)) # OK
                g = (5 * t + 1) % 16 # OK
            elif t >= 32 and t < 48:
                f = B ^ C ^ D # OK
                g = (3 * t + 5) % 16 # OK
            elif t >= 48 and t < 64:
                f = C ^ (B | (~D)) # OK
                g = (7 * t) % 16 # OK


            new_B = (A + f + x[j + g] + K[t]) & 0xffffffff
            new_B = (ROTL(new_B, r[t]) & 0xffffffff) + B

            A, B, C, D = D, new_B, B, C

        A = (a + A) % 2**32
        B = (b + B) % 2**32
        C = (c + C) % 2**32
        D = (d + D) % 2**32

        # j += 16
    print(A, B, C, D)
    return wordToHex(A) + wordToHex(B) + wordToHex(C) + wordToHex(D)

print(md5('juju'))