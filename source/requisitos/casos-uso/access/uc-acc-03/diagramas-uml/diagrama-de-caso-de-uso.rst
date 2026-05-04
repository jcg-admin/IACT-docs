8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_ACC_03 — actores y casos asociados

 @startuml

 left to right direction

 actor "view_assignments" as INVOKER
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "Sistema" as Sistema <<sistema>>

 rectangle "MOD_Access" {
   usecase "UC_ACC_03\nConsultar Permisos" as UC03
   usecase "Cargar Assignments\ndirectos" as DIR
   usecase "Expandir AGRs\nen funciones" as AGR
   usecase "Cargar permisos\nexcepcionales" as EXC
   usecase "Consolidar\n+ metadata origen" as CONS
   usecase "Detectar SoD\ninformativo" as SOD
   usecase "Audit selectivo\nP-16" as AUDS
 }

 INVOKER --> UC03
 UC03 ..> DIR : <<include>>
 UC03 ..> AGR : <<include>>
 UC03 ..> EXC : <<include>>
 UC03 ..> CONS : <<include>>
 UC03 ..> SOD : <<include>>
 UC03 ..> AUDS : <<include>>
 Sistema --> AUDS
 AUDS --> view_audit_log

 note bottom of CONS
   3 fuentes: direct + AGR + excepcional
   deduplicacion + metadata por funcion
 end note
 note bottom of SOD
   INFORMATIVO no bloqueo
   (UC_ACC_01 valida write-time)
 end note

 @enduml

