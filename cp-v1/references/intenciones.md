# Intenciones: la base de cada skill

Cada skill generada parte de una intención principal. La intención decide qué secciones lleva el `SKILL.md` del proyecto y qué hace el agente primero.

## Desarrollar

Construir algo nuevo: software, página web, app, script, base de datos, modelo, documento técnico.

**El agente debe:**
- Definir arquitectura y estructura de carpetas antes de escribir código.
- Fijar stack y versiones (lenguaje, framework, base de datos).
- Establecer convenciones: nombres, estilo, idioma de comentarios.
- Trabajar por incrementos pequeños que funcionen, con pruebas o verificación en cada uno.

**Secciones obligatorias en la skill:** Objetivo · Stack · Estructura del proyecto · Convenciones · Flujo de desarrollo · Cómo probar · Entregables.

**Herramientas típicas:** script de andamiaje del proyecto, plantilla de README, checklist de pruebas, `.gitignore` adecuado, `.env.example`.

## Complementar

Mejorar, extender, corregir u optimizar algo que ya existe (código, documento, base de datos, trabajo previo).

**El agente debe:**
- Leer y entender lo existente **antes** de proponer cambios.
- Respetar el estilo, la estructura y las decisiones previas salvo que el usuario pida cambiarlas.
- Hacer cambios incrementales y reversibles, explicando qué cambió.
- Nunca reescribir desde cero sin autorización.

**Secciones obligatorias:** Qué existe (inventario) · Qué se va a mejorar · Reglas de compatibilidad · Cómo verificar que nada se rompió.

**Herramientas típicas:** checklist de revisión, plantilla de "antes/después", script de comparación o pruebas de regresión.

## Gestionar

Planificar, organizar y dar seguimiento: proyectos, tareas, cronogramas, equipos, datos, reportes, trabajos académicos.

**El agente debe:**
- Descomponer el objetivo en entregables e hitos con responsables y fechas (las fechas van en `PROGRESO.md`, no en la skill).
- Definir formatos fijos de reporte y seguimiento.
- Mantener un registro de decisiones.
- En gestión de datos: definir origen, limpieza, formato de salida y validación.

**Secciones obligatorias:** Objetivo y alcance · Entregables · Formato de seguimiento · Formato de reportes · Criterios de terminado.

**Herramientas típicas:** plantilla de cronograma, plantilla de acta o reporte semanal, plantilla de tabla resumen, scripts de limpieza o conteo de datos.

## Administrar

Operar y mantener algo en el tiempo: sistemas, servidores, bases de datos, repositorios, cuentas, documentación, procesos recurrentes.

**El agente debe:**
- Trabajar con procedimientos paso a paso (runbooks) y checklists.
- Pedir confirmación antes de cualquier acción irreversible (borrar, sobrescribir, migrar, cambiar permisos).
- Registrar cada operación realizada.
- Aplicar mínimo privilegio y respaldos antes de cambios.

**Secciones obligatorias:** Inventario del sistema · Procedimientos frecuentes · Respaldos y recuperación · Permisos y accesos (sin credenciales) · Registro de operaciones.

**Herramientas típicas:** runbooks, checklist de mantenimiento, script de respaldo, plantilla de registro de incidencias.

## Intenciones combinadas

Muchos proyectos mezclan intenciones (ej. *desarrollar* una web y luego *administrarla*). Elige la principal para la estructura base y añade las secciones obligatorias de las secundarias. Si el proyecto cambia de fase (de desarrollo a mantenimiento), actualiza la skill con una versión mayor (`v2.0`).
