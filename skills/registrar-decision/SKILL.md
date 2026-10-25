---
name: registrar-decision
description: Crea un ADR (Architecture Decision Record) en docs/decisiones/ de inventario-saas. Úsala al elegir una tecnología o proveedor, adelantar algo de Fase 2/Escala, cambiar un patrón, o reemplazar una decisión anterior.
---

# Registrar una decisión (ADR)

> Skill de desarrollo del equipo de agentes de inventario-saas · Intención: **desarrollar** · Dominio: **software** · Versión: **1.0** · Creada: 2026-10-24

1. Revisa `docs/decisiones/README.md` y los ADR existentes: ¿ya está decidido? ¿contradice alguno?
2. Siguiente número libre `NNNN`. Archivo `docs/decisiones/ADR-NNNN-<titulo-en-kebab>.md`:

```markdown
# ADR-NNNN · <Título>

- Estado: propuesta | aceptada | reemplazada por ADR-XXXX · Fecha: AAAA-MM-DD · Decide: <agentes / usuario>

## Contexto
<problema, restricciones, fase de la hoja de ruta>

## Decisión
<qué se hace, concreto>

## Alternativas descartadas
- <opción>: <por qué no>

## Consecuencias
<qué cambia para cada agente, costos, riesgos; para almacenes nuevos: consistencia fuerte o eventual (CAP)>

## Fuentes
<capítulo de libro en docs/conocimiento/ o URL de documentación oficial>
```

3. Agrega la fila a la tabla de `docs/decisiones/README.md`.
4. Si reemplaza otra, cambia **solo** la línea de estado de la anterior a `reemplazada por ADR-NNNN`.
5. Si implica costo, contrato con un proveedor o cambio de alcance, deja el estado en `propuesta` y
   pregúntale al usuario; solo él la pasa a `aceptada`.
6. Avisa a los agentes afectados con la skill `entrega-entre-agentes`.
