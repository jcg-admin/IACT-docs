.. meta::
 :artefacto: ARQ_MOD_002_DIAG_CICLO_VIDA
 :tipo: Diagrama Arquitectonico — Comportamiento de Modulo
 :dominio: arquitectura_tecnica
 :subdominio: modulos/user-identity/diagramas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _arq_mod_002_ciclo_vida_usuario:

=========================
Ciclo de Vida del Usuario
=========================

Ciclo de Vida del Usuario
=========================

.. uml::
 :caption: Ciclo de vida del usuario — estados y transiciones (BR-009 soft delete).

 @startuml

 [*] --> PENDIENTE_CONFIGURACION : alta en el sistema\n(create_users)

 PENDIENTE_CONFIGURACION --> ACTIVO : completa preguntas\nde seguridad

 ACTIVO --> INACTIVO : deactivate_users\n(soft delete, BR-009)
 ACTIVO --> BLOQUEADO : intentos fallidos exceden\numbral (ARQ_MOD_003)

 INACTIVO --> ACTIVO : update_users reactiva
 BLOQUEADO --> ACTIVO : update_users desbloquea

 note right of BLOQUEADO
   Solo RBAC (update_users)
   puede desbloquear — no el
   propio usuario.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modulos/user-identity/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
