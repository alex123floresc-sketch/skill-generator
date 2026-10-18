# Changelog — cp-v1

## v1.0 — 2026-10-18
- Versión inicial de la fábrica de skills.
- Flujo de 8 pasos: entorno, intención, búsqueda, borrador, preguntas, generación, trabajo como agente, publicación.
- Intenciones: desarrollar, complementar, gestionar, administrar. Dominios con prefijo `cp-<dominio>-`.
- Scripts: new_skill, validate_skill, scan_secrets, registry, package_skill. Instalador `install.sh`.
- Protocolo de seguridad con dos puntos de control y escaneo de secretos obligatorio.
