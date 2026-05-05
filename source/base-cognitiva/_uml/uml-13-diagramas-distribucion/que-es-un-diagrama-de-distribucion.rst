Qué es un diagrama de distribución
==================================

El elemento primordial del hardware es un **nodo**: un nombre
genérico para todo tipo de **recurso de cómputo**.

Existen dos tipos de nodos:

- **Procesador** — puede ejecutar un componente.
- **Dispositivo** — no lo ejecuta; tiene contacto de alguna
  forma con el mundo exterior (impresora, monitor, etc.).

En UML, un **cubo** representa a un nodo. Asigne un nombre y
puede utilizar un **estereotipo** para indicar el tipo de
recurso.

.. uml::

   @startuml

   node "ServidorWeb" <<procesador>> as SW
   node "Impresora"   <<dispositivo>> as P
   @enduml

Si el nodo es parte de un paquete, su nombre puede contener
también el del paquete.

Se puede dividir al cubo en compartimientos que agreguen
información (componentes colocados en el nodo):

.. uml::

   @startuml

   node "ServidorWeb" as SW {
     component "Apache"        as Ap
     component "PHP runtime"   as PHP
     component "App de cliente" as App
   }
   @enduml

Otra forma de indicar los componentes distribuidos es mostrarlos
en relaciones de **dependencia** con un nodo:

.. uml::

   @startuml

   node "ServidorWeb" as SW
   component "Apache"      as Ap
   component "PHP runtime" as PHP
   SW <.. Ap  : <<deploys>>
   SW <.. PHP : <<deploys>>
   @enduml

Una **línea** que asocie a dos cubos representa una **conexión**
entre ellos. No necesariamente un cable: también puede ser una
conexión inalámbrica (infrarroja, satelital, etc.).

Puede usar un **estereotipo** para dar información respecto a la
conexión:

.. uml::

   @startuml

   node "Cliente"    as C
   node "Servidor"   as S
   node "BD Server"  as BASE_DATOS
   node "Impresora"  as P

   C  -- S  : <<HTTPS>>
   S  -- BASE_DATOS : <<TCP/IP — JDBC>>
   C  -- P  : <<USB>>
   S  .. P  : <<inalambrica IR>>
   @enduml

La conexión es el tipo común de asociación entre dos nodos, pero
es posible utilizar otros (como **agregación** o **dependencia**)
y representarlos de las formas ya conocidas.
