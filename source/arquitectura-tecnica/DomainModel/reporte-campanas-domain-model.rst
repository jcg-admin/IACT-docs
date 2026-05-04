.. meta::
 :artefacto: AT_UC_RPT_14_DOMAIN_DOMAIN_MODEL
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_14_domain_domain_model:

========================
UC_RPT_14 — Domain Model
========================

UC_RPT_14 — Reporte de Campanas: Domain Model
======================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/reports/uc-rpt-14/index`.

.. uml::
 :caption: UC_RPT_14 — Domain Model

 @startuml

 left to right direction

 class ReporteCampana
 class BaseAnaliticaIVR
 class ReporteCampana

 ReporteCampana --> BaseAnaliticaIVR
 BaseAnaliticaIVR --> ReporteCampana

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/reports/uc-rpt-14/index`
