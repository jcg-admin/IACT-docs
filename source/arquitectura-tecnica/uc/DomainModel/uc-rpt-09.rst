.. meta::
 :artefacto: AT_UC_RPT_09_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: uc/DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_09_domain:

=====================================================
UC_RPT_09 — Configurar Filtros: Domain Model
=====================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/reports/uc-rpt-09/index`.

.. uml::
 :caption: UC_RPT_09 — Domain Model

 @startuml

 left to right direction

 class FiltroReporte
 class Reporte
 class BaseAnaliticaIVR

 FiltroReporte --> Reporte
 Reporte --> BaseAnaliticaIVR

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/reports/uc-rpt-09/index`
