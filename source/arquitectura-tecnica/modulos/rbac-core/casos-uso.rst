.. _arq-mod-003-casos-uso:

================================================
ARQ_MOD_003 — Casos de Uso y Requisitos
================================================

.. contents:: Contenido
 :local:
 :depth: 1

----

Casos de Uso Asociados
=======================

Especificaciones completas:
:doc:`/requisitos/casos-uso/access/index` ·
:doc:`/requisitos/casos-uso/permissions/index`

.. list-table::
 :widths: 12 40 48
 :header-rows: 1

 * - UC ID
   - Nombre
   - Descripcion
 * - UC_041
   - Administrar_Catalogo_Roles
   - CRUD de roles funcionales (R001-R017)
 * - UC_042
   - Calcular_Permisos_Efectivos
   - Aplicar precedencia y SoD
 * - UC_043
   - Asignar_Retirar_Roles
   - Gestionar roles de un usuario
 * - UC_044
   - Configurar_Segmentos_Datos
   - Data segments por centro, servicio
 * - UC_045
   - Asignar_Permisos_Directos
   - Con justificacion y vigencia max 6 meses
 * - UC_046
   - Simular_Acceso_Usuario
   - Preview "¿que veria este usuario?"
 * - UC_047
   - Consultar_Matriz_Roles
   - Vista consolidada para PMO

----

Requisitos Funcionales Derivados
==================================

Los requisitos funcionales derivados de RBAC_CORE se detallan en
:doc:`/requisitos/requisitos-funcionales/access/index`.
