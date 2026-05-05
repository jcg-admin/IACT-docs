```yml
created_at: 2026-05-04 05:21:29
project: IACT-docs
work_package: 2026-05-04-05-21-29-arqtecnica-pascalcase-fix
phase: Phase 8 — PLAN EXECUTION
author: NestorMonroy
status: En curso
```

# Task Plan — Renombrar Directorios PascalCase en arquitectura-tecnica

## Bloque A — Renombrar directorios via git mv

- [x] **T-001** `git mv ArquitecturaSistema arquitectura-sistema`
- [x] **T-002** `git mv BoundedContexts bounded-contexts`
- [x] **T-003** `git mv DeployView deploy-view`
- [x] **T-004** `git mv DesignView design-view`
- [x] **T-005** `git mv DomainModel domain-model`
- [x] **T-006** `git mv ImplementationView implementation-view`
- [x] **T-007** `git mv ProcessView process-view`
- [x] **T-008** `git mv UCModuleView uc-module-view`
- [x] **T-009** `git mv UMLSystemView uml-system-view`
- [x] **T-010** `git mv UseCaseView use-case-view`

## Bloque B — Actualizar referencias externas

- [x] **T-011** Actualizar `arquitectura-sistema.rst` (3 refs a ArquitecturaSistema)
- [x] **T-012** Actualizar `diagramas-uml-sistema.rst` (12 refs a UMLSystemView)
- [x] **T-013** Actualizar `modelo-dominio-iact.rst` (9 refs a BoundedContexts)
- [x] **T-014** Actualizar `vistas-kruchten.rst` (12 refs a 6 directorios Kruchten)
- [x] **T-015** Actualizar `diagramas-uc-por-modulo.rst` (refs a UCModuleView)
- [x] **T-016** Verificar que no queden refs a nombres PascalCase

## Bloque C — Verificación y commit

- [ ] **T-017** Verificar build (make html)
- [ ] **T-018** Commit: "Rename PascalCase dirs to kebab-case (STD-007)"
