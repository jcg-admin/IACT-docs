.. _arq-mod-002-casos-uso:

================================================
ARQ_MOD_002 — Casos de Uso y Requisitos
================================================

.. contents:: Contenido
 :local:
 :depth: 1

----

Casos de Uso Asociados
=======================

Especificaciones completas: :doc:`/requisitos/casos-uso/users/index`

.. list-table::
 :widths: 12 40 48
 :header-rows: 1

 * - UC ID
   - Nombre
   - Descripcion
 * - UC_006
   - Crear_Cuenta_Usuario
   - Alta con username autogenerado, estado inicial
 * - UC_007
   - Actualizar_Datos_Usuario
   - Modificar nombre, apellidos, unidad, estado
 * - UC_008
   - Baja_Logica_Usuario
   - Soft delete con deleted_at/by
 * - UC_009
   - Gestionar_Preguntas_Seguridad
   - Alta/cambio de min 3 preguntas
 * - UC_010
   - Consultar_Perfil_Usuario
   - Ver datos basicos y roles asignados

----

Requisitos Funcionales Derivados
==================================

.. list-table::
 :widths: 12 45 20 23
 :header-rows: 1

 * - FR ID
   - Nombre
   - Deriva de
   - Descripcion
 * - FR_006
   - Generar_Username_Automatico
   - UC_006
   - Patron: inicial + apellido + numero
 * - FR_007
   - Validar_Datos_Usuario
   - UC_007
   - Campos obligatorios, formatos
 * - FR_008
   - Ejecutar_Baja_Logica
   - UC_008
   - Soft delete, no hard delete
 * - FR_009
   - Almacenar_Preguntas_Seguridad
   - UC_009
   - Hash de respuestas, min 3
 * - FR_010
   - Cargar_Perfil_Usuario
   - UC_010
   - Incluir roles desde RBAC
