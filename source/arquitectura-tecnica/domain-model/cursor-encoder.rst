.. meta::
 :artefacto: AT_DM_CLASS_CURSOR_ENCODER
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Audit
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_cursor_encoder:

=============
CursorEncoder
=============

Codifica y decodifica **cursores opacos** usados para
paginación cursor-based de los resultados de
``AuditQueryService``. Encapsula la representación interna
del cursor (incluye campos como ``last_event_id`` y
``last_occurred_at``) en un string opaco resistente a
manipulación por el cliente.

Los cursores son **stateless** del lado del servidor: toda
la información necesaria para retomar la paginación está en
el cursor mismo, firmado para detectar tampering.

.. uml::
 :caption: Clase CursorEncoder — codificación opaca de
           cursores de paginación cursor-based.

 @startuml

 class CursorEncoder {
   - signing_key : SecretKey
   - encoding_version : Integer
   --
   + encode(state : CursorState) : String
   + decode(cursor : String) : CursorState
   + is_valid(cursor : String) : Boolean
   - sign(payload : Bytes) : Bytes
   - verify_signature(payload : Bytes, signature : Bytes) : Boolean
 }

 class CursorState {
   + last_event_id : UUID
   + last_occurred_at : DateTime
   + filters_hash : String
   + page_size : Integer
   + version : Integer
 }

 class InvalidCursorError {
   + reason : InvalidReason
 }

 enum InvalidReason {
   MALFORMED
   SIGNATURE_MISMATCH
   VERSION_UNSUPPORTED
   EXPIRED
 }

 CursorEncoder "1" ..> "0..*" CursorState : encodes/decodes
 CursorEncoder "1" ..> "0..*" InvalidCursorError : throws
 InvalidCursorError "*" -- "1" InvalidReason

 note right of CursorEncoder
   Cursor = base64(payload + signature).
   Stateless, server-side no almacena.
   filters_hash detecta cambio de filtros
   entre paginas (forzar nuevo query).
 end note

 @enduml

Operaciones principales
=======================

- ``encode(state)`` — serializa ``CursorState`` a JSON,
  firma, codifica en base64 URL-safe.
- ``decode(cursor)`` — invierte el proceso. Verifica firma;
  si falla, lanza ``InvalidCursorError`` con ``reason``
  apropiada.
- ``is_valid(cursor)`` — verificación rápida sin
  reconstruir ``CursorState``; útil para early-reject.

Razones de invalidación (``InvalidReason``)
===========================================

- ``MALFORMED`` — el cursor no es base64 válido o el JSON
  interno está corrupto.
- ``SIGNATURE_MISMATCH`` — el cliente alteró el contenido
  del cursor.
- ``VERSION_UNSUPPORTED`` — cursor de una versión anterior
  del schema; el cliente debe iniciar nueva paginación.
- ``EXPIRED`` — el cursor tiene timestamp más antiguo que
  el TTL configurado (rara; útil contra replay).

Restricciones aplicables
========================

- **P-15** — cursores opacos previenen IDOR
  (Insecure Direct Object Reference).
- ``filters_hash`` se incluye para que cambiar filtros
  entre páginas obligue a un nuevo cursor (no se puede
  paginar resultados con filtros distintos).

Trazabilidad a UCs
==================

Usado en todo UC que pagina ``AuditEvent``:

- :doc:`/requisitos/casos-uso/audit/uc-aud-01/index`
- :doc:`/requisitos/casos-uso/audit/uc-aud-02/index`
- :doc:`/requisitos/casos-uso/permissions/uc-perm-10/index`

Relaciones
==========

- Componente interno de ``AuditQueryService``
  (composición fuerte).
- Codifica/decodifica instancias de ``CursorState``.
- Lanza ``InvalidCursorError`` ante manipulación.
