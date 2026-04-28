.. meta::
   :artefacto: CNST_026
   :tipo: Restriccion
   :dominio: normativa
   :subdominio: restricciones
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2025-12-17
   :ultimo_cambio: 2026-04-28
   :autor: NestorMonroy
   :clasificacion: Critico

.. _cnst-026:

===========================================
CNST-026: PII Prohibida en Logs y Auditoria
===========================================

Enunciado
---------

Esta PROHIBIDO incluir PII (Personally Identifiable Information) en
mensajes de log y registros de auditoria. La PII a referenciar se
guarda como ID; el detalle se consulta de la BD por separado segun
el RBAC vigente.

Justificacion
-------------

Los logs son persistidos, replicados a sistemas de observabilidad y eventualmente exportados para soporte. Cualquier PII en los logs amplia la superficie de exposicion fuera del ambito controlado por el RBAC, viola regulaciones tipicas de proteccion de datos y crea pasivos legales.

Categorias prohibidas
---------------------

- Telefono, email, direccion fisica completa.
- Numero de identificacion oficial (DNI, CURP, RFC, SSN, etc.).
- Datos financieros (numero de tarjeta, IBAN).
- Datos biometricos.
- Contenido completo de mensajes de usuarios.

Que SI puede aparecer
---------------------

- ``user_id`` (UUID o entero).
- ``recipient_count`` (numero, no listado).
- ``operation`` (nombre de la accion).

Verificacion
------------

.. code-block:: python

   import re
   PII_PATTERNS = [r"\b\d{10}\b", r"[\w.+-]+@[\w-]+\.[\w.-]+"]

Referencias cruzadas
--------------------

- :doc:`CNST_024_Logs_Estructurados_en_Formato_JSON`
- :doc:`CNST_025_Auditoria_Inmutable_Append_Only`
