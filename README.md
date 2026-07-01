# 🤖 RADI - Compagnon Numérique Éducatif pour Écoles

> *Un petit assistant bienveillant pour sensibiliser les enfants au numérique, inspiré de Clippy mais en mieux !*

---

## 📌 **À propos de RADI**

**RADI** (Robot d'Accompagnement à la Découverte Informatique) est un compagnon numérique conçu pour les écoles. Il s'installe sur les PC sous **Windows 10/11**, se lance automatiquement au démarrage et apparaît périodiquement pour donner des **conseils éducatifs** sur :
- La **sécurité en ligne** (mots de passe, phishing)
- Le **bon usage du numérique** (temps d'écran, ergonomie)
- Les **bonnes pratiques** (respect, droit à l'image, empreinte numérique)

**Inspiration** : Clippy (Microsoft Office 97-2003), mais avec une approche **pédagogique et non intrusive**.

---

## 🏗️ **Architecture du Projet**

| **Composant**          | **Rôle**                                  | **Technologie**       |
|------------------------|-------------------------------------------|-----------------------|
| `radi.py`              | Code principal (fenêtre flottante)        | Python + PyQt6        |
| `data/conseils.json`   | Base de données des conseils              | JSON                  |
| `assets/radi.png`      | Sprite du compagnon (style Clippy)        | Image PNG             |
| `install.bat`          | Script d'installation (lancement auto)   | Batch (Windows)       |

---

## 📦 **Structure des Fichiers**

```
RADI/
├── README.md              # Ce fichier
├── radi.py                # Code principal
├── assets/
│   ├── radi.png           # Sprite de RADI (150x150px recommandé)
│   └── sounds/            # (Optionnel) Sons pour les notifications
├── data/
│   └── conseils.json      # Base de conseils éducatifs
└── install.bat            # Script d'installation automatique
```

---

## 🚀 **Installation**

### **Prérequis**
1. **Python 3.10 ou supérieur** installé sur les machines.
   - Téléchargement : [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. **PyQt6** (pour l'interface graphique) :
   ```bash
   pip install PyQt6
   ```

### **Étapes d'installation**
1. **Copier le dossier `RADI/`** sur le PC (ex: `C:\Program Files\RADI\`).
2. **Exécuter `install.bat` en tant qu'administrateur** :
   - Clique droit sur `install.bat` → "Exécuter en tant qu'administrateur".
   - Cela ajoute RADI au **démarrage automatique de Windows**.
3. **Redémarrer le PC** pour vérifier que RADI apparaît bien.

> **⚠️ Note** : Si tu veux éviter d'installer Python sur chaque machine, utilise [PyInstaller](#-créer-un-exécutable-exe) pour générer un `.exe` autonome.

---

## 💻 **Personnalisation**

### **1. Modifier les conseils**
Édite le fichier `data/conseils.json` pour ajouter/supprimer des conseils. Format :
```json
[
    {
        "texte": "⚡ Pense à éteindre ton écran pour économiser l'énergie !",
        "niveau": "primaire",  // Optionnel
        "categorie": "écologie"  // Optionnel
    },
    {
        "texte": "🔒 Ne partage jamais tes mots de passe, même avec tes amis !",
        "niveau": "collège",
        "categorie": "sécurité"
    }
]
```

### **2. Changer l'apparence de RADI**
- Remplace `assets/radi.png` par ton propre sprite (taille recommandée : **150x150 pixels**).
- Pour un effet plus dynamique, utilise un **GIF animé** (à renommer en `.png` ou à adapter dans le code).

### **3. Modifier la fréquence des conseils**
Dans `radi.py`, cherche la ligne :
```python
self.timer.start(300000)  # 300000 ms = 5 minutes
```
- Change `300000` pour ajuster la fréquence (en millisecondes).

---

## 🔧 **Fonctionnalités Avancées (Optionnelles)**

### **🎵 Ajouter des sons**
1. Crée un dossier `assets/sounds/` et ajoute un fichier `.wav` (ex: `pop.wav`).
2. Dans `radi.py`, décommente/modifie le code lié à `QSoundEffect` (ligne ~50).

### **🎭 Animations (style Clippy)**
Pour ajouter des animations (ex: RADI qui bouge), modifie la méthode `show_balloon` dans `radi.py` :
```python
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve

# Dans RadiWindow.__init__()
self.animation = QPropertyAnimation(self, b"geometry")
self.animation.setDuration(500)
self.animation.setEasingCurve(QEasingCurve.Type.OutBounce)

# Dans show_balloon()
self.move(self.x(), self.y() + 200)  # Commence en bas
self.show()
self.animation.setStartValue(self.geometry())
self.animation.setEndValue(self.geometry().translated(0, -200))  # Monte
self.animation.start()
```

### **📊 Suivi des Conseils Lus**
Pour éviter de répéter les mêmes conseils, ajoute un système de logs dans `data/radi_logs.json` :
```python
import json
from datetime import datetime

def log_conseil(conseil_id):
    try:
        with open("data/radi_logs.json", "r") as f:
            logs = json.load(f)
    except FileNotFoundError:
        logs = []
    
    logs.append({
        "conseil_id": conseil_id,
        "date": datetime.now().isoformat(),
        "vue": True
    })
    
    with open("data/radi_logs.json", "w") as f:
        json.dump(logs, f, indent=2)
```

---

## 📦 **Créer un Exécutable (.exe)**

Pour déployer RADI **sans installer Python** sur chaque machine :

1. Installe **PyInstaller** :
   ```bash
   pip install pyinstaller
   ```

2. Génère l'exécutable (depuis le dossier `RADI/`) :
   ```bash
   pyinstaller --onefile --windowed --icon=assets/radi.ico --name RADI radi.py
   ```
   > **Options** :
   > - `--onefile` : Un seul fichier `.exe`.
   > - `--windowed` : Pas de console visible.
   > - `--icon=assets/radi.ico` : Icône personnalisée (à créer).

3. Récupère `RADI.exe` dans le dossier `dist/`.
4. Modifie `install.bat` pour pointer vers `RADI.exe` au lieu de `python.exe radi.py`.

---

## 🏫 **Déploiement en Masse (Réseau Scolaire)**

### **Méthode 1 : Script PowerShell**
Pour installer RADI sur **tous les PC d'un réseau Active Directory** :
```powershell
$computers = Get-ADComputer -Filter * | Select-Object -ExpandProperty Name
$source = "\\serveur\partage\RADI\"
$destination = "C:\Program Files\RADI\"

foreach ($computer in $computers) {
    # Copier les fichiers
    Copy-Item -Path $source -Destination "\$computer\$destination" -Recurse -Force
    
    # Exécuter l'installation en admin
    Invoke-Command -ComputerName $computer -ScriptBlock {
        Start-Process -FilePath "cmd.exe" -ArgumentList "/c C:\Program Files\RADI\install.bat" -Verb RunAs
    }
}
```

### **Méthode 2 : GPO (Stratégie de Groupe)**
1. Crée un **package MSI** avec [Inno Setup](https://jrsoftware.org/isinfo.php) ou [Advanced Installer](https://www.advancedinstaller.com/).
2. Déploie le package via **GPO** (Group Policy Object) dans Active Directory.

---

## 📝 **Idées de Conseils Éducatifs**

Voici une liste de conseils à inclure dans `conseils.json` :

### **🔐 Sécurité**
- "🔑 Utilise des mots de passe **uniques** pour chaque compte. Un gestionnaire de mots de passe peut t'aider !"
- "🚨 Méfie-toi des emails ou messages qui demandent tes informations personnelles, même s'ils semblent officiels."
- "🔒 Active la **double authentification** sur tes comptes importants (ex: email, jeux en ligne)."
- "📱 Ne te connecte pas à un Wi-Fi public sans protection (ex: VPN)."

### **👁️‍🗨️ Respect & Droit à l'Image**
- "📸 Avant de publier une photo de quelqu'un, **demande-lui son accord** !"
- "🗣️ Sur internet, soyez **bienveillants**. Un message peut blesser même s'il est écrit pour rire."
- "🚫 Le cyberharcèlement est **interdit par la loi**. Si tu en es victime ou témoin, parles-en à un adulte."

### **⏳ Temps d'Écran & Santé**
- "👀 Fais une pause de **20 secondes toutes les 20 minutes** pour reposer tes yeux (règle 20-20-20)."
- "💪 Bouge ! Passe au moins **1 heure par jour** sans écran pour ton corps et ton esprit."
- "🌙 Éteins tes écrans **1 heure avant de dormir** pour mieux t'endormir."

### **🌍 Écologie Numérique**
- "🗑️ Supprime les **fichiers inutiles** et vide ta corbeille pour libérer de l'espace."
- "💾 Préfère le **stockage local** (clé USB, disque dur) au cloud quand c'est possible."
- "📧 Nettoie régulièrement ta boîte mail : **1 email = ~10g de CO2/an** !"

### **🎮 Bonnes Pratiques**
- "🔍 Vérifie toujours l'**URL** d'un site avant de saisir tes identifiants (ex: `https://` + cadenas 🔒)."
- "📂 Sauvegarde tes **travaux importants** sur une clé USB ou un disque dur externe."
- "🛑 Ne télécharge pas de logiciels **crackés** : ils contiennent souvent des virus."

---

## 🐞 **Dépannage**

| **Problème**                     | **Solution**                                                                 |
|----------------------------------|------------------------------------------------------------------------------|
| RADI ne se lance pas au démarrage | Exécute `install.bat` **en admin**. Vérifie que le raccourci est dans `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\`. |
| Fenêtre qui ne s'affiche pas      | Vérifie que `PyQt6` est installé (`pip install PyQt6`).                  |
| Erreur "conseils.json introuvable" | Vérifie que le fichier `data/conseils.json` existe et est valide.         |
| Python n'est pas reconnu          | Ajoute Python au PATH ou utilise le chemin complet (`C:\Python39\python.exe`). |

---

## 📜 **Licence & Crédits**

- **Licence** : Ce projet est **libre d'utilisation** pour un usage éducatif non commercial.
- **Crédits** : Inspiré par Clippy (Microsoft), développé pour les écoles.
- **Auteur** : [Ton Nom / Établissement]

---

## 📬 **Contact & Contributions**

- **Bugs/Améliorations** : Ouvre une issue sur [ton dépôt Git] (si applicable).
- **Nouveaux conseils** : Propose-les via [formulaire/email].

---

*"Le numérique est un outil puissant. Apprenons à l'utiliser **avec sagesse** !"* 🌟
