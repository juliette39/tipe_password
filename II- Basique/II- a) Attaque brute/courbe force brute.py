import matplotlib.pyplot as plt
import numpy as np

arrondi = lambda l, x, e : str(int(round(x/(10**(l-e)), 0))) + "e" + str(l-e) if l > e else str(x)

def temps(s):
    s = round(s, 3)
    m, h, j, a = 60, 3600, 3600*24, 3600*24*365

    if s > a:
        x = int(round(s/a, 0))
        return arrondi(len(str(x)), x, 3) + "a"
    elif s > j:
        x = int(round(s/j, 0))
        return arrondi(len(str(x)), x, 3) + "j"
    elif s > h:
        x = int(round(s/h, 0))
        return arrondi(len(str(x)), x, 3) + "h"
    elif s > m:
        x = int(round(s/m, 0))
        return arrondi(len(str(x)), x, 3) + "min"
    else:
        return str(s) + "s"

def courbe(y, z):

    couleur = 'purple'
    plt.rcParams.update({'font.sans-serif':'Tahoma'})
    plt.clf()
    fig = plt.figure(1, figsize=(6, 7))
    ax1 = fig.add_subplot(2, 1, 1)
    plt.yticks(fontsize = 10)
    plt.xticks(fontsize = 10)
    plt.yscale('log')
    i = len(z)
    x = np.linspace(1, i, i)
    ax1.plot(x, z, couleur)
    (xmin, xmax) = ax1.xaxis.get_view_interval()
    (ymin, ymax) = ax1.yaxis.get_view_interval()

    ax1 = fig.add_subplot(2, 1, 1)
    plt.yscale('log')
    i = len(y)
    x = np.linspace(1, i, i)
    ax1.plot(x, y, couleur)

    ax2 = ax1.twinx()
    plt.yscale('log')
    ax2.plot(x, y, couleur)

    ax1.set_xlim(xmin, xmax)
    ax2.set_xlim(xmin, xmax)
    ax1.set_ylim(ymin, ymax)
    ax2.set_ylim(ymin, ymax)
    ax2.yaxis.set_ticklabels([temps(i) for i in ax1.get_yticks()], fontsize = 8)

    ax1.set_ylabel('temps (s)', fontsize = 12)

    ax3 = fig.add_subplot(2, 1, 2)
    plt.yscale('log')
    i = len(z)
    x = np.linspace(1, i, i)
    ax3.plot(x, z, couleur)

    ax4 = ax3.twinx()
    plt.yscale('log')
    ax4.plot(x, z, couleur)

    ax4.yaxis.set_ticklabels([temps(i) for i in ax3.get_yticks()], fontsize = 8)
    ax3.set_xlabel('nombre lettres', fontsize = 12)
    ax3.set_ylabel('temps (s)', fontsize = 12)
    ax1.set_title("Temps pour générer tous les mots de n lettres\n", fontsize = 16)

    plt.savefig("Temps pour générer tous les mots jusqu'à {} caractères.png".format(i))
    plt.show()

courbe([0.00015807151794433594, 0.005568981170654297, 0.11891508102416992, 3.490976095199585,
            86.7342791557312, 2402.337882757187,65502.59010100365],
       [0.0002609647989273071, 0.019876070737838748, 1.3695568049669264, 101.19039012982844,
            6791.717667701912, 419072.78867693007, 26370887.313664626, 1774671384.1215305, 114197049354.61603,
            7421171615163.042, 422434355080551.3, 3.093496404845014e+16, 2.04761186994996e+18, 1.3255018005042317e+20])