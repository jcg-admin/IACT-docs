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
       usecase "Iniciar sesión"  as INICIAR_SESION
       usecase "Cerrar sesión"   as CERRAR_SESION
     }

     package "UC_USR (4 UCs)" {
       usecase "CRUD usuarios" as CRUD_USUARIOS
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
       usecase "Ver dashboard"       as VER_DASHBOARD_IVR
       usecase "Exportar reporte"    as EJECUTAR_PROCEDIMIENTO_RPT
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
       usecase "Consultar logs"      as CONSULTAR_LOGS
     }
   }

   Operador   --> INICIAR_SESION
   Operador   --> VER_DASHBOARD_IVR
   Supervisor --> EJECUTAR_PROCEDIMIENTO_RPT
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
