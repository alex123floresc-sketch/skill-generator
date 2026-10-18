#!/usr/bin/env python3
"""Registro de skills generadas (REGISTRO.md) y búsqueda de skills existentes.

Uso:
  registry.py buscar  --raiz <carpeta-de-skills> --texto "palabras clave"
  registry.py agregar --raiz <carpeta-de-skills> --skill <ruta-skill>
  registry.py listar  --raiz <carpeta-de-skills>
"""
import argparse
import re
import sys
import unicodedata
from pathlib import Path

ENCABEZADO = (
    "# Registro de skills\n\n"
    "Skills generadas con CP V1. Este archivo lo mantiene `cp-v1/scripts/registry.py`.\n\n"
    "| Skill | Versión | Intención | Dominio | Descripción |\n"
    "|---|---|---|---|---|\n"
)


def normalizar(t):
    t = unicodedata.normalize("NFKD", t.lower())
    return "".join(c for c in t if not unicodedata.combining(c))


def info_skill(ruta):
    texto = (ruta / "SKILL.md").read_text(encoding="utf-8")
    nombre = re.search(r"(?m)^name:\s*(.+)$", texto)
    desc = re.search(r"(?m)^description:\s*(.+)$", texto)
    intencion = re.search(r"Intención:\s*\*\*(\w+)\*\*", texto)
    dominio = re.search(r"Dominio:\s*\*\*([\w-]+)\*\*", texto)
    version = "1.0"
    cl = ruta / "CHANGELOG.md"
    if cl.exists():
        v = re.findall(r"(?m)^## v(\d+\.\d+)", cl.read_text(encoding="utf-8"))
        if v:
            version = max(v, key=lambda s: tuple(map(int, s.split("."))))
    return {
        "nombre": nombre.group(1).strip() if nombre else ruta.name,
        "descripcion": desc.group(1).strip() if desc else "",
        "intencion": intencion.group(1) if intencion else "-",
        "dominio": dominio.group(1) if dominio else "-",
        "version": version,
        "ruta": ruta,
    }


def skills_en(raiz):
    return [info_skill(p.parent) for p in sorted(raiz.glob("*/SKILL.md"))]


def buscar(raiz, texto):
    palabras = [p for p in normalizar(texto).split() if len(p) > 2]
    resultados = []
    for s in skills_en(raiz):
        bolsa = normalizar(f"{s['nombre']} {s['descripcion']} {s['dominio']} {s['intencion']}")
        puntaje = sum(1 for p in palabras if p in bolsa)
        if puntaje:
            resultados.append((puntaje, s))
    resultados.sort(key=lambda x: -x[0])
    if not resultados:
        print("Sin coincidencias.")
        return
    for puntaje, s in resultados:
        print(f"[{puntaje}] {s['nombre']} v{s['version']} ({s['intencion']}/{s['dominio']}) -> {s['ruta']}")
        print(f"     {s['descripcion'][:160]}")


def escribir_registro(raiz):
    filas = []
    for s in skills_en(raiz):
        desc = s["descripcion"].replace("|", "/")
        if len(desc) > 140:
            desc = desc[:137] + "..."
        filas.append(f"| [`{s['nombre']}`]({s['ruta'].name}/) | {s['version']} | {s['intencion']} | {s['dominio']} | {desc} |")
    (raiz / "REGISTRO.md").write_text(ENCABEZADO + "\n".join(filas) + ("\n" if filas else ""), encoding="utf-8")
    print(f"REGISTRO.md actualizado ({len(filas)} skills).")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("accion", choices=("buscar", "agregar", "listar"))
    p.add_argument("--raiz", required=True)
    p.add_argument("--texto", default="")
    p.add_argument("--skill")
    a = p.parse_args()
    raiz = Path(a.raiz).expanduser().resolve()
    raiz.mkdir(parents=True, exist_ok=True)

    if a.accion == "buscar":
        if not a.texto:
            sys.exit("Indica --texto")
        buscar(raiz, a.texto)
    elif a.accion == "agregar":
        if not a.skill or not (Path(a.skill) / "SKILL.md").exists():
            sys.exit("Indica --skill con una carpeta que contenga SKILL.md")
        skill = Path(a.skill).expanduser().resolve()
        if skill.parent != raiz:
            print(f"AVISO: la skill no está dentro de {raiz}; cópiala ahí para que aparezca en el registro.")
        escribir_registro(raiz)
    else:
        for s in skills_en(raiz):
            print(f"{s['nombre']} v{s['version']} ({s['intencion']}/{s['dominio']})")


if __name__ == "__main__":
    main()
