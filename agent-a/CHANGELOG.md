# Changelog — agent-a

Formato: `vMAYOR.MENOR` — MENOR para ajustes e intuitividad, MAYOR para cambios de estructura o alcance.

## v2.0 — 2026-10-18
- Renombrada de `cp-v1` a `agent-a`: agente principal que genera, administra y selecciona skills.
- Nuevo: atajos de uso rápido (`agent-a nueva`, `continuar`, `listar`, `auditar`, `publicar`…).
- Nuevo: selección en dos niveles (skill de proyecto + herramienta por momento) con historial de uso (`references/seleccion.md`).
- Nuevo: administración del catálogo — listar, buscar, seleccionar, registrar, usar, auditar, versionar, archivar, restaurar (`scripts/manage.py`, reemplaza a `registry.py`).
- Nuevo: reglas numeradas R-01…R-53 (`references/reglas.md`).
- Nuevo: regla de mejora continua — una mejora de intuitividad por uso como única modificación general autorizada (`references/mejora-continua.md`).
- Prefijo de skills generadas cambia a `a-<dominio>-<proyecto>`.
- Correcciones: la descripción con `: ` rompía el YAML (ahora se valida y se corrige); `--base` exigía descripción nueva para evitar skills duplicadas; versión de SKILL.md y CHANGELOG ahora se sincronizan y se auditan; `buscar` ya no crea carpetas vacías; la plantilla de progreso de cada skill ya no queda ignorada por git; validación de referencias a archivos inexistentes.

## v1.0 — 2026-10-18
- Versión inicial (CP V1): fábrica de skills por proyecto, 8 pasos, intenciones, plantillas, scripts y protocolo de seguridad.
