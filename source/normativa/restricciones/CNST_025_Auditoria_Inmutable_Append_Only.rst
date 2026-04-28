.. meta::
   :artefacto: CNST_025
   :tipo: Restriccion
   :dominio: normativa
   :subdominio: restricciones
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2025-12-17
   :ultimo_cambio: 2026-04-28
   :autor: NestorMonroy
   :clasificacion: Critico

.. _cnst-025:

=========================================
CNST-025: Auditoria Inmutable Append-Only
=========================================

Enunciado
---------

Los registros de auditoria del sistema IACT DEBEN ser inmutables.
Esta prohibido ``UPDATE`` y ``DELETE`` sobre la tabla de auditoria,
incluso desde superusuario de aplicacion.

Justificacion
-------------

La trazabilidad legal y forense requiere garantia de no manipulacion.
Un audit log mutable es indistinguible de no tener audit log a ojos
de un auditor externo.

Especificacion
--------------

- Modelo ``AuditLog`` rechaza ``save()`` para registros existentes
  (override que rechaza ``pk is not None``).
- A nivel BD: trigger que rechaza ``UPDATE`` y ``DELETE``.
- Usuario de BD de aplicacion sin permisos ``UPDATE``/``DELETE`` sobre
  la tabla.
- Retencion minima: 7 anos.

Verificacion
------------

.. code-block:: sql

   CREATE OR REPLACE FUNCTION audit_immutable() RETURNS TRIGGER AS $$
   BEGIN RAISE EXCEPTION 'audit log is append-only'; END;
   $$ LANGUAGE plpgsql;

Referencias cruzadas
--------------------

- :doc:`CNST_024_Logs_Estructurados_en_Formato_JSON`
- :doc:`CNST_026_PII_Prohibida_en_Logs_y_Auditoria`
