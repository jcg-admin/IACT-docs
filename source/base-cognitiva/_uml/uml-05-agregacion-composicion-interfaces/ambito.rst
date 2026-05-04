Ámbito
======

Existen dos tipos de ámbito: el de **instancia** y el de
**archivador**.

.. list-table::
 :widths: 20 40 40
 :header-rows: 1

 * -
   - Ámbito de Instancia
   - Ámbito de Archivador
 * - **Definición**
   - Cada instancia de una clase tiene su propio conjunto de
     valores para los atributos y operaciones. Los valores
     pueden diferir de una instancia a otra.
   - Sólo habrá un único valor para el atributo u operación,
     compartido por todas las instancias de la clase. Cualquier
     cambio se reflejará en todas las instancias.
 * - **Uso**
   - Cuando es necesario que un grupo específico de instancias
     comparta valores exactos de un atributo privado, pero cada
     instancia tiene su propia representación y estado.
   - Cuando se necesita que un atributo u operación tenga un
     único valor compartido. Frecuente para configuraciones,
     constantes o recursos compartidos.
 * - **Ejemplo**
   - Si tienes una clase ``Coche``, cada objeto (``coche1``,
     ``coche2``...) tendrá su propio valor para atributos como
     ``color`` o ``marca``.
   - Si tienes una clase ``Configuracion``, un atributo como
     ``_version`` podría ser común para todas las instancias.

.. note::

 - **Instancia:** cada instancia cuenta con su propio valor en
   un atributo u operación. Es lo más común.
 - **Archivador:** sólo hay un valor del atributo u operación en
   todas las instancias (subrayado en el diagrama).

.. uml::

   @startuml

   class Coche {
     - color : String
     - marca : String
     {static} - cantidadFabricados : Integer
     --
     + arrancar()
     {static} + obtenerTotalFabricados() : Integer
   }
   note right of Coche
     ``color`` y ``marca`` son
     ámbito de **instancia**
     (uno por objeto).

     ``cantidadFabricados`` es
     ámbito de **archivador**
     (compartido por todos —
     subrayado en el diagrama).
   end note
   @enduml

----
