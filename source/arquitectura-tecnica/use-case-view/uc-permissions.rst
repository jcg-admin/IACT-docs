.. meta::
 :artefacto: AT_UC_MOD_PERMISSIONS
 :tipo: Diagrama Arquitectonico — UC por Modulo
 :dominio: arquitectura_tecnica
 :subdominio: UCModuleView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_mod_permissions:

=============================================================
MOD_Permissions — Gestion Granular de Permisos: UC por Modulo
=============================================================

MOD_Permissions — Gestion Granular de Permisos
================================================

Vista tecnica del RBAC: gestion de grupos de permisos, funciones a
grupos, verificacion efectiva y generacion del menu dinamico basado
en ``effective_set``.

.. uml::
 :caption: Figura 19 — MOD_Permissions: casos de uso

 @startuml
 left to right direction

 actor "assign_function_groups" as assign_function_groups
 actor "revoke_function_group" as revoke_function_group
 actor "create_function_group" as create_function_group
 actor "assign_functions_to_group" as assign_functions_to_group
 actor "view_assignments" as view_assignments
 actor "view_audit_log" as view_audit_log
 actor "User\n(autenticado)" as user_autenticado

 rectangle "MOD_Permissions" {
   usecase "UC_PERM_01\nAsignar Grupo\na Usuario" as ASIGNAR_GRUPO
   usecase "UC_PERM_02\nRevocar Grupo\na Usuario" as REVOCAR_GRUPO
   usecase "UC_PERM_03\nConceder Permiso\nExcepcional" as CONCEDER_PERMISO_EXCEPCIONAL
   usecase "UC_PERM_04\nRevocar Permiso\nExcepcional" as REVOCAR_PERMISO_EXCEPCIONAL
   usecase "UC_PERM_05\nCrear / Modificar /\nRetirar Grupo" as GESTIONAR_GRUPO_ACCESO
   usecase "UC_PERM_06\nAsignar Funciones\na Grupo" as ASIGNAR_FUNCIONES_GRUPO
   usecase "UC_PERM_07\nVerificar Permiso\nde Usuario" as VERIFICAR_PERMISO_USUARIO
   usecase "UC_PERM_08\nGenerar Menu\nDinamico\n[view_own_navigation]" as GENERAR_MENU_DINAMICO
   usecase "UC_PERM_09\nAuditar Acceso\n(write side)" as AUDITAR_ACCESO
   usecase "UC_PERM_10\nConsultar Auditoria\nde Permisos" as AUDITORIA_ACCESO
 }

 assign_function_groups --> ASIGNAR_GRUPO
 revoke_function_group --> REVOCAR_GRUPO
 assign_function_groups --> CONCEDER_PERMISO_EXCEPCIONAL
 assign_function_groups --> REVOCAR_PERMISO_EXCEPCIONAL
 create_function_group --> GESTIONAR_GRUPO_ACCESO
 assign_functions_to_group --> ASIGNAR_FUNCIONES_GRUPO
 view_assignments --> VERIFICAR_PERMISO_USUARIO
 user_autenticado --> GENERAR_MENU_DINAMICO
 view_audit_log --> AUDITORIA_ACCESO

 ASIGNAR_GRUPO ..> AUDITAR_ACCESO : <<include>>
 REVOCAR_GRUPO ..> AUDITAR_ACCESO : <<include>>
 CONCEDER_PERMISO_EXCEPCIONAL ..> AUDITAR_ACCESO : <<include>>
 REVOCAR_PERMISO_EXCEPCIONAL ..> AUDITAR_ACCESO : <<include>>
 ASIGNAR_FUNCIONES_GRUPO ..> AUDITAR_ACCESO : <<include>>
 GENERAR_MENU_DINAMICO ..> VERIFICAR_PERMISO_USUARIO : <<include>>

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
