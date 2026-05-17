8.3 Estado
==========

.. uml::

 @startuml
 [*] --> dialing
 dialing --> ringing
 ringing --> bridged : pickup
 ringing --> failed : no_answer|busy
 bridged --> ended : hangup
 failed --> [*]
 ended --> [*]
 @enduml

