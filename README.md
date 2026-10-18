# skill-generator · agent-a

**agent-a** (antes CP V1) es el agente principal de skills para Claude y Claude Code. Hace tres cosas:

1. **Genera** una skill dedicada para cada proyecto, o reutiliza una que ya exista.
2. **Administra** el catálogo: registra, versiona, audita, archiva y publica skills.
3. **Selecciona** en cada momento qué skill o herramienta usar, según la tarea y el historial de uso.

Sirve para cualquier intención: **desarrollar**, **complementar**, **gestionar** o **administrar**.

## Uso rápido

Pídelo con tus palabras o con un atajo:

| Atajo | Qué hace |
|---|---|
| `agent-a nueva <descripción>` | Crea una skill para un proyecto nuevo |
| `agent-a continuar <proyecto>` | Retoma un proyecto desde su `PROGRESO.md` |
| `agent-a usar <skill>` | Trabaja con una skill concreta |
| `agent-a listar` / `buscar <palabras>` | Consulta el catálogo |
| `agent-a auditar` | Revisa errores, duplicados y skills sin uso |
| `agent-a mejorar <skill>` / `archivar <skill>` | Mantenimiento |
| `agent-a publicar [<skill>]` | Valida, escanea y sube a GitHub |
| `agent-a ayuda` | Muestra los atajos y el estado del catálogo |

Ejemplos:
- "agent-a nueva: página web de inventario con PostgreSQL para el curso de Base de Datos"
- "Continúa el proyecto de la tienda web" → encuentra la skill guardada y sigue.

## Flujo

1. Detecta el entorno (Claude Code o app de Claude).
2. Clasifica intención y dominio.
3. **Selecciona**: busca una skill del mismo proyecto o de la misma estructura antes de crear.
4. Propone un borrador y espera tu **autorización** (punto de control 1).
5. Hace hasta 5 preguntas específicas y genera la skill `a-<dominio>-<proyecto>`.
6. Trabaja como agente del proyecto, eligiendo la herramienta adecuada en cada momento.
7. Al cerrar, valida, escanea y **publica con tu confirmación** (punto de control 2).

## Estructura

```
skill-generator/
├── agent-a/
│   ├── SKILL.md                 ← instrucciones principales
│   ├── CHANGELOG.md
│   ├── references/              ← reglas, selección, administración, mejora continua,
│   │                              intenciones, dominios, preguntas, entornos, seguridad, publicación
│   ├── templates/               ← plantillas de SKILL, PROGRESO, CHANGELOG y secciones
│   └── scripts/                 ← new_skill, manage, validate_skill, scan_secrets, package_skill
├── skills/
│   ├── REGISTRO.md              ← índice de skills generadas
│   ├── uso.json                 ← historial de uso (alimenta la selección)
│   └── <nombre>/                ← cada skill generada
├── install.sh
└── README.md
```

## Instalación

### Claude Code

```bash
git clone https://github.com/alex123floresc-sketch/skill-generator.git
cd skill-generator
./install.sh                     # agent-a + todas las skills generadas
./install.sh a-web-mi-proyecto   # agent-a + una skill concreta
```

Se instalan en `~/.claude/skills/`. Para un solo proyecto: `DESTINO=.claude/skills ./install.sh`. Si tenías `cp-v1` instalada, el instalador la retira automáticamente (la mueve, no la borra).

### Claude (app)

1. `python3 agent-a/scripts/package_skill.py agent-a --salida dist`
2. Sube `dist/agent-a.zip` en la sección de skills de la configuración de Claude. Si tenías `cp-v1`, desactívala para que no compitan.

## Herramientas

| Script | Función |
|---|---|
| `new_skill.py` | Crea una skill desde plantillas o la deriva de otra (`--base`) |
| `manage.py` | listar · buscar · seleccionar · registrar · usar · auditar · version · archivar · restaurar |
| `validate_skill.py` | Frontmatter, nombre, descripción, versión y referencias |
| `scan_secrets.py` | Detecta credenciales, tokens y datos personales |
| `package_skill.py` | Valida, escanea y empaqueta en `.zip` |

Solo usan la biblioteca estándar de Python 3.9+.

## Seguridad

- Dos puntos de control: antes de crear y antes de publicar.
- Escaneo de secretos obligatorio; con hallazgos no se publica.
- Nunca se guardan credenciales, `.env` reales, datos personales ni bases de datos reales.
- Las skills no se borran: se archivan. Sin `push --force`.
- agent-a solo se automodifica con mejoras de intuitividad (una por uso, avisando y versionando).

Reglas completas en [`agent-a/references/reglas.md`](agent-a/references/reglas.md) y [`seguridad.md`](agent-a/references/seguridad.md).
