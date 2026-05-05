```yml
created_at: 2026-05-04 05:21:29
project: IACT-docs
work_package: 2026-05-04-05-21-29-arqtecnica-pascalcase-fix
phase: Phase 11 — TRACK
author: NestorMonroy
status: En curso
```

# Changelog — Renombrar Directorios PascalCase en arquitectura-tecnica

## Changed

- `ArquitecturaSistema/` → `arquitectura-sistema/` (T-001, 3 archivos)
- `BoundedContexts/` → `bounded-contexts/` (T-002, 10 archivos)
- `DeployView/` → `deploy-view/` (T-003, 81 archivos)
- `DesignView/` → `design-view/` (T-004, 161 archivos)
- `DomainModel/` → `domain-model/` (T-005, 161 archivos)
- `ImplementationView/` → `implementation-view/` (T-006, 81 archivos)
- `ProcessView/` → `process-view/` (T-007, 81 archivos)
- `UCModuleView/` → `uc-module-view/` (T-008, 14 archivos)
- `UMLSystemView/` → `uml-system-view/` (T-009, 13 archivos)
- `UseCaseView/` → `use-case-view/` (T-010, 81 archivos)
- `arquitectura-sistema.rst`: toctree refs actualizadas (T-011)
- `diagramas-uml-sistema.rst`: 12 refs UMLSystemView → uml-system-view (T-012)
- `modelo-dominio-iact.rst`: 9 refs BoundedContexts → bounded-contexts (T-013)
- `vistas-kruchten.rst`: 12 refs a 6 vistas Kruchten actualizadas (T-014)
- `diagramas-uc-por-modulo.rst`: 13 refs UCModuleView → uc-module-view (T-015)

## Origen

STD-007 §3.1 exige minúsculas exclusivamente con guión medio. Los 10
subdirectorios fueron creados con PascalCase siguiendo instrucciones del
usuario, sin priorizar el estándar. Detectado en sesión 2026-05-04.

## Status de promoción a CHANGELOG.md raíz

Pendiente — WP en curso (falta verificación build T-017 y commit T-018).
