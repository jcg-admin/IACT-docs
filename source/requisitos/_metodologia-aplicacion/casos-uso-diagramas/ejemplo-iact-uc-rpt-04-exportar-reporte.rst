5.1 Ejemplo IACT — UC_RPT_04 (Exportar reporte)
-----------------------------------------------

.. uml::

   @startuml

   left to right direction
   actor Supervisor

   rectangle "IACT" {
     usecase "UC_RPT_04\nExportar reporte"  as RPT04
     usecase "UC_RPT_03\nVer reportes\nhistóricos"   as RPT03
     usecase "UC_PERM_07\nVerificar permiso\n+ throttling\nCNST_020"            as SERVICIO_PERMISOS
     usecase "Aplicar filtro\nsegmento\n(BR_012,\nCNST_008)"                    as APLICAR_FILTRO_SEGMENTO
     usecase "Registrar en\nAuditLog\n(CNST_025)"                               as SERVICIO_AUDITORIA
   }

   Supervisor --> RPT04

   RPT04 ..> SERVICIO_PERMISOS  : <<include>>
   RPT04 ..> RPT03 : <<include>>
   RPT04 ..> APLICAR_FILTRO_SEGMENTO   : <<include>>
   RPT04 ..> SERVICIO_AUDITORIA   : <<include>>

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
