.. _arq-mod-002-diagramas:

================================================
ARQ_MOD_002 — Diagramas de Comportamiento
================================================


Ciclo de Vida del Usuario
=========================

.. uml::
 :caption: Ciclo de vida del usuario — estados y transiciones (BR-009 soft delete).

 @startuml

 [*] --> PENDIENTE_CONFIGURACION : alta en el sistema

 PENDIENTE_CONFIGURACION --> ACTIVO : completa preguntas\nde seguridad

 ACTIVO --> INACTIVO : administrador desactiva\n(soft delete, BR-009)
 ACTIVO --> BLOQUEADO : intentos fallidos exceden\numbral (ARQ_MOD_003)

 INACTIVO --> ACTIVO : administrador reactiva
 BLOQUEADO --> ACTIVO : administrador desbloquea

 note right of BLOQUEADO
   Solo ARQ_MOD_003 (RBAC)
   puede desbloquear — no el
   propio usuario.
 end note

 @enduml
