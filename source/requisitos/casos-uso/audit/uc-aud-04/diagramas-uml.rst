.. _uc-aud-04-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "Compliance Officer" as O
 actor "ComplianceWorker" as W
 actor "HMAC Signer" as H
 actor "Mailbox" as MB
 rectangle "MOD_Audit" {
   usecase "UC_AUD_04\nGenerar Reporte" as UC04
   usecase "Verify" as V
 }
 O --> UC04
 O --> V
 UC04 --> W
 W --> H
 W --> MB
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 start
 :POST template + period;
 :JWT + RBAC;
 :Validar;
 :Encolar Worker;
 :Audit QUEUED;
 :202;

 ... background ...

 :Re-check permiso;
 :Ejecutar template queries;
 :Sanitize;
 :Firmar HMAC;
 :Upload storage + URL;
 :Audit GENERATED + hash;
 :Mailbox notify;
 stop
 @enduml

8.3 Flujo de firma
==================

.. uml::

 @startuml
 component "Reporte raw" as R
 component "Sanitize" as S
 component "Hash sha256" as H
 component "HMAC con KMS key" as M
 component "Reporte firmado" as F
 R --> S
 S --> H
 H --> M
 M --> F
 @enduml

8.4 Verify
==========

.. uml::

 @startuml
 actor "Verificador" as V
 participant "VerifyEndpoint" as E
 participant "Storage" as ST
 participant "HMAC Verifier" as H
 V -> E: GET /verify/{job_id}
 E -> ST: descarga file
 ST --> E: file
 E -> H: recompute hash + signature
 H --> E: match? bool
 E --> V: result
 @enduml
