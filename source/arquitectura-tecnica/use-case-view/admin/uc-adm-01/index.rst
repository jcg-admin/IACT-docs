.. meta::
 :artefacto: AT_UC_UC_ADM_01
 :tipo: Diagrama Arquitectonico — UC
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_uc_uc_adm_01:

====================
UC_ADM_01
====================

Diagrama de caso de uso (uml-07) para ``UC_ADM_01``.

.. uml::
 :caption: UC_ADM_01 — UC_ADM_01

 @startuml
 left to right direction

 actor SystemAdmin

 rectangle "MOD_Admin" {
   usecase "UC_ADM_01\nUC_ADM_01" as UC_ADM_01
 }

 SystemAdmin --> UC_ADM_01

 @enduml

Especificación
==============

La especificación completa de este UC vive en:

- :doc:`/requisitos/casos-uso/admin/uc-adm-01/index`

Vista de módulo
===============

Para ver este UC en el contexto de todos los UCs del módulo,
ver :doc:`/arquitectura-tecnica/use-case-view/admin/index`.
