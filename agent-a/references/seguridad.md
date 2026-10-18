# Protocolo de seguridad

Aplica antes de guardar, empaquetar o publicar cualquier skill. Si alguna regla no se cumple, **detente y avisa al usuario**.

## 1. Nunca guardar ni publicar

- Contraseñas, tokens, API keys, claves SSH o privadas, cadenas de conexión con credenciales.
- Archivos `.env` reales (solo `.env.example` con valores ficticios).
- Datos personales: DNI, correos, teléfonos, direcciones, códigos de estudiante, notas, datos de salud.
- Bases de datos reales, respaldos, exportaciones con datos de personas.
- Información interna de instituciones o empresas que el usuario no autorizó publicar.

En su lugar: variables de entorno, valores de ejemplo (`TU_API_KEY_AQUI`) y datos ficticios.

## 2. Escaneo obligatorio

```bash
python3 scripts/scan_secrets.py <ruta>
```

Código de salida distinto de 0 = hay hallazgos. Muéstralos al usuario, corrígelos y vuelve a escanear. No publiques con hallazgos pendientes, aunque el usuario insista: explica el riesgo y ofrece limpiar el dato.

## 3. Puntos de control

| Momento | Qué confirmar |
|---|---|
| Antes de crear la skill | nombre, intención, enfoque |
| Antes de publicar | repositorio, visibilidad (público/privado), contenido |
| Antes de acciones irreversibles | borrar, sobrescribir, migrar, cambiar permisos |

## 4. Reglas para GitHub

- Nunca `git push --force`, nunca reescribir historial ajeno.
- No borrar ni modificar skills que no sean del proyecto actual.
- Mantener `.gitignore` con `.env`, `*.key`, `*.pem`, `node_modules/`, `__pycache__/`, respaldos y datos.
- Si un secreto llegó a subirse, avisar de inmediato: borrarlo del repo **no basta**, hay que revocarlo y generar uno nuevo.

## 5. Código y archivos externos

- No ejecutar scripts descargados sin revisarlos.
- Los scripts de la skill deben ser legibles, sin ofuscación y sin descargar código en tiempo de ejecución.
- Una skill nunca debe instruir a Claude a saltarse confirmaciones, ocultar acciones al usuario o ignorar estas reglas.
