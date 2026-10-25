---
name: entrega-entre-agentes
description: Registra en docs/tablero.md una entrega (handoff) de un agente a otro de inventario-saas, o actualiza el estado de una tarea. Úsala al terminar o bloquear una tarea, cuando necesites algo de otra área (tabla, endpoint, evento, diseño, revisión) o cuando otro agente deba continuar tu trabajo.
---

# Entrega entre agentes

> Skill de desarrollo del equipo de agentes de inventario-saas · Intención: **desarrollar** · Dominio: **software** · Versión: **1.0** · Creada: 2026-10-24

El tablero (`docs/tablero.md`) es la memoria compartida del equipo. Nadie trabaja "en privado".

## Pasos

1. Lee `docs/tablero.md` completo.
2. Actualiza la fila de tu tarea en **Tareas** (`pendiente` → `en curso` → `en revisión` → `hecha`, o
   `bloqueada` con motivo). Si la tarea no existe, agrégala con el siguiente `T-NNN` libre y dueño correcto
   (o pídesela al `arquitecto` si no está clara).
3. Agrega una entrega al final de **Entregas entre agentes** con el siguiente `E-NNN` libre:

```
### E-NNN · <tu-agente> → <agente-destino> · <AAAA-MM-DD>
- Tarea: T-NNN
- Qué cambió: <archivos/áreas, en 1–3 líneas>
- Contrato afectado: <openapi.yaml#/paths/... | eventos.md#tipo | V<n>__x.sql | ninguno>
- Qué necesito de ti: <acción concreta y verificable>
- Cómo verificarlo: <comando, prueba o pantalla>
```

4. Si la entrega pide cambiar un contrato, el destino es el `arquitecto` (o `mensajeria` para eventos,
   `base-datos` para tablas). Incluye la propuesta concreta (YAML/SQL), no solo la idea.
5. Si la entrega quita "sin entregas todavía", borra esa línea.

## Reglas
- Hechos verificados, no intenciones: si una prueba no se ejecutó, dilo.
- Una entrega por destinatario; si hay varios, varias entregas.
- No edites entregas antiguas de otros; responde con una nueva que la referencie (`Responde a E-NNN`).
