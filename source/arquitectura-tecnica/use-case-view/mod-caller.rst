.. meta::
 :artefacto: AT_UC_MOD_CALLER
 :tipo: Diagrama Arquitectonico — UC por Modulo
 :dominio: arquitectura_tecnica
 :subdominio: UCModuleView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_mod_caller:

=======================================================
MOD_Caller — Experiencia del Cliente IVR: UC por Modulo
=======================================================

MOD_Caller — Experiencia del Cliente IVR
==========================================

Comportamiento del cliente (llamante externo) dentro del flujo
IVR: llamar, navegar menus, esperar en cola, recibir callback y
responder encuesta CSAT post-llamada.

.. uml::
 :caption: Figura 27 — MOD_Caller: casos de uso

 @startuml
 left to right direction

 actor "Caller\n(externo)" as CALLER

 rectangle "MOD_Caller" {
   usecase "UC_CLI_01\nLlamar al\nSistema IVR" as LLAMAR_SISTEMA_IVR
   usecase "UC_CLI_02\nNavegar Menu\nIVR" as NAVEGAR_MENU_IVR
   usecase "UC_CLI_03\nEsperar en Cola\nde Atencion" as ESPERAR_COLA
   usecase "UC_CLI_04\nRecibir\nCallback" as RECIBIR_CALLBACK
   usecase "UC_CLI_05\nResponder Encuesta\nCSAT post-llamada\n[offer_csat_post_call]" as RESPONDER_ENCUESTA_CSAT
 }

 CALLER --> LLAMAR_SISTEMA_IVR
 CALLER --> NAVEGAR_MENU_IVR
 CALLER --> ESPERAR_COLA
 CALLER --> RECIBIR_CALLBACK
 CALLER --> RESPONDER_ENCUESTA_CSAT

 LLAMAR_SISTEMA_IVR ..> NAVEGAR_MENU_IVR : <<include>>
 NAVEGAR_MENU_IVR ..> ESPERAR_COLA : <<extend>>
 ESPERAR_COLA ..> RECIBIR_CALLBACK : <<extend>>
 RESPONDER_ENCUESTA_CSAT ..> LLAMAR_SISTEMA_IVR : <<include>>

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
