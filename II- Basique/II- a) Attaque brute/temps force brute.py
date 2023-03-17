caracteres = "abcdefghijklmnopqrstuvwxyz"
import time
import hashlib

def dec2base(i, caracteres):
    """Convertit i en base 10 en result en base len(caracteres) avec la liste de caractères caracteres"""

    l = len(caracteres)
    result = caracteres[i % l]
    i = (i//l) - 1

    while i > -1:
        i, result = (i // l) - 1, caracteres[i % l] + result
    return result

def hachage(mot):
    """hash mot avec md5"""

    return hashlib.new('md5', mot.encode('utf-8')).hexdigest()


def forceBrute(mdp, mini = 1, maxi = 10, caracteres = ""):
    """Test par force brute jusqu'à ce que la valeur vaille mdp"""

    tps = time.time()
    l = len(caracteres)
    N = sum([l**i for i in range(0, maxi+1)])
    cherche = sum([l**i for i in range(1, mini)])

    while hachage(dec2base(cherche, caracteres)) != mdp and cherche < N:
        cherche += 1

    return time.time() - tps

i = 10

for t in range(1, i):
    a = forceBrute(hachage(caracteres[-1] * int(t)), t, t, caracteres)
    print(t, a)