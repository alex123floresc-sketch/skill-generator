---
name: integracion-externa
description: Patrón para integrar un servicio externo en inventario-saas (pasarela de pago, SUNAT vía Nubefact/APIsPERU, correo, WhatsApp, almacenamiento S3/R2) con puerto de dominio, adaptador, timeouts, reintentos, idempotencia, webhooks firmados, sandbox y pruebas. Úsala al conectar cualquier API de terceros.
---

# Integración externa

> Skill de desarrollo del equipo de agentes de inventario-saas · Intención: **desarrollar** · Dominio: **software** · Versión: **1.0** · Creada: 2026-10-24

1. **Documenta el proveedor** en `docs/integraciones/<proveedor>.md`: URLs de sandbox y producción,
   autenticación, límites, errores, webhooks, costos, enlace a la documentación oficial. Si implica costo o
   contrato → ADR en estado `propuesta` y pregunta al usuario (skill `registrar-decision`).
2. **Puerto en el dominio** (`<modulo>.dominio`): interfaz en términos de negocio, p. ej.
   `EmisorComprobantes.emitir(Comprobante) : ResultadoEmision`. Sin tipos del proveedor.
3. **Adaptador** en `<modulo>.infraestructura.<proveedor>`: cliente HTTP (`RestClient`) con
   timeout de conexión y lectura explícitos; mapeo de errores del proveedor a errores de dominio.
4. **Resiliencia** (Resilience4j cuando esté en la fase; antes, reintento simple):
   - Reintentos con backoff exponencial **solo** si la operación es idempotente o lleva clave de idempotencia.
   - Circuit breaker y bulkhead por proveedor.
   - Operaciones que no deben perderse (emitir comprobante, enviar correo) → asíncronas vía evento/outbox.
5. **Webhooks**: endpoint dedicado, verificación de firma/secret, respuesta 2xx rápida, procesamiento
   asíncrono, deduplicación por id de evento del proveedor.
6. **Secretos**: variables de entorno documentadas en `.env.example` sin valores reales; certificados
   (SUNAT) en el gestor de secretos.
7. **Pruebas**: adaptador con WireMock (respuestas reales del sandbox guardadas como fixtures),
   implementación falsa del puerto para pruebas del dominio, prueba de idempotencia (doble webhook).
8. **Observabilidad**: métricas de latencia/errores por proveedor (Micrometer) y alerta si el circuito se abre.
9. Revisión de `seguridad` y entrega a `qa` (skill `entrega-entre-agentes`).
