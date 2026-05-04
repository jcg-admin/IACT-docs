.. meta::
 :artefacto: AT_UC_PERM_08_PROCESS
 :tipo: Diagrama Arquitectonico — Process View
 :dominio: arquitectura_tecnica
 :subdominio: ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_perm_08_process:

===========================================================
UC_PERM_08 — Generar Menu Dinamico: Process View
===========================================================

Flujo de actividades y concurrencia para UC_PERM_08.

.. uml::
 :caption: UC_PERM_08 — Process View (actividades)

 @startuml

 start
 :view_assignments solicita Generar Menu Dinamico;
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

 :doc:`/requisitos/casos-uso/permissions/uc-perm-08/flujo-principal`
 :doc:`/requisitos/casos-uso/permissions/uc-perm-08/flujos-alternos`
