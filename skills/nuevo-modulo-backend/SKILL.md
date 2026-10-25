---
name: nuevo-modulo-backend
description: Crea la estructura de un módulo nuevo del monolito modular Spring Boot de inventario-saas (paquetes api/dominio/aplicacion/infraestructura/web, límites con Spring Modulith, eventos). Úsala al empezar un módulo de docs/arquitectura.md §3 que aún no existe.
---

# Nuevo módulo backend

> Skill de desarrollo del equipo de agentes de inventario-saas · Intención: **desarrollar** · Dominio: **software** · Versión: **1.0** · Creada: 2026-10-24

1. Confirma que el módulo figura en `docs/arquitectura.md` §3. Si no, pide al `arquitecto` agregarlo.
2. Estructura en `apps/api/src/main/java/pe/inventario/saas/<modulo>/`:

```
<modulo>/
  package-info.java        // @org.springframework.modulith.ApplicationModule(displayName = "...")
  api/                     // lo ÚNICO que otros módulos pueden usar: interfaces, records, eventos públicos
  dominio/                 // entidades, value objects, reglas, excepciones de dominio, puertos (interfaces)
  aplicacion/              // casos de uso (@Service, @Transactional), uno por intención: RegistrarVenta
  infraestructura/         // repositorios JPA, adaptadores externos (implementan puertos)
  web/                     // @RestController + DTOs de la API + mapeadores MapStruct
```

3. Reglas de dependencia: `web → aplicacion → dominio ← infraestructura`; nadie fuera del módulo importa
   `dominio`, `aplicacion` ni `infraestructura` de otro módulo. Comunicación entre módulos: `api` (llamada
   síncrona) o eventos registrados en `docs/contratos/eventos.md`.
4. Entidades con `tienda_id` (`@TenantId` o filtro) — ver ADR-0002.
5. Prueba de arquitectura: `ApplicationModules.of(Aplicacion.class).verify()` (Modulith) o regla ArchUnit
   equivalente mientras no esté Modulith.
6. Prueba `@ApplicationModuleTest` o de integración del primer caso de uso.
7. Entrega a `qa` y, si publica eventos, a `mensajeria`.
