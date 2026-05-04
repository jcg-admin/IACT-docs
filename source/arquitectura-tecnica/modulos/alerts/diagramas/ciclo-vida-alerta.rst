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

Ciclo de Vida de una Alerta
============================

.. uml::
 :caption: Estados de una alerta — desde el disparo hasta su resolucion.

 @startuml

 [*] --> PENDIENTE : condicion umbral detectada

 PENDIENTE --> ACTIVA : sistema confirma condicion\npersiste (evaluacion periodica)
 PENDIENTE --> [*] : condicion ya no se cumple\n(falsa alarma)

 ACTIVA --> RECONOCIDA : acknowledge_alert invoca UC_ALR_03
 ACTIVA --> ACTIVA : suscriptores notificados\nvia InternalMailbox (CNST-001)

 RECONOCIDA --> RESUELTA : operador marca como resuelta
 RESUELTA --> [*] : alerta archivada\n(inmutable, CNST-025)

 note right of ACTIVA
   Nunca por email (CNST-001).
   BR-016: tasa abandono >30%
   genera alerta automatica.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modulos/alerts/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
