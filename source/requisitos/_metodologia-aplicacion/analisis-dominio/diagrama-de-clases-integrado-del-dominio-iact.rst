7. Diagrama de clases integrado del dominio IACT
================================================

Vista global con relaciones (extracto cubriendo los seis
paquetes):

.. uml::

   @startuml

   class Usuario
   class Sesion
   class SegmentoDatos
   class Funcion
   class Grupo
   class Llamada
   class Reporte
   class Metrica
   class EjecucionETL
   class ErrorETL
   class Alerta
   class Umbral
   class BuzonInterno
   class EventoAuditoria

   ' RBAC
   Usuario "1" -- "0..1" Sesion           : posee
   Usuario "1" -- "1"   SegmentoDatos     : restringido_por
   Usuario "*" -- "*"   Grupo             : asignado_a
   Grupo   "*" -- "*"   Funcion           : contiene

   ' Llamadas → reportes
   Llamada "0..*" -- "1" SegmentoDatos    : pertenece_a
   Reporte "1"    -- "1..*" Metrica       : contiene
   Reporte "*"    -- "0..*" Llamada       : agrega

   ' Pipeline
   EjecucionETL "1" *-- "0..*" ErrorETL   : compone
   EjecucionETL "0..*" -- "1..*" Llamada  : carga

   ' Alertas
   Alerta "1" -- "1" Umbral               : usa
   Alerta "1" -- "0..*" Usuario           : suscriptos
   Alerta -- BuzonInterno                 : notifica_via

   ' Auditoría
   Usuario "1" -- "0..*" EventoAuditoria  : genera

   note bottom of EventoAuditoria
     CNST_025 — append-only,
     inmutable, sin delete().
   end note
   note right of BuzonInterno
     CNST_001 — sólo buzón
     interno, NO email.
   end note
   @enduml

----
