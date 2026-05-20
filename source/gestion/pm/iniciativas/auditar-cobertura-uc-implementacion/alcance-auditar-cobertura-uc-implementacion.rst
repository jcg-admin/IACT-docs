.. meta::
   :artefacto: ALCANCE-AUDITAR-COBERTURA-UC-IMPLEMENTACION
   :tipo: Alcance
   :dominio: gestion
   :subdominio: pm/iniciativas/auditar-cobertura-uc-implementacion
   :repo_objetivo: multiple
   :estado: Pendiente
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T20:13:49
   :ultimo_cambio: 2026-05-19T20:13:49
   :autor: NestorMonroy
   :clasificacion: Interno

.. _alcance-auditar-cobertura-uc-implementacion:

==============================================================
Alcance: Auditar Cobertura UC -> Implementacion
==============================================================

Por que existe
==============

Sponsor pregunto "se implementaron todos los flujos de los
UCs?". La respuesta honesta hasta el momento fue: en esta
sesion no se implemento ningun UC nuevo; solo se habilito el
runtime existente (DBs, venvs, build, tests) y se resolvieron
fallas de infraestructura (URL routing, grants, fixtures). El
codigo de los apps preexistia.

Pero **no se ha auditado**:

* Cuantos de los 75 UCs in-scope ya tienen implementacion
  en IACT-api.
* Cuantos tienen componente UI correspondiente.
* Cuantos tienen test que los ejercite end-to-end (no solo
  unit test del helper).
* Cuantos quedan **sin implementar** o con implementacion
  **parcial**.

Sin esa matriz, no hay forma de responder con numeros
verificables y la pregunta del sponsor queda en
"probablemente la mayoria" — claim SPECULATIVE prohibido por
calibration-verified-numbers.

Criterio de completitud verificable
=====================================

* ``deep-analisis-cobertura-uc-implementacion.rst`` lista
  los 75 UCs in-scope con su dominio y nombre canonico.
* Para cada UC, la matriz documenta:

  - ``api_view``: ruta y archivo del view/viewset que lo
    implementa, o "ausente".
  - ``api_url``: registro en ``config/urls.py`` o
    ``apps/{dominio}/urls.py``, o "ausente".
  - ``api_test``: archivo de test que lo ejercita (o
    "ausente").
  - ``ui_component``: componente/screen en
    ``IACT-ui/src/`` que consume el endpoint (o
    "ausente").
  - ``ui_test``: archivo jest que lo cubre (o "ausente").
  - ``db_support``: tabla/SP relevante en ``IACT-db/``
    (cuando aplique) o "no aplica".
  - ``estado``: ``Implementado`` (api+ui+test) /
    ``Parcial`` (algunos pero no todos) / ``No
    implementado``.

* Conteo agregado por dominio y estado.
* Lista explicita de UCs sin implementacion para
  iniciativas futuras de desarrollo.

In-scope
========

* Investigacion read-only en IACT-api, IACT-ui, IACT-db,
  IACT-docs. No se modifica codigo.
* Enumeracion de UCs por dominio.
* Heuristica de mapeo UC -> codigo: por nombre del UC
  (kebab + numero), por prefijo del dominio, por grep en
  comentarios docstring que mencionen el UC ID.
* Resolucion explicita del scope "uc-opr-*, uc-sup-*,
  uc-cli-01..05 OUT": presentar dos lecturas (estricta
  literal vs por categoria de actor) y elegir la que el
  sponsor confirme.
* Matriz y conteos.
* Identificacion de patron de OUT vs IN.

Out-of-scope
============

* Implementacion de UCs faltantes (cada bucket sera
  iniciativa propia).
* Auditoria de calidad de la implementacion existente
  (cobertura de codigo, code smells). Solo se valida
  presencia.
* Verificacion de que los flujos implementados respondan
  exactamente al FR del UC. Solo se verifica que existe
  endpoint + UI + test asociado al UC.
* Auditoria de los 18 UCs OUT por scope explicito
  (uc-opr-*, uc-sup-*, uc-cli-01..05).
* Implementacion en repos no listados (server/devops).

Decisiones de contenido tomadas durante la lectura
====================================================

* La iniciativa se clasifica como **documental** segun
  PROC-GOB-013 v2.0.0 (no produce codigo, solo RST).
* La matriz se presenta como una lista RST de filas
  con sus columnas; si el volumen excede 75 filas con
  evidencia textual y el archivo supera ~800 lineas, se
  separa en un artefacto hijo
  ``matriz-cobertura-uc.rst``.
* Las dos lecturas del OUT (estricta vs categoria) se
  presentan en el deep-analisis con conteos para que el
  sponsor decida. Por defecto, la matriz cubre los 75
  UCs y marca con una columna ``scope`` si IN o OUT
  bajo cada lectura.
