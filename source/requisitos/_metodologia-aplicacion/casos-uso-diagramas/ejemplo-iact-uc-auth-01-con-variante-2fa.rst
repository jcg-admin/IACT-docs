7.1 Ejemplo IACT — UC_AUTH_01 con variante 2FA
----------------------------------------------

.. uml::

   @startuml

   left to right direction
   actor Usuario

   rectangle "IACT" {
     usecase "UC_AUTH_01\nIniciar sesión\n(BASE)"       as A1
     usecase "UC_AUTH_01b\nIniciar sesión\ncon 2FA"     as A1B
   }

   Usuario --> A1
   Usuario --> A1B

   A1B --|> A1

   note right of A1B
     UC_AUTH_01b HEREDA de UC_AUTH_01:
       + paso adicional de verificación
         del segundo factor (TOTP / SMS
         interno) tras validar password.
     Sólo aplica a usuarios con 2FA
     habilitado en su cuenta.
   end note
   @enduml
