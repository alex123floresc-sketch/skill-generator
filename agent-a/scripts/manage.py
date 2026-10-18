#!/usr/bin/env python3
"""Administración del catálogo de skills de agent-a.

Acciones:
  listar      --raiz R                         Catálogo con versión y usos
  buscar      --raiz R [--raiz R2] --texto T   Coincidencias por palabras
  seleccionar --raiz R [--raiz R2] --texto T   Recomienda qué skill usar (palabras + historial)
  registrar   --raiz R --skill S [--copiar] [--reemplazar]   Registra (y opcionalmente copia) una skill
  usar        --raiz R --skill NOMBRE --contexto "3-8 palabras"   Anota un uso
  auditar     --raiz R [--dias 90]             Errores, versiones, solapes, skills sin uso
  version     --skill S --tipo menor|mayor --nota "..."   Sube versión (SKILL.md + CHANGELOG)
  archivar    --raiz R --skill NOMBRE          Mueve a <raiz>/_archivo (no borra)
  restaurar   --raiz R --skill NOMBRE          Devuelve desde _archivo
"""
import argparse
import datetime
import json
import re
import shutil
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_skill import validar, versiones, version_mayor, CHANGELOG_RE  # noqa: E402

ARCHIVO = "_archivo"
USO = "uso.json"
MAX_CONTEXTOS = 10
STOP = set(
    "de la el los las un una unos unas y o a en con por para del al que se su sus es lo como "
    "mas pero sin sobre este esta esto ese esa cuando usala usar use skill proyecto quiero "
    "the and for with to of in on".split()
)
ENCABEZADO = (
    "# Registro de skills\n\n"
    "Índice generado por `agent-a/scripts/manage.py`. No editar a mano.\n\n"
    "| Skill | Versión | Intención | Dominio | Usos | Descripción |\n"
    "|---|---|---|---|---|---|\n"
)


# ---------- utilidades ----------

def normalizar(t):
    t = unicodedata.normalize("NFKD", t.lower())
    return "".join(c for c in t if not unicodedata.combining(c))


def palabras(t):
    return {w for w in re.findall(r"[a-z0-9]+", normalizar(t)) if len(w) > 2 and w not in STOP}


def hoy():
    return datetime.date.today().isoformat()


def info_skill(ruta):
    texto = (ruta / "SKILL.md").read_text(encoding="utf-8")
    nombre = re.search(r"(?m)^name:\s*(.+)$", texto)
    desc = re.search(r"(?m)^description:\s*(.+)$", texto)
    intencion = re.search(r"Intención:\s*\*\*([\w-]+)\*\*", texto)
    dominio = re.search(r"Dominio:\s*\*\*([\w-]+)\*\*", texto)
    enc, cambios = versiones(ruta)
    return {
        "nombre": nombre.group(1).strip() if nombre else ruta.name,
        "descripcion": desc.group(1).strip().strip("\"'") if desc else "",
        "intencion": intencion.group(1) if intencion else "-",
        "dominio": dominio.group(1) if dominio else "-",
        "version": enc or cambios or "1.0",
        "ruta": ruta,
    }


def skills_en(raiz):
    if not raiz.exists():
        return []
    return [info_skill(p.parent) for p in sorted(raiz.glob("*/SKILL.md")) if p.parent.name != ARCHIVO]


def leer_uso(raiz):
    f = raiz / USO
    if f.exists():
        try:
            return json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            print(f"AVISO: {f} está dañado; se ignora el historial.")
    return {}


def guardar_uso(raiz, datos):
    (raiz / USO).write_text(json.dumps(datos, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def escribir_registro(raiz):
    uso = leer_uso(raiz)
    filas = []
    for s in skills_en(raiz):
        desc = s["descripcion"].replace("|", "/")
        desc = desc if len(desc) <= 140 else desc[:137] + "..."
        usos = uso.get(s["nombre"], {}).get("usos", 0)
        filas.append(
            f"| [`{s['nombre']}`]({s['ruta'].name}/) | {s['version']} | {s['intencion']} | "
            f"{s['dominio']} | {usos} | {desc} |"
        )
    (raiz / "REGISTRO.md").write_text(ENCABEZADO + "\n".join(filas) + ("\n" if filas else ""), encoding="utf-8")
    print(f"REGISTRO.md actualizado ({len(filas)} skills).")


def raices(args):
    return [Path(r).expanduser().resolve() for r in args.raiz]


def puntuar(texto, raices_):
    consulta = palabras(texto)
    resultados = []
    for raiz in raices_:
        uso = leer_uso(raiz)
        for s in skills_en(raiz):
            p_nombre = len(consulta & palabras(s["nombre"].replace("-", " "))) * 3
            p_meta = len(consulta & palabras(f"{s['dominio']} {s['intencion']}")) * 2
            p_desc = len(consulta & palabras(s["descripcion"]))
            base = p_nombre + p_meta + p_desc
            h = uso.get(s["nombre"], {})
            p_ctx = len(consulta & palabras(" ".join(h.get("contextos", [])))) * 1.5
            p_freq = min(h.get("usos", 0), 10) * 0.1 if base else 0
            errores, _ = validar(s["ruta"])
            total = base + p_ctx + p_freq - (2 if errores else 0)
            if total > 0:
                resultados.append((round(total, 1), s, h))
    resultados.sort(key=lambda x: (-x[0], x[1]["nombre"]))
    return resultados


# ---------- acciones ----------

def accion_listar(args):
    for raiz in raices(args):
        uso = leer_uso(raiz)
        lista = skills_en(raiz)
        print(f"# {raiz} ({len(lista)} skills)")
        for s in lista:
            h = uso.get(s["nombre"], {})
            print(f"- {s['nombre']} v{s['version']} ({s['intencion']}/{s['dominio']}) "
                  f"usos={h.get('usos', 0)} último={h.get('ultimo', '-')}")
        archivadas = sorted(p.parent.name for p in (raiz / ARCHIVO).glob("*/SKILL.md")) if (raiz / ARCHIVO).exists() else []
        if archivadas:
            print(f"  Archivadas: {', '.join(archivadas)}")


def accion_buscar(args):
    if not args.texto:
        sys.exit("Indica --texto")
    res = puntuar(args.texto, raices(args))
    if not res:
        print("Sin coincidencias.")
        return
    for pts, s, _ in res:
        print(f"[{pts}] {s['nombre']} v{s['version']} ({s['intencion']}/{s['dominio']}) -> {s['ruta']}")
        print(f"     {s['descripcion'][:160]}")


def accion_seleccionar(args):
    if not args.texto:
        sys.exit("Indica --texto")
    res = puntuar(args.texto, raices(args))
    if not res or res[0][0] < 2:
        print("RECOMENDACIÓN: crear una skill nueva (no hay coincidencias suficientes).")
        for pts, s, _ in res[:3]:
            print(f"  débil [{pts}] {s['nombre']}")
        return
    top = res[0]
    segundo = res[1][0] if len(res) > 1 else 0
    if top[0] >= 2 * segundo:
        print(f"RECOMENDACIÓN: usar {top[1]['nombre']} v{top[1]['version']} [{top[0]}] -> {top[1]['ruta']}")
    else:
        print("RECOMENDACIÓN: preguntar al usuario entre estas candidatas:")
    for pts, s, h in res[:3]:
        print(f"  [{pts}] {s['nombre']} ({s['intencion']}/{s['dominio']}) usos={h.get('usos', 0)} — {s['descripcion'][:110]}")


def accion_registrar(args):
    raiz = raices(args)[0]
    raiz.mkdir(parents=True, exist_ok=True)
    if not args.skill:
        sys.exit("Indica --skill")
    skill = Path(args.skill).expanduser().resolve()
    if not (skill / "SKILL.md").exists():
        sys.exit(f"No hay SKILL.md en {skill}")
    errores, _ = validar(skill)
    if errores:
        sys.exit("La skill tiene errores de validación:\n- " + "\n- ".join(errores))
    if skill.parent != raiz:
        if not args.copiar:
            print(f"AVISO: {skill.name} no está en {raiz}; usa --copiar para incluirla en el registro.")
        else:
            destino = raiz / skill.name
            if destino.exists():
                if not args.reemplazar:
                    sys.exit(f"{destino} ya existe. Confirma con el usuario y repite con --reemplazar.")
                shutil.rmtree(destino)
            shutil.copytree(skill, destino, ignore=shutil.ignore_patterns("PROGRESO.md", "__pycache__", "*.pyc", "*.zip"))
            print(f"Copiada a {destino}")
    escribir_registro(raiz)


def accion_usar(args):
    raiz = raices(args)[0]
    if not args.skill:
        sys.exit("Indica --skill con el nombre de la skill")
    if not (raiz / args.skill / "SKILL.md").exists():
        sys.exit(f"No existe {args.skill} en {raiz}")
    uso = leer_uso(raiz)
    h = uso.setdefault(args.skill, {"usos": 0, "contextos": []})
    h["usos"] = h.get("usos", 0) + 1
    h["ultimo"] = hoy()
    ctx = " ".join((args.contexto or "").split())[:80]
    if ctx:
        h["contextos"] = ([c for c in h.get("contextos", []) if c != ctx] + [ctx])[-MAX_CONTEXTOS:]
    guardar_uso(raiz, uso)
    print(f"Uso registrado: {args.skill} (total {h['usos']}).")


def accion_auditar(args):
    raiz = raices(args)[0]
    lista = skills_en(raiz)
    uso = leer_uso(raiz)
    limite = datetime.date.today() - datetime.timedelta(days=args.dias)
    hallazgos = 0
    print(f"# Auditoría de {raiz} ({len(lista)} skills)")
    for s in lista:
        errores, avisos = validar(s["ruta"])
        for e in errores:
            print(f"ERROR   {s['nombre']}: {e}"); hallazgos += 1
        for a in avisos:
            print(f"AVISO   {s['nombre']}: {a}"); hallazgos += 1
        h = uso.get(s["nombre"])
        if not h:
            print(f"SIN USO {s['nombre']}: nunca registrada con 'usar'"); hallazgos += 1
        elif h.get("ultimo") and datetime.date.fromisoformat(h["ultimo"]) < limite:
            print(f"INACTIVA {s['nombre']}: último uso {h['ultimo']} (> {args.dias} días); ¿archivar?"); hallazgos += 1
    for i, a in enumerate(lista):
        pa = palabras(a["descripcion"])
        for b in lista[i + 1:]:
            pb = palabras(b["descripcion"])
            if pa and pb:
                jac = len(pa & pb) / len(pa | pb)
                if jac >= 0.6:
                    print(f"SOLAPE  {a['nombre']} ~ {b['nombre']} ({jac:.0%}): diferenciar descripciones o fusionar")
                    hallazgos += 1
    huerfanos = set(uso) - {s["nombre"] for s in lista}
    for n in sorted(huerfanos):
        print(f"AVISO   uso.json menciona '{n}', que no está en el catálogo activo"); hallazgos += 1
    print(f"\n{hallazgos} hallazgo(s)." if hallazgos else "\nTodo en orden.")


def accion_version(args):
    if not args.skill or not args.tipo or not args.nota:
        sys.exit("Indica --skill, --tipo (menor|mayor) y --nota")
    ruta = Path(args.skill).expanduser().resolve()
    skill_md, cl = ruta / "SKILL.md", ruta / "CHANGELOG.md"
    if not skill_md.exists():
        sys.exit(f"No hay SKILL.md en {ruta}")
    enc, cambios = versiones(ruta)
    actual = version_mayor([v for v in (enc, cambios) if v]) or "1.0"
    may, men = map(int, actual.split("."))
    nueva = f"{may + 1}.0" if args.tipo == "mayor" else f"{may}.{men + 1}"

    texto = skill_md.read_text(encoding="utf-8")
    if re.search(r"Versión:\s*\*\*\d+\.\d+\*\*", texto):
        texto = re.sub(r"Versión:\s*\*\*\d+\.\d+\*\*", f"Versión: **{nueva}**", texto, count=1)
        skill_md.write_text(texto, encoding="utf-8")
    else:
        print("AVISO: SKILL.md no tiene encabezado 'Versión: **X.Y**'; solo se actualiza el CHANGELOG.")

    entrada = f"## v{nueva} — {hoy()}\n- {' '.join(args.nota.split())}\n\n"
    if cl.exists():
        cl_txt = cl.read_text(encoding="utf-8")
        m = CHANGELOG_RE.search(cl_txt)
        cl_txt = cl_txt[:m.start()] + entrada + cl_txt[m.start():] if m else cl_txt.rstrip() + "\n\n" + entrada
    else:
        cl_txt = f"# Changelog — {ruta.name}\n\n" + entrada
    cl.write_text(cl_txt, encoding="utf-8")
    print(f"{ruta.name}: v{actual} -> v{nueva}")


def mover(origen, destino, verbo):
    if not origen.exists():
        sys.exit(f"No existe {origen}")
    if destino.exists():
        sys.exit(f"Ya existe {destino}; resuélvelo con el usuario antes de {verbo}.")
    destino.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(origen), str(destino))


def accion_archivar(args):
    raiz = raices(args)[0]
    mover(raiz / args.skill, raiz / ARCHIVO / args.skill, "archivar")
    print(f"Archivada: {args.skill} (en {ARCHIVO}/; no se borró)")
    escribir_registro(raiz)


def accion_restaurar(args):
    raiz = raices(args)[0]
    mover(raiz / ARCHIVO / args.skill, raiz / args.skill, "restaurar")
    print(f"Restaurada: {args.skill}")
    escribir_registro(raiz)


ACCIONES = {
    "listar": accion_listar, "buscar": accion_buscar, "seleccionar": accion_seleccionar,
    "registrar": accion_registrar, "usar": accion_usar, "auditar": accion_auditar,
    "version": accion_version, "archivar": accion_archivar, "restaurar": accion_restaurar,
}


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("accion", choices=ACCIONES)
    p.add_argument("--raiz", action="append", default=[], help="Carpeta de skills (repetible en buscar/seleccionar)")
    p.add_argument("--texto", default="")
    p.add_argument("--skill")
    p.add_argument("--contexto", default="")
    p.add_argument("--copiar", action="store_true")
    p.add_argument("--reemplazar", action="store_true")
    p.add_argument("--dias", type=int, default=90)
    p.add_argument("--tipo", choices=("menor", "mayor"))
    p.add_argument("--nota", default="")
    a = p.parse_args()
    if a.accion != "version" and not a.raiz:
        sys.exit("Indica --raiz")
    if a.accion in ("archivar", "restaurar") and not a.skill:
        sys.exit("Indica --skill")
    ACCIONES[a.accion](a)


if __name__ == "__main__":
    main()
