.. meta::
 :artefacto: AT_DM_CLASS_PII_SCANNER
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

.. _dm_class_pii_scanner:

==========
PIIScanner
==========

Detector y enmascarador de información personalmente
identificable (PII) en el campo ``details`` de un
``AuditEvent`` antes de su persistencia. Aplica reglas
configurables por categoría (email, teléfono, número de
documento, IP, dirección postal) sobre estructuras anidadas
del payload.

Cumple **CNST-026**: ningún ``AuditEvent`` debe persistir PII
en claro. La detección produce un reporte estructurado
(``ScanReport``) que el ``Sanitizer`` consume para reemplazar
los valores detectados por tokens reversibles o irreversibles
según la política.

.. uml::
 :caption: Clase PIIScanner — detector de PII en payload de
           AuditEvent (CNST-026).

 @startuml

 class PIIScanner {
   - rules : List<DetectionRule>
   - tokenization_strategy : TokenizationStrategy
   --
   + scan(payload : JSON) : ScanReport
   + scan_field(field_path : String, value : String) : List<Match>
   + sanitize(payload : JSON) : SanitizedPayload
   + register_rule(rule : DetectionRule) : void
   + remove_rule(category : PIICategory) : void
 }

 class DetectionRule {
   + category : PIICategory
   + pattern : Regex
   + min_confidence : Float
   --
   + matches(value : String) : Boolean
   + extract(value : String) : List<Match>
 }

 class Match {
   + category : PIICategory
   + field_path : String
   + start : Integer
   + end : Integer
   + raw_value : String
   + confidence : Float
 }

 class ScanReport {
   + matches : List<Match>
   + categories_found : Set<PIICategory>
   + total_count : Integer
   --
   + has_pii() : Boolean
   + by_category(category : PIICategory) : List<Match>
 }

 enum PIICategory {
   EMAIL
   PHONE
   NATIONAL_ID
   IP_ADDRESS
   POSTAL_ADDRESS
   CREDIT_CARD
   FULL_NAME
 }

 enum TokenizationStrategy {
   REVERSIBLE
   IRREVERSIBLE_HASH
   FIXED_TOKEN
 }

 PIIScanner *-- "*" DetectionRule : composes
 PIIScanner "1" ..> "0..*" ScanReport : returns
 PIIScanner "*" -- "1" TokenizationStrategy
 DetectionRule "*" -- "1" PIICategory
 ScanReport *-- "*" Match
 Match "*" -- "1" PIICategory

 note right of PIIScanner
   CNST-026: detecta PII antes de persistir.
   Sanitizer consume el reporte y aplica
   tokenizacion (reversible o no).
 end note

 @enduml

Categorías PII detectadas
=========================

- ``EMAIL`` — direcciones de correo electrónico.
- ``PHONE`` — números telefónicos en formatos comunes.
- ``NATIONAL_ID`` — identificadores nacionales (CURP, RFC,
  DNI según país).
- ``IP_ADDRESS`` — IPv4 e IPv6 fuera de rangos permitidos.
- ``POSTAL_ADDRESS`` — calle, número, código postal.
- ``CREDIT_CARD`` — número de tarjeta (Luhn).
- ``FULL_NAME`` — nombres detectados por NER (heurístico).

Restricciones aplicables
========================

- **CNST-026** — sin PII en claro en almacenes
  inmutables.
- **P-09** — si ``ScanReport.has_pii() == true`` y la
  política configurada es estricta, ``AuditService`` debe
  abortar la transacción del UC invocante.

Trazabilidad a UCs
==================

Invocado indirectamente por todos los UCs que producen
``AuditEvent`` con campo ``details``. Particularmente
crítico en:

- :doc:`/requisitos/casos-uso/audit/uc-aud-03/index`
  (export — sanitización adicional).
- :doc:`/requisitos/casos-uso/auth/uc-auth-01/index`
  (LOGIN: details puede incluir IP y user-agent).

Relaciones
==========

- Compuesto por una colección de ``DetectionRule``.
- Devuelve ``ScanReport`` consumido por ``Sanitizer``.
- Ambos son componentes de ``AuditService``.
