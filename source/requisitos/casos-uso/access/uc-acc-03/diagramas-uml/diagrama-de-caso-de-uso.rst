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
   usecase "UC_ACC_03\nConsultar Permisos" as UC_ACC_03
   usecase "Cargar Assignments\ndirectos" as AsignacionesDirectas
   usecase "Expandir AGRs\nen funciones" as GrupoAcceso
   usecase "Cargar permisos\nexcepcionales" as ExcepcionSistema
   usecase "Consolidar\n+ metadata origen" as CONSOLIDAR_METADATA
   usecase "Detectar separacion\ninformativo" as ValidadorSeparacion
   usecase "Audit selectivo\nP-16" as AUDITORIA_SELECTIVA
 }

 INVOKER --> UC_ACC_03
 UC_ACC_03 ..> DIR : <<include>>
 UC_ACC_03 ..> AGR : <<include>>
 UC_ACC_03 ..> EXC : <<include>>
 UC_ACC_03 ..> CONSOLIDAR_METADATA : <<include>>
 UC_ACC_03 ..> VALIDAR_SEPARATION : <<include>>
 UC_ACC_03 ..> AUDITORIA_SELECTIVA : <<include>>
 Sistema --> AUDITORIA_SELECTIVA
 AUDITORIA_SELECTIVA --> view_audit_log

 note bottom of CONSOLIDAR_METADATA
   3 fuentes: direct + AGR + excepcional
   deduplicacion + metadata por funcion
 end note
 note bottom of VALIDAR_SEPARATION
   INFORMATIVO no bloqueo
   (UC_ACC_01 valida write-time)
 end note

 @enduml

