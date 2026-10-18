# Selección: qué skill o herramienta usar en cada momento

agent-a elige en dos niveles:

1. **Skill de proyecto** — cuál de las skills `a-*` gobierna el trabajo (una por proyecto).
2. **Skill o herramienta de momento** — qué usar para la fase concreta (redactar un Word, armar un Excel, diseñar una interfaz…). Se suman a la skill de proyecto y cambian según la fase.

## Nivel 1 — Skill de proyecto

```bash
python3 scripts/manage.py seleccionar --texto "<pedido resumido>" --raiz <carpeta> [--raiz <otra>]
```

El puntaje combina:
- coincidencia de palabras con nombre, descripción, dominio e intención (peso alto en el nombre),
- historial de uso: cuántas veces se usó y si los contextos anteriores se parecen al pedido,
- penalización a skills archivadas (no aparecen) y a las que tienen errores de validación.

Interpretación del resultado:

| Resultado | Acción |
|---|---|
| Una candidata con puntaje claramente mayor (≥ 2× la segunda) | Usarla; decir cuál en una línea |
| Varias parecidas | Mostrar hasta 3 y preguntar |
| Ninguna o puntaje muy bajo | Proponer crear una nueva |

## Nivel 2 — Herramienta por momento

Usa la que esté disponible en la sesión; si no lo está, la alternativa indicada.

| Momento del trabajo | Usar | Alternativa |
|---|---|---|
| Entender archivos adjuntos | skill de lectura de archivos / PDF | leer con scripts |
| Redactar documento para entregar (informe, guía, trabajo) | skill de documentos de Claude; Word solo si piden .docx | Markdown |
| Hoja de cálculo, tablas, conteos, fórmulas | skill de xlsx | CSV + script Python |
| Presentación / exposición | skill de diapositivas; pptx si piden archivo | — |
| PDF (crear, unir, rellenar) | skill de pdf | — |
| Interfaz web, página, prototipo visual | skill de diseño frontend | HTML/CSS propio |
| Gráficos y dashboards | skill de visualización de datos | matplotlib / Chart.js |
| Investigación con muchas fuentes | skill de investigación profunda / búsqueda web | búsquedas manuales |
| Diseño gráfico (certificados, afiches) | conector de Canva o Figma si está conectado | Design/HTML |
| Evaluar o afinar una skill con pruebas | skill-creator (evals, descripción) | revisión manual |
| Código, repositorios, scripts | herramientas de archivos y terminal | — |
| Publicar skills | `manage.py` + git (§7 de SKILL.md) | `.zip` con `package_skill.py` |

## Momentos de un proyecto típico

1. **Arranque** → agent-a (selección/creación) + lectura de adjuntos.
2. **Planificación** → plantillas de la skill de proyecto (cronograma, entregables).
3. **Ejecución** → herramienta del entregable (código, xlsx, docs, diseño…).
4. **Revisión** → checklists de la skill + validaciones.
5. **Entrega** → formato pedido (docs, pdf, pptx, repo).
6. **Cierre** → `PROGRESO.md` final, versión de la skill, publicación.

## Reglas

- Anunciar el cambio de herramienta solo si afecta lo que el usuario recibe (ej. "Lo armo en Excel").
- No cargar skills "por si acaso": solo la que el momento necesita.
- Si una skill de proyecto define su propia herramienta para un momento, esa manda sobre esta tabla.
