.. meta::
 :artefacto: ARQ_MOD_007_DIAG_FLUJO_EMISION
 :tipo: Diagrama Arquitectonico — Comportamiento de Modulo
 :dominio: arquitectura_tecnica
 :subdominio: modulos/audit/diagramas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _arq_mod_007_flujo_emision_auditoria:

=======================================
Flujo de Emision de Evento de Auditoria
=======================================

Flujo de Emision de Evento de Auditoria
=========================================

.. uml::
 :caption: Secuencia de emision de AuditEvent — post-commit en transaccion separada.

 @startuml

 participant "Servicio de Origen\n(UC_ACC, UC_USR, etc.)" as ServicioDeOrigen
 participant "Middleware\nAudit Emitter" as Middleware
 database "audit_log\n(PostgreSQL — append-only)" as AREP

 ServicioDeOrigen -> ServicioDeOrigen : ejecuta operacion de escritura
 ServicioDeOrigen -> Middleware : notificar evento\n{tipo, usuario, entidad, timestamp}
 note right of ServicioDeOrigen
   La operacion principal
   ya fue confirmada en BD.
   El audit no la bloquea.
 end note
 Middleware -> AREP : registrar AuditEvent\n(transaccion separada)

 alt fallo en insercion de audit
   Middleware -> Middleware : registrar alarma interna\n(no abortar operacion original)
 end

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modulos/audit/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
