.. meta::
   :artefacto: CNST_021
   :tipo: Restriccion
   :dominio: normativa
   :subdominio: restricciones
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2025-12-17
   :ultimo_cambio: 2026-04-28
   :autor: NestorMonroy
   :clasificacion: Alto

.. _cnst-021:

==================================================
CNST-021: Stack Obligatorio Ubuntu Apache mod_wsgi
==================================================

Enunciado
---------

El sistema IACT DEBE desplegarse sobre el stack Ubuntu Server +
Apache HTTP Server + ``mod_wsgi`` + Python 3.x. Esta prohibido el uso
de stacks alternativos en produccion.

Justificacion
-------------

Restriccion del cliente: la operacion del cliente esta estandarizada
sobre Ubuntu+Apache. Cambiar el stack obligaria a re-certificar el
ambiente y rompe SLAs operativos del cliente.

Especificacion
--------------

- OS: Ubuntu Server LTS (22.04 o superior).
- HTTP: Apache 2.4+ con ``mod_wsgi`` (no Nginx, no Caddy).
- WSGI: ``mod_wsgi`` (no Gunicorn, no uWSGI).
- Python: 3.10+ instalado en virtualenv.

Verificacion
------------

.. code-block:: bash

   apache2 -v | grep "Apache/2"
   apt list --installed | grep libapache2-mod-wsgi-py3

Referencias cruzadas
--------------------

- :doc:`CNST_022_Estructura_de_Directorios_en_Servidor`
