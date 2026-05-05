10.1 SecRules usa Funcion (UC_PERM_07)
--------------------------------------

.. uml::

   @startuml

   class SecRules {
     + verificarPermiso(usuario : Usuario, funcion : Funcion) : Boolean
   }
   class Usuario
   class Funcion

   SecRules ..> Usuario : <<usa>>
   SecRules ..> Funcion : <<usa>>
   note right of SecRules
     Dependencia: SecRules usa
     Usuario y Funcion como
     parámetros — no las contiene
     ni las hereda.
   end note
   @enduml
