Profundización
--------------

Determinar cuáles son los casos de uso de alto nivel y a partir
de ellos, generar el modelo detallado.

Una actividad extremadamente importante en una firma de
consultoría es la **generación de propuestas**, así que
examinemos el caso de uso *"Crear una propuesta"*.

Las entrevistas con los consultores probablemente le indicarán
cuántos pasos se necesitan en este caso de uso. El actor inicial
es un consultor.

- El consultor tiene que **iniciar una sesión** en la LAN y ser
  **verificado** como usuario válido.
- Luego tendrá que utilizar algún software integrado para oficina
  (procesador de textos, hoja de cálculo y gráficos) para
  escribir la propuesta. En el proceso, el consultor podría
  volver a utilizar **porciones de propuestas previas**.
- La firma podría tener una directiva de que un funcionario
  corporativo y otros dos consultores **revisen** una propuesta
  antes de que llegue a manos del cliente. Por lo que el
  consultor almacena la propuesta en un área central accesible
  mediante la LAN, y envía a los correos electrónicos de los tres
  revisores un mensaje que indique que la propuesta se encuentra
  lista.
- Luego de recibir los comentarios y hacer las modificaciones
  necesarias, el consultor **imprime** la propuesta y la envía
  por correo al cliente.
- Cuando todo termina, el consultor **se retira** de la red.

Ciertos pasos se repetirán de un caso de uso a otro, y ello le
llevará a otros casos de uso (posiblemente incluidos):

- *Iniciar una sesión* y *ser verificado* son dos pasos que
  pueden incluir varios casos de uso → creará un caso de uso
  ``"Verificar usuario"`` que incluye ``"Crear una propuesta"``.
- Otro par de casos de uso son ``"Utilizar software de oficina"``
  y ``"Finalizar sesión de la red"``.

Posiblemente las propuestas sean distintas para clientes nuevos y
clientes constantes; en ese caso crearía
``"Crear una propuesta para un cliente nuevo"`` que **extiende**
a ``"Crear una propuesta"``.

.. uml::

   @startuml

   left to right direction
   actor Consultor
   actor "Funcionario\ncorporativo" as FC

   rectangle "LAN — Crear propuesta" {
     usecase "Crear una propuesta"                            as CU
     usecase "Crear una propuesta\npara un cliente nuevo"     as CUE
     usecase "Verificar usuario"                              as VU
     usecase "Utilizar software\nde oficina"                  as SO
     usecase "Finalizar sesión\nde la red"                    as FS
     usecase "Almacenar la propuesta"                         as AP
     usecase "Notificar revisores\n(correo)"                  as NR
     usecase "Imprimir y enviar\nal cliente"                  as IM
   }

   Consultor --> CU
   FC        --> NR

   CUE  ..|>  CU                : <<extend>>
   CU   ..>   VU                : <<include>>
   CU   ..>   SO                : <<include>>
   CU   ..>   AP                : <<include>>
   CU   ..>   NR                : <<include>>
   CU   ..>   IM                : <<include>>
   CU   ..>   FS                : <<include>>
   @enduml

Recuerde que **el análisis del caso de uso describe el
comportamiento de un sistema, nunca toca a la implementación**.

----
