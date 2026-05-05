Asociaciones calificadas
========================

En una asociación de uno a muchos, cuando un objeto de una clase
tiene que seleccionar un objeto particular de otro tipo para
cumplir con un papel en la asociación, la primera clase deberá
atenerse a un atributo en particular para localizar al objeto
adecuado. Dicho atributo es un **identificador** — puede ser un
número de identidad. Esa información se conoce como
**calificador**.

Un calificador es una asociación que **resuelve el problema de
la búsqueda de uno a muchos a uno a uno**. El símbolo en UML es
un **pequeño rectángulo** adjunto a la clase que hará la
búsqueda.

Ejemplo: una recepcionista puede obtener una sola reservación
gracias al número de confirmación de dicha reservación.

La idea es **reducir, con eficiencia, la multiplicidad de uno a
muchos a una multiplicidad de uno a uno**.

.. uml::

   @startuml

   class Recepcionista
   class Reservacion
   Recepcionista "1" -[#black]- "(numeroConfirmacion)" Reservacion : busca
   note right of Reservacion
     Multiplicidad efectiva
     reducida a 1:1 mediante
     el calificador
     numeroConfirmacion.
   end note
   @enduml
