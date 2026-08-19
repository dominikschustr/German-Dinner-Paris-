#!/bin/bash
# Ein Befehl von der Aenderung zur Live-Seite.
#
#   ./deploy.sh              nimmt eine Standard-Commitnachricht
#   ./deploy.sh "Text hier"  nimmt deine
#
# Setzt voraus, dass "git push" ohne Rueckfrage laeuft — also ein
# hinterlegter SSH-Schluessel. Solange das nicht eingerichtet ist,
# bricht das Skript beim Push ab und du laedst docs/ von Hand hoch.

set -e
cd "$(dirname "$0")"

echo "→ docs/ neu bauen"
python3 build.py

if git diff --quiet && git diff --cached --quiet; then
  echo "→ nichts geaendert, nichts zu tun"
  exit 0
fi

echo "→ committen"
git add -A
git commit -q -m "${1:-Website aktualisiert}"

echo "→ zu GitHub schieben"
git push -q origin main

echo
echo "Fertig. GitHub Pages baut jetzt neu, das dauert ein bis zwei Minuten:"
echo "https://dominikschustr.github.io/german-dinner-paris/"
