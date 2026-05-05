Subestados secuenciales
-----------------------

Los subestados secuenciales **suceden uno detrás de otro**.

Dentro del estado *Operación* de la GUI, tendrá la siguiente
secuencia:

- *A la espera de acción del usuario*
- *Registro de una acción del usuario*
- *Representación de la acción del usuario*

La acción del usuario desencadena la transición a partir de
*A la espera* hacia *Registro*. Las actividades dentro del
*Registro* trascienden hacia *Representación*. Después del
tercer estado, la GUI vuelve a iniciar *A la espera*.

.. uml::

   @startuml

   state Operacion {
     [*] --> Espera
     Espera : "A la espera de\nacción del usuario"
     Espera --> Registro : accionUsuario
     Registro : "Registro de una\nacción del usuario"
     Registro --> Representacion
     Representacion : "Representación de la\nacción del usuario"
     Representacion --> Espera
   }
   @enduml
