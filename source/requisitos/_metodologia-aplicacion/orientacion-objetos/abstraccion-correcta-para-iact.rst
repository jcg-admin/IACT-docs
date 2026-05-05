2.2 Abstracción correcta para IACT
----------------------------------

.. uml::

   @startuml

   class Llamada {
     - id : Integer
     - centro_id : Integer
     - campana_id : Integer
     - servicio_id : Integer
     - tipo : Enum
     - duracion_seg : Integer
     - tiempo_espera_seg : Integer
     - resultado : Enum
     - fecha : DateTime
     + getDuracion() : Integer
     + getTipo() : Enum
     + esAbandonada() : Boolean
   }
   note right of Llamada
     Abstracción para analytics:
     sólo atributos relevantes para
     calcular métricas (BR_016 tasa
     de abandono, BR_017 tiempo
     promedio de espera, BR_018
     índice de eficiencia).
   end note
   @enduml
