.. _uc-aud-04-parte-08-diagrama-secuencia-verify:

8.4 Diagrama de secuencia — Verificar reporte firmado
=======================================================

.. uml::
 :caption: UC_AUD_04 — flujo de verificacion de un reporte.

 @startuml

 actor "verify_audit_report" as verify_audit_report
 participant "Servicio de Aplicacion" as SvcAplicacion
 participant "Storage" as Storage
 participant "HmacVerifier" as HmacVerifier

 verify_audit_report -> SvcAplicacion: GET /api/v1/audit/reports/{job_id}/verify/
 SvcAplicacion -> Storage: descargar archivo + signature
 Storage --> SvcAplicacion: file + signature

 SvcAplicacion -> HmacVerifier: recompute hash + verify signature
 HmacVerifier --> SvcAplicacion: { match: bool, hash }

 alt verificado
   SvcAplicacion --> verify_audit_report: 200 { verified: true, hash }
 else hash mismatch
   SvcAplicacion --> verify_audit_report: 200 { verified: false, reason }
 end

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`diagrama-de-flujo-de-firma`.
