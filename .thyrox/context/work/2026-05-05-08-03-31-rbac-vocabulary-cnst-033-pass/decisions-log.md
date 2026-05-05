```yml
created_at: 2026-05-05 08:12:00
updated_at: 2026-05-05 08:12:00
project: IACT-docs
work_package: 2026-05-05-08-03-31-rbac-vocabulary-cnst-033-pass
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Decisions Log — RBAC Vocabulary CNST-033 Pass

----

## D-01 — Anular D-11 del WP arq-tecnica-uml-deepening

**Contexto:** D-11 del WP predecesor declaró
"excepción documentada a STD-008" para mantener
``ServicioReportes`` y sus métodos en castellano.

**Evidencia que invalida D-11:**

CNST-033 §2 — Regla Fundamental:

  > CODIGO: Ingles (clases, metodos, variables,
  > codenames, nombres de funciones, campos SQL)
  > **No hay excepciones.**

CNST-033 §9 — Reglas de Revisión:

  > Las siguientes condiciones constituyen errores de
  > nivel CRITICO: codename en espanol; nombre de clase
  > que describe mecanismo en lugar de dominio
  > (RBACBackend, HasFunction).

**Decisión:** D-11 queda **anulada**. La excepción
declarada era inválida desde su origen — el ejecutor
desconocía CNST-033 v2.0.0 al aprobarla.

**Consecuencia operativa:** todos los identificadores
en castellano del domain-model deben pasar a inglés.

----

## D-02 — Eliminar ServicioReportes (no renombrar)

**Contexto:** ``ServicioReportes`` era una facade legacy
sin lógica propia que delegaba a los 4 ``XxxReportService``
modernos.

**Decisión:** **eliminar el archivo y la clase**, no
renombrar.

**Justificación:**

1. La razón documentada para mantenerla (D-11) era
   "compatibilidad de API legada" — invalidada por D-01.
2. Es una clase **sin lógica propia** — solo delega.
   Clean Code rechaza wrappers vacíos sin valor de
   dominio (Robert C. Martin, *Clean Code* cap. 3:
   "Functions should do one thing").
3. CNST-033 §4.2 prohíbe nombres que **describen
   mecanismo** ("RBACBackend", "HasFunction"). ``Facade``
   es exactamente eso: el patrón GoF, no un concepto de
   dominio.
4. Los 5 ``XxxReportService`` modernos son la API
   canónica. Eliminar la facade hace que el modelo
   refleje fielmente el código objetivo.

**Renombrar a otro nombre (e.g. ``OperationalReportService``)
fue evaluado y descartado:** no aporta valor de dominio
sobre los 5 servicios especializados; introduce
ambigüedad ("¿qué reporta?"); CNST-033 §4.1 prohíbe
duplicar contexto del módulo en el nombre.

----

## D-03 — Renombrar las 4 clases XxxReportService

**Contexto:** las clases tienen nombre de dominio en
castellano, violando CNST-033 §4.2.

**Decisión:**

| Actual | Nuevo nombre | Justificación CNST-033 |
|--------|--------------|------------------------|
| ``AbandonoReportService`` | ``AbandonmentReportService`` | §8.1 sustantivo inglés directo |
| ``ClientesReportService`` | ``CallerReportService`` | §8.2 "clientes" del IVR = "callers" (terminología call-center) |
| ``MenuIvrReportService`` | ``IvrNavigationReportService`` | ver D-04 |
| ``TransferenciasReportService`` | ``TransferReportService`` | §8.1 sustantivo inglés directo |

**Convenciones aplicadas:**

- PascalCase para nombre de clase (PEP-8, CNST-033 §4.2).
- Sufijo ``Service`` mantenido — es eponym de
  stratification DDD (Eric Evans), no patrón GoF.
  Distinto del caso ``Facade`` (D-02).
- Sin sufijos de patrón (``Manager``, ``Handler``,
  ``Helper``, ``Util``) per Clean Code.

**Archivos correspondientes** (kebab-case del nombre de
clase, convención local):

- ``abandono-report-service.rst`` →
  ``abandonment-report-service.rst``
- ``clientes-report-service.rst`` →
  ``caller-report-service.rst``
- ``menu-ivr-report-service.rst`` →
  ``ivr-navigation-report-service.rst``
- ``transferencias-report-service.rst`` →
  ``transfer-report-service.rst``

----

## D-04 — IvrNavigationReportService (no MenuNavigation)

**Contexto:** alternativas para ``MenuIvrReportService``:

- A) ``MenuNavigationReportService``
- B) ``IvrNavigationReportService``
- C) ``VoiceMenuReportService``
- D) ``CallNavigationReportService``

**Decisión:** **Opción B** — ``IvrNavigationReportService``.

**Análisis completo:** ver
``discover/ivr-naming-analysis.md``.

**Razones principales:**

1. **CNST-033 §8.2 NO aplica a IVR.** §8.2 castiga
   acrónimos técnicos que ocultan dominio (``ETL``,
   ``SoD``). IVR es lo opuesto:
   ``base-cognitiva/glosario.rst`` declara IVR como
   "**el dominio del cual IACT extrae métricas**".
2. **Coherencia con corpus**: BREQ-007 = "integracion-ivr-operacional";
   producto = "IVR Analytics & Customer Tracking".
3. **Disambiguación**: ya existe clase ``Menu`` (RBAC).
   ``MenuNavigation`` colisiona semánticamente.
4. **Clean Code "intention-revealing names"** (Martin):
   ``IvrNavigation`` revela intención sin contexto
   adicional.
5. **Casing**: ``Ivr`` (PascalCase, no ``IVR``) per
   PEP-8 para acrónimos embebidos
   (``XmlParser``-style).

----

## D-05 — Renombrar atributos protegidos heredados

**Contexto:** ``BaseReportService`` (D-07 del WP
predecesor) define atributos protegidos
``stat_repo``, ``kpi_calculator``, ``segment_resolver``.
Las subclases concretas heredan estos nombres.

**Decisión:** los nombres ya están en inglés y son
descriptivos. **No requieren cambio.**

CNST-033 §3.5 valida ``snake_case`` inglés para campos.
Verificación: ``stat_repo`` ✓, ``kpi_calculator`` ✓,
``segment_resolver`` ✓.

----

## D-06 — Política para refs ``:doc:`` y code samples en UCs

**Contexto:** 23 archivos en ``source/`` referencian las
clases a renombrar. El subset crítico es:

- 8 UCs en ``source/requisitos/casos-uso/reports/uc-rpt-{13,15,16,17}``
- 1 estándar (``std-011-alias-diagramas-uml.rst``)
- 4 archivos de system-view y design-view
- 6 archivos del propio domain-model
- 4 archivos de ``modulos/vis-reports/``

**Decisión:** **actualizar todas las referencias en el
mismo commit que el renaming**, en un solo sweep
mecanizado.

**Justificación:**

- Si se posterga, los ``:doc:`` quedan colgando y
  ``make html`` falla.
- La regla I-002 (git como única persistencia) impide
  archivos ``.bak`` o copias paralelas.
- Atomicidad: el renaming + actualización de refs es
  conceptualmente una sola operación.

**Estrategia operativa:**

1. ``git mv`` para los 4 archivos renombrados (preserva
   historial).
2. ``rm`` para ``servicio-reportes.rst``.
3. Sweep ``sed``-style sobre los 23 archivos para:
   - Reemplazar nombres de clase
   - Reemplazar paths ``:doc:`` y refs internas
   - Reemplazar nombres de método (4 métodos en
     castellano de ``ServicioReportes``)
4. Pre-render PlantUML (validar que diagramas
   renderizan sin errores).
5. ``make html`` (validar 0 warnings nuevos).

----

## D-07 — Code samples en UCs: actualizar firmas en pseudocódigo

**Contexto:** algunos UCs (uc-rpt-13/15/16/17) tienen
bloques ``contract`` y pseudocódigo invocando los
servicios. Por ejemplo:

.. code-block:: text

   contract AbandonoReportService:
     def get_abandono_per_period(period):
       ...
   data = ServicioReportes.llamadas_abandonadas(trimestre)

**Decisión:** actualizar pseudocódigo a inglés:

.. code-block:: text

   contract AbandonmentReportService:
     def get_abandonment_per_period(period):
       ...
   data = AbandonmentReportService.get(period)

Justificación: los UCs documentan el **contrato**,
no la API legacy. Si CNST-033 invalida el castellano,
los UCs deben reflejar el contrato canónico.

Métodos castellanos de ``ServicioReportes`` reemplazados:

| Método actual | Método del XxxReportService canónico |
|---------------|--------------------------------------|
| ``llamadas_abandonadas(trimestre)`` | ``AbandonmentReportService.get(invoker, period)`` |
| ``menu_redirigidos(trimestre)`` | ``IvrNavigationReportService.get(invoker, period, filters)`` |
| ``clientes(trimestre)`` | ``CallerReportService.get(invoker, period, filters)`` |
| ``centros_transferencia(trimestre)`` | ``TransferReportService.get(invoker, period, filters)`` |
| ``centros_xsegmento(trimestre)`` | ``TransferReportService.by_center(invoker, period)`` |

----

## Pendientes de decisión

(ninguno — WP en ejecución)
