```yml
created_at: 2026-05-04 15:02:00
project: THYROX
work_package: 2026-05-04-15-00-00-uml-coverage-housekeeping
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
```

# WP-3: uml-coverage-housekeeping — Scope

## Problema

Tres defectos menores detectados en el audit de cobertura _uml que no justifican WPs
separados pero deben resolverse antes de cerrar el audit.

## Tareas

### T-1: Eliminar directorio stub vacío `rbac/raci-rbac-iact/`
- `arquitectura-tecnica/rbac/raci-rbac-iact/` = 0 archivos (stub residual de Bloque G)
- Los RACI están correctamente en `normativa/gobernanza/raci-rbac/`
- El toctree de `rbac/index.rst` ya fue corregido (usa seealso, no toctree)
- Acción: `rm -rf arquitectura-tecnica/rbac/raci-rbac-iact/`

### T-2: Corregir título de `vistas-kruchten.rst`
- Título actual: "Vista de Casos de Uso — Arquitectura Tecnica" (incorrecto)
- Título correcto: "Vistas Arquitectónicas — Modelo 5+1 IACT"
- El artefacto en metadata ya es correcto: `INDEX_AT_VISTAS_KRUCHTEN`

### T-3: Fix PlantUML en `dfd-nivel-0-contexto.rst` (G-04)
- Aliases usados: `IVR`, `SUP`, `ANA`, `SCH` (no definidos)
- Aliases definidos: `SistemaIVR`, `SupervisorSistema`, `AnalistaReportes`, `DisparadorScheduler`
- El diagrama no renderiza actualmente
- Acción: corregir las 4 referencias de alias en las flechas

## Criterios de aceptación

- [ ] `rbac/raci-rbac-iact/` eliminado
- [ ] `vistas-kruchten.rst` título corregido
- [ ] DFD Nivel 0 renderiza sin error PlantUML
- [ ] Build verde sin warnings nuevos
