.. meta::
 :artefacto: AT_UC_SUP_03_PROCESS
 :tipo: Diagrama Arquitectonico — Process View
 :dominio: arquitectura_tecnica
 :subdominio: ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_sup_03_process:

================================================================
UC_SUP_03 — Mensaje Broadcast al Equipo: Process View
================================================================

Flujo de actividades y concurrencia para UC_SUP_03.

.. uml::
 :caption: UC_SUP_03 — Process View (actividades)

 @startuml

 start
 :broadcast_team_messages solicita Mensaje Broadcast al Equipo;
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

 :doc:`/requisitos/casos-uso/supervision/uc-sup-03/flujo-principal`
 :doc:`/requisitos/casos-uso/supervision/uc-sup-03/flujos-alternos`
