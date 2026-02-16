#!/usr/bin/env bash
set -euo pipefail

# Install runtime dependencies for this Manim project on Ubuntu/Debian.
# Usage:
#   bash scripts/install_deps.sh            # install system + python packages
#   bash scripts/install_deps.sh --check    # only check installed versions

CHECK_ONLY="${1:-}"

check_cmd() {
  local name="$1"
  local cmd="$2"
  if command -v "$cmd" >/dev/null 2>&1; then
    echo "[OK] $name: $($cmd --version 2>/dev/null | head -n 1)"
  else
    echo "[MISSING] $name ($cmd)"
  fi
}

if [[ "$CHECK_ONLY" == "--check" ]]; then
  echo "== Dependency check =="
  check_cmd "Python" "python3"
  check_cmd "pip" "pip"
  check_cmd "Manim" "manim"
  check_cmd "FFmpeg" "ffmpeg"
  check_cmd "LaTeX" "latex"
  check_cmd "dvisvgm" "dvisvgm"
  exit 0
fi

echo "== Installing system dependencies (requires network + sudo/root) =="
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y \
  ffmpeg \
  texlive \
  texlive-latex-extra \
  texlive-fonts-recommended \
  dvisvgm

echo "== Installing Python dependencies =="
python3 -m pip install -U pip
python3 -m pip install manim

echo "== Final check =="
"$0" --check
