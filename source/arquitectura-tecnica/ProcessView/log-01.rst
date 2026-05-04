.. meta::
 :artefacto: AT_UC_LOG_01_PROCESS
 :tipo: Diagrama Arquitectonico — Process View
 :dominio: arquitectura_tecnica
 :subdominio: ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_log_01_process:

===============================================================
UC_LOG_01 — Consultar Logs del Sistema: Process View
===============================================================

Flujo de actividades y concurrencia para UC_LOG_01.

.. uml::
 :caption: UC_LOG_01 — Process View (actividades)

 @startuml

 start
 :view_application_logs solicita Consultar Logs del Sistema;
 :Validar autenticacion y permisos RBAC;
 if (permisos validos?) then (si)
   :Ejecutar logica principal;
   :Persistir resultado;
   :Registrar AuditEvent;
   :Retornar respuesta exitosa;
 else (no)
   :Retornar error 403;
 endif
 stop

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/logs/uc-log-01/flujo-principal`
 :doc:`/requisitos/casos-uso/logs/uc-log-01/flujos-alternos`
