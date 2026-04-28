.. meta::
   :artefacto: CNST_018
   :tipo: Restriccion
   :dominio: normativa
   :subdominio: restricciones
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2025-12-17
   :ultimo_cambio: 2026-04-28
   :autor: NestorMonroy
   :clasificacion: Alto

.. _cnst-018:

============================================
CNST-018: Rango Maximo de Consulta de 2 Anos
============================================

Enunciado
---------

Toda consulta de reporte, dashboard o exportacion DEBE acotarse a un
rango maximo de 2 anos (730 dias) entre ``fecha_inicio`` y
``fecha_fin``. La validacion del rango debe ocurrir ANTES de ejecutar
la query.

Justificacion
-------------

Consultas de mas de 2 anos sobre datos de IVR pueden escanear
millones de registros, generan timeouts, bloquean recursos y rara
vez son utiles desde el punto de vista de negocio.

Parametros
----------

- ``MAX_QUERY_DAYS = 730``.
- Excepcion permitida: rol ``ADMIN_ANALITICA`` con job offline (no
  consulta interactiva).

Verificacion
------------

.. code-block:: python

   if (date_end - date_start).days > 730:
       raise ValidationError("rango maximo 730 dias (2 anos)")

Referencias cruzadas
--------------------

- :doc:`CNST_017_SLA_de_Tiempos_de_Respuesta`
- :doc:`CNST_019_Exportaciones_Asincronas_Sobre_10k_Registros`
