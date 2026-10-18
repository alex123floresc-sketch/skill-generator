# skill-generator · CP V1

**CP V1** es una *fábrica de skills* para Claude y Claude Code. Cuando pides un proyecto —desarrollar, complementar, gestionar o administrar cualquier cosa—, CP V1:

1. **Busca** si ya existe una skill para ese proyecto o esa estructura y la reutiliza.
2. Si no existe, **analiza tu pedido**, te propone un borrador y espera tu autorización.
3. Hace **preguntas específicas** (máx. 5 por ronda) para entender el proyecto.
4. **Genera** una skill dedicada con instrucciones, plantillas y scripts.
5. Trabaja como **agente del proyecto**, actualizando la skill cuando aprende algo nuevo.
6. Al cerrar, la **publica en este repositorio** para reutilizarla después.

## Estructura

```
skill-generator/
├── cp-v1/                       ← la fábrica
│   ├── SKILL.md                 ← flujo principal
│   ├── references/              ← intenciones, dominios, preguntas, entornos, seguridad, publicación
│   ├── templates/               ← plantillas de SKILL.md, PROGRESO.md, CHANGELOG.md
│   └── scripts/                 ← new_skill, validate_skill, scan_secrets, registry, package_skill
├── skills/
│   ├── REGISTRO.md              ← índice de skills generadas
│   └── <nombre>/                ← cada skill generada
├── install.sh                   ← instalador para Claude Code
└── README.md
```

## Intenciones

| Intención | Para qué |
|---|---|
| **Desarrollar** | crear software, webs, apps, scripts, bases de datos |
| **Complementar** | mejorar o extender algo que ya existe |
| **Gestionar** | planificar, organizar, dar seguimiento, manejar datos y reportes |
| **Administrar** | operar, mantener y documentar sistemas o procesos |

## Instalación

### Claude Code

```bash
git clone https://github.com/alex123floresc-sketch/skill-generator.git
cd skill-generator
./install.sh                    # cp-v1 + todas las skills generadas
./install.sh cp-web-mi-proyecto # cp-v1 + una skill concreta
```

Se instalan en `~/.claude/skills/`. Para instalarlas solo en un proyecto: `DESTINO=.claude/skills ./install.sh`.

### Claude (app)

1. Empaqueta la skill: `python3 cp-v1/scripts/package_skill.py cp-v1 --salida dist`
2. Sube `dist/cp-v1.zip` en la sección de skills de la configuración de Claude.

## Uso

Pide tu proyecto con normalidad, por ejemplo:

- "Usa CP V1 para desarrollar una página web de inventario con PostgreSQL."
- "Quiero gestionar el conteo de encuestas del curso; crea una skill para este proyecto."
- "Continúa el proyecto de la tienda web" → CP V1 encuentra la skill guardada y sigue desde `PROGRESO.md`.

## Herramientas

| Script | Función |
|---|---|
| `new_skill.py` | Crea una skill nueva desde plantillas, o deriva una de otra existente (`--base`) |
| `validate_skill.py` | Revisa frontmatter, nombre y descripción |
| `scan_secrets.py` | Detecta credenciales, tokens y datos personales |
| `registry.py` | Busca skills existentes y mantiene `skills/REGISTRO.md` |
| `package_skill.py` | Valida, escanea y empaqueta en `.zip` |

Todos usan solo la biblioteca estándar de Python 3.

## Seguridad

- Dos puntos de control obligatorios: antes de crear y antes de publicar.
- Escaneo de secretos antes de empaquetar o subir; si hay hallazgos, no se publica.
- Nunca se guardan credenciales, `.env` reales, datos personales ni bases de datos reales.
- Sin `push --force`; el estado de cada proyecto (`PROGRESO.md`) queda fuera de este repo.

Detalle completo en [`cp-v1/references/seguridad.md`](cp-v1/references/seguridad.md).
