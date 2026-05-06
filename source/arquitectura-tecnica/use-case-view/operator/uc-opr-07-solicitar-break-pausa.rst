.. meta::
 :artefacto: AT_UC_OPR_07_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: operator
 :estado: Reservado
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Importante

.. _at_uc_opr_07_solicitar_break_pausa:

============================================================
UC_OPR_07 — Solicitar Break / Pausa
============================================================

Agente solicita break (coffee, lunch, bathroom, training, meeting).
Cada tipo tiene quota policy. Sistema transiciona estado, inicia
tracker de duracion. ``request_break``.

.. uml::
 :caption: UC_OPR_07 — actores y casos asociados.

 @startuml

 left to right direction

 actor "request_break" as request_break
 actor "Action" as Action <<sistema>>
 actor "Session" as Session <<sistema>>
 actor "TimingCalculator" as TimingCalculator <<sistema>>

 rectangle "MOD_Operator" {
   usecase "UC_OPR_07\nSolicitar Break / Pausa" as UC_OPR_07
   usecase "Validar break_type\n(coffee | lunch | bathroom |\ntraining | meeting)" as VALIDAR_TYPE
   usecase "Validar quota\n(policy)" as VALIDAR_QUOTA
   usecase "Transicion estado\na break" as TRANSICIONAR
   usecase "Iniciar tracker\nde duracion" as TRACK
 }

 request_break --> UC_OPR_07

 UC_OPR_07 ..> VALIDAR_TYPE : <<include>>
 UC_OPR_07 ..> VALIDAR_QUOTA : <<include>>
 UC_OPR_07 ..> TRANSICIONAR : <<include>>
 UC_OPR_07 ..> TRACK : <<include>>

 VALIDAR_TYPE --> Action
 VALIDAR_QUOTA --> Action
 TRANSICIONAR --> Session
 TRACK --> TimingCalculator

 note bottom of VALIDAR_QUOTA
   Cada tipo: quota diaria
   (coffee 15min × N, lunch 60min × 1,
   bathroom 5min × M). Exceeder dispara
   alerta operativa al supervisor.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/action` —
   catalogo break types + quota policy.
 - :doc:`/arquitectura-tecnica/domain-model/session` —
   Session state=break.
 - :doc:`/arquitectura-tecnica/domain-model/timing-calculator` —
   tracker duracion.
 - :doc:`/requisitos/casos-uso/operator/uc-opr-07/index` —
   spec textual.
