import matplotlib.pyplot as plt
import numpy as np
from math import log, exp

unite = ["o", "ko", "Mo", "Go", "To"]
arrondi = lambda l, x, e : str(int(round(x/(10**(l-e)), 0))) + "e" + str(l-e) if l > e else str(x)

alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
l = len(alphabet)

def taille(n):
    nb_ligne = l**n
    mot = n
    hach = 32 # Hach codé en octets : taille 32
    carac = 2
    taille = nb_ligne * (carac + hach + mot)
    return taille

def tailleSTR(o):
    o_s = str(int(o))
    l = len(o_s)
    if l > len(unite)*3:
        o = int(round(o/(10**(12)), 0))
        l = len(str(o)) - 1
        o_s = arrondi(l, o, 0) + unite[-1]
    elif l > 3:
        l -= 1
        l1 = l % 3
        o_s = str(int(round(o/(10**(l - l1)), 0))) + unite[((l-l1) // 3)]
    else:
        o_s += unite[0]
    return o_s

def courbe(i):
    couleur = 'purple'
    plt.rcParams.update({'font.sans-serif':'Tahoma'})

    plt.clf()
    fig = plt.figure(2, figsize=(7, 6))
    ax1 = fig.add_subplot()
    plt.yticks(fontsize = 10)
    plt.xticks(fontsize = 10)
    plt.yscale('log', basey=10)
    ax2 = ax1.twinx()

    x = np.linspace(1, i, i)
    y = [taille(i) for i in x]
    plt.yscale('log', basey=10)

    ax1.plot(x, y, couleur)
    ax2.plot(x, y, couleur)

    ax2.yaxis.set_ticklabels([tailleSTR(i) for i in ax1.get_yticks()], fontsize = 10)

    ax1.set_xlabel('nombre lettres', fontsize = 12)
    ax1.set_ylabel('poids (octets)', fontsize = 12)
    plt.title("Poids pour générer tous les mots de n lettres\n", fontsize = 16)
    plt.savefig("Poids pour générer tous les mots jusqu'à {} caractères.png".format(i))
    plt.show()

courbe(14)