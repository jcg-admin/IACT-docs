.. meta::
   :artefacto: index_auth
   :tipo: Indice
   :dominio: requisitos
   :subdominio: casos_uso/auth
   :estado: Completado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _casos-uso-auth-index:

==============================================================================
MOD_Auth: Casos de Uso de Autenticacion
==============================================================================

Modulo de Autenticacion - Version 2.0 con diagramas PlantUML.

.. contents:: Contenido
   :local:
   :depth: 2

----

Resumen
-------

.. list-table::
   :widths: 30 70
   :header-rows: 0

   * - **Modulo**
     - MOD_Auth
   * - **UC Documentados**
     - 5 (UC-001 a UC-005)
   * - **Version**
     - 2.0.0 (con PlantUML)
   * - **Estado**
     - Completado
   * - **BReq Origen**
     - BReq-004: Cumplimiento de Seguridad
   * - **BR Aplicables**
     - BR_004, BR_005, BR_008, BR_015

----

Casos de Uso
------------

.. list-table::
   :widths: 12 35 15 15 23
   :header-rows: 1

   * - ID
     - Nombre
     - Complejidad
     - Diagramas
     - Estado
   * - UC-001
     - Iniciar Sesion
     - Media
     - 3
     - Completado
   * - UC-002
     - Cerrar Sesion
     - Baja
     - 3
     - Completado
   * - UC-003
     - Recuperar Password
     - Media
     - 3
     - Completado
   * - UC-004
     - Cambiar Password Propio
     - Media
     - 3
     - Completado
   * - UC-005
     - Gestionar Sesiones Activas
     - Media
     - 3
     - Completado

----

Descripcion de Casos de Uso
---------------------------

UC-001: Iniciar Sesion
^^^^^^^^^^^^^^^^^^^^^^

Permite a un usuario autenticarse proporcionando credenciales para obtener
acceso al sistema. Implementa sesion unica (BR_005) y registro de auditoria
(BR_008).

- **Actor:** Usuario no autenticado
- **FR Derivados:** 12
- **BR:** BR_005, BR_008, BR_015

UC-002: Cerrar Sesion
^^^^^^^^^^^^^^^^^^^^^

Permite finalizar la sesion activa de manera segura, invalidando el token
JWT y registrando el evento en auditoria.

- **Actor:** Usuario autenticado
- **FR Derivados:** 8
- **BR:** BR_008

UC-003: Recuperar Password
^^^^^^^^^^^^^^^^^^^^^^^^^^

Permite recuperar acceso mediante pregunta de seguridad. Genera password
temporal mostrado en pantalla (BR_004) con cambio forzado posterior.

- **Actor:** Usuario no autenticado
- **FR Derivados:** 10
- **BR:** BR_004, BR_008

UC-004: Cambiar Password Propio
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Permite cambiar el password propio validando el actual y aplicando politicas
de complejidad. Invalida todas las sesiones tras el cambio.

- **Actor:** Usuario autenticado
- **FR Derivados:** 10
- **BR:** BR_008

UC-005: Gestionar Sesiones Activas
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Permite a administradores visualizar y cerrar forzadamente sesiones activas
de otros usuarios. Requiere permiso AUT-004.

- **Actor:** Administrador de Seguridad (AGR-008)
- **FR Derivados:** 10
- **BR:** BR_005, BR_008
- **Funcion RBAC:** AUT-004

----