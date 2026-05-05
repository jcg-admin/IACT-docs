8.4 Diagrama de estados — User.first_login
==========================================

.. uml::
 :caption: Estado first_login del User

 @startuml

 [*] --> first_login_true : UC_USR_01\n(creacion)

 first_login_true --> first_login_true : UC_AUTH_03\n(reset por admin)
 first_login_true --> first_login_false : UC_AUTH_04\n(cambio voluntario\npost first login)

 first_login_false --> first_login_true : UC_AUTH_03\n(reset)

 note right of first_login_true
   UC_AUTH_01 detecta first_login=true
   y dispara FA-01 → forzar UC_AUTH_04
 end note

 @enduml
