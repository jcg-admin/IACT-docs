.. meta::
 :artefacto: AT_UC_LOG_01_DOMAIN_ESTADO
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_log_01_domain_estado:

=============================================================
UC_LOG_01 — Consultar Logs del Sistema — Estado de EntradaLog
=============================================================

.. uml::
 :caption: UC_LOG_01 — Consultar Logs del Sistema — Estado de EntradaLog

 @startuml
 hide empty description

 [*] --> Generado : evento tecnico ocurre
 Generado --> Almacenado : escribir en log
 Almacenado --> Consultable : indice disponible
 Consultable --> Archivado : rotacion de logs
 Archivado --> [*] : purgar segun retencion

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/logs/uc-log-01/index`

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/logs/uc-log-01/index`
