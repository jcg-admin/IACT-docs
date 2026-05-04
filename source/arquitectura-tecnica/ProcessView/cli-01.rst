.. meta::
 :artefacto: AT_UC_CLI_01_PROCESS
 :tipo: Diagrama Arquitectonico — Process View
 :dominio: arquitectura_tecnica
 :subdominio: ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_cli_01_process:

===================================================================
UC_CLI_01 — Iniciar Llamada al Call Center: Process View
===================================================================

Flujo de actividades y concurrencia para UC_CLI_01.

.. uml::
 :caption: UC_CLI_01 — Process View (actividades)

 @startuml

 start
 :CallerExterno solicita Iniciar Llamada al Call Center;
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

 :doc:`/requisitos/casos-uso/caller/uc-cli-01/flujo-principal`
 :doc:`/requisitos/casos-uso/caller/uc-cli-01/flujos-alternos`
