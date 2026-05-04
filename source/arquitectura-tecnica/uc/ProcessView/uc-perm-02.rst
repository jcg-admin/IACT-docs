.. meta::
 :artefacto: AT_UC_PERM_02_PROCESS
 :tipo: Diagrama Arquitectonico — Process View
 :dominio: arquitectura_tecnica
 :subdominio: uc/ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_perm_02_process:

=============================================================
UC_PERM_02 — Revocar Grupo a Usuario: Process View
=============================================================

Flujo de actividades y concurrencia para UC_PERM_02.

.. uml::
 :caption: UC_PERM_02 — Process View (actividades)

 @startuml

 start
 :revoke_function_group solicita Revocar Grupo a Usuario;
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

 :doc:`/requisitos/casos-uso/permissions/uc-perm-02/flujo-principal`
 :doc:`/requisitos/casos-uso/permissions/uc-perm-02/flujos-alternos`
