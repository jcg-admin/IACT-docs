8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_OPR_07 — actores y casos asociados

 @startuml

 left to right direction

 actor "request_break" as INVOKER
 actor "Action" as POLICY <<sistema>>
 actor "Session" as SESSION <<sistema>>
 actor "TimingCalculator" as TC <<sistema>>

 rectangle "MOD_Operator" {
   usecase "UC_OPR_07\nSolicitar Break / Pausa" as UC_OPR_07
   usecase "Validar break_type\n(coffee | lunch | bathroom |\ntraining | meeting)" as VALIDAR_TYPE
   usecase "Validar quota\n(policy)" as VALIDAR_QUOTA
   usecase "Transicion estado\na break" as TRANSICIONAR
   usecase "Iniciar tracker\nde duracion" as TRACK
 }

 INVOKER --> UC_OPR_07
 UC_OPR_07 ..> VALIDAR_TYPE : <<include>>
 UC_OPR_07 ..> VALIDAR_QUOTA : <<include>>
 UC_OPR_07 ..> TRANSICIONAR : <<include>>
 UC_OPR_07 ..> TRACK : <<include>>

 VALIDAR_TYPE --> POLICY
 VALIDAR_QUOTA --> POLICY
 TRANSICIONAR --> SESSION
 TRACK --> TC

 note bottom of VALIDAR_QUOTA
   Cada tipo tiene quota diaria
   (coffee 15min × N, lunch 60min × 1,
   bathroom 5min × M). Exceeder dispara
   alerta operativa al supervisor.
 end note

 note right of POLICY
   Action entity: configurable
   por team / segmento. Definido
   en MOD_Admin (out of scope
   para operator).
 end note

 @enduml

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/action` —
   catalogo de break types + quota policy.
 - :doc:`/arquitectura-tecnica/domain-model/session` —
   Session con state=break + break_type.
 - :doc:`/arquitectura-tecnica/domain-model/timing-calculator` —
   tracker de duracion del break.
