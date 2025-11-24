import sys
from PyQt6 import QtWidgets, uic, QtCore, QtGui


class ArcadeLauncher(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # 1. Chargement de l'interface .ui faite sur Qt Designer
        # Assure-toi que le fichier est bien dans le même dossier
        try:
            uic.loadUi("launcher.ui", self)
        except FileNotFoundError:
            print("Erreur : Le fichier 'launcher.ui' est introuvable.")
            sys.exit()

        # 2. Variables du jeu
        self.selected_difficulty = 1  # Par défaut : Niveau 1

        # 3. Configuration des boutons
        # On met les boutons dans une liste pour les gérer facilement
        self.difficulty_buttons = [
            self.btn_diff_1,
            self.btn_diff_2,
            self.btn_diff_3,
            self.btn_diff_4,
            self.btn_diff_5
        ]

        # On connecte chaque bouton à la fonction de sélection
        for index, btn in enumerate(self.difficulty_buttons):
            # L'index va de 0 à 4, donc on ajoute 1 pour avoir le niveau 1 à 5
            level = index + 1
            btn.clicked.connect(lambda checked, l=level: self.set_difficulty(l))

        # Connexion du bouton JOUER
        self.btn_play.clicked.connect(self.launch_game)

        # 4. Initialisation visuelle
        self.update_ui_styles()

        # Titre de la fenêtre
        self.setWindowTitle("Aviation Arcade - Launcher")

    def set_difficulty(self, level):
        """Met à jour le niveau choisi et rafraîchit le visuel"""
        self.selected_difficulty = level
        print(f"Difficulté sélectionnée : {self.selected_difficulty}")

        # Si tu as un label de statut, on le met à jour
        if hasattr(self, 'lbl_status'):
            self.lbl_status.setText(f"Niveau actuel : {self.selected_difficulty}")

        self.update_ui_styles()

    def update_ui_styles(self):
        """
        Applique un style CSS pour montrer quel bouton est actif.
        C'est ici qu'on donne le look 'Arcade'.
        """
        # Style pour un bouton inactif (gris/normal)
        style_inactive = """
            QPushButton {
                background-color: rgba(0, 0, 0, 150);
                color: white;
                border: 2px solid #555;
                border-radius: 10px;
                font-weight: bold;
                font-family: 'Courier New', monospace;
            }
            QPushButton:hover {
                border: 2px solid #00aaff;
            }
        """

        # Style pour le bouton ACTIF (Brillant, Neon)
        style_active = """
            QPushButton {
                background-color: rgba(0, 170, 255, 180);
                color: white;
                border: 3px solid #ffffff;
                border-radius: 10px;
                font-weight: bold;
                font-size: 14px;
                font-family: 'Courier New', monospace;
            }
        """

        for index, btn in enumerate(self.difficulty_buttons):
            level = index + 1
            if level == self.selected_difficulty:
                btn.setStyleSheet(style_active)
            else:
                btn.setStyleSheet(style_inactive)

    def launch_game(self):
        """Fonction appelée quand on clique sur JOUER"""
        print("------------------------------------------------")
        print(f"Lancement du jeu avec Difficulté : {self.selected_difficulty}")
        print("Chargement des assets...")
        print("Vroum vroum ! Décollage !")
        print("------------------------------------------------")

        # ICI : Tu peux fermer cette fenêtre et lancer ton jeu Pygame ou autre
        # self.close()
        # main_game.run(self.selected_difficulty)


# --- Exécution de l'application ---
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ArcadeLauncher()
    window.show()
    sys.exit(app.exec())