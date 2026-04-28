.. meta::
   :artefacto: CNST_002
   :tipo: Restriccion
   :dominio: normativa
   :subdominio: restricciones
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2025-12-17
   :ultimo_cambio: 2026-04-28
   :autor: NestorMonroy
   :clasificacion: Critico

.. _cnst-002:

===================================
CNST-002: Buzon Interno Obligatorio
===================================

Enunciado
---------

Toda notificacion del sistema IACT a usuarios DEBE entregarse a traves
del buzon interno de la aplicacion, con limites cuantitativos
estrictos sobre alcance, consolidacion y frecuencia de evaluacion.

Justificacion
-------------

Garantiza un canal unico, auditable y bajo control del sistema,
alineado con :doc:`CNST_001_Prohibicion_de_Email_y_SMTP`. Previene
saturacion del buzon, fatiga de alertas y abuso del canal.

Parametros
----------

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Parametro
     - Valor
   * - Maximo destinatarios por alerta
     - 50 usuarios
   * - Ventana de consolidacion de alertas iguales
     - 1 hora
   * - Frecuencia de evaluacion de condiciones
     - cada 5-15 minutos (no real-time)
   * - Otros canales permitidos
     - ninguno (sin SMS, push ni webhooks)

Especificacion
--------------

- Modelo ``InternalMessage`` con campos ``recipient``, ``subject``,
  ``body``, ``priority`` y ``read_at``.
- Alertas del mismo tipo y metrica disparadas en menos de 1 hora se
  consolidan en un unico mensaje.
- Una alerta no admite mas de 50 destinatarios simultaneos.
- La evaluacion de condiciones corre en intervalos de 5 a 15 minutos.

Verificacion
------------

.. code-block:: python

   assert max_recipients(alert) <= 50
   assert dedup_window_hours == 1
   assert evaluation_interval_minutes in range(5, 16)

Referencias cruzadas
--------------------

- :doc:`CNST_001_Prohibicion_de_Email_y_SMTP`
- :doc:`CNST_008_Sincronizacion_ETL_en_Ventana_de_6_a_12_Horas`
