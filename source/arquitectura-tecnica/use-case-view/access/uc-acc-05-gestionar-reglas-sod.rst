.. meta::
 :artefacto: AT_UC_ACC_05_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: access
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Importante

.. _at_uc_acc_05_gestionar_reglas_sod:

==================================
UC_ACC_05 — Gestionar Reglas SoD
==================================

Vista operativa de reglas SoD (lectura). ``view_separation_rules``
permite consultar reglas activas. La gestion CRUD completa esta en
UC_ADM_01 (admin de reglas). UC_ACC_05 es la consulta — los validators
de UC_ACC_01/04 + UC_PERM_03 cargan estas reglas en cache.

.. uml::
 :caption: UC_ACC_05 — actores y casos asociados.

 @startuml

 left to right direction

 actor "view_separation_rules" as view_separation_rules
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "SeparationRuleRepo" as SeparationRuleRepo <<sistema>>
 actor "PermissionCache" as PermissionCache <<sistema>>

 rectangle "MOD_Access" {
   usecase "UC_ACC_05\nGestionar Reglas SoD\n(consulta operativa)" as UC_ACC_05
   usecase "Verificar\nview_separation_rules" as VERIFICAR_AGR
   usecase "Listar reglas\nactivas (cache)" as LISTAR
   usecase "Filtrar por scope\n+ rule_group" as FILTRAR
 }

 view_separation_rules --> UC_ACC_05

 UC_ACC_05 ..> VERIFICAR_AGR : <<include>>
 UC_ACC_05 ..> LISTAR : <<include>>
 UC_ACC_05 ..> FILTRAR : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 LISTAR --> SeparationRuleRepo
 LISTAR --> PermissionCache
 FILTRAR --> SeparationRuleRepo

 note bottom of UC_ACC_05
   UC_ADM_01 gestiona ciclo de vida
   completo (create/update/disable).
   UC_ACC_05 es solo consulta read-only.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/separation-rule` —
   entity consultada.
 - :doc:`/arquitectura-tecnica/domain-model/separation-rule-repo` —
   repositorio.
 - :doc:`/arquitectura-tecnica/domain-model/permission-cache` —
   reglas activas cacheadas.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica view_separation_rules.
 - :doc:`/requisitos/casos-uso/admin/uc-adm-01/index` —
   gestion CRUD completa.
 - :doc:`/requisitos/casos-uso/access/uc-acc-05/index` —
   spec textual.
