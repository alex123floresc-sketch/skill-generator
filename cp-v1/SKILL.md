---
name: cp-v1
description: Fábrica de skills por proyecto (CP V1). Úsala SIEMPRE que el usuario pida iniciar, continuar, retomar, replicar o escalar un proyecto de cualquier tipo — desarrollar (software, webs, apps, scripts), complementar (mejorar o extender algo que ya existe), gestionar (planificar, organizar tareas, cronogramas, seguimiento de proyectos, datos) o administrar (operar, mantener, documentar sistemas, bases de datos, repositorios, procesos). También cuando mencione "CP V1", "cp-v1", "crea una skill para este proyecto", "usa la skill del proyecto", "proyecto categoría ...", o quiera que Claude trabaje como agente dedicado a un proyecto. Busca primero si ya existe una skill guardada para ese proyecto y la reutiliza; si no, diseña una nueva con el usuario, la hace evolucionar mientras avanza el proyecto y la publica en GitHub al cerrar. Funciona en Claude (app) y en Claude Code.
---

# CP V1 — Fábrica de skills por proyecto

CP V1 convierte cualquier proyecto en una **skill dedicada** que Claude puede reutilizar: para seguir el mismo proyecto otro día, o para arrancar uno nuevo con la misma estructura. No hace falta que exista un proyecto previo: sirve para lo que el usuario necesite, desde gestión de datos y desarrollo web hasta tareas académicas o administración de sistemas.

Lee este archivo completo antes de actuar. Los detalles están en `references/`; ábrelos cuando el paso lo indique.

## Principios

1. **Primero reutilizar, luego crear.** Nunca generes una skill nueva sin buscar antes una existente.
2. **El usuario autoriza.** Hay dos puntos de control obligatorios: antes de crear la skill y antes de publicarla. Nada se publica sin un "sí" explícito.
3. **Método ≠ estado.** La skill guarda *cómo se hace* (estructura, reglas, herramientas). El avance (*qué está hecho y qué falta*) va en `PROGRESO.md` dentro del proyecto, nunca dentro de la skill.
4. **Pocas preguntas, pero buenas.** Máximo 5 por ronda, solo las que cambian cómo se construye la skill.
5. **Seguridad siempre.** Ningún secreto, credencial o dato personal entra en una skill ni en el repositorio (ver `references/seguridad.md`).

## Flujo de trabajo

### Paso 0 — Detectar entorno

Determina dónde estás, porque cambia cómo se guarda la skill (detalle en `references/entornos.md`):

- **Claude Code**: hay sistema de archivos del usuario; las skills viven en `~/.claude/skills/` (personales) o `.claude/skills/` (del proyecto). Puedes escribirlas directamente.
- **Claude (app web/escritorio/móvil)**: no puedes instalar skills por tu cuenta. Generas los archivos, los empaquetas en `.zip` y el usuario los añade; si hay una herramienta para proponer skills (tarjeta de revisión), úsala. Si la sesión tiene acceso a git, también puedes publicar en GitHub.

### Paso 1 — Clasificar la intención

Toda petición se clasifica en **una intención principal** (puede haber secundarias). Esto define la base de la skill. Abre `references/intenciones.md` para el detalle de cada una.

| Intención | Señales en el pedido | La skill se centra en |
|---|---|---|
| **Desarrollar** | crear, construir, programar, hacer una web/app/script | arquitectura, stack, estructura de carpetas, convenciones de código, pruebas |
| **Complementar** | mejorar, extender, agregar a, corregir, optimizar algo existente | leer lo existente primero, respetar su estilo, cambios incrementales |
| **Gestionar** | planificar, organizar, cronograma, seguimiento, tareas, datos, reportes | entregables, hitos, formatos de reporte, plantillas de seguimiento |
| **Administrar** | mantener, operar, documentar, respaldar, configurar, monitorear | procedimientos (runbooks), checklists, permisos, respaldos |

Además identifica el **dominio** (datos, web, académico, gestión de proyectos, sistemas, otro) con `references/dominios.md`. Intención + dominio = punto de partida de la skill.

Si la intención no es clara, pregúntala en la primera ronda del Paso 4.

### Paso 2 — Buscar una skill existente

Busca en este orden y detente en la primera coincidencia útil:

1. Las skills disponibles en la sesión actual (lista de skills del sistema).
2. En Claude Code: `~/.claude/skills/` y `.claude/skills/` del proyecto actual.
3. El repositorio de skills del usuario (por defecto `skills/REGISTRO.md` en el repo `skill-generator`), si hay acceso a git o GitHub.

Para buscar en un directorio local usa:

```bash
python3 <ruta-cp-v1>/scripts/registry.py buscar --raiz <carpeta-de-skills> --texto "<palabras clave>"
```

Según el resultado:

- **Coincide el mismo proyecto** → carga esa skill y su `PROGRESO.md`, resume en 2–3 líneas dónde quedó el trabajo y continúa como agente de ese proyecto. Salta al Paso 6.
- **Coincide la misma estructura, proyecto distinto** → ofrece *reutilizarla tal cual* o *derivar una nueva versión* a partir de ella (copia, renombra y ajusta). Continúa en el Paso 3 usando esa skill como base.
- **No hay coincidencia** → continúa en el Paso 3.

### Paso 3 — Analizar el pedido y proponer un borrador

- **Pedido detallado** (ya describe tareas, funcionamiento, entregables o tecnologías): extrae de ahí objetivo, alcance, entregables, herramientas y restricciones, y redacta un **borrador breve** de la skill (nombre, descripción, secciones principales). No inventes requisitos que el usuario no dio; márcalos como pendientes.
- **Pedido vago**: no redactes nada todavía; pasa directo a las preguntas del Paso 4 y luego vuelve aquí.

Muestra el borrador en un resumen corto (no el archivo completo) y pide autorización:

> **Punto de control 1:** "¿Creo la skill `<nombre>` con este enfoque? Puedes ajustar lo que quieras antes."

Sin confirmación explícita no se crea nada.

### Paso 4 — Preguntas específicas

Usa el banco de `references/preguntas.md`. Reglas:

- Máximo **5 preguntas por ronda**; si existe una herramienta de preguntas de opción múltiple, úsala.
- Pregunta solo lo que el pedido no responde y que cambia la skill: objetivo final, entregable y formato, tecnologías o herramientas obligatorias, restricciones (plazo, normas, formato de la institución), y nivel de autonomía deseado.
- Si el usuario no está disponible para responder, toma la interpretación más razonable, dila en una línea y continúa.

### Paso 5 — Generar la skill

1. Elige el nombre: minúsculas con guiones, formato `cp-<dominio>-<proyecto>` (ej. `cp-web-tienda-artesanias`, `cp-datos-encuesta-campus`). Máximo 64 caracteres.
2. Crea la estructura con el script de andamiaje:

   ```bash
   python3 <ruta-cp-v1>/scripts/new_skill.py \
     --nombre cp-web-tienda-artesanias \
     --intencion desarrollar --dominio web \
     --descripcion "Qué hace y CUÁNDO usarla (frases y contextos que la activan)" \
     --destino <carpeta-de-skills>
   ```

   Esto genera, a partir de `templates/`:

   ```
   cp-<dominio>-<proyecto>/
   ├── SKILL.md          ← instrucciones del agente del proyecto
   ├── CHANGELOG.md      ← historial de versiones
   ├── references/       ← documentación extensa (stack, normas, formatos)
   ├── templates/        ← plantillas de entregables (incluye PROGRESO.md)
   └── scripts/          ← herramientas reutilizables
   ```

3. Completa el `SKILL.md` generado con lo aprendido en los Pasos 3–4. La **descripción** es lo que hace que Claude active la skill: incluye qué hace, para qué proyecto y frases concretas que la disparan. Hazla algo "insistente" para que no deje de activarse.
4. Agrega las herramientas que el proyecto necesite (scripts, plantillas, checklists) — solo las que realmente se usarán.
5. Valida antes de entregar:

   ```bash
   python3 <ruta-cp-v1>/scripts/validate_skill.py <ruta-skill>
   python3 <ruta-cp-v1>/scripts/scan_secrets.py <ruta-skill>
   ```

6. Guarda según el entorno (`references/entornos.md`) y registra la skill:

   ```bash
   python3 <ruta-cp-v1>/scripts/registry.py agregar --raiz <carpeta-de-skills> --skill <ruta-skill>
   ```

### Paso 6 — Trabajar como agente del proyecto

Desde aquí sigues las instrucciones de la skill generada. Durante el trabajo:

- Mantén `PROGRESO.md` en la carpeta del **proyecto** (no en la skill): qué se hizo, decisiones, pendientes. Actualízalo al final de cada sesión de trabajo.
- **Regla de actualización de la skill.** Modifica la skill solo cuando:
  - el usuario corrige una forma de trabajar ("así no, hazlo de esta forma"),
  - un mismo procedimiento se repite dos o más veces (conviértelo en script o plantilla),
  - se incorpora una herramienta, tecnología o norma nueva al proyecto.
  En cada cambio sube la versión (`v1.0` → `v1.1` para ajustes, `v2.0` para cambios de estructura) y anota una línea en `CHANGELOG.md`.
- No pongas en la skill datos que caducan (fechas concretas, estados de tareas, cifras del momento).

### Paso 7 — Cerrar y publicar en GitHub

Al terminar el proyecto (o en un hito importante, nunca en cada avance):

1. Ejecuta de nuevo `validate_skill.py` y `scan_secrets.py`. Si el escaneo encuentra algo, **detente** y muéstraselo al usuario.
2. **Punto de control 2:** confirma con el usuario el repositorio destino, si es público o privado, y que el contenido puede publicarse.
3. Publica siguiendo `references/publicacion-github.md`: la skill va en `skills/<nombre>/` del repositorio, se actualiza `skills/REGISTRO.md`, y se hace commit con mensaje descriptivo. Nunca uses `push --force` ni borres skills ajenas.
4. En Claude (app), además genera el `.zip` para que el usuario pueda instalarla:

   ```bash
   python3 <ruta-cp-v1>/scripts/package_skill.py <ruta-skill> --salida <carpeta>
   ```

5. Informa en 2–3 líneas: nombre y versión de la skill, dónde quedó publicada y cómo reutilizarla.

## Reutilizar una skill publicada

- **Claude Code:** clona el repo y copia la carpeta de la skill a `~/.claude/skills/`, o ejecuta `install.sh` del repositorio.
- **Claude (app):** descarga o genera el `.zip` de la skill y añádelo desde la configuración de skills.
- **Proyecto nuevo con la misma estructura:** copia la skill con otro nombre (`new_skill.py --base <skill-existente>`), limpia lo específico del proyecto anterior y ajusta la descripción.

## Archivos de referencia

| Archivo | Cuándo leerlo |
|---|---|
| `references/intenciones.md` | Paso 1: qué priorizar según desarrollar / complementar / gestionar / administrar |
| `references/dominios.md` | Paso 1 y 5: herramientas y secciones típicas por dominio |
| `references/preguntas.md` | Paso 4: banco de preguntas por intención y dominio |
| `references/entornos.md` | Pasos 0, 5 y 7: cómo guardar e instalar en Claude Code y en Claude (app) |
| `references/seguridad.md` | Siempre antes de guardar o publicar |
| `references/publicacion-github.md` | Paso 7: procedimiento de publicación |
