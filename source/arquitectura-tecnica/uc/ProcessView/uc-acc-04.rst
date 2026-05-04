.. meta::
 :artefacto: AT_UC_ACC_04_PROCESS
 :tipo: Diagrama Arquitectonico — Process View
 :dominio: arquitectura_tecnica
 :subdominio: uc/ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_acc_04_process:

======================================================
UC_ACC_04 — Asignar Agrupador: Process View
======================================================

Flujo de actividades y concurrencia para UC_ACC_04.

.. uml::
 :caption: UC_ACC_04 — Process View (actividades)

 @startuml

 start
 :assign_function_groups solicita Asignar Agrupador;
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

 :doc:`/requisitos/casos-uso/access/uc-acc-04/flujo-principal`
 :doc:`/requisitos/casos-uso/access/uc-acc-04/flujos-alternos`
