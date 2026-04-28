.. meta::
   :artefacto: CNST_024
   :tipo: Restriccion
   :dominio: normativa
   :subdominio: restricciones
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2025-12-17
   :ultimo_cambio: 2026-04-28
   :autor: NestorMonroy
   :clasificacion: Alto

.. _cnst-024:

============================================
CNST-024: Logs Estructurados en Formato JSON
============================================

Enunciado
---------

Todo log emitido por el sistema IACT DEBE ser estructurado en formato
JSON con campos estandar. Esta prohibido el log de texto libre en
produccion.

Justificacion
-------------

El log estructurado es procesable por herramientas de observabilidad
(ELK, Loki, Sentry) sin parsers ad hoc. El texto libre es opaco al
analisis automatizado.

Campos estandar
---------------

- ``timestamp`` (ISO 8601, UTC).
- ``level`` (``DEBUG|INFO|WARNING|ERROR|CRITICAL``).
- ``logger`` (path del modulo).
- ``message`` (mensaje principal).
- ``request_id`` (UUID por request).
- ``user_id`` (si autenticado).
- ``module`` y ``function``.

Verificacion
------------

.. code-block:: bash

   tail -1 /var/log/iact/app.log | jq -e '.timestamp and .level' && echo "OK"

Referencias cruzadas
--------------------

- :doc:`CNST_025_Auditoria_Inmutable_Append_Only`
- :doc:`CNST_026_PII_Prohibida_en_Logs_y_Auditoria`
