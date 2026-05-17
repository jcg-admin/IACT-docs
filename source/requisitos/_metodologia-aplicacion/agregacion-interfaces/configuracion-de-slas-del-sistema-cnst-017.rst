7.1 Configuración de SLAs del sistema (CNST_017)
------------------------------------------------

.. uml::

   @startuml
   allowmixing

   class ConfiguracionSLA {
     {static} - sla_max_seg : Integer = 10
     {static} - retencion_max_anios : Integer = 2
     {static} - export_csv_max : Integer = 100000
     {static} - export_excel_max : Integer = 50000
     {static} - export_pdf_max : Integer = 10000
     {static} - throttling_intentos_login : Integer = 5
     {static} - throttling_ventana_min : Integer = 5
     {static} + getSlaMaxSeg() : Integer
     {static} + getExportLimit(formato : Enum) : Integer
   }
   note right of ConfiguracionSLA
     Todos los atributos son
     **archivador** (subrayados):
     una sola configuración
     compartida por todo el
     sistema. Refleja:
       CNST_017 (SLA)
       CNST_015 (retención 2 años)
       CNST_019/020 (export)
       CNST_011 (throttling)
   end note
   @enduml
