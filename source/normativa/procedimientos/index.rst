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

   PROC-DEV-001-pipeline_trabajo_iact
   PROC-DEV-002-sdlc_process

.. toctree::
   :maxdepth: 1
   :caption: DevOps

   PROC-DEVOPS-001-devops_automation

.. toctree::
   :maxdepth: 1
   :caption: Operaciones (OPS)

   PROC-OPS-001-deployment
   PROC-OPS-002-setup-entorno-desarrollo

.. toctree::
   :maxdepth: 1
   :caption: Calidad (QA)

   PROC-QA-001-actividades_garantia_documental
   PROC-QA-002-estrategia_qa

.. toctree::
   :maxdepth: 1
   :caption: Gobernanza (GOB)

   PROC-GOB-001-mapeo_procesos_templates
   PROC-GOB-002-gobernanza-sdlc
   PROC-GOB-008-reorganizacion-estructura-documental

----

Procedimientos de gobernanza (PROCED-MOD-NNN)
=============================================

.. toctree::
   :maxdepth: 1
   :caption: Desarrollo

   PROCED-DEV-001-crear_pull_request
   PROCED-DEV-002-code_review
   PROCED-DEV-003-resolver_conflictos_merge

.. toctree::
   :maxdepth: 1
   :caption: DevOps

   PROCED-DEVOPS-001-deploy_staging

.. toctree::
   :maxdepth: 1
   :caption: Gobernanza

   PROCED-GOB-001-crear_adr
   PROCED-GOB-002-actualizar_documentacion
   PROCED-GOB-003-documentar-regla-negocio
   PROCED-GOB-004-crear-caso-uso
   PROCED-GOB-005-analisis-impacto-cambios
   PROCED-GOB-006-generar-diagrama-uml-plantuml
   PROCED-GOB-007-consolidacion-ramas-git
   PROCED-GOB-008-configurar-permisos-git-push
   PROCED-GOB-009-refactorizaciones-codigo-tdd

.. toctree::
   :maxdepth: 1
   :caption: Calidad

   PROCED-QA-001-ejecutar_tests

----

Procedimientos de generación de artefactos (PROC_Desc)
======================================================

Procedimientos que rigen cómo se generan los artefactos del
proyecto a partir de plantillas y reglas de derivación.

.. toctree::
   :maxdepth: 1
   :caption: Generación por tipo de artefacto

   PROC_Generacion_BReq
   PROC_Generacion_BR
   PROC_Generacion_UC
   PROC_Generacion_FR
   PROC_Generacion_NFR
   PROC_Generacion_CNST
   PROC_Generacion_MOD
   PROC_Generacion_FD
   PROC_Generacion_VIEW
   PROC_Generacion_API
   PROC_Generacion_ADR
   PROC_Generacion_STD
   PROC_Generacion_POL
   PROC_Generacion_TST
   PROC_Generacion_RTM
   PROC_Generacion_Index

.. toctree::
   :maxdepth: 1
   :caption: Derivación entre niveles

   PROC_Derivacion_BReq_BR
   PROC_Derivacion_BR_UC
   PROC_Derivacion_UC_FR
   PROC_Derivacion_FR_CODE
   PROC_Derivacion_FR_TST

.. toctree::
   :maxdepth: 1
   :caption: Revisión y validación

   PROC_Revision_TPL_Previo_Generacion
   PROC_Revision_UC_Previo_Derivacion
   PROC_Revision_Artefactos
   PROC_Validacion_Sphinx
   PROC_Verificacion_Cobertura
   PROC_Identificar_Gaps_Huerfanos

.. toctree::
   :maxdepth: 1
   :caption: Lifecycle documental

   PROC_Crear_Plan_Analisis
   PROC_Crear_Estructura_Directorios_Tmp
   PROC_Cambio_Requisitos
   PROC_Aprobacion_Documentos
   PROC_Actualizacion_Modelo_Documental
   PROC_Auditoria_Documental
   PROC_Versionado_Semantico
   PROC_Publicacion_Documentacion
   PROC_Congelamiento_Subdominio
   PROC_Descongelamiento_Subdominio

.. toctree::
   :maxdepth: 1
   :caption: Procedimiento integrador (meta-flujo)

   PROC_Elaboracion_Completa_Requisitos

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
