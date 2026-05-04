.. meta::
 :artefacto: AT_UC_USR_03_PROCESS
 :tipo: Diagrama Arquitectonico — Process View
 :dominio: arquitectura_tecnica
 :subdominio: ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_usr_03_process:

======================================================
UC_USR_03 — Modificar Usuario: Process View
======================================================

Flujo de actividades y concurrencia para UC_USR_03.

.. uml::
 :caption: UC_USR_03 — Process View (actividades)

 @startuml

 start
 :update_users solicita Modificar Usuario;
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

 :doc:`/requisitos/casos-uso/users/uc-usr-03/flujo-principal`
 :doc:`/requisitos/casos-uso/users/uc-usr-03/flujos-alternos`
