7.1 Asociaciones canónicas IACT
-------------------------------

.. uml::

   @startuml

   class Usuario
   class Sesion
   class Grupo
   class Funcion
   class SegmentoDatos
   class Reporte
   class Alerta

   Usuario "1" -- "0..1" Sesion          : posee
   Usuario "1" -- "1"   SegmentoDatos    : restringido_por
   Usuario "*" -- "*"   Grupo            : asignado_a
   Grupo   "*" -- "*"   Funcion          : contiene
   Usuario "1" -- "0..*" Reporte         : consulta
   Usuario "1" -- "0..*" Alerta          : suscrito_a

   note right of Usuario
     - Usuario posee 0..1 Sesion          (CNST_002)
     - Usuario tiene 1 segmento           (BR_012)
     - Usuario en 0..* grupos             (UC_PERM_01)
     - Grupo contiene 0..* funciones      (UC_PERM_06)
     - Usuario consulta 0..* reportes     (UC_RPT)
     - Usuario suscrito a 0..* alertas    (UC_ALR_05)
   end note
   @enduml
