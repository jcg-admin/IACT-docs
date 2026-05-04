4.1 ``calcularValor()`` polimórfico en métricas IACT
----------------------------------------------------

.. uml::

   @startuml

   abstract class Metrica {
     - nombre : String
     - segmento : SegmentoDatos
     + calcularValor(periodo : Rango) : Decimal
   }

   class TasaAbandono {
     + calcularValor(periodo : Rango) : Decimal
   }

   class TiempoPromedioEspera {
     + calcularValor(periodo : Rango) : Decimal
   }

   class IndiceEficiencia {
     - peso_atendidas : Decimal
     - peso_tiempo : Decimal
     + calcularValor(periodo : Rango) : Decimal
   }

   Metrica <|-- TasaAbandono
   Metrica <|-- TiempoPromedioEspera
   Metrica <|-- IndiceEficiencia

   note right of Metrica
     Polimorfismo (BR_016, BR_017, BR_018):
       TasaAbandono           → abandonadas / total × 100
       TiempoPromedioEspera   → SUM(esperas) / N
       IndiceEficiencia       → fórmula compuesta
                                ponderada por servicio
   end note
   @enduml
