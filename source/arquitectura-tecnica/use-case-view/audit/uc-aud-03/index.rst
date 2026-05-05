.. meta::
 :artefacto: AT_UC_UC_AUD_03
 :tipo: Diagrama Arquitectonico — UC
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_uc_uc_aud_03:

==============================
UC_AUD_03 — Exportar Auditoria
==============================

Diagrama de caso de uso (uml-07) para ``UC_AUD_03``.

.. uml::
 :caption: UC_AUD_03 — Exportar Auditoria

 @startuml
 left to right direction

 actor Auditor

 rectangle "MOD_Audit" {
   usecase "UC_AUD_03\nExportar Auditoria" as UC_AUD_03
 }

 Auditor --> UC_AUD_03

 @enduml

Especificación
==============

La especificación completa de este UC vive en:

- :doc:`/requisitos/casos-uso/audit/uc-aud-03/index`

Vista de módulo
===============

Para ver este UC en el contexto de todos los UCs del módulo,
ver :doc:`/arquitectura-tecnica/use-case-view/audit/index`.
