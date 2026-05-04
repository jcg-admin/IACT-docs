.. meta::
 :artefacto: AT_UC_RPT_03_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: uc/DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_03_domain:

==========================================================
UC_RPT_03 — Ver Reportes Historicos: Domain Model
==========================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/reports/uc-rpt-03/index`.

.. uml::
 :caption: UC_RPT_03 — Domain Model

 @startuml

 left to right direction

 class ReporteHistorico
 class BaseAnaliticaIVR
 class ReporteHistorico

 ReporteHistorico --> BaseAnaliticaIVR
 BaseAnaliticaIVR --> ReporteHistorico

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/reports/uc-rpt-03/index`
