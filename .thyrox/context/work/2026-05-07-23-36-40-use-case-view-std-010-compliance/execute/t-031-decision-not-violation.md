```yml
created_at: 2026-05-07 23:59:00
project: IACT-docs
work_package: 2026-05-07-23-36-40-use-case-view-std-010-compliance
phase: Phase 10 — EXECUTE
author: NestorMonroy
status: Aprobado
version: 1.0.0
type: Decision (no-op task)
```

# T-031 — Decision: no es violacion STD-010 §4

## Contexto

El audit identifico `actor "User" as User <<sistema>>` en
`source/arquitectura-tecnica/use-case-view/reports/uc-rpt-11-compartir-reporte.rst:38`
como potencial violacion (Cat-D actor "User" generico).

## Re-evaluacion semantica

Tras lectura del archivo completo, **el actor `User` en
linea 38 representa la entidad domain-model `User` (clase),
NO un actor humano**.

Evidencias:

- Stereotype `<<sistema>>` (no `<<beneficiario>>` ni
  humano).
- Coexiste con otros actores entidad: `AccessGroup
  <<sistema>>`, `SavedView <<sistema>>`.
- La flecha `RECEPTOR_VAL --> User` (linea 64) apunta a
  esta entidad para validar que el receptor existe.
- El actor humano del UC esta en linea 32:
  `actor "share_reports" as share_reports` (codename
  correcto) y linea 33: `actor "Receptor User/AGR" as
  Receptor <<beneficiario>>` (descripcion del rol del
  receptor).

## Distincion STD-010 §4

STD-010 §4 prohibe nombres institucionales para actores
humanos:

```
' PROHIBIDO (humano sin codename)
actor "Analista de Datos" as U
actor "Administrador" as A
```

Pero NO prohibe entidades del domain-model como actores con
`<<sistema>>` stereotype. Estas representan clases del
modelo, NO personas. Patron observado en multiples archivos:
`AccessGroup`, `SavedView`, `Call`, `Session` aparecen como
actores `<<sistema>>` legitimamente.

## Conclusion

`actor "User" as User <<sistema>>` en uc-rpt-11 **NO es
violacion**. Es la entidad domain-model `User` referenciada
para validacion de receptor.

T-031 se cierra sin cambios. Marca [x] en task-plan.

## Refs

- STD-010 §4 (reglas de diagramas UML).
- D-DIAG-001 (codenames RBAC en diagramas).
- discover/std-010-audit.md (audit inicial).
- discover/deep-audit-extended.md (audit profundo).
