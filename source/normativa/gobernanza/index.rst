.. meta::
 :artefacto: INDEX_GOBERNANZA
 :tipo: Indice
 :dominio: normativa
 :subdominio: gobernanza
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-04-28
 :ultimo_cambio: 2026-04-28
 :autor: NestorMonroy
 :clasificacion: Interno

Gobernanza del Proyecto
=======================

Las decisiones de gobernanza (ADR-GOB-NNN) registran las elecciones
arquitectonicas y metodologicas que aplican al proyecto IACT como un
todo, sin atarse a un tier tecnico especifico.

A diferencia de los ADRs tecnicos (ADR-BACK, ADR-FRONT, ADR-DEVOPS,
ADR-QA), que viven en sus respectivos cajones, los ADR-GOB son
transversales: describen como se organiza el proyecto, como se
estructuran los artefactos de requisitos, y como se trazan las
relaciones entre ellos.

Catalogo
--------

.. toctree::
 :maxdepth: 1
 :caption: ADRs de Gobernanza

 ADR-GOB-001-organizacion-proyecto-por-dominio
 ADR-GOB-002-plantuml-para-diagramas
 ADR-GOB-003-jerarquia-requerimientos-5-niveles
 ADR-GOB-004-clasificacion-reglas-negocio
 ADR-GOB-005-especificacion-casos-uso
 ADR-GOB-006-diagramas-uml-casos-uso
 ADR-GOB-007-trazabilidad-artefactos-requisitos
 ADR-GOB-008-rbac-coexistencia-acc-perm

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
