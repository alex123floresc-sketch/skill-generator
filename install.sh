#!/usr/bin/env bash
# Instala agent-a y las skills generadas en Claude Code (~/.claude/skills).
# Uso:
#   ./install.sh                     # instala agent-a y todas las skills de skills/
#   ./install.sh a-web-algo          # instala agent-a y solo esa skill
#   DESTINO=.claude/skills ./install.sh   # instalar como skills del proyecto
set -euo pipefail

RAIZ="$(cd "$(dirname "$0")" && pwd)"
DESTINO="${DESTINO:-$HOME/.claude/skills}"
mkdir -p "$DESTINO"

copiar() {
  local origen="$1" nombre
  nombre="$(basename "$origen")"
  if [ ! -f "$origen/SKILL.md" ]; then
    echo "Omitido (sin SKILL.md): $nombre"; return
  fi
  if [ -d "$DESTINO/$nombre" ]; then
    echo "Actualizando: $nombre"
    rm -rf "${DESTINO:?}/$nombre"
  else
    echo "Instalando:   $nombre"
  fi
  cp -R "$origen" "$DESTINO/$nombre"
  rm -rf "$DESTINO/$nombre/__pycache__" "$DESTINO/$nombre/scripts/__pycache__"
}

# La versión anterior (cp-v1) se retira sin borrarla, para que no compita con agent-a.
if [ -d "$DESTINO/cp-v1" ]; then
  RETIRO="$(dirname "$DESTINO")/skills-archivo"
  mkdir -p "$RETIRO"
  mv "$DESTINO/cp-v1" "$RETIRO/cp-v1-$(date +%Y%m%d%H%M%S)"
  echo "Retirada:     cp-v1 (movida a $RETIRO)"
fi

copiar "$RAIZ/agent-a"

if [ $# -gt 0 ]; then
  for s in "$@"; do copiar "$RAIZ/skills/$s"; done
else
  for d in "$RAIZ"/skills/*/; do
    [ -d "$d" ] || continue
    [ "$(basename "$d")" = "_archivo" ] && continue
    copiar "${d%/}"
  done
fi

echo "Listo. Skills en: $DESTINO (inicia una sesión nueva de Claude Code para cargarlas)."
