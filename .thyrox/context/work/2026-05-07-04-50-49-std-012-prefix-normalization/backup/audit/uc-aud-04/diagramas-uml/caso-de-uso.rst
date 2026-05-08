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
   usecase "UC_AUD_04\nGenerar Reporte" as UC_AUD_04
   usecase "Verify" as Verify
 }
 generate_compliance_report --> UC_AUD_04
 generate_compliance_report --> Verify
 UC_AUD_04 --> Complianceworker
 Complianceworker --> HmacSigner
 Complianceworker --> Mailbox
 @enduml

