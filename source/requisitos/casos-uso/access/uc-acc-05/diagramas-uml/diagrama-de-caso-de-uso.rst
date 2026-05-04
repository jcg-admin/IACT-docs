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
   usecase "UC_ACC_05\nGestionar SoD" as UC05
   usecase "Listar reglas" as VistaListado
   usecase "Crear regla" as UCCRE
   usecase "Modificar regla" as UCMOD
   usecase "Retirar regla" as UCRET
   usecase "AuditEvent" as AuditEmitter
   usecase "Invalidar cache\nde reglas" as CACHE
 }

 VIEWER --> UC05
 MANAGER --> UC05
 UC05 ..> LST : <<extend>>
 UC05 ..> UCCRE : <<extend>>
 UC05 ..> UCMOD : <<extend>>
 UC05 ..> UCRET : <<extend>>
 UCCRE ..> EMI : <<include>>
 UCMOD ..> EMI : <<include>>
 UCRET ..> EMI : <<include>>
 UCCRE ..> CACHE : <<include>>
 UCMOD ..> CACHE : <<include>>
 UCRET ..> CACHE : <<include>>
 EMI --> view_audit_log
 SistemaConsumidores ..> CACHE : <<consume>>

 note bottom of CACHE
   UC_ACC_01/04/PERM_03 cargan reglas
   ACTIVE en cache para SoD write-time
 end note

 @enduml

