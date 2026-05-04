8.4 Diagrama de secuencia (P-09)
================================

.. uml::
 :caption: UC_PERM_09 — audit-or-abort

 @startuml

 participant "Caller UC" as CallerUc
 participant "TxManager" as Txmanager
 participant "AuditService" as Auditservice
 participant "AuditRepo" as Auditrepo
 participant "AlertHook" as Alerthook

 CallerUc -> Txmanager: BEGIN
 Txmanager --> CallerUc: tx
 CallerUc -> Auditservice: emit(event, ctx)
 Auditservice -> Auditservice: validate + PII scan + sanitize
 Auditservice -> Auditrepo: registrar (in tx)
 Auditrepo --> Auditservice: id
 Auditservice --> CallerUc: id
 CallerUc -> Txmanager: COMMIT
 Txmanager --> CallerUc: ok
 Txmanager -> Alerthook: on_commit(event)
 Alerthook -> Alerthook: push to AlertEngine

 note over CallerUc, Auditrepo
   Si Auditservice o Auditrepo fallan, CallerUc hace ROLLBACK.
   La operacion principal no avanza.
 end note

 @enduml
