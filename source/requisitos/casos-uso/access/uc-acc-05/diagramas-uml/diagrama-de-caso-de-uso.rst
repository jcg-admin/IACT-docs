8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_ACC_05 — actores y casos asociados

 @startuml
 left to right direction

 actor "view_separation_rules" as VIEWER
 actor "view_separation_rules" as MANAGER
 actor "view_audit_log" as view_audit_log
 actor "Sistema (consumidores)" as SistemaConsumidores

 rectangle "MOD_Access" {
   usecase "UC_ACC_05\nGestionar SoD" as UC_ACC_05
   usecase "Listar reglas" as VistaListado
   usecase "Crear regla" as CREAR_AGRUPADOR
   usecase "Modificar regla" as MODIFICAR_AGRUPADOR
   usecase "Retirar regla" as RETIRAR_AGRUPADOR
   usecase "AuditEvent" as AuditEmitter
   usecase "Invalidar cache\nde reglas" as CACHE_PERMISOS
 }

 VIEWER --> UC_ACC_05
 MANAGER --> UC_ACC_05
 UC_ACC_05 ..> LST : <<extend>>
 UC_ACC_05 ..> CREAR_AGRUPADOR : <<extend>>
 UC_ACC_05 ..> MODIFICAR_AGRUPADOR : <<extend>>
 UC_ACC_05 ..> RETIRAR_AGRUPADOR : <<extend>>
 CREAR_AGRUPADOR ..> EMI : <<include>>
 MODIFICAR_AGRUPADOR ..> EMI : <<include>>
 RETIRAR_AGRUPADOR ..> EMI : <<include>>
 CREAR_AGRUPADOR ..> CACHE_PERMISOS : <<include>>
 MODIFICAR_AGRUPADOR ..> CACHE_PERMISOS : <<include>>
 RETIRAR_AGRUPADOR ..> CACHE_PERMISOS : <<include>>
 EMI --> view_audit_log
 SistemaConsumidores ..> CACHE_PERMISOS : <<consume>>

 note bottom of CACHE_PERMISOS
   UC_ACC_01/04/PERM_03 cargan reglas
   ACTIVE en cache para SoD write-time
 end note

 @enduml

