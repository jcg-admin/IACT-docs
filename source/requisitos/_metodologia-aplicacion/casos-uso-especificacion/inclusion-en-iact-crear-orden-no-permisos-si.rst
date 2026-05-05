5.1 Inclusión en IACT — Crear orden NO; permisos SÍ
---------------------------------------------------

En IACT, casi todos los UCs operativos **incluyen UC_PERM_07
(Verificar permiso de usuario)** como primer paso. Es el
equivalente a *"abrir la máquina"* del ejemplo del libro.

.. uml::

   @startuml

   left to right direction
   actor Operador
   actor Supervisor
   actor Auditor

   rectangle "IACT" {
     usecase "UC_RPT_01\nVer dashboard"          as RPT01
     usecase "UC_RPT_03\nVer reportes históricos" as RPT03
     usecase "UC_RPT_04\nExportar reporte"        as RPT04
     usecase "UC_AUD_01\nConsultar auditoría"     as AUD01
     usecase "UC_PIP_04\nSolicitar reintento ETL" as PIP04
     usecase "UC_PERM_07\nVerificar permiso"      as PERM07
     usecase "Registrar en AuditLog\n(CNST_025)"  as AUDLOG
   }

   Operador   --> RPT01
   Operador   --> RPT04
   Supervisor --> RPT03
   Auditor    --> AUD01

   RPT01 ..> PERM07  : <<include>>
   RPT03 ..> PERM07  : <<include>>
   RPT04 ..> PERM07  : <<include>>
   AUD01 ..> PERM07  : <<include>>
   PIP04 ..> PERM07  : <<include>>

   RPT01 ..> AUDLOG  : <<include>>
   RPT03 ..> AUDLOG  : <<include>>
   RPT04 ..> AUDLOG  : <<include>>
   AUD01 ..> AUDLOG  : <<include>>
   PIP04 ..> AUDLOG  : <<include>>
   @enduml
