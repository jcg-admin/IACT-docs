.. _uc-rpt-14-parte-08-diagrama-secuencia:

8.4 Diagrama de secuencia
==========================

.. uml::
 :caption: UC_RPT_14 — listado de campanas.

 @startuml

 actor "view_reports" as view_reports
 participant "Servicio de Aplicacion" as SvcAplicacion
 database   "Base Analitica" as BaseAnalitica

 view_reports -> SvcAplicacion: GET /api/v1/campaigns/
 SvcAplicacion -> SvcAplicacion: verificar capability
 SvcAplicacion -> BaseAnalitica: aggregate by campaign
 BaseAnalitica --> SvcAplicacion: rows
 SvcAplicacion --> view_reports: 200 con items

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
