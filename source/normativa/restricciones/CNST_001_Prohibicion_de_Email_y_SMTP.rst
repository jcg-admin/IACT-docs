.. meta::
   :artefacto: CNST_001
   :tipo: Restriccion
   :dominio: normativa
   :subdominio: restricciones
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2025-12-17
   :ultimo_cambio: 2026-04-28
   :autor: NestorMonroy
   :clasificacion: Critico

.. _cnst-001:

=====================================
CNST-001: Prohibicion de Email y SMTP
=====================================

Enunciado
---------

El sistema IACT NO PUEDE enviar correos electronicos por SMTP, ni
integrar servicios de email transaccional, bajo ninguna circunstancia.

Justificacion
-------------

Restriccion de negocio impuesta por el cliente. El cliente NO permite
que aplicaciones corporativas envien correos a traves de servicios
SMTP externos o internos por razones de control de canal y trazabilidad.

Especificacion
--------------

- Prohibido importar ``django.core.mail``, ``smtplib`` o ``sendmail``.
- Prohibido integrar SaaS de email (SendGrid, Mailgun, AWS SES).
- Prohibido configurar servidores SMTP corporativos.
- Prohibido enviar notificaciones por email a usuarios o administradores.

Mecanismo alternativo
---------------------

Toda notificacion debe usar el buzon interno definido en
:doc:`CNST_002_Buzon_Interno_Obligatorio`.

Verificacion
------------

.. code-block:: bash

   grep -E "django-mail|sendgrid|mailgun" requirements.txt && exit 1 || exit 0

Referencias cruzadas
--------------------

- :doc:`CNST_002_Buzon_Interno_Obligatorio`
