# Design System — abgeleitet von lafamiglia.vc

**Analysebasis:** Live-DOM (Computed Styles) + vollständiges Stylesheet
`la-famiglia-a8686e.webflow.7e5d4f5bf.css` (55 KB) + Inline-Embeds der Seiten `/` und `/founders`.
Gemessen bei Viewport 1440×900, 600×900 und 375×812.
Technischer Unterbau der Referenz: **Webflow**. Alle Zahlen unten sind gemessen, nicht geschätzt —
Ausnahmen sind explizit als *[geschätzt]* markiert.

---

## 1. Executive Summary des Designs

Das Design ist ein **Anti-Grid-Poster-Layout**: eine einzige, extrem breite Textspalte, in die
überdimensionale Display-Headlines gesetzt werden, die fast immer die volle Contentbreite ausfüllen.
Der gesamte Rest des Layouts besteht aus Leerraum und freigestellten Bildobjekten, die **absolut
positioniert über die Typografie gelegt** werden.

Fünf Mechaniken tragen den gesamten Look:

1. **Ein einziger fluider Basiswert.** `body { font-size: 1vw }`. Jede Größe im Design — Schrift,
   Padding, Abstände, Radien, Bildbreiten — ist ein `em`-Vielfaches dieses Werts. Über 1440 px
   friert er bei 14.4 px ein. Das Layout skaliert dadurch als *ein starres Poster*, nicht als
   fließendes Web-Layout.
2. **Doppelt gesetzte Headlines.** Jede große Überschrift existiert zweimal im DOM: einmal als
   gefüllter schwarzer Text, einmal als Outline (`-webkit-text-stroke: 1px`, transparente Füllung),
   absolut deckungsgleich darüber. Zwischen beiden liegt ein freigestelltes Bild. Das erzeugt den
   Signature-Effekt: das Bild verdeckt die gefüllte Schrift, die Outline bleibt darüber sichtbar.
3. **Vier Farben, keine Grautöne dazwischen.** Aperol-Orange, Hellgrau, Schwarz, Weiß. Sektionen
   sind vollflächige Farbblöcke; Kontrast entsteht durch Sektionswechsel, nie durch Schattierung.
4. **Null Transitions auf Desktop.** Alle Hover-Zustände sind harte Farbinversionen mit
   `transition-duration: 0s`. Die einzige Dauer-Animation ist ein 60-Sekunden-Marquee.
5. **Keine Schatten, keine Verläufe, keine Blur-Effekte.** Flächen werden ausschließlich durch
   `1px solid black` und großzügige Radien getrennt.

Die visuelle Wirkung: laut, plakatartig, italienisch-brutalistisch — aber technisch minimalistisch
umgesetzt (das gesamte Custom-CSS sind ~175 Regeln).

---

## 2. Design-System-Übersicht

| Ebene | Prinzip |
|---|---|
| Skalierungsmodell | Ein Basisunit `u`, alles in `em`-Vielfachen davon |
| Grid | Kein Spaltengrid. Eine 1280 px Contentspalte, Elemente über `max-width` + `margin-left` positioniert |
| Farbmodell | 4 Kernfarben, semantisch über Sektionshintergrund gesteuert |
| Typo-Modell | 2 Familien, 2 Rollen: Display (riesig) und UI/Body (klein). Nichts dazwischen |
| Flächen-Modell | Weiße Karten mit 1px schwarzem Rahmen auf farbigem Grund |
| Bewegung | Statisch, außer einem Endlos-Marquee |
| Breakpoint-Modell | 1 realer Layout-Breakpoint (479 px). Alles darüber ist ein einziges fluid skaliertes Layout |

### 2.1 Der Basisunit — die zentrale Regel

```css
/* Original */
body { font-size: 1vw; }
@media (min-width: 1440px) { body { font-size: 0.9em; } }  /* = 14.4px, eingefroren */
```

| Viewport | Basisunit `u` |
|---|---|
| ≥ 1440 px | **14.4 px** (fix) |
| 480 – 1439 px | **1 vw** (fluid) |
| ≤ 479 px | **1 vw** (fluid, aber eigener Multiplikatorsatz) |

Äquivalent: `--u: min(1vw, 14.4px)`.

> **Verifizierter Mangel der Referenz — bitte nicht übernehmen.**
> Weil zwischen 480 px und 991 px kein einziger Override existiert, skaliert auch der Fließtext mit
> `1vw`. Gemessen bei Viewport 600 px: Body-Copy **6.66 px**, Navigationslinks **6.66 px**,
> `.headlinesmall` **13.32 px**. Der Bereich 480–767 px ist faktisch unlesbar. Abschnitt 10.4
> enthält den korrigierten Token.

---

## 3. Layout & Grid

### 3.1 Container

```css
.container {
  max-width: 100em;        /* 1440px @ u=14.4 */
  margin-inline: auto;
  padding-inline: 5.56em;  /* 80.06px */
}
```

| Wert | @1440 px | in `u` |
|---|---|---|
| Container max-width | 1440 px | 100 u |
| Seitenpadding | 80 px | 5.56 u |
| **Nutzbare Contentbreite** | **1280 px** | 88.9 u |

Die Contentbreite von 1280 px ist die Referenzachse des gesamten Designs — Headlines sind exakt so
breit, das 50/50-Layout teilt exakt hier.

### 3.2 Es gibt kein Spaltengrid

Die Referenz nutzt **kein CSS-Grid und kein Flex-Grid für Content**. Positionierung erfolgt über
drei Muster:

**Muster A — Volle Breite (Headlines)**
Headline füllt die 1280 px. Immer.

**Muster B — Textblock mit Offset**
```css
.pwrapper        { max-width: 36.11em; }  /* 520px = 40.6% der Contentbreite */
.pwrapper.right  { margin-left: 44.44em; } /* 640px = exakt 50% */
.pwrapper.wide   { max-width: 60em; }      /* 864px = 67.5% */
```
Textspalten sind nie zentriert und nie volle Breite. Sie sitzen entweder linksbündig bei 0 oder
starten exakt bei 50 % der Contentbreite. Der Whitespace daneben ist der Bildbereich.

**Muster C — 50/50 Split mit Sticky-Visual** (`/founders`)
```css
._5050wrapper    { display: flex; align-items: flex-start; }
.foundersvisual  { width: 50%; position: sticky; top: 0; padding-top: 6em; }  /* 640px */
.founderscollection { width: 50%; padding-top: 3.5em; }                       /* 640px */
```
Kein Gap. Die beiden Hälften stoßen aneinander; visuelle Trennung entsteht durch den Whitespace
innerhalb der Elemente.

### 3.3 Vertikale Rhythmik — Spacer-Divs statt Margins

Die Referenz verwendet **keine vertikalen Margins zwischen Sektionsteilen**. Stattdessen leere
`div`s mit fester Höhe. Das ist unüblich, aber der Grund für die konsistente Rhythmik.

| Klasse | `em` | @1440 px | @375 px (Mobile-Override) |
|---|---|---|---|
| `.spacertiny` | 2 / 4 | 28.8 px | 15 px |
| `.spacersmall` | 6 / 10 | 86.4 px | 37.5 px |
| `.spacermedium` | 9 / 25 | 129.6 px | 93.75 px |
| `.spacerbig` | 15 / 30 | 216 px | 112.5 px |

Beachte die Inversion: auf Mobile werden `tiny`/`small` **kleiner** relativ, `medium`/`big` deutlich
**größer** relativ — die Sektionsabstände wachsen, die Detailabstände schrumpfen.

### 3.4 Gemessener Sektionsaufbau der Startseite (Viewport 1440 px)

| # | Sektion | Höhe | Hintergrund | Inhalt |
|---|---|---|---|---|
| 1 | `.section.aperol` | 959 px | `#ff4f2c` | Header, Hero-H1 (doppelt), Statue + Sonnenbrille, Intro-Paragraph |
| 2 | `.section.grigio.overflowhidden` | 1726 px | `#dfdfdf` | H2 (doppelt), zwei Hand-Cutouts, Textblock rechts |
| 3 | `.section.black` | 1926 px | `#000` | Zentrierte weiße H2, 3× Marquee, CTA-Button |
| 4 | `.section` | 1708 px | transparent + Foto | H2, Textblock rechts, Full-Bleed-Foto unten |
| 5 | `.section.grigio` | 154 px | `#dfdfdf` | Footer |
| | **Gesamt** | **6472 px** | | 5 Sektionen für ~120 Wörter Text |

Das Verhältnis ist die eigentliche Designaussage: **~6470 px Seitenhöhe für 4 Überschriften und
3 Absätze.** Whitespace ist hier nicht Beiwerk, sondern das Hauptmaterial.

Gemessene Elementpositionen (Dokumentkoordinaten, 1440 px):

| Element | left | top | Breite × Höhe |
|---|---|---|---|
| `img.logo` | 80 | 14 | 146 × 39 |
| `h1.heading` (beide) | 80 | 140 | 1280 × 415 |
| `img.glasses` | 658 | 219 | 393 × 135 |
| `img.statue` | 642 | 319 | 346 × 456 |
| `p.paragraph` | 80 | 641 | 520 × 102 |
| `h2.heading` (beide) | 80 | 1175 | 1280 × 680 |
| `img.handright` | 678 | 1235 | 867 × 319 |
| `img.handleft` | −70 | 1292 | 578 × 287 |
| Textblock rechts | 720 | 1985 | 520 × 474 |
| `.marquee-wrapper` ×3 | 0 | 3484 / 3715 / 3945 | 1440 × 230 |
| CTA-Button | 580 | 4305 | 279 × 90 |
| `.footerwrapper` | 80 | 6405 | 1280 × 67 |

`img.handleft` startet bei `left: −70` — Bilder dürfen bewusst über den Viewportrand hinauslaufen,
abgefangen durch `overflow: hidden` auf der Sektion.

### 3.5 Verhältnis Text / Bild / Whitespace *[geschätzt, aus Flächenmessung]*

Bezogen auf die Startseite bei 1440 px:

- **Typografie (inkl. Display):** ca. 22 % der Fläche
- **Bilder / Medien:** ca. 13 %
- **Leerfläche (reiner Hintergrund):** ca. 65 %

Die Schätzung basiert auf den Bounding-Boxen der Tabelle in 3.4 gegen die Gesamtfläche
1440 × 6472 px. Für neue Seiten ist die praktische Regel wichtiger: **jede Sektion beginnt und endet
mit einem `spacerbig` (216 px)**, und zwischen Headline und zugehörigem Text liegen mindestens
`spacermedium` (130 px).

---

## 4. Typografie

### 4.1 Schriftfamilien

| Rolle | Original | Gewichte | Freie Alternative |
|---|---|---|---|
| Display | **MD Nichrome** (Mass-Driver) | 300 Light, 400 Regular | *Anton*, *Archivo Black*, *Bebas Neue*; am nächsten: **Anton** (kommerziell: MD Nichrome, Monument Extended, PP Right Grotesk) |
| UI / Body | **Helvetica Neue LT Pro** | 400 Roman, 500 Medium, 700 Bold | **Inter**, *Helvetica Now*, *Neue Haas Grotesk*; System-Fallback: `-apple-system, "Helvetica Neue", Arial` |

MD Nichrome ist eine hoch-kondensierte Display-Grotesk mit sehr geringer Punzenweite. Wird
ausschließlich in `text-transform: uppercase` und bei Größen ≥ 60 px eingesetzt — nie für UI.

Helvetica Neue trägt **alles andere**: Navigation, Buttons, Fließtext, Footer. Es gibt keine dritte
Familie.

> **Bug in der Referenz:** `.navtrigger` deklariert `font-family: Helveticaneueltstd bd` — für diese
> Familie existiert kein `@font-face`. Der mobile Menü-Trigger fällt auf die Systemschrift zurück.
> Nicht übernehmen.

### 4.2 Typografie-Skala

Alle Größen als `em`-Vielfache des Basisunits `u`. Spalte „@1440“ = Rendergröße bei eingefrorenem
`u = 14.4 px`.

| Token | Klasse | Größe (`u`) | @1440 px | Weight | Line-Height | Letter-Spacing | Transform |
|---|---|---|---|---|---|---|---|
| `display-2xl` | `.heading` | 17.5 | **252 px** | 400 | 0.9 → 226.8 px | −0.01vw (−0.14 px) | uppercase |
| `display-xl` | `.heading.half` | 16 | **230.4 px** | 400 | 0.9 → 207.4 px | −0.01vw | uppercase |
| `display-ticker` | `.tickerlink` | 17.5**vw** | 252 px | 300 | 0.9 | −0.01vw | uppercase |
| `display-name` | `.membername` | 17.5 | 252 px | 400 | 0.9 | −0.01vw | — |
| `heading-sm` | `.headlinesmall` | 2.22 | **31.97 px** | 500 | 1.0 | −0.01vw | — |
| `body-lg` | `p`, `.paragraph` | 1.81 | **26.06 px** | 400 | 1.3 → 33.9 px | −0.02em (−0.52 px) | — |
| `button` | `.button` | 1.67 | **24.05 px** | 700 | 1.3 → 31.3 px | −0.01vw | — |
| `nav` | `.navlink` | 1.11 | **15.98 px** | 700 | 1.3 → 20.8 px | −0.02em (−0.32 px) | — |
| `caption` | `.psmall` | 1.11 | **15.98 px** | 400 | 1.5 → 24 px | −0.01vw | — |
| `link-sm` | `.link` | 1.0 | **14.4 px** | 700 | 1.3 | −0.01vw | — |

**Die Skala hat ein bewusstes Loch.** Zwischen `heading-sm` (32 px) und `display-2xl` (252 px)
existiert nichts. Es gibt keine H3, keine H4, keine Zwischenüberschrift. Wer eine Hierarchiestufe
braucht, nimmt `heading-sm` oder Fettung — **nicht** eine erfundene Zwischengröße. Das ist der
wichtigste Erhaltungssatz der Typografie.

Verhältnis Headline zu Fließtext: **252 / 26.06 ≈ 9.7 : 1**. Zum Vergleich liegt ein
konventionelles Corporate-Design bei 2.5–4 : 1.

### 4.3 Mobile-Skala (≤ 479 px)

Eigener Multiplikatorsatz auf demselben `u = 1vw`. Spalte „@375“ ist die Rendergröße.

| Token | Größe (`u`) | @375 px | Änderung ggü. Desktop-Multiplikator |
|---|---|---|---|
| `display-xl` (H1) | 16 | **60 px** | unverändert (`.heading.half` ist spezifischer) |
| `display-2xl` (H2) | 19.7 | **73.9 px** | 17.5 → 19.7 |
| `heading-sm` | 4.62 | 17.33 px | 2.22 → 4.62 |
| `body-lg` | 4.62 | 17.33 px | 1.81 → 4.62 |
| `button` | 4.0 | 15 px | 1.67 → 4.0 |
| `nav` | 4.0 | 15 px | 1.11 → 4.0 |
| `caption` | 3.59 | 13.46 px | 1.11 → 3.59 |

Die Display-Größe schrumpft von 252 px auf 74 px (Faktor 0.29), der Fließtext von 26 px auf 17.3 px
(Faktor 0.67). **Das Kontrastverhältnis fällt von 9.7:1 auf 4.3:1** — Mobile ist deutlich zahmer als
Desktop. Das ist beabsichtigt und sollte übernommen werden.

### 4.4 Textfarben

| Kontext | Farbe |
|---|---|
| `p`, Headlines, Nav, Captions | `#000` |
| `body` Default (praktisch ungenutzt) | `#333` |
| Auf schwarzer Sektion | `#fff` |
| Links (`a`) | `#ff4f2c` |
| Button gefüllt | `#fffcfc` |
| `.grid-card` | `rgba(255,255,255,0.19)` |
| Dropdown-Trigger offen | `rgba(0,0,0,0.36)` |

### 4.5 Font-Rendering

```css
body { -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }
```
Bei 252 px Schriftgrößen sichtbar relevant — übernehmen.

---

## 5. Farbpalette

### 5.1 Kernpalette (4 Farben, als CSS-Variablen im Original)

| Rolle | Name | HEX | RGB | HSL |
|---|---|---|---|---|
| Primary / Accent | `--aperol` | `#FF4F2C` | `rgb(255, 79, 44)` | `hsl(10, 100%, 59%)` |
| Background | `--grigio` | `#DFDFDF` | `rgb(223, 223, 223)` | `hsl(0, 0%, 87%)` |
| Text / Border / Surface | `--black` | `#000000` | `rgb(0, 0, 0)` | `hsl(0, 0%, 0%)` |
| Surface | `--white` | `#FFFFFF` | `rgb(255, 255, 255)` | `hsl(0, 0%, 100%)` |

### 5.2 Abgeleitete Werte (im CSS vorhanden, nicht als Variable)

| Zweck | HEX | RGB | HSL |
|---|---|---|---|
| Body-Default-Text | `#333333` | `rgb(51,51,51)` | `hsl(0,0%,20%)` |
| Text auf gefülltem Button | `#FFFCFC` | `rgb(255,252,252)` | `hsl(0,100%,99%)` |
| Bild-Platzhalter hinter Full-Bleed-Foto | `#B1C4DE` | `rgb(177,196,222)` | `hsl(215,41%,78%)` |
| Grid-Card-Text | `rgba(255,255,255,.19)` | — | — |
| Grid-Card-Border | `rgba(238,237,242,.19)` | — | — |
| Dropdown-Trigger offen | `rgba(0,0,0,.36)` | — | — |

### 5.3 Einsatzregeln — wo welche Farbe liegt

**Aperol (`#FF4F2C`)** hat genau zwei Aufgaben:
1. **Hero-Sektion vollflächig.** Nur die erste Sektion der Startseite. Nirgends sonst als Fläche.
2. **Linkfarbe.** Alle `<a>`-Elemente im Fließtext und Footer.
3. **Hover des Marquee-Tickers.** Der weiße Outline-Text wird zu gefülltem Aperol.

Aperol wird **nie** als Buttonhintergrund, nie als Kartenhintergrund und nie als Textfarbe im
Fließtext verwendet. Es ist ein Flächen- und Signalton, kein UI-Ton.

**Grigio (`#DFDFDF`)** ist der eigentliche Grundton: Body-Hintergrund, Sektion 2, Footer-Sektion,
und alle Unterseiten (`/founders` startet direkt in Grigio).

**Schwarz** ist Textfarbe, Rahmenfarbe *und* Sektionsfläche. Die schwarze Sektion ist der visuelle
Höhepunkt der Seite (Portfolio-Marquee).

**Weiß** ist ausschließlich Surface: Navigationspille, Karten, Akkordeon-Elemente. Nie eine
Sektionsfläche.

### 5.4 Semantische Rollen für das neue System

Die Referenz kennt **kein Success/Warning/Error** — es gibt keine Formulare, keine Statusanzeigen,
keine Validierung im gesamten CSS. Für das neue System sind folgende Ergänzungen nötig; sie sind
**nicht aus der Referenz abgeleitet**, sondern so gewählt, dass sie sich in die Palette einfügen
(gleiche Sättigung, gleiche Helligkeitslage wie Aperol):

| Rolle | Vorschlag | HSL | Begründung |
|---|---|---|---|
| `success` | `#1F9E5B` | `hsl(150, 67%, 37%)` | dunkler als Aperol, damit weißer Text passt |
| `warning` | `#E5A100` | `hsl(42, 100%, 45%)` | gleiche Sättigung wie Aperol, andere Hue-Familie |
| `error` | `#C4231A` | `hsl(3, 76%, 43%)` | Aperol-verwandt, aber klar dunkler → verwechselungsfrei |

Regel: **Der Accent-Ton darf nicht gleichzeitig Error-Ton sein.** Da Aperol im Orange-Rot-Bereich
liegt, muss Error deutlich abgedunkelt und entsättigt werden.

### 5.5 Kontrastwerte (berechnet, WCAG 2.1)

| Kombination | Ratio | Bewertung |
|---|---|---|
| Schwarz auf Aperol | **6.41 : 1** | AA für Fließtext ✓, AAA nur für Große Schrift |
| Schwarz auf Grigio | **15.8 : 1** | AAA ✓ |
| Weiß auf Schwarz | **21 : 1** | AAA ✓ |
| Weiß auf Aperol | **3.28 : 1** | ✗ für Fließtext, nur für ≥24 px Bold |
| Aperol auf Grigio (Links) | **2.9 : 1** | ✗ — Links im Footer sind grenzwertig |

**Handlungsempfehlung für das neue System:** Weiß nie auf dem Accent-Ton für Fließtext. Für Links
auf hellem Grund den Accent um ca. 12 % abdunkeln (`hsl(10, 100%, 47%)` → 4.6:1) oder Links
zusätzlich unterstreichen.

---

## 6. Spacing-System

Alle Werte in `u`. Die Referenz hat kein benanntes Spacing-System — die folgende Skala ist aus den
tatsächlich verwendeten Werten rekonstruiert und deckt jede vorkommende Größe ab.

| Token | `u` | @1440 px | Fundstelle im Original |
|---|---|---|---|
| `space-2xs` | 0.5 | 7.2 px | Button-Zeilenabstand mobil |
| `space-xs` | 1 | 14.4 px | Header-Padding, Card-Gutter, Logo-Offset |
| `space-sm` | 2 | 28.8 px | Card-Innenpadding, `spacertiny`, `.link`-Abstand |
| `space-md` | 2.5 | 36 px | Akkordeon-Padding oben, Plus-Icon-Box |
| `space-lg` | 3.5 | 50.4 px | Collection-Padding oben |
| `space-xl` | 5.56 | 80 px | **Container-Seitenpadding** |
| `space-2xl` | 6 | 86.4 px | `spacersmall`, Sticky-Visual-Padding |
| `space-3xl` | 9 | 129.6 px | `spacermedium` |
| `space-4xl` | 15 | 216 px | `spacerbig` — Sektionsabstand |

### 6.1 Vertikale Rhythmus-Regeln (aus dem DOM abgeleitet)

1. Jede Sektion öffnet mit `space-4xl` (216 px) und schließt mit `space-4xl`.
   → Zwischen zwei Sektionen liegen effektiv **432 px** Leerraum.
2. Zwischen Header und erster Headline: `space-2xl` (86.4 px).
3. Zwischen Headline und zugehörigem Textblock: `space-3xl` (129.6 px).
4. Zwischen Textblock und Button: `space-2xl` (86.4 px).
5. Innerhalb von Karten: `space-sm` (28.8 px) allseitig.

### 6.2 Horizontale Regeln

- Contentkante immer bei `space-xl` (80 px) vom Viewportrand.
- Karten-Gutter: `2 × space-xs` = 28.8 px (über negative Collection-Margins gelöst).
- Textspalten starten entweder bei 0 oder bei exakt 50 % der Contentbreite (640 px).

---

## 7. Komponenten

### 7.1 Header

```
.headerwrapper  display:flex; justify-content:space-between; align-items:stretch;
                padding-top: 1em (14.4px); position: relative;
```
Nicht sticky. Nur das Logo scrollt mit; die Navigationspille ist separat `position: fixed`.

| Element | Wert @1440 |
|---|---|
| Logo (SVG) | 146 × 39 px, `width: 10.14em`, `padding-top: 1em` |
| Logo-Position | left 80 px, top 14 px |

### 7.2 Navigation (Desktop)

Eine **freischwebende Pille oben rechts** — keine Full-Width-Leiste.

```css
.navwrapper {
  position: fixed;  z-index: 900;
  background: #fff;  border: 1px solid #000;
  border-radius: 1.39em;      /* 20.02px */
  display: flex; align-items: center;
  overflow: hidden;           /* schneidet Hover-Flächen am Radius ab */
}
```

| Eigenschaft | Wert @1440 |
|---|---|
| Position | fixed, top 14.4 px, right 80 px |
| Größe | 182 × 74 px |
| Radius | 20.02 px |
| Border | 1 px solid #000 |
| Hintergrund | #fff |
| z-index | 900 |

```css
.navlink {
  font: 700 1.11em/1.3 "Helvetica Neue";   /* 15.98px */
  letter-spacing: -.02em;
  padding: 1.7em .9em 1.5em;               /* 27.2 / 14.4 / 24 px — em der eigenen Größe! */
  color: #000;  display: block;
}
.navlink.first { padding-left: 1.5em; }    /* 24px */
.navlink.last  { padding-right: 1.2em; }   /* 19.2px */
.navlink:hover { background: #000; color: #fff; opacity: 1; }
```

**Wichtig:** Die `em`-Paddings in `.navlink` beziehen sich auf die **eigene** `font-size` (15.98 px),
weil `font-size` in derselben Regel gesetzt ist. Nicht auf `u`. Beim Nachbau leicht falsch zu machen.

Hover: harter Umschlag auf schwarze Fläche, **ohne Transition**. Weil der Container
`overflow: hidden` und Radius hat, wird die schwarze Fläche an der Pillenkante sauber beschnitten.
`opacity: 1` überschreibt die globale `a:hover { opacity: .5 }`-Regel.

Kein Focus-State im gesamten Stylesheet. **Für das neue System zwingend zu ergänzen** (siehe 14.4).

### 7.3 Navigation (Mobile, ≤ 479 px)

Wechselt von oben-rechts nach **unten-zentriert** — eine Bottom-Sheet-Pille.

```css
.navwrapper {
  position: fixed;  inset: auto 0% 0%;      /* bottom 0, horizontal 0 */
  flex-direction: column;  justify-content: flex-end;
  max-width: 45em;         /* 168.75px @375 */
  height: auto;
  margin: 0 auto 3em;      /* 11.25px Abstand zum unteren Rand */
  border-radius: 3em;      /* 11.25px */
  z-index: 100;
}
.navlink, .navtrigger { font-size: 4em; width: 100%; text-align: center; padding-inline: 0; }
.navtrigger { display: block; padding: 1.4em 0 1.2em; }
.navtrigger.w--open { color: rgba(0,0,0,.36); }
```

Die Links sind zunächst ausgeblendet (`.dropdown-list-2 { display: none }`) und klappen über dem
Trigger auf (`order: -1`). Öffnungsverzögerung `data-delay="300"`, kein Hover-Trigger
(`data-hover="false"`).

### 7.4 Hero Section

Der Signature-Aufbau. Struktur exakt:

```html
<div class="section aperol">
  <div class="container">
    <div class="headerwrapper">…</div>
    <div class="spacersmall"></div>
    <div class="headingwrapper intro">
      <h1 class="heading ontop half">Überschrift</h1>   <!-- Outline, position:absolute, z-3 -->
      <img class="glasses">                              <!-- z-2 -->
      <img class="statue">                               <!-- z-1 -->
      <h1 class="heading half">Überschrift</h1>          <!-- gefüllt, im Fluss, z-auto -->
    </div>
    <div class="spacersmall"></div>
    <div class="pwrapper"><p class="paragraph">…</p></div>
    <div class="spacerbig"></div>
  </div>
</div>
```

Die Z-Ordnung ist die ganze Mechanik:

| Layer | z-index | Element |
|---|---|---|
| 3 | oben | Outline-Headline (transparent gefüllt, 1 px Kontur) |
| 2 | | vorderes Bildobjekt (Sonnenbrille) |
| 1 | | hinteres Bildobjekt (Statue) |
| — | unten | gefüllte Headline (normaler Fluss) |

```css
.heading.ontop { position: absolute; z-index: 3; margin-top: 0; }
@supports (-webkit-text-stroke: 1px black) {
  .ontop { -webkit-text-stroke: 1px black; -webkit-text-fill-color: transparent; }
}
@media (max-width: 477px) {
  .ontop { -webkit-text-stroke: 0.7px black; }
}
```

Bildpositionierung im Hero (absolut, in `em`):

```css
.statue  { z-index:1; width:24.03em; margin-top:12.4em; margin-left:39em;   position:absolute; }
.glasses { z-index:2; width:27.29em; margin-top: 5.5em; margin-left:40.1em; position:absolute; }
```
@1440: Statue 346 px breit bei Offset 562/179 px, Brille 393 px bei 578/79 px.

**Regel für neue Seiten:** Das Bildobjekt muss so platziert werden, dass es die gefüllte Headline
teilweise überdeckt — sonst entsteht der Effekt nicht. Zielbereich: horizontal zwischen 40 % und
75 % der Contentbreite, vertikal im unteren Drittel der Headline.

### 7.5 Buttons

```css
.button {
  display: inline-block;
  font: 700 1.67em/1.3 "Helvetica Neue";  /* 24.05px */
  letter-spacing: -.01vw;
  padding: 1.3em 1.5em 1em;               /* 31.3 / 36.1 / 24 px */
  border: .07em solid #fff;               /* ≈1.7px */
  border-radius: 1em;                     /* 24.05px — em der eigenen font-size */
  background: transparent;
  color: #fff;
  cursor: pointer;
}
```

Gemessene Buttongröße @1440: **279 × 90 px** („View Full Portfolio").

Das Padding ist **optisch asymmetrisch**: oben 1.3em, unten 1.0em. Das ist kein Fehler — es
kompensiert die Grundlinienlage von Helvetica Neue und lässt den Text optisch zentriert wirken.
Übernehmen.

**Drei Varianten, alle über Farbinversion definiert:**

| Variante | Default | Hover |
|---|---|---|
| `.button` (auf dunkel) | transparent, weißer Rahmen, weißer Text | **weiße Fläche, schwarzer Text** |
| `.button.black` (auf hell) | transparent, schwarzer Rahmen, schwarzer Text | **schwarze Fläche, weißer Text** |
| `.button.black.filled` | schwarze Fläche, Text `#fffcfc` | **weiße Fläche, schwarzer Text** |

Alle Hover-Wechsel sind **instantan** (`transition-duration: 0s` — verifiziert am Computed Style).
Das ist die zentrale Interaktionsentscheidung des Designs und darf nicht durch „weiche" Transitions
ersetzt werden.

Mobile-Override:
```css
@media (max-width:479px) {
  .button { border-width: 1px; font-size: 4em; }     /* 15px, Radius 15px, Box 175×56 */
  .button.black.filled.row, .button.black.row { margin-right: 0; margin-bottom: .5em; }
}
```
Aus der horizontalen Buttonreihe wird auf Mobile ein vertikaler Stack.

### 7.6 Karte — Team-Mitglied (`.membercard`)

> Die Klassen `.membercard`, `.teamimage01–03`, `.memberinfo`, `.memberticker`, `.grid-card` sind im
> Stylesheet vollständig definiert, werden aber auf den derzeit erreichbaren Seiten (`/`,
> `/founders`) **nicht gerendert** (`/team` liefert eine Webflow-Utility-Seite). Die folgenden Werte
> stammen daher **aus dem CSS, nicht aus einer Messung** — sie sind rechnerisch korrekt, aber der
> visuelle Zusammenbau ist *[geschätzt]*.

```css
.membercard {
  background: #fff;  border: 1px solid #000;  border-radius: 1.39em;  /* 20.02px */
  height: 44.31em;                                                    /* 638px */
  display: flex; flex-direction: column; justify-content: center; align-items: flex-start;
  width: 100%;  position: relative;  overflow: hidden;
}
.teamimage01, .teamimage02, .teamimage03 {
  position: absolute;  z-index: 1;
  max-height: 33em;                 /* 475px */
  max-width: none;  margin-inline: auto;
}
.memberinfo {
  position: absolute;  inset: auto 0% 0%;   /* am unteren Kartenrand */
  z-index: 2;
  width: 100.2%;  margin-bottom: -.2%;  margin-left: -.1%;   /* überlappt den Kartenrand */
  background: #fff;  border: 1px solid #000;  border-radius: 1.2em;  /* 17.28px */
  padding: 2em;                                                       /* 28.8px */
}
.membername { font-size: 17.5em; line-height: .9; white-space: nowrap; -webkit-text-stroke: 1px #fff; }
.memberticker { position: absolute; display: flex; flex-direction: row; align-items: center; }
```

Aufbau: Weiße Karte, darin ein laufender Riesentext mit dem Namen (Outline in Weiß auf Weiß →
subtiles Relief), darüber das freigestellte Porträt, davor unten ein Info-Kasten, der bewusst
1 px über die Kartenkante hinaussteht (`100.2%` / `−.2%`).

Grid: `.team-collection { margin-inline: -1em }` + `.teamitem { padding: 0 1em 2em }` →
**28.8 px Gutter**, Spaltenzahl über Webflow-Collection *[geschätzt: 3 auf Desktop]*.

Mobile:
```css
.membercard  { border-radius: 5.13em; height: auto; padding-top: 30em; justify-content: flex-start; }
.teamimage01 { position: relative; max-height: 70em; margin-top: 4em; }
.teamimage02, .teamimage03 { display: none; }   /* nur ein Bild auf Mobile */
.memberinfo  { position: relative; border: none; padding: 6em; transition: all .2s; }
.teamitem    { padding: 0 0 4em; }              /* einspaltig */
```

### 7.7 Akkordeon / „Rolodex" (`/founders`)

Die stärkste Komponente der Referenz. Karten **überlappen sich vertikal** und bilden einen Stapel.

```css
.rolladexitem {
  position: relative;  z-index: 2;
  background: #fff;  border: 1px solid #000;
  border-radius: 1.2rem;        /* 19.2px — beachte: rem, nicht em! */
  margin-top: -3.4em;           /* −48.96px → Überlappung */
  width: 100%;  overflow: hidden;  cursor: pointer;
  padding: 0;
}
.rolladexitem:last-child { padding-top: 2.5em; padding-bottom: 0; display: flex; }

.companydropdowntoggle {
  display: flex; justify-content: space-between; align-items: center;
  padding: 2.5em 2em 5.5em;     /* 36 / 28.8 / 79.2px */
  cursor: pointer;
}
.companydropdownlist {
  background: #fff;  padding-inline: 2em;  overflow: hidden;
  position: relative;  display: none;
  transform: translateY(-5em);  /* −72px: zieht den Inhalt unter den Toggle */
}
.pluswrapper.desktop { width: 2.5em; height: 2.5em; display: flex; }   /* 36×36px */
.line          { position: absolute; width: 100%; height: 1px; background: #000; }
.line.vertical { transform: rotate(90deg); }
```

Gemessen @1440: Karte 640 × 157 px, Radius 19.2 px, Toggle-Padding 36/28.8/79.2 px, Plus-Icon
36 × 36 px bei x = 1294.

**Der `-3.4em` Overlap ist der Kern.** Jede Karte schiebt sich 49 px unter die vorherige; das
großzügige `padding-bottom: 5.5em` (79 px) im Toggle sorgt dafür, dass der überlappte Bereich leer
ist. Ergebnis: ein Kartenstapel wie ein Rolodex, ohne einen einzigen Schatten.

Das Plus-Icon ist **kein Icon-Font und kein SVG**: zwei absolut positionierte 1-px-Divs, eines um
90° rotiert. Übernehmen — es skaliert perfekt mit und braucht keinen Asset-Load.

Webflow-Dropdown-Konfiguration: `data-hover="false"`, `data-delay="200"`.

Mobile:
```css
.rolladexitem { margin-top: -8.2em; border-radius: 5.13em; padding: 6em 6em 12em; transition: all .2s; }
.companydropdownlist { position: static; transform: none; padding-inline: 0; }
.companydropdowntoggle.w--open { margin-bottom: 4em; }
```
Auf Mobile ist dies die **einzige Stelle mit einer Transition** (`all .2s ease`).

### 7.8 Marquee / Ticker

```css
.marquee-wrapper { position: relative; width: 100%; height: 16vw; display: flex; align-items: center; z-index: 1; }
.marquee-track    { position: absolute; white-space: nowrap; will-change: transform;
                    animation: marquee-horizontal 60s linear infinite; }
.marquee-track-02 { animation: marquee-horizontal-02 60s linear infinite; }
.marquee-list { display: flex; flex-wrap: nowrap; }
.marquee-item { display: flex; justify-content: center; align-items: center; margin-right: 6vw; }

@keyframes marquee-horizontal    { from { transform: translateX(0);    } to { transform: translateX(-50%); } }
@keyframes marquee-horizontal-02 { from { transform: translateX(-50%); } to { transform: translateX(0);    } }

@media (min-width: 992px) {
  .marquee-track:hover, .marquee-track-02:hover { animation-play-state: paused; }
}

.tickerlink { font: 300 17.5vw/.9 "MD Nichrome"; text-transform: uppercase; white-space: nowrap;
              color: #fff; z-index: 4; }
@supports (-webkit-text-stroke: 1px white) {
  .tickerlink       { -webkit-text-stroke: 1px #fff;    -webkit-text-fill-color: transparent; }
  .tickerlink:hover { -webkit-text-stroke: 0 #ff4f2c;   -webkit-text-fill-color: #ff4f2c;     }
}
```

**Implementierungsdetail:** Die Liste muss **exakt zweimal** im DOM stehen (zwei identische
`.marquee-list` im Track), damit `translateX(-50%)` einen nahtlosen Loop erzeugt. Gemessen: 3
Marquee-Reihen à 230 px Höhe, Reihe 2 läuft gegenläufig.

Hover-Verhalten: Der weiße Outline-Text füllt sich **hart** mit Aperol und verliert seine Kontur.
Zusätzlich pausiert der gesamte Track. Beides ohne Transition.

`.foundercursor01–03` sind drei 30vw breite Bilder pro Ticker-Item, per Default
`display: none` — vorgesehen als Cursor-Follow-Bilder beim Hover *[geschätzt: die zugehörige
JS-Logik ist auf der Live-Seite nicht aktiv]*.

### 7.9 Content-Sektion mit Full-Bleed-Bild

```css
.section          { position: relative; overflow: hidden; }
.bgimagewrapper   { position: absolute; z-index: 0; width: 100%; height: 100%;
                    background: #b1c4de;
                    display: flex; flex-direction: column; justify-content: flex-end; align-items: flex-start; }
.bgimage          { z-index: 0; width: 100%; max-width: none; object-fit: cover; }
.bgimagespacer    { height: 50vw; }
```

Muster: Das Bild sitzt **unten** in der Sektion (`justify-content: flex-end`), der Text darüber im
freien Bereich. `.bgimagespacer` (50 vw = 720 px @1440) reserviert die Höhe im Fluss. Der
Hintergrund `#b1c4de` ist die Farbe, die während des Bildladens sichtbar ist — ein bewusst gesetzter
Ladeplatzhalter, nicht Zufall.

### 7.10 Footer

```css
.footerwrapper { display: flex; justify-content: space-between; align-items: center; padding-bottom: 3em; }
.psmall        { font-size: 1.11em; line-height: 1.5; color: #000; margin-bottom: 0; }
.link          { font-weight: 700; margin-right: 2em; cursor: pointer; color: #ff4f2c; }
```

Gemessen @1440: 1280 × 67 px bei y = 6405. Links: Copyright. Rechts: 5 Rechtslinks in Aperol,
28.8 px Abstand.

Mobile:
```css
.footerwrapper      { flex-direction: column; align-items: flex-start; padding-bottom: 30em; }
.link               { margin-left: 0; margin-right: 5em; }
.copryrightwrapper  { margin-bottom: 4em; }
.container.paddingtop { padding-top: 38.3em; }   /* 143.6px @375 */
```
Das große `padding-bottom: 30em` (112 px) schafft Platz für die fixierte Bottom-Navigation.

### 7.11 Formulare / Inputs / Badges / Tabs

**Existieren im Design nicht.** Das Stylesheet enthält ausschließlich Webflow-Defaults für
`.w-input`, `.w-tab-link`, `.w-slider` etc. — keine einzige Custom-Regel. Es gibt keine Badges,
keine Tabs, keine Formulare, keine Tooltips, keine Modals.

Für das neue System siehe Abschnitt 14.3: dort ist ein Input/Form-Set spezifiziert, das aus den
vorhandenen Prinzipien (1 px schwarzer Rahmen, weiße Fläche, `radius-md`, harte Zustände)
konsequent abgeleitet ist — als Erweiterung gekennzeichnet, nicht als Fund.

---

## 8. Borders, Radius & Shadows

### 8.1 Border-System

| Kontext | Wert |
|---|---|
| Alle Flächen (Nav, Karten, Akkordeon) | `1px solid #000` |
| Buttons Desktop | `.07em solid` → ≈1.7 px |
| Buttons Mobile | `1px solid` |
| Plus-Icon-Linien | `1px` Höhe, `#000` |
| Grid-Card | `border-bottom: 1.5px solid rgba(238,237,242,.19)` |
| Text-Outline | `-webkit-text-stroke: 1px` (Desktop) / `0.7px` (≤477 px) |

**Regel: Die Rahmenstärke skaliert nicht mit.** Bei 1 px bleibt es bei 1 px, egal wie groß der
Viewport. Das ist bewusst — mitwachsende Rahmen würden bei 252-px-Typografie plump wirken.
Einzige Ausnahme ist der Button (`.07em`), was auf Mobile explizit auf `1px` zurückkorrigiert wird.

### 8.2 Radius-System

Das Original ist hier inkonsistent (drei verschiedene Einheiten). Rekonstruierte, bereinigte Skala:

| Token | Original | @1440 px | @375 px | Verwendung |
|---|---|---|---|---|
| `radius-sm` | — | 8 px | 8 px | *(Erweiterung: Inputs, kleine Elemente)* |
| `radius-md` | `1.2em` | 17.3 px | 19.2 px | Info-Kasten in Karte |
| `radius-lg` | `1.2rem` / `5.13em` | 19.2 px | 19.24 px | Akkordeon-Karte |
| `radius-xl` | `1.39em` / `3em` | 20.0 px | 11.25 px | Navigationspille, Team-Karte |
| `radius-btn` | `1em` (der eigenen `font-size`) | 24.05 px | 15 px | Button |
| `radius-full` | `50%` / `100%` | — | — | nur Webflow-Defaults, ungenutzt |

Die drei Werte 17.3 / 19.2 / 20.0 px sind praktisch nicht unterscheidbar. **Empfehlung für das neue
System: auf zwei Werte reduzieren** — `radius-md: 1.2rem` (19.2 px) für alle Flächen,
`radius-btn: 1em` (relativ zur Buttongröße) für Buttons. Das ist die einzige Vereinfachung, die ich
gegenüber der Referenz vorschlage; sie ändert das Erscheinungsbild nicht messbar.

Auffällig: Der Button-Radius ist an die **eigene Schriftgröße** gekoppelt (`1em` bei
`font-size: 1.67em`). Dadurch bleibt das Verhältnis Radius zu Texthöhe über alle Viewports konstant
— ein guter Trick, den man behalten sollte.

### 8.3 Shadows

**Es gibt keine.** Verifiziert: das gesamte Stylesheet enthält nur drei `box-shadow`-Deklarationen,
alle in Webflow-Defaults (`.w-input:focus`, Lightbox, Slider-Nav). Keine einzige Custom-Komponente
hat einen Schatten.

Tiefe entsteht ausschließlich durch:
1. **z-index-Stapelung** (Outline-Text über Bild über Fülltext)
2. **Negative Margins** (`-3.4em` Kartenüberlappung)
3. **1px schwarze Rahmen** auf weißen Flächen

Für das neue System: `--shadow-none: none` als expliziter Token, damit klar ist, dass es eine
Entscheidung ist und kein Versäumnis.

### 8.4 Opacity, Gradients, Blur, Glassmorphism

| Effekt | Status im Original |
|---|---|
| Opacity | Nur `a:hover { opacity: .5 }` und Alpha-Farben (`.19`, `.36`) |
| Gradients | **keine** |
| `backdrop-filter` / Blur | **keine** |
| Glassmorphism | **nein** — die Nav-Pille ist deckendes Weiß, kein Frosted Glass |
| Overlays | **keine** Farb-Overlays über Bildern |
| Mix-Blend-Modes | **keine** |

Das ist keine Lücke, sondern die Kernaussage: **Alle Effekte im Design sind Kompositionseffekte, keine
Filtereffekte.** Wer hier einen Verlauf oder ein Glass-Panel einbaut, bricht das System.

---

## 9. Bilder & Medien

### 9.1 Gemessene Assets

| Klasse | Format | Intrinsisch | Gerendert @1440 | `object-fit` | Radius |
|---|---|---|---|---|---|
| `.logo` | SVG | 146 × 25 | 146 × 39 | fill | 0 |
| `.glasses` | PNG (α) | 393 × 135 | 393 × 135 | fill | 0 |
| `.statue` | PNG (α) | 347 × 457 | 346 × 456 | fill | 0 |
| `.handleft` | PNG (α) | 576 × 286 | 578 × 287 | fill | 0 |
| `.handright` | PNG (α) | 864 × 317 | 867 × 319 | fill | 0 |
| `.coffee` | PNG (α) | — | 54.17em breit | fill | 0 |
| `.bgimage` | JPG | — | 1440 × auto | **cover** | 0 |

### 9.2 Regeln

**Kein einziges Bild hat einen Border-Radius.** Nicht eines. Bilder sind entweder freigestellte
Objekte mit Alphakanal oder ein Full-Bleed-Foto — beide brauchen keine Maske.

**Kein `object-fit` außer beim Full-Bleed-Foto.** Alle Cutouts werden in ihrer natürlichen Ratio
skaliert (`width` in `em`, Höhe automatisch). Es gibt **keine festen Seitenverhältnisse** und keine
`aspect-ratio`-Boxen im gesamten CSS.

**Positionierung ausschließlich absolut, in `em`:**
```css
.statue    { width: 24.03em; margin-top: 12.4em;  margin-left: 39em;   position: absolute; }
.glasses   { width: 27.29em; margin-top:  5.5em;  margin-left: 40.1em; position: absolute; }
.handright { width: 60.21em; margin-top:  4.2em;  margin-left: 41.5em; position: absolute; }
.handleft  { width: 40.14em; margin-top:  8.1em;  margin-left:-10.4em; position: absolute; }
.coffee    { width: 54.17em; margin-top: -8.8em;  margin-left: 40.4em; position: absolute; }
```
`.handleft` mit `margin-left: -10.4em` läuft links aus dem Bild — die Sektion fängt es mit
`overflow: hidden` ab. Das ist ein wiederkehrendes Muster: **mindestens ein Bildobjekt pro Sektion
sollte angeschnitten sein.**

Responsive Größen über `sizes`-Attribut:
```html
<img class="handleft"  sizes="(max-width: 479px) 60vw, 40vw" srcset="…">
<img class="handright" sizes="(max-width: 479px) 89vw, 60vw" srcset="…">
```

### 9.3 Bildbriefing für neue Inhalte

Die konkreten Motive sind nicht zu übernehmen. Damit dieselbe visuelle Wirkung entsteht, müssen die
neuen Bilder folgende **Eigenschaften** erfüllen:

**Typ A — Freigestellte Objekte (das Hauptmaterial, 4–6 pro Seite)**
- PNG oder WebP **mit Alphakanal**, vollständig freigestellt, keine Restkanten
- Motive mit **klarer, geschlossener Silhouette** (ein Objekt, kein Arrangement)
- **Hoher Eigenkontrast, aber gedämpfte Farbigkeit** — die Referenz nutzt Gips, Schwarzweiß und
  Metall, damit die Objekte gegen die Aperol-Fläche nicht konkurrieren. Bunte Objekte auf farbiger
  Fläche zerstören den Effekt
- Auflösung mindestens **1.6× der Renderbreite** (Referenz: 864 px Asset für 867 px Rendergröße
  — grenzwertig; besser 1400–1800 px Kantenlänge)
- Motivwelt: **ein einzelnes physisches Objekt, leicht überhöht/absurd im Kontext**. Bei der
  Referenz: antike Büste mit Sonnenbrille, Hände, Espressotasse. Für ein anderes Thema wäre das
  äquivalente Prinzip ein alltägliches Objekt der Branche, isoliert und übergroß

**Typ B — Full-Bleed-Foto (max. 1 pro Seite)**
- JPG/WebP, Querformat, **mindestens 2880 px breit**
- Motiv mit **ruhiger oberer Bildhälfte** — der Text steht darüber
- Dominante Farbe sollte als Ladeplatzhalter im Wrapper hinterlegt werden (Referenz: `#b1c4de`)

**Typ C — Porträts (Team/Personen)**
- Freigestellt vor transparentem Hintergrund, **Hochformat ca. 3:4**
- Halbnah, Blick zur Kamera, einheitliche Ausleuchtung über alle Porträts
- max. 475 px Renderhöhe (`max-height: 33em`)

**Nicht verwenden:** Stockfotos mit Hintergrund, abgerundete Bildkacheln, Bildraster,
Bild-Overlays, Duotone-Filter, Hero-Video.

---

## 10. Responsive Verhalten

### 10.1 Breakpoints

| Breakpoint | Im Original | Was passiert |
|---|---|---|
| **≥ 1440 px** | `min-width: 1440px` | Basisunit friert bei 14.4 px ein. Layout wächst nicht mehr, wird nur zentriert |
| **992 – 1439 px** | — | **Keine Regel.** Reines vw-Scaling |
| **768 – 991 px** | `max-width: 991px` | Nur eine Regel (`.grid-card`). Layout unverändert |
| **480 – 767 px** | `max-width: 767px` | **Keine Custom-Regel.** Layout unverändert — hier liegt der Defekt |
| **≤ 479 px** | `max-width: 479px` | **Der einzige echte Layout-Breakpoint** (≈100 Regeln) |
| **≤ 477 px** | `max-width: 477px` | Text-Stroke von 1 px auf 0.7 px |

Die 991er- und 767er-Blöcke enthalten fast ausschließlich Webflow-Systemregeln. Das Design hat
faktisch **einen** Breakpoint.

### 10.2 Was sich bei ≤ 479 px ändert

| Bereich | Desktop | Mobile |
|---|---|---|
| Navigation | Pille oben rechts, horizontal | Pille unten zentriert, vertikal, mit „Menu"-Trigger |
| Logo | 146 px | 112.5 px |
| H1 | 230 px | 60 px |
| H2 | 252 px | 74 px |
| Fließtext | 26 px | 17.3 px |
| Textspalten | 520 px / Offset 640 px | 100 %, kein Offset |
| 50/50-Split | `flex-row` | `flex-column` |
| Sticky-Visual | `position: sticky` | statisch, `margin-top: -36.9em` |
| Team-Karte | fixe Höhe 638 px, Bild absolut | `height: auto`, Bild im Fluss, nur 1 von 3 Bildern |
| Akkordeon-Overlap | −49 px | −30.75 px |
| Buttons | Zeile | Stack |
| Footer | Zeile, `space-between` | Spalte, linksbündig |
| Card-Radius | 20 px | 19.2 px |
| Nav-Radius | 20 px | 11.25 px |
| Transitions | keine | `all .2s` auf Akkordeon + Karten-Info |

### 10.3 Was sich *nicht* ändert

- Container-Seitenpadding bleibt `5.56em` (proportional identisch)
- Die Doppel-Headline-Mechanik bleibt aktiv (nur dünnerer Stroke)
- Farbschema, Rahmenstärken, Bildbehandlung
- Reihenfolge und Anzahl der Sektionen

### 10.4 Korrektur des Skalierungsdefekts *(Empfehlung, nicht aus der Referenz)*

Der Bereich 480–767 px rendert Fließtext bei 8.7–13.9 px und Navigation bei 5.3–8.5 px. Verifiziert
bei 600 px Viewport: **6.66 px Navigationsschrift.**

Fix ohne Änderung der Designsprache — der Basisunit bekommt eine Untergrenze:

```css
:root { --u: clamp(10px, 1vw, 14.4px); }
body  { font-size: var(--u); }

@media (max-width: 479px) {
  :root { --u: clamp(3.6px, 1vw, 5px); }   /* Mobile hat eigene Multiplikatoren */
}
```

Wirkung: unterhalb von 1000 px Viewport friert der Unit bei 10 px ein → Fließtext 18.1 px,
Navigation 11.1 px, H2 175 px. Das Layout wird dabei relativ zur Viewportbreite größer, was den
Poster-Charakter im Tabletbereich sogar verstärkt. Ab 480 px greift der Mobile-Satz.

Alternativ (konservativer): einen echten Tablet-Breakpoint bei 991 px einziehen, der die
Multiplikatoren zwischen Desktop- und Mobile-Satz interpoliert.

---

## 11. Animationen & Interaktionen

### 11.1 Vollständige Inventur

Gemessen an den Computed Styles: **`transition-duration` ist auf allen Desktop-Komponenten `0s`.**
`transition-property: all`, `timing-function: ease` sind gesetzt, aber ohne Dauer wirkungslos.

| Interaktion | Trigger | Änderung | Dauer | Easing |
|---|---|---|---|---|
| Link generisch | `a:hover` | `opacity: 1 → .5` | **0 s** | — |
| Navigationslink | `:hover` | BG transparent → `#000`, Text `#000 → #fff` | **0 s** | — |
| Button (hell) | `:hover` | BG transparent → `#fff`, Text `#fff → #000` | **0 s** | — |
| Button `.black` | `:hover` | BG transparent → `#000`, Text `#000 → #fff` | **0 s** | — |
| Button `.black.filled` | `:hover` | BG `#000 → #fff`, Text `#fffcfc → #000` | **0 s** | — |
| Ticker-Link | `:hover` | Stroke `1px #fff` → `0`, Fill `transparent → #ff4f2c` | **0 s** | — |
| Marquee-Track | `:hover` (≥992 px) | `animation-play-state: running → paused` | 0 s | — |
| Marquee-Lauf | permanent | `translateX(0) → (-50%)` | **60 s** | `linear`, `infinite` |
| Marquee Reihe 2 | permanent | `translateX(-50%) → (0)` | **60 s** | `linear`, gegenläufig |
| Dropdown Navigation | Click | Webflow-Dropdown öffnen | `data-delay: 300` | Webflow-Default |
| Dropdown Akkordeon | Click | Webflow-Dropdown öffnen | `data-delay: 200` | Webflow-Default |
| Akkordeon Mobile | `:hover`/State | `all` | **.2 s** | `ease` |
| Karten-Info Mobile | State | `all` | **.2 s** | `ease` |

### 11.2 Was es *nicht* gibt

- **Keine Scroll-Animationen.** Verifiziert: das HTML enthält keine Webflow-IX2-Daten
  (`actionLists`, `eventTypeId` — beides null Treffer). Nichts faded ein, nichts sliced herein
- Keine Parallax-Effekte
- Keine Reveal-/Stagger-Animationen
- Keine Zahl-Counter, keine Progress-Indikatoren
- Keine Seitenübergänge
- Keine `scroll-behavior: smooth`

Die einzige scrollgebundene Bewegung ist `position: sticky` auf `.foundersvisual` — das Visual bleibt
stehen, während die Akkordeonliste daran vorbeiläuft.

### 11.3 Microinteractions

Ein einziges Custom-Skript, das die **Textselektionsfarbe bei jedem Mausklick rotiert**:

```js
$('body').mousedown(selectColor);
$('body').mouseup(selectColor);
// wechselt body zwischen .select1 / .select2 / .select3
```

> Die zugehörigen `::selection`-Regeln existieren im Stylesheet **nicht** — verifiziert. Das Skript
> ist wirkungslos (Restcode aus einem Template). Ebenso `$('.grid_media').draggable()`, dessen
> Zielelemente auf keiner Seite existieren. **Nicht übernehmen.**
>
> Die *Idee* ist allerdings gut und passt zum Charakter. Wer sie will, braucht zusätzlich:
> ```css
> .select1 ::selection { background: #ff4f2c; color: #fff; }
> .select2 ::selection { background: #000;    color: #ff4f2c; }
> .select3 ::selection { background: #dfdfdf; color: #000; }
> ```

### 11.4 Bewegungsprinzip für das neue System

> **Zustandswechsel sind Schnitte, keine Blenden.**

Hover, Active und Open sind harte Umschaltungen ohne Dauer. Die einzige Bewegung im Design ist
kontinuierlich und richtungsstabil (Marquee). Es gibt keine Beschleunigung, kein Ein- und
Ausschwingen, keine Elastizität.

Wer Transitions ergänzen will, sollte maximal `0.12s linear` auf Farbwerte setzen — alles darüber
kippt das Design ins Konventionelle.

**Barrierefreiheit:** Der 60-s-Marquee läuft ohne `prefers-reduced-motion`-Ausnahme. Für das neue
System zwingend ergänzen (siehe 14.4).

---

## 12. Design Tokens

Die Datei `tokens.css` im Projektordner enthält diesen Block einsatzbereit. Hier die Struktur mit
Begründungen.

```css
:root {
  /* ══ 1. BASIS-UNIT ══════════════════════════════════════════
     Die zentrale Größe. Alles andere ist ein Vielfaches davon.
     clamp() korrigiert den Skalierungsdefekt der Referenz (10.4). */
  --u: clamp(10px, 1vw, 14.4px);

  /* ══ 2. FARBEN ══════════════════════════════════════════════ */
  --color-primary:        #FF4F2C;   /* rgb(255,79,44)   hsl(10,100%,59%)  */
  --color-primary-ink:    #E03A18;   /* abgedunkelt für Links auf hell     */
  --color-secondary:      #000000;
  --color-accent:         var(--color-primary);

  --color-background:     #DFDFDF;   /* rgb(223,223,223) hsl(0,0%,87%)     */
  --color-background-alt: #000000;   /* Sektionsfläche „dunkel"            */
  --color-background-hero:var(--color-primary);
  --color-surface:        #FFFFFF;   /* Karten, Nav-Pille — nie Sektion    */

  --color-text-primary:   #000000;
  --color-text-secondary: #333333;
  --color-text-inverse:   #FFFFFF;
  --color-text-on-fill:   #FFFCFC;
  --color-text-muted:     rgba(255,255,255,.19);

  --color-border:         #000000;
  --color-border-subtle:  rgba(238,237,242,.19);

  --color-success:        #1F9E5B;   /* Erweiterung, nicht in Referenz     */
  --color-warning:        #E5A100;   /* Erweiterung                        */
  --color-error:          #C4231A;   /* Erweiterung                        */

  --color-image-placeholder: #B1C4DE;

  /* ══ 3. TYPOGRAFIE ══════════════════════════════════════════ */
  --font-display: "Anton", "MD Nichrome", Impact, sans-serif;
  --font-body:    "Inter", "Helvetica Neue", -apple-system, Arial, sans-serif;

  --fw-regular: 400;
  --fw-medium:  500;
  --fw-bold:    700;

  /* Größen als Vielfache von --u */
  --fs-display-2xl: calc(var(--u) * 17.5);   /* 252px  @1440 */
  --fs-display-xl:  calc(var(--u) * 16);     /* 230px  @1440 */
  --fs-heading-sm:  calc(var(--u) * 2.22);   /* 32px         */
  --fs-body-lg:     calc(var(--u) * 1.81);   /* 26px         */
  --fs-button:      calc(var(--u) * 1.67);   /* 24px         */
  --fs-nav:         calc(var(--u) * 1.11);   /* 16px         */
  --fs-caption:     calc(var(--u) * 1.11);   /* 16px         */
  --fs-link-sm:     calc(var(--u) * 1);      /* 14.4px       */

  --lh-display: .9;
  --lh-tight:   1;
  --lh-body:    1.3;
  --lh-loose:   1.5;

  --ls-display: -.01vw;
  --ls-body:    -.02em;

  /* ══ 4. SPACING ═════════════════════════════════════════════ */
  --space-2xs: calc(var(--u) * 0.5);   /*   7.2px */
  --space-xs:  calc(var(--u) * 1);     /*  14.4px */
  --space-sm:  calc(var(--u) * 2);     /*  28.8px */
  --space-md:  calc(var(--u) * 2.5);   /*  36px   */
  --space-lg:  calc(var(--u) * 3.5);   /*  50.4px */
  --space-xl:  calc(var(--u) * 5.56);  /*  80px   ← Container-Padding */
  --space-2xl: calc(var(--u) * 6);     /*  86.4px */
  --space-3xl: calc(var(--u) * 9);     /* 129.6px */
  --space-4xl: calc(var(--u) * 15);    /* 216px   ← Sektionsabstand   */

  /* ══ 5. SIZING & CONTAINER ══════════════════════════════════ */
  --container-max-width:  calc(var(--u) * 100);    /* 1440px */
  --container-padding:    var(--space-xl);
  --content-width:        calc(var(--u) * 88.9);   /* 1280px */
  --column-text:          calc(var(--u) * 36.11);  /*  520px */
  --column-text-wide:     calc(var(--u) * 60);     /*  864px */
  --column-offset-half:   calc(var(--u) * 44.44);  /*  640px */
  --card-height:          calc(var(--u) * 44.31);  /*  638px */
  --portrait-max-height:  calc(var(--u) * 33);     /*  475px */
  --marquee-height:       16vw;
  --fullbleed-height:     50vw;

  /* ══ 6. BORDER RADIUS ═══════════════════════════════════════ */
  --radius-sm:   8px;
  --radius-md:   1.2rem;   /* 19.2px — alle Flächen */
  --radius-lg:   1.2rem;
  --radius-btn:  1em;      /* relativ zur Buttonschrift */
  --radius-pill: 1.39em;

  /* ══ 7. BORDERS ═════════════════════════════════════════════ */
  --border-width:        1px;    /* skaliert bewusst NICHT mit */
  --border-width-thick:  1.5px;
  --border-default:      var(--border-width) solid var(--color-border);
  --text-stroke:         1px;
  --text-stroke-mobile:  0.7px;

  /* ══ 8. SHADOWS ═════════════════════════════════════════════ */
  --shadow-none: none;     /* bewusste Entscheidung, kein Versäumnis */
  --shadow-card: none;

  /* ══ 9. TRANSITIONS ═════════════════════════════════════════ */
  --transition-instant: 0s;              /* Default für alle Hover-States */
  --transition-fast:    .12s linear;     /* Obergrenze, falls nötig       */
  --transition-mobile:  .2s ease;        /* nur Akkordeon/Karten ≤479px   */
  --marquee-duration:   60s;
  --marquee-easing:     linear;
  --dropdown-delay:     200ms;

  /* ══ 10. Z-INDEX ════════════════════════════════════════════ */
  --z-base:            0;
  --z-image-back:      1;
  --z-image-front:     2;
  --z-heading-outline: 3;
  --z-ticker:          4;
  --z-card-overlay:    2;
  --z-nav-mobile:      100;
  --z-nav:             900;

  /* ══ 11. BREAKPOINTS (als Referenz, in @media wörtlich) ═════ */
  --bp-mobile:  479px;
  --bp-tablet:  767px;
  --bp-laptop:  991px;
  --bp-freeze: 1440px;
}

/* Mobile-Multiplikatorsatz */
@media (max-width: 479px) {
  :root {
    --u: clamp(3.6px, 1vw, 5px);

    --fs-display-2xl: calc(var(--u) * 19.7);
    --fs-display-xl:  calc(var(--u) * 16);
    --fs-heading-sm:  calc(var(--u) * 4.62);
    --fs-body-lg:     calc(var(--u) * 4.62);
    --fs-button:      calc(var(--u) * 4);
    --fs-nav:         calc(var(--u) * 4);
    --fs-caption:     calc(var(--u) * 3.59);

    --space-xs:  calc(var(--u) * 2);
    --space-sm:  calc(var(--u) * 4);
    --space-2xl: calc(var(--u) * 10);
    --space-3xl: calc(var(--u) * 25);
    --space-4xl: calc(var(--u) * 30);

    --radius-pill: 3em;
    --text-stroke: var(--text-stroke-mobile);
  }
}
```

---

## 13. Übergeordnete Designprinzipien

Diese zehn Regeln sind das eigentliche Ergebnis der Analyse. Wer sie einhält, erzeugt ein Design
derselben Familie — auch mit völlig anderen Farben, Inhalten und Bildern.

**1. Ein Wert regiert alles.**
Es gibt exakt eine Basisgröße. Jede Schriftgröße, jedes Padding, jeder Radius, jede Bildbreite ist
ein `em`-Vielfaches davon. Keine willkürlichen Pixelwerte. Ausnahmen: Rahmenstärken (immer 1 px) und
Textkonturen.

**2. Der typografische Kontrast ist ~10:1.**
Display-Text ist rund zehnmal so groß wie Fließtext. Es gibt nichts dazwischen. Dieses Verhältnis
ist wichtiger als die absoluten Größen — es überträgt sich auf jedes Farbschema und jeden Inhalt.

**3. Whitespace ist zwei Drittel der Seite.**
Jede Sektion öffnet und schließt mit 216 px Leerraum. Content-Dichte ist niedrig und soll es
bleiben. Wenn eine Sektion voll wirkt, ist zu viel drin.

**4. Der Akzentton ist Fläche oder Signal, nie UI.**
Aperol füllt eine ganze Sektion oder färbt einen Link. Es füllt nie einen Button, nie eine Karte,
nie eine Überschrift. Diese Enthaltsamkeit macht die Farbe stark.

**5. Bilder liegen über der Typografie, nicht daneben.**
Freigestellte Objekte werden absolut über die Headline gelegt und dürfen den Text verdecken. Der
Doppel-Headline-Trick (gefüllt unten, Outline oben) macht das möglich, ohne Lesbarkeit zu verlieren.
Kein Bild sitzt in einer Box.

**6. Mindestens ein Bildobjekt pro Sektion ist angeschnitten.**
Objekte laufen über den Viewportrand hinaus; `overflow: hidden` auf der Sektion fängt sie ab. Das
erzeugt den Eindruck, das Layout sei größer als der Bildschirm.

**7. Tiefe entsteht durch Stapelung, nicht durch Schatten.**
z-index, negative Margins und 1-px-Rahmen ersetzen jede Form von Elevation. Kein Schatten, kein
Verlauf, kein Blur — nirgends.

**8. Zustandswechsel sind Schnitte.**
Hover invertiert Vorder- und Hintergrundfarbe, sofort. Keine Transition, kein Fade. Das ist keine
Nachlässigkeit, sondern das prägendste Interaktionsmerkmal des Designs.

**9. Gruppierung durch Fläche, nicht durch Linien oder Abstände.**
Zusammengehöriges sitzt in einer weißen Karte mit 1-px-Rahmen und großem Radius auf farbigem
Grund. Es gibt keine Trennlinien, keine Divider, keine Hintergrund-Schattierungen.

**10. Hierarchie entsteht durch Größe und Sektionsfarbe, nicht durch Gewicht.**
Es gibt nur drei Schriftgewichte, und sie markieren Funktion (400 Fließtext, 500 kleine Headline,
700 UI), nicht Wichtigkeit. Wichtigkeit wird über Größe und über den Wechsel des
Sektionshintergrunds erzeugt.

### 13.1 Verhältnis Minimalismus zu Dekoration

Das Design ist **strukturell minimalistisch und inhaltlich dekorativ**. Die Struktur ist so einfach
wie möglich (eine Spalte, vier Farben, keine Effekte, ~175 CSS-Regeln); die Dekoration liegt
vollständig in zwei Elementen: der überdimensionalen Display-Typografie und den freigestellten
Bildobjekten.

Das ist die reproduzierbare Formel: **Reduziere alles außer Schriftgröße und Bildmotiv.** Wer
Dekoration hinzufügen will, vergrößert die Headline oder fügt ein Objekt hinzu — er fügt keinen
Verlauf, kein Muster und keinen Schatten hinzu.

---

## 14. Entwickler-Spezifikation

### 14.1 Dateien in diesem Ordner

| Datei | Inhalt |
|---|---|
| `DESIGN-SYSTEM.md` | dieses Dokument |
| `tokens.css` | Abschnitt 12 einsatzbereit |
| `base.css` | Reset, Basiselemente, Layout-Primitives |
| `components.css` | Alle Komponenten aus Abschnitt 7 |

Einbindung:
```html
<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="base.css">
<link rel="stylesheet" href="components.css">
```

### 14.2 Was ausgetauscht wird — und wo genau

| Auszutauschen | Datei | Stelle |
|---|---|---|
| Farben | `tokens.css` | Block 2, nur die 4 Kernfarben ändern; alles andere leitet sich ab |
| Schriften | `tokens.css` | `--font-display`, `--font-body` + `@font-face` in `base.css` |
| Logo | HTML | `<img class="logo">`, SVG, Breite über `--u * 10.14` |
| Bilder | HTML | Klassen `.hero-object-back` / `.hero-object-front` mit `em`-Offsets |
| Texte | HTML | direkt |
| Sektionsfolge | HTML | Sektionen kopieren, `.section--aperol` / `--grigio` / `--black` wechseln |

**Was nicht angefasst werden darf**, sonst bricht die Designfamilie:
`--u` und alle `calc(var(--u) * …)`-Multiplikatoren, `--border-width: 1px`,
`--transition-instant: 0s`, `--shadow-*: none`, die z-index-Leiter, die Doppel-Headline-Struktur.

### 14.3 Erweiterungen (nicht in der Referenz vorhanden)

Formulare, Inputs, Badges und Tabs existieren im Original nicht. Sie sind in `components.css`
konsequent aus den vorhandenen Prinzipien abgeleitet:

- **Input:** weiße Fläche, `1px solid #000`, `--radius-md`, `--fs-body-lg`, Padding `--space-sm`,
  kein Schatten, Focus = 2 px schwarzer Ring ohne Transition
- **Badge:** `--fs-caption`, `--radius-pill`, `1px solid`, transparent, uppercase
- **Tab:** wie Navigationslink — harter Farbumschlag, aktiver Tab schwarz gefüllt

Diese Komponenten sind als Erweiterung markiert und können ohne Bruch entfernt werden.

### 14.4 Pflicht-Ergänzungen zur Barrierefreiheit

Die Referenz hat drei verifizierte Lücken. Für das neue System zwingend:

```css
/* 1. Focus-States — im Original existiert KEINE einzige :focus-Regel */
a:focus-visible, button:focus-visible, .button:focus-visible,
.navlink:focus-visible, [tabindex]:focus-visible {
  outline: 2px solid currentColor;
  outline-offset: 3px;
}

/* 2. Reduced Motion — der 60s-Marquee läuft im Original ungebremst */
@media (prefers-reduced-motion: reduce) {
  .marquee-track, .marquee-track-02 { animation: none; transform: none; }
  *, *::before, *::after { animation-duration: .01ms !important; transition-duration: .01ms !important; }
}

/* 3. Linkkontrast — Accent auf Grigio ist nur 2.9:1 */
a { color: var(--color-primary-ink); text-decoration: underline; text-underline-offset: .15em; }
.section--dark a { color: var(--color-primary); }
```

Außerdem: `-webkit-text-stroke` mit `-webkit-text-fill-color: transparent` ist nicht in allen
Engines identisch. Das Original kapselt es korrekt in `@supports` — beibehalten, sonst wird die
Outline-Headline in nicht unterstützenden Browsern unsichtbar.

### 14.5 Umsetzungsreihenfolge

1. `tokens.css` einbinden, die 4 Kernfarben austauschen, Schriften laden
2. Container + Spacer-Primitives (`.spacer--sm/md/lg/xl`) — der vertikale Rhythmus zuerst
3. Sektionsvarianten (`--aperol` / `--grigio` / `--black` / `--image`)
4. Doppel-Headline-Komponente inkl. `@supports`-Kapselung — das ist die Signature, zuerst richtig
   bauen
5. Navigationspille (Desktop fixed oben rechts, Mobile fixed unten zentriert)
6. Buttons mit den drei Inversionsvarianten
7. Karten + Akkordeon-Stapel
8. Marquee (Liste zweimal im DOM!)
9. Mobile-Breakpoint bei 479 px mit dem eigenen Multiplikatorsatz
10. Focus-States und `prefers-reduced-motion`

---

## 15. Umsetzungs-Checkliste

**Fundament**
- [ ] `--u: clamp(10px, 1vw, 14.4px)` gesetzt, `body { font-size: var(--u) }`
- [ ] Container 100 u max-width, 5.56 u Seitenpadding → 88.9 u Contentbreite
- [ ] Alle Größen als `calc(var(--u) * n)` — keine losen Pixelwerte außer Rahmen

**Farbe**
- [ ] Genau 4 Kernfarben definiert
- [ ] Accent nur als Sektionsfläche und Linkfarbe, nie als Button-/Kartenfüllung
- [ ] Weiß nur als Surface, nie als Sektionsfläche
- [ ] Kontrast Text/Fläche ≥ 4.5:1 geprüft (Accent ggf. abdunkeln)

**Typografie**
- [ ] Zwei Familien: Display (uppercase, ≥60 px) und Body
- [ ] Display-zu-Body-Verhältnis ~10:1 auf Desktop, ~4:1 auf Mobile
- [ ] Keine erfundene Zwischengröße zwischen 32 px und 230 px
- [ ] `line-height: .9` auf Display, `1.3` auf Body
- [ ] Negatives Letter-Spacing (−.01vw Display, −.02em Body)
- [ ] `-webkit-font-smoothing: antialiased`

**Layout**
- [ ] Kein Spaltengrid — Textblöcke über `max-width` + `margin-left`
- [ ] Textspalten bei 0 oder exakt 50 % der Contentbreite
- [ ] Sektionen öffnen und schließen mit `--space-4xl` (216 px)
- [ ] Whitespace-Anteil ≥ 60 % der Seitenfläche

**Signature-Effekt**
- [ ] Headline zweimal im DOM (gefüllt + Outline)
- [ ] Outline absolut positioniert, z-index 3, in `@supports` gekapselt
- [ ] Bildobjekt liegt dazwischen (z-index 1 und 2)
- [ ] Bildobjekt überdeckt 20–40 % der Headlinefläche

**Bilder**
- [ ] Freigestellte PNG/WebP mit Alpha, geschlossene Silhouette, gedämpfte Farbigkeit
- [ ] Kein Border-Radius auf Bildern
- [ ] Kein `object-fit` außer beim Full-Bleed-Foto
- [ ] Mindestens ein Objekt pro Sektion angeschnitten, Sektion mit `overflow: hidden`
- [ ] Ladeplatzhalterfarbe hinter dem Full-Bleed-Foto

**Flächen & Effekte**
- [ ] `1px solid` Rahmen, skaliert nicht mit
- [ ] Ein Radiuswert für alle Flächen (`1.2rem`), Buttonradius relativ zur eigenen Schriftgröße
- [ ] **Null** `box-shadow`, **null** `gradient`, **null** `backdrop-filter`
- [ ] Kartenstapel über negative Margins statt Elevation

**Interaktion**
- [ ] Alle Hover-States sind Farbinversionen mit `transition-duration: 0s`
- [ ] Marquee: Liste zweimal im DOM, 60 s linear infinite, `translateX(0 → −50%)`
- [ ] Zweite Marquee-Reihe gegenläufig
- [ ] `animation-play-state: paused` auf Hover ab 992 px
- [ ] Keine Scroll-Reveals, keine Fades, keine Parallax

**Responsive**
- [ ] Einziger echter Breakpoint bei 479 px mit eigenem Multiplikatorsatz
- [ ] Navigation wandert von oben rechts nach unten zentriert
- [ ] 50/50-Splits werden zur Spalte, Sticky wird statisch
- [ ] Buttonreihen werden zum Stack
- [ ] Bei 600 px Viewport nachgemessen: Fließtext ≥ 16 px, Navigation ≥ 14 px

**Barrierefreiheit**
- [ ] `:focus-visible` auf allen interaktiven Elementen
- [ ] `prefers-reduced-motion` stoppt den Marquee
- [ ] Links unterstrichen oder Accent abgedunkelt
- [ ] `@supports`-Kapselung um `-webkit-text-stroke`

---

### Anhang — Quellenlage

| Bereich | Belegt durch | Sicherheit |
|---|---|---|
| Farben, Schriften, Größen, Radien, Rahmen | Stylesheet + Computed Styles | gemessen |
| Layoutmaße, Sektionshöhen, Elementpositionen | `getBoundingClientRect()` @1440/600/375 | gemessen |
| Transitions, Animationen | Computed `transition-duration`, Keyframes | gemessen |
| Fehlen von Scroll-Animationen | HTML-Suche nach IX2-Daten: 0 Treffer | verifiziert |
| Fehlen von Schatten/Verläufen | Vollständige Stylesheet-Suche | verifiziert |
| Skalierungsdefekt 480–767 px | Live-Messung bei 600 px Viewport | verifiziert |
| Team-Karten (`.membercard` etc.) | nur Stylesheet — auf `/` und `/founders` nicht gerendert | **geschätzt** (visueller Zusammenbau) |
| Flächenanteile Text/Bild/Whitespace | Bounding-Box-Rechnung | **geschätzt** |
| Spaltenzahl Team-Grid | nicht ermittelbar | **geschätzt** |
| Cursor-Follow-Bilder im Ticker | CSS vorhanden, JS inaktiv | **geschätzt** |
| Success/Warning/Error | in der Referenz nicht vorhanden | **Erweiterung** |
| Formulare, Inputs, Badges, Tabs | in der Referenz nicht vorhanden | **Erweiterung** |
