.. meta::
   :artefacto: ALCANCE-AUDITAR-IMPLEMENTACION-UCS-API-UI
   :tipo: Alcance
   :dominio: gestion
   :subdominio: pm/iniciativas/auditar-implementacion-ucs-api-ui
   :repo_objetivo: multiple
   :estado: Completada
   :version: 1.0.0
   :fecha_creacion: 2026-07-03T22:15:30
   :ultimo_cambio: 2026-07-03T22:15:30
   :autor: NestorMonroy
   :clasificacion: Interno

.. _alcance-auditar-implementacion-ucs-api-ui:

==============================================================
Alcance: Auditar Implementacion UCs en api y ui
==============================================================

Por que existe
==============

El corpus de UCs en docs cambio desde la ultima auditoria de
cobertura (2026-05-19, ``auditar-cobertura-uc-implementacion``
+ ``verificar-mapping-docs-codigo-todos-los-dominios``):

* Se agregaron **14 UCs nuevos** (uc-078..091): los UCs
  retro-documentados por
  ``documentar-ucs-implementados-no-declarados`` (uc-078..090)
  y el UC de sistema uc-091 (ETL diario, spec-from-code).
* Se retiro ``uc-047-resolver-segmento-usuario`` (resuelto por
  ``aclarar-uc-047-resolver-segmento``).
* El codigo tambien cambio: aparecieron markers nuevos en api
  (``UC_PERM_09``, ``UC_USR_08``, ``UC_DSH_01..04``,
  ``UC_ADM_04/05``) y en ui (``UC_ADM_01..05``,
  ``UC_ACC_06/07``, ``UC_ALR_06``).

La pregunta "¿los UCs que mencionan los docs estan
implementados en api e ui?" no tenia respuesta verificada para
el corpus **actual** de 88 UCs. Esta iniciativa la produce.

Criterio de completitud verificable
=====================================

* Matriz completa 88 filas: UC docs × marker canonico ×
  presencia api × presencia ui × estado
  (:doc:`matriz-implementacion-uc-api-ui`).
* Cada conteo acompañado del comando exacto que lo produjo
  (protocolo grep-validado).
* Buckets negativos inspeccionados antes de publicar cualquier
  "sin implementar".
* Lista de hallazgos con clasificacion PROVEN/INFERRED y las
  iniciativas derivadas que corresponda abrir.

In-scope
========

* Investigacion read-only en IACT-api (``**/*.py``) e IACT-ui
  (``src/**/*.{js,jsx,ts,tsx}``). No se modifica codigo.
* Los 88 UCs de ``source/requisitos/requisitos-funcionales/``
  (uc-001..uc-091 con huecos 047-049).
* Mapping UC docs → marker por **validacion textual**: se
  reutiliza el mapping verificado de
  ``verificar-mapping-docs-codigo-todos-los-dominios`` para
  uc-001..077 y el campo ``Marker código`` declarado en el RST
  de uc-078..090; uc-091 declara scheduler (APScheduler) como
  implementacion api.
* Deteccion de markers en formas compuestas
  (``UC_RPT_07/08``, ``UC_ACC_06-07``) y rangos
  (``UC_ADM_01..03``), distinguiendo evidencia fuerte
  (numero nombrado explicitamente) de debil (interior de
  rango en comentario).
* Deuda documental inversa: markers en codigo sin UC docs.

Out-of-scope
============

* Implementacion de faltantes — cada hallazgo accionable se
  deriva a iniciativa propia.
* Auditoria de calidad/conformidad FR por FR (cubierta por
  ``auditar-conformidad-fr-tests-aceptacion`` y sucesoras).
  Solo se valida **presencia** de implementacion.
* Verificacion de tests por UC (la corrida 2026-05-19 la
  incluyo; el sponsor pidio aqui api + ui).
* IACT-db (salvo la referencia declarada por uc-091).
* Los 18 UCs OUT (operator, caller, supervision) — docs los
  declara "Modulo reservado (out-of-scope para v5.6.0)"; solo
  se verifica que efectivamente no exista marker en codigo.
