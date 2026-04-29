.. meta::
   :artefacto: INDEX_DATABASES
   :tipo: Indice
   :dominio: databases
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2026-04-29
   :ultimo_cambio: 2026-04-29
   :autor: NestorMonroy
   :clasificacion: Interno

==============
Bases de Datos
==============

Documentacion del modelo de datos dual del sistema IACT (MySQL IVR
readonly + PostgreSQL Analytics) y del pipeline ETL.

.. toctree::
   :maxdepth: 1

   modelo-dual
   etl-pipeline

.. note::

   Las restricciones del modelo de datos viven en
   :doc:`/normativa/restricciones/CNST_006_Arquitectura_de_Base_de_Datos_Dual`,
   :doc:`/normativa/restricciones/CNST_007_Base_de_Datos_IVR_es_Solo_Lectura`,
   :doc:`/normativa/restricciones/CNST_008_Sincronizacion_ETL_en_Ventana_de_6_a_12_Horas`.
