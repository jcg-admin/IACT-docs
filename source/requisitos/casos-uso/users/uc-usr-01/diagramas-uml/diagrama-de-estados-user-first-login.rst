8.4 Diagrama de estados — User.first_login
==========================================

.. uml::
 :caption: Estados first_login del nuevo User

 @startuml

 [*] --> first_login_true : UC_USR_01 (creacion)

 first_login_true --> first_login_true : UC_AUTH_03\n(admin reset)
 first_login_true --> first_login_false : UC_AUTH_04\n(cambio post first login)

 first_login_false --> first_login_true : UC_AUTH_03

 note right of first_login_true
   UC_AUTH_01 detecta first_login=true
   y dispara FA-01 → forzar UC_AUTH_04
 end note

 @enduml
