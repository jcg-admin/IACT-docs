.. meta::
 :artefacto: AT_UC_RPT_15_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_15_domain:

============================================================
UC_RPT_15 — Reporte de Transferencias: Domain Model
============================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/reports/uc-rpt-15/index`.

.. uml::
 :caption: UC_RPT_15 — Domain Model

 @startuml

 left to right direction

 class ReporteTransferencia
 class BaseAnaliticaIVR
 class ReporteTransferencia

 ReporteTransferencia --> BaseAnaliticaIVR
 BaseAnaliticaIVR --> ReporteTransferencia

 @enduml


.. uml::
 :caption: UC_RPT_15 — Reporte de Transferencias — Estado de Reporte

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
 :doc:`/requisitos/casos-uso/reports/uc-rpt-15/index`
