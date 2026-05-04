.. meta::
 :artefacto: AT_UC_RPT_16_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: uc/DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_16_domain:

=======================================================
UC_RPT_16 — Reporte de Menus IVR: Domain Model
=======================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/reports/uc-rpt-16/index`.

.. uml::
 :caption: UC_RPT_16 — Domain Model

 @startuml

 left to right direction

 class ReporteMenuIVR
 class BaseAnaliticaIVR
 class ReporteMenuIVR

 ReporteMenuIVR --> BaseAnaliticaIVR
 BaseAnaliticaIVR --> ReporteMenuIVR

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/reports/uc-rpt-16/index`
