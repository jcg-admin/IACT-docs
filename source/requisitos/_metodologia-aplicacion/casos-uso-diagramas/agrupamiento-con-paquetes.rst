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
       usecase "Asignar funciones"   as ASIGNAR_FUNCIONES_A_USUARIO
       usecase "Gestionar separacion de deberes"       as GESTIONAR_REGLAS_SEPARACION
     }

     package "UC_PERM (10 UCs)" {
       usecase "Verificar permiso"   as VERIFICAR_PERMISO
       usecase "Generar menú\ndinámico" as GENERAR_MENU_DINAMICO
     }

     package "UC_RPT (14 UCs)" {
       usecase "Ver dashboard"       as VER_DASHBOARD_IVR
       usecase "Exportar reporte"    as EJECUTAR_PROCEDIMIENTO_RPT
     }

     package "UC_ALR (5 UCs)" {
       usecase "Reconocer alerta"    as RECONOCER_ALERTA
     }

     package "UC_PIP (4 UCs)" {
       usecase "Supervisar ETL"      as PASO_AUTENTICACION
       usecase "Solicitar reintento" as GESTION_PIPELINE_ETL
     }

     package "UC_AUD (4 UCs)" {
       usecase "Consultar auditoría" as CONSULTAR_AUDITORIA
     }

     package "UC_LOG (7 UCs)" {
       usecase "Consultar logs"      as CONSULTAR_LOGS
     }
   }

   Operador   --> INICIAR_SESION
   Operador   --> VER_DASHBOARD_IVR
   Supervisor --> EJECUTAR_PROCEDIMIENTO_RPT
   Supervisor --> RECONOCER_ALERTA
   AdminAcceso         --> ASIGNAR_FUNCIONES_A_USUARIO
   AdminAcceso         --> GESTIONAR_REGLAS_SEPARACION
   AdminPipeline         --> PASO_AUTENTICACION
   AdminPipeline         --> GESTION_PIPELINE_ETL
   Auditor    --> CONSULTAR_AUDITORIA
   @enduml

**Notación de ruta:** un UC dentro de un paquete se referencia
con ``Paquete::UC`` (ej: ``UC_RPT::Ver dashboard``).
