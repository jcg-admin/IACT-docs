.. meta::
 :artefacto: AT_UC_RPT_13_DOMAIN_ESTADO
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_13_domain_estado:

================================================
UC_RPT_13 — Reporte de Colas — Estado de Reporte
================================================

.. uml::
 :caption: UC_RPT_13 — Reporte de Colas — Estado de Reporte

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
 :doc:`/requisitos/casos-uso/reports/uc-rpt-13/index`

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/reports/uc-rpt-13/index`
