```yml
project: IACT-docs
work_package: 2026-05-08-21-46-06-etl-ivr-flow-v2-doc
created_at: 2026-05-08 21:46:06
current_phase: Phase 1 — DISCOVER
status: Activo (pausa temporal de continuacion del DAG de vistas — prioridad del ejecutor)
author: NestorMonroy
flow: rm
methodology_step: rm-management
size: mediano-grande (documento source ~600 lineas, multiples niveles arquitectonicos, multiples ubicaciones candidatas en el corpus)
target: Documentar y aclarar el "Flujo ETL IVR v2.1" provisto por el ejecutor en el corpus IACT-docs. Adaptarlo al formato RST + vocabulario STD-010 + ubicacion canonica en arquitectura-tecnica/.
trigger: directiva del ejecutor "antes de continuar con este, es muy importante documentar y aclarar el [Flujo ETL IVR v2.1]"
```

# WP — Flujo ETL IVR v2.1 documentation

## Phase 1 — DISCOVER

### Que es el "Flujo ETL IVR v2.1"

Documento de ~600 lineas provisto por el ejecutor que describe
**completamente** el pipeline ETL del sistema IACT desde la
fuente IVR hasta los endpoints Django REST. El documento
**fusiona** dos documentos previos:

- `FLUJO-ETL-V2.md` (arquitectura sin codigo)
- `FLUJO-ETL-COMPLETO.md` (codigo v1 con nombres obsoletos)

Cubre **6 niveles arquitectonicos**:

- **Nivel 0** Funciones de utilidad (7 funciones SQL):
  `fn_did_segmento`, `fn_normalizar_centro`, `fn_normalizar_menu`,
  `fn_duracion_seg`, `ivr_es_dia_semana`,
  `ivr_contar_dias_semana`, `ivr_agregar_dias_semana`.
- **Nivel 1** Disparo del ETL (2 mecanismos):
  `evt_etl_diario` (MySQL Event 02:00 AM) y
  `manage.py run_etl` (Django command con heartbeat).
- **Nivel 2** Orquestacion con checkpoints:
  `sp_etl_maestro` con `job_execution_log`.
- **Nivel 3** ETLs especificos (`sp_etl_base_detalle`,
  `sp_etl_base_clientes`, `sp_etl_validar`,
  `sp_etl_historico`).
- **Nivel 4** Tablas intermedias y SPs de reporte (5 tablas
  + 7 SPs `sp_rpt_*`).
- **Nivel 5** Django REST Framework (settings, router,
  services, views, urls).

Tambien incluye:

- DDL completo de las 5 tablas (`base_ivr_detalle`,
  `base_ivr_clientes`, `etl_runs`, `job_execution_log`,
  `job_config`).
- Codigo SQL real de los SPs.
- Codigo Python real de Django command + DRF views.
- Comparacion con FUNC_REPORTE_COBRANZA del legacy.
- Tabla de estado de los 17 componentes (Desplegado/Pendiente).
- Restricciones tecnicas (CNST-ETL-001..008, CNST-003,
  ADR-BACK-012, IVR-7-dias).

### Estado actual de la documentacion ETL en el corpus

Auditoria de archivos relacionados con ETL/pipeline:

| Ubicacion | Contenido actual | Granularidad | Cobertura v2.1 |
|---|---|---|---|
| `arquitectura-tecnica/modulos/etl-monitoring/` | `index.rst` + 4 sub-archivos: responsabilidades, dependencias, componentes, restricciones + `diagramas/` con 3 diagramas (componentes-mod-pipeline, flujo-etl-nocturno, sub-estados-proceso-etl) | Modulo arquitectonico (ARQ_MOD_004) — perspectiva de **monitoreo**, no ejecucion | Parcial: existe el flujo pero sin codigo real ni DDL |
| `arquitectura-tecnica/design-view/pipeline/` | `index.rst` + `bounded-context.rst` + `interaction-pattern.rst` + `pipeline-execution-lifecycle.rst` + `etl-execution-flow.rst` | Vista de diseno modular del pipeline | Parcial: clases y secuencias pero sin DDL ni codigo Python |
| `arquitectura-tecnica/implementation-view/pipeline/` | `index.rst` + `layer-structure.rst` | Capas API/service/repo/orm | Solo capas — sin codigo real |
| `arquitectura-tecnica/system-view/etl-execution-lifecycle.rst` | FSM ETL global del sistema | Vista de sistema | Diagrama estados — sin DDL |
| `arquitectura-tecnica/scheduled-tasks.rst` | Top-level con tareas programadas | Generico | Menciona ETL nocturno |
| `requisitos/casos-uso/pipeline/uc-pip-01..04` | UCs de supervision ETL | Vista de requisitos | UCs textuales — sin codigo |

**Ningun archivo del corpus actual contiene:**

- DDL real de `base_ivr_detalle`, `base_ivr_clientes`,
  `etl_runs`, `job_execution_log`, `job_config`.
- Codigo SQL real de los 5 SPs ETL + 7 SPs de reporte +
  7 funciones de utilidad.
- Codigo Python del management command `run_etl` +
  heartbeat + Django services + views + urls.
- Tabla de estado de los 17 componentes.
- Comparacion con legacy FUNC_REPORTE_COBRANZA.
- DAG de niveles 0-5.

**Conclusion del audit:** el documento v2.1 cubre informacion
**ausente** del corpus actual. No es una duplicacion — es la
primera documentacion implementation-level del ETL real.

### Decision de ubicacion (propuestas)

#### Opcion A — Nuevo directorio dedicado

```
source/arquitectura-tecnica/pipeline-etl-iact/
  index.rst                       (overview + DAG niveles 0-5)
  utility-functions.rst           (Nivel 0)
  triggers.rst                    (Nivel 1)
  orchestration.rst               (Nivel 2)
  etl-procedures.rst              (Nivel 3)
  intermediate-tables.rst         (Nivel 4 tablas)
  report-procedures.rst           (Nivel 4 SPs reporte)
  django-rest-integration.rst     (Nivel 5)
  legacy-comparison.rst           (FUNC_REPORTE_COBRANZA)
  components-status.rst           (estado de los 17 componentes)
```

Pros: granular, navegable, refs `:doc:` precisas.
Contras: 9 archivos nuevos + 1 directorio.

#### Opcion B — Un solo archivo grande en modulos/etl-monitoring/

```
source/arquitectura-tecnica/modulos/etl-monitoring/
  ...
  implementation-flow-v2-1.rst    ← NUEVO (todo el doc fusionado)
```

Pros: minimal, complementa los `responsabilidades` /
`componentes` / `dependencias` / `restricciones` ya existentes.
Contras: archivo de ~600 lineas, dificil navegar, mezcla de
todos los niveles.

#### Opcion C — Distribuir en archivos existentes

Agregar contenido a los archivos ya existentes:
- DDL → nuevo `intermediate-tables-ddl.rst` en
  `design-view/pipeline/` o `modulos/etl-monitoring/`.
- Codigo SQL → nuevo `etl-procedures-sql.rst` en alguna
  ubicacion.
- Codigo Python → `implementation-view/pipeline/layer-structure.rst`
  (extender con codigo real).
- Comparacion legacy → en `procedimientos/` o `gobernanza/`.

Pros: integrado con la estructura existente.
Contras: dificil de mantener cohesion del v2.1; el documento
fuente esta diseñado como una unidad integrada.

#### Recomendacion

**Opcion A** parece la mas adecuada por:

- El documento es una unidad coherente (niveles 0-5 con DAG
  explicito) que se rompe artificialmente al distribuir.
- La granularidad por nivel facilita ediciones y reviews
  independientes.
- Establece un nuevo "dominio" en el corpus
  (`pipeline-etl-iact/`) que claramente documenta el ETL real
  en implementation-level. Coexiste con
  `modulos/etl-monitoring/` (perspectiva de monitoreo
  funcional) y `design-view/pipeline/` (estructura de diseño)
  sin solapar.

### Decisiones pendientes del ejecutor

- **D1 (ubicacion):** Opcion A (nuevo directorio
  `pipeline-etl-iact/`) / B (un archivo en
  `modulos/etl-monitoring/`) / C (distribuir).
- **D2 (idioma del codigo SQL/Python):** preservar `tal cual`
  (espanol+ingles tecnico mezclado en variables como
  `iniciado_en`, `mensaje_error`, `trimestre`) o migrar
  identifiers a ingles consistente. El doc fuente usa una
  mezcla; el corpus general migro a ingles tecnico (CLEAN_CODE
  §1.5).
- **D3 (vocabulario STD-010):** el doc menciona `MariaDB` y
  `PostgreSQL` por nombre — STD-010 §2.1 marca
  `arquitectura-tecnica/**` como "No — libre" asi que se
  pueden mantener los nombres tecnologicos. Confirmar.
- **D4 (status real de componentes):** la tabla de estado del
  doc lista 6 componentes como "Pendiente"
  (`evt_etl_diario`, `manage.py run_etl`, `settings.py
  DATABASES dual`, `services/ivr_reports.py`,
  `views/ivr_reports.py`, APScheduler). ¿El corpus debe
  documentarlos como "diseno aprobado pendiente
  implementacion" o esperar a que se implementen?

### Pendientes para Phase 2-10

1. Resolver D1-D4 con el ejecutor.
2. Crear estructura de archivos elegida.
3. Convertir el contenido del input a formato RST con:
   - Frontmatter meta (artefacto, tipo, dominio, version,
     estado).
   - Bloques de codigo SQL/Python en `.. code-block:: sql/python`.
   - Tablas en formato `list-table::`.
   - Diagramas ASCII en `:: code-block:: text`.
   - Cross-refs `:doc:` a UCs, modulos, design-view del
     pipeline.
4. Build strict y verificacion de cross-refs.

### Refs

- Input source preserved en
  `inputs/flujo-etl-ivr-v2-1-fuente.md`.
- Audit existente en `modulos/etl-monitoring/`,
  `design-view/pipeline/`, `implementation-view/pipeline/`,
  `system-view/etl-execution-lifecycle.rst`.
