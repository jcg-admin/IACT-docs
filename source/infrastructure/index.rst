.. meta::
   :artefacto: INDEX-INFRASTRUCTURE
   :tipo: Indice
   :dominio: infrastructure
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2026-05-16T23:01:11
   :ultimo_cambio: 2026-05-16T23:01:11
   :autor: NestorMonroy
   :clasificacion: Interno

.. _infrastructure:

================
Infrastructure
================

Documentacion del entorno de servidor del proyecto IACT:
topologia de despliegue, configuracion Ubuntu + Apache + mod_wsgi,
y convenciones operativas.

.. toctree::
   :maxdepth: 1

   overview
   conventions

Trazabilidad
============

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Decisiones de arquitectura**
     - :doc:`/devops/adr-devops-001-vagrant-mod-wsgi-importante-produc` ·
       :doc:`/devops/adr-devops-003-wasi-style-virtualization-importante-db`
   * - **Runbooks operativos**
     - :doc:`/devops/runbooks/index`
