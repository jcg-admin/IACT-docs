```yml
project: IACT-docs
work_package: 2026-05-07-04-08-13-use-case-view-analysis
created_at: 2026-05-07 04:08:13
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-elicitation
size: TBD (depende del Phase 1)
target: Auditar y analizar todo lo existente en source/arquitectura-tecnica/use-case-view/* (12 modulos + 2 panoramas + 1 index, ~101 archivos rst). Detectar gaps, inconsistencias, duplicaciones, violaciones de STD-010/STD-011, falta de cobertura UC ↔ catálogo RBAC, alineacion con UCs en source/requisitos/casos-uso/.
predecessor_wp: 2026-05-06-21-42-06-menu-rbac-user-scope-docs (cerrado, aprobado 2026-05-07 04:08)
trigger: directiva del ejecutor "vas a abrir uno nuevo para analizar lo que tenemos en source/arquitectura-tecnica/use-case-view/*"
```

# WP — Use-Case View Analysis

## Trigger

El ejecutor pidio analizar el cajon
``source/arquitectura-tecnica/use-case-view/`` que tiene
**101 archivos rst** distribuidos en 12 modulos + 2
panoramas + 1 index.

Estructura observada:

::

   source/arquitectura-tecnica/use-case-view/
   ├── index.rst
   ├── panorama-iact.rst
   ├── mapa-funciones-rbac.rst
   ├── access/         (cluster ACC)
   ├── admin/          (cluster ADM — recien extendido v5.6.x)
   ├── alerts/         (cluster ALR)
   ├── audit/          (cluster AUD)
   ├── auth/           (cluster AUTH)
   ├── caller/         (cluster CLI)
   ├── logs/           (cluster LOG)
   ├── operator/       (cluster OPR)
   ├── permissions/    (cluster PERM)
   ├── pipeline/       (cluster PIP)
   ├── reports/        (cluster RPT)
   ├── supervision/    (cluster SUP)
   └── users/          (cluster USR)

## Output esperado del WP

Phase 1 DISCOVER produce
``discover/use-case-view-audit.md`` con:

1. **Inventario completo** — listado de archivos por cluster
   con conteo de UCs, diagramas, tablas.
2. **Gap analysis vs catalogo RBAC**:
   - ¿Cada UC del catalogo tiene su entry en use-case-view?
   - ¿Cada entry de use-case-view tiene UC en catalogo?
   - Matriz de cobertura cluster-by-cluster.
3. **Gap analysis vs casos-uso/**:
   - ¿Cada uml-07 standalone en use-case-view tiene su spec
     completa en source/requisitos/casos-uso/?
   - ¿Hay UCs en casos-uso/ sin diagrama en use-case-view?
4. **Auditoria de conformidad**:
   - STD-010 (vocabulario abstracto) en participantes / actores.
   - STD-011 (aliases auto-documentados) en diagramas.
   - CNST-033 (conformidad UML).
   - Consistencia con catalogo de funciones (codenames RBAC).
5. **Detección de inconsistencias**:
   - Conteos desactualizados (e.g., total UCs por cluster).
   - Cross-refs rotos.
   - UCs duplicados (mismo UC en dos archivos).
   - Diagramas sin actores RBAC declarados.
6. **Stakeholders y stopping points** del WP.
7. **Recomendaciones** sobre que correcciones aplicar y en
   que orden.

## Restricciones

- **NO** modificar source/ en Phase 1 — solo analisis.
- Cumplir STD-010, STD-011 en cualquier output.
- Strict build (``-W``) tras cualquier cambio (Phase 7+ si
  aplica).
- R-2.0 — sin Monitor para builds <5min.

## Stopping points

- **SP-01** (humano): aprobar el inventario antes de
  Phase 3/5.
- **SP-02**: build strict 0 warnings tras cualquier cambio.
- **SP-03** (humano): aprobar el plan correctivo antes de
  Phase 7 DESIGN.

## Hipotesis iniciales (a validar en Phase 1)

1. El cluster ADM esta recien actualizado (v5.6.x extension);
   los demas clusters podrian tener desactualizaciones
   similares.
2. El conteo "85 UCs totales" en matriz-dependencias-uc-iact
   debe coincidir con la suma de UCs en cada cluster de
   use-case-view.
3. Algunos UCs reservados (OPR/SUP) podrian estar declarados
   en use-case-view como activos.
4. ``mapa-funciones-rbac.rst`` y ``panorama-iact.rst``
   podrian tener conteos desalineados (64/77 vs 67/80).
