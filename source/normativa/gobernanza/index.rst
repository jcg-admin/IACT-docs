.. meta::
 :artefacto: INDEX_GOBERNANZA
 :tipo: Indice
 :dominio: normativa
 :subdominio: gobernanza
 :estado: Vigente
 :version: 1.1.0
 :fecha_creacion: 2026-04-28
 :ultimo_cambio: 2026-04-29
 :autor: NestorMonroy
 :clasificacion: Interno

Gobernanza del Proyecto
=======================

Las decisiones arquitectonicas (ADR) del proyecto IACT viven en este
cajon, organizadas por modulo:

- **ADR-GOB**: gobernanza transversal (organizacion, requisitos,
  diagramas, trazabilidad).
- **ADR-BACK**: decisiones del backend (Django, ORM, permisos).
- **ADR-FRONT**: decisiones del frontend (React, Webpack, state
  management).
- **ADR-DEVOPS**: decisiones de infraestructura y despliegue.
- **ADR-QA**: decisiones de testing y calidad.

Catalogo
--------

.. toctree::
 :maxdepth: 1
 :caption: ADRs de Gobernanza (transversales)

 adr-gob-001-organizacion-proyecto-por-dominio
 adr-gob-002-plantuml-para-diagramas
 adr-gob-003-jerarquia-requerimientos-5-niveles
 adr-gob-004-clasificacion-reglas-negocio
 adr-gob-005-especificacion-casos-uso
 adr-gob-006-diagramas-uml-casos-uso
 adr-gob-007-trazabilidad-artefactos-requisitos
 adr-gob-008-rbac-coexistencia-acc-perm

.. toctree::
 :maxdepth: 1
 :caption: ADRs Backend

 adr-back-001-grupos-funcionales-sin-jerarquia
 adr-back-002-configuracion-dinamica-sistema
 adr-back-003-orm-sql-hybrid-permissions
 adr-back-004-sistema-permisos-sin-roles-jerarquicos

.. toctree::
 :maxdepth: 1
 :caption: ADRs Frontend

 adr-front-001-frontend-modular-monolith
 adr-front-002-redux-toolkit-state-management
 adr-front-003-webpack-bundler
 adr-front-004-arquitectura-microfrontends
 adr-front-010-typescript-adopcion-gradual

.. toctree::
 :maxdepth: 1
 :caption: ADRs DevOps

 adr-devops-001-vagrant-mod-wsgi-importante-produc
 adr-devops-003-wasi-style-virtualization-importante-db

.. toctree::
 :maxdepth: 1
 :caption: ADRs QA

 adr-qa-002-testing-strategy-jest-testing-library

Estructura por dominio
----------------------

**Organizacion del proyecto**

- :doc:`adr-gob-001-organizacion-proyecto-por-dominio` — organizacion
  del repositorio por dominio (no por tipo de archivo).

**Documentacion y diagramas**

- :doc:`adr-gob-002-plantuml-para-diagramas` — PlantUML como
  estandar para todos los diagramas UML.
- :doc:`adr-gob-006-diagramas-uml-casos-uso` — diagramas UML
  obligatorios para los casos de uso.

**Modelo de requisitos**

- :doc:`adr-gob-003-jerarquia-requerimientos-5-niveles` — jerarquia
  de 5 niveles (BReq → BR → UC → FR → NFR/CNST).
- :doc:`adr-gob-004-clasificacion-reglas-negocio` — clasificacion
  y formato canonico de las BRs.
- :doc:`adr-gob-005-especificacion-casos-uso` — formato completo de
  los UCs.
- :doc:`adr-gob-007-trazabilidad-artefactos-requisitos` — matrices
  de trazabilidad bidireccional entre BR/UC/FR/CNST.

Convenciones
------------

- Numeracion ``ADR-GOB-NNN`` flat consecutiva (sin gaps).
- Cada ADR tiene clasificacion ``Critico``, ``Alto`` o ``Medio`` segun
  el impacto de revertirlo o ignorarlo.
- ADRs tecnicos (BACK/FRONT/DEVOPS/QA) viven en sus cajones
  respectivos, no aqui (ver `discover/handoff-to-tech-wps.md` del
  WP gobernanza para el detalle de transferencias).
- El formato sigue
  :doc:`/normativa/estandares/std-007-convencion-naming` y
  :doc:`/normativa/estandares/plantillas/tpl-adr-decisiones-arquitectonicas`.
