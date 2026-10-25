---
name: nueva-pantalla
description: Crea una pantalla o flujo en apps/web de inventario-saas (React 19 + TanStack Router/Query/Table + shadcn/ui + React Hook Form/Zod) usando el cliente generado por Orval, con estados de carga/vacío/error/sin permiso, accesibilidad y pruebas. Úsala para cualquier vista nueva o rediseño de una existente.
---

# Nueva pantalla web

> Skill de desarrollo del equipo de agentes de inventario-saas · Intención: **desarrollar** · Dominio: **software** · Versión: **1.0** · Creada: 2026-10-24

1. **Requisitos**: tarea del tablero, endpoints en `docs/contratos/openapi.yaml` y diseño/indicaciones de
   `diseno-ui` en `docs/diseno/`. Si el endpoint no existe, entrega a `backend`/`arquitecto` (skill
   `nuevo-endpoint`) en vez de simularlo.
2. **Cliente**: regenera con Orval; usa los hooks generados (`useListarProductos`, ...). Nada de `fetch` manual.
3. **Ruta** (TanStack Router) en `apps/web/src/rutas/<modulo>/...`; valida `search params` con Zod
   (paginación, filtros) para que la URL sea compartible.
4. **Componentes**: shadcn/ui + tokens de `packages/ui`. Tablas con TanStack Table y paginación del
   servidor. Formularios con React Hook Form + `zodResolver`; mapear `errores` del `problem+json` a campos.
5. **Estados obligatorios**: cargando (skeleton), vacío (con acción principal), error (mensaje + reintentar),
   sin permiso, y en escritorio sin conexión.
6. **Textos**: términos de `docs/glosario.md`; montos con `Intl.NumberFormat('es-PE', {style:'currency', currency})`.
7. **Accesibilidad**: etiquetas en campos, foco al abrir diálogos, todo operable con teclado, contraste AA.
8. **Pruebas**: Vitest + Testing Library (render, interacción principal, error). Mock de la API con MSW.
9. **Verificar**: `pnpm --filter web lint test build`; abrir en el navegador (escritorio y 390 px de ancho),
   consola sin errores.
10. Entrega a `qa` (E2E) y `documentacion` (manual) con la skill `entrega-entre-agentes`.
