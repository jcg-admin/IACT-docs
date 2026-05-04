.. meta::
 :artefacto: AT_UC_OPR_04_PROCESS
 :tipo: Diagrama Arquitectonico — Process View
 :dominio: arquitectura_tecnica
 :subdominio: uc/ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_04_process:

========================================================
UC_OPR_04 — Hold Unhold Llamada: Process View
========================================================

Flujo de actividades y concurrencia para UC_OPR_04.

.. uml::
 :caption: UC_OPR_04 — Process View (actividades)

 @startuml

 start
 :hold_calls solicita Hold Unhold Llamada;
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

 :doc:`/requisitos/casos-uso/operator/uc-opr-04/flujo-principal`
 :doc:`/requisitos/casos-uso/operator/uc-opr-04/flujos-alternos`
