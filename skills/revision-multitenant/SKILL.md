---
name: revision-multitenant
description: Revisa un cambio de inventario-saas buscando fugas entre tiendas (tenants), fallos de permisos y de seguridad - RLS, tienda_id, consultas nativas, caché, búsqueda, archivos, logs y eventos. Úsala antes de dar por terminada cualquier tarea que toque datos de negocio, y cuando el arquitecto, seguridad o qa revisen un PR.
---

# Revisión multi-tenant y de seguridad

> Skill de desarrollo del equipo de agentes de inventario-saas · Intención: **desarrollar** · Dominio: **software** · Versión: **1.0** · Creada: 2026-10-24

Revisa el diff (`git diff main...HEAD` o los archivos indicados) contra cada punto. Reporta
`archivo:línea · severidad (crítica/alta/media/baja) · problema · corrección`.

## Base de datos
- [ ] Tabla de negocio nueva con `tienda_id`, RLS **habilitado y forzado** y política (ver skill `nueva-migracion`).
- [ ] `UNIQUE` e índices incluyen `tienda_id` como primera columna.
- [ ] Ninguna función `SECURITY DEFINER` ni rol con `BYPASSRLS` usado por la app.

## Backend
- [ ] El tenant sale del JWT (`TenantContext`), nunca de path/query/body.
- [ ] `SET LOCAL app.tienda_id` dentro de la transacción; `TenantContext` limpiado en `finally`.
- [ ] Consultas nativas y `@Query` parametrizadas (sin concatenar strings).
- [ ] Buscar por id devuelve 404 (no 403) si el recurso es de otra tienda, para no revelar existencia.
- [ ] `@PreAuthorize` en cada operación; datos sensibles (costos, márgenes) filtrados por rol en el DTO.
- [ ] Jobs programados/batch/consumidores de eventos fijan el tenant del mensaje antes de tocar datos.

## Otras capas
- [ ] Caché (Redis): la clave incluye `tienda_id`.
- [ ] Búsqueda/analítica: filtro obligatorio por `tienda_id` en cada consulta.
- [ ] Archivos: ruta con prefijo `tienda_id/`, URL firmada con expiración.
- [ ] Eventos: `tiendaId` en el sobre; sin datos personales sensibles.
- [ ] Logs/Sentry: `tienda_id` sí, tokens/contraseñas/datos personales no.
- [ ] Web/escritorio: caché de TanStack Query y almacenamiento local se limpian al cerrar sesión o cambiar de tienda.

## Pruebas
- [ ] Existe prueba "la tienda B no ve / no modifica datos de la tienda A" para cada recurso nuevo.
- [ ] Existe prueba de 403 por rol sin permiso.

Si hay un hallazgo crítico: marca la tarea como `bloqueada` en el tablero y deja una entrega al dueño.
