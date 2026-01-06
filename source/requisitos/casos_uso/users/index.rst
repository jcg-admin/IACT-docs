cat > /mnt/user-data/outputs/casos_uso_v2/users/ << 'EOF'
.. meta::
   :artefacto: index_users
   :tipo: Indice
   :dominio: requisitos
   :subdominio: casos_uso/users
   :estado: Completado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _casos-uso-users-index:

==============================================================================
MOD_Users: Casos de Uso de Gestion de Usuarios
==============================================================================

Modulo de Gestion de Usuarios - Version 2.0 con diagramas PlantUML.

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
     - MOD_Users
   * - **UC Documentados**
     - 4 (UC-006 a UC-009)
   * - **Version**
     - 2.0.0 (con PlantUML)
   * - **Estado**
     - Completado
   * - **BReq Origen**
     - BReq-004: Cumplimiento de Seguridad
   * - **BR Aplicables**
     - BR_004, BR_008

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
   * - UC-006
     - Crear Usuario
     - Media
     - 3
     - Completado
   * - UC-007
     - Modificar Usuario
     - Baja
     - 3
     - Completado
   * - UC-008
     - Dar de Baja Usuario
     - Baja
     - 3
     - Completado
   * - UC-009
     - Listar Usuarios
     - Baja
     - 3
     - Completado

----

Descripcion de Casos de Uso
---------------------------

UC-006: Crear Usuario
^^^^^^^^^^^^^^^^^^^^^

Permite crear nuevas cuentas de usuario con password temporal y flag
de cambio obligatorio. Valida unicidad de username y email.

- **Actor:** Administrador de Usuarios (AGR-007)
- **FR Derivados:** 11
- **BR:** BR_004, BR_008
- **Funcion RBAC:** USR-001

UC-007: Modificar Usuario
^^^^^^^^^^^^^^^^^^^^^^^^^

Permite modificar datos de usuario existente. Registra valores anteriores
y nuevos en auditoria para trazabilidad completa.

- **Actor:** Administrador de Usuarios (AGR-007)
- **FR Derivados:** 9
- **BR:** BR_008
- **Funcion RBAC:** USR-002

UC-008: Dar de Baja Usuario
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Permite dar de baja logica a un usuario (no eliminacion fisica). Invalida
sesiones y suspende permisos. Requiere motivo obligatorio.

- **Actor:** Administrador de Usuarios (AGR-007)
- **FR Derivados:** 9
- **BR:** BR_008
- **Funcion RBAC:** USR-003

UC-009: Listar Usuarios
^^^^^^^^^^^^^^^^^^^^^^^

Permite visualizar lista de usuarios con paginacion, busqueda y filtros.
Punto de entrada para operaciones de gestion.

- **Actor:** Administrador de Usuarios (AGR-007)
- **FR Derivados:** 9
- **BR:** Ninguna especifica
- **Funcion RBAC:** USR-004

----

Diagramas Incluidos
-------------------

Cada UC incluye 3 diagramas PlantUML:

1. **Diagrama de Caso de Uso** - Actores y relaciones
2. **Diagrama de Secuencia** - Flujo normal detallado
3. **Diagrama de Actividad** - Decisiones y caminos alternos

Total: **12 diagramas** en este modulo.

----

Metricas
--------

.. list-table::
   :widths: 40 30 30
   :header-rows: 1

   * - Metrica
     - Valor
     - Notas
   * - UC Documentados
     - 4
     - 100%
   * - FR Derivados
     - 38
     - ~9.5 por UC
   * - Diagramas PlantUML
     - 12
     - 3 por UC
   * - Lineas de documentacion
     - ~2,175
     - Total modulo

----

Funciones RBAC del Modulo
-------------------------

.. list-table::
   :widths: 15 35 50
   :header-rows: 1

   * - Funcion
     - Nombre
     - UC que Requiere
   * - USR-001
     - Crear Usuario
     - UC-006
   * - USR-002
     - Modificar Usuario
     - UC-007
   * - USR-003
     - Dar de Baja Usuario
     - UC-008
   * - USR-004
     - Consultar Usuarios
     - UC-009

----

.. toctree::
   :maxdepth: 1
   :caption: Casos de Uso

   UC_006_Crear_Usuario
   UC_007_Modificar_Usuario
   UC_008_Baja_Usuario
   UC_009_Listar_Usuarios

----

Historial de Cambios
--------------------

.. list-table::
   :widths: 12 12 20 56
   :header-rows: 1

   * - Version
     - Fecha
     - Autor
     - Cambios
   * - 2.0.0
     - 2026-01-06
     - Equipo IACT
     - Fase 2 completada: 4 UC con PlantUML embebido
