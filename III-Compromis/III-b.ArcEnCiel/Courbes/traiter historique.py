import matplotlib.pyplot as plt

fichier = "/Users/juliettedebono/Documents/MP*/TIPE/Rainbow Tables/historiques création table AEC.txt"
T, M, temps = [], [], []

with open(fichier, 'r') as f:
    ligne = f.readline()
    while ligne != "":
        if ligne == "\n":
            for i in range(len(liste)):
                T.append(T2)
                M.append(i*100)
                temps.append(int(liste[i]))
        elif "Création table arc en ciel T : " in ligne:
            ligne = ligne.strip().replace("Création table arc en ciel T : ", "").replace(" , M : ", ",").replace(" : ", ",").replace(" secondes", "")
            T2 = int(ligne.split(",")[0])
            liste = []
        else:
            liste.append(ligne.strip().split(" secondes")[0])
        ligne = f.readline()

fig = plt.figure()
ax = fig.gca(projection = '3d')

my_cmap = plt.get_cmap('rainbow')
trisurf = ax.plot_trisurf(T, M, temps, linewidth = 0.1, antialiased = False, cmap = my_cmap)
fig.colorbar(trisurf, ax = ax, shrink = 0.8)

ax.scatter(T, M, temps, marker='_', color = "r", alpha = 0.1) # Points

ax.view_init(*(34, -144))

ax.set_title('Temps en fonction de M et T : historique')
ax.set_xlabel('T')
ax.set_ylabel('M')
ax.set_zlabel('temps')
plt.savefig("/Users/juliettedebono/Documents/MP*/TIPE/Rainbow Tables/Courbes historique")
plt.show()