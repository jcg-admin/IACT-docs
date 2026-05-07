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
