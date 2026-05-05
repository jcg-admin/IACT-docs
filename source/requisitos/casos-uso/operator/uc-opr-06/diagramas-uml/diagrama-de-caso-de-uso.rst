8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_OPR_06 — actores y casos asociados

 @startuml

 left to right direction

 actor "set_call_disposition" as INVOKER
 actor "DispositionCatalog" as CATALOG <<sistema>>
 actor "CallSessionRepo" as REPO <<sistema>>
 actor "PIISanitizer" as SANITIZER <<sistema>>

 rectangle "MOD_Operator" {
   usecase "UC_OPR_06\nIngresar Disposition" as UC_OPR_06
   usecase "Validar agente\nen after_call_work" as VALIDAR_STATE
   usecase "Validar code\n(catalogo configurable)" as VALIDAR_CODE
   usecase "Sanitizar notes\n(≤ 500 chars, sin PII)" as SANITIZAR
   usecase "Persistir Disposition\nen CallSession" as PERSISTIR
 }

 INVOKER --> UC_OPR_06
 UC_OPR_06 ..> VALIDAR_STATE : <<include>>
 UC_OPR_06 ..> VALIDAR_CODE : <<include>>
 UC_OPR_06 ..> SANITIZAR : <<include>>
 UC_OPR_06 ..> PERSISTIR : <<include>>

 VALIDAR_CODE --> CATALOG
 SANITIZAR --> SANITIZER
 PERSISTIR --> REPO

 note bottom of VALIDAR_CODE
   Catalog: resolved, follow_up,
   escalation, unreachable,
   do_not_call (configurable).
   Disposition obligatoria post-call.
 end note

 note bottom of SANITIZAR
   CNST-026 sin PII en notes.
   Max 500 chars. Sanitizer
   detecta numeros telefonicos,
   emails, ids de cliente.
 end note

 @enduml
