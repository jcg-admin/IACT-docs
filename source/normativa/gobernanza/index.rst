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

 ADR-GOB-001-organizacion-proyecto-por-dominio
 ADR-GOB-002-plantuml-para-diagramas
 ADR-GOB-003-jerarquia-requerimientos-5-niveles
 ADR-GOB-004-clasificacion-reglas-negocio
 ADR-GOB-005-especificacion-casos-uso
 ADR-GOB-006-diagramas-uml-casos-uso
 ADR-GOB-007-trazabilidad-artefactos-requisitos
 ADR-GOB-008-rbac-coexistencia-acc-perm

.. toctree::
 :maxdepth: 1
 :caption: ADRs Backend

 ADR-BACK-001-grupos-funcionales-sin-jerarquia
 ADR-BACK-002-configuracion-dinamica-sistema
 ADR-BACK-003-orm-sql-hybrid-permissions
 ADR-BACK-004-sistema-permisos-sin-roles-jerarquicos

.. toctree::
 :maxdepth: 1
 :caption: ADRs Frontend

 ADR-FRONT-001-frontend-modular-monolith
 ADR-FRONT-002-redux-toolkit-state-management
 ADR-FRONT-003-webpack-bundler
 ADR-FRONT-004-arquitectura-microfrontends
 ADR-FRONT-010-typescript-adopcion-gradual

.. toctree::
 :maxdepth: 1
 :caption: ADRs DevOps

 ADR-DEVOPS-001-vagrant-mod-wsgi-importante-produc
 ADR-DEVOPS-003-wasi-style-virtualization-importante-db

.. toctree::
 :maxdepth: 1
 :caption: ADRs QA

 ADR-QA-002-testing-strategy-jest-testing-library

Estructura por dominio
----------------------

**Organizacion del proyecto**

- :doc:`ADR-GOB-001-organizacion-proyecto-por-dominio` — organizacion
  del repositorio por dominio (no por tipo de archivo).

**Documentacion y diagramas**

- :doc:`ADR-GOB-002-plantuml-para-diagramas` — PlantUML como
  estandar para todos los diagramas UML.
- :doc:`ADR-GOB-006-diagramas-uml-casos-uso` — diagramas UML
  obligatorios para los casos de uso.

**Modelo de requisitos**

- :doc:`ADR-GOB-003-jerarquia-requerimientos-5-niveles` — jerarquia
  de 5 niveles (BReq → BR → UC → FR → NFR/CNST).
- :doc:`ADR-GOB-004-clasificacion-reglas-negocio` — clasificacion
  y formato canonico de las BRs.
- :doc:`ADR-GOB-005-especificacion-casos-uso` — formato completo de
  los UCs.
- :doc:`ADR-GOB-007-trazabilidad-artefactos-requisitos` — matrices
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
  :doc:`/normativa/estandares/STD_007_Convencion_Naming` y
  :doc:`/normativa/estandares/plantillas/TPL_ADR_Decisiones_Arquitectonicas`.
