.. meta::
 :artefacto: AT_UC_RPT_09_USECASE
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

.. _at_uc_rpt_09_configurar_filtros:

==============================
UC_RPT_09 — Configurar Filtros
==============================

User crea/modifica/borra ``SavedFilter``. ``manage_own_filters``
implicita (auto al rol User). Limit hard 30 SavedFilter por User.
Filter encapsula solo filtros (period, dimensiones); diferente de
SavedView (incluye presentation).

.. uml::
 :caption: UC_RPT_09 — actores y casos asociados.

 @startuml

 left to right direction

 actor "manage_own_filters" as manage_own_filters
 actor "SavedFilter" as SavedFilter <<sistema>>
 actor "FilterValidator" as FilterValidator <<sistema>>
 actor "ColumnCatalog" as ColumnCatalog <<sistema>>

 rectangle "MOD_Reports" {
   usecase "UC_RPT_09\nConfigurar Filtros" as UC_RPT_09
   usecase "Validar limite\n< 30 filters por User" as LIMIT
   usecase "Validar payload\n(filtros + dimensiones)" as VALIDAR
   usecase "Validar columnas\nen catalogo" as VALIDAR_COLS
   usecase "Persistir SavedFilter" as PERSIST
 }

 manage_own_filters --> UC_RPT_09

 UC_RPT_09 ..> LIMIT : <<include>>
 UC_RPT_09 ..> VALIDAR : <<include>>
 UC_RPT_09 ..> VALIDAR_COLS : <<include>>
 UC_RPT_09 ..> PERSIST : <<include>>

 VALIDAR --> FilterValidator
 VALIDAR_COLS --> ColumnCatalog
 PERSIST --> SavedFilter

 note bottom of UC_RPT_09
   Diferencia con UC_RPT_10:
   SavedFilter solo guarda filtros;
   SavedView incluye presentation
   completa (orden, group_by, chart).
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/saved-filter` —
   entity persistida.
 - :doc:`/arquitectura-tecnica/domain-model/filter-validator` —
   validacion.
 - :doc:`/arquitectura-tecnica/domain-model/column-catalog` —
   catalogo de columnas validas.
 - :doc:`/requisitos/casos-uso/reports/uc-rpt-09/index` —
   spec textual.
