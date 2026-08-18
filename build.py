#!/usr/bin/env python3
"""Baut den Auslieferungsordner docs/ aus den Quellen im Wurzelverzeichnis.

Zwei Schritte:
  1. Bilder optimieren, falls die optimierte Fassung fehlt oder aelter ist
     als das Original. Cutouts brauchen Alpha und werden WebP, das
     Panorama hat keins und wird JPEG.
  2. HTML und CSS kopieren und die Bildnamen im HTML umschreiben.

Die Originale werden nie veraendert.
"""
import os
import shutil
from PIL import Image

OUT = "docs"
QUALITAET = 88

# Original -> Zielformat. Alles mit Alpha muss WebP werden.
CUTOUTS = [
    "01_Eiffelturm.png",
    "02_Brandenburgertor_cut.png",
    "03_Arc_cut.png",
    "04_Baguette_cut.png",
    "05_Currywurst_cut.png",
    "09_SacreCoeur_cut.png",
]
PHOTOS = ["11_Paris.png"]

QUELLEN = ["index.html", "gastgeber.html",
           "tokens.css", "base.css", "components.css", "page.css"]


def veraltet(src, dst):
    return not os.path.exists(dst) or os.path.getmtime(src) > os.path.getmtime(dst)


def main():
    os.makedirs(OUT, exist_ok=True)
    ersetzungen = {}

    for f in CUTOUTS:
        ziel = f.replace(".png", ".webp")
        pfad = os.path.join(OUT, ziel)
        if veraltet(f, pfad):
            Image.open(f).convert("RGBA").save(
                pfad, "WEBP", quality=QUALITAET, method=6)
            print(f"  neu  {ziel}")
        ersetzungen[f] = ziel

    for f in PHOTOS:
        ziel = f.replace(".png", ".jpg")
        pfad = os.path.join(OUT, ziel)
        if veraltet(f, pfad):
            Image.open(f).convert("RGB").save(
                pfad, "JPEG", quality=QUALITAET, optimize=True, progressive=True)
            print(f"  neu  {ziel}")
        ersetzungen[f] = ziel

    for f in QUELLEN:
        ziel = os.path.join(OUT, f)
        if f.endswith(".html"):
            s = open(f, encoding="utf-8").read()
            for alt, neu in ersetzungen.items():
                s = s.replace(alt, neu)
            open(ziel, "w", encoding="utf-8").write(s)
        else:
            shutil.copy2(f, ziel)

    gewicht = sum(os.path.getsize(os.path.join(OUT, x))
                  for x in os.listdir(OUT))
    print(f"\n{OUT}/ fertig — {gewicht/1048576:.2f} MB")


if __name__ == "__main__":
    main()
