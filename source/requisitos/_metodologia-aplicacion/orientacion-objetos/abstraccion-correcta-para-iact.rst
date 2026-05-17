2.2 Abstracción correcta para IACT
----------------------------------

.. uml::

   @startuml

   class Call {
     - id : Integer
     - center_id : Integer
     - campaign_id : Integer
     - service_id : Integer
     - type : Enum
     - duration_sec : Integer
     - wait_time_sec : Integer
     - outcome : Enum
     - date : DateTime
     + getDuration() : Integer
     + getType() : Enum
     + isAbandoned() : Boolean
   }
   note right of Call
     Abstracción para analytics:
     sólo atributos relevantes para
     calcular métricas (BR_016 tasa
     de abandono, BR_017 tiempo
     promedio de espera, BR_018
     índice de eficiencia).
   end note
   @enduml
