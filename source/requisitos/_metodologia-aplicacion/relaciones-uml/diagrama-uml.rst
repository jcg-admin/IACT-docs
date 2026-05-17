Diagrama UML
~~~~~~~~~~~~

.. uml::

   @startuml

   class Airline {
     - name : String
     - code : String
     - associatedRoutes : Set<Route>
     + addRoute(r : Route)
     + removeRoute(r : Route)
     + getRoutes() : Set<Route>
   }

   class Route {
     - code : String
     - origin : String
     - destination : String
     - state : RouteState
     - associatedAirlines : Set<Airline>
     + getDetails() : String
     + updateState(s : RouteState)
     + addAirline(a : Airline)
     + removeAirline(a : Airline)
   }

   enum RouteState {
     ACTIVE
     SUSPENDED
     CANCELLED
   }

   Airline "*" -- "*" Route : administers / belongs
   Route -- RouteState
   @enduml

**Elementos UML clave:**

- **Multiplicidad**: ``*..*`` — una aerolínea tiene
  varias rutas, una ruta puede pertenecer a varias
  aerolíneas.
- **Navegabilidad**: bidireccional — ambas clases son
  conscientes de la relación.
- **Roles**: ``administra`` (Aerolínea→Ruta) y
  ``pertenece`` (Ruta→Aerolínea).
