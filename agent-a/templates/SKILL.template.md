---
name: {{NOMBRE}}
description: {{DESCRIPCION}}
---

# {{TITULO}}

> Skill gestionada por agent-a · Intención: **{{INTENCION}}** · Dominio: **{{DOMINIO}}** · Versión: **1.0** · Creada: {{FECHA}}

## Objetivo del proyecto

<!-- 1 a 3 líneas: qué debe existir o lograrse al terminar. -->

## Cuándo usar esta skill

- Cuando el usuario pida continuar, revisar o ampliar este proyecto.
- Cuando quiera iniciar un proyecto nuevo con la misma estructura.
<!-- Agrega frases concretas que el usuario suele usar. -->

## Antes de empezar

1. Lee `PROGRESO.md` en la carpeta del proyecto (si no existe, créalo desde `templates/PROGRESO.plantilla.md`).
2. Resume en 2–3 líneas dónde quedó el trabajo y qué sigue.
3. Confirma con el usuario la tarea de esta sesión si no es obvia.

## Contexto y restricciones

<!-- Normas, formatos obligatorios, tecnologías, plazos tipo, rúbricas. -->

{{SECCIONES_INTENCION}}

## Herramientas de esta skill

| Herramienta | Uso |
|---|---|
| `templates/PROGRESO.plantilla.md` | Seguimiento del estado del proyecto (se copia a la carpeta del proyecto) |
<!-- Añade scripts y plantillas a medida que se creen. -->

## Criterios de terminado

<!-- Qué debe cumplirse para dar una tarea o el proyecto por terminado. -->

## Seguridad

- No guardar en esta skill ni en el repositorio: credenciales, `.env` reales, datos personales ni bases de datos reales.
- Pedir confirmación antes de acciones irreversibles y antes de publicar.

## Mantenimiento de la skill

Actualiza esta skill solo cuando el usuario corrija una forma de trabajar, un procedimiento se repita dos o más veces, o se incorpore una herramienta nueva. Sube la versión y anota el cambio en `CHANGELOG.md`. El estado del proyecto va en `PROGRESO.md`, nunca aquí.
