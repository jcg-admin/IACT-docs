8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_PERM_07 — verificar permiso

 @startuml
 left to right direction

 actor "rbac_decorator" as rbac_decorator
 actor "view_assignments" as ADMIN
 actor "view_own_navigation" as MENU

 rectangle "MOD_Permissions (servicio)" {
   usecase "UC_PERM_07\nVerificar Permiso" as UC07
   usecase "Bulk check" as BULK
   usecase "Cache lookup" as CACHE
   usecase "Algoritmo precedencia" as AlgoritmoPrecedencia
 }

 rbac_decorator --> UC07
 ADMIN --> UC07
 MENU --> BULK
 UC07 ..> CACHE : <<include>>
 UC07 ..> ALG : <<include>>
 BULK ..> CACHE : <<include>>
 BULK ..> ALG : <<include>>

 note bottom of UC07
   Read-only. Sin audit por invocacion.
   Fail-closed ante errores.
 end note

 @enduml

