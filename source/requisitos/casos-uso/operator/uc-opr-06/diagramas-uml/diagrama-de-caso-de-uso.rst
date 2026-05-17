8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_OPR_06 — actores y casos asociados

 @startuml

 left to right direction

 actor "set_call_disposition" as INVOKER
 actor "Action" as ACTION <<sistema>>
 actor "Call" as CALL <<sistema>>
 actor "PIIScanner" as PII <<sistema>>
 actor "Sanitizer" as SAN <<sistema>>

 rectangle "MOD_Operator" {
   usecase "UC_OPR_06\nIngresar Disposition" as UC_OPR_06
   usecase "Validar agente\nen after_call_work" as VALIDAR_STATE
   usecase "Validar code\n(catalogo Action)" as VALIDAR_CODE
   usecase "Sanitizar notes\n(≤ 500 chars, sin PII)" as SANITIZAR
   usecase "Persistir Disposition\nen Call" as PERSISTIR
 }

 INVOKER --> UC_OPR_06
 UC_OPR_06 ..> VALIDAR_STATE : <<include>>
 UC_OPR_06 ..> VALIDAR_CODE : <<include>>
 UC_OPR_06 ..> SANITIZAR : <<include>>
 UC_OPR_06 ..> PERSISTIR : <<include>>

 VALIDAR_CODE --> ACTION
 SANITIZAR --> PII
 SANITIZAR --> SAN
 PERSISTIR --> CALL

 note bottom of VALIDAR_CODE
   Catalog: resolved, follow_up,
   escalation, unreachable,
   do_not_call (configurable
   via Action entity).
 end note

 note bottom of SANITIZAR
   CNST-026 sin PII en notes.
   Max 500 chars. PIIScanner
   detecta numeros telefonicos,
   emails, ids de cliente;
   Sanitizer reemplaza.
 end note

 @enduml

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/call` —
   Call con campos disposition_code + disposition_notes.
 - :doc:`/arquitectura-tecnica/domain-model/action` —
   catalogo configurable de disposition codes.
 - :doc:`/arquitectura-tecnica/domain-model/pii-scanner` —
   detector de PII en notes.
 - :doc:`/arquitectura-tecnica/domain-model/sanitizer` —
   sanitizador que reemplaza PII detectada.
