.. meta::
   :artefacto: CNST_008
   :tipo: Restriccion
   :dominio: normativa
   :subdominio: restricciones
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2025-12-17
   :ultimo_cambio: 2026-04-28
   :autor: NestorMonroy
   :clasificacion: Alto

.. _cnst-008:

=======================================================
CNST-008: Sincronizacion ETL en Ventana de 6 a 12 Horas
=======================================================

Enunciado
---------

La sincronizacion de datos desde BD IVR hacia BD Analytics SOLO PUEDE
ejecutarse mediante procesos ETL programados en ventanas de 6 a 12
horas. Esta prohibido el uso de mecanismos de tiempo real (CDC,
WebSockets, replicacion sincrona, polling agresivo).

Justificacion
-------------

Garantiza carga predecible sobre la BD IVR del cliente y permite
planificacion de mantenimiento. El sistema IACT esta disenado para
analisis historico, no para operacion en tiempo real.

Parametros
----------

- Frecuencia ETL: cada 6 a 12 horas.
- Ventana preferente: madrugada (02:00-04:00 hora local).
- Mecanismo: ``django-crontab`` o scheduler equivalente.
- Mecanismos prohibidos: Debezium, WebSockets, polling inferior a 6 h,
  triggers cross-database.

UI obligatoria
--------------

Las vistas que consultan datos provenientes de IVR DEBEN mostrar al
usuario el ``timestamp`` de la ultima actualizacion ETL para que
quede explicita la edad de los datos.

Verificacion
------------

.. code-block:: python

   from etl.models import ETLRun
   last = ETLRun.objects.latest("finished_at")
   assert (now() - last.finished_at).total_seconds() <= 12 * 3600

Referencias cruzadas
--------------------

- :doc:`CNST_006_Arquitectura_de_Base_de_Datos_Dual`
- :doc:`CNST_007_Base_de_Datos_IVR_es_Solo_Lectura`
