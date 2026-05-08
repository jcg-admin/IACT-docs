```yml
project: IACT-docs
work_package: 2026-05-05-08-03-31-rbac-vocabulary-cnst-033-pass
created_at: 2026-05-05 08:03:31
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-validation
predecessor_wp: 2026-05-05-07-40-30-arq-tecnica-uml-rigor-pass
target: Aplicar CNST-033 Vocabulario Unificado RBAC al domain-model
```

# WP — RBAC Vocabulary CNST-033 Pass

## Trigger

Al cerrar pendientes RBAC del WP predecesor
(``arq-tecnica-uml-rigor-pass``) se descubrió que
**CNST-033 v2.0.0** (vivo en
``source/normativa/restricciones/cnst-033-vocabulario-unificado-rbac.rst``)
**invalida la decisión D-11** del WP predecesor.

CNST-033 §2 establece literalmente:

> CODIGO: Ingles (clases, metodos, variables, codenames,
> nombres de funciones, campos SQL)
>
> **No hay excepciones.**

Y §9 declara que el incumplimiento es "**error de nivel
CRITICO en revisión de código**".

## Hallazgos preliminares (a confirmar en DISCOVER)

5 archivos del domain-model violan CNST-033:

| Archivo | Clase | Tipo de violación |
|---------|-------|-------------------|
| ``abandono-report-service.rst`` | ``AbandonoReportService`` | nombre dominio en español |
| ``clientes-report-service.rst`` | ``ClientesReportService`` | español |
| ``menu-ivr-report-service.rst`` | ``MenuIvrReportService`` | acrónimo IVR no expandido (§8.2) |
| ``transferencias-report-service.rst`` | ``TransferenciasReportService`` | español |
| ``servicio-reportes.rst`` | ``ServicioReportes`` + 4 métodos en español | violación total |

Otros archivos del domain-model deben revisarse:

- ¿Existen otros nombres de clase, atributos o métodos
  en español?
- ¿Hay codenames de funciones (atributos
  ``function_code``) que no estén en el catálogo
  canónico de CNST-033 §5?

## Renaming propuesto (a validar con CNST-033 §8)

| Actual | Propuesto | Justificación |
|--------|-----------|---------------|
| ``AbandonoReportService`` | ``AbandonmentReportService`` | sustantivo inglés directo |
| ``ClientesReportService`` | ``CallerReportService`` | §8.2 "clientes" en IVR = "callers" |
| ``MenuIvrReportService`` | TBD: ``IvrNavigationReportService`` o ``MenuNavigationReportService`` | §8.2 expandir acrónimos. **Decisión pendiente** |
| ``TransferenciasReportService`` | ``TransferReportService`` | §8.2 directo |
| ``ServicioReportes`` | TBD: ``ReportFacadeService`` o **eliminar** | facade legacy. **Decisión pendiente del ejecutor** |

Métodos de ``ServicioReportes`` (§8.1):

| Actual | Propuesto |
|--------|-----------|
| ``llamadas_abandonadas`` | ``abandoned_calls`` o ``get_abandonments`` |
| ``menu_redirigidos`` | ``redirected_menu`` o ``get_menu_redirections`` |
| ``clientes`` | ``unique_callers`` o ``get_callers`` |
| ``centros_transferencia`` | ``transfer_centers`` o ``get_transfers`` |

## Áreas a revisar

1. **R-naming-clases**: spot-check de todas las 68 clases
   del domain-model contra CNST-033 §4.2.
2. **R-naming-metodos**: spot-check de signatures contra
   §4.3.
3. **R-codenames**: validar que todo
   ``function_code`` en signatures use el catálogo
   canónico §5 (RPT-001..RPT-008, ALR-001..ALR-006,
   etc.).
4. **R-grupos**: validar nombres de ``FunctionGroup``
   contra catálogo §6.
5. **R-sod**: validar ``SeparationRule`` contra §7.
6. **R-impactos**: enumerar todos los archivos que
   referencian las clases a renombrar (``:doc:``,
   ``grep`` por nombre de clase, code samples).
7. **R-archivos**: nombres de archivo ``.rst`` —
   ¿deben renombrarse para alinear con el nuevo nombre
   de clase? Convención del proyecto: kebab-case del
   nombre de clase.
8. **R-uc-impacto**: ¿algún UC referencia los métodos
   en español de ``ServicioReportes``? Si sí, validar
   que el cambio no rompe trazabilidad.

## Output esperado

- ``discover/cnst-033-violations-inventory.md`` —
  inventario completo de violaciones (no solo las 5
  identificadas).
- ``analyze/renaming-impact-map.md`` — mapa de impacto:
  por cada renaming, qué archivos cambian y qué refs
  ``:doc:`` se rompen.
- ``decisions-log.md`` — D-NN para cada nombre nuevo
  acordado, con cita literal de CNST-033 sección.
- ``track/{wp}-changelog.md`` — registro por archivo
  modificado.

## Riesgos

- **R1**: el renaming puede romper builds de Sphinx si
  algún ``:doc:`` queda colgando. Mitigación: ejecutar
  ``make html`` tras cada batch y resolver los
  warnings.
- **R2**: los ``function_code`` referenciados en
  signatures (e.g. ``view_reports``) ya están en
  inglés conforme catálogo CNST-033 §5; verificar que
  no haya regresiones en el sweep.
- **R3**: el alcance puede crecer si aparecen más
  clases en español ocultas. Mitigación: DISCOVER
  exhaustivo antes de tocar nada.

## Stopping points

- **SP-01**: tras inventario completo de violaciones
  (decidir si scope crece más allá de las 5
  identificadas).
- **SP-02**: tras decidir nombre final de
  ``MenuIvrReportService`` y de ``ServicioReportes``
  (las dos decisiones pendientes).
- **SP-03**: tras renaming del primer archivo
  (validar que ``:doc:`` refs se actualizan
  correctamente).
- **SP-04**: pre-merge — make html exit 0, 0 warnings
  nuevos.

## Predecesores

- ``2026-05-05-07-40-30-arq-tecnica-uml-rigor-pass``
  — pasada UML que descubrió la violación.
- ``2026-05-05-06-41-02-arq-tecnica-uml-deepening``
  — donde se aprobó D-11 (excepción STD-008 para
  ``ServicioReportes``) que CNST-033 invalida. Habrá
  que registrar la reversión D-11 → ANULADA.

## Decisiones pendientes del ejecutor

1. Nombre final para ``MenuIvrReportService``:
   ``IvrNavigationReportService`` vs
   ``MenuNavigationReportService``.
2. Política para ``ServicioReportes``:
   ``ReportFacadeService`` (mantener) vs **eliminar**
   (los XxxReportService modernos son la API canónica).
