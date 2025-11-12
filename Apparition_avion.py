import random
from math import pi, tan
from random import randint
import time
from matplotlib import pyplot as plt

#Definition des éléments
xlim = 500
ylim = 500
zmin = 200
zmax = 500

def coordonnees():
    x = random.uniform(-xlim, xlim)
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
            coordonnees()
            cap(x,y)
    a = tan(teta)
    return a, teta          #teta : angle en rad & a : coef directeur de la trajectoire

#Equation de trajectoire :
def y1(a,x):
    return a*x

def graph():
    Y = []
    X = [i for i in range(-xlim, xlim)]
    for j in X:
        Y.append(y1(a,j))
    return X, Y




if __name__ == "__main__":
    x, y, z =coordonnees()
    a, teta = cap(x, y)
    X, Y = graph()
    plt.plot(X, Y)
    plt.axis('equal')
    plt.xlim(-xlim, xlim)
    plt.ylim(-ylim, ylim)
    plt.show()




print(coordonnees())