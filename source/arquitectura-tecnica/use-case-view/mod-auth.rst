.. meta::
 :artefacto: AT_UC_MOD_AUTH
 :tipo: Diagrama Arquitectonico — UC por Modulo
 :dominio: arquitectura_tecnica
 :subdominio: UCModuleView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_mod_auth:

==================================================
MOD_Auth — Autenticacion y Sesiones: UC por Modulo
==================================================

MOD_Auth — Autenticacion y Sesiones
=====================================

Gestiona el ciclo de vida de la sesion del usuario: login, logout,
recuperacion y cambio de contrasena, y gestion de sesiones activas.

.. uml::
 :caption: Figura 16 — MOD_Auth: casos de uso

 @startuml
 left to right direction

 actor "User\n(no autenticado)" as UsuarioAnonimo
 actor "User\n(autenticado)" as user_autenticado
 actor "view_all_active_sessions" as view_all_active_sessions

 rectangle "MOD_Auth" {
   usecase "UC_AUTH_01\nIniciar Sesion" as A01
   usecase "UC_AUTH_02\nCerrar Sesion" as A02
   usecase "UC_AUTH_03\nRecuperar Contrasena" as A03
   usecase "UC_AUTH_04\nCambiar Contrasena" as A04
   usecase "UC_AUTH_05\nGestionar Sesiones" as A05
   usecase "UC_PERM_08\nGenerar Menu Dinamico\n[view_own_navigation]" as GENERAR_MENU_DINAMICO
 }

 UsuarioAnonimo --> A01
 UsuarioAnonimo --> A03
 user_autenticado --> A02
 user_autenticado --> A04
 view_all_active_sessions --> A05
 A01 ..> GENERAR_MENU_DINAMICO : <<include>>

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
