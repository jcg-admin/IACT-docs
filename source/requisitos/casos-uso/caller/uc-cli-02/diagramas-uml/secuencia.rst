8.4 Secuencia
=============

.. uml::

 @startuml
 actor "Caller" as Caller
 participant "IVR" as IVR
 participant "Telephony" as Telephony
 IVR -> Telephony: play prompt
 Telephony -> Caller: audio
 Caller -> Telephony: DTMF
 Telephony -> IVR: digit
 IVR -> IVR: navigate
 IVR -> Telephony: play next
 @enduml
