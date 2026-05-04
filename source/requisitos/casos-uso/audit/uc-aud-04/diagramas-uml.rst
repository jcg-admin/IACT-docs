.. _uc-aud-04-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "generate_compliance_report" as generate_compliance_report
 actor "ComplianceWorker" as Complianceworker
 actor "HMAC Signer" as HmacSigner
 actor "Mailbox" as Mailbox
 rectangle "MOD_Audit" {
   usecase "UC_AUD_04\nGenerar Reporte" as UC04
   usecase "Verify" as V
 }
 generate_compliance_report --> UC04
 generate_compliance_report --> V
 UC04 --> Complianceworker
 Complianceworker --> HmacSigner
 Complianceworker --> Mailbox
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
 rectangle "ReporteRaw" as ReporteRaw
 rectangle "Sanitize" as Sanitize
 rectangle "HashSha256" as HashSha256
 rectangle "HMACKMS" as HMACKMS
 rectangle "ReporteFirmado" as ReporteFirmado
 ReporteRaw --> Sanitize
 Sanitize --> HashSha256
 HashSha256 --> HMACKMS
 HMACKMS --> ReporteFirmado
 @enduml

8.4 Verify
==========

.. uml::

 @startuml
 actor "Verificador" as Verificador
 participant "VerifyEndpoint" as Verifyendpoint
 participant "Storage" as Storage
 participant "HMAC Verifier" as HmacVerifier
 Verificador -> Verifyendpoint: GET /verify/{job_id}
 Verifyendpoint -> Storage: descarga file
 Storage --> Verifyendpoint: file
 Verifyendpoint -> HmacVerifier: recompute hash + signature
 HmacVerifier --> Verifyendpoint: match? bool
 Verifyendpoint --> Verificador: result
 @enduml
