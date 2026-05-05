Diagrama UML
~~~~~~~~~~~~

.. uml::

   @startuml

   class Aerolinea {
     - nombre : String
     - codigo : String
     - rutasAsociadas : Set<Ruta>
     + agregarRuta(r : Ruta)
     + removerRuta(r : Ruta)
     + obtenerRutas() : Set<Ruta>
   }

   class Ruta {
     - codigo : String
     - origen : String
     - destino : String
     - estado : EstadoRuta
     - aerolineasAsociadas : Set<Aerolinea>
     + obtenerDetalles() : String
     + actualizarEstado(e : EstadoRuta)
     + agregarAerolinea(a : Aerolinea)
     + removerAerolinea(a : Aerolinea)
   }

   enum EstadoRuta {
     ACTIVA
     SUSPENDIDA
     CANCELADA
   }

   Aerolinea "*" -- "*" Ruta : administra / pertenece
   Ruta -- EstadoRuta
   @enduml

**Elementos UML clave:**

- **Multiplicidad**: ``*..*`` — una aerolínea tiene
  varias rutas, una ruta puede pertenecer a varias
  aerolíneas.
- **Navegabilidad**: bidireccional — ambas clases son
  conscientes de la relación.
- **Roles**: ``administra`` (Aerolínea→Ruta) y
  ``pertenece`` (Ruta→Aerolínea).
