# Mejora continua de agent-a

**Regla vigente (desde v2.0, hasta que el usuario indique otra cosa):** en cada uso, agent-a puede aplicar **una** mejora orientada a hacerse más intuitivo. Es la única modificación general de agent-a autorizada por ahora.

## Cuándo aplicar una mejora

Al final de cada uso, revisa si hubo fricción:

- El usuario tuvo que repetir o aclarar algo que agent-a debió entender.
- Una pregunta fue innecesaria o confusa.
- Un paso se hizo en mal orden o sobró.
- Un script falló o dio un mensaje poco claro.
- Faltó un atajo o ejemplo que habría ahorrado tiempo.

Si no hubo fricción, **no se cambia nada**. No hay obligación de mejorar en cada uso.

## Qué se puede cambiar

- Redacción de instrucciones, mensajes y resúmenes.
- Orden de pasos y ejemplos.
- Nuevos atajos en la tabla §1 o alias en la descripción.
- Valores por defecto (ej. preguntar menos cuando el pedido ya es claro).
- Corrección de errores en los scripts de agent-a.

## Qué NO se puede cambiar por esta vía

- Reglas de seguridad (R-01 a R-09) y puntos de control (R-10 a R-12).
- El alcance o propósito de agent-a, su nombre o la estructura de carpetas.
- Eliminar secciones o referencias.
- Otras skills (esas siguen R-32).
- Esta misma regla.

## Procedimiento

1. Identifica la fricción en una frase.
2. Aplica **un solo** cambio pequeño.
3. Valida: `validate_skill.py <agent-a>`.
4. Sube versión menor: `manage.py version --skill <agent-a> --tipo menor --nota "Intuitividad: <cambio>"`.
5. Avisa al usuario en una línea: "Mejoré agent-a (v2.1): <cambio>."
6. Publica en GitHub junto con la siguiente publicación (no hace falta un push solo por esto, salvo que el usuario lo pida).

Según el entorno:
- **Claude Code**: aplica el cambio en la copia instalada y en el repo.
- **Claude (app)**: no puedes modificar la skill instalada. Propón el cambio (o úsalo vía la herramienta de proponer skills) y aplícalo en el repo si hay acceso; el usuario reinstala.

## Si el usuario pide otra cosa

Cuando el usuario pida una modificación general distinta, se aplica lo que pida y, si cambia esta regla, se actualiza este archivo con versión mayor.
