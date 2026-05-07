.. meta::
 :artefacto: AT_DM_CLASS_HMAC_VERIFIER
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Audit
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-07
 :ultimo_cambio: 2026-05-07
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_hmac_verifier:

============
HmacVerifier
============

Verificador HMAC para integridad de exportes de audit reports
y de cadenas de audit log (chain hashing). Recomputa el hash
sobre el contenido descargado y lo compara con la signature
adjunta — si difieren, el report ha sido alterado en transito
o en almacenamiento.

Es invocado por el ``Servicio de Aplicacion`` cuando un user
con codename ``view_audit`` solicita ``verify_audit_report``
sobre un report previamente exportado.

.. uml::
 :caption: HmacVerifier — recomputo y comparacion HMAC.

 @startuml

 class HmacVerifier {
   - signing_key_ref : SecretKey
   --
   + verify(content : bytes, signature : bytes) : VerifyResult
   + verify_chain(from_id : UUID, to_id : UUID) : ChainVerifyResult
   + recompute(content : bytes) : Hash
 }

 class VerifyResult {
   + match : Boolean
   + hash : Hash
   + reason : String
 }

 class ChainVerifyResult {
   + chain_intact : Boolean
   + broken_at : UUID
 }

 HmacVerifier ..> VerifyResult : returns
 HmacVerifier ..> ChainVerifyResult : returns

 @enduml

Operaciones principales
=======================

- ``verify(content, signature)`` — recompute HMAC sobre
  ``content`` con la ``signing_key_ref`` (referencia a la
  clave gestionada por vault) y compara con ``signature``.
  Devuelve ``match: true/false`` + el hash recomputado.
- ``verify_chain(from_id, to_id)`` — verifica integridad de
  la cadena de hashes de ``AuditEvent`` entre dos ids.
- ``recompute(content)`` — solo computa el hash, sin
  comparar.

Restricciones aplicables
========================

- **CNST-025** — los exportes de audit deben ser firmados
  con HMAC al momento de generacion; este verificador es la
  contraparte que valida.
- **CNST-026** — la cadena de hashes de ``AuditEvent`` es
  inmutable; ``verify_chain`` la audita.

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/audit/uc-aud-04/index` —
  verificacion de export firmado.

Relaciones
==========

- Es invocado por el ``Servicio de Aplicacion`` durante el
  endpoint ``GET /api/v1/audit/reports/{job_id}/verify/``.
- No persiste estado; la ``signing_key_ref`` viene de
  configuracion de runtime.

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/audit-event`
 - :doc:`/arquitectura-tecnica/domain-model/audit-service`
