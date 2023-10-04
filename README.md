# tipe_password

Projet réalisé dans le cadre de mon TIPE (Travaux d'initiative personnelle encadrés) en deuxième année de CPGE.
Projet essentiellement réalisé en python

## Déchiffrement de mots de passe : Étude de différentes méthodes.
*Quelles sont les meilleures méthodes pour déchiffrer un mot de passe ?*

## Le hachage

*Comment les mots de passe sont protégés : les fonctions de hachage*

J'ai codé ma propre fonction de hachage [md5.py](/I-Hachage/I-a.MyHash/md5.py)
J'ai aussi haché des images pour visualiser les conséquences d'une fonction de hachage (grande modification au moindre pixel changé) [hachage_image.py](/I-Hachage/I-b.Image_Hachee/hachage_image.py)

<img src="/X-Documents/Tipe_présentation/Tipe_présentation%20copie_page-0003.jpg" />

Ainsi le hash des mots de passe sont stockés dans des base de données, et si un hackeur obtient cette base de donnée, il ne peut pas connaître en clair les mots de passe et donc les réutilisés.

<img src="/X-Documents/Tipe_présentation/Tipe_présentation%20copie_page-0004.jpg" />

## Les attaques basiques

Il existe 3 méthodes basiques principales pour retrouver le mot de passe d'origine à partir d'un hash.

### Attaque Brute

La force brute consiste à tout tester jusqu'a ce qu'on obtienne le bon hash. On obtient alors le mot de passe d'origine.
On va tester d'abord a, puis b, puis c… puis aa, puis ab…
C'est une méthode très longue qui demande beaucoup de puissance de calcul.

### Attaque mémoire

L'attaque mémoire consiste à faire tous les calcul de la force brute mais d'enregister les valeurs. Ainsi on peut calculer à l'avance tous les hash des mots de passe, puis une fois générer, on a juste à chercher dans la base de données le mot de passe en clair correspondant au hash.
C'est une méthode qui demande du temps de calcul préalable, mais surtout beaucoup de mémoire pour stocker les résultats.

### Dictionnaire

C'est comme une attaque par mémoire, mais on ne va pas tout tester, seulement les mots de passe courant et/ou des mots existants. Cela permet de ne calculer que pour les mots de passe qui ont le plus de chance d'être utilisés.

## Compromis

Pour améliorer ces attaques, il est possible d'en faire des compromis, ce qu'on appelle des compromis temps-mémoire.

### Les tables classiques

Le premier à parler de ces compromis est Hellman en 1980.

<img src="/X-Documents/Tipe_présentation/Tipe_présentation%20copie_page-0008.jpg" />

<img src="/X-Documents/Tipe_présentation/Tipe_présentation%20copie_page-0009.jpg" />

<img src="/X-Documents/Tipe_présentation/Tipe_présentation%20copie_page-0010.jpg" />

### Les tables arc-en-ciel

Philippe Oechslin en 2003 propose une amélioration avec les tables arc en ciel.

<img src="/X-Documents/Tipe_présentation/Tipe_présentation%20copie_page-0013.jpg" />

<img src="/X-Documents/Tipe_présentation/Tipe_présentation%20copie_page-0014.jpg" />

## Comparaison

Voici uen comparaison de ces méthodes 

<img src="/X-Documents/Tipe_présentation/Tipe_présentation%20copie_page-0018.jpg" />

## Autres idées

### Boite_mail

Il s'agit d'un programme qui reproduit une boîte mail fictive stockant des mots de passe. Elle reproduit la méthode de hachage vu précédemment en ne stockant que les hash des mots de passe.

### MyHashFunct

Il s'agit des autres fonctions de hachage codées, à savoir SHA1, et de tests pour vérifier leur validité.

### Points distingués

C'est une méthode développée par Ronald Rivest en 1982. J'en ai codé une implémentation [Points_distingues](/X-Autre%20idées/Points_distingues).

<img src="/X-Documents/Tipe_présentation/Tipe_présentation%20copie_page-0021.jpg" />

## Documents

Enfin voici les documents du projet : les slides, le texte, les articles dont les recherches sont tirées et les illustrations.
