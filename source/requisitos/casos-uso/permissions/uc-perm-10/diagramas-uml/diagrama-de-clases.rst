8.3 Diagrama de clases
======================

.. uml::
 :caption: Estructura

 @startuml

 class AuditQueryService {
   list(filters, cursor, page_size)
   get(id)
   aggregate(filters, group_by)
   export(filters, format)
 }

 class AuditRepo {
   query(filters, cursor, limit)
   get_by_id(id)
   aggregate(filters, group_by)
 }

 class CursorEncoder {
   encode(last)
   decode(cursor)
 }

 class Sanitizer {
   truncate(payload)
 }

 class ExportWorker {
   enqueue(job)
   process(job)
 }

 AuditQueryService --> AuditRepo
 AuditQueryService --> CursorEncoder
 AuditQueryService --> Sanitizer
 AuditQueryService --> ExportWorker

 @enduml

