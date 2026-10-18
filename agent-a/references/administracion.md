# Administración del catálogo de skills

Todo se hace con `scripts/manage.py`. La "raíz" es la carpeta que contiene las skills (`skills/` del repo, `~/.claude/skills/`, `.claude/skills/`).

## Archivos que mantiene

| Archivo | Contenido |
|---|---|
| `<raiz>/REGISTRO.md` | Índice legible: skill, versión, intención, dominio, usos, descripción |
| `<raiz>/uso.json` | Historial de uso: veces, último uso, contextos recientes (máx. 10 por skill, 80 caracteres c/u) |
| `<raiz>/_archivo/` | Skills archivadas (fuera de selección y del registro activo) |

El contexto de uso es una etiqueta corta del tipo de tarea ("crud usuarios", "reporte semanal"), nunca datos personales.

## Operaciones

### Listar y buscar
```bash
manage.py listar --raiz skills
manage.py buscar --raiz skills --texto "inventario postgresql"
```

### Registrar
```bash
manage.py registrar --raiz skills --skill ruta/a/a-web-inventario [--copiar]
```
`--copiar` copia la skill dentro de la raíz si está en otra carpeta (si ya existe, se reemplaza solo esa carpeta tras confirmar con el usuario).

### Registrar uso
```bash
manage.py usar --raiz skills --skill a-web-inventario --contexto "formulario de productos"
```
Hacerlo al activar una skill de proyecto (R-44).

### Auditar
```bash
manage.py auditar --raiz skills --dias 90
```
Detecta: errores de validación, versión del encabezado distinta al CHANGELOG, descripciones que se solapan (posibles duplicados), skills sin uso en N días, marcadores `{{...}}` sin completar.

Qué hacer con cada hallazgo:

| Hallazgo | Acción sugerida |
|---|---|
| Error de validación | Corregir y subir versión menor |
| Versiones desincronizadas | `manage.py version` con la nota pendiente |
| Solape de descripciones | Diferenciar descripciones o proponer fusionar (con confirmación) |
| Sin uso prolongado | Proponer archivar (no hacerlo sin confirmación) |
| Marcadores sin completar | Completar o eliminar la sección |

### Versionar
```bash
manage.py version --skill skills/a-web-inventario --tipo menor --nota "Agrega plantilla de reporte"
```
Actualiza el encabezado `Versión: **X.Y**` del `SKILL.md` y añade la entrada al `CHANGELOG.md`.

### Archivar y restaurar
```bash
manage.py archivar  --raiz skills --skill a-web-viejo
manage.py restaurar --raiz skills --skill a-web-viejo
```
Archivar mueve la carpeta a `_archivo/`. Nunca se borra (R-13).

### Fusionar (manual, con confirmación)
1. Elegir la skill que queda (la más usada o más completa).
2. Pasar a ella las secciones y herramientas útiles de la otra.
3. Versión mayor en la que queda; archivar la otra.

### Renombrar (con confirmación, R-12)
1. Derivar con `new_skill.py --base <vieja> --nombre <nuevo>`.
2. Archivar la vieja. Avisar que el nombre anterior deja de activarse.

## Rutina recomendada

- Al iniciar un proyecto: `seleccionar`.
- Al activar una skill: `usar`.
- Al cerrar un proyecto: `version` + `registrar` + publicar.
- Cada cierto tiempo o cuando el usuario pida orden: `auditar`.
