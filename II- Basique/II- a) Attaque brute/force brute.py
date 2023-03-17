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

def testValidite(mot : str, hach : str) -> bool :
    """Renvoie si mot est bien l'antécédent de hash avec la fonction du hachage de datas"""
    return hachage(mot) == hach

'''
def forceBrute(mdp, mini = 1, maxi = 10, caracteres = caracteres):
    """Test par force brute jusqu'à ce que la valeur vaille mdp"""

    tps = time.time()

    for i in range(mini, maxi + 1):
        for tup in product(caracteres, repeat=i):
            mot = ''.join(tup)
            if hachage(mot) == mdp:
                return mot, time.time() - tps
    return None'''

def forceBrute(mdp, mini = 1, maxi = 10, caracteres = ""):
    """Test par force brute jusqu'à ce que la valeur vaille mdp"""

    l = len(caracteres)
    N = sum([l**i for i in range(0, maxi+1)])
    cherche = sum([l**i for i in range(1, mini)])

    while hachage(dec2base(cherche, caracteres)) != mdp and cherche < N:
        cherche += 1

    return dec2base(cherche, caracteres)

caracteres = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
result = "TiP3" # Mot imposé
# mini = 4
# maxi = mini

# hach = hachage(result) # Hache le mot choisi
# print(hach, result) # Affiche le hach du mot cherché

# t = time.time() # Démare le compteur de temps

# mot = forceBrute(hach, mini, maxi, caracteres) # Cherche l'antécédent du hach

# print(mot) # Affice le mot de passe trouvé
# print(testValidite(mot, hach)) # Vérifie que c'est le bon mot
# print("Temps pour recherche force brute : {} secondes".format(time.time() - t))