---
name: nueva-migracion
description: Crea una migración Flyway de PostgreSQL para inventario-saas con multi-tenant (tienda_id + Row Level Security), tipos, restricciones e índices correctos. Úsala para cualquier tabla, columna, índice, vista, función o trigger nuevo o modificado.
---

# Nueva migración Flyway

> Skill de desarrollo del equipo de agentes de inventario-saas · Intención: **desarrollar** · Dominio: **software** · Versión: **1.0** · Creada: 2026-10-24

Carpeta: `apps/api/src/main/resources/db/migration/`. Lee `docs/conocimiento/bases-de-datos.md` y ADR-0002.

## 1. Nombre
`V<siguiente-n>__<descripcion_en_snake>.sql` (doble guion bajo). Mira el número más alto existente.
**Nunca** modifiques una migración ya aplicada/commiteada.

## 2. Plantilla de tabla de negocio
```sql
CREATE TABLE producto (
    id             uuid PRIMARY KEY,
    tienda_id      uuid NOT NULL REFERENCES tienda (id),
    sku            text NOT NULL CHECK (length(sku) BETWEEN 1 AND 64),
    nombre         text NOT NULL CHECK (length(nombre) BETWEEN 1 AND 200),
    precio_venta   numeric(14,2) NOT NULL CHECK (precio_venta >= 0),
    moneda         char(3) NOT NULL DEFAULT 'PEN',
    activo         boolean NOT NULL DEFAULT true,
    version        bigint NOT NULL DEFAULT 0,
    creado_en      timestamptz NOT NULL DEFAULT now(),
    actualizado_en timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT uq_producto_tienda_sku UNIQUE (tienda_id, sku)
);

CREATE INDEX ix_producto_tienda_nombre ON producto (tienda_id, nombre);

ALTER TABLE producto ENABLE ROW LEVEL SECURITY;
ALTER TABLE producto FORCE ROW LEVEL SECURITY;
CREATE POLICY aislamiento_tienda ON producto
    USING (tienda_id = current_setting('app.tienda_id')::uuid)
    WITH CHECK (tienda_id = current_setting('app.tienda_id')::uuid);

GRANT SELECT, INSERT, UPDATE ON producto TO app_inventario;
GRANT SELECT ON producto TO app_lectura;
```

## 3. Lista de verificación
- [ ] `tienda_id` + RLS habilitado **y forzado** + política (salvo tablas globales justificadas: `tienda`, `plan`).
- [ ] FK con índice que empieza por `tienda_id`; `UNIQUE` siempre incluye `tienda_id`.
- [ ] Dinero `numeric(14,2)`, cantidades `numeric(14,3)`, fechas `timestamptz`; nada de `float`/`money`.
- [ ] `CHECK` para invariantes; `NOT NULL` por defecto.
- [ ] `GRANT` mínimos a `app_inventario`/`app_lectura` (sin `DELETE` en tablas históricas).
- [ ] Tablas solo-inserción (movimientos, auditoría) con trigger que impide UPDATE/DELETE.
- [ ] Migración compatible hacia atrás con la versión anterior del backend (añadir antes de quitar).
- [ ] Índices sobre tablas grandes en Fase 2+: `CREATE INDEX CONCURRENTLY` en una migración aparte que
      Flyway ejecute fuera de transacción (archivo de configuración del script `V<n>__x.sql.conf` con
      `executeInTransaction=false`; confirmar la sintaxis en la documentación de la versión de Flyway usada).
- [ ] Actualizar `docs/modelo-datos.md` (Mermaid `erDiagram`).

## 4. Probar
`./mvnw -B -Dtest='*Migracion*,*Aislamiento*' verify` con Testcontainers; luego entrega a `backend` y `qa`.
