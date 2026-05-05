.. meta::
 :artefacto: AT_UC_UC_AUD_02
 :tipo: Diagrama Arquitectonico — UC
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_uc_uc_aud_02:

============================
UC_AUD_02 — Buscar Auditoria
============================

Diagrama de caso de uso (uml-07) para ``UC_AUD_02``.

.. uml::
 :caption: UC_AUD_02 — Buscar Auditoria

 @startuml
 left to right direction

 actor Auditor

 rectangle "MOD_Audit" {
   usecase "UC_AUD_02\nBuscar Auditoria" as UC_AUD_02
 }

 Auditor --> UC_AUD_02

 @enduml

Especificación
==============

La especificación completa de este UC vive en:

- :doc:`/requisitos/casos-uso/audit/uc-aud-02/index`

Vista de módulo
===============

Para ver este UC en el contexto de todos los UCs del módulo,
ver :doc:`/arquitectura-tecnica/use-case-view/audit/index`.
