9. Agrupamiento con paquetes
============================

Los **paquetes** organizan UCs en grupos coherentes por
dominio funcional. En IACT, cada paquete corresponde a un
módulo del catálogo modular.

.. uml::

   @startuml

   left to right direction
   actor Operador
   actor Supervisor
   actor "Admin Acceso"   as AdminAcceso
   actor "Admin Pipeline" as AdminPipeline
   actor Auditor

   rectangle "IACT" {
     package "UC_AUTH (5 UCs)" {
       usecase "Iniciar sesión"  as A1
       usecase "Cerrar sesión"   as A2
     }

     package "UC_USR (4 UCs)" {
       usecase "CRUD usuarios" as U1
     }

     package "UC_ACC (9 UCs)" {
       usecase "Asignar funciones"   as AC1
       usecase "Gestionar SoD"       as AC5
     }

     package "UC_PERM (10 UCs)" {
       usecase "Verificar permiso"   as PE7
       usecase "Generar menú\ndinámico" as PE8
     }

     package "UC_RPT (14 UCs)" {
       usecase "Ver dashboard"       as R1
       usecase "Exportar reporte"    as R4
     }

     package "UC_ALR (5 UCs)" {
       usecase "Reconocer alerta"    as AL3
     }

     package "UC_PIP (4 UCs)" {
       usecase "Supervisar ETL"      as P1
       usecase "Solicitar reintento" as P4
     }

     package "UC_AUD (4 UCs)" {
       usecase "Consultar auditoría" as AU1
     }

     package "UC_LOG (7 UCs)" {
       usecase "Consultar logs"      as L1
     }
   }

   Operador   --> A1
   Operador   --> R1
   Supervisor --> R4
   Supervisor --> AL3
   AdminAcceso         --> AC1
   AdminAcceso         --> AC5
   AdminPipeline         --> P1
   AdminPipeline         --> P4
   Auditor    --> AU1
   @enduml

**Notación de ruta:** un UC dentro de un paquete se referencia
con ``Paquete::UC`` (ej: ``UC_RPT::Ver dashboard``).

----
