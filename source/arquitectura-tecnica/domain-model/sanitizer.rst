.. meta::
 :artefacto: AT_DM_CLASS_SANITIZER
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

.. _dm_class_sanitizer:

=========
Sanitizer
=========

Componente que **transforma el payload** de un ``AuditEvent``
para llevarlo a una forma canónica y segura antes de
persistir. Aplica dos transformaciones:

1. **Tokenización de PII** según el ``ScanReport`` producido
   por ``PIIScanner``: sustituye valores en claro por tokens
   (reversibles o no).
2. **Truncado y normalización** de campos opcionales:
   ``user_agent``, mensajes largos, payloads de
   debugging — limita tamaño máximo y normaliza encoding.

Es un componente puro (sin estado persistido). Cada llamada
recibe el payload original más el reporte de PII y devuelve
el payload sanitizado.

.. uml::
 :caption: Clase Sanitizer — transformación de payload
           para forma canónica y segura.

 @startuml

 class Sanitizer {
   - max_string_length : Integer
   - max_array_length : Integer
   - tokenization_strategy : TokenizationStrategy
   --
   + sanitize(payload : JSON, scan_report : ScanReport) : JSON
   + truncate(value : String, max_length : Integer) : String
   + normalize_encoding(value : String) : String
   + tokenize_match(match : Match) : String
   + redact_field(payload : JSON, field_path : String) : JSON
   + apply_caps(payload : JSON) : JSON
 }

 enum TokenizationStrategy {
   REVERSIBLE
   IRREVERSIBLE_HASH
   FIXED_TOKEN
 }

 class JSON
 class ScanReport
 class Match

 Sanitizer "1" ..> "0..*" JSON : transforms
 Sanitizer "1" ..> "0..*" ScanReport : reads
 Sanitizer "1" ..> "0..*" Match : tokenizes
 Sanitizer "*" -- "1" TokenizationStrategy

 note right of Sanitizer
   Componente puro: stateless,
   idempotente. Encapsula politicas
   de truncado y enmascaramiento.
 end note

 @enduml

Operaciones principales
=======================

- ``sanitize(payload, scan_report)`` — punto de entrada
  principal. Itera sobre los matches del ``ScanReport`` y
  reemplaza cada valor en el path correspondiente.
- ``truncate(value, max_length)`` — corta strings que excedan
  el límite, agregando sufijo ``...`` para indicar truncado.
- ``normalize_encoding(value)`` — convierte a UTF-8
  normalizado (NFC).
- ``tokenize_match(match)`` — produce el token de reemplazo
  según ``tokenization_strategy``.

Estrategias de tokenización
===========================

- **REVERSIBLE** — el token puede revertirse a su valor
  original con una clave (uso interno restringido a
  investigación de incidentes, P-39 audit reforzado).
- **IRREVERSIBLE_HASH** — hash criptográfico determinístico;
  permite consultas por hash pero no recuperación.
- **FIXED_TOKEN** — reemplazo por valor fijo
  (``"[REDACTED]"``) para máxima opacidad.

Restricciones aplicables
========================

- **CNST-026** — no se persiste ningún valor PII en claro
  después del sanitize.
- **P-39** — la elección de estrategia es auditable (un
  cambio de política se registra como evento).

Trazabilidad a UCs
==================

Invocado por ``AuditService.emit()`` en todos los UCs que
generan ``AuditEvent``. Crítico en:

- :doc:`/requisitos/casos-uso/audit/uc-aud-03/index`
  (export — sanitización doble).
- :doc:`/requisitos/casos-uso/auth/uc-auth-01/index`
  (LOGIN, IP del cliente).

Relaciones
==========

- Componente de ``AuditService`` (composición fuerte).
- Lee ``ScanReport`` producido por ``PIIScanner``.
- Transforma instancias de ``JSON`` (no las posee).
