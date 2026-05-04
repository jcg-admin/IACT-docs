.. meta::
 :artefacto: AT_UC_CLI_05_PROCESS
 :tipo: Diagrama Arquitectonico — Process View
 :dominio: arquitectura_tecnica
 :subdominio: ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_cli_05_process:

=================================================================
UC_CLI_05 — Calificar Atencion Post-Call: Process View
=================================================================

Flujo de actividades y concurrencia para UC_CLI_05.

.. uml::
 :caption: UC_CLI_05 — Process View (actividades)

 @startuml

 start
 :CallerExterno solicita Calificar Atencion Post-Call;
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

 :doc:`/requisitos/casos-uso/caller/uc-cli-05/flujo-principal`
 :doc:`/requisitos/casos-uso/caller/uc-cli-05/flujos-alternos`
