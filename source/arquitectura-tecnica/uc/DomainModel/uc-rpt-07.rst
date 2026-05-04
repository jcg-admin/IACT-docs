.. meta::
 :artefacto: AT_UC_RPT_07_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: uc/DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_07_domain:

====================================================
UC_RPT_07 — Programar Reporte: Domain Model
====================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/reports/uc-rpt-07/index`.

.. uml::
 :caption: UC_RPT_07 — Domain Model

 @startuml

 left to right direction

 class ReporteProgramado
 class Reporte
 class ReporteProgramado

 ReporteProgramado --> Reporte
 Reporte --> ReporteProgramado

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/reports/uc-rpt-07/index`
