.. meta::
 :artefacto: AT_UC_RPT_12_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_12_domain:

=====================================================
UC_RPT_12 — Reporte de Agentes: Domain Model
=====================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/reports/uc-rpt-12/index`.

.. uml::
 :caption: UC_RPT_12 — Domain Model

 @startuml

 left to right direction

 class ReporteAgente
 class BaseAnaliticaIVR
 class ReporteAgente

 ReporteAgente --> BaseAnaliticaIVR
 BaseAnaliticaIVR --> ReporteAgente

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/reports/uc-rpt-12/index`
