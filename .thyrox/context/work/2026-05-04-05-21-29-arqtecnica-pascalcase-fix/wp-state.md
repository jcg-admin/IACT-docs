```yml
project: IACT-docs
work_package: 2026-05-04-05-21-29-arqtecnica-pascalcase-fix
created_at: 2026-05-04 05:21:29
current_phase: Phase 10 — IMPLEMENT
flow: thyrox
methodology_step: thyrox:implement
author: NestorMonroy
status: En curso
```

# WP — Renombrar Directorios PascalCase en arquitectura-tecnica

## Origen

STD-007 §3.1 exige minúsculas exclusivamente con guión medio como separador.
Los 10 subdirectorios de `source/arquitectura-tecnica/` usan PascalCase —
violación detectada por el ejecutor. Los directorios fueron creados siguiendo
instrucciones del usuario sin priorizar STD-007.

## Scope

10 directorios a renombrar:

| Actual (PascalCase) | Correcto (kebab-case) |
|---------------------|----------------------|
| `ArquitecturaSistema` | `arquitectura-sistema` |
| `BoundedContexts` | `bounded-contexts` |
| `DeployView` | `deploy-view` |
| `DesignView` | `design-view` |
| `DomainModel` | `domain-model` |
| `ImplementationView` | `implementation-view` |
| `ProcessView` | `process-view` |
| `UCModuleView` | `uc-module-view` |
| `UMLSystemView` | `uml-system-view` |
| `UseCaseView` | `use-case-view` |

49 referencias externas a actualizar (verificado con grep).
