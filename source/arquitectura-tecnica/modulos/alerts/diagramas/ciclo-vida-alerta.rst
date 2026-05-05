.. meta::
 :artefacto: ARQ_MOD_006_DIAG_CICLO_VIDA
 :tipo: Diagrama Arquitectonico — Comportamiento de Modulo
 :dominio: arquitectura_tecnica
 :subdominio: modulos/alerts/diagramas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _arq_mod_006_ciclo_vida_alerta:

===========================
Ciclo de Vida de una Alerta
===========================

.. uml::
 :caption: Estados de una alerta — desde el disparo hasta su resolucion.

 @startuml

 [*] --> ACTIVE : Threshold superado\n(evaluacion periodica)

 ACTIVE --> ACKNOWLEDGED : Alert.acknowledge()\n<<D-02>>
 ACTIVE --> DISABLED : Alert.disable()\n(supervisor desactiva)

 ACKNOWLEDGED --> DISABLED : supervisor cierra\n(resolucion confirmada)
 ACKNOWLEDGED --> ACTIVE : condicion persiste\n(re-evaluacion)

 DISABLED --> [*] : alerta archivada\n(append-only, CNST-025)

 note right of ACTIVE
   Notificacion via InternalMailbox.
   Nunca por email (CNST-001).
   BR-016: tasa abandono >30%
   genera alerta automatica.
   AlertState: ACTIVE / ACKNOWLEDGED / DISABLED
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modulos/alerts/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
