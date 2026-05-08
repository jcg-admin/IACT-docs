8.4 Secuencia
=============

.. uml::

 @startuml
 actor "Caller" as Caller
 participant "Queue" as Queue
 participant "Router" as Router
 actor "answer_inbound_calls" as answer_inbound_calls
 Caller -> Queue: enter
 Queue -> Router: notify
 Router -> answer_inbound_calls: offer
 answer_inbound_calls -> Router: answer
 Router -> Queue: dequeue
 Queue -> Caller: bridge
 @enduml
