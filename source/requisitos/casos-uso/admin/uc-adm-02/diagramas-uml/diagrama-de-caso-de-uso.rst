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
 actor "PermissionService" as PS <<sistema>>
 actor "PermissionCache" as PC <<sistema>>
 actor "EvaluatorReloader" as EE <<sistema>>
 actor "AuditService" as AS <<sistema>>

 rectangle "MOD_Admin" {
   usecase "UC_ADM_02\nGestionar Catalogo\nde Funciones" as UC_ADM_02
   usecase "Validar codename\nunico (snake_case)" as VALIDAR_CODENAME
   usecase "Validar module\nvalido" as VALIDAR_MODULE
   usecase "Validar scope" as VALIDAR_SCOPE
   usecase "Persistir Function\n(BR-009 baja logica)" as PERSISTIR
   usecase "Emitir AuditEvent\nFUNCTION_*" as AUDIT
   usecase "Invalidar cache\nde permisos" as INVALIDAR
   usecase "EvaluatorReloader\n.reload_catalog()" as RELOAD
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
 UC_ADM_02 ..> INVALIDAR : <<include>>
 UC_ADM_02 ..> RELOAD : <<include>>

 INVALIDAR --> PC
 RELOAD --> EE
 RELOAD --> PS
 AUDIT --> AS
 AS --> view_audit_log

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
   AGR-010 system_admin agrupa
   las 4 funciones. Catalogo activo
   alimenta PermissionService y
   construccion del effective_set.
 end note

 @enduml

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/function` —
   entidad Function persistida por este UC.
 - :doc:`/arquitectura-tecnica/domain-model/function-group` —
   FunctionGroup que consume el catalogo activo (UC_ADM_03).
 - :doc:`/arquitectura-tecnica/domain-model/permission-service` —
   servicio que consume catalogo activo para verificacion runtime.
 - :doc:`/arquitectura-tecnica/domain-model/permission-cache` —
   cache invalidada al cambiar catalogo.
 - :doc:`/arquitectura-tecnica/domain-model/evaluator-reloader` —
   notificado para refrescar catalogo en runtime.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor de AuditEvent FUNCTION_*.
 - :doc:`/arquitectura-tecnica/domain-model/audit-event` —
   estructura del evento emitido (CNST-025).
