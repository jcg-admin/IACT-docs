.. meta::
 :artefacto: AT_UC_LOG_02_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_log_02_domain:

=========================================================
UC_LOG_02 — Consultar Logs del ETL: Domain Model
=========================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/logs/uc-log-02/index`.

.. uml::
 :caption: UC_LOG_02 — Domain Model

 @startuml

 left to right direction

 class ETLLogEntry
 class etl_runs
 class ETLLogEntry

 ETLLogEntry --> etl_runs
 etl_runs --> ETLLogEntry

 @enduml


.. uml::
 :caption: UC_LOG_02 — Consultar Logs del ETL — Estado de EntradaLog

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
 :doc:`/requisitos/casos-uso/logs/uc-log-02/index`
