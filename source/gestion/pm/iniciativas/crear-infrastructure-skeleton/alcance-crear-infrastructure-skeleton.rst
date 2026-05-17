.. meta::
   :artefacto: ALCANCE-CREAR-INFRASTRUCTURE-SKELETON
   :tipo: Alcance
   :dominio: gestion
   :subdominio: pm/iniciativas/crear-infrastructure-skeleton
   :estado: Aprobado
   :version: 1.0.0

.. _alcance-crear-infrastructure-skeleton:

===========================================
Alcance: Crear Infrastructure Skeleton
===========================================

Por que existe
==============

``source/infrastructure/`` no existe. Es el unico dominio del stack
de producto (Ubuntu + Apache + mod_wsgi) sin representacion en
``source/``. El ADR-DEVOPS-001 y ADR-DEVOPS-003 documentan las
decisiones pero no la topologia ni las convenciones operativas.

Criterio de completitud verificable
=====================================

3 archivos RST existen en ``source/infrastructure/``, estan
enlazados desde ``source/index.rst``, y el build produce 0 warnings.

In-scope
========

- ``source/infrastructure/index.rst``
- ``source/infrastructure/overview.rst`` — topologia, VM, Apache, mod_wsgi
- ``source/infrastructure/conventions.rst`` — naming, paths, puertos, logging
- Actualizar ``source/index.rst`` para incluir infrastructure/
- Actualizar iniciativas/index.rst

Out-of-scope
============

- Scripts Ansible/shell de aprovisionamiento
- Configuraciones Apache concretas (vhosts, SSL)
- Migracion de los 344 MD de temp-holding/infraestructura/
  (contenido de requisitos de infraestructura — iniciativa futura)
