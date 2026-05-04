.. _uc-cli-02-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "Caller" as Caller
 rectangle "MOD_Caller" {
   usecase "UC_CLI_02\nNavegar IVR" as UC
   usecase "UC_CLI_03\nEsperar cola" as Q
   usecase "UC_CLI_04\nCallback" as CB
 }
 Caller --> UC
 UC ..> Q : <<extend>>
 UC ..> CB : <<extend>>
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 start
 :Cargar IVR;
 :Reproducir nodo;
 repeat
   :Esperar input;
   if (Input recibido?) then (si)
     if (Opcion valida?) then (si)
       :Avanzar a hijo;
     else (no)
       :Re-prompt;
     endif
   else (timeout)
     :Re-prompt o fallback;
   endif
 repeat while (no llego a salida)
 :Ejecutar accion;
 stop
 @enduml

8.3 Tree
========

.. uml::

 @startuml
 (Entry) -> (Opcion 1)
 (Entry) -> (Opcion 2)
 (Entry) -> (Opcion 0 hablar agente)
 (Opcion 1) -> (Submenu)
 @enduml

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
