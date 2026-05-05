8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_ADM_02 — actores y casos asociados

 @startuml

 left to right direction

 actor "create_function" as F_CREATE
 actor "update_function" as F_UPDATE
 actor "deactivate_function" as F_DEACTIVATE
 actor "view_functions" as F_VIEW <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "PermissionsEngine" as PE <<sistema>>
 actor "Sistema" as Sistema <<sistema>>

 rectangle "MOD_Admin" {
   usecase "UC_ADM_02\nGestionar Catalogo\nde Funciones" as UC_ADM_02
   usecase "Validar codename\nunico (snake_case)" as VALIDAR_CODENAME
   usecase "Validar module\nvalido" as VALIDAR_MODULE
   usecase "Validar scope" as VALIDAR_SCOPE
   usecase "Persistir Function\n(BR-009 baja logica)" as PERSISTIR
   usecase "AuditEvent\nFUNCTION_*" as AUDIT
   usecase "PermissionsEngine\n.reload_catalog()" as RELOAD
 }

 F_CREATE --> UC_ADM_02
 F_UPDATE --> UC_ADM_02
 F_DEACTIVATE --> UC_ADM_02
 F_VIEW --> UC_ADM_02

 UC_ADM_02 ..> VALIDAR_CODENAME : <<include>>
 UC_ADM_02 ..> VALIDAR_MODULE : <<include>>
 UC_ADM_02 ..> VALIDAR_SCOPE : <<include>>
 UC_ADM_02 ..> PERSISTIR : <<include>>
 UC_ADM_02 ..> AUDIT : <<include>>
 UC_ADM_02 ..> RELOAD : <<include>>

 Sistema --> AUDIT
 Sistema --> RELOAD
 AUDIT --> view_audit_log
 RELOAD --> PE

 note bottom of VALIDAR_CODENAME
   P-44: codename inmutable
   tras creacion. Solo es
   editable description, scope,
   is_active en update.
 end note

 note bottom of AUDIT
   FUNCTION_CREATED / UPDATED /
   DEACTIVATED. CNST-025 alta
   criticidad — define el
   catalogo RBAC del sistema.
 end note

 note right of F_VIEW
   AGR-009 admin_sistema agrupa
   las 4 funciones. Catalogo activo
   alimenta PermissionsEngine y
   construccion del effective_set.
 end note

 @enduml
