```yml
created_at: 2026-05-04 15:02:00
project: THYROX
work_package: 2026-05-04-14-59-45-uml-coverage-context-view
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
```

# WP-1: uml-coverage-context-view — Scope

## Problema

El viewpoint Context (Rozanski & Woods) está ausente como vista canónica en
`arquitectura-tecnica/`. Solo existe un DFD nivel 0 parcial (`arquitectura-sistema/
dfd-nivel-0-contexto.rst`) con un bug de PlantUML (aliases undefined).

## Prescripción base-cognitiva

- `vistas-y-viewpoints.rst`: Context = viewpoint overarching, informa a todos los demás
- `contexto-empirico.rst`: Context = HIGH importancia para IACT
- `proceso-definicion-arquitectonica.rst` Tabla 7-1: Salida = "borrador de vista Context con IVR como actor externo"

## Alcance del WP

1. **Fix G-04**: Corregir aliases PlantUML en `arquitectura-sistema/dfd-nivel-0-contexto.rst`
2. **Crear `arquitectura-tecnica/context-view/`**:
   - `index.rst` — índice del viewpoint
   - `context-diagram.rst` — System boundary diagram completo (stakeholders, externos, interfaces)
   - `external-interfaces.rst` — Definición de interfaces externas (IVR/MariaDB, AD, APScheduler)
   - `stakeholders.rst` — Mapa de stakeholders (AGR_ADMIN, AGR_OPERADOR, AGR_AUDITOR, instituciones)
3. **Actualizar `vistas-kruchten.rst`**: Agregar `context-view/index` al toctree
4. **Actualizar `framework-rozanski.rst`**: Marcar Context viewpoint como implementado

## Criterios de aceptación

- [ ] `context-view/index.rst` referenciado en `vistas-kruchten.rst`
- [ ] Context diagram renderiza en PlantUML (sin aliases undefined)
- [ ] External interfaces documentan protocolo, dirección y restricciones (P-01: IVR read-only)
- [ ] Stakeholders identificados con roles RBAC
- [ ] Build verde sin warnings nuevos
