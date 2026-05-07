.. _uc-aud-04-parte-08-diagrama-flujo-de-firma:

8.3 Diagrama de flujo de firma
================================

.. uml::
 :caption: UC_AUD_04 — pipeline de firmado del reporte.

 @startuml

 rectangle "Reporte raw\n(template aplicado)" as ReporteRaw
 rectangle "Sanitize\n(PII filter)" as Sanitize
 rectangle "Hash SHA-256" as HashSha256
 rectangle "HMAC-KMS\n(firma con clave gestionada)" as HMACKMS
 rectangle "Reporte firmado\ncon signature" as ReporteFirmado

 ReporteRaw --> Sanitize : remover PII
 Sanitize --> HashSha256 : calcular hash
 HashSha256 --> HMACKMS : firmar hash
 HMACKMS --> ReporteFirmado : adjuntar signature

 note bottom of HMACKMS
   La clave KMS esta protegida
   por hardware (HSM en
   produccion). Verificacion
   posterior reproduce el hash
   y valida la firma sin
   exponer la clave privada.
 end note

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`diagrama-de-secuencia-verify`.
 - :doc:`/arquitectura-tecnica/domain-model/hmac-verifier`.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service`.
