8.2 Diagrama de estado
======================

.. uml::

 @startuml
 [*] --> offline
 offline --> available : login
 available --> busy : llamada (auto)
 busy --> after_call_work : hangup (auto)
 after_call_work --> available : wrap-up done
 available --> break : manual
 break --> available : manual
 available --> training : manual
 training --> available : end
 available --> offline : logout
 break --> offline : logout
 training --> offline : logout
 after_call_work --> offline : logout
 @enduml

