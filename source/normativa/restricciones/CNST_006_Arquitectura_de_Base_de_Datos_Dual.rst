.. meta::
   :artefacto: CNST_006
   :tipo: Restriccion
   :dominio: normativa
   :subdominio: restricciones
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2025-12-17
   :ultimo_cambio: 2026-04-28
   :autor: NestorMonroy
   :clasificacion: Critico

.. _cnst-006:

============================================
CNST-006: Arquitectura de Base de Datos Dual
============================================

Enunciado
---------

El sistema IACT DEBE operar sobre dos bases de datos separadas: BD
IVR (origen del cliente) y BD Analytics (BD del sistema IACT). No se
permite una unica BD compartida ni acceso directo de IACT a la BD del
cliente para escritura.

Justificacion
-------------

Aisla el sistema del cliente de cualquier riesgo de modificacion
desde IACT. Permite definir politicas de acceso, ETL y disponibilidad
independientes.

Especificacion
--------------

- BD IVR: MySQL o equivalente, propiedad del cliente, accesible solo
  en lectura desde IACT.
- BD Analytics: PostgreSQL, propiedad del sistema IACT, read/write
  para IACT, no accesible al cliente.
- Routers Django enrutan modelos al alias correcto.

Verificacion
------------

.. code-block:: python

   from django.conf import settings
   assert "ivr" in settings.DATABASES
   assert "default" in settings.DATABASES
   assert settings.DATABASE_ROUTERS

Referencias cruzadas
--------------------

- :doc:`CNST_007_Base_de_Datos_IVR_es_Solo_Lectura`
- :doc:`CNST_008_Sincronizacion_ETL_en_Ventana_de_6_a_12_Horas`
