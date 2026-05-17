.. meta::
 :artefacto: ARQ_MOD_003_DIAG_CONFLICTO_SEPARACION
 :tipo: Diagrama Arquitectonico — Comportamiento de Modulo
 :dominio: arquitectura_tecnica
 :subdominio: modulos/permissions/diagramas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _arq_mod_003_evaluacion_conflicto_separacion:

===============================================
Evaluacion de Conflicto separacion de deberes
===============================================

.. uml::
 :caption: Evaluación de conflicto de separacion — antes de activar cualquier asignación.

 @startuml

 start

 :Solicitud de asignación\nde función F al usuario U;

 :Obtener funciones activas del usuario U;

 if (¿Alguna función activa entra\nen conflicto de separacion con F?) then (sí)
   :Rechazar asignación\n→ error SEPARATION_VIOLATION;
   stop
 else (no)
   :Registrar asignación;
   :Emitir AuditEvent\n(PERMISSION_GRANT);
   stop
 endif

 note right
   Conflictos definidos:
   - Creador de usuarios <-> Auditor
   - Administrador de reportes <-> Exportación ilimitada
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modulos/permissions/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
