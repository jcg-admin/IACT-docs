.. meta::
 :artefacto: AT_UC_RPT_02_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: uc/DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_02_domain:

==============================================================
UC_RPT_02 — Ver Metricas en Tiempo Real: Domain Model
==============================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/reports/uc-rpt-02/index`.

.. uml::
 :caption: UC_RPT_02 — Domain Model

 @startuml

 left to right direction

 class MetricaKPI
 class BaseAnaliticaIVR
 class MetricaKPI

 MetricaKPI --> BaseAnaliticaIVR
 BaseAnaliticaIVR --> MetricaKPI

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/reports/uc-rpt-02/index`
