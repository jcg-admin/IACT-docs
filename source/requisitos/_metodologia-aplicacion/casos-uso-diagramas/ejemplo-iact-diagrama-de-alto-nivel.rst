4. Ejemplo IACT — diagrama de alto nivel
========================================

Diagrama del **sistema completo IACT** mostrando los UCs
operativos clave por dominio funcional, con sus actores
internos y externos.

.. uml::

   @startuml

   left to right direction

   actor Operador
   actor Supervisor
   actor "Admin\nAcceso"     as Admin
   actor "Admin\nPipeline"   as Admin
   actor Auditor
   actor "Sistema /\nScheduler" as Sched
   actor "IVR\nConmutador"  as SISTEMA_IVR

   rectangle "IACT" {
     usecase "UC_AUTH_01\nIniciar sesión"     as AUTH01
     usecase "UC_RPT_01\nVer dashboard"       as RPT01
     usecase "UC_RPT_04\nExportar reporte"    as RPT04
     usecase "UC_ALR_03\nReconocer alerta"    as ALR03
     usecase "UC_ACC_01\nAsignar funciones"   as UC_ACC_01
     usecase "UC_PERM_07\nVerificar permiso"  as PERM07
     usecase "UC_PIP_01\nSupervisar ETL"      as PIP01
     usecase "UC_PIP_04\nSolicitar reintento" as PIP04
     usecase "UC_AUD_01\nConsultar auditoría" as AUD01
     usecase "UC_AUD_03\nExportar auditoría"  as AUD03
     usecase "Carga ETL\nnocturna"            as SERVICIO_ETL
   }

   Operador   --> AUTH01
   Operador   --> RPT01
   Operador   --> RPT04
   Operador   --> ALR03

   Supervisor --> AUTH01
   Supervisor --> RPT04
   Supervisor --> ALR03

   Admin         --> UC_ACC_01
   Admin         --> PIP01
   Admin         --> PIP04
   Auditor    --> AUD01
   Auditor    --> AUD03

   Sched      --> SERVICIO_ETL
   SISTEMA_IVR        <-- SERVICIO_ETL

   RPT01      ..> PERM07 : <<include>>
   RPT04      ..> PERM07 : <<include>>
   UC_ACC_01      ..> PERM07 : <<include>>
   AUD01      ..> PERM07 : <<include>>
   PIP04      ..> PERM07 : <<include>>
   @enduml

**Lectura del diagrama:**

- Cinco actores **operativos** (Operador, Supervisor,
  AdminAcceso, AdminPipeline, Auditor) inician UCs
  específicos según su rol.
- Dos actores **sistema/externos** (Scheduler y IVR
  Conmutador) participan en la carga ETL.
- ``UC_PERM_07`` (verificar permiso) es **incluido por
  todos** los UCs operativos — es el equivalente IACT a
  *"abrir la máquina"* del ejemplo del libro.
