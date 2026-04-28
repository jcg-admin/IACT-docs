.. meta::
   :artefacto: CNST_022
   :tipo: Restriccion
   :dominio: normativa
   :subdominio: restricciones
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2025-12-17
   :ultimo_cambio: 2026-04-28
   :autor: NestorMonroy
   :clasificacion: Medio

.. _cnst-022:

===============================================
CNST-022: Estructura de Directorios en Servidor
===============================================

Enunciado
---------

El despliegue del sistema IACT en servidor DEBE seguir una estructura
de directorios fija para garantizar previsibilidad de operaciones,
backups y rollback.

Estructura
----------

::

   /opt/iact/
   |-- current/           -> symlink al release activo
   |-- releases/
   |   |-- 2026-04-28-001/
   |   |-- 2026-04-28-002/
   |   `-- ...
   |-- shared/
   |   |-- media/
   |   |-- logs/
   |   `-- env/
   `-- venv/

Justificacion
-------------

La estrategia tipo Capistrano permite rollback atomico (cambiar
symlink) y aisla artefactos compartidos del codigo de cada release.

Verificacion
------------

.. code-block:: bash

   test -L /opt/iact/current && echo "OK"
   readlink /opt/iact/current

Referencias cruzadas
--------------------

- :doc:`CNST_021_Stack_Obligatorio_Ubuntu_Apache_mod_wsgi`
- :doc:`CNST_023_Rollback_Obligatorio_en_Cada_Deployment`
