5.1 Ejemplo IACT — UC_RPT_04 (Exportar reporte)
-----------------------------------------------

.. uml::

   @startuml

   left to right direction
   actor Supervisor

   rectangle "IACT" {
     usecase "UC_RPT_04\nExportar reporte"  as RPT04
     usecase "UC_RPT_03\nVer reportes\nhistóricos"   as RPT03
     usecase "UC_PERM_07\nVerificar permiso\n+ throttling\nCNST_020"            as PERM
     usecase "Aplicar filtro\nsegmento\n(BR_012,\nCNST_008)"                    as SEG
     usecase "Registrar en\nAuditLog\n(CNST_025)"                               as AUD
   }

   Supervisor --> RPT04

   RPT04 ..> PERM  : <<include>>
   RPT04 ..> RPT03 : <<include>>
   RPT04 ..> SEG   : <<include>>
   RPT04 ..> AUD   : <<include>>

   note right of RPT04
     UC_RPT_04 INCLUYE:
       - Verificar permiso del formato
         (CSV / Excel / PDF) con
         throttling diario CNST_020
       - Ver reporte histórico que se
         exporta (UC_RPT_03)
       - Aplicar filtro de segmento
         del usuario (BR_012)
       - Registrar export en
         AuditLog inmutable (CNST_025)
   end note
   @enduml
