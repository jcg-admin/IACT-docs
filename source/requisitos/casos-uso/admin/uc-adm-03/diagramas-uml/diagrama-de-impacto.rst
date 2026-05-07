.. _uc-adm-03-parte-08-diagrama-impacto:

8.3 Diagrama de impacto — preview de cambio
============================================

.. uml::
 :caption: UC_ADM_03 — preview de impacto sin persistir cambios.

 @startuml

 actor "assign_functions_to_group" as assign_functions_to_group
 participant "Interfaz de Usuario" as InterfazDeUsuario
 participant "Servicio de Aplicacion" as SvcAplicacion
 database   "Almacen de Datos" as AlmacenDatos
 participant "EvaluatorReloader" as EvaluatorReloader
 participant "ImpactReport" as ImpactReport

 assign_functions_to_group -> InterfazDeUsuario: GET /impact/?add=codename
 InterfazDeUsuario -> SvcAplicacion: GET /api/v1/admin/system-groups/{id}/impact/

 SvcAplicacion -> AlmacenDatos: users_with_agr(group_id)
 AlmacenDatos --> SvcAplicacion: [user_ids]

 SvcAplicacion -> EvaluatorReloader: preview_effective_set(group_id, add=codename)
 EvaluatorReloader --> SvcAplicacion: ImpactReport

 SvcAplicacion --> InterfazDeUsuario: { affected_users: N, preview: [...] }
 InterfazDeUsuario --> assign_functions_to_group: vista de impacto

 note right of EvaluatorReloader
   No persiste ningun cambio.
   Solo simula el efecto del add
   sobre el effective_set de los
   users que tienen el AGR.
 end note

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`/arquitectura-tecnica/domain-model/evaluator-reloader`.
 - :doc:`/arquitectura-tecnica/domain-model/effective-permissions-aggregator`.
