```yml
created_at: 2026-05-02 06:33:05
project: IACT-docs
work_package: 2026-05-02-06-33-05-rbac-cajones
phase: Phase 8 — PLAN EXECUTION
author: NestorMonroy
status: En ejecución
```

# Task Plan — rbac-cajones

## Objetivo

Reestructurar los 2 archivos planos de `source/arquitectura-tecnica/rbac/` en
subdirectorios cajones, siguiendo el patrón aplicado a `modulos/`. Agregar
diagramas PlantUML donde no existen. Actualizar `rbac/index.rst` con toctrees
a los nuevos cajones.

## Archivos a reemplazar

| Archivo plano | Cajón destino |
|---------------|---------------|
| `rbac/modelo-rbac-iact.rst` | `rbac/modelo-rbac-iact/` (11 archivos) |
| `rbac/raci-rbac-iact.rst` | `rbac/raci-rbac-iact/` (7 archivos) |

---

## Tareas

### T-001 — Crear `modelo-rbac-iact/index.rst`
- [ ] `.. _modelo-rbac-iact:` label
- [ ] Título, propósito (model conceptual canónico RBAC IACT v5.4.0)
- [ ] Toctree apuntando a: filosofia, arquitectura, catalogo-funciones,
      grupos-funciones, sod, permisos-temporales, modelo-datos,
      implementacion, mapeo-uc, diagramas, resumen
- [ ] Nota de referencias a CNST_029/030/031

### T-002 — Crear `modelo-rbac-iact/filosofia.rst`
- [ ] Label `.. _modelo-rbac-iact-filosofia:`
- [ ] Extraer sección 1 FILOSOFÍA (L348–L387): principio central + enfoque sin pretensiones

### T-003 — Crear `modelo-rbac-iact/arquitectura.rst`
- [ ] Label `.. _modelo-rbac-iact-arquitectura:`
- [ ] Extraer sección 2 ARQUITECTURA (L388–L456): distribución de 61 funciones

### T-004 — Crear `modelo-rbac-iact/catalogo-funciones.rst`
- [ ] Label `.. _modelo-rbac-iact-catalogo:`
- [ ] Extraer sección 3 CATÁLOGO (L457–L1069): 8 subsecciones MOD_Auth..MOD_Logs
- [ ] Preservar todas las list-tables de funciones con códigos, descripción,
      restricciones, notas de versión

### T-005 — Crear `modelo-rbac-iact/grupos-funciones.rst`
- [ ] Label `.. _modelo-rbac-iact-grupos:`
- [ ] Extraer sección 4 GRUPOS (L1070–L1354): catálogo de grupos AGR-001..010
      + detalle por grupo

### T-006 — Crear `modelo-rbac-iact/sod.rst`
- [ ] Label `.. _modelo-rbac-iact-sod:`
- [ ] Extraer sección 5 SoD (L1355–L1457): SOD-001..003 con reglas, rationale,
      consecuencias

### T-007 — Crear `modelo-rbac-iact/permisos-temporales.rst`
- [ ] Label `.. _modelo-rbac-iact-permisos-temporales:`
- [ ] Extraer sección 6 (L1458–L1507): concepto, reglas, ejemplo

### T-008 — Crear `modelo-rbac-iact/modelo-datos.rst`
- [ ] Label `.. _modelo-rbac-iact-modelo-datos:`
- [ ] Extraer sección 7 (L1508–L1527): tablas del modelo de datos

### T-009 — Crear `modelo-rbac-iact/implementacion.rst`
- [ ] Label `.. _modelo-rbac-iact-implementacion:`
- [ ] Extraer secciones 8+9 (L1528–L2879): SQL + Django implementation
- [ ] Preservar todos los code-blocks SQL y Python intactos

### T-010 — Crear `modelo-rbac-iact/mapeo-uc.rst`
- [ ] Label `.. _modelo-rbac-iact-mapeo-uc:`
- [ ] Extraer sección 10 (L2550–L2730): tabla completa funciones → UCs

### T-011 — Crear `modelo-rbac-iact/resumen.rst`
- [ ] Label `.. _modelo-rbac-iact-resumen:`
- [ ] Extraer secciones 11+12 (L2731–L2935): migración v5.2.0 + resumen + métricas

### T-012 — Crear `modelo-rbac-iact/diagramas.rst` (NUEVO — no existe en original)
- [ ] Label `.. _modelo-rbac-iact-diagramas:`
- [ ] Diagrama 1: class diagram jerarquía conceptual RBAC (User ↔ Assignment ↔
      Function ↔ FunctionGroup ↔ SoDRule)
- [ ] Diagrama 2: sequence diagram enforcement flow (request → AuthGuard →
      FunctionCheck → SoDValidation → response)
- [ ] Diagrama 3: activity diagram asignación de función con validación SoD

### T-013 — Crear `raci-rbac-iact/index.rst`
- [ ] `.. _raci-rbac-iact:` label
- [ ] Toctree: stakeholders, raci-modulo, raci-grupos, raci-sod, raci-gobernanza,
      convenciones, trazabilidad

### T-014 — Crear `raci-rbac-iact/stakeholders.rst`
- [ ] Label `.. _raci-rbac-iact-stakeholders:`
- [ ] Secciones 1+2 (L31–L107): convencion RACI + stakeholders identificados

### T-015 — Crear `raci-rbac-iact/raci-modulo.rst`
- [ ] Label `.. _raci-rbac-iact-modulo:`
- [ ] Sección 3 (L109–L727): RACI por módulo (MOD_Auth..MOD_Logs) con todas las tablas

### T-016 — Crear `raci-rbac-iact/raci-grupos.rst`
- [ ] Label `.. _raci-rbac-iact-grupos:`
- [ ] Sección 4 (L730–L814): RACI por grupo predefinido AGR-001..010

### T-017 — Crear `raci-rbac-iact/raci-sod.rst`
- [ ] Label `.. _raci-rbac-iact-sod:`
- [ ] Sección 5 (L817–L854): RACI sobre reglas SoD SOD-001..003

### T-018 — Crear `raci-rbac-iact/raci-gobernanza.rst`
- [ ] Label `.. _raci-rbac-iact-gobernanza:`
- [ ] Sección 6 (L856–L934): RACI sobre operaciones de gobernanza

### T-019 — Crear `raci-rbac-iact/convenciones.rst`
- [ ] Label `.. _raci-rbac-iact-convenciones:`
- [ ] Secciones 7+9+10 (L935..L1074): convenciones de uso + mantenimiento +
      fundamento documental

### T-020 — Crear `raci-rbac-iact/trazabilidad.rst`
- [ ] Label `.. _raci-rbac-iact-trazabilidad:`
- [ ] Sección 8 (L967–L986): trazabilidad con :doc: links a normativa/restricciones

### T-021 — Actualizar `rbac/index.rst`
- [ ] Cambiar toctree de `modelo-rbac-iact` → `modelo-rbac-iact/index`
- [ ] Cambiar toctree de `raci-rbac-iact` → `raci-rbac-iact/index`

### T-022 — Eliminar archivos planos reemplazados
- [ ] `rm source/arquitectura-tecnica/rbac/modelo-rbac-iact.rst`
- [ ] `rm source/arquitectura-tecnica/rbac/raci-rbac-iact.rst`

### T-023 — Build 0 warnings
- [ ] `make html` → 0 warnings, exit 0
- [ ] Fix any RST transition / orphan / reference issues

### T-024 — Commit y push
- [ ] `git add -A && git commit` (Tim Pope style)
- [ ] `git push -u origin claude/review-ucs-work-state-phwmj`
- [ ] Actualizar WP changelog
