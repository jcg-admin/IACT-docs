```yml
created_at: 2026-05-04 15:02:00
project: THYROX
work_package: 2026-05-04-15-00-30-uml-coverage-operational-view
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
```

# WP-2: uml-coverage-operational-view — Scope

## Problema

El viewpoint Operational (Rozanski & Woods) está completamente ausente en `arquitectura-tecnica/`.
Es el único viewpoint de Rozanski sin equivalente en ningún otro framework (Kruchten, Soni,
Clements, Garland). Para IACT es de importancia HIGH (auditoría, monitorización, soporte).

## Prescripción base-cognitiva

- `contexto-empirico.rst`: Operational = HIGH para IACT ("Auditoría, monitorización, soporte")
- `framework-rozanski.rst` Tabla 1: cubre system installation, administration, configuration,
  support, migration — con diagramas Activity, Class, Component, Composite Structure,
  Deployment, Object, Package, Profile, Sequence/Communication, State, Timing, Use case
- `frameworks-comparacion.rst`: "Operational no tiene cobertura en el modelo 5+1 actual"

## Alcance del WP

1. **Crear `arquitectura-tecnica/operational-view/`**:
   - `index.rst` — índice del viewpoint
   - `system-installation.rst` — instalación y bootstrap del sistema
   - `system-administration.rst` — administración: RBAC (AGR_ADMIN), gestión de usuarios,
     activación/desactivación, permisos temporales
   - `system-configuration.rst` — configuración: variables de entorno, parámetros ETL,
     umbrales de alerta, horarios APScheduler
   - `system-support.rst` — soporte: monitoreo de pipeline ETL, dashboards, alertas,
     procedimientos de diagnóstico
   - `system-migration.rst` — migración de datos IVR, runbooks Django migrations
2. **Actualizar `vistas-kruchten.rst`**: Agregar `operational-view/index` al toctree
3. **Actualizar `framework-rozanski.rst`**: Marcar Operational viewpoint como implementado

## Criterios de aceptación

- [ ] `operational-view/index.rst` referenciado en `vistas-kruchten.rst`
- [ ] Al menos 4 de los 5 model types cubiertos (installation, administration, configuration, support)
- [ ] Diagramas de actividad para flujos de administración (Use case para AGR_ADMIN)
- [ ] Referencia a CNST-029..CNST-033 (RBAC operacional)
- [ ] Build verde sin warnings nuevos
