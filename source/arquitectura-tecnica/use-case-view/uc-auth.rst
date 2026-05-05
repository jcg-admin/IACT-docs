.. meta::
 :artefacto: AT_UC_MOD_AUTH
 :tipo: Diagrama Arquitectonico — UC por Modulo
 :dominio: arquitectura_tecnica
 :subdominio: UCModuleView
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_mod_auth:

==================================================
MOD_Auth — Autenticacion y Sesiones: UC por Modulo
==================================================

Gestiona el ciclo de vida de la sesión del usuario: login,
logout, recuperación y cambio de contraseña, y gestión de
sesiones activas.

.. uml::
 :caption: MOD_Auth — actores con jerarquía
           Usuario → Autenticado → SystemAdmin.

 @startuml
 left to right direction

 actor "User\n<<unauthenticated>>" as UnauthUser
 actor "User\n<<authenticated>>"   as AuthUser
 actor SystemAdmin

 UnauthUser <|-- AuthUser
 AuthUser   <|-- SystemAdmin

 rectangle "MOD_Auth" {
   usecase "UC_AUTH_01\nIniciar Sesion" as INICIAR_SESION
   usecase "UC_AUTH_02\nCerrar Sesion" as CERRAR_SESION
   usecase "UC_AUTH_03\nRecuperar Contrasena" as RECUPERAR_CONTRASENA
   usecase "UC_AUTH_04\nCambiar Contrasena" as CAMBIAR_CONTRASENA
   usecase "UC_AUTH_05\nGestionar Sesiones" as GESTIONAR_SESIONES
   usecase "UC_PERM_08\nGenerar Menu Dinamico" as GENERAR_MENU_DINAMICO
 }

 UnauthUser --> INICIAR_SESION
 UnauthUser --> RECUPERAR_CONTRASENA
 AuthUser   --> CERRAR_SESION
 AuthUser   --> CAMBIAR_CONTRASENA
 SystemAdmin --> GESTIONAR_SESIONES

 INICIAR_SESION ..> GENERAR_MENU_DINAMICO : <<include>>

 note right of MOD_Auth
   Codenames RBAC:
     UnauthUser (sin autenticación) →
       UC_AUTH_01, UC_AUTH_03
     AuthUser → UC_AUTH_02, UC_AUTH_04
     SystemAdmin (AGR-010) →
       view_all_active_sessions
       close_user_session
       reset_password
 end note

 @enduml

Lectura del diagrama
====================

- ``UnauthUser`` (User sin sesión activa) inicia
  ``UC_AUTH_01 Iniciar Sesión`` y
  ``UC_AUTH_03 Recuperar Contraseña``.
- ``AuthUser`` (User con sesión activa) hereda y agrega
  ``UC_AUTH_02 Cerrar Sesión`` y
  ``UC_AUTH_04 Cambiar Contraseña``.
- ``SystemAdmin`` (AGR-010) ejecuta
  ``UC_AUTH_05 Gestionar Sesiones`` con permisos de
  ``view_all_active_sessions``, ``close_user_session``,
  ``reset_password``.
- ``UC_AUTH_01`` ``<<include>>`` ``UC_PERM_08`` para
  generar el menú dinámico tras login exitoso.

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
