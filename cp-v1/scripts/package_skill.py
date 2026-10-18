#!/usr/bin/env python3
"""Empaqueta una skill en .zip para añadirla en Claude (app).

Uso: package_skill.py <ruta-skill> [--salida <carpeta>]
Valida y escanea antes de empaquetar; se detiene si hay errores o secretos.
"""
import argparse
import subprocess
import sys
import zipfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
OMITIR = {".git", "__pycache__", "node_modules", ".DS_Store", "PROGRESO.md"}


def correr(script, ruta):
    r = subprocess.run([sys.executable, str(AQUI / script), str(ruta)])
    return r.returncode == 0


def main():
    p = argparse.ArgumentParser()
    p.add_argument("skill")
    p.add_argument("--salida", default=".")
    a = p.parse_args()
    ruta = Path(a.skill).expanduser().resolve()
    if not correr("validate_skill.py", ruta):
        sys.exit("Validación fallida: corrige los errores antes de empaquetar.")
    if not correr("scan_secrets.py", ruta):
        sys.exit("Escaneo con hallazgos: elimina los datos sensibles antes de empaquetar.")
    salida = Path(a.salida).expanduser().resolve()
    salida.mkdir(parents=True, exist_ok=True)
    destino = salida / f"{ruta.name}.zip"
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(ruta.rglob("*")):
            rel = f.relative_to(ruta)
            if f.is_file() and not (OMITIR & set(rel.parts)) and f.name != ".gitkeep":
                z.write(f, Path(ruta.name) / rel)
    print(f"Paquete creado: {destino}")


if __name__ == "__main__":
    main()
