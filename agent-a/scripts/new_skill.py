#!/usr/bin/env python3
"""Crea la estructura de una skill de proyecto con las plantillas de agent-a.

Uso:
  new_skill.py --nombre a-web-mi-proyecto --intencion desarrollar --dominio web \
               --descripcion "Qué hace y cuándo usarla" --destino ./skills
  new_skill.py --nombre a-web-otro --base ./skills/a-web-mi-proyecto \
               --descripcion "Nueva descripción" --destino ./skills

Al terminar imprime la ruta de la skill creada.
"""
import argparse
import datetime
import re
import shutil
import sys
from pathlib import Path

INTENCIONES = ("desarrollar", "complementar", "gestionar", "administrar")
DOMINIOS = ("datos", "web", "soft", "bd", "acad", "gest", "sis", "dis", "gen")
NOMBRE_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
RAIZ_AGENTE = Path(__file__).resolve().parent.parent
TEMPLATES = RAIZ_AGENTE / "templates"


def leer_secciones():
    texto = (TEMPLATES / "secciones-intencion.md").read_text(encoding="utf-8")
    bloques, actual = {}, None
    for linea in texto.splitlines():
        if linea.startswith("@@ "):
            actual = linea[3:].strip()
            bloques[actual] = []
        elif actual:
            bloques[actual].append(linea)
    return {k: "\n".join(v).strip() for k, v in bloques.items()}


def render(plantilla, datos):
    texto = (TEMPLATES / plantilla).read_text(encoding="utf-8")
    for clave, valor in datos.items():
        texto = texto.replace("{{" + clave + "}}", valor)
    return texto


def limpiar_descripcion(desc):
    desc = " ".join(desc.split())
    if ": " in desc:
        desc = desc.replace(": ", " — ")
        print("AVISO: se reemplazó ': ' por ' — ' en la descripción para no romper el YAML.")
    if "<" in desc or ">" in desc:
        sys.exit("La descripción no puede contener < ni >.")
    if len(desc) > 1024:
        sys.exit(f"La descripción supera 1024 caracteres ({len(desc)}).")
    return desc


def validar_nombre(nombre):
    if not NOMBRE_RE.match(nombre) or len(nombre) > 64:
        sys.exit(f"Nombre inválido '{nombre}': usa minúsculas, números y guiones (máx. 64).")
    if "claude" in nombre or "anthropic" in nombre:
        sys.exit("El nombre no puede contener 'claude' ni 'anthropic'.")
    if not nombre.startswith("a-"):
        print(f"AVISO: '{nombre}' no sigue la convención a-<dominio>-<proyecto>.")


def crear_desde_base(args, destino, desc):
    base = Path(args.base).expanduser().resolve()
    if not (base / "SKILL.md").exists():
        sys.exit(f"No se encontró SKILL.md en la base: {base}")
    shutil.copytree(base, destino, ignore=shutil.ignore_patterns("PROGRESO.md", "__pycache__", "*.pyc"))
    skill_md = destino / "SKILL.md"
    texto = skill_md.read_text(encoding="utf-8")
    texto = re.sub(r"(?m)^name:.*$", lambda _: f"name: {args.nombre}", texto, count=1)
    texto = re.sub(r"(?m)^description:.*$", lambda _: f"description: {desc}", texto, count=1)
    texto = re.sub(r"Versión:\s*\*\*\d+\.\d+\*\*", "Versión: **1.0**", texto, count=1)
    skill_md.write_text(texto, encoding="utf-8")
    hoy = datetime.date.today().isoformat()
    (destino / "CHANGELOG.md").write_text(
        f"# Changelog — {args.nombre}\n\n"
        "Formato: `vMAYOR.MENOR` — MENOR para ajustes, MAYOR para cambios de estructura o de fase.\n\n"
        f"## v1.0 — {hoy}\n- Derivada de `{base.name}` con agent-a.\n",
        encoding="utf-8",
    )
    print(f"Skill derivada de {base.name}. Revisa y limpia lo específico del proyecto anterior.")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--nombre", required=True)
    p.add_argument("--intencion", choices=INTENCIONES)
    p.add_argument("--dominio", default="gen")
    p.add_argument("--descripcion", required=True, help="Qué hace, para qué proyecto y cuándo usarla")
    p.add_argument("--titulo", default="")
    p.add_argument("--destino", required=True, help="Carpeta donde se crea la skill")
    p.add_argument("--base", help="Skill existente de la que derivar la nueva")
    args = p.parse_args()

    validar_nombre(args.nombre)
    desc = limpiar_descripcion(args.descripcion)
    if args.dominio not in DOMINIOS:
        print(f"AVISO: dominio '{args.dominio}' no es estándar ({', '.join(DOMINIOS)}).")
    destino = Path(args.destino).expanduser().resolve() / args.nombre
    if destino.exists():
        sys.exit(f"Ya existe {destino}. Usa otro nombre o actualiza la skill existente.")
    destino.parent.mkdir(parents=True, exist_ok=True)

    if args.base:
        crear_desde_base(args, destino, desc)
        print(destino)
        return

    if not args.intencion:
        sys.exit(f"Para una skill nueva indica --intencion ({', '.join(INTENCIONES)}).")

    hoy = datetime.date.today().isoformat()
    titulo = args.titulo or args.nombre.removeprefix("a-").replace("-", " ").title()
    datos = {
        "NOMBRE": args.nombre,
        "DESCRIPCION": desc,
        "TITULO": titulo,
        "INTENCION": args.intencion,
        "DOMINIO": args.dominio,
        "FECHA": hoy,
        "SECCIONES_INTENCION": leer_secciones().get(args.intencion, ""),
    }

    for sub in ("references", "templates", "scripts"):
        (destino / sub).mkdir(parents=True, exist_ok=True)
    (destino / "SKILL.md").write_text(render("SKILL.template.md", datos), encoding="utf-8")
    (destino / "CHANGELOG.md").write_text(render("CHANGELOG.template.md", datos), encoding="utf-8")
    (destino / "templates" / "PROGRESO.plantilla.md").write_text(
        render("PROGRESO.template.md", datos), encoding="utf-8")
    for sub in ("references", "scripts"):
        (destino / sub / ".gitkeep").touch()

    print(destino)


if __name__ == "__main__":
    main()
