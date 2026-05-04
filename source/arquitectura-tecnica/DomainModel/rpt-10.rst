.. meta::
 :artefacto: AT_UC_RPT_10_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_10_domain:

================================================
UC_RPT_10 — Guardar Vista: Domain Model
================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/reports/uc-rpt-10/index`.

.. uml::
 :caption: UC_RPT_10 — Domain Model

 @startuml

 left to right direction

 class VistaGuardada
 class FiltroReporte
 class VistaGuardada

 VistaGuardada --> FiltroReporte
 FiltroReporte --> VistaGuardada

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/reports/uc-rpt-10/index`
