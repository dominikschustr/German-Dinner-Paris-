# German Dinner Paris — Aufbau des Repos

    index.html          Startseite (Quelle)
    gastgeber.html      Unterseite (Quelle)
    tokens.css          Design Tokens — Farben, Typo, Spacing
    base.css            Reset, Basiselemente, Layout-Primitives
    components.css      alle Komponenten
    page.css            seitenspezifische Ergänzungen
    DESIGN-SYSTEM.md    die Analyse, aus der das System stammt
    NN_*.png            Originalbilder (unkomprimiert, nicht ausgeliefert)
    docs/               DAS IST DIE LIVE-SEITE (GitHub Pages liest hier)

## Ändern und neu ausspielen

Bearbeitet werden immer die Dateien im Wurzelverzeichnis, nie die in
`docs/` — die werden überschrieben. Danach:

    python3 build.py

Das kopiert HTML und CSS nach `docs/`, rechnet die Bildnamen auf die
optimierten Fassungen um (WebP bzw. JPEG) und erzeugt fehlende Bilder neu.

## Warum optimierte Bilder

Die Original-PNGs wiegen zusammen 13,5 MB. Als WebP mit Alpha bzw. JPEG
sind es 1,6 MB — 12 % davon, ohne sichtbaren Unterschied. Für eine Seite,
die auf jedem Bildschirm sechs bis sieben Bilder lädt, ist das der
Unterschied zwischen brauchbar und unbenutzbar im Mobilfunknetz.

Das Panorama `11_Paris` wird JPEG, weil es keinen Alphakanal braucht.
Alle freigestellten Objekte brauchen Alpha und werden WebP.

## Achtung: Nahtfarbe

`--color-horizon-sky` in `tokens.css` ist der Mittelwert der obersten
Bildzeile von `11_Paris`. Der Verlauf über dem Foto endet auf genau
diesem Wert, deshalb ist die Kante unsichtbar. Wird das Bild getauscht,
muss der Wert neu bestimmt werden:

    python3 -c "from PIL import Image; import numpy as np; \
      a=np.asarray(Image.open('11_Paris.png').convert('RGB')); \
      print('#%02X%02X%02X' % tuple(a[0].mean(axis=0).round().astype(int)))"
