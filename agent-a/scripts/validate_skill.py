#!/usr/bin/env python3
"""Valida una skill: frontmatter, nombre, descripción, versión y estructura.

Uso: validate_skill.py <ruta-skill> [<ruta-skill> ...]
Sale con código 1 si alguna tiene errores. Los avisos no bloquean.
"""
import re
import sys
from pathlib import Path

NOMBRE_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
VERSION_RE = re.compile(r"Versión:\s*\*\*(\d+\.\d+)\*\*")
CHANGELOG_RE = re.compile(r"(?m)^## v(\d+\.\d+)")


def leer_frontmatter(texto):
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", texto, re.S)
    if not m:
        return None
    datos = {}
    for linea in m.group(1).splitlines():
        if ":" in linea and not linea.startswith((" ", "\t")):
            k, v = linea.split(":", 1)
            datos[k.strip()] = v.strip()
    return datos


def version_mayor(versiones):
    return max(versiones, key=lambda s: tuple(map(int, s.split(".")))) if versiones else None


def versiones(ruta):
    """Devuelve (versión del encabezado de SKILL.md, versión más alta del CHANGELOG)."""
    skill = (ruta / "SKILL.md").read_text(encoding="utf-8")
    enc = VERSION_RE.search(skill)
    cl = ruta / "CHANGELOG.md"
    cambios = version_mayor(CHANGELOG_RE.findall(cl.read_text(encoding="utf-8"))) if cl.exists() else None
    return (enc.group(1) if enc else None), cambios


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
        errores.append(f"'name' inválido: {nombre} (minúsculas, números y guiones; máx. 64)")
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
        if ": " in desc and not (desc.startswith('"') or desc.startswith("'")):
            errores.append("'description' contiene ': ' (rompe el YAML); reescríbela o ponla entre comillas")
        if len(desc) < 80:
            avisos.append("'description' muy corta: incluye qué hace y CUÁNDO usarla")

    if "{{" in texto:
        avisos.append("Quedan marcadores {{...}} sin reemplazar en SKILL.md")
    lineas = texto.count("\n")
    if lineas > 500:
        avisos.append(f"SKILL.md tiene {lineas} líneas; mueve detalle a references/")

    if not (ruta / "CHANGELOG.md").exists():
        avisos.append("Falta CHANGELOG.md")
    else:
        enc, cambios = versiones(ruta)
        if enc and cambios and enc != cambios:
            avisos.append(f"Versión desincronizada: SKILL.md dice {enc}, CHANGELOG dice {cambios} (usa manage.py version)")

    for ref in re.findall(r"`((?:references|templates|scripts)/[\w.\-/]+)`", texto):
        if "<" not in ref and not (ruta / ref).exists():
            avisos.append(f"Se menciona {ref} pero no existe")
    return errores, avisos


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    fallo = False
    for arg in sys.argv[1:]:
        ruta = Path(arg).expanduser().resolve()
        errores, avisos = validar(ruta)
        for a in avisos:
            print(f"AVISO [{ruta.name}]: {a}")
        for e in errores:
            print(f"ERROR [{ruta.name}]: {e}")
        if errores:
            fallo = True
        else:
            print(f"OK: {ruta.name} es válida.")
    sys.exit(1 if fallo else 0)


if __name__ == "__main__":
    main()
