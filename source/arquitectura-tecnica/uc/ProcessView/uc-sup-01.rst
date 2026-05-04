.. meta::
 :artefacto: AT_UC_SUP_01_PROCESS
 :tipo: Diagrama Arquitectonico — Process View
 :dominio: arquitectura_tecnica
 :subdominio: uc/ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_sup_01_process:

=======================================================
UC_SUP_01 — Monitorear Llamada: Process View
=======================================================

Flujo de actividades y concurrencia para UC_SUP_01.

.. uml::
 :caption: UC_SUP_01 — Process View (actividades)

 @startuml

 start
 :monitor_live_calls solicita Monitorear Llamada;
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

 :doc:`/requisitos/casos-uso/supervision/uc-sup-01/flujo-principal`
 :doc:`/requisitos/casos-uso/supervision/uc-sup-01/flujos-alternos`
