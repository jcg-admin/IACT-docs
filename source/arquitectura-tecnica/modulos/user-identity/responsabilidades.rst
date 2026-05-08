.. _arq-mod-002-responsabilidades:

================================================
ARQ_MOD_002 — Responsabilidades del Modulo
================================================

.. contents:: Contenido
 :local:
 :depth: 1

----

PUEDE Hacer
===========

.. list-table::
 :widths: 60 20 20
 :header-rows: 1

 * - Responsabilidad
   - UC Relacionado
   - CNST
 * - Crear cuenta con username autogenerado
   - UC_006
   - CNST_005
 * - Asignar estado inicial PENDIENTE_CONFIGURACION
   - UC_006
   - -
 * - Generar contrasena temporal
   - UC_006
   - CNST_001
 * - Actualizar nombre, apellidos, unidad organizacional
   - UC_007
   - -
 * - Cambiar estado del usuario (ACTIVO, INACTIVO, BLOQUEADO)
   - UC_007
   - -
 * - Ejecutar baja logica (soft delete)
   - UC_008
   - CNST_009
 * - Almacenar deleted_at, deleted_by
   - UC_008
   - CNST_009
 * - Gestionar preguntas de seguridad (min 3)
   - UC_009
   - CNST_001
 * - Mostrar perfil con roles asignados
   - UC_010
   - -
 * - Asociar usuario con roles (relacion M:N)
   - UC_007
   - -

----

NO PUEDE Hacer (Violaciones)
=============================

.. warning::

 Las siguientes acciones **violan la separacion de responsabilidades**:

- **Calcular permisos efectivos**

  - Ejemplo: "Si tiene rol X y segmento Y, puede acceder a Z"
  - Responsabilidad de → :ref:`arq-mod-003`

- **Validar conflictos de roles (separation of duties)**

  - Ejemplo: "No puede tener rol A y rol B simultaneamente"
  - Responsabilidad de → :ref:`arq-mod-003`

- **Definir catalogos de permisos**

  - Los enums y catalogos de permisos van en RBAC_CORE
  - Responsabilidad de → :ref:`arq-mod-003`

- **Implementar logica de precedencia**

  - Directo > Rol > Segmento
  - Responsabilidad de → :ref:`arq-mod-003`
