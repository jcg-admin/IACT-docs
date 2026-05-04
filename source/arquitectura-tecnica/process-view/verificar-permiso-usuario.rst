.. meta::
 :artefacto: AT_UC_PERM_07_PROCESS
 :tipo: Diagrama Arquitectonico — Process View
 :dominio: arquitectura_tecnica
 :subdominio: ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_perm_07_process:

==================================================================
UC_PERM_07 — Verificar Permiso de Usuario: Process View
==================================================================

Flujo de actividades y concurrencia para UC_PERM_07.

.. uml::
 :caption: UC_PERM_07 — Process View (actividades)

 @startuml

 start
 :view_assignments solicita Verificar Permiso de Usuario;
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

 :doc:`/requisitos/casos-uso/permissions/uc-perm-07/flujo-principal`
 :doc:`/requisitos/casos-uso/permissions/uc-perm-07/flujos-alternos`
