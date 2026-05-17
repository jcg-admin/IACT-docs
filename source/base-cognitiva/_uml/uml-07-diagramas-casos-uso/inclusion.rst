Inclusión
---------

En los casos de uso *"Reabastecer"* y*"Recolectar dinero"*,
ambos se inician mediante la apertura de la máquina y finalizan
con el cierre y sellado de la misma. El caso de uso *"Exhibir el
interior"* se creó para capturar el primer par de pasos, y
*"Cubrir el interior"* para el segundo. Tanto*"Reabastecer"*
como *"Recolectar dinero"* incluyen este par de casos de uso.

Para representar la inclusión utilizará el símbolo que usó para
la dependencia entre clases: una **línea discontinua con una
punta de flecha** que conecta los casos de uso apuntando hacia
el caso de uso dependiente; sobre la línea agregará un
estereotipo: la palabra ``<<incluir>>`` (o ``<<include>>``)
bordeada por dos pares de paréntesis angulares.

.. uml::

   @startuml

   left to right direction
   actor Proveedor
   actor Recolector

   rectangle "Máquina de Gaseosas" {
     usecase "Reabastecer"          as UC2
     usecase "Recolectar el dinero" as UC3
     usecase "Exhibir el interior"  as UCIN
     usecase "Cubrir el interior"   as UCOUT
   }
   Proveedor  --> UC2
   Recolector --> UC3
   UC2 ..> UCIN  : <<include>>
   UC2 ..> UCOUT : <<include>>
   UC3 ..> UCIN  : <<include>>
   UC3 ..> UCOUT : <<include>>
   @enduml

Un caso de uso incluido **nunca aparecerá solo**: funciona como
parte de un caso de uso que lo incluya. El primer paso en el
caso de uso *"Reabastecer"* podría ser ``«incluir» (Exhibir el
interior)``.
