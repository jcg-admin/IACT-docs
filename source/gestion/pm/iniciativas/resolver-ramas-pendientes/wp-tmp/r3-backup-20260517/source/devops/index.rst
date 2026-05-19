.. meta::
 :artefacto: INDEX_DEVOPS
 :tipo: Indice
 :dominio: devops
 :estado: Aprobado
 :version: 1.2.0
 :fecha_creacion: 2026-04-29
 :ultimo_cambio: 2026-05-16T23:01:11
 :autor: NestorMonroy
 :clasificacion: Interno

======
DevOps
======

Decisiones arquitectonicas y procedimientos operativos de
infrastructura y despliegue del proyecto IACT.

ADRs de DevOps viven en este dominio per STD-007 v2.0.2 §4.
Runbooks operativos viven en ``devops/runbooks/``.
La topologia del servidor (Ubuntu + Apache + mod_wsgi) esta
documentada en :doc:`/infrastructure/overview`.

.. toctree::
 :maxdepth: 1
 :caption: ADRs DevOps

 adr-devops-001-vagrant-mod-wsgi-importante-produc
 adr-devops-003-wasi-style-virtualization-importante-db

.. toctree::
 :maxdepth: 1
 :caption: Runbooks Operativos

 runbooks/index
