Caso de uso "Recolectar el dinero"
----------------------------------

El recolector inicia debido también a que ha pasado **cierto
tiempo**. La persona deberá seguir la misma secuencia que en
*"Reabastecer"* para abrir la máquina. El recolector sacará el
dinero de la máquina y seguirá los pasos de *"Reabastecer"* para
cerrar y poner el seguro a la máquina.

- **Condición previa:** el paso del intervalo.
- **Resultado:** el dinero en las manos del recolector.

.. uml::

   @startuml

   left to right direction
   actor Cliente
   actor Proveedor
   actor Recolector
   actor Tiempo as T

   rectangle "Máquina de Gaseosas" {
     usecase "Comprar gaseosa"      as UC1
     usecase "Reabastecer"          as UC2
     usecase "Recolectar el dinero" as UC3
   }
   Cliente     --> UC1
   Proveedor   --> UC2
   Recolector  --> UC3
   T           --> UC2
   T           --> UC3
   @enduml

Cuando **derivamos un caso de uso**, no nos preocupamos por la
forma de implementarlo. No nos interesamos en los aspectos
internos de la máquina de gaseosa, tampoco por la forma en que
funcione el mecanismo de refrigeración, o por la forma en que la
máquina controle la cantidad de dinero. **Intentamos ver la
forma** en que la máquina lucirá para alguien que tenga que
utilizarla.

El objetivo es **derivar una colección de casos de uso** que,
finalmente, mostraremos a las *personas que diseñen la máquina*
y a las *personas que la construirán*.

Nuestros casos de uso reflejan lo que los clientes, recolectores
y proveedores desean, por lo que el resultado será una máquina
que **todos esos grupos** puedan utilizar con facilidad.

----
