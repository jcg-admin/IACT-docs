.. meta::
 :artefacto: AT_UC_USR_02_PROCESS
 :tipo: Diagrama Arquitectonico — Process View
 :dominio: arquitectura_tecnica
 :subdominio: ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_usr_02_process:

=======================================================
UC_USR_02 — Consultar Usuarios: Process View
=======================================================

Flujo de actividades y concurrencia para UC_USR_02.

.. uml::
 :caption: UC_USR_02 — Process View (actividades)

 @startuml

 start
 :list_users solicita Consultar Usuarios;
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

 :doc:`/requisitos/casos-uso/users/uc-usr-02/flujo-principal`
 :doc:`/requisitos/casos-uso/users/uc-usr-02/flujos-alternos`
