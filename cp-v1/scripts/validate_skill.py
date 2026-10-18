#!/usr/bin/env python3
"""Valida la estructura de una skill: frontmatter, nombre y descripción.

Uso: validate_skill.py <ruta-skill>
Sale con código 1 si hay errores.
"""
import re
import sys
from pathlib import Path

NOMBRE_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def leer_frontmatter(texto):
    m = re.match(r"^---\n(.*?)\n---\n", texto, re.S)
    if not m:
        return None
    datos = {}
    for linea in m.group(1).splitlines():
        if ":" in linea and not linea.startswith(" "):
            k, v = linea.split(":", 1)
            datos[k.strip()] = v.strip()
    return datos


def validar(ruta):
    errores, avisos = [], []
    skill_md = ruta / "SKILL.md"
    if not skill_md.exists():
        return [f"Falta {skill_md}"], avisos
    texto = skill_md.read_text(encoding="utf-8")
    fm = leer_frontmatter(texto)
    if fm is None:
        return ["SKILL.md no empieza con frontmatter YAML (--- ... ---)"], avisos

    nombre = fm.get("name", "")
    desc = fm.get("description", "")
    if not nombre:
        errores.append("Falta 'name' en el frontmatter")
    elif not NOMBRE_RE.match(nombre) or len(nombre) > 64:
        errores.append(f"'name' inválido: {nombre} (minúsculas, números, guiones, máx. 64)")
    elif nombre != ruta.name:
        avisos.append(f"'name' ({nombre}) no coincide con la carpeta ({ruta.name})")
    if any(p in nombre for p in ("claude", "anthropic")):
        errores.append("'name' no puede contener 'claude' ni 'anthropic'")

    if not desc:
        errores.append("Falta 'description' en el frontmatter")
    else:
        if len(desc) > 1024:
            errores.append(f"'description' supera 1024 caracteres ({len(desc)})")
        if "<" in desc or ">" in desc:
            errores.append("'description' no debe contener < ni >")
        if len(desc) < 80:
            avisos.append("'description' muy corta: incluye qué hace y CUÁNDO usarla")

    if "{{" in texto:
        avisos.append("Quedan marcadores {{...}} sin reemplazar en SKILL.md")
    lineas = texto.count("\n")
    if lineas > 500:
        avisos.append(f"SKILL.md tiene {lineas} líneas; mueve detalle a references/")
    if not (ruta / "CHANGELOG.md").exists():
        avisos.append("Falta CHANGELOG.md")
    return errores, avisos


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    ruta = Path(sys.argv[1]).expanduser().resolve()
    errores, avisos = validar(ruta)
    for a in avisos:
        print(f"AVISO: {a}")
    for e in errores:
        print(f"ERROR: {e}")
    if errores:
        sys.exit(1)
    print(f"OK: {ruta.name} es válida.")


if __name__ == "__main__":
    main()
