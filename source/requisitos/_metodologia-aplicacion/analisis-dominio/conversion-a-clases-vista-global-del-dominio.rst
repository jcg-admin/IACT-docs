3.2 Conversión a clases (vista global del dominio)
--------------------------------------------------

.. uml::

   @startuml

   package "Acceso & RBAC" as MODULO_ACCESO_RBAC {
     class Usuario
     class Sesion
     class SegmentoDatos
     class Funcion
     class Grupo
     class PermisoExcepcional
   }

   package "Llamadas / IVR" as MODULO_LLAMADAS_IVR {
     class Llamada
     class Centro
     class Campana
     class Servicio
     class Region
   }

   package "Reportes / Métricas" as MODULO_REPORTES {
     class Reporte
     class Dashboard
     class Metrica
     class Filtro
   }

   package "Pipeline ETL" as MODULO_ETL {
     class EjecucionETL
     class ErrorETL
     class FilaCargada
     class Scheduler
   }

   package "Alertas / Notificaciones" as MODULO_ALERTAS {
     class Alerta
     class Umbral
     class Suscripcion
     class BuzonInterno
   }

   package "Auditoría" as MODULO_AUDITORIA {
     class EventoAuditoria
     class AuditoriaPermiso
     class AuditoriaAcceso
   }
   @enduml
