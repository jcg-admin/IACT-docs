.. meta::
 :artefacto: AT_UC_ACC_03_PROCESS
 :tipo: Diagrama Arquitectonico — Process View
 :dominio: arquitectura_tecnica
 :subdominio: uc/ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_acc_03_process:

=================================================================
UC_ACC_03 — Consultar Permisos Efectivos: Process View
=================================================================

Flujo de actividades y concurrencia para UC_ACC_03.

.. uml::
 :caption: UC_ACC_03 — Process View (actividades)

 @startuml

 start
 :view_assignments solicita Consultar Permisos Efectivos;
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

 :doc:`/requisitos/casos-uso/access/uc-acc-03/flujo-principal`
 :doc:`/requisitos/casos-uso/access/uc-acc-03/flujos-alternos`
