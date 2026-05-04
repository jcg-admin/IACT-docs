.. meta::
 :artefacto: INDEX_AT_VISTAS_KRUCHTEN
 :tipo: Indice
 :dominio: arquitectura_tecnica
 :subdominio: vistas_kruchten
 :estado: Vigente
 :version: 1.2.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at-uc-index:

==========================================
Vistas Arquitectonicas — Modelo 5+1 IACT
==========================================

Indice maestro de las vistas arquitectonicas del sistema IACT
siguiendo el modelo **5+1 (variante DDD de Kruchten)**. Cada vista
cubre un conjunto de concerns de stakeholders segun Rozanski & Woods.

.. list-table::
 :widths: 25 20 55
 :header-rows: 1

 * - Vista
   - Tipo (Rozanski)
   - Descripcion
 * - :doc:`context-view/index`
   - Context (overarching)
   - Frontera del sistema, entidades externas (IVR, APScheduler),
     stakeholders (AGR_ADMIN/OPERADOR/AUDITOR), interfaces y
     restricciones fundamentales (P-01).
 * - :doc:`use-case-view/index`
   - Functional
   - Diagrama UC con actores RBAC, includes y extends.
     13 modulos canonicos. Une todas las demas vistas.
 * - :doc:`domain-model/index`
   - Information
   - Entidades del dominio (26 clases en 8 BCs), atributos,
     metodos, enums y relaciones directas entre clases.
 * - :doc:`process-view/index`
   - Concurrency
   - Patrones de concurrencia: ETL pipeline, alertas paralelas,
     sesiones JWT, dashboard. 4 diagramas canonicos.
 * - :doc:`design-view/index`
   - Development (secuencias)
   - Secuencias de diseno por modulo. Como el sistema resuelve
     cada UC tecnicamente (STD-011 CamelCase).
 * - :doc:`implementation-view/index`
   - Development (componentes)
   - Componentes y stack de 5 capas por modulo. Organizacion
     del codigo fuente.
 * - :doc:`deploy-view/index`
   - Deployment
   - Distribucion fisica. 3 variantes: estandar, auth-cache, etl.

----

.. toctree::
 :maxdepth: 2
 :caption: Vistas arquitectonicas

 context-view/index
 use-case-view/index
 domain-model/index
 process-view/index
 design-view/index
 implementation-view/index
 deploy-view/index
