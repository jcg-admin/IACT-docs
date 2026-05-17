.. _arq-mod-006-dependencias:

==================================
ARQ_MOD_006 — Dependencias
==================================


Depende de
==========

.. list-table::
 :widths: 35 65
 :header-rows: 1

 * - Modulo
   - Razon
 * - :ref:`arq-mod-001`
   - Requiere sesion autenticada
 * - :ref:`arq-mod-003`
   - Verifica permisos de configurar alertas
 * - :ref:`arq-mod-004`
   - Obtiene metricas para evaluar condiciones
 * - :ref:`arq-mod-005`
   - Puede usar metricas agregadas

----

Es Requerido por
================

.. list-table::
 :widths: 35 65
 :header-rows: 1

 * - Modulo
   - Razon
 * - :ref:`arq-mod-001`
   - Envia codigo temporal via InternalMessage
 * - :ref:`arq-mod-004`
   - Notifica fallos de ETL
 * - :ref:`arq-mod-007`
   - Registra alertas generadas
