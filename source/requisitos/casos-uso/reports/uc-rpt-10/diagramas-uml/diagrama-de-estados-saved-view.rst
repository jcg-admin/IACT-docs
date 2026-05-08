.. _uc-rpt-10-parte-08-diagrama-estados-saved-view:

8.4 Diagrama de estados — SavedView
=====================================

.. uml::
 :caption: SavedView — ciclo de vida.

 @startuml

 [*] --> active : crear (UC_RPT_10)
 active --> degraded : columna deprecada en\nColumnCatalog
 degraded --> active : columna restaurada
 active --> deleted : delete (BR-009)
 deleted --> [*]

 note right of degraded
   La vista referencia columnas
   marcadas como deprecadas pero
   sigue siendo aplicable.
   El UI muestra warning.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/saved-view`.
 - :doc:`/requisitos/reglas-negocio/br-009-bajas-logicas`.
