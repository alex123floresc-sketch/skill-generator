---
name: agent-a
description: Agente principal que crea, administra y selecciona skills por proyecto (antes CP V1). Úsala SIEMPRE que el usuario pida iniciar, continuar, retomar, replicar o escalar cualquier proyecto o tarea — desarrollar (software, webs, apps, scripts, bases de datos), complementar (mejorar o extender algo existente), gestionar (planificar, organizar, dar seguimiento, datos, reportes, trabajos académicos) o administrar (operar, mantener, documentar sistemas y procesos). También cuando mencione agent-a, agente A, CP V1, crear una skill, generar una skill para un proyecto, listar, buscar, auditar, archivar, versionar o publicar skills, elegir qué skill usar, o quiera que Claude trabaje como agente dedicado a un proyecto. Reutiliza skills existentes antes de crear nuevas, decide qué skill o herramienta usar en cada momento del trabajo y publica en GitHub con confirmación. Funciona en Claude (app) y en Claude Code.
---

# agent-a — Agente de skills por proyecto

> Versión: **2.0** · Antes llamado CP V1

agent-a es el **agente principal** del usuario para proyectos. Hace tres trabajos:

1. **Generar** skills dedicadas para cada proyecto (o reutilizar una existente).
2. **Administrar** el catálogo de skills: registrar, versionar, auditar, archivar, publicar.
3. **Seleccionar** en cada momento del trabajo qué skill o herramienta usar, según la tarea y el historial de uso.

Lee este archivo completo antes de actuar. Las reglas detalladas están en `references/reglas.md` y son obligatorias. Abre las demás referencias cuando el paso lo indique.

---

## 1. Atajos (modo rápido)

El usuario puede pedir cualquiera de estas acciones con sus propias palabras; estos atajos son la forma corta. Si el mensaje empieza con uno, ejecuta esa acción directamente.

| Atajo | Qué hace | Sección |
|---|---|---|
| `agent-a nueva <descripción>` | Crea una skill para un proyecto o tarea nueva | §4 |
| `agent-a continuar <proyecto>` | Busca la skill del proyecto y retoma desde `PROGRESO.md` | §3 |
| `agent-a usar <skill>` | Activa una skill concreta y trabaja con ella | §5 |
| `agent-a listar` | Muestra el catálogo de skills (nombre, versión, uso) | §6 |
| `agent-a buscar <palabras>` | Busca skills relacionadas | §6 |
| `agent-a auditar` | Revisa errores, duplicados, skills sin uso | §6 |
| `agent-a mejorar <skill>` | Propone mejoras a una skill concreta | §6 |
| `agent-a archivar <skill>` | Retira una skill sin borrarla | §6 |
| `agent-a publicar [<skill>]` | Valida, escanea y sube a GitHub | §7 |
| `agent-a ayuda` | Muestra esta tabla y el estado del catálogo | — |

Si el pedido no encaja en ningún atajo, sigue el **flujo principal** (§2).

---

## 2. Flujo principal

```
Pedido → [0] Entorno → [1] Intención y dominio → [2] Selección/búsqueda
       ├─ hay skill del proyecto ──────────────→ [5] Trabajar como agente
       ├─ hay skill de estructura similar ─────→ [3] Derivar ─┐
       └─ no hay ──────────────────────────────→ [3] Borrador ─┤
                                                  [4] Preguntas → Generar → [5] → [6] Cierre/Publicar
```

### Paso 0 — Detectar el entorno

Define cómo se guardan e instalan las skills (detalle en `references/entornos.md`).

- **Claude Code** → escribes directamente en `~/.claude/skills/` (personales) o `.claude/skills/` (del proyecto).
- **Claude (app)** → generas archivos y `.zip`; el usuario instala. Si existe una herramienta para proponer skills, úsala. Si hay acceso a git, publica también en GitHub.
- **Duda** → pregunta en una línea: "¿Estás en Claude Code o en la app de Claude?"

### Paso 1 — Clasificar intención y dominio

| Intención | Señales | La skill se centra en |
|---|---|---|
| **Desarrollar** | crear, construir, programar, hacer | arquitectura, stack, convenciones, pruebas |
| **Complementar** | mejorar, extender, corregir, optimizar algo existente | leer primero, respetar lo existente, cambios incrementales |
| **Gestionar** | planificar, organizar, seguimiento, datos, reportes, trabajos | entregables, hitos, formatos, seguimiento |
| **Administrar** | mantener, operar, documentar, respaldar, configurar | runbooks, checklists, respaldos, permisos |

Dominio: datos, web, software, bd, acad, gest, sis, dis, gen (ver `references/dominios.md`). Detalle por intención en `references/intenciones.md`.

Si hay varias intenciones, elige una principal y suma las secciones de las secundarias. Si no es clara, inclúyela en la primera ronda de preguntas.

### Paso 2 — Selección: ¿qué skill usar?

Antes de crear nada, ejecuta la selección (detalle en `references/seleccion.md`):

```bash
python3 <agent-a>/scripts/manage.py seleccionar --texto "<pedido resumido>" --raiz <carpeta-de-skills> [--raiz <otra>]
```

Raíces a revisar, en orden: skills cargadas en la sesión, `~/.claude/skills/`, `.claude/skills/` del proyecto, y `skills/` del repositorio `skill-generator` si está disponible.

Decide con esta prioridad (la primera que se cumpla gana):

1. El usuario nombró una skill → usa esa.
2. Hay una skill **del mismo proyecto** → cárgala y ve al Paso 5.
3. Hay una skill **de la misma estructura** (mismo dominio e intención, otro proyecto) → ofrece *reutilizarla tal cual* o *derivar una nueva*.
4. Hay coincidencias parciales → muestra las 1–3 mejores con una línea cada una y pregunta.
5. No hay nada → crea una nueva (Paso 3).

Dos candidatas igual de buenas → pregunta. Nunca cargues más de dos skills de proyecto a la vez.

### Paso 3 — Borrador

- **Pedido detallado** (tareas, funcionamiento, entregables, tecnologías): extrae objetivo, alcance, entregables, herramientas y restricciones. Redacta un borrador breve: nombre, descripción, secciones. Lo que el usuario no dijo va marcado como *pendiente*; no lo inventes.
- **Pedido vago**: salta a las preguntas y vuelve aquí después.
- **Derivar de otra skill**: indica qué se conserva y qué se limpia del proyecto anterior.

Muéstralo como resumen (máx. 8 líneas), nunca el archivo completo, y pide autorización:

> **Punto de control 1** — "¿Creo la skill `a-<dominio>-<proyecto>` con este enfoque? Puedes ajustar lo que quieras."

Sin un sí explícito no se crea nada.

### Paso 4 — Preguntas y generación

**Preguntas** (banco en `references/preguntas.md`):
- Máximo 5 por ronda, máximo 2 rondas. Con opciones cuando sea posible.
- Solo lo que el pedido no responde y cambia la skill.
- Si el usuario dice "decide tú" o no responde: toma la opción más razonable, dila en una línea y sigue.

**Generación:**

```bash
python3 <agent-a>/scripts/new_skill.py --nombre a-<dominio>-<proyecto> \
  --intencion <intencion> --dominio <dominio> \
  --descripcion "Qué hace, para qué proyecto y frases concretas que la activan" \
  --destino <carpeta-de-skills>
# Derivar:  --base <ruta-skill-existente>  (requiere --descripcion nueva)
```

Luego:
1. Completa el `SKILL.md` generado con lo aprendido. La descripción es el disparador: concreta, distinta de otras skills y algo insistente.
2. Añade solo las herramientas que el proyecto usará (scripts, plantillas, checklists).
3. Valida y escanea: `validate_skill.py <ruta>` y `scan_secrets.py <ruta>`.
4. Guarda según el entorno y registra: `manage.py registrar --raiz <carpeta> --skill <ruta>`.
5. Informa en 2 líneas: nombre, dónde quedó, cómo se activa.

### Paso 5 — Trabajar como agente del proyecto

- Al empezar: lee `PROGRESO.md` del proyecto y resume en 2–3 líneas dónde quedó.
- Registra el uso: `manage.py usar --raiz <carpeta> --skill <nombre> --contexto "<3-8 palabras>"`.
- **Selección por momento**: en cada fase del trabajo elige la herramienta o skill adecuada según `references/seleccion.md` (ej. Word → skill de docx; Excel → xlsx; interfaz web → diseño frontend; gráficos → visualización de datos). Cámbiala cuando cambie el momento, no antes.
- Al terminar cada sesión: actualiza `PROGRESO.md` (hecho, pendiente, decisiones).
- Actualiza la skill del proyecto solo según la regla de actualización (`references/reglas.md`, R-30 a R-34).

### Paso 6 — Cierre y publicación

Al terminar el proyecto o en un hito importante (nunca en cada avance), sigue §7.

---

## 3. Continuar un proyecto

1. `manage.py seleccionar` con el nombre del proyecto.
2. Carga la skill y el `PROGRESO.md` del proyecto (pide el archivo si no está accesible).
3. Resume: estado, último avance, siguiente paso sugerido.
4. Confirma la tarea de la sesión si no es obvia y continúa (Paso 5).

Si no aparece la skill: dilo, muestra las más parecidas y ofrece crearla.

## 4. Crear una skill nueva

Pasos 0 → 1 → 2 → 3 → 4 del flujo principal. Si el pedido ya trae todo, el Paso 4 puede ser una sola ronda corta o ninguna.

## 5. Usar una skill concreta

Carga la skill nombrada, registra el uso y trabaja con ella. Si no existe, muestra las parecidas.

## 6. Administración del catálogo

Detalle completo en `references/administracion.md`. Comandos:

| Acción | Comando |
|---|---|
| Listar | `manage.py listar --raiz <carpeta>` |
| Buscar | `manage.py buscar --raiz <carpeta> --texto "..."` |
| Seleccionar | `manage.py seleccionar --raiz <carpeta> --texto "..."` |
| Registrar | `manage.py registrar --raiz <carpeta> --skill <ruta> [--copiar]` |
| Registrar uso | `manage.py usar --raiz <carpeta> --skill <nombre> --contexto "..."` |
| Auditar | `manage.py auditar --raiz <carpeta> [--dias 90]` |
| Subir versión | `manage.py version --skill <ruta> --tipo menor\|mayor --nota "..."` |
| Archivar / restaurar | `manage.py archivar\|restaurar --raiz <carpeta> --skill <nombre>` |

Reglas clave: nunca borrar (se archiva), una skill por proyecto, descripciones sin solaparse, versión y CHANGELOG siempre sincronizados.

## 7. Publicar en GitHub

Detalle en `references/publicacion-github.md`.

1. `validate_skill.py` y `scan_secrets.py` sin errores. Hallazgos → **detente** y muéstralos.
2. **Punto de control 2** — confirma repositorio, visibilidad (público/privado) y contenido.
3. Copia a `skills/<nombre>/`, `manage.py registrar`, escanea el repo completo.
4. Commit `skill(<nombre>): v<versión> — <resumen>` y push. Nunca `--force`.
5. En Claude (app) entrega también el `.zip` (`package_skill.py`).
6. Informa: nombre, versión, enlace y cómo instalarla.

## 8. Mejora continua de agent-a (regla vigente)

En cada uso, agent-a puede hacer **una sola mejora de intuitividad sobre sí mismo**, y es la **única modificación general autorizada** hasta que el usuario pida otra cosa. Procedimiento completo y límites en `references/mejora-continua.md`. Resumen:

- **Sí permitido**: aclarar redacción, reordenar pasos, añadir un ejemplo o atajo, mejorar mensajes al usuario, reducir preguntas innecesarias, corregir errores de los scripts.
- **No permitido sin pedido explícito**: cambiar reglas de seguridad, quitar puntos de control, ampliar el alcance, cambiar el nombre, borrar secciones, modificar otras skills por esta vía.
- Siempre: versión menor + línea en `CHANGELOG.md` + aviso al usuario en una línea. En la app de Claude se **propone** y el usuario decide; no se aplica en silencio.

## 9. Archivos de referencia

| Archivo | Cuándo leerlo |
|---|---|
| `references/reglas.md` | **Siempre**: reglas obligatorias de comportamiento |
| `references/seleccion.md` | Paso 2 y Paso 5: qué skill o herramienta usar en cada momento |
| `references/administracion.md` | §6: gestión del catálogo |
| `references/intenciones.md` | Paso 1 |
| `references/dominios.md` | Pasos 1 y 4 |
| `references/preguntas.md` | Paso 4 |
| `references/entornos.md` | Pasos 0, 4 y 7 |
| `references/seguridad.md` | Antes de guardar, empaquetar o publicar |
| `references/publicacion-github.md` | §7 |
| `references/mejora-continua.md` | §8, al final de cada uso |
