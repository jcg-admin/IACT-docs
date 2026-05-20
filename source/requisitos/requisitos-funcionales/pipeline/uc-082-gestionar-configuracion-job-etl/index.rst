.. _uc_082_gestionar_configuracion_job_etl:

==================================================
UC-082: Gestionar Configuración del Job ETL
==================================================

.. note::

   UC documentado retroactivamente por la iniciativa
   ``documentar-ucs-implementados-no-declarados``. El
   marker ``UC_PIP_05`` ya existia en codigo
   (apps/pipeline/job_config_views.py) con la
   descripcion "Gestionar configuracion del job ETL"
   pero carecia de RST en docs.

1. Identificación
-----------------

.. list-table::
   :widths: 25 75

   * - **ID**
     - UC-082
   * - **Marker código**
     - ``UC_PIP_05``
   * - **Nombre**
     - Gestionar Configuración del Job ETL
   * - **Actor**
     - Admin / ETL Operations
   * - **Módulo**
     - MOD_Pipeline
   * - **Tipo**
     - Funcional / Admin

2. Especificación
-----------------

CRUD de configuracion de jobs ETL en la tabla
``job_config`` (MariaDB ivr_legacy). Permite:

* Listar configuraciones de todos los jobs.
* Habilitar/deshabilitar un job (BR-ETL-01).
* Modificar timeout, frecuencia o trigger source.
* Inspeccionar detalle (max retries, condiciones de
  skip, etc.).

Endpoints:

* GET /api/pipeline/job-config/
* GET /api/pipeline/job-config/{job_name}/
* PATCH /api/pipeline/job-config/{job_name}/

Diferencia con UC-074 (solicitar reintento): este UC
toca configuracion persistente; UC-074 dispara una
ejecucion adhoc.

3. Trazabilidad
---------------

.. list-table::
   :widths: 20 80

   * - **Marker código**
     - ``UC_PIP_05``
   * - **Implementación**
     - ``apps/pipeline/job_config_views.py``
   * - **TEST**
     - TST-fr-082-XX (pendiente)
   * - **Iniciativa origen**
     - documentar-ucs-implementados-no-declarados
   * - **Regla negocio**
     - BR-ETL-01 (habilitar/deshabilitar job)
