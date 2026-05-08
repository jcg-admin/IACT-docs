.. meta::
 :artefacto: AT_DESIGN_MOD_ADMIN
 :tipo: Diagrama Arquitectonico — Design View — Module Box
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :modulo: admin
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_mod_admin:

============================================================
Design View — MOD_Admin: Vista de Diseño
============================================================

Caja del modulo **MOD_Admin** (gestion de catalogos RBAC).
Este modulo administra el ciclo de vida del catalogo de
funciones, agrupadores predefinidos (AGRs) y reglas de
separacion (SoD).

Materializa los UCs UC_ADM_01..05 documentados en
:doc:`/arquitectura-tecnica/use-case-view/admin/index`.

Vista panoramica del modulo
============================

.. uml::
 :caption: MOD_Admin — entidades del catalogo y puntos de
           contacto inter-modulo. Subset curado; detalle de
           repositories en :doc:`class`.

 @startuml

 package "MOD_Admin" {
   class Function <<entity>>
   class FunctionGroup <<entity>>
   class SeparationRule <<entity>>
 }

 class AuthorizationGuard <<service>>
 class AuditService <<service>>

 FunctionGroup *-- "*" Function : agrupa
 SeparationRule --> Function : restringe pares (A,B)

 AuthorizationGuard ..> Function : <<verify>>
 Function ..> AuditService : <<emite eventos>>
 FunctionGroup ..> AuditService : <<emite eventos>>
 SeparationRule ..> AuditService : <<emite eventos>>

 note bottom of Function
   3 entidades del catalogo RBAC.
   Repositories y detalles en :doc:`class`.
 end note

 @enduml

Lectura del diagrama
====================

- **Tres entidades del catalogo:** ``Function`` (atomic
  capability), ``FunctionGroup`` (agrupador predefinido para
  AGRs) y ``SeparationRule`` (par prohibido de funciones
  para separation-of-duties).
- ``FunctionGroup`` agrega instancias de ``Function``; el
  catalogo de AGRs predefinidos vive en este modulo.
- ``SeparationRule`` restringe pares (conjuntoA, conjuntoB)
  de funciones que no pueden coexistir en el effective_set
  de un mismo usuario.
- ``AuthorizationGuard`` consume el catalogo en tiempo de
  ejecucion para verificar capabilities.
- Cada cambio en el catalogo emite ``AuditEvent`` inmutable
  via ``AuditService``.

Clases canonicas que materializan el modulo
============================================

- :doc:`/arquitectura-tecnica/domain-model/function` —
  Function entity (catalogo).
- :doc:`/arquitectura-tecnica/domain-model/function-repo` —
  FunctionRepo.
- :doc:`/arquitectura-tecnica/domain-model/function-group` —
  FunctionGroup (AGR base).
- :doc:`/arquitectura-tecnica/domain-model/function-group-repo` —
  FunctionGroupRepo.
- :doc:`/arquitectura-tecnica/domain-model/separation-rule` —
  SeparationRule.
- :doc:`/arquitectura-tecnica/domain-model/separation-rule-repo` —
  SeparationRuleRepo.
- :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
  AuthorizationGuard (consumidor externo).
- :doc:`/arquitectura-tecnica/domain-model/audit-service` —
  AuditService (consumidor externo).

Sub-vistas del modulo
======================

.. toctree::
 :maxdepth: 1
 :caption: Diagramas del modulo MOD_Admin

 class
 sequence

----

.. seealso::

 - :doc:`/arquitectura-tecnica/use-case-view/admin/index` —
   UCs del modulo (vista de requisitos).
 - :doc:`/arquitectura-tecnica/design-view/index` —
   raiz de DesignView.
 - :doc:`/arquitectura-tecnica/design-view/access/index` —
   modulo que consume el catalogo (asignaciones).
 - :doc:`/arquitectura-tecnica/design-view/package-overview`.
