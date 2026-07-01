#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RADI - Robot d'Accompagnement à la Découverte Informatique
Compagnon numérique éducatif pour les écoles - Version 2.0 (Clippy 2.0)

Améliorations :
- Animations fluides (glisse + rebond)
- Style moderne avec ombres et bordures arrondies
- Fenêtre déplaçable (glisser-déposer)
- Son d'apparition (optionnel)

Auteur: [Ton Nom / Établissement]
Licence: Libre pour usage éducatif non commercial.
"""

import sys
import random
import json
from pathlib import Path
from datetime import datetime

from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QVBoxLayout,
    QWidget,
    QSystemTrayIcon,
    QMenu,
    QGraphicsDropShadowEffect,
)
from PyQt6.QtGui import QPixmap, QIcon, QFont, QAction, QMouseEvent, QCursor
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint, QUrl, pyqtSignal, QSize
from PyQt6.QtMultimedia import QSoundEffect

# =============================================================================
# CONSTANTES
# =============================================================================

# Chemin de la racine du projet (dossier parent de ce fichier)
BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
DATA_DIR = BASE_DIR / "data"

# Fichiers
CONSEILS_FILE = DATA_DIR / "conseils.json"
LOGS_FILE = DATA_DIR / "radi_logs.json"

# =============================================================================
# FONCTIONS UTILITAIRES
# =============================================================================

def charger_conseils():
    """Charge la liste des conseils depuis le fichier JSON."""
    if not CONSEILS_FILE.exists():
        # Créer un fichier par défaut si inexistant
        conseils_default = [
            {
                "id": 1,
                "texte": "⚡ Pense à éteindre ton écran quand tu ne l'utilises pas pour économiser l'énergie !",
                "categorie": "écologie",
                "niveau": "primaire",
            },
            {
                "id": 2,
                "texte": "🔒 Protège tes mots de passe comme un trésor. Ne les partage jamais, même avec tes amis !",
                "categorie": "sécurité",
                "niveau": "collège",
            },
            {
                "id": 3,
                "texte": "📵 Fais des pauses régulières pour reposer tes yeux et bouger un peu ! (Règle 20-20-20)",
                "categorie": "santé",
                "niveau": "tous",
            },
            {
                "id": 4,
                "texte": "💡 Sur internet, tout ce que tu publies peut rester en ligne pour toujours. Réfléchis avant de partager !",
                "categorie": "bonnes_pratiques",
                "niveau": "collège",
            },
            {
                "id": 5,
                "texte": "🛡️ Méfie-toi des messages ou liens suspects, même s'ils semblent venir d'un ami.",
                "categorie": "sécurité",
                "niveau": "tous",
            },
            {
                "id": 6,
                "texte": "📸 Avant de publier une photo de quelqu'un, demande-lui son accord !",
                "categorie": "respect",
                "niveau": "primaire",
            },
            {
                "id": 7,
                "texte": "🔑 Utilise des mots de passe différents pour chaque compte. Un gestionnaire de mots de passe peut t'aider !",
                "categorie": "sécurité",
                "niveau": "collège",
            },
            {
                "id": 8,
                "texte": "🌙 Éteins tes écrans 1 heure avant de dormir pour mieux t'endormir.",
                "categorie": "santé",
                "niveau": "tous",
            },
            {
                "id": 9,
                "texte": "🗑️ Supprime les fichiers inutiles et vide ta corbeille pour libérer de l'espace.",
                "categorie": "écologie",
                "niveau": "primaire",
            },
            {
                "id": 10,
                "texte": "🔍 Vérifie toujours l'URL d'un site avant de saisir tes identifiants (cherche le cadenas 🔒).",
                "categorie": "sécurité",
                "niveau": "collège",
            },
        ]
        DATA_DIR.mkdir(exist_ok=True)
        with open(CONSEILS_FILE, "w", encoding="utf-8") as f:
            json.dump(conseils_default, f, indent=2, ensure_ascii=False)
        return conseils_default

    with open(CONSEILS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def log_conseil(conseil_id: int):
    """Enregistre qu'un conseil a été affiché."""
    logs = []
    if LOGS_FILE.exists():
        try:
            with open(LOGS_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            logs = []

    logs.append(
        {
            "conseil_id": conseil_id,
            "date": datetime.now().isoformat(),
            "vu": True,
        }
    )

    with open(LOGS_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)


def get_non_vus_recemment(conseils: list, limite_jours: int = 1) -> list:
    """Retourne les conseils non vus récemment."""
    if not LOGS_FILE.exists():
        return conseils

    try:
        with open(LOGS_FILE, "r", encoding="utf-8") as f:
            logs = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return conseils

    # Filtrer les conseils vus il y a moins de `limite_jours` jours
    conseils_vus_recemment = set()
    for log in logs:
        log_date = datetime.fromisoformat(log["date"])
        if (datetime.now() - log_date).days < limite_jours:
            conseils_vus_recemment.add(log["conseil_id"])

    # Retourner les conseils non vus récemment
    return [c for c in conseils if c.get("id") not in conseils_vus_recemment]


# =============================================================================
# CLASSE PRINCIPALE : FENÊTRE RADI
# =============================================================================


class RadiWindow(QWidget):
    """Fenêtre flottante affichant RADI et un conseil.
    
    Fonctionnalités :
    - Effet d'ombre moderne
    - Déplacement par glisser-déposer
    - Animations fluides
    """

    # Signal pour le déplacement
    move_signal = pyqtSignal(QPoint)

    def __init__(self, assets_dir: Path):
        super().__init__()

        # Configuration de la fenêtre
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(240, 300)
        
        # Variables pour le déplacement
        self.old_pos = None
        self.dragging = False
        
        # Style moderne : ombre portée
        self.set_ombre_effet()

        # Layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Image de RADI
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Charger l'image (avec fallback si introuvable)
        image_path = assets_dir / "radi.png"
        if image_path.exists():
            pixmap = QPixmap(str(image_path))
            if not pixmap.isNull():
                self.image_label.setPixmap(pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))
                print("✅ Image chargée depuis : assets/radi.png")
            else:
                self.image_label.setText("🤖")
                self.image_label.setFont(QFont("Segoe UI Emoji", 60))
                print("⚠️  assets/radi.png existe mais ne peut pas être chargé comme image")
        else:
            self.image_label.setText("🤖")
            self.image_label.setFont(QFont("Segoe UI Emoji", 60))
            print("⚠️  assets/radi.png introuvable. Utilisation de l'emoji 🤖")

        self.layout.addWidget(self.image_label)

        # Texte du conseil
        self.conseil_label = QLabel()
        self.conseil_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        self.conseil_label.setWordWrap(True)
        self.conseil_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.conseil_label.setStyleSheet(
            """
            QLabel {
                color: #FFFFFF;
                background: rgba(40, 40, 60, 220);
                padding: 16px 12px 16px 12px;
                border-radius: 14px;
                margin: 8px;
                border: 1px solid rgba(255, 255, 255, 30);
            }
            """
        )
        self.layout.addWidget(self.conseil_label)

        # Animations
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(400)
        self.animation.setEasingCurve(QEasingCurve.Type.OutBack)
        
        # Animation d'opacité pour un effet plus doux
        self.opacity_animation = QPropertyAnimation(self, b"windowOpacity")
        self.opacity_animation.setDuration(300)

        # Timer pour la fermeture automatique
        self.close_timer = QTimer(self)
        self.close_timer.setSingleShot(True)
        self.close_timer.timeout.connect(self.hide)

        # Position initiale
        self.move_to_corner()

    def set_ombre_effet(self):
        """Ajoute un effet d'ombre moderne à la fenêtre."""
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(12)  # Flou réduit pour éviter les bugs Windows
        shadow.setXOffset(0)       # Décalage horizontal
        shadow.setYOffset(3)      # Légère ombre vers le bas
        shadow.setColor(Qt.GlobalColor.black)  # Couleur de l'ombre
        self.setGraphicsEffect(shadow)

    def move_to_corner(self):
        """Positionne la fenêtre en bas à droite de l'écran."""
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() - self.width() - 20, screen.height() - self.height() - 20)

    def show_conseil(self, texte: str, duration: int = 15000):
        """Affiche un conseil avec animation améliorée (fondu)."
        self.conseil_label.setText(texte)

        # Positionner la fenêtre à sa position finale
        self.move_to_corner()
        
        # Animation de fondu pour éviter les bugs Windows avec les fenêtres transparentes
        self.setWindowOpacity(0)
        self.show()
        
        # Animation d'opacité (0 -> 1)
        self.opacity_animation.setStartValue(0)
        self.opacity_animation.setEndValue(1)
        self.opacity_animation.start()

        # Fermeture automatique après `duration` ms
        self.close_timer.start(duration)

    def mousePressEvent(self, event):
        """Début du déplacement par glisser-déposer."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()
            self.dragging = True
            # On n'a pas besoin de hide() ici, on va déplacer

    def mouseMoveEvent(self, event):
        """Déplacement de la fenêtre."""
        if self.dragging and self.old_pos:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        """Fin du déplacement."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            self.old_pos = None
            # Fermer la fenêtre si on a juste cliqué (pas déplacé)
            if event.globalPosition().toPoint() == self.old_pos:
                self.hide()


# =============================================================================
# CLASSE APPLICATION : GESTION GLOBALE
# =============================================================================


class RadiApp:
    """Application principale de RADI."""

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        self.app.setApplicationName("RADI")
        self.app.setApplicationVersion("2.0.0")

        # Vérifier/créer les dossiers nécessaires
        ASSETS_DIR.mkdir(exist_ok=True)
        DATA_DIR.mkdir(exist_ok=True)
        
        # Initialiser le son (optionnel)
        self.sound_effect = None
        self.init_sound()

        # Fenêtre principale
        self.window = RadiWindow(ASSETS_DIR)

        # Icône dans la barre des tâches
        self.tray_icon = QSystemTrayIcon(self.app)
        icon_path = ASSETS_DIR / "radi.png"
        if icon_path.exists():
            self.tray_icon.setIcon(QIcon(str(icon_path)))
            print("✅ Icône chargée depuis : assets/radi.png")
        else:
            # Utiliser une icône système par défaut (computer, folder, etc.)
            try:
                # Essayer plusieurs icônes système courantes
                for theme_icon in ["computer", "application-x-executable", "folder", "dialog-information"]:
                    icon = QIcon.fromTheme(theme_icon)
                    if not icon.isNull():
                        self.tray_icon.setIcon(icon)
                        print(f"⚠️  assets/radi.png introuvable. Utilisation de l'icône système : {theme_icon}")
                        break
                else:
                    # Si aucune icône thème ne fonctionne, créer une icône vide (affichera l'icône par défaut de QSystemTrayIcon)
                    self.tray_icon.setIcon(QIcon())
                    print("⚠️  assets/radi.png introuvable. Aucune icône système trouvée.")
            except Exception as e:
                print(f"⚠️  Erreur avec les icônes système : {e}")
                self.tray_icon.setIcon(QIcon())
            print("💡 Pour résoudre : exécute 'python generate_radi.py' pour créer radi.png")

        # Menu du tray
        tray_menu = QMenu()
        
        action_conseil = QAction("Afficher un conseil", self.app)
        action_conseil.triggered.connect(self.show_random_conseil)
        tray_menu.addAction(action_conseil)
        
        tray_menu.addSeparator()
        
        # Option pour activer/désactiver le son
        self.son_active = True
        action_son = QAction("Son activé", self.app)
        action_son.setCheckable(True)
        action_son.setChecked(self.son_active)
        action_son.triggered.connect(self.toggle_son)
        tray_menu.addAction(action_son)
        
        tray_menu.addSeparator()
        
        action_quitter = QAction("Quitter RADI", self.app)
        action_quitter.triggered.connect(self.quit)
        tray_menu.addAction(action_quitter)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        # Timer pour afficher des conseils périodiquement
        # 300000 ms = 5 minutes (ajustable)
        self.timer = QTimer()
        self.timer.timeout.connect(self.show_random_conseil)
        self.timer.start(300000)

    def init_sound(self):
        """Initialise le son d'apparition."""
        sound_path = ASSETS_DIR / "pop.wav"
        if sound_path.exists():
            self.sound_effect = QSoundEffect()
            self.sound_effect.setSource(QUrl.fromLocalFile(str(sound_path)))
            self.sound_effect.setVolume(0.5)  # Volume à 50%
            print("🔊 Son chargé depuis : assets/pop.wav")
        else:
            print("💡 Pour activer le son : place un fichier 'pop.wav' dans assets/")

    def play_sound(self):
        """Joue le son d'apparition."""
        if self.sound_effect and self.son_active:
            self.sound_effect.play()

    def toggle_son(self, state):
        """Active/désactive le son."""
        self.son_active = state
        action = self.tray_icon.contextMenu().actions()[2]  # 3ème action = son
        action.setText("Son activé" if state else "Son désactivé")
        print(f"🔊 Son {'activé' if state else 'désactivé'}")

    def show_random_conseil(self):
        """Affiche un conseil aléatoire."""
        conseils = charger_conseils()

        # Essayer de prendre un conseil non vu récemment
        conseils_non_vus = get_non_vus_recemment(conseils)
        if conseils_non_vus:
            conseil = random.choice(conseils_non_vus)
        else:
            conseil = random.choice(conseils)

        # Jouer le son
        self.play_sound()
        
        # Afficher et logger
        self.window.show_conseil(conseil["texte"])
        if "id" in conseil:
            log_conseil(conseil["id"])

    def quit(self):
        """Quitte l'application."""
        self.app.quit()

    def run(self):
        """Lance l'application."""
        print("=" * 60)
        print("🚀 RADI v2.0 (Clippy 2.0) est lancé !")
        print("=" * 60)
        print("✨Nouveautés :")
        print("  • Animation fluide avec effet rebond")
        print("  • Style moderne avec ombres")
        print("  • Fenêtre déplaçable (glisser-déposer)")
        print("  • Menu étendu (clic droit sur l'icône)")
        print("=" * 60)
        print("💡 Attends 3 secondes pour le premier conseil...")
        print("📍 Astuce : Clic droit sur l'icône → 'Son activé/désactivé'")
        print("=" * 60)
        # Afficher un conseil au démarrage (après 3 secondes)
        QTimer.singleShot(3000, self.show_random_conseil)
        sys.exit(self.app.exec())


# =============================================================================
# POINT D'ENTRÉE
# =============================================================================

if __name__ == "__main__":
    RadiApp().run()
