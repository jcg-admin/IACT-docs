.. _uc-alr-04-parte-08-diagrama-secuencia:

8.4 Diagrama de secuencia
==========================

.. uml::
 :caption: UC_ALR_04 — consulta historial.

 @startuml

 actor "view_alert_history" as view_alert_history
 participant "Interfaz de Usuario" as InterfazDeUsuario
 participant "Servicio de Aplicacion" as SvcAplicacion
 database   "AlertRepo" as AlertRepo
 participant "TimingCalculator" as TimingCalculator
 participant "Servicio de Cache" as SvcCache

 view_alert_history -> InterfazDeUsuario: GET /history
 InterfazDeUsuario -> SvcAplicacion: GET /api/v1/alerts/history
 SvcAplicacion -> SvcAplicacion: verificar capability\n(cache)

 SvcAplicacion -> SvcCache: get(key=hash(filters))
 alt cache HIT
   SvcCache --> SvcAplicacion: cached summary
 else cache MISS
   SvcCache --> SvcAplicacion: null
   SvcAplicacion -> AlertRepo: query history\n  WHERE state IN (resolved,closed)
   AlertRepo --> SvcAplicacion: rows
   SvcAplicacion -> TimingCalculator: compute_ttak + compute_ttar
   TimingCalculator --> SvcAplicacion: stats
   SvcAplicacion -> SvcCache: set(key, summary, ttl)
 end

 SvcAplicacion --> InterfazDeUsuario: 200 OK + summary
 InterfazDeUsuario --> view_alert_history: vista historica

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`diagrama-de-actividad`.
 - :doc:`/arquitectura-tecnica/domain-model/alert`.
