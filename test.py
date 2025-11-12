import random
from math import pi, tan
from random import randint
import time
from matplotlib import pyplot as plt

# Definition des éléments
xlim = 500
ylim = 500
zmin = 200
zmax = 500


def coordonnees():
    x = 0
    y = 0
    # On s'assure que x et y ne sont pas 0 pour la fonction cap()
    while x == 0:
        x = random.uniform(-xlim, xlim)
    while y == 0:
        y = random.uniform(-ylim, ylim)

    z = random.uniform(zmin, zmax)
    return x, y, z


def cap(x, y):
    teta = 0
    # Votre logique 'match' est conservée
    match (x, y):
        case (x, y) if x > 0 and y > 0:
            teta = random.uniform(pi, 3 * pi / 2)
        case (x, y) if x < 0 and y > 0:
            teta = random.uniform(3 * pi / 2, 2 * pi)
        case (x, y) if x < 0 and y < 0:
            teta = random.uniform(0, pi / 2)
        case (x, y) if x > 0 and y < 0:
            teta = random.uniform(pi / 2, pi)

    a = tan(teta)
    return a, teta  # teta : angle en rad & a : coef directeur


# Equation de trajectoire : y = a*x + b
def y1(a, x, b):
    return a * x + b


# Modifiée pour prendre 'a' ET 'b'
def graph(a, b):
    Y = []
    X = [i for i in range(-xlim, xlim)]
    for j in X:
        # On appelle la nouvelle fonction y1
        Y.append(y1(a, j, b))
    return X, Y


# --- MAIN ---
if __name__ == "__main__":
    # 1. Obtenir les coordonnées du point
    x, y, z = coordonnees()

    # 2. Obtenir la pente 'a' aléatoire (basée sur votre logique)
    a, teta = cap(x, y)

    # 3. CALCULER 'b' (l'ordonnée à l'origine)
    # Puisque y = a*x + b, alors :
    b = y - (a * x)

    # 4. Générer la ligne (y = ax + b)
    X, Y = graph(a, b)

    # 5. Tracer la ligne
    plt.plot(X, Y, label=f'Trajectoire (y = {a:.2f}x + {b:.2f})', color='blue')

    # 6. Tracer le point (x, y)
    # Il sera parfaitement sur la ligne
    plt.plot(x, y,
             'ro',  # 'r' = rouge, 'o' = cercle
             markersize=8,  # Rendre le point plus visible
             label=f'Point ({x:.1f}, {y:.1f})')

    # 7. Mettre en forme et afficher
    plt.axis('equal')
    plt.xlim(-xlim, xlim)
    plt.ylim(-ylim, ylim)
    plt.title('Point sur une droite (ne passant pas par l\'origine)')
    plt.legend()
    plt.grid(True)
    plt.show()