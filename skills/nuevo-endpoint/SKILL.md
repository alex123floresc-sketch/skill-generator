---
name: nuevo-endpoint
description: Flujo "contrato primero" para agregar o cambiar un endpoint HTTP de inventario-saas - openapi.yaml, implementación Spring Boot, pruebas, regeneración del cliente Orval y entrega a frontend/escritorio. Úsala siempre que una funcionalidad necesite una ruta nueva o cambie una existente.
---

# Nuevo endpoint (contrato primero)

> Skill de desarrollo del equipo de agentes de inventario-saas · Intención: **desarrollar** · Dominio: **software** · Versión: **1.0** · Creada: 2026-10-24

## 1. Contrato — `docs/contratos/openapi.yaml`
- Ruta bajo `/api/v1/<recurso-en-plural-kebab>`; `operationId` en español camelCase (`listarProductos`).
- Tag = módulo (`catalogo`, `inventario`, ...). Términos de `docs/glosario.md`.
- Reutiliza `Dinero`, `Pagina`, `Problema` y las respuestas `NoAutenticado`, `SinPermiso`, `NoEncontrado`.
- Listas: parámetros `pagina`, `tamano` (máx. 100), `orden`; respuesta `{ items: [...], pagina: Pagina }`.
- Documenta cada error de negocio con su `code` (`STOCK_INSUFICIENTE`, `SKU_DUPLICADO`).
- Nunca un parámetro `tiendaId`: el tenant sale del token.
- Cambio incompatible ⇒ nueva versión o campo nuevo opcional; nunca romper a web/escritorio en silencio.
- Si no eres el `arquitecto`, deja la propuesta en una entrega para su aprobación antes de implementar
  algo grande; cambios pequeños y compatibles pueden ir en el mismo PR y él los revisa.

## 2. Implementación — `apps/api`
- Controlador en `<modulo>.web` → caso de uso en `<modulo>.aplicacion` → dominio.
- DTOs `record` con Bean Validation; MapStruct para mapear.
- `@PreAuthorize` con el permiso; transacción en el caso de uso.
- Errores de negocio con `ReglaNegocioException(codigo)`.

## 3. Pruebas
- Unitarias del caso de uso.
- Integración (MockMvc/RestAssured + Testcontainers): éxito, validación (400), sin token (401),
  sin permiso (403), **recurso de otra tienda (404)**.
- Comprobar que springdoc genera lo mismo que el contrato (diff en CI).

## 4. Cliente y entrega
- `pnpm --filter api-client generate` (Orval) y compilar `apps/web`.
- Entrega a `frontend` (y `escritorio` si aplica) y a `qa` con la skill `entrega-entre-agentes`.
