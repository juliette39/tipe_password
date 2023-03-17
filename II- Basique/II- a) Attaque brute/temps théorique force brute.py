import time, hashlib

def hachage(mot) -> str:
    """hash mot avec md5"""

    return hashlib.new('md5', mot.encode('utf-8')).hexdigest()

def dec2base(i, caracteres):
    """Convertit i en base 10 en result en base len(caracteres) avec la liste de caractères caracteres"""

    l = len(caracteres)
    result = caracteres[i % l]
    i = (i//l) - 1

    while i > -1:
        i, result = (i // l) - 1, caracteres[i % l] + result
    return result

def red(h : str, i, t : int, n) -> int :
    """Transforme un hash en indice"""
    N = n + l**i
    h = str(h)
    return (int(h, 16) + t) % N

caracteres = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
l = len(caracteres)
e = 10000
y = []

for i in range(1, 15):
    n = sum([l**k for k in range(1, i+1)]) - 1

    h = hachage(dec2base(n, caracteres))
    st = time.time()

    for _ in range(e):
        # On réalise l'opération un certain nombre de fois
        hachage(dec2base(red(h, i, 1, n), caracteres))

    t = (time.time() - st) / e
    y.append(n*t)

print(y)

# iMac 2009
# [1, 2, 3, 4, 5, 6, 7]
# [0.00015807151794433594, 0.005568981170654297, 0.11891508102416992, 3.490976095199585, 86.7342791557312, 2402.337882757187, 65502.59010100365]

# MacBookAir 2017
# [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
# [0.0002609647989273071, 0.019876070737838748, 1.3695568049669264, 101.19039012982844, 6791.717667701912, 419072.78867693007, 26370887.313664626, 1774671384.1215305, 114197049354.61603, 7421171615163.042, 422434355080551.3, 3.093496404845014e+16, 2.04761186994996e+18, 1.3255018005042317e+20]
