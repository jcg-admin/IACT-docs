```yml
project: IACT-docs
work_package: 2026-05-05-07-40-30-arq-tecnica-uml-rigor-pass
created_at: 2026-05-05 07:40:30
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-analysis
predecessor_wp: 2026-05-05-06-41-02-arq-tecnica-uml-deepening
target: Aplicar rigor UML completo (uml-04) a los 37 archivos de domain-model/
```

# WP — Domain Model UML Rigor Pass

## Trigger

El WP predecesor (``arq-tecnica-uml-deepening``) cerró los
41 stubs como ``Vigente`` aplicando un patrón consistente
(composition / aggregation / dependency / enums) pero
**NO aplicó los 8 conceptos** documentados en
``source/base-cognitiva/_uml/uml-04-uso-relaciones/``.

Ver decisión D-12 del WP predecesor.

## Alcance

Recorrer los 37 archivos canónicos en
``source/arquitectura-tecnica/domain-model/`` (excluyendo
``index.rst``, ``README.rst``, y los stubs originalmente
sin diagrama) aplicando un checklist por archivo.

## Los 8 puntos de la pasada

Por cada archivo, validar y corregir:

| # | Concepto | Fuente uml-04 | Detección |
|---|----------|---------------|-----------|
| 1 | Multiplicidades en extremos | ``multiplicidad.rst`` | toda relación ``o-- / *-- / -->`` debe llevar ``"N"`` o ``"0..1"`` etc. |
| 2 | Roles en extremos | ``asociacion-binaria.rst`` | el extremo con valor semántico (``: stat_repo``) lleva el rol |
| 3 | Restricciones ``{ordered}``, ``{unique}``, ``{readOnly}`` | ``restricciones-en-las-asociaciones.rst`` | colecciones temporales ``List<Bucket>`` → ``{ordered}``; catálogos → ``{readOnly}`` |
| 4 | Asociaciones calificadas ``[key]`` | ``asociaciones-calificadas.rst`` | ``PermissionCache``, ``RBACRepo`` resuelven por clave |
| 5 | Clases de asociación | ``clases-de-asociacion.rst`` | ``AccessGroupFunction`` debe ser clase de asociación entre ``AccessGroup`` y ``Function`` |
| 6 | Generalización / clases abstractas | ``herencia-y-generalizacion.rst``, ``clases-abstractas.rst`` | ``BaseReportService`` abstracto del que heredan los 4 ``XxxReportService``; patrón ``Repository`` abstracto |
| 7 | Asociaciones reflexivas | ``asociaciones-reflexivas.rst`` | ``Menu`` (padre/hijo), ``NavDomain`` jerárquico |
| 8 | Tipo correcto de dependencia | ``dependencias.rst`` | distinguir ``..>`` por uso (parámetro), por instanciación, por retorno |

## Áreas a revisar (por bounded context)

1. **R-audit** (9 archivos): patrón Repository abstracto;
   multiplicidades en cadenas ``AuditService → Validator``.
2. **R-alerts** (5 archivos): asociación reflexiva en
   ``AlertRule`` si tiene reglas anidadas.
3. **R-rbac** (10 archivos): **clase de asociación**
   ``AccessGroupFunction``; reflexiva en ``Menu`` y
   ``NavDomain``; calificada en ``PermissionCache``.
4. **R-reports** (17 archivos): **generalización**
   ``BaseReportService``; ``{ordered}`` en ``buckets``;
   ``{readOnly}`` en ``column_catalog``.

## Output esperado

- Por cada archivo: rediagramado con los 8 puntos
  aplicables marcados.
- ``analyze/uml-04-checklist.md`` — matriz archivo × punto
  con estado (✓ aplicado / N/A / pendiente).
- Entrada en ``track/{wp}-changelog.md`` por cada archivo
  modificado.
- Decisiones nuevas en ``decisions-log.md`` (especialmente
  el diseño del ``BaseReportService`` abstracto).

## Riesgos

- **R1**: la generalización ``BaseReportService`` puede
  romper los diagramas individuales si los hace demasiado
  abstractos. Mitigación: mantener el diagrama por clase
  con la herencia explícita pero los atributos heredados
  no repetidos.
- **R2**: las asociaciones calificadas con sintaxis
  PlantUML pueden no renderizar bien. Mitigación: validar
  con ``plantuml-guide/`` y el script de pre-render.
- **R3**: scope creep — pasar de "rigor UML" a
  "redesign". Mitigación: el WP NO redefine modelos,
  solo aplica notación correcta a lo ya modelado.

## Stopping points

- **SP-01**: tras inventario inicial (¿37 archivos? ¿qué
  excluir?).
- **SP-02**: tras diseñar ``BaseReportService`` (validar
  jerarquía antes de aplicar a 17 archivos).
- **SP-03**: tras Audit BC (validar patrón Repository
  abstracto antes de RBAC).
- **SP-04**: antes de merge a ``feature/solve-problem-docs``.

## Predecesores

- ``2026-05-05-06-41-02-arq-tecnica-uml-deepening``
  — completó los 41 stubs y reconoció el gap (D-12).
- ``2026-05-05-05-44-25-plantuml-svg-prerender``
  — pre-render que validará los nuevos diagramas.
