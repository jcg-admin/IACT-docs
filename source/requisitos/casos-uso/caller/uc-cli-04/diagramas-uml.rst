.. _uc-cli-04-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "Caller" as Caller
 actor "answer_inbound_calls" as answer_inbound_calls
 rectangle "MOD_Caller" {
   usecase "UC_CLI_04\nCallback" as UcCli04
   usecase "UC_OPR_03\nDial" as UcOpr03
 }
 Caller --> UcCli04
 UcCli04 --> answer_inbound_calls
 answer_inbound_calls --> UcOpr03
 UcOpr03 ..> UcCli04 : consume CallbackEntry
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 start
 :Ofrecer callback;
 if (Cliente acepta?) then (no)
   :Sigue cola;
   stop
 endif
 :Capturar numero;
 if (DNC?) then (si)
   :Mensaje rechazo;
   stop
 endif
 :Hash + INSERT CallbackEntry;
 :Audit;
 :Confirmar + hangup;
 stop
 @enduml

8.3 Estado
==========

.. uml::

 @startuml
 [*] --> pending
 pending --> in_progress : agente toma
 in_progress --> done : llamada exitosa
 in_progress --> expired : ventana cerro
 pending --> expired : sin tomar
 done --> [*]
 expired --> [*]
 @enduml

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
 IVR -> Callbackrepo: INSERT pending
 IVR -> Caller: confirma + hangup

 ... despues ...
 answer_inbound_calls -> Callbackrepo: take callback
 answer_inbound_calls -> Caller: dial (UC_OPR_03)
 @enduml
