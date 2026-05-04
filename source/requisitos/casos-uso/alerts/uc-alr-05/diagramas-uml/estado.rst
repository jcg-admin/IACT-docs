8.3 Estado
==========

.. uml::

 @startuml
 [*] --> active : crear
 active --> paused : mute / segmento revoke
 paused --> active : unmute / segmento restore
 active --> [*] : delete
 @enduml

