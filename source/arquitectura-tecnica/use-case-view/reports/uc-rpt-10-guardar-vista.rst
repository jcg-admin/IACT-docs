.. meta::
 :artefacto: AT_UC_RPT_10_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: reports
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Importante

.. _at_uc_rpt_10_guardar_vista:

==============================
UC_RPT_10 — Guardar Vista
==============================

User crea/modifica/borra ``SavedView``. ``manage_own_views`` implicita.
Limit hard 30 SavedView por User. SavedView encapsula toda la
configuracion (filtros + columnas + orden + group_by + chart).

.. uml::
 :caption: UC_RPT_10 — actores y casos asociados.

 @startuml

 left to right direction

 actor "manage_own_views" as manage_own_views
 actor "SavedView" as SavedView <<sistema>>
 actor "FilterValidator" as FilterValidator <<sistema>>
 actor "ColumnCatalog" as ColumnCatalog <<sistema>>

 rectangle "MOD_Reports" {
   usecase "UC_RPT_10\nGuardar Vista" as UC_RPT_10
   usecase "Validar limite\n< 30 vistas por User" as LIMIT
   usecase "Validar payload\n(filtros + columnas + orden\n+ group_by + chart)" as VALIDAR
   usecase "Persistir SavedView" as PERSIST
 }

 manage_own_views --> UC_RPT_10

 UC_RPT_10 ..> LIMIT : <<include>>
 UC_RPT_10 ..> VALIDAR : <<include>>
 UC_RPT_10 ..> PERSIST : <<include>>

 VALIDAR --> FilterValidator
 VALIDAR --> ColumnCatalog
 PERSIST --> SavedView

 note bottom of LIMIT
   Hard limit: 30 vistas por User.
   Forza al User a curar su set
   activo.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/saved-view` —
   entity persistida.
 - :doc:`/arquitectura-tecnica/domain-model/saved-filter` —
   subset (UC_RPT_09).
 - :doc:`/arquitectura-tecnica/domain-model/filter-validator` —
   validacion payload.
 - :doc:`/arquitectura-tecnica/domain-model/column-catalog` —
   columnas validas.
 - :doc:`/requisitos/casos-uso/reports/uc-rpt-10/index` —
   spec textual.
