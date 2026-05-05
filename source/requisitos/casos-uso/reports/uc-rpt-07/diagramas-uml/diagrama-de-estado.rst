8.4 Diagrama de estado
======================

.. uml::
 :caption: ScheduledReport

 @startuml
 [*] --> active : crear
 active --> paused : eliminar pause
 paused --> active : resume
 active --> auto_paused : 3 fallos
 auto_paused --> active : User fix
 active --> [*] : eliminar paused --> [*] : eliminar auto_paused --> [*] : DELETE
 @enduml
