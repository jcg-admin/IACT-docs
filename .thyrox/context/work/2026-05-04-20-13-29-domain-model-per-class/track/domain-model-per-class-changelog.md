```yml
created_at: 2026-05-04 20:20:00
updated_at: 2026-05-04 20:20:00
project: THYROX
work_package: 2026-05-04-20-13-29-domain-model-per-class
phase: Phase 11 — TRACK
author: NestorMonroy
status: Borrador
```

# Changelog — domain-model-per-class

## Removed

- **`arquitectura-tecnica/modulos/user-identity/diagramas/clases-modulo-identidad.rst`**
  — eliminado. Las 3 clases que contenía (User, Session, AuditEvent) son
  canónicas en `domain-model/` con atributos más completos. El archivo
  combinado tenía atributos desactualizados y no referenciaba la fuente
  de verdad. Filosofía StarUML: un archivo por clase, el índice navega
  sin duplicar contenido.

## Changed

- **`domain-model/user.rst`** (v1.1.0 → v1.2.0):
  - Agregada clase stub `AuditEvent` con 4 atributos esenciales.
  - Agregada relación `User "1" --> "0..*" AuditEvent : genera`.
  - Agregado `seealso` a `domain-model/audit-event`.
  - La relación User→AuditEvent era el único aporte único de
    `clases-modulo-identidad.rst` no presente en los archivos canónicos.

- **`modulos/user-identity/diagramas/index.rst`** (v1.0.0 → 1.1.0):
  - Eliminada entrada `clases-modulo-identidad` del toctree.
  - Agregada nota que las clases canónicas viven en `domain-model/`.
  - Agregado `seealso` a `domain-model/user`, `session`, `audit-event`.
  - Patrón StarUML: index como punto de navegación, no como contenido.

## Status de promoción a CHANGELOG.md raíz

Pendiente de merge a `main`. Entrada sugerida bajo `### Changed`:

```
- Eliminar clases-modulo-identidad.rst (atributos duplicados y
  desactualizados vs domain-model/). Integrar User→AuditEvent en
  domain-model/user.rst v1.2.0. Actualizar diagramas/index.rst para
  navegar a los archivos canónicos de domain-model/.
```
