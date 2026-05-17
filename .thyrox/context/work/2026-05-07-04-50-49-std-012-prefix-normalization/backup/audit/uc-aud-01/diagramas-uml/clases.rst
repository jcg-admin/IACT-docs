8.3 Clases
==========

.. uml::

 @startuml
 class GeneralAuditService
 class AuditRepo
 class CursorEncoder
 class AuditService
 GeneralAuditService --> AuditRepo
 GeneralAuditService --> CursorEncoder
 GeneralAuditService --> AuditService
 @enduml

