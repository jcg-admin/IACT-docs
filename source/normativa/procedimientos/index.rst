.. meta::
 :artefacto: Index_Procedimientos
 :tipo: Indice
 :dominio: normativa
 :subdominio: procedimientos
 :estado: Aprobado
 :version: 2.0.0
 :fecha_creacion: 2026-01-07
 :ultimo_cambio: 2026-04-28
 :autor: Equipo IACT
 :clasificacion: Interno

.. _procedimientos:

==============
Procedimientos
==============

Propósito
=========

Este subdominio agrupa los **procedimientos** del proyecto IACT:
secuencias paso-a-paso que describen cómo se ejecutan las
operaciones recurrentes en cada disciplina del proyecto
(desarrollo, devops, operaciones, calidad, gobernanza,
documentación).

Categorización
==============

- ``PROC-MOD-NNN-desc`` — procedimientos generales de un módulo
  funcional (DEV, DEVOPS, OPS, QA, GOB).
- ``PROCED-MOD-NNN-desc`` — procedimientos de gobernanza
  (creación de artefactos, revisión, aprobación).
- ``PROC_Desc`` — procedimientos de generación y derivación de
  artefactos documentales (variante sin módulo, scope
  transversal).

----

Procedimientos generales (PROC-MOD-NNN)
=======================================

.. toctree::
 :maxdepth: 1
 :caption: Desarrollo (DEV)

 proc-dev-001-pipeline-trabajo-iact
 proc-dev-002-sdlc-process

.. toctree::
 :maxdepth: 1
 :caption: DevOps

 proc-devops-001-devops-automation

.. toctree::
 :maxdepth: 1
 :caption: Operaciones (OPS)

 proc-ops-001-deployment
 proc-ops-002-setup-entorno-desarrollo

.. toctree::
 :maxdepth: 1
 :caption: Calidad (QA)

 proc-qa-001-actividades-garantia-documental
 proc-qa-002-estrategia-qa

.. toctree::
 :maxdepth: 1
 :caption: Gobernanza (GOB)

 proc-gob-001-mapeo-procesos-templates
 proc-gob-002-gobernanza-sdlc
 proc-gob-008-reorganizacion-estructura-documental

----

Procedimientos de gobernanza (PROCED-MOD-NNN)
=============================================

.. toctree::
 :maxdepth: 1
 :caption: Desarrollo

 proced-dev-001-crear-pull-request
 proced-dev-002-code-review
 proced-dev-003-resolver-conflictos-merge

.. toctree::
 :maxdepth: 1
 :caption: DevOps

 proced-devops-001-deploy-staging

.. toctree::
 :maxdepth: 1
 :caption: Gobernanza de excepciones

 proc-excepciones-cnst

.. toctree::
 :maxdepth: 1
 :caption: Gobernanza

 proced-gob-001-crear-adr
 proced-gob-002-actualizar-documentacion
 proced-gob-003-documentar-regla-negocio
 proced-gob-004-crear-caso-uso
 proced-gob-005-analisis-impacto-cambios
 proced-gob-006-generar-diagrama-uml-plantuml
 proced-gob-007-consolidacion-ramas-git
 proced-gob-008-configurar-permisos-git-push
 proced-gob-009-refactorizaciones-codigo-tdd

.. toctree::
 :maxdepth: 1
 :caption: Calidad

 proced-qa-001-ejecutar-tests

----

Procedimientos de generación de artefactos (PROC_Desc)
======================================================

Procedimientos que rigen cómo se generan los artefactos del
proyecto a partir de plantillas y reglas de derivación.

.. toctree::
 :maxdepth: 1
 :caption: Generación por tipo de artefacto

 proc-generacion-breq
 proc-generacion-br
 proc-generacion-uc
 proc-generacion-fr
 proc-generacion-nfr
 proc-generacion-cnst
 proc-generacion-mod
 proc-generacion-fd
 proc-generacion-view
 proc-generacion-api
 proc-generacion-adr
 proc-generacion-std
 proc-generacion-pol
 proc-generacion-tst
 proc-generacion-rtm
 proc-generacion-index

.. toctree::
 :maxdepth: 1
 :caption: Derivación entre niveles

 proc-derivacion-breq-br
 proc-derivacion-br-uc
 proc-derivacion-uc-fr
 proc-derivacion-fr-code
 proc-derivacion-fr-tst

.. toctree::
 :maxdepth: 1
 :caption: Revisión y validación

 proc-revision-tpl-previo-generacion
 proc-revision-uc-previo-derivacion
 proc-revision-artefactos
 proc-validacion-sphinx
 proc-verificacion-cobertura
 proc-identificar-gaps-huerfanos

.. toctree::
 :maxdepth: 1
 :caption: Lifecycle documental

 proc-crear-plan-analisis
 proc-crear-estructura-directorios-tmp
 proc-cambio-requisitos
 proc-aprobacion-documentos
 proc-actualizacion-modelo-documental
 proc-auditoria-documental
 proc-versionado-semantico
 proc-publicacion-documentacion
 proc-congelamiento-subdominio
 proc-descongelamiento-subdominio

.. toctree::
 :maxdepth: 1
 :caption: Procedimiento integrador (meta-flujo)

 proc-elaboracion-completa-requisitos

----

Guías y procedimientos transversales
====================================

.. toctree::
 :maxdepth: 1

 guia-completa-desarrollo-features
 procedimiento-analisis-seguridad
 procedimiento-desarrollo-local
 procedimiento-diseno-tecnico
 procedimiento-gestion-cambios
 procedimiento-instalacion-entorno
 procedimiento-qa
 procedimiento-release
 procedimiento-revision-documental
 procedimiento-trazabilidad-requisitos
