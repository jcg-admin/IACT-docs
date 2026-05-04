.. meta::
 :artefacto: AT_UC_RPT_01_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_01_domain:

================================================
UC_RPT_01 — Ver Dashboard: Domain Model
================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/reports/uc-rpt-01/index`.

.. uml::
 :caption: UC_RPT_01 — Domain Model

 @startuml

 left to right direction

 class DashboardWidget
 class BaseAnaliticaIVR
 class DashboardWidget

 DashboardWidget --> BaseAnaliticaIVR
 BaseAnaliticaIVR --> DashboardWidget

 @enduml


.. uml::
 :caption: UC_RPT_01 — Ver Dashboard — Estado de Reporte

 @startuml
 hide empty description

 [*] --> Solicitado : solicitar reporte
 Solicitado --> Generando : iniciar generacion
 Generando --> Listo : generacion exitosa
 Listo --> Entregado : descargar / visualizar
 Entregado --> Archivado : archivar
 Generando --> Error : fallo en generacion
 Error --> [*] : descartar
 Archivado --> [*] : purgar

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/reports/uc-rpt-01/index`
