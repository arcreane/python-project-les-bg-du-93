import random
from math import pi, tan, atan
from random import randint
import time
from matplotlib import pyplot as plt

#Definition des éléments
xlim = 500
ylim = 500
zmin = 200
zmax = 500

def coordonnees():
    x = 1
    y = 1
    while -250 < x < 250 :
        x = random.uniform(-xlim, xlim)
    while -250 < y < 250 :
        y = random.uniform(-ylim, ylim)
    z = random.uniform(zmin, zmax)
    return x, y, z

def cap(x, y):
    teta = 0
    match (x,y):
        case (x,y) if x > 0 and y > 0 :
            teta = random.uniform(pi, 3*pi/2)
        case (x,y) if x < 0 and y > 0 :
            teta = random.uniform(3*pi/2, 2*pi)
        case (x,y) if x < 0 and y < 0 :
            teta = random.uniform(0, pi/2)
        case (x,y) if x > 0 and y < 0 :
            teta = random.uniform(pi/2, pi)
        case _:
            x, y = coordonnees()
            cap(x,y)
    a = tan(teta)
    return a, teta          #teta : angle en rad & a : coef directeur de la trajectoire

#Equation de trajectoire :
def y1(a,x1,b):
    return a*x1 + b


def graph(a, b):
    Y = []
    X = [i for i in range(-xlim, xlim)]
    for j in X:
        try:
            Y.append(y1(a,j, b))
        except :
            Y.append(0)
    return X, Y




if __name__ == "__main__":
    x, y, z =coordonnees()
    a, teta = cap(x, y)
    b = y - a * x

    X, Y = graph(a, b)

    plt.plot(x, y, 'ro')      #Point de départ de l'avion
    plt.plot(X, Y)            #Trajectoire de l'avion

    plt.axis('equal')               #Axes othonormés

    plt.xlim(-xlim, xlim)     #Limites des axes
    plt.ylim(-ylim, ylim)

    plt.show()




print(coordonnees())