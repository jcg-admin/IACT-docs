.. meta::
   :artefacto: index_access
   :tipo: Indice
   :dominio: requisitos
   :subdominio: casos_uso/access
   :estado: En Desarrollo
   :version: 2.0.0

.. _casos-uso-access-index:

==============================================================================
MOD_Access: Casos de Uso de Control de Acceso
==============================================================================

Indice de Casos de Uso del modulo de Control de Acceso (RBAC).

----

Resumen
-------

.. list-table::
   :widths: 30 70
   :header-rows: 0

   * - **Modulo**
     - MOD_Access
   * - **UC Planificados**
     - 9 (UC-010, UC-011, UC-041 a UC-047)
   * - **Version**
     - 2.0.0 (con PlantUML)
   * - **BReq Origen**
     - BReq-004: Cumplimiento de Seguridad

----

Casos de Uso
------------

.. list-table::
   :widths: 15 40 20 25
   :header-rows: 1

   * - ID
     - Nombre
     - Complejidad
     - Estado
   * - UC-010
     - Asignar Funciones a Usuario
     - Alta
     - Pendiente
   * - UC-011
     - Revocar Funciones a Usuario
     - Media
     - Pendiente
   * - UC-041
     - Asignar Segmento de Datos
     - Media
     - Pendiente
   * - UC-042
     - Revocar Segmento de Datos
     - Baja
     - Pendiente
   * - UC-043
     - Configurar Restricciones SoD
     - Alta
     - Pendiente
   * - UC-044
     - Consultar Permisos Efectivos
     - Media
     - Pendiente
   * - UC-045
     - Gestionar Catalogo Agrupadores
     - Media
     - Pendiente
   * - UC-046
     - Gestionar Catalogo Funciones
     - Media
     - Pendiente
   * - UC-047
     - Auditar Cambios de Permisos
     - Media
     - Pendiente

----

.. toctree::
   :maxdepth: 1
   :caption: Casos de Uso

   UC_010_Asignar_Funciones
   UC_011_Revocar_Funciones
   UC_041_Asignar_Segmento
   UC_042_Revocar_Segmento
   UC_043_Configurar_SoD
   UC_044_Consultar_Permisos
   UC_045_Gestionar_Agrupadores
   UC_046_Gestionar_Funciones
   UC_047_Auditar_Permisos
