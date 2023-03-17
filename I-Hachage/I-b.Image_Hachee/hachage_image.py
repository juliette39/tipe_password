import matplotlib as plt
import matplotlib.image as mpimg
from subprocess import Popen, PIPE
import numpy as np

def hachage(mot) -> str:
    """hash mot avec md5"""
    return hashlib.new('md5', mot.encode('utf-8')).hexdigest()

def hacher(hach, fileout):

    nb_ligne, nb_pixel, nb_carreau_ligne, nb_carreau_colonne = 300, 4, 5, 3
    nb_colonne = int((nb_ligne / nb_carreau_ligne) * nb_carreau_colonne)

    liste = [int(hach[i*2:i*2+2], 16) for i in range(len(hach)//2)]
    image = np.zeros((nb_carreau_ligne, nb_carreau_colonne, nb_pixel))

    k = 0
    for i in range(nb_carreau_ligne):
        for j in range(nb_carreau_colonne):
            val = liste[k]
            image[i][j] = np.array(plt.cm.gist_rainbow(X=val))

            k += 1

    tableau_vide = np.zeros((nb_ligne, nb_colonne, nb_pixel))

    for i in range(nb_ligne):
        for j in range(nb_colonne):

            tableau_vide[i][j] = image[int(nb_carreau_ligne*i/nb_ligne), int(nb_carreau_colonne*j/nb_colonne)]

    mpimg.imsave(fileout, tableau_vide)

file = "./Raphaël.png"

p = Popen(["md5", file], stdin=PIPE, stdout=PIPE, stderr=PIPE)
output, err = p.communicate(b"input data that is passed to subprocess' stdin")

hach = output.decode("utf-8").strip("\n").split(" ")[-1]
fileout = "./Raphaël-Haché.png"
hacher(hach, fileout)