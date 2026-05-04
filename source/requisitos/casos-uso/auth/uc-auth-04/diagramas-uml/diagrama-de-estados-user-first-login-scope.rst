8.4 Diagrama de estados — User.first_login + scope
==================================================

.. uml::
 :caption: Transiciones de scope post UC_AUTH_04

 @startuml

 state "Sesion scope reducido" as REDUCED
 state "Sesion scope pleno" as FULL

 [*] --> REDUCED : UC_AUTH_01 + FA-01\n(first_login=true)

 REDUCED --> FULL : UC_AUTH_04 OK\n(first_login=false)

 FULL --> FULL : UC_AUTH_04 voluntario

 FULL --> REDUCED : UC_AUTH_03\n(admin reset)\nuser proximo login

 @enduml
