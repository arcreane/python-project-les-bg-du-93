import sys
import random
from math import pi, tan, sqrt, atan2, degrees, cos, sin, radians
import os

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, Qt, QPoint
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Circle
from matplotlib.path import Path
from matplotlib.markers import MarkerStyle
from matplotlib.transforms import Affine2D

# Votre fichier d'interface
from interface import Ui_MainWindow

# --- CONFIGURATION DES IMAGES ---
IMAGE_MENU = "fond_menu.png"
IMAGE_JEU = "fond_jeu.png"

# --- Paramètres Globaux ---
xlim = 1000
ylim = 1000
zmin = 9000
zmax = 12000

# Paramètres de vitesse (en pixels par tick)
VITESSE_DEFAUT = 5.0
VITESSE_MIN = 2.0
VITESSE_MAX = 10.0
PAS_VITESSE = 1.0  # Combien on ajoute/enlève à chaque clic

COULEURS_DISPO = [
    ("Rouge", "red"), ("Bleu", "blue"), ("Vert", "green"),
    ("Orange", "darkorange"), ("Violet", "purple"), ("Cyan", "cyan"),
    ("Magenta", "magenta"), ("Noir", "black"), ("Marron", "brown"), ("Gris", "gray")
]

verts = [(1, 0), (-1, 1), (-0.5, 0), (-1, -1), (1, 0)]
codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
PLANE_PATH = Path(verts, codes)

# ==========================================
# --- STYLES PIXEL ART ---
# ==========================================
STYLE_PIXEL_ORANGE = """
QPushButton {
    background-color: #eda339; color: #2d1b00;
    font-family: 'Courier New', monospace; font-weight: bold; font-size: 16px;
    border: 4px solid black;
    border-top-color: #ffcc88; border-left-color: #ffcc88;
    border-bottom-color: #a66b1e; border-right-color: #a66b1e;
    padding: 5px;
}
QPushButton:hover { background-color: #ffb85c; }
QPushButton:pressed {
    background-color: #a66b1e;
    border-top-color: #2d1b00; border-left-color: #2d1b00;
    border-bottom-color: #ffcc88; border-right-color: #ffcc88;
    padding-top: 7px; padding-left: 7px;
}
QPushButton:checked {
     background-color: #4cd74c; color: #004d00; border: 4px solid black;
     border-top-color: #8aff8a; border-left-color: #8aff8a;
     border-bottom-color: #006400; border-right-color: #006400;
}
"""

STYLE_PIXEL_VERT = """
QPushButton {
    background-color: #26c226; color: black;
    font-family: 'Courier New', monospace; font-weight: bold; font-size: 20px;
    border: 4px solid black;
    border-top-color: #66ff66; border-left-color: #66ff66;
    border-bottom-color: #006400; border-right-color: #006400;
    padding: 5px;
}
QPushButton:hover { background-color: #33d633; }
QPushButton:pressed {
    background-color: #006400;
    border-top-color: #003300; border-left-color: #003300;
    border-bottom-color: #66ff66; border-right-color: #66ff66;
    padding-top: 7px; padding-left: 7px;
}
"""

STYLE_PIXEL_ROUGE = """
QPushButton {
    background-color: #d62626; color: white;
    font-family: 'Courier New', monospace; font-weight: bold; font-size: 14px;
    border: 3px solid black;
    border-top-color: #ff6666; border-left-color: #ff6666;
    border-bottom-color: #640000; border-right-color: #640000;
}
QPushButton:hover { background-color: #e63333; }
QPushButton:pressed {
    background-color: #640000;
    border-top-color: #330000; border-left-color: #330000;
    border-bottom-color: #ff6666; border-right-color: #ff6666;
    padding-top: 5px; padding-left: 5px;
}
"""


# ==========================================
# WIDGET BOUSSOLE
# ==========================================
class CompassWidget(QtWidgets.QWidget):
    angleChanged = QtCore.pyqtSignal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(100, 100)
        self.angle = 0.0
        self.active = False

    def set_angle(self, radians):
        self.angle = radians
        self.update()

    def set_active(self, active):
        self.active = active
        self.update()

    def mousePressEvent(self, event):
        if self.active and event.button() == Qt.LeftButton:
            self._update_angle_from_mouse(event.pos())

    def mouseMoveEvent(self, event):
        if self.active and (event.buttons() & Qt.LeftButton):
            self._update_angle_from_mouse(event.pos())

    def _update_angle_from_mouse(self, pos):
        center = QPoint(self.width() // 2, self.height() // 2)
        dx = pos.x() - center.x()
        dy = pos.y() - center.y()
        new_angle = atan2(-dy, dx)
        self.angle = new_angle
        self.angleChanged.emit(self.angle)
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        center = QPoint(w // 2, h // 2)
        radius = min(w, h) // 2 - 5

        painter.setBrush(QtGui.QColor("#1a1a1a"))
        painter.setPen(QtGui.QPen(QtGui.QColor("black"), 2))
        painter.drawEllipse(center, radius, radius)

        painter.setPen(QtGui.QColor("#4cd74c"))
        painter.setFont(QtGui.QFont("Courier New", 10, QtGui.QFont.Bold))
        painter.drawText(center.x() - 5, center.y() - radius + 15, "N")
        painter.drawText(center.x() + radius - 15, center.y() + 5, "E")
        painter.drawText(center.x() - 5, center.y() + radius - 5, "S")
        painter.drawText(center.x() - radius + 5, center.y() + 5, "W")

        if not self.active: return

        needle_len = radius - 10
        end_x = center.x() + needle_len * cos(self.angle)
        end_y = center.y() - needle_len * sin(self.angle)

        pen_needle = QtGui.QPen(QtGui.QColor("yellow"), 3)
        painter.setPen(pen_needle)
        painter.drawLine(center, QPoint(int(end_x), int(end_y)))
        painter.setBrush(QtGui.QColor("yellow"))
        painter.drawEllipse(center, 4, 4)


# ==========================================
# CLASSE AVION
# ==========================================
class Avion:
    def __init__(self, ax, nom_couleur, code_couleur, suffixe=""):
        self.ax = ax
        self.name = f"Avion {nom_couleur}{suffixe}"
        self.short_name = f"{nom_couleur}{suffixe}"
        self.color_code = code_couleur

        self.x = 0.0
        self.y = 0.0
        self.spawn_on_edge()
        self.z = random.uniform(zmin, zmax)

        # --- NOUVELLE GESTION VITESSE ---
        # On définit une vitesse de base propre à chaque avion (légère variation)
        # Mais le contrôle se fait sur une valeur absolue
        variation = random.uniform(-0.5, 0.5)
        self.vitesse_actuelle = VITESSE_DEFAUT + variation

        self.teta = 0.0
        self.calculer_cap_vers_centre()

        self.line_x = []
        self.line_y = []
        self.update_trajectory_line()

        self.line, = self.ax.plot(self.line_x, self.line_y, color=self.color_code, linestyle='-', alpha=0.3)
        t = Affine2D().rotate_deg(degrees(self.teta))
        m = MarkerStyle(PLANE_PATH, transform=t)
        self.point, = self.ax.plot(self.x, self.y, marker=m, markersize=15, color=self.color_code, picker=10)

        self.approaching = False
        self.finished = False

        self.update_equation_droite()

    def spawn_on_edge(self):
        cote = random.randint(1, 4)
        if cote == 1:
            self.x, self.y = -xlim, random.uniform(-ylim, ylim)
        elif cote == 2:
            self.x, self.y = xlim, random.uniform(-ylim, ylim)
        elif cote == 3:
            self.x, self.y = random.uniform(-xlim, xlim), -ylim
        else:
            self.x, self.y = random.uniform(-xlim, xlim), ylim

    def calculer_cap_vers_centre(self):
        target_x = random.uniform(-200, 200)
        target_y = random.uniform(-200, 200)
        self.teta = atan2(target_y - self.y, target_x - self.x)
        self.update_equation_droite()
        self.update_trajectory_line()

    def update_equation_droite(self):
        if abs(cos(self.teta)) < 0.001:
            self.a = 999999
        else:
            self.a = tan(self.teta)
        self.b = self.y - self.a * self.x

    def update_trajectory_line(self):
        distance_visuelle = 2500
        end_x = self.x + distance_visuelle * cos(self.teta)
        end_y = self.y + distance_visuelle * sin(self.teta)
        self.line_x = [self.x, end_x]
        self.line_y = [self.y, end_y]

    def changer_vitesse(self, delta):
        """Ajoute ou retire une valeur fixe à la vitesse"""
        self.vitesse_actuelle += delta
        # Bornes de sécurité
        if self.vitesse_actuelle < VITESSE_MIN:
            self.vitesse_actuelle = VITESSE_MIN
        elif self.vitesse_actuelle > VITESSE_MAX:
            self.vitesse_actuelle = VITESSE_MAX

    def avancer(self):
        if self.finished: return

        # --- LOGIQUE AIMANT (Atterrissage Précis) ---
        if self.approaching:
            dist_centre = sqrt(self.x ** 2 + self.y ** 2)
            if dist_centre < self.vitesse_actuelle * 1.5:
                self.x = 0
                self.y = 0
                self.point.set_data([self.x], [self.y])
                self.finished = True
                return

        dx = self.vitesse_actuelle * cos(self.teta)
        dy = self.vitesse_actuelle * sin(self.teta)

        self.x += dx
        self.y += dy

        self.point.set_data([self.x], [self.y])

        if abs(self.x) > xlim * 1.1 or abs(self.y) > ylim * 1.1:
            self.finished = True

    def get_vitesse_kph(self):
        # Affichage fictif en km/h (x60 pour faire joli)
        return int(self.vitesse_actuelle * 60)

    def get_current_pos(self):
        return self.x, self.y

    def get_distance_to_center(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def get_distance_to_plane(self, other):
        x2, y2 = other.get_current_pos()
        return sqrt((x2 - self.x) ** 2 + (y2 - self.y) ** 2)

    def start_approach(self):
        if self.finished or self.approaching: return

        target_angle = atan2(0 - self.y, 0 - self.x)
        self.changer_cap(target_angle)
        self.approaching = True

        self.line.set_linestyle('--')
        self.line.set_linewidth(2)

    def changer_cap(self, angle_radians):
        if self.finished: return
        self.approaching = False

        self.teta = angle_radians

        t = Affine2D().rotate_deg(degrees(self.teta))
        self.point.set_marker(MarkerStyle(PLANE_PATH, transform=t))

        self.update_equation_droite()
        self.update_trajectory_line()
        self.line.set_data(self.line_x, self.line_y)
        self.line.set_linestyle(':')

    def effacer(self):
        self.point.remove()
        self.line.remove()

    def pouvait_atterrir(self):
        dist = abs(self.b) / sqrt(self.a ** 2 + 1)
        return dist <= 150


# ==========================================
# 1. LA FENÊTRE DE MENU (LAUNCHER)
# ==========================================
class Ui_MenuWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 550)

        style_fond = "background-color: #2b2b2b;"
        if os.path.exists(IMAGE_MENU):
            img_path = IMAGE_MENU.replace('\\', '/')
            style_fond = f"border-image: url({img_path}) 0 0 0 0 stretch stretch;"

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet(f"#centralwidget {{ {style_fond} }}")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setContentsMargins(50, 30, 50, 30)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setText("AVIATION ARCADE")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet("""
            color: #FFD700;
            font-size: 32px; font-weight: bold; font-family: 'Courier New';
            background-color: rgba(0, 0, 0, 180); border: 4px solid black;
            padding: 10px; margin-bottom: 20px;
        """)
        self.verticalLayout.addWidget(self.label)

        self.label_niv = QtWidgets.QLabel("SÉLECTIONNEZ LA DIFFICULTÉ :", self.centralwidget)
        self.label_niv.setAlignment(QtCore.Qt.AlignCenter)
        self.label_niv.setStyleSheet(
            "color: white; font-family: 'Courier New'; font-weight: bold; background-color: rgba(0,0,0,100); padding: 5px;")
        self.verticalLayout.addWidget(self.label_niv)

        self.buttons = []
        labels = [
            "1. DÉBUTANT (1 Avion)",
            "2. CADET (2 Avions)",
            "3. COMMANDANT (3 Avions)",
            "4. EXPERT (4 Avions)",
            "5. TOP GUN (10 Avions)"
        ]

        for i, text in enumerate(labels):
            btn = QtWidgets.QPushButton(self.centralwidget)
            btn.setText(text)
            btn.setMinimumHeight(45)
            btn.setStyleSheet(STYLE_PIXEL_ORANGE)
            btn.setCheckable(True)
            self.verticalLayout.addWidget(btn)
            self.buttons.append(btn)

        self.verticalLayout.addSpacing(20)

        self.launch_btn = QtWidgets.QPushButton(self.centralwidget)
        self.launch_btn.setText("DÉCOLLAGE IMMÉDIAT")
        self.launch_btn.setMinimumHeight(70)
        self.launch_btn.setStyleSheet(STYLE_PIXEL_VERT)
        self.verticalLayout.addWidget(self.launch_btn)

        MainWindow.setCentralWidget(self.centralwidget)


class MenuWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MenuWindow()
        self.ui.setupUi(self)
        self.selected_level = 1
        for i, btn in enumerate(self.ui.buttons):
            btn.clicked.connect(lambda checked, idx=i: self.select_level(idx))
        self.select_level(0)
        self.ui.launch_btn.clicked.connect(self.launch_game)

    def select_level(self, index):
        for i, btn in enumerate(self.ui.buttons):
            if i == index:
                btn.setChecked(True)
                if index == 4:
                    self.selected_level = 10
                else:
                    self.selected_level = index + 1
            else:
                btn.setChecked(False)

    def launch_game(self):
        self.game_window = MainWindow(nb_avions_depart=self.selected_level)
        self.game_window.showFullScreen()
        self.close()

    # ==========================================


# 2. LA FENÊTRE DE JEU (MAINWINDOW)
# ==========================================
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure(figsize=(5, 4), dpi=100)
        fig.subplots_adjust(left=0.04, right=0.99, bottom=0.04, top=0.99)
        fig.patch.set_facecolor('none')
        self.ax = fig.add_subplot(111)
        self.ax.set_facecolor((0, 0, 0, 0.5))
        self.ax.tick_params(colors='white')
        for spine in self.ax.spines.values():
            spine.set_edgecolor('white')
        super().__init__(fig)
        self.setParent(parent)
        self.setStyleSheet("background: transparent;")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, nb_avions_depart=5):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        style_fond = "background-color: #2b2b2b;"
        if os.path.exists(IMAGE_JEU):
            img_path = IMAGE_JEU.replace('\\', '/')
            style_fond = f"border-image: url({img_path}) 0 0 0 0 stretch stretch;"

        self.setStyleSheet(f"""
            QMainWindow {{ {style_fond} }}
            QWidget#centralwidget {{ background: transparent; }}
            QLabel {{ color: white; font-family: 'Courier New'; font-weight: bold; }}
            QGroupBox {{ 
                background-color: rgba(0, 0, 0, 180); 
                color: white; 
                font-family: 'Courier New'; 
                font-weight: bold; 
                border: 2px solid #555; 
                margin-top: 10px; 
            }}
            QGroupBox::title {{ subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; background-color: transparent; }}
            QListWidget {{ background-color: rgba(0, 0, 0, 180); color: white; border: 3px solid black; font-family: 'Courier New'; }}
            {STYLE_PIXEL_ORANGE}
        """)

        self.target_nb_avions = nb_avions_depart

        # --- INTERFACE ---
        new_central_widget = QtWidgets.QWidget()
        new_central_widget.setObjectName("centralwidget")
        main_layout = QtWidgets.QHBoxLayout(new_central_widget)

        self.canvas = MplCanvas(self)
        main_layout.addWidget(self.canvas, stretch=3)

        right_panel = QtWidgets.QWidget()
        right_layout = QtWidgets.QVBoxLayout(right_panel)
        main_layout.addWidget(right_panel, stretch=1)

        self.ui.listWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        right_layout.addWidget(QtWidgets.QLabel("<b>TOUR DE CONTRÔLE</b>"))
        right_layout.addWidget(self.ui.listWidget)

        alert_box = QtWidgets.QGroupBox("STATUT TRAFIC")
        alert_layout = QtWidgets.QVBoxLayout()
        self.ui.label_7.setAlignment(QtCore.Qt.AlignCenter)
        alert_layout.addWidget(self.ui.label_7)
        alert_box.setLayout(alert_layout)
        right_layout.addWidget(alert_box)

        info_box = QtWidgets.QGroupBox("INFORMATIONS AVION")
        info_layout = QtWidgets.QVBoxLayout()
        info_layout.addWidget(self.ui.label_5)
        info_layout.addWidget(self.ui.label_6)
        info_box.setLayout(info_layout)
        right_layout.addWidget(info_box)

        action_box = QtWidgets.QGroupBox("ACTIONS PILOTE")
        action_layout = QtWidgets.QVBoxLayout()
        speed_layout = QtWidgets.QHBoxLayout()

        # --- NOUVEAUX BOUTONS VITESSE ---
        self.ui.pushButton_3.setText("ACCÉLÉRER (+)")
        self.ui.pushButton_2.setText("RALENTIR (-)")

        speed_layout.addWidget(self.ui.pushButton_3)
        speed_layout.addWidget(self.ui.pushButton_2)
        action_layout.addLayout(speed_layout)
        action_layout.addWidget(self.ui.pushButton)

        self.compass = CompassWidget()
        action_layout.addWidget(QtWidgets.QLabel("Modif. Cap :"))
        action_layout.addWidget(self.compass, 0, QtCore.Qt.AlignCenter)

        action_box.setLayout(action_layout)
        right_layout.addWidget(action_box)

        right_layout.addStretch()

        stats_box = QtWidgets.QGroupBox("STATISTIQUES")
        stats_layout = QtWidgets.QVBoxLayout()
        stats_layout.addWidget(self.ui.label_4)
        stats_layout.addWidget(self.ui.label_3)
        stats_layout.addWidget(self.ui.label_2)
        stats_layout.addWidget(self.ui.label)
        stats_box.setLayout(stats_layout)
        right_layout.addWidget(stats_box)

        sys_layout = QtWidgets.QHBoxLayout()
        self.btn_window_mode = QtWidgets.QPushButton("Fenêtré")
        sys_layout.addWidget(self.btn_window_mode)
        sys_layout.addWidget(self.ui.pushButton_5)
        sys_layout.addWidget(self.ui.pushButton_6)
        right_layout.addLayout(sys_layout)

        self.setCentralWidget(new_central_widget)

        self.ui.pushButton.clicked.connect(self.action_land_selected)
        self.ui.pushButton_3.clicked.connect(self.action_accelerate)
        self.ui.pushButton_2.clicked.connect(self.action_decelerate)
        self.ui.pushButton_6.clicked.connect(self.close)
        self.ui.pushButton_5.clicked.connect(self.go_home)
        self.btn_window_mode.clicked.connect(self.action_toggle_fullscreen)
        self.compass.angleChanged.connect(self.update_plane_heading)

        self.ui.pushButton_5.setStyleSheet(STYLE_PIXEL_VERT)
        self.ui.pushButton_6.setStyleSheet(STYLE_PIXEL_ROUGE)

        self.ui.listWidget.itemClicked.connect(self.action_select_plane)
        self.canvas.mpl_connect('pick_event', self.on_pick)

        self.canvas.ax.axhline(y=0, color='white', linewidth=1)
        self.canvas.ax.axvline(x=0, color='white', linewidth=1)
        mon_cercle = Circle((0, 0), 150, color='#4cd74c', fill=False, linewidth=2, linestyle='--')
        self.canvas.ax.add_patch(mon_cercle)
        self.canvas.ax.set_xlim(-xlim, xlim)
        self.canvas.ax.set_ylim(-ylim, ylim)
        self.canvas.ax.set_aspect('equal')

        self.highlight_marker, = self.canvas.ax.plot([], [], marker='o', markersize=35, color='none',
                                                     markeredgecolor='yellow', markeredgewidth=3, visible=False)

        self.score = 0
        self.nb_atterrissages = 0
        self.liste_avions = []
        self.selected_plane = None
        self.color_index = 0
        self.global_alert_text = "Urgence : RAS"
        self.global_alert_style = "color: #4cd74c;"
        self.is_fullscreen = True

        if self.target_nb_avions == 10:
            txt_niv = "TOP GUN"
        else:
            txt_niv = str(self.target_nb_avions)
        self.ui.label_3.setText(f"Niveau : {txt_niv}")

        self.spawn_plane(self.target_nb_avions)
        self.update_labels_general()

        self.timer = QTimer(self)
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start()

    def go_home(self):
        self.timer.stop()
        self.menu = MenuWindow()
        self.menu.show()
        self.close()

    def action_toggle_fullscreen(self):
        if self.is_fullscreen:
            self.showNormal();
            self.btn_window_mode.setText("Plein Écran");
            self.is_fullscreen = False
        else:
            self.showFullScreen();
            self.btn_window_mode.setText("Fenêtré");
            self.is_fullscreen = True

    def on_pick(self, event):
        for avion in self.liste_avions:
            if avion.point == event.artist:
                self.selected_plane = avion
                self.update_info_panel()
                self.update_highlight()
                items = self.ui.listWidget.findItems(avion.name, QtCore.Qt.MatchExactly)
                if items: self.ui.listWidget.setCurrentItem(items[0])
                break

    def get_next_color(self):
        nom, code = COULEURS_DISPO[self.color_index % len(COULEURS_DISPO)]
        self.color_index += 1
        suffixe = f" {(self.color_index // len(COULEURS_DISPO)) + 1}" if self.color_index // len(
            COULEURS_DISPO) > 0 else ""
        return nom, code, suffixe

    def spawn_plane(self, count=1):
        for _ in range(count):
            nom, code, suf = self.get_next_color()
            p = Avion(self.canvas.ax, nom, code, suf)
            self.liste_avions.append(p)
            self.ui.listWidget.addItem(p.name)

    def action_select_plane(self, item):
        for avion in self.liste_avions:
            if avion.name == item.text():
                self.selected_plane = avion
                self.update_highlight()
                break
        self.update_info_panel()

    def update_highlight(self):
        if self.selected_plane and not self.selected_plane.finished:
            x, y = self.selected_plane.get_current_pos()
            if x != 9999 and not self.selected_plane.finished:
                self.highlight_marker.set_data([x], [y])
                self.highlight_marker.set_visible(True)
                return
        self.highlight_marker.set_visible(False)

    def update_plane_heading(self, angle):
        if self.selected_plane:
            self.selected_plane.changer_cap(angle)

    def action_accelerate(self):
        # Ajoute PAS_VITESSE (ex: +1.0 pixel/tick)
        if self.selected_plane:
            self.selected_plane.changer_vitesse(PAS_VITESSE)
            self.update_info_panel()

    def action_decelerate(self):
        # Retire PAS_VITESSE (ex: -1.0 pixel/tick)
        if self.selected_plane:
            self.selected_plane.changer_vitesse(-PAS_VITESSE)
            self.update_info_panel()

    def action_land_selected(self):
        if self.selected_plane:
            if self.selected_plane.get_distance_to_center() <= 150 and not self.selected_plane.approaching:
                self.selected_plane.start_approach();
                self.ui.pushButton.setEnabled(False)

    def update_labels_general(self):
        self.ui.label_4.setText(f"Score : {self.score}")
        self.ui.label_2.setText(f"Avions en vol : {len(self.liste_avions)}")
        self.ui.label.setText(f"Atterrissages : {self.nb_atterrissages}")
        self.ui.label_7.setText(self.global_alert_text);
        self.ui.label_7.setStyleSheet(self.global_alert_style)

    def update_info_panel(self):
        if self.selected_plane:
            self.ui.label_5.setText(f"Vitesse : {self.selected_plane.get_vitesse_kph()} km/h")
            self.ui.label_6.setText(f"Altitude : {self.selected_plane.z:.0f} m")
            self.ui.label_5.setStyleSheet(f"color: {self.selected_plane.color_code}; font-weight: bold;")
            in_zone = self.selected_plane.get_distance_to_center() <= 150 and not self.selected_plane.approaching
            self.ui.pushButton.setEnabled(in_zone)
            if in_zone:
                self.ui.pushButton.setStyleSheet(STYLE_PIXEL_VERT)
            else:
                self.ui.pushButton.setStyleSheet(STYLE_PIXEL_ORANGE)
            self.compass.set_active(True)
            self.compass.set_angle(self.selected_plane.teta)
        else:
            self.ui.label_5.setText("Vitesse : -");
            self.ui.label_6.setText("Altitude : -")
            self.ui.pushButton.setEnabled(False);
            self.ui.pushButton.setStyleSheet(STYLE_PIXEL_ORANGE)
            self.compass.set_active(False)

    def update_simulation(self):
        avions_suppr = set()
        alert_lvl, alert_txt, alert_col = 0, "Urgence : RAS", "color: #4cd74c;"

        for i, p1 in enumerate(self.liste_avions):
            if p1.finished: continue
            if p1.approaching and alert_lvl < 1: alert_lvl = 1; alert_txt = "Urgence : ATTERRISSAGE"; alert_col = "color: #4cd74c; font-weight: bold;"
            for j in range(i + 1, len(self.liste_avions)):
                p2 = self.liste_avions[j]
                if p2.finished: continue
                dist = p1.get_distance_to_plane(p2)

                if dist < 15:
                    self.score -= 200
                    if self.score < 0: self.score = 0
                    avions_suppr.update([p1, p2])
                    alert_lvl = 3;
                    alert_txt = f"CRASH : {p1.short_name}/{p2.short_name}";
                    alert_col = "color: #d62626; font-weight: bold; font-size: 14px;"
                elif dist < 50 and alert_lvl < 2:
                    alert_lvl = 2;
                    alert_txt = f"DANGER : {p1.short_name}/{p2.short_name}";
                    alert_col = "color: #eda339; font-weight: bold;"

        self.global_alert_text, self.global_alert_style = alert_txt, alert_col

        for p in self.liste_avions:
            if p in avions_suppr: continue
            p.avancer()
            if p.finished:
                if p.approaching:
                    self.score += 100
                    self.nb_atterrissages += 1
                else:
                    if p.pouvait_atterrir():
                        self.score -= 50
                        if self.score < 0: self.score = 0
                avions_suppr.add(p)

        for p in avions_suppr:
            if self.selected_plane == p:
                self.selected_plane = None
                self.ui.listWidget.clearSelection()
                self.highlight_marker.set_visible(False)
                self.compass.set_active(False)

            items = self.ui.listWidget.findItems(p.name, QtCore.Qt.MatchExactly)
            if items: self.ui.listWidget.takeItem(self.ui.listWidget.row(items[0]))
            p.effacer()
            if p in self.liste_avions: self.liste_avions.remove(p)
            self.spawn_plane(1)

        self.update_highlight()
        self.update_labels_general();
        self.update_info_panel();
        self.canvas.draw()

        if self.score >= 1000:
            self.timer.stop()
            msg = QtWidgets.QMessageBox(self)
            msg.setWindowTitle("MISSION ACCOMPLIE")
            msg.setText(
                f"Félicitations Commandant !\n\nVous avez atteint 1000 points au niveau {self.ui.label_3.text()}.")
            msg.setStyleSheet(
                "QMessageBox { background-color: #2b2b2b; } QLabel { color: white; font-family: 'Courier New'; } QPushButton { " + STYLE_PIXEL_VERT + "}")
            msg.exec_()
            self.go_home()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MenuWindow()
    window.show()
    sys.exit(app.exec_())