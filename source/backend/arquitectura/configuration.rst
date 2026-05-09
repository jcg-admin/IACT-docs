:orphan:

.. meta::
 :artefacto: BACK_ARQ_CONFIGURATION
 :tipo: Documentacion de Arquitectura
 :dominio: backend
 :subdominio: arquitectura
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-09
 :ultimo_cambio: 2026-05-09
 :autor: NestorMonroy
 :clasificacion: Importante

.. _back_arq_configuration:

============================================================
Configuracion dinamica del backend
============================================================

Patron de configuracion del backend Django de IACT.
Documenta el modelo dual de configuracion (estatica via
``settings`` + dinamica via ``job_config`` ORM) y las
restricciones operacionales que aplican.

----

Niveles de configuracion
=========================

.. list-table::
 :widths: 25 30 45
 :header-rows: 1

 * - Nivel
   - Persistencia
   - Cuando usar
 * - **Estatica**
   - ``config/settings/{base,dev,prod}.py``
   - Valores que cambian solo con redeploy
     (``DATABASES``, ``INSTALLED_APPS``,
     ``MIDDLEWARE``, ``LOGGING``).
 * - **Por entorno**
   - env vars (``IACT_*``)
   - Secretos, hostnames, paths que cambian entre
     entornos sin redeploy del codigo.
 * - **Dinamica (runtime)**
   - tabla ``job_config`` (MariaDB)
   - Habilitacion/deshabilitacion de jobs,
     intervalos minimos (CNST-003), umbrales
     ajustables.

Configuracion dinamica — tabla ``job_config``
==============================================

La tabla vive en la base IACT. Esquema documentado en
:doc:`/arquitectura-tecnica/pipeline-etl-iact/intermediate-tables`.

Casos de uso:

- Habilitar/deshabilitar el ETL diario sin redeploy.
- Ajustar el intervalo minimo entre ejecuciones (CNST-003).
- Habilitar temporalmente ``etl_historico`` durante un
  backfill manual y deshabilitarlo al terminar.

Lectura
--------

.. code-block:: python

   from django.db import connection

   def is_job_enabled(job_name: str) -> bool:
       with connection.cursor() as c:
           c.execute(
               "SELECT is_enabled FROM job_config WHERE job_name = %s",
               [job_name],
           )
           row = c.fetchone()
           return bool(row and row[0])

Escritura
----------

Las escrituras a ``job_config`` requieren permission
``manage_pipeline_config`` y dejan registro en
``AuditEvent`` (CNST-025).

----

.. seealso::

 - :doc:`/arquitectura-tecnica/pipeline-etl-iact/intermediate-tables` —
   DDL de ``job_config``.
 - :doc:`/normativa/estandares/estandares-codigo` —
   estandares de codigo backend.
