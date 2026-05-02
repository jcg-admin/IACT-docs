.. _arq-mod-007-diagramas:

================================================
ARQ_MOD_007 — Diagramas de Comportamiento
================================================


Flujo de Emision de Evento de Auditoria
=========================================

.. uml::
 :caption: Secuencia de emisión de AuditEvent — post-commit en transacción separada.

 @startuml

 participant "Servicio\nde Origen" as SVC
 participant "Middleware\nAudit Emitter" as AEM
 participant "Repositorio\nde Auditoría" as AREP

 SVC -> SVC : ejecuta operación de escritura\n(UC_ACC_01, UC_USR_01, etc.)
 SVC -> AEM : notifica evento\n{tipo, usuario, entidad, timestamp}
 note right of SVC
   La operación principal
   ya fue confirmada en BD.
   El audit no la bloquea.
 end note
 AEM -> AREP ++ : insertar AuditEvent\n(transacción separada, append-only)
 return AuditEvent persistido

 alt fallo en inserción de audit
   AEM -> AEM : registrar alarma interna\n(no abortar la operación original)
 end

 @enduml
