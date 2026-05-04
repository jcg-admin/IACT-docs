.. meta::
 :artefacto: AT_UC_OPR_09_PROCESS
 :tipo: Diagrama Arquitectonico — Process View
 :dominio: arquitectura_tecnica
 :subdominio: ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_09_process:

=====================================================================
UC_OPR_09 — Ver Propio Historial de Llamadas: Process View
=====================================================================

Flujo de actividades y concurrencia para UC_OPR_09.

.. uml::
 :caption: UC_OPR_09 — Process View (actividades)

 @startuml

 start
 :view_own_call_history solicita Ver Propio Historial de Llamadas;
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

 :doc:`/requisitos/casos-uso/operator/uc-opr-09/flujo-principal`
 :doc:`/requisitos/casos-uso/operator/uc-opr-09/flujos-alternos`
