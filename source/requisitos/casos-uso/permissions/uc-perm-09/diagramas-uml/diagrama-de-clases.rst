8.3 Diagrama de clases
======================

.. uml::
 :caption: Estructura del servicio

 @startuml

 class AuditService {
   emit(event)
   emit_batch(events)
 }

 class AuditValidator {
   validate(event)
 }

 class PIIScanner {
   scan(payload)
 }

 class Sanitizer {
   sanitize(payload)
 }

 class AuditRepo {
   insert(event)
   insert_batch(events)
 }

 class AlertHook {
   on_commit(event)
 }

 AuditService --> AuditValidator
 AuditService --> PIIScanner
 AuditService --> Sanitizer
 AuditService --> AuditRepo
 AuditService --> AlertHook

 note right of AuditRepo
   Tabla append-only.
   CONSTRAINT prohibe actualizar/eliminar.
 end note

 @enduml

