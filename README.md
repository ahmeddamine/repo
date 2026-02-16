# Mini-projet Manim CE — Limites d’une fonction (1BAC SM, Maroc BIOF)

Ce mini-projet produit une vidéo pédagogique complète avec Manim Community Edition.

## Fichiers
- `main.py` : scène Manim `VideoLimites` (13 scènes pédagogiques).
- `voiceover_fr.md` : voix-off en français avec timings approximatifs.
- `README.md` : installation, rendu et dépannage.

## Dépendances
- Python **3.10+** recommandé.
- Manim Community Edition.
- FFmpeg.
- LaTeX (obligatoire pour `MathTex`):
  - Linux: **TeX Live**
  - Windows: **MiKTeX**
  - macOS: MacTeX
- Binaire `dvisvgm` (utilisé par Manim pour convertir la sortie LaTeX).

---

## Installation rapide

### 1) Environnement Python
```bash
python -m venv .venv
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
```

### 2) Installer Manim
```bash
pip install -U pip
pip install manim
```

### 3) Vérifier les outils système
```bash
manim --version
ffmpeg -version
latex --version
dvisvgm --version
```

---


## Installation automatisée (script)

Un script est fourni pour installer les dépendances sur Ubuntu/Debian:

```bash
bash scripts/install_deps.sh
```

Mode vérification uniquement:

```bash
bash scripts/install_deps.sh --check
```

## Commande de rendu (demandée)
```bash
manim -pqh main.py VideoLimites
```

Autres options:
```bash
manim -pql main.py VideoLimites   # rendu rapide (low)
manim -pqk main.py VideoLimites   # qualité très haute (4K)
```

---

## Dépannage LaTeX (MiKTeX / TeX Live)

Si `MathTex` échoue au rendu:

1. Vérifier que `latex` est disponible:
   ```bash
   latex --version
   ```
2. Vérifier `dvisvgm`:
   ```bash
   dvisvgm --version
   ```
3. Installer une distribution complète:
   - **Windows**: installer MiKTeX, autoriser l’installation automatique des packages.
   - **Linux**: installer TeX Live complet (ou au minimum paquets latex + dvisvgm).
4. Vérifier la variable `PATH` (terminal redémarré après installation).
5. Refaire un test simple:
   ```bash
   manim -pql main.py VideoLimites
   ```

### Exemple paquets Linux (Debian/Ubuntu)
```bash
sudo apt update
sudo apt install -y ffmpeg texlive texlive-latex-extra texlive-fonts-recommended dvisvgm
```

---

## Notes pédagogiques couvertes
- Définition intuitive de la limite et lecture graphique.
- Limite à gauche / à droite.
- Cas du trou (limite existante sans valeur au point).
- Propriétés de calcul (somme, différence, produit par constante, produit, quotient avec condition).
- Limites usuelles.
- Méthodes: factorisation-simplification (0/0), rationalisation.
- Limites à l’infini (polynôme et rationnelle par division dominante).
- Pièges fréquents + exercices corrigés.
