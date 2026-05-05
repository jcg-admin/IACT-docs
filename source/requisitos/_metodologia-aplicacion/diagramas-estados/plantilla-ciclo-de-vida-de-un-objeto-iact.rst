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

   state "AbortadoFlowFinal" as ETL_ABORTADO #FFAAAA
   EstadoInicial --> ETL_ABORTADO : error
   EstadoCasoA --> ETL_ABORTADO : error
   EstadoCasoB --> ETL_ABORTADO : error
   ETL_ABORTADO : entry / registrar abort en audit_log
   ETL_ABORTADO --> [*]

   Final --> [*]
   @enduml
