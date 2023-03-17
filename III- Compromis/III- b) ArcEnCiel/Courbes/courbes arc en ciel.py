tempsf = lambda x : ((6.5*(10**(-6))) * (x**2)) - 0.00063 * x + 2.65
# Temps de recherche en fonction de T de la table (expérimental)
arrondi = lambda l, x, e : str(int(round(x/(10**(l-e)), 0))) + "e" + str(l-e) if l > e else str(x)
taille = lambda nb_ligne : nb_ligne * (2 + 4*2)
unite = ["o", "ko", "Mo", "Go", "To"]

def tempsSTR(s):
    s = round(s, 3)
    m, h, j, a = 60, 3600, 3600*24, 3600*24*365
    if s > a:
        x, string = int(round(s/a, 0)), "a"
    elif s > j:
        x, string = int(round(s/j, 0)), "j"
    elif s > h:
        x, string = int(round(s/h, 0)), "h"
    elif s > m:
        x, string = int(round(s/m, 0)), "min"
    else:
        return str(s) + "s"
    return arrondi(len(str(x)), x, 3) + string

def tailleSTR(o):
    o_s = str(int(o))
    l = len(o_s)
    if l > len(unite)*3:
        o = int(round(o/(10**(12)), 0))
        l = len(str(o)) - 1
        return arrondi(l, o, 0) + unite[-1]
    elif l > 3:
        l -= 1
        l1 = l % 3
        return str(int(round(o/(10**(l - l1)), 0))) + unite[((l-l1) // 3)]
    else:
        return o_s + unite[0]

import matplotlib.pyplot as plt
import numpy as np
import sqlite3
database = "./T M temps T = 9000 M = 12000 Pas = 1000.sqlite"

conn = sqlite3.connect(database)
cur = conn.cursor()
cur.execute("""SELECT SUM(temps) FROM Temps""")
val = cur.fetchone()[0]
cur.execute("""SELECT T, M, temps FROM Temps""")
tableau = np.array(cur.fetchall())
T, M, temps = tableau[:,0], tableau[:,1], tableau[:,2]

plt.rcParams.update({'font.sans-serif':'Tahoma'})
fig = plt.figure(1, figsize=(8, 7))
ax = fig.gca(projection = '3d')

my_cmap = plt.get_cmap('rainbow')
trisurf = ax.plot_trisurf(T, M, temps, linewidth = 0.1, antialiased = False, cmap = my_cmap)
ax.scatter(T, M, temps, marker='_', color = "r", alpha = 0.1) # Points

ax.yaxis.set_ticklabels([tailleSTR(taille(i)) for i in ax.get_yticks()], fontsize = 10)
ax.xaxis.set_ticklabels([tempsSTR(tempsf(i)) for i in ax.get_xticks()], fontsize = 10)
ax.zaxis.set_ticklabels([tempsSTR(i) for i in ax.get_zticks()], fontsize = 10)
cb = fig.colorbar(trisurf, ax = ax, shrink = 0.8)
cb.ax.set_yticklabels([tempsSTR(i) for i in ax.get_zticks()], fontsize = 10)

ax.view_init(*(25, -155))
ax.set_title('Temps en fonction de M et T', fontsize = 16)
ax.set_xlabel('\n\ntemps de recherche\nproportionnel à T', fontsize = 12)
ax.set_ylabel('\nmémoire\nproportionnelle à M', fontsize = 12)
ax.set_zlabel('\ntemps création', fontsize = 12)
plt.savefig("./Courbes T = 9000 M = 12000 Pas = 1000")