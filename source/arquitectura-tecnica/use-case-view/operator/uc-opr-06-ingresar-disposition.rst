.. meta::
 :artefacto: AT_UC_OPR_06_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: operator
 :estado: Fuera del scope
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Importante

.. _at_uc_opr_06_ingresar_disposition:

============================================================
UC_OPR_06 — Ingresar Disposition
============================================================

Tras after_call_work, agente registra disposition (resolved,
follow_up, escalation, unreachable, do_not_call). Notes opcionales
≤500 chars sanitized (CNST-026). ``set_call_disposition`` obligatoria.

.. uml::
 :caption: UC_OPR_06 — actores y casos asociados.

 @startuml

 left to right direction

 actor "set_call_disposition" as set_call_disposition
 actor "Action" as Action <<sistema>>
 actor "Call" as Call <<sistema>>
 actor "PIIScanner" as PIIScanner <<sistema>>
 actor "Sanitizer" as Sanitizer <<sistema>>

 rectangle "MOD_Operator" {
   usecase "UC_OPR_06\nIngresar Disposition" as UC_OPR_06
   usecase "Validar agente\nen after_call_work" as VALIDAR_STATE
   usecase "Validar code\n(catalogo Action)" as VALIDAR_CODE
   usecase "Sanitizar notes\n(≤500 chars, sin PII)" as SANITIZAR
   usecase "Persistir Disposition\nen Call" as PERSISTIR
 }

 set_call_disposition --> UC_OPR_06

 UC_OPR_06 ..> VALIDAR_STATE : <<include>>
 UC_OPR_06 ..> VALIDAR_CODE : <<include>>
 UC_OPR_06 ..> SANITIZAR : <<include>>
 UC_OPR_06 ..> PERSISTIR : <<include>>

 VALIDAR_CODE --> Action
 SANITIZAR --> PIIScanner
 SANITIZAR --> Sanitizer
 PERSISTIR --> Call

 note bottom of VALIDAR_CODE
   Catalog: resolved, follow_up,
   escalation, unreachable,
   do_not_call (configurable
   via Action entity).
 end note

 note bottom of SANITIZAR
   CNST-026 sin PII en notes.
   Max 500 chars. PIIScanner +
   Sanitizer reemplazan.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/call` —
   Call con disposition_code + notes.
 - :doc:`/arquitectura-tecnica/domain-model/action` —
   catalogo de codigos.
 - :doc:`/arquitectura-tecnica/domain-model/pii-scanner` —
   detector.
 - :doc:`/arquitectura-tecnica/domain-model/sanitizer` —
   reemplaza.
 - :doc:`/arquitectura-tecnica/domain-model/strategy-pattern` —
   DispositionPromptStrategy.
 - :doc:`/requisitos/casos-uso/operator/uc-opr-06/index` —
   spec textual.
