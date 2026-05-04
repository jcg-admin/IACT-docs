.. meta::
 :artefacto: AT_UC_OPR_07_PROCESS
 :tipo: Diagrama Arquitectonico — Process View
 :dominio: arquitectura_tecnica
 :subdominio: uc/ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_07_process:

==========================================================
UC_OPR_07 — Solicitar Break Pausa: Process View
==========================================================

Flujo de actividades y concurrencia para UC_OPR_07.

.. uml::
 :caption: UC_OPR_07 — Process View (actividades)

 @startuml

 start
 :request_break solicita Solicitar Break Pausa;
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

 :doc:`/requisitos/casos-uso/operator/uc-opr-07/flujo-principal`
 :doc:`/requisitos/casos-uso/operator/uc-opr-07/flujos-alternos`
