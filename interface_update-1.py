import sys
import os
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLabel, QWidget, QFrame


class ArcadeLauncher(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # --- 1. CONFIGURATION DE LA FENÊTRE ---
        self.setWindowTitle("Aviation Arcade - Launcher")
        self.resize(1024, 600)  # Taille par défaut

        # --- 2. GESTION DU FOND D'ÉCRAN ---
        # On cherche l'image dans le même dossier que le script
        image_name = "background.jpg"  # <--- MET LE NOM DE TON IMAGE ICI
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, image_name)

        if os.path.exists(image_path):
            # Création de la palette pour mettre l'image en fond
            pixmap = QtGui.QPixmap(image_path)
            # On adapte l'image à la taille de l'écran (optionnel, sinon elle se répète ou se coupe)
            pixmap = pixmap.scaled(self.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                   QtCore.Qt.TransformationMode.SmoothTransformation)
            palette = QtGui.QPalette()
            brush = QtGui.QBrush(pixmap)
            palette.setBrush(QtGui.QPalette.ColorRole.Window, brush)
            self.setPalette(palette)
        else:
            print(f"ATTENTION : L'image '{image_name}' n'a pas été trouvée. Fond gris par défaut.")
            self.setStyleSheet("background-color: #333;")

        # --- 3. CRÉATION DES ÉLÉMENTS (WIDGETS) ---

        # Le widget central qui contient tout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout vertical pour empiler les éléments
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # Tout centrer
        self.layout.setSpacing(15)  # Espace entre les boutons

        # Titre (Optionnel, style arcade)
        self.lbl_title = QLabel("SELECT DIFFICULTY")
        self.lbl_title.setStyleSheet(
            "color: white; font-size: 30px; font-weight: bold; font-family: 'Courier New'; background: transparent;")
        self.lbl_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.lbl_title)

        # -- CRÉATION AUTOMATIQUE DES 5 BOUTONS DE DIFFICULTÉ --
        self.selected_difficulty = 1
        self.difficulty_buttons = []  # Liste pour stocker les boutons

        difficulty_names = ["PILOTE DÉBUTANT", "CADET", "COMMANDANT", "TOP GUN", "EXPERT"]

        for i in range(5):
            level = i + 1
            btn_name = difficulty_names[i]

            btn = QPushButton(f"{level}. {btn_name}")
            btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            btn.setFixedSize(300, 50)  # Taille fixe pour que ce soit propre

            # Connexion du clic : attention à la "lambda" pour capturer la bonne valeur de level
            btn.clicked.connect(lambda checked, l=level: self.set_difficulty(l))

            self.layout.addWidget(btn)
            self.difficulty_buttons.append(btn)

        # Séparateur vide pour espacer
        spacer = QFrame()
        spacer.setFrameShape(QFrame.Shape.HLine)
        spacer.setFixedSize(300, 20)
        spacer.setStyleSheet("background: transparent;")
        self.layout.addWidget(spacer)

        # -- BOUTON JOUER --
        self.btn_play = QPushButton("DÉCOLLAGE IM MÉDIAT")
        self.btn_play.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.btn_play.setFixedSize(350, 70)
        self.btn_play.clicked.connect(self.launch_game)
        self.layout.addWidget(self.btn_play)

        # --- 4. STYLE INITIAL ---
        self.update_ui_styles()

    def set_difficulty(self, level):
        """Change le niveau et met à jour les couleurs"""
        self.selected_difficulty = level
        print(f"Niveau choisi : {self.selected_difficulty}")
        self.update_ui_styles()

    def update_ui_styles(self):
        """Applique le look ARCADE (Néon/Pixel)"""

        # Style pour les boutons de difficulté INACTIFS
        style_diff_inactive = """
            QPushButton {
                background-color: rgba(0, 0, 0, 180);
                color: #aaaaaa;
                border: 2px solid #555;
                border-radius: 5px;
                font-family: 'Courier New';
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                border: 2px solid #ffffff;
                color: white;
            }
        """

        # Style pour le bouton de difficulté SÉLECTIONNÉ (Vert/Bleu néon)
        style_diff_active = """
            QPushButton {
                background-color: rgba(0, 255, 100, 200);
                color: black;
                border: 3px solid white;
                border-radius: 5px;
                font-family: 'Courier New';
                font-weight: bold;
                font-size: 18px;
            }
        """

        # Style pour le gros bouton JOUER (Rouge/Orange)
        style_play = """
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffcc00, stop:1 #ff6600);
                color: black;
                border: 4px solid white;
                border-radius: 15px;
                font-family: 'Arial Black';
                font-size: 22px;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffee00, stop:1 #ff8800);
            }
            QPushButton:pressed {
                background-color: #cc4400;
                border: 4px solid #aaaaaa;
            }
        """

        # Application des styles
        for index, btn in enumerate(self.difficulty_buttons):
            level = index + 1
            if level == self.selected_difficulty:
                btn.setStyleSheet(style_diff_active)
            else:
                btn.setStyleSheet(style_diff_inactive)

        self.btn_play.setStyleSheet(style_play)

    def launch_game(self):
        print(f"--- LANCEMENT DU JEU (Difficulté {self.selected_difficulty}) ---")
        # Ici, tu mettras le code pour lancer ta fenêtre de jeu Pygame
        # ex: jeu = Jeu(self.selected_difficulty)
        # jeu.run()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ArcadeLauncher()
    window.show()
    sys.exit(app.exec())