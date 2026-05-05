.. meta::
 :artefacto: AT_UC_MOD_CALLER
 :tipo: Diagrama Arquitectonico — UC por Modulo
 :dominio: arquitectura_tecnica
 :subdominio: UCModuleView
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_mod_caller:

=======================================================
MOD_Caller — Experiencia del Cliente IVR: UC por Modulo
=======================================================

Comportamiento del caller (cliente externo) dentro del
flujo IVR: llamar, navegar menús, esperar en cola, recibir
callback y responder encuesta CSAT post-llamada.

.. uml::
 :caption: MOD_Caller — Caller externo es el actor principal;
           IvrSwitch es sistema externo conmutador.

 @startuml
 left to right direction

 actor "Caller\n<<external>>"     as Caller
 actor "IvrSwitch\n<<system>>"    as IvrSwitch

 rectangle "MOD_Caller" {
   usecase "UC_CLI_01\nLlamar al\nSistema IVR" as LLAMAR_SISTEMA_IVR
   usecase "UC_CLI_02\nNavegar Menu\nIVR" as NAVEGAR_MENU_IVR
   usecase "UC_CLI_03\nEsperar en Cola\nde Atencion" as ESPERAR_COLA
   usecase "UC_CLI_04\nRecibir\nCallback" as RECIBIR_CALLBACK
   usecase "UC_CLI_05\nResponder Encuesta\nCSAT post-llamada" as RESPONDER_ENCUESTA_CSAT
 }

 Caller --> LLAMAR_SISTEMA_IVR
 Caller --> NAVEGAR_MENU_IVR
 Caller --> ESPERAR_COLA
 Caller --> RECIBIR_CALLBACK
 Caller --> RESPONDER_ENCUESTA_CSAT

 LLAMAR_SISTEMA_IVR --> IvrSwitch
 RECIBIR_CALLBACK   <-- IvrSwitch

 LLAMAR_SISTEMA_IVR ..> NAVEGAR_MENU_IVR : <<include>>
 NAVEGAR_MENU_IVR ..> ESPERAR_COLA : <<extend>>
 ESPERAR_COLA ..> RECIBIR_CALLBACK : <<extend>>
 RESPONDER_ENCUESTA_CSAT ..> LLAMAR_SISTEMA_IVR : <<include>>

 note right of MOD_Caller
   Caller: actor externo no autenticado.
     No tiene codenames RBAC.
   IvrSwitch: sistema externo conmutador.
     Origina el callback (UC_CLI_04).
   Codename relacionado:
     offer_csat_post_call (configuracion del
     supervisor, no del Caller).
 end note

 @enduml

Lectura del diagrama
====================

- ``Caller`` es un actor **externo no autenticado** —
  llama al sistema y navega el árbol IVR.
- ``IvrSwitch`` es **sistema externo** (PBX /
  conmutador): recibe la llamada inicial del caller y
  origina el callback en ``UC_CLI_04``.
- ``UC_CLI_01`` ``<<include>>`` ``UC_CLI_02``: llamar
  implica entrar al menú.
- ``UC_CLI_02`` ``<<extend>>`` ``UC_CLI_03``: opcional
  (algunas selecciones llevan a cola, otras no).
- ``UC_CLI_03`` ``<<extend>>`` ``UC_CLI_04``: si el
  caller cuelga durante la espera, puede recibir
  callback.

Implementación en domain-model
==============================

Las clases canónicas que materializan estos UCs viven en
``source/arquitectura-tecnica/domain-model/``:

- :doc:`/arquitectura-tecnica/domain-model/call` — Call (entidad creada al atender).

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
