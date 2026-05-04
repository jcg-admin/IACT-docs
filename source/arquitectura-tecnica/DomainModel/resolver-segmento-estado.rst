.. meta::
 :artefacto: AT_UC_INC_RPT_01_DOMAIN_ESTADO
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_inc_rpt_01_domain_estado:

=====================================================
UC_INC_RPT_01 — Resolver Segmento — Estado de Reporte
=====================================================

.. uml::
 :caption: UC_INC_RPT_01 — Resolver Segmento — Estado de Reporte

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
 :doc:`/requisitos/casos-uso/reports/uc-inc-rpt-01/index`

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/reports/uc-inc-rpt-01/index`
