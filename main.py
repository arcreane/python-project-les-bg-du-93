import sys
import random
from math import pi, tan, sqrt, atan2, degrees, cos, sin, radians
import os
import time
from types import NoneType

from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtCore import QTimer, Qt, QPoint
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Circle
from matplotlib.path import Path
from matplotlib.markers import MarkerStyle
from matplotlib.transforms import Affine2D

app = QtWidgets.QApplication(sys.argv)

xlim = 1000
ylim = 1000
zmin = 9000
zmax = 12000

VITESSE_DEFAUT = 5.0
VITESSE_MIN = 2.0
VITESSE_MAX = 10.0
PAS_VITESSE = 1.0

COULEURS_DISPO = [
    ("Rouge", "red"), ("Bleu", "blue"), ("Vert", "green"),
    ("Orange", "darkorange"), ("Violet", "purple"), ("Cyan", "cyan"),
    ("Magenta", "magenta"), ("Noir", "black"), ("Marron", "brown"), ("Gris", "gray")
]

#Création de l'icone de l'avion
verts = [(1, 0), (-1, 1), (-0.5, 0), (-1, -1), (1, 0)]#Liste des coordonnées des sommets
codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]#Comment relier ces sommet
PLANE_PATH = Path(verts, codes)#Creation de l'objet qui servira d'icone d'avion

selected_button = None
nb_avions = 7


class Avion :
    def __init__(self, ax, nom_couleur, code_couleur):
        self.ax = ax
        self.name = f"Avion {nom_couleur}"
        self.color_code = code_couleur

        self.x = 0.0
        self.y = 0.0
        self.teta = 0.0
        self.apparition_avion()
        self.update_equation_droite()
        self.z = random.uniform(zmin, zmax)


        variation = random.uniform(-0.5, 0.5)
        self.speed = VITESSE_DEFAUT + variation

        t = Affine2D().rotate_deg(degrees(self.teta))
        m = MarkerStyle(PLANE_PATH, transform=t)
        self.point, = self.ax.plot(self.x, self.y, marker=m, markersize=15, color=self.color_code, markeredgecolor="white", markeredgewidth=0.3, picker=10)


        self.approaching = False
        self.peut_atterir = False


    def apparition_avion(self):
        cote = random.choice(("haut", "bas", "gauche", "droite"))
        if cote == "gauche":
            self.x, self.y, self.teta = -xlim, random.uniform(-ylim, ylim), random.uniform(-pi/4, pi/4)
        elif cote == "droite":
            self.x, self.y, self.teta = xlim, random.uniform(-ylim, ylim), random.uniform(3*pi/4, 5*pi/4)
        elif cote == "bas":
            self.x, self.y, self.teta = random.uniform(-xlim, xlim), -ylim, random.uniform(pi/4, 3*pi/4)
        else:
            self.x, self.y, self.teta = random.uniform(-xlim, xlim), ylim, random.uniform(5*pi/4, 7*pi/4)


    def update_equation_droite(self):
        self.a = tan(self.teta)
        self.b = self.y - self.a * self.x

    def get_current_pos(self):
        return self.x, self.y

    def distance_to_center(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def get_distance_to_plane(self, other):
        x2, y2 = other.get_current_pos()
        return sqrt((x2 - self.x) ** 2 + (y2 - self.y) ** 2)

    def avancer(self):
        dx = self.speed * cos(self.teta)
        dy = self.speed * sin(self.teta)

        self.x += dx
        self.y += dy

        self.point.set_data([self.x], [self.y])

    def atterissage(self):
        if self.approaching :
            return
        elif self.peut_atterir is True :
            direction_centre = atan2(0 - self.y, 0 - self.x)
            self.changer_cap(direction_centre)
            self.approaching = True


    def changer_cap(self, angle_radians):
            self.approaching = False

            self.teta = angle_radians
            t = Affine2D().rotate_deg(degrees(self.teta))
            self.point.set_marker(MarkerStyle(PLANE_PATH, transform=t))

            self.update_equation_droite()





    def effacer(self):
        self.point.remove()





class Menu :
    def __init__(self):
        self.fenetre_1 = uic.loadUi("fenetre_1.ui")

        self.Bouttons = [
            self.fenetre_1.pushButton_1,
            self.fenetre_1.pushButton_2,
            self.fenetre_1.pushButton_3,
            self.fenetre_1.pushButton_4,
            self.fenetre_1.pushButton_5
        ]
        self.style_button_1 = self.fenetre_1.pushButton_1.styleSheet()
        self.style_button_2 = self.fenetre_1.pushButton_1.styleSheet()
        self.style_button_3 = self.fenetre_1.pushButton_1.styleSheet()
        self.style_button_4 = self.fenetre_1.pushButton_1.styleSheet()
        self.style_button_5 = self.fenetre_1.pushButton_1.styleSheet()

        self.style = [
            self.style_button_1,
            self.style_button_2,
            self.style_button_3,
            self.style_button_4,
            self.style_button_5
        ]




        # Ici on met lambda car pour les pushButton, on veut que la fonction associée n'ait pas d'arguments
        self.fenetre_1.pushButton_1.clicked.connect(lambda: self.choix_du_niveau(self.fenetre_1.pushButton_1))
        self.fenetre_1.pushButton_2.clicked.connect(lambda: self.choix_du_niveau(self.fenetre_1.pushButton_2))
        self.fenetre_1.pushButton_3.clicked.connect(lambda: self.choix_du_niveau(self.fenetre_1.pushButton_3))
        self.fenetre_1.pushButton_4.clicked.connect(lambda: self.choix_du_niveau(self.fenetre_1.pushButton_4))
        self.fenetre_1.pushButton_5.clicked.connect(lambda: self.choix_du_niveau(self.fenetre_1.pushButton_5))


    def choix_du_niveau(self, name):
        global selected_button, nb_avions

        selected_button = name.text()
        match selected_button:
            case "Débutant":
                nb_avions = 1
            case "Intermédiaire":
                nb_avions = 2
            case "Affirmé":
                nb_avions = 3
            case "Avancé":
                nb_avions = 5
            case "TOP GUN":
                nb_avions = 10

        for i in range(len(self.Bouttons)):
            self.Bouttons[i].setStyleSheet(self.style[i])
        self.fenetre_1.pushButton_6.setEnabled(True)
        self.fenetre_1.label_2.setText(f"Difficulté sélectionné : {selected_button}")
        name.setStyleSheet("background-color: yellow;")



class Jeu :
    def __init__(self):
        #Initialisation de la fenetre 2
        self.fenetre_2 = uic.loadUi("fenetre_2.ui")

        #Import du graphique matplotlib
        fig = Figure(figsize=(5, 4), dpi=100)
        fig.subplots_adjust(left=0.04, right=0.99, bottom=0.04, top=0.99)
        fig.patch.set_facecolor('none')

        self.ax = fig.add_subplot(111)
        self.ax.set_facecolor((0, 0, 0, 0.5))
        self.ax.tick_params(colors='white')
        for spine in self.ax.spines.values():
            spine.set_edgecolor('white')

        self.canvas = FigureCanvas(fig)
        self.canvas.setStyleSheet("background: transparent;")

        self.canvas.mpl_connect('pick_event', self.click)

        QtWidgets.QVBoxLayout(self.fenetre_2.widget).addWidget(self.canvas)

        #Initialisation du fond du graphique
        self.ax.axhline(y=0, color='white', linewidth=1)
        self.ax.axvline(x=0, color='white', linewidth=1)
        rayon_atterissage = Circle((0, 0), 150, color='#4cd74c', fill=False, linewidth=2, linestyle='--')
        self.ax.add_patch(rayon_atterissage)
        self.ax.set_xlim(-xlim, xlim)
        self.ax.set_ylim(-ylim, ylim)
        self.ax.set_aspect('equal')

        #Initialisation du jeux
        self.victory_level_1 = False
        self.victory_level_2 = False
        self.victory_level_3 = False
        self.victory_level_4 = False

        self.victory = None

        #Initialisation des variables sur la page
        self.score = 0
        self.nb_atterrissages = 0
        self.liste_avions = []
        self.plane_state = "RAS"

        self.fenetre_2.progressBar.setMinimum(0)
        self.fenetre_2.progressBar.setMaximum(1000)

        self.selected_plane = None
        self.j = 0

        #Connections des clics
        self.fenetre_2.listWidget.itemClicked.connect(self.selection)

        #Lancement du paramètre temporel
        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update)
        self.timer.start()

    def spawn_avions(self, n):
        for i in range(n):
            self.j += 1
            nom, code = COULEURS_DISPO[self.j % len(COULEURS_DISPO)]
            avion = Avion(self.ax, nom, code)
            self.liste_avions.append(avion)
            self.fenetre_2.listWidget.addItem(f"Avion {nom}")

    def click(self, event):
        for avion in self.liste_avions :
            if avion.point == event.artist :
                items = self.fenetre_2.listWidget.findItems(avion.name, Qt.MatchExactly)
                item = items[0]
                self.fenetre_2.listWidget.setCurrentItem(item)
                self.selection(item)

    def selection(self, item):
        #Appelée quand on clique sur un avion dans la Qliste ou sur le graphique et update les labels vitesse, altitude, nom de l'avion
        if item == "Supr" :
            self.fenetre_2.label_1.setText("Sélectionnez un avion")
            self.fenetre_2.label_2.setText("")
            self.fenetre_2.label_3.setText("")

        else :
            if self.selected_plane is not None :
                self.selected_plane.point.set_markeredgecolor(None)
                self.selected_plane.point.set_markeredgewidth(None)
                self.selected_plane = None
            for avion in self.liste_avions :
                if avion.name == item.text() :
                        self.fenetre_2.label_1.setText(f"{avion.name}")
                        self.fenetre_2.label_2.setText(f"Vitesse : {int(54 * avion.speed)} km/h")
                        self.fenetre_2.label_3.setText(f"Altitude : {int(avion.z)} m")
                        try:
                            self.fenetre_2.pushButton_1.disconnect()
                            self.fenetre_2.dial.disconnect()
                        except TypeError:
                            pass

                        self.selected_plane = avion

                        self.fenetre_2.dial.valueChanged.connect(lambda : self.guidage_avion(avion))
                        self.fenetre_2.pushButton_1.clicked.connect(avion.atterissage)
                        self.fenetre_2.pushButton_1.setEnabled(True)
                        self.fenetre_2.dial.setEnabled(True)
                        avion.point.set_markeredgecolor("yellow")
                        avion.point.set_markeredgewidth(1)


                        #Initialisation de la boussole
                        valeur_dial = int(270 - degrees(avion.teta)) % 360
                        self.fenetre_2.dial.setValue(valeur_dial)

                        break

    def guidage_avion(self, avion):
        angle = int(270 - self.fenetre_2.dial.value()) % 360
        angle_radians = radians(angle)
        avion.changer_cap(angle_radians)

    def update_labels(self):
        self.fenetre_2.label_4.setText(f"Score : {self.score}")
        self.fenetre_2.label_6.setText(f"Avions en vol : {len(self.liste_avions)}")
        self.fenetre_2.label_7.setText(f"Atterissages : {self.nb_atterrissages}")
        self.fenetre_2.label.setText(f"Urgence : {self.plane_state}")

        self.fenetre_2.progressBar.setValue(self.score)

    def update(self):
        self.update_labels()

        if self.score >= 1000 :#Si le score atteint 1000 on a fini ce niveau
            self.fin_de_jeu()

        avion_a_supr = []
        for avion in self.liste_avions :

            if avion.distance_to_center() < 5 :

                self.score += 100
                self.nb_atterrissages += 1
                avion_a_supr.append(avion)

            else :

                for autre_avion in self.liste_avions :#Si les avions sont trop près, risque de colision
                    if avion == autre_avion :
                        continue
                    else :
                        if avion.get_distance_to_plane(autre_avion) < 50 :
                            self.plane_state = f"Colision entre {avion.name} et {autre_avion.name}"
                            self.score -= 100
                            avion_a_supr.append(avion)

                        elif avion.x > 1000 or avion.x < -1000 or avion.y > 1000 or avion.y < -1000 : #Si l'avion sort des limites du cadre
                            self.score -= 50
                            avion_a_supr.append(avion)

                        elif avion.get_distance_to_plane(autre_avion) < 150:
                            self.plane_state = f"Danger entre {avion.name} et {autre_avion.name}"


                if avion.distance_to_center() < 150 :
                    avion.peut_atterir = True

                avion.avancer()

        for avion in avion_a_supr:  # Suppression des avions
            # Déselection de l'avion
            self.selection("Supr")
            self.fenetre_2.listWidget.clearSelection()

            # Suppression de l'avion dans la liste et le graphique
            avion.effacer()
            self.liste_avions.remove(avion)
            #enlever l'avion de la Qlist
            items = self.fenetre_2.listWidget.findItems(avion.name, Qt.MatchExactly)
            if len(items) > 0:
                row = self.fenetre_2.listWidget.row(items[0])
                self.fenetre_2.listWidget.takeItem(row)

            # On fait apparaitre un nouvel avion
            self.spawn_avions(1)

        #A chaque tours on va verifier si on a gagné
        if self.victory is not None:
            self.victory.victoire()

        self.canvas.draw()

    def fin_de_jeu(self):
            match selected_button:
                case "Débutant":
                    self.victory_level_1 = True
                case "Intermédiaire":
                    self.victory_level_2 = True
                case "Affirmé":
                    self.victory_level_3 = True
                case "Avancé":
                    self.victory_level_4 = True
                case "TOP GUN":
                    self.victory.top_gun()










class App :
    def __init__(self):
        self.menu = Menu()
        self.jeu = Jeu()

        self.jeu.vicotry = self
        self.high_score = 0

        self.menu.fenetre_1.pushButton_6.clicked.connect(self.launch_level)
        self.jeu.fenetre_2.pushButton_2.clicked.connect(self.home)
        self.jeu.fenetre_2.pushButton_3.clicked.connect(self.quit)
        self.menu.fenetre_1.pushButton.clicked.connect(self.admin)

        self.menu.fenetre_1.showMaximized()


    def victoire(self):
        if (self.jeu.victory_level_1 is True
                and self.jeu.victory_level_2 is True
                and self.jeu.victory_level_3 is True
                and self.jeu.victory_level_4 is True):
            self.menu.fenetre_1.pushButton_5.setEnabled(True)
        if self.jeu.victory_level_1 is True :
            self.menu.fenetre_1.pushButton_1.setStyleSheet("QPushButton {background-color: green;}")
            self.menu.style_button_1 = self.menu.fenetre_1.pushButton_1.styleSheet()
        if self.jeu.victory_level_2 is True :
            self.menu.fenetre_1.pushButton_2.setStyleSheet("QPushButton {background-color: green;}")
            self.menu.style_button_2 = self.menu.fenetre_1.pushButton_1.styleSheet()
        if self.jeu.victory_level_3 is True :
            self.menu.fenetre_1.pushButton_3.setStyleSheet("QPushButton {background-color: green;}")
            self.menu.style_button_3 = self.menu.fenetre_1.pushButton_1.styleSheet()
        if self.jeu.victory_level_4 is True :
            self.menu.fenetre_1.pushButton_4.setStyleSheet("QPushButton {background-color: green;}")
            self.menu.style_button_4 = self.menu.fenetre_1.pushButton_1.styleSheet()

    def admin(self):
        self.jeu.victory_level_1 = True
        self.jeu.victory_level_2 = True
        self.jeu.victory_level_3 = True
        self.jeu.victory_level_4 = True
        self.victoire()

    def top_gun(self):
        score = self.jeu.score
        if score > self.high_score :
            self.high_score = score
        self.menu.fenetre_1.label_3.setText(f"HIGH SCORE \n {self.high_score}")


    def home(self):
        self.jeu.fenetre_2.close()
        self.menu.fenetre_1.showMaximized()
        self.jeu.fenetre_2.listWidget.clear()

        avion_a_supr = []
        for avion in self.jeu.liste_avions :
            avion_a_supr.append(avion)
        for avion in avion_a_supr :#Suppression des avions
            # Déselection de l'avion
            self.jeu.selection("Supr")
            self.jeu.fenetre_2.listWidget.clearSelection()

            # self.compass.set_active(False)

            # Suppression de l'avion dans la liste et le graphique
            avion.effacer()
            self.jeu.liste_avions.remove(avion)
            items = self.jeu.fenetre_2.listWidget.findItems(avion.name, Qt.MatchExactly)
            if len(items) > 0:
                row = self.jeu.fenetre_2.listWidget.row(items[0])
                self.jeu.fenetre_2.listWidget.takeItem(row)

        self.jeu.score = 0
        self.jeu.nb_atterrissages = 0


    def quit(self):
        self.jeu.fenetre_2.close()
        sys.exit()

    def launch_level(self):
        self.jeu.fenetre_2.showMaximized()
        self.menu.fenetre_1.close()
        self.jeu.fenetre_2.label_5.setText(f"Niveau : {selected_button}")

        for i in range(len(self.menu.Bouttons)):
            self.menu.Bouttons[i].setStyleSheet(self.menu.style[i])

        #Creation des avions
        self.jeu.spawn_avions(nb_avions)



if __name__ == "__main__":
    start = App()
    sys.exit(app.exec_())