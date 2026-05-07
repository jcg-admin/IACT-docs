```yml
project: IACT-docs
work_package: 2026-05-07-04-50-49-std-012-prefix-normalization
created_at: 2026-05-07 04:50:49
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-elicitation
size: TBD (depende del inventario Phase 1)
target: Resolver inconsistencia normativa STD-011 vs STD-012 sobre prefijo `diagrama-de-` en archivos UML de UCs. Actualizar STD-012 a v1.1.0 con prefijo obligatorio. Aplicar las operaciones de archivo (renames + deletes) en commit dedicado separado del cambio normativo. Approach: Opcion B aprobada por ejecutor.
predecessor_wp: 2026-05-07-04-08-13-use-case-view-analysis (G-CU-06 escindido aqui)
trigger: directiva del ejecutor "abre un nuevo wp en donde realices un analisis de cuantos se van a actualizar" tras aprobar Opcion B
```

# WP — STD-012 v1.1.0 Prefix Normalization

## Trigger

Durante la ejecucion del WP previo
``2026-05-07-04-08-13-use-case-view-analysis`` se detecto
**inconsistencia normativa critica**:

- ``STD-012`` (Tipos de Diagramas UML, v1.0.0) prescribe
  nombres **sin prefijo**: ``caso-de-uso.rst``,
  ``actividad.rst``, ``secuencia.rst``, ``clases.rst``,
  ``estados-{entidad}.rst``.
- ``STD-011`` (Aliases auto-documentados) usa en sus
  ejemplos canonicos **con prefijo**:
  ``diagrama-de-caso-de-uso.rst``,
  ``diagrama-de-secuencia.rst``, etc.
- La practica reciente del proyecto (UCs nuevos
  uc-acc-02, uc-auth-01, uc-perm-08, UC_ADM_04/05) ya
  migro al prefijo.

El ejecutor aprobo la **Opcion B**: actualizar STD-012 a
v1.1.0 con prefijo obligatorio + renombrar archivos legacy
+ eliminar pares duplicados.

## Output esperado del WP

**Phase 1 DISCOVER:**

- Inventario exhaustivo de archivos legacy (caso-de-uso,
  actividad, secuencia, clases, estados-*) por cluster.
- Inventario de archivos canonicos existentes con prefijo.
- Detección de **conflictos** (¿hay archivos legacy SIN
  contraparte canonica que requieran rename + recreate?).
- Identificación de toctree afectados.
- Identificación de cross-refs externos que romperian.
- Plan de ejecucion en lotes con orden de dependencias.

**Phase 7 DESIGN/EXECUTE (post-aprobacion):**

- Commit 1: STD-012 v1.1.0 con prefijo obligatorio +
  changelog explicito de la razon del cambio.
- Commit 2: renames + deletes de archivos + toctree
  updates en commit dedicado.

**Phase 11 TRACK:**

- Verificacion: build sphinx strict EXIT=0.
- Verificacion: 0 archivos legacy restantes.
- Verificacion: cross-refs todos validos.
- Changelog del WP + lessons learned.

## Restricciones

- Phase 1 NO modifica source/ — solo analisis.
- STD-012 v1.1.0 modifica **unicamente** las secciones de
  nomenclatura de archivos de diagrama. No debe tocar
  nada mas (condicion del ejecutor).
- Las operaciones de archivo van en commit **dedicado**
  separado del cambio normativo (condicion del ejecutor).
- Strict build (`-W`) tras cualquier cambio.

## Stopping points

- **SP-01** (humano): aprobar el plan de ejecucion antes
  de Phase 7 (cuantos archivos exactos, riesgos
  detectados).
- **SP-02:** strict build EXIT=0 tras commit normativo.
- **SP-03:** strict build EXIT=0 tras commit de renames.
- **SP-04** (humano): aprobar cierre del WP.

## Items diferidos al WP previo

El WP previo
``2026-05-07-04-08-13-use-case-view-analysis`` queda con
2 items pendientes:

- G-CU-06: resuelto en este WP (escindido).
- G-CU-08: 40 archivos TBD/TODO/FIXME — se procesa al
  cierre de este WP.

## Hipotesis iniciales

1. Total de archivos legacy: ~133 (49 caso-de-uso + 46
  actividad + 24 secuencia + 14 clases).
2. Total de archivos canonicos existentes: 83 cdu + 31
  actividad + (TBD secuencia) + 0 clases.
3. Pares duplicados: 49 cdu requieren delete legacy
  (canonical preservado).
4. Solo legacy sin canonical: 84 archivos requieren
  rename (no delete — son la unica version).
5. Toctree afectados: ~85 (uno por UC).
6. Cross-refs externos: bajo (solo STD-012 mismo + posibles
  notas en otros archivos).
