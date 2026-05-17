.. _uc-alr-02-parte-08-diagrama-secuencia:

8.4 Diagrama de secuencia
==========================

.. uml::
 :caption: UC_ALR_02 — listado con auto-refresh.

 @startuml

 actor "view_alerts" as view_alerts
 participant "Interfaz de Usuario" as InterfazDeUsuario
 participant "Servicio de Aplicacion" as SvcAplicacion
 database   "AlertRepo" as AlertRepo

 view_alerts -> InterfazDeUsuario: abrir vista de alertas

 loop cada 10s
   InterfazDeUsuario -> SvcAplicacion: GET /api/v1/alerts/active/
   SvcAplicacion -> SvcAplicacion: verificar capability\nview_alerts (cache)
   SvcAplicacion -> AlertRepo: query active state\n(firing, acknowledged)\n  AND scope IN segments
   AlertRepo --> SvcAplicacion: rows (paginado)
   SvcAplicacion --> InterfazDeUsuario: 200 OK
   InterfazDeUsuario -> view_alerts: actualizar UI
 end

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`diagrama-de-actividad`.
 - :doc:`/arquitectura-tecnica/domain-model/alert`.
 - :doc:`/arquitectura-tecnica/domain-model/alert-repo`.
