#!/usr/bin/env bash
# Instala CP V1 y las skills generadas en Claude Code (~/.claude/skills).
# Uso:
#   ./install.sh                 # instala cp-v1 y todas las skills de skills/
#   ./install.sh cp-web-algo     # instala cp-v1 y solo esa skill
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
}

copiar "$RAIZ/cp-v1"

if [ $# -gt 0 ]; then
  for s in "$@"; do copiar "$RAIZ/skills/$s"; done
else
  for d in "$RAIZ"/skills/*/; do [ -d "$d" ] && copiar "${d%/}"; done
fi

echo "Listo. Skills en: $DESTINO (inicia una sesión nueva de Claude Code para cargarlas)."
