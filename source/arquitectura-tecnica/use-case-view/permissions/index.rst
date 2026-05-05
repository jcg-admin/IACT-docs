.. meta::
 :artefacto: AT_UC_MOD_PERMISSIONS
 :tipo: Diagrama Arquitectonico — UC por Modulo
 :dominio: arquitectura_tecnica
 :subdominio: UCModuleView
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_mod_permissions:

=============================================================
MOD_Permissions — Gestion Granular de Permisos: UC por Modulo
=============================================================

Vista técnica del RBAC: gestión de grupos de permisos,
funciones a grupos, verificación efectiva y generación del
menú dinámico basado en ``effective_set``.

.. uml::
 :caption: MOD_Permissions — AccessAdmin gestiona;
           User autenticado consume verificación y menú.

 @startuml
 left to right direction

 actor User
 actor AccessAdmin
 actor Auditor

 actor TargetUser

 rectangle "MOD_Permissions" {
   usecase "UC_PERM_01\nAsignar Grupo\na Usuario" as ASIGNAR_GRUPO
   usecase "UC_PERM_02\nRevocar Grupo\na Usuario" as REVOCAR_GRUPO
   usecase "UC_PERM_03\nConceder Permiso\nExcepcional" as CONCEDER_PERMISO_EXCEPCIONAL
   usecase "UC_PERM_04\nRevocar Permiso\nExcepcional" as REVOCAR_PERMISO_EXCEPCIONAL
   usecase "UC_PERM_05\nCrear / Modificar /\nRetirar Grupo" as GESTIONAR_GRUPO_ACCESO
   usecase "UC_PERM_06\nAsignar Funciones\na Grupo" as ASIGNAR_FUNCIONES_GRUPO
   usecase "UC_PERM_07\nVerificar Permiso\nde Usuario" as VERIFICAR_PERMISO_USUARIO
   usecase "UC_PERM_08\nGenerar Menu\nDinamico" as GENERAR_MENU_DINAMICO
   usecase "UC_PERM_09\nAuditar Acceso\n(write side)" as AUDITAR_ACCESO
   usecase "UC_PERM_10\nConsultar Auditoria\nde Permisos" as AUDITORIA_ACCESO
 }

 User --> GENERAR_MENU_DINAMICO
 User --> VERIFICAR_PERMISO_USUARIO

 AccessAdmin --> ASIGNAR_GRUPO
 AccessAdmin --> REVOCAR_GRUPO
 AccessAdmin --> CONCEDER_PERMISO_EXCEPCIONAL
 AccessAdmin --> REVOCAR_PERMISO_EXCEPCIONAL
 AccessAdmin --> GESTIONAR_GRUPO_ACCESO
 AccessAdmin --> ASIGNAR_FUNCIONES_GRUPO

 Auditor --> AUDITORIA_ACCESO

 ASIGNAR_GRUPO ..> AUDITAR_ACCESO : <<include>>
 REVOCAR_GRUPO ..> AUDITAR_ACCESO : <<include>>
 CONCEDER_PERMISO_EXCEPCIONAL ..> AUDITAR_ACCESO : <<include>>
 REVOCAR_PERMISO_EXCEPCIONAL ..> AUDITAR_ACCESO : <<include>>
 ASIGNAR_FUNCIONES_GRUPO ..> AUDITAR_ACCESO : <<include>>
 GENERAR_MENU_DINAMICO ..> VERIFICAR_PERMISO_USUARIO : <<include>>
 ASIGNAR_GRUPO --> TargetUser
 REVOCAR_GRUPO --> TargetUser
 CONCEDER_PERMISO_EXCEPCIONAL --> TargetUser
 REVOCAR_PERMISO_EXCEPCIONAL --> TargetUser

 note right of MOD_Permissions
   Codenames RBAC:
     User → view_own_navigation, view_assignments
     AccessAdmin (AGR-007) →
       assign_function_groups, revoke_function_group,
       create_function_group, assign_functions_to_group,
       grant_exceptional_permission,
       revoke_exceptional_permission
     Auditor (AGR-008) → view_audit_log
   UC_PERM_07 es el include canónico de toda
   verificación de permiso (P-15).
 end note

 @enduml

Lectura del diagrama
====================

- ``User`` autenticado obtiene su menú dinámico
  (``UC_PERM_08``) y verifica permisos
  (``UC_PERM_07``).
- ``UC_PERM_08`` ``<<include>>`` ``UC_PERM_07`` —
  generar el menú implica verificar las funciones
  efectivas.
- ``AccessAdmin`` gestiona el catálogo de grupos y
  funciones; toda escritura ``<<include>>``
  ``UC_PERM_09 Auditar Acceso`` (P-09: audit-or-abort).
- ``Auditor`` consulta ``UC_PERM_10`` (read-only).

Implementación en domain-model
==============================

Las clases canónicas que materializan estos UCs viven en
``source/arquitectura-tecnica/domain-model/``:

- :doc:`/arquitectura-tecnica/domain-model/permission-service` — PermissionService (UC_PERM_07).
- :doc:`/arquitectura-tecnica/domain-model/permission-cache` — PermissionCache.
- :doc:`/arquitectura-tecnica/domain-model/rbac-repo` — RbacRepo.
- :doc:`/arquitectura-tecnica/domain-model/access-group` — AccessGroup.
- :doc:`/arquitectura-tecnica/domain-model/access-group-function` — AccessGroupFunction (clase de asociación).
- :doc:`/arquitectura-tecnica/domain-model/function` — Function.
- :doc:`/arquitectura-tecnica/domain-model/function-group` — FunctionGroup (UC_PERM_05).
- :doc:`/arquitectura-tecnica/domain-model/section` — Section.
- :doc:`/arquitectura-tecnica/domain-model/action` — Action.
- :doc:`/arquitectura-tecnica/domain-model/menu` — Menu (UC_PERM_08).
- :doc:`/arquitectura-tecnica/domain-model/nav-domain` — NavDomain.

Casos de uso del módulo
=========================

Cada UC tiene su especificación textual completa y su diagrama
individual (con `<<include>>` y `<<extend>>` per uml-07) en
``source/requisitos/casos-uso/``:

.. list-table::
 :header-rows: 1
 :widths: 20 50 30

 * - UC
   - Nombre
   - Diagrama
 * - :doc:`UC_PERM_01 </requisitos/casos-uso/permissions/uc-perm-01/index>`
   - Asignar Grupo a Usuario
   - :doc:`Diagrama </requisitos/casos-uso/permissions/uc-perm-01/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_PERM_02 </requisitos/casos-uso/permissions/uc-perm-02/index>`
   - Revocar Grupo a Usuario
   - :doc:`Diagrama </requisitos/casos-uso/permissions/uc-perm-02/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_PERM_03 </requisitos/casos-uso/permissions/uc-perm-03/index>`
   - Conceder Permiso Excepcional
   - :doc:`Diagrama </requisitos/casos-uso/permissions/uc-perm-03/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_PERM_04 </requisitos/casos-uso/permissions/uc-perm-04/index>`
   - Revocar Permiso Excepcional
   - :doc:`Diagrama </requisitos/casos-uso/permissions/uc-perm-04/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_PERM_05 </requisitos/casos-uso/permissions/uc-perm-05/index>`
   - Crear Grupo de Permisos
   - :doc:`Diagrama </requisitos/casos-uso/permissions/uc-perm-05/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_PERM_06 </requisitos/casos-uso/permissions/uc-perm-06/index>`
   - Asignar Funciones a Grupo
   - :doc:`Diagrama </requisitos/casos-uso/permissions/uc-perm-06/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_PERM_07 </requisitos/casos-uso/permissions/uc-perm-07/index>`
   - Verificar Permiso de Usuario
   - :doc:`Diagrama </requisitos/casos-uso/permissions/uc-perm-07/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_PERM_08 </requisitos/casos-uso/permissions/uc-perm-08/index>`
   - Generar Menu Dinamico
   - :doc:`Diagrama </requisitos/casos-uso/permissions/uc-perm-08/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_PERM_09 </requisitos/casos-uso/permissions/uc-perm-09/index>`
   - Auditar Acceso (write side)
   - :doc:`Diagrama </requisitos/casos-uso/permissions/uc-perm-09/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_PERM_10 </requisitos/casos-uso/permissions/uc-perm-10/index>`
   - Consultar Auditoria de Permisos
   - :doc:`Diagrama </requisitos/casos-uso/permissions/uc-perm-10/diagramas-uml/diagrama-de-caso-de-uso>`

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`

UC standalone uml-07
====================

Diagramas standalone uml-07 por UC (auto-explicativos):

.. toctree::
 :maxdepth: 1

 uc-perm-01-asignar-grupo-a-usuario
 uc-perm-02-revocar-grupo-a-usuario
 uc-perm-03-conceder-permiso-excepcional
 uc-perm-04-revocar-permiso-excepcional
 uc-perm-05-crear-grupo-de-permisos
 uc-perm-06-asignar-funciones-a-grupo
 uc-perm-07-verificar-permiso-de-usuario
 uc-perm-08-generar-menu-dinamico
 uc-perm-09-auditar-acceso-write-side
 uc-perm-10-consultar-auditoria-de-permisos
