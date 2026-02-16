# Mini-projet Manim — Limites (1BAC SM Maroc)

Ce projet contient une vidéo pédagogique Manim Community Edition : **« Limites — formules et méthodes »**.

## Fichiers
- `main.py` : code Manim (scène `VideoLimites`).
- `voiceover_fr.md` : script voix-off en français, synchronisé par scènes.
- `README.md` : installation, rendu et dépannage.

## Dépendances
- **Python** : 3.10+ recommandé.
- **Manim Community Edition** : version récente (ex. `0.18.x` ou plus).
- **LaTeX** (obligatoire pour `MathTex/Tex`) :
  - Distribution TeX (TeX Live / MacTeX / MiKTeX)
  - Outils utilisés par Manim : `latex`, `dvisvgm` (selon plateforme)
- **FFmpeg** (pour l’export vidéo).

## Installation (exemple)

### 1) Créer un environnement virtuel
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows PowerShell
```

### 2) Installer Manim
```bash
pip install -U pip
pip install manim
```

### 3) Vérifier les binaires système
```bash
manim --version
latex --version
dvisvgm --version
ffmpeg -version
```

## Rendu de la vidéo
Commande demandée :
```bash
manim -pqh main.py VideoLimites
```

### Autres variantes utiles
- Qualité basse (rapide) :
```bash
manim -pql main.py VideoLimites
```
- Qualité haute 1080p :
```bash
manim -pqh main.py VideoLimites
```
- Qualité production 4K (long) :
```bash
manim -pqk main.py VideoLimites
```

## Notes pédagogiques intégrées
La vidéo couvre :
1. Introduction et objectifs.
2. Intuition graphique de la limite.
3. Définition niveau bac.
4. Propriétés de calcul (somme, différence, produit, quotient, constante).
5. Limites usuelles et rappel du **Df** + conditions (dénominateur non nul).
6. Méthodes : substitution, factorisation, rationalisation, comparaison des degrés à l’infini.
7. Pièges fréquents.
8. Mini-exercices avec correction.

## Check-list en cas d’erreur LaTeX
Si le rendu échoue sur `MathTex/Tex`, vérifier :
- [ ] `latex` est installé et accessible (`latex --version`).
- [ ] `dvisvgm` est installé (`dvisvgm --version`).
- [ ] Une distribution TeX complète est installée (TeX Live / MiKTeX / MacTeX).
- [ ] Les paquets mathématiques usuels sont présents (install complète recommandée).
- [ ] Le terminal utilisé pour lancer Manim voit bien les binaires TeX (PATH correct).
- [ ] Refaire un test simple :
  ```bash
  manim -pql main.py VideoLimites
  ```

## Remarque
Le script voix-off se trouve dans `voiceover_fr.md` avec des timings approximatifs pour faciliter l’enregistrement et la synchronisation.
