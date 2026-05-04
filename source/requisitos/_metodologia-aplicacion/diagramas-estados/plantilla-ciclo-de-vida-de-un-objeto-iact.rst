13.11 Plantilla — ciclo de vida de un objeto IACT
-------------------------------------------------

.. uml::

   @startuml
   title Ciclo de vida — <Objeto IACT>

   [*] --> EstadoInicial : crear

   EstadoInicial : entry / inicializar
   EstadoInicial : do / esperar evento

   state c <<choice>>

   EstadoInicial --> c : evento_decision

   c --> EstadoCasoA : [cond_a]
   c --> EstadoCasoB : [cond_b]
   c --> [*] : [else]

   EstadoCasoA --> Final : completar
   EstadoCasoB --> Final : completar

   state "AbortadoFlowFinal" as ABT #FFAAAA
   EstadoInicial --> ABT : error
   EstadoCasoA --> ABT : error
   EstadoCasoB --> ABT : error
   ABT : entry / registrar abort en audit_log
   ABT --> [*]

   Final --> [*]
   @enduml
