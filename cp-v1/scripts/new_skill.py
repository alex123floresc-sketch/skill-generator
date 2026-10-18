#!/usr/bin/env python3
"""Crea la estructura de una skill de proyecto a partir de las plantillas de CP V1.

Uso:
  new_skill.py --nombre cp-web-mi-proyecto --intencion desarrollar --dominio web \
               --descripcion "Qué hace y cuándo usarla" --destino ./skills
  new_skill.py --nombre cp-web-otro --base ./skills/cp-web-mi-proyecto --destino ./skills
"""
import argparse
import datetime
import re
import shutil
import sys
from pathlib import Path

INTENCIONES = ("desarrollar", "complementar", "gestionar", "administrar")
NOMBRE_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
RAIZ_CP = Path(__file__).resolve().parent.parent
TEMPLATES = RAIZ_CP / "templates"


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


def validar_nombre(nombre):
    if not NOMBRE_RE.match(nombre) or len(nombre) > 64:
        sys.exit(f"Nombre inválido '{nombre}': usa minúsculas, números y guiones (máx. 64).")
    if "claude" in nombre or "anthropic" in nombre:
        sys.exit("El nombre no puede contener 'claude' ni 'anthropic'.")


def crear_desde_base(args, destino):
    base = Path(args.base)
    if not (base / "SKILL.md").exists():
        sys.exit(f"No se encontró SKILL.md en la base: {base}")
    shutil.copytree(base, destino, ignore=shutil.ignore_patterns("PROGRESO.md", "__pycache__"))
    skill_md = destino / "SKILL.md"
    texto = skill_md.read_text(encoding="utf-8")
    texto = re.sub(r"(?m)^name:.*$", f"name: {args.nombre}", texto, count=1)
    if args.descripcion:
        desc = args.descripcion.replace("\n", " ")
        texto = re.sub(r"(?m)^description:.*$", lambda _: f"description: {desc}", texto, count=1)
    skill_md.write_text(texto, encoding="utf-8")
    hoy = datetime.date.today().isoformat()
    (destino / "CHANGELOG.md").write_text(
        f"# Changelog — {args.nombre}\n\n## v1.0 — {hoy}\n- Derivada de `{base.name}` con CP V1.\n",
        encoding="utf-8",
    )
    print(f"Skill derivada de {base.name}. Revisa y limpia lo específico del proyecto anterior.")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--nombre", required=True)
    p.add_argument("--intencion", choices=INTENCIONES)
    p.add_argument("--dominio", default="otro")
    p.add_argument("--descripcion", default="")
    p.add_argument("--titulo", default="")
    p.add_argument("--destino", required=True, help="Carpeta donde se crea la skill")
    p.add_argument("--base", help="Skill existente para derivar una nueva")
    args = p.parse_args()

    validar_nombre(args.nombre)
    destino = Path(args.destino).expanduser() / args.nombre
    if destino.exists():
        sys.exit(f"Ya existe {destino}. Usa otro nombre o actualiza la skill existente.")

    if args.base:
        crear_desde_base(args, destino)
        print(destino)
        return

    if not args.intencion or not args.descripcion:
        sys.exit("Para una skill nueva se requieren --intencion y --descripcion.")

    hoy = datetime.date.today().isoformat()
    titulo = args.titulo or args.nombre.replace("-", " ").title()
    datos = {
        "NOMBRE": args.nombre,
        "DESCRIPCION": args.descripcion.replace("\n", " "),
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
    (destino / "templates" / "PROGRESO.plantilla.md").write_text(render("PROGRESO.template.md", datos), encoding="utf-8")
    for sub in ("references", "scripts"):
        (destino / sub / ".gitkeep").touch()

    print(destino)


if __name__ == "__main__":
    main()
