.. _arq-mod-006-diagramas:

================================================
ARQ_MOD_006 — Diagramas de Comportamiento
================================================


Ciclo de Vida de una Alerta
============================

.. uml::
 :caption: Estados de una alerta — desde el disparo hasta su resolución.

 @startuml

 [*] --> PENDIENTE : condición umbral detectada

 PENDIENTE --> ACTIVA : sistema confirma condición\npersiste (evaluación periódica)
 PENDIENTE --> [*] : condición ya no se cumple\n(falsa alarma)

 ACTIVA --> RECONOCIDA : operador reconoce alerta\n(UC_ALR_03)
 ACTIVA --> ACTIVA : suscriptores notificados\nvía buzón interno (CNST_001)

 RECONOCIDA --> RESUELTA : operador marca como resuelta
 RESUELTA --> [*] : alerta archivada\n(inmutable, CNST_025)

 note right of ACTIVA
   Si tiene suscriptores activos,
   el sistema entrega mensaje
   vía InternalMailbox —
   nunca por email (CNST_001).
 end note

 @enduml
