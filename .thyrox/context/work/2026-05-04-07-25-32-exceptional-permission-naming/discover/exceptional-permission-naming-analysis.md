```yml
created_at: 2026-05-04 07:25:32
project: IACT-docs
work_package: 2026-05-04-07-25-32-exceptional-permission-naming
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# Discover — ExceptionalPermission vs ExceptionalGrant

## Problema

Dos nombres distintos para el mismo concepto de dominio:
- `ExceptionalPermission` — usado en UC docs, arquitectura, bounded context
- `ExceptionalGrant` — propuesto en `adr-back-006 §2.4` como rename canónico

## Evidencia de distribución (PROVEN via grep)

### ExceptionalPermission (dominante — 80+ ocurrencias)

**Arquitectura técnica:**
- `bounded-context-rbac.rst` — UML class diagram: `class ExceptionalPermission`
- `bounded-contexts/overview.rst` — `class ExceptionalPermission`
- `domain-model/conceder-permiso-excepcional-domain-model.rst`
- `domain-model/permiso-temporal-domain-model.rst`
- `domain-model/revocar-permiso-excepcional-domain-model.rst`
- `matriz-dependencias-uc-iact.rst` (4 ocurrencias)
- `modelo-dominio-iact.rst`

**Casos de uso (implementados, con archivos):**
- `uc-acc-03/` (múltiples subdoc)
- `uc-acc-08/` (múltiples subdoc, incluyendo diagrama de estados)
- `uc-perm-03/`, `uc-perm-04/`, `uc-perm-07/`, `uc-perm-08/`
- `uc-auth-01/`
- `fr-014-01-validar-permiso-excepcional.rst`

**Repository pattern establecido:**
- `ExceptionalPermissionRepository` (interface de repositorio en UC docs)
- `ExceptionalPermissionRepo` (abrev. en diagramas)

### ExceptionalGrant (aislado — 1 ocurrencia)

- `adr-back-006-rbac-estrategia-implementacion.rst:191`
  ```
  * - ``PermisoExcepcional``
    - ``ExceptionalGrant``
    - Sustantivo apropiado al scope
  ```

## Análisis

`ExceptionalGrant` fue propuesto en `adr-back-006 §2.4` como tabla de
renames de modelos Django legacy → canónico. Sin embargo:

1. **Nunca fue adoptado** — ningún otro documento del corpus lo usa.
2. **`ExceptionalPermission` es el estándar de facto** — 80+ ocurrencias
   en documentos de arquitectura y UC con implementación real.
3. **El patrón de nombre es coherente con el dominio**: `exceptional`
   adjetivo + `permission` sustantivo (el concepto es un permiso que es
   excepcional, no una concesión/grant). Comparable: `FunctionGroup`,
   `SeparationRule`, `UserFunctionGrant` (el grant es la operación de
   asignar, no el objeto resultante).
4. **Repository interface ya nombrado**: `ExceptionalPermissionRepository`
   está definido en UC docs como contrato de datos — cambiarlo requeriría
   actualizar todos los contratos.

## Decisión

`ExceptionalPermission` es el nombre canónico para el objeto de dominio.
`adr-back-006 §2.4` debe corregirse: `ExceptionalGrant` → `ExceptionalPermission`.

**Nota sobre `UserFunctionGrant`:** ese sí usa "Grant" correctamente —
es la entidad de asignación directa user→function (acto de conceder).
`ExceptionalPermission` es distinto: es el registro del permiso
excepcional vigente, no el acto de concesión.
