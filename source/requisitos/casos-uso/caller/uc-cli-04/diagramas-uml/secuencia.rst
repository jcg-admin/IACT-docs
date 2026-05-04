8.4 Secuencia
=============

.. uml::

 @startuml
 actor "Caller" as Caller
 participant "IVR" as IVR
 database "CallbackRepo" as Callbackrepo
 actor "answer_inbound_calls" as answer_inbound_calls
 IVR -> Caller: oferta callback
 Caller -> IVR: acepta + numero
 IVR -> Callbackrepo: registrar pending
 IVR -> Caller: confirma + hangup

 ... despues ...
 answer_inbound_calls -> Callbackrepo: take callback
 answer_inbound_calls -> Caller: dial (UC_OPR_03)
 @enduml
