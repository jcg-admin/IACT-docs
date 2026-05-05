8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_PERM_07 — verificar permiso

 @startuml
 left to right direction

 actor "rbac_decorator" as rbac_decorator
 actor "view_assignments" as ADMINISTRADOR_SISTEMA
 actor "view_own_navigation" as VIEW_NAVEGACION_DINAMICA

 rectangle "MOD_Permissions (servicio)" {
   usecase "UC_PERM_07\nVerificar Permiso" as UC07
   usecase "Bulk check" as VERIFICACION_MASIVA
   usecase "Cache lookup" as CACHE_PERMISOS
   usecase "Algoritmo precedencia" as AlgoritmoPrecedencia
 }

 rbac_decorator --> UC07
 ADMINISTRADOR_SISTEMA --> UC07
 VIEW_NAVEGACION_DINAMICA --> VERIFICACION_MASIVA
 UC07 ..> CACHE_PERMISOS : <<include>>
 UC07 ..> ALG : <<include>>
 VERIFICACION_MASIVA ..> CACHE_PERMISOS : <<include>>
 VERIFICACION_MASIVA ..> ALG : <<include>>

 note bottom of UC07
   Read-only. Sin audit por invocacion.
   Fail-closed ante errores.
 end note

 @enduml

