.. _uc-aud-01-parte-08-diagrama-clases:

8.3 Diagrama de clases
=======================

.. uml::
 :caption: UC_AUD_01 — clases involucradas en consulta audit.

 @startuml

 class GeneralAuditService {
   + query(filters, cursor) : AuditQueryResult
 }

 class AuditRepo {
   + find(filters, cursor) : List
 }

 class CursorEncoder {
   + encode(state) : String
   + decode(cursor) : State
 }

 class AuditService {
   + emit(event_type, payload) : AuditEvent
 }

 class PIIScanner {
   + sanitize(rows) : List
 }

 GeneralAuditService --> AuditRepo : queries
 GeneralAuditService --> CursorEncoder : paginates
 GeneralAuditService --> PIIScanner : sanitizes
 GeneralAuditService --> AuditService : emits meta-audit

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/audit-event`.
 - :doc:`/arquitectura-tecnica/domain-model/audit-query-service`.
 - :doc:`/arquitectura-tecnica/domain-model/audit-repo`.
 - :doc:`/arquitectura-tecnica/domain-model/cursor-encoder`.
 - :doc:`/arquitectura-tecnica/domain-model/pii-scanner`.
