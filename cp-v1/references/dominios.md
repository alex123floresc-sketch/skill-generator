# Dominios: herramientas y secciones típicas

Usa el dominio para decidir qué incluir en `references/`, `templates/` y `scripts/` de la skill generada. Incluye solo lo que el proyecto realmente usará.

| Dominio | Prefijo | Ejemplos de proyecto | Herramientas sugeridas |
|---|---|---|---|
| Datos | `cp-datos-` | encuestas, conteo de cuestionarios, limpieza de Excel, estadística, dashboards | script de limpieza/conteo (Python, pandas), plantilla de tabla resumen, diccionario de datos, checklist de validación |
| Web | `cp-web-` | páginas, apps web, APIs, prototipos con base de datos | estructura de carpetas, plantilla de README, `.env.example`, checklist de despliegue, convenciones de componentes |
| Software | `cp-soft-` | programas, scripts, bots, apps de escritorio o móviles | arquitectura, convenciones, pruebas, guía de compilación |
| Base de datos | `cp-bd-` | modelos E-R, CRUDs, PostgreSQL/MySQL, migraciones | convenciones de nombres, plantillas SQL, script de datos de prueba, checklist de normalización |
| Académico | `cp-acad-` | trabajos, informes, exposiciones, tareas de cursos | formato de la institución, estructura del informe, plantilla de citas, checklist de entrega |
| Gestión | `cp-gest-` | proyectos de equipo, emprendimientos, eventos, planes | plantilla de cronograma, reporte semanal, registro de decisiones, matriz de responsables |
| Sistemas | `cp-sis-` | servidores, redes, repositorios, cuentas, mantenimiento | runbooks, checklist de respaldo, registro de operaciones |
| Diseño | `cp-dis-` | certificados, presentaciones, interfaces, material gráfico | guía de estilo (colores, tipografías), plantillas, checklist de revisión visual |
| Otro | `cp-gen-` | cualquier cosa que no encaje | define las secciones con el usuario en el Paso 4 |

## Secciones comunes a toda skill generada

1. **Objetivo del proyecto** (1–3 líneas).
2. **Cuándo usar esta skill** (repite y amplía lo de la descripción).
3. **Contexto y restricciones** (normas, formatos, herramientas obligatorias).
4. **Flujo de trabajo** paso a paso.
5. **Herramientas disponibles** (scripts y plantillas de la skill, cómo se usan).
6. **Criterios de calidad / terminado.**
7. **Seguridad** (qué nunca guardar ni publicar en este proyecto).
8. **Estado del proyecto:** "Leer `PROGRESO.md` del proyecto antes de continuar."
