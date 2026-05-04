.. meta::
 :artefacto: AT_UC_RPT_17_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: uc/DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_17_domain:

=============================================================
UC_RPT_17 — Reporte de Clientes Unicos: Domain Model
=============================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/reports/uc-rpt-17/index`.

.. uml::
 :caption: UC_RPT_17 — Domain Model

 @startuml

 left to right direction

 class ReporteCliente
 class BaseAnaliticaIVR
 class ReporteCliente

 ReporteCliente --> BaseAnaliticaIVR
 BaseAnaliticaIVR --> ReporteCliente

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/reports/uc-rpt-17/index`
