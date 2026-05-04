.. meta::
 :artefacto: AT_UC_PERM_06_PROCESS
 :tipo: Diagrama Arquitectonico — Process View
 :dominio: arquitectura_tecnica
 :subdominio: uc/ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_perm_06_process:

===============================================================
UC_PERM_06 — Asignar Funciones a Grupo: Process View
===============================================================

Flujo de actividades y concurrencia para UC_PERM_06.

.. uml::
 :caption: UC_PERM_06 — Process View (actividades)

 @startuml

 start
 :assign_functions_to_group solicita Asignar Funciones a Grupo;
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

 :doc:`/requisitos/casos-uso/permissions/uc-perm-06/flujo-principal`
 :doc:`/requisitos/casos-uso/permissions/uc-perm-06/flujos-alternos`
