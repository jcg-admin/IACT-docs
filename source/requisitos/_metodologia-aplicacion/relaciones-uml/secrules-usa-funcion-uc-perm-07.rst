10.1 SecRules usa Funcion (UC_PERM_07)
--------------------------------------

.. uml::

   @startuml

   class SecRules {
     + verifyPermission(user : User, function : Function) : Boolean
   }
   class User
   class Function

   SecRules ..> User : <<uses>>
   SecRules ..> Function : <<uses>>
   note right of SecRules
     Dependencia: SecRules usa
     User y Function como
     parámetros — no las contiene
     ni las hereda.
   end note
   @enduml
