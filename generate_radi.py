#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour générer une image de base pour RADI.
Exécute ce script pour créer automatiquement un fichier assets/radi.png
avec un design simple de robot.

Utilisation :
    python generate_radi.py

Prérequis :
    pip install Pillow
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path


def generer_image_robot(couleur_principal=(50, 150, 250), couleur_secondaire=(200, 200, 200)):
    """Génère une image de robot simple pour RADI."""
    # Créer une image 150x150 avec fond transparent
    taille = (150, 150)
    img = Image.new('RGBA', taille, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Coordonnées
    center_x, center_y = 75, 75

    # Tête (cercle)
    draw.ellipse((center_x - 45, center_y - 40, center_x + 45, center_y + 10), 
                fill=(*couleur_principal, 255), outline='black', width=2)

    # Yeux (grands)
    draw.ellipse((center_x - 30, center_y - 25, center_x - 10, center_y - 5), 
                fill='white', outline='black', width=1)
    draw.ellipse((center_x + 10, center_y - 25, center_x + 30, center_y - 5), 
                fill='white', outline='black', width=1)

    # Pupilles
    draw.ellipse((center_x - 25, center_y - 20, center_x - 15, center_y - 10), 
                fill='black')
    draw.ellipse((center_x + 15, center_y - 20, center_x + 25, center_y - 10), 
                fill='black')

    # Reflets dans les yeux (petits cercles blancs)
    draw.ellipse((center_x - 22, center_y - 18, center_x - 18, center_y - 14), 
                fill='white')
    draw.ellipse((center_x + 18, center_y - 18, center_x + 22, center_y - 14), 
                fill='white')

    # Bouche (sourire)
    draw.arc((center_x - 20, center_y - 5, center_x + 20, center_y + 15), 
             0, 180, fill='black', width=2)

    # Corps (rectangle)
    draw.rectangle((center_x - 35, center_y + 10, center_x + 35, center_y + 60), 
                   fill=(*couleur_principal, 255), outline='black', width=2)

    # Bras gauche
    draw.rectangle((center_x - 55, center_y + 20, center_x - 35, center_y + 35), 
                   fill=(*couleur_principal, 255), outline='black', width=1)
    # Main gauche (cercle)
    draw.ellipse((center_x - 58, center_y + 30, center_x - 52, center_y + 36), 
                fill=(*couleur_secondaire, 255))

    # Bras droit
    draw.rectangle((center_x + 35, center_y + 20, center_x + 55, center_y + 35), 
                   fill=(*couleur_principal, 255), outline='black', width=1)
    # Main droite (cercle)
    draw.ellipse((center_x + 52, center_y + 30, center_x + 58, center_y + 36), 
                fill=(*couleur_secondaire, 255))

    # Jambes
    draw.rectangle((center_x - 25, center_y + 60, center_x - 10, center_y + 90), 
                   fill=(*couleur_principal, 255), outline='black', width=1)
    draw.rectangle((center_x + 10, center_y + 60, center_x + 25, center_y + 90), 
                   fill=(*couleur_principal, 255), outline='black', width=1)

    # Pieds
    draw.rectangle((center_x - 28, center_y + 90, center_x - 7, center_y + 95), 
                   fill=(*couleur_secondaire, 255), outline='black', width=1)
    draw.rectangle((center_x + 7, center_y + 90, center_x + 28, center_y + 95), 
                   fill=(*couleur_secondaire, 255), outline='black', width=1)

    # Antenne (optionnelle)
    draw.line((center_x + 10, center_y - 50, center_x + 10, center_y - 35), 
              fill=(*couleur_secondaire, 255), width=2)
    draw.ellipse((center_x + 7, center_y - 53, center_x + 13, center_y - 47), 
                fill=(*couleur_principal, 255), outline='black', width=1)

    return img


def generer_image_hibou():
    """Génère une image de hibou pour RADI."""
    taille = (150, 150)
    img = Image.new('RGBA', taille, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    center_x, center_y = 75, 75

    # Corps (ovale)
    draw.ellipse((center_x - 40, center_y - 20, center_x + 40, center_y + 60), 
                fill=(139, 69, 19, 255), outline='black', width=2)

    # Tête (cercle)
    draw.ellipse((center_x - 35, center_y - 50, center_x + 35, center_y - 5), 
                fill=(139, 69, 19, 255), outline='black', width=2)

    # Oreilles
    draw.polygon([(center_x - 30, center_y - 45), (center_x - 20, center_y - 60), (center_x - 10, center_y - 45)], 
                 fill=(139, 69, 19, 255), outline='black')
    draw.polygon([(center_x + 30, center_y - 45), (center_x + 20, center_y - 60), (center_x + 10, center_y - 45)], 
                 fill=(139, 69, 19, 255), outline='black')

    # Yeux (grands cercles)
    draw.ellipse((center_x - 25, center_y - 35, center_x - 5, center_y - 15), 
                fill='white', outline='black', width=2)
    draw.ellipse((center_x + 5, center_y - 35, center_x + 25, center_y - 15), 
                fill='white', outline='black', width=2)

    # Pupilles (noires)
    draw.ellipse((center_x - 20, center_y - 30, center_x - 10, center_y - 20), 
                fill='black')
    draw.ellipse((center_x + 10, center_y - 30, center_x + 20, center_y - 20), 
                fill='black')

    # Bec (triangle)
    draw.polygon([(center_x - 5, center_y - 5), (center_x + 5, center_y - 5), (center_x, center_y + 5)], 
                 fill=(255, 215, 0, 255), outline='black')

    # Plumes sur le ventre
    draw.ellipse((center_x - 25, center_y - 5, center_x + 25, center_y + 30), 
                 fill=(205, 133, 63, 255), outline='black', width=1)

    # Ailes (simplifiées)
    draw.ellipse((center_x - 55, center_y - 10, center_x - 25, center_y + 40), 
                 fill=(139, 69, 19, 200), outline='black', width=1)
    draw.ellipse((center_x + 25, center_y - 10, center_x + 55, center_y + 40), 
                 fill=(139, 69, 19, 200), outline='black', width=1)

    return img


def generer_image_coeur():
    """Génère une image de cœur pour RADI (style bienveillant)."""
    taille = (150, 150)
    img = Image.new('RGBA', taille, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    center_x, center_y = 75, 75

    # Cœur (formé de deux cercles et un triangle)
    draw.ellipse((center_x - 30, center_y - 20, center_x + 10, center_y + 30), 
                fill=(255, 50, 100, 255), outline='black', width=2)
    draw.ellipse((center_x + 10, center_y - 20, center_x + 50, center_y + 30), 
                fill=(255, 50, 100, 255), outline='black', width=2)
    draw.polygon([(center_x - 10, center_y + 30), (center_x + 10, center_y + 30), (center_x, center_y + 50)], 
                 fill=(255, 50, 100, 255), outline='black', width=2)

    # Yeux
    draw.ellipse((center_x - 20, center_y - 10, center_x - 5, center_y + 5), 
                fill='white', outline='black', width=1)
    draw.ellipse((center_x + 5, center_y - 10, center_x + 20, center_y + 5), 
                fill='white', outline='black', width=1)

    # Pupilles
    draw.ellipse((center_x - 18, center_y - 8, center_x - 8, center_y), 
                fill='black')
    draw.ellipse((center_x + 8, center_y - 8, center_x + 18, center_y), 
                fill='black')

    # Bouche (sourire)
    draw.arc((center_x - 15, center_y + 10, center_x + 15, center_y + 30), 
             0, 180, fill='black', width=2)

    return img


def main():
    """Point d'entrée du script."""
    print("=" * 70)
    print("Générateur d'image pour RADI")
    print("=" * 70)
    print()
    print("Choisis un design pour RADI :")
    print("  1. 🤖 Robot (design par défaut)")
    print("  2. 🦉 Hibou (sagesse)")
    print("  3. ❤️ Cœur (bienveillance)")
    print()

    choix = input("Entrez le numéro de votre choix (1-3) [1] : ").strip()
    if not choix:
        choix = "1"

    # Créer le dossier assets s'il n'existe pas
    assets_dir = Path(__file__).parent / "assets"
    assets_dir.mkdir(exist_ok=True)

    image_path = assets_dir / "radi.png"

    try:
        if choix == "1":
            print("\n✅ Génération de l'image ROBOT...")
            img = generer_image_robot()
        elif choix == "2":
            print("\n✅ Génération de l'image HIBOU...")
            img = generer_image_hibou()
        elif choix == "3":
            print("\n✅ Génération de l'image CŒUR...")
            img = generer_image_coeur()
        else:
            print("\n⚠️  Choix invalide. Utilisation du design par défaut (Robot).")
            img = generer_image_robot()

        img.save(image_path)
        print(f"✅ Image sauvegardée dans : {image_path}")
        print(f"\nTu peux maintenant lancer RADI avec : python radi.py")

    except ImportError as e:
        print(f"\n❌ Erreur : {e}")
        print("\nLe module Pillow est requis. Installez-le avec :")
        print("    pip install Pillow")
    except Exception as e:
        print(f"\n❌ Erreur inattendue : {e}")


if __name__ == "__main__":
    main()
