.. _uc-alr-05-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "User" as User
 actor "subscribe_to_alert" as subscribe_to_alert
 rectangle "MOD_Alerts" {
   usecase "UC_ALR_05\nSubscriptions" as UC05
   usecase "Bulk add" as BA
   usecase "Mute global" as M
 }
 User --> UC05
 subscribe_to_alert --> UC05
 UC05 ..> BA : <<extend>>
 User --> M
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 start
 :POST sub;
 :JWT + RBAC (own o admin);
 :Validar type + scope;
 if (Cross-segmento?) then (si)
   :400; stop
 endif
 if (Duplicada?) then (si)
   :409; stop
 endif
 :INSERT;
 :Audit;
 :201;
 stop
 @enduml

8.3 Estado
==========

.. uml::

 @startuml
 [*] --> active : crear
 active --> paused : mute / segmento revoke
 paused --> active : unmute / segmento restore
 active --> [*] : delete
 @enduml

8.4 Clases
==========

.. uml::

 @startuml
 class Subscription
 class SubscriptionRepo
 class SegmentChangeListener
 SubscriptionRepo -- Subscription
 SegmentChangeListener -- SubscriptionRepo
 @enduml
