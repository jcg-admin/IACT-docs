.. meta::
   :artefacto: CNST_019
   :tipo: Restriccion
   :dominio: normativa
   :subdominio: restricciones
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2025-12-17
   :ultimo_cambio: 2026-04-28
   :autor: NestorMonroy
   :clasificacion: Alto

.. _cnst-019:

======================================================
CNST-019: Exportaciones Asincronas Sobre 10k Registros
======================================================

Enunciado
---------

Toda exportacion que supere 10 000 registros DEBE procesarse de forma
asincrona. La respuesta sincrona DEBE retornar ``202 Accepted`` con
``job_id`` y la entrega final ocurre por el buzon interno.

Justificacion
-------------

Procesamiento sincrono de >10k registros excede el SLA del endpoint y
bloquea workers. La asincronia preserva la disponibilidad para otros
usuarios.

Especificacion
--------------

- Umbral: 10 000 registros.
- Mecanismo: ``Celery`` o equivalente con cola dedicada ``exports``.
- Respuesta sincrona: ``202 Accepted`` + ``{"job_id": ...}``.
- Notificacion al completar: mensaje en buzon interno (CNST_002).

Verificacion
------------

.. code-block:: python

   if total > 10_000:
       job = export_async.delay(query_params)
       return Response({"job_id": job.id}, status=202)

Referencias cruzadas
--------------------

- :doc:`CNST_002_Buzon_Interno_Obligatorio`
- :doc:`CNST_020_Throttling_de_Exportaciones_por_Formato`
