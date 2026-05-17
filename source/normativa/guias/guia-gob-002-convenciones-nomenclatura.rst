:orphan:

.. meta::
 :artefacto: NORM_GUIA_GOB_002_CONVENCIONES_NOMENCLATURA
 :tipo: Guia de Gobernanza
 :dominio: normativa
 :subdominio: guias
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-09
 :ultimo_cambio: 2026-05-09
 :autor: NestorMonroy
 :clasificacion: Critico

.. _norm_guia_gob_002_convenciones_nomenclatura:

============================================================
GUIA-GOB-002 — Convenciones de Nomenclatura
============================================================

Convenciones de naming para artefactos del corpus IACT-docs.
Aplica CLEAN_CODE §6.2 (naming basado en contenido) y los
prefijos de tipo definidos en
:doc:`/normativa/gobernanza/adr-gob-002-plantuml-para-diagramas`.

Archivos .rst del corpus
=========================

.. list-table::
 :widths: 30 30 40
 :header-rows: 1

 * - Tipo de artefacto
   - Patron de nombre
   - Ejemplos
 * - ADR de gobernanza
   - ``adr-gob-{NNN}-{tema-descriptivo}.rst``
   - ``adr-gob-001-organizacion-proyecto-por-dominio``
 * - ADR de backend
   - ``adr-back-{NNN}-{tema}.rst``
   - ``adr-back-002-configuracion-dinamica-sistema``
 * - ADR de devops
   - ``adr-devops-{NNN}-{tema}.rst``
   - ``adr-devops-001-vagrant-mod-wsgi-importante-produc``
 * - Procesos
   - ``proc-{dominio}-{NNN}-{nombre}.rst``
   - ``proc-dev-001-pipeline-trabajo-iact``
 * - Procedimientos
   - ``proced-{dominio}-{NNN}-{nombre}.rst``
   - ``proced-dev-001-crear-pull-request``
 * - Estandares
   - ``std-{NNN}-{nombre}.rst`` o ``estandares-{tema}.rst``
   - ``std-010-vocabulario-controlado``,
     ``estandares-codigo``
 * - Plantillas
   - ``tpl-{tipo}-{nombre}.rst``
   - ``tpl-uc-actor-secundario``
 * - Casos de uso
   - ``uc-{modulo}-{NN}/`` (directorio)
   - ``uc-acc-01/``, ``uc-pip-04/``
 * - Reglas de negocio
   - ``br-{NNN}-{tema}.rst``
   - ``br-007-separacion-de-funciones``

Reglas
=======

- **Kebab-case** en todos los archivos (``mi-archivo.rst``,
  no ``mi_archivo.rst``).
- **Sin numeros como prefijo de archivo** salvo cuando el
  numero es parte del ID semantico (``adr-gob-NNN``,
  ``br-NNN``, ``uc-XXX-NN``).
- **Sin prefijos de tipo de diagrama** (no
  ``componentes-X.rst``, ``secuencia-X.rst``,
  ``clases-X.rst``); el nombre describe el contenido
  (``layer-structure.rst``, ``user-creation-flow.rst``,
  ``entity-model.rst``).
- **Lowercase** en todo el path. Excepcion historica:
  IDs de plantillas como ``UC-ALR-05`` (mayuscula) en
  contenido del documento.

Identifiers internos
=====================

Cada documento declara un identifier en su meta y un
``_label:`` para cross-references. El label sigue:

.. code-block:: rst

   .. _at_design_seq_access:
   .. _arq_mod_admin:
   .. _back_arq_configuration:

Patron: ``{dominio}_{categoria}_{tema}`` separado por
underscore (no kebab) en labels.

Cross-references
=================

Preferir ``:doc:`` con path absoluto desde ``source/``:

.. code-block:: rst

   :doc:`/normativa/gobernanza/adr-gob-001-organizacion-proyecto-por-dominio`

Sobre ``:ref:`` con label:

.. code-block:: rst

   :ref:`arq_mod_admin`

Evitar paths relativos largos (``../../../``) — son fragiles
ante reorganizacion.

----

.. seealso::

 - :doc:`/normativa/gobernanza/adr-gob-001-organizacion-proyecto-por-dominio`
 - :doc:`/normativa/estandares/estandares-codigo`
 - :doc:`/normativa/guias/diferencia-procesos-procedimientos`
