#!/usr/bin/env python3
"""Busca secretos y datos sensibles antes de guardar o publicar.

Uso: scan_secrets.py <ruta> [<ruta> ...]
Sale con código 1 si encuentra algo. Revisa cada hallazgo manualmente:
puede haber falsos positivos (ej. valores de ejemplo).
"""
import re
import sys
from pathlib import Path

PATRONES = [
    ("Clave privada", re.compile(r"-----BEGIN (RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY")),
    ("Token de GitHub", re.compile(r"\b(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}")),
    ("Clave AWS", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Clave de Google API", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("Clave de OpenAI/Anthropic", re.compile(r"\bsk-(ant-)?[A-Za-z0-9_\-]{20,}")),
    ("Token de Slack", re.compile(r"\bxox[abprs]-[A-Za-z0-9\-]{10,}")),
    ("JWT", re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}")),
    ("Cadena de conexión con contraseña", re.compile(r"\b[a-z+]+://[^\s:/@]+:[^\s@/]{3,}@[^\s]+", re.I)),
    ("Asignación de secreto", re.compile(
        r"(?i)\b(password|passwd|contraseña|clave|secret|api[_-]?key|token|access[_-]?key)\b\s*[:=]\s*['\"]?([^\s'\"#]{6,})")),
    ("Correo electrónico", re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b")),
    ("Posible DNI/teléfono (8-9 dígitos)", re.compile(r"(?<![\d.\-])\d{8,9}(?![\d.\-])")),
]

EJEMPLO = re.compile(r"(?i)(example|ejemplo|tu_|your_|xxx|changeme|\.\.\.|<|placeholder|dummy|ficticio)")
CORREOS_PERMITIDOS = re.compile(r"(?i)@(example\.(com|org)|anthropic\.com|users\.noreply\.github\.com)$")
ARCHIVOS_PROHIBIDOS = re.compile(r"(?i)(^|/)(\.env(\..+)?|.*\.(pem|key|p12|pfx|sqlite3?|db|dump|bak))$")
OMITIR_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv"}
EXT_BINARIAS = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".ico", ".woff", ".woff2", ".ttf"}


def archivos(ruta):
    if ruta.is_file():
        yield ruta
        return
    for f in ruta.rglob("*"):
        if f.is_file() and not (OMITIR_DIRS & set(f.parts)):
            yield f


def escanear(f):
    hallazgos = []
    rel = f.as_posix()
    if ARCHIVOS_PROHIBIDOS.search(rel) and not rel.endswith(".env.example"):
        hallazgos.append((0, "Archivo sensible (no debe publicarse)", f.name))
    if f.suffix.lower() in EXT_BINARIAS or f.name == "scan_secrets.py":
        return hallazgos
    try:
        texto = f.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return hallazgos
    for n, linea in enumerate(texto.splitlines(), 1):
        for nombre, patron in PATRONES:
            for m in patron.finditer(linea):
                valor = m.group(0)
                if nombre == "Correo electrónico" and CORREOS_PERMITIDOS.search(valor):
                    continue
                if nombre in ("Asignación de secreto", "Cadena de conexión con contraseña") and EJEMPLO.search(linea):
                    continue
                hallazgos.append((n, nombre, valor[:60]))
    return hallazgos


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    total = 0
    for arg in sys.argv[1:]:
        for f in archivos(Path(arg).expanduser()):
            for n, tipo, valor in escanear(f):
                total += 1
                print(f"{f}:{n}: {tipo}: {valor}")
    if total:
        print(f"\n{total} hallazgo(s). Revísalos y elimínalos antes de publicar.")
        sys.exit(1)
    print("OK: no se encontraron secretos ni datos sensibles.")


if __name__ == "__main__":
    main()
