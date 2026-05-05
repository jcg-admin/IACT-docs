.. meta::
 :artefacto: INDEX_AT_PERSPECTIVAS
 :tipo: Indice — Perspectivas Arquitectonicas
 :dominio: arquitectura_tecnica
 :subdominio: Perspectivas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at-perspectivas-index:

=======================================
Perspectivas Arquitectonicas — IACT
=======================================

Las perspectivas son analisis transversales que se aplican a las vistas
existentes para validar que el sistema exhibe propiedades de calidad
requeridas. Fuente: Rozanski & Woods, *Software Systems Architecture* — Cap. 4.

A diferencia de los viewpoints, una perspectiva no produce vistas nuevas:
produce **insights**, **mejoras** y **artefactos** que moldean las vistas
ya definidas. Una perspectiva se aplica a cada vista donde tiene impacto.

Perspectivas implementadas
============================

Solo se desarrollan las tres perspectivas de relevancia ALTA para IACT.
Performance y Evolution tienen cobertura parcial en las vistas existentes
(design-view y implementation-view) y no requieren documento independiente.

.. list-table::
 :header-rows: 1
 :widths: 25 75

 * - Perspectiva
   - Descripcion
 * - :doc:`perspectiva-security`
   - Acceso controlado a recursos sensibles: RBAC multi-nivel,
     JWT con sesion unica, credenciales de solo lectura a IVR
     (P-01, CNST-007). Afecta: Functional, Information, Deployment
     y Operational.
 * - :doc:`perspectiva-regulation`
   - Conformidad con requisitos regulatorios: auditoria de acceso
     append-only (CNST-025), trazabilidad de acciones ciudadanas,
     separacion de funciones (CNST-030), permisos temporales
     documentados (CNST-031).
 * - :doc:`perspectiva-availability`
   - Disponibilidad y resiliencia: aislamiento de fallos del pipeline
     ETL (P-04), recovery procedures, degradacion graceful ante
     indisponibilidad de la BD Operativa IVR.

Cobertura en las vistas existentes
=====================================

.. list-table::
 :header-rows: 1
 :widths: 22 13 13 13 13 13

 * - Vista
   - Security
   - Regulation
   - Availability
   - Performance
   - Evolution
 * - **Context View**
   - Alta
   - Media
   - Alta
   - Baja
   - Baja
 * - **Use Case View**
   - Alta
   - Alta
   - Baja
   - Media
   - Alta
 * - **Domain Model**
   - Media
   - Media
   - Baja
   - Baja
   - Alta
 * - **Process View**
   - Media
   - Media
   - Alta
   - Alta
   - Media
 * - **Design View**
   - Alta
   - Media
   - Media
   - Media
   - Alta
 * - **Implementation View**
   - Media
   - Baja
   - Baja
   - Baja
   - Alta
 * - **Deployment View (+1)**
   - Alta
   - Baja
   - Alta
   - Alta
   - Media
 * - **Operational View**
   - Alta
   - Alta
   - Alta
   - Baja
   - Baja

.. toctree::
 :maxdepth: 1
 :caption: Perspectivas

 perspectiva-security
 perspectiva-regulation
 perspectiva-availability

----

.. seealso::

 :doc:`/base-cognitiva/_uml/uml-14-uml-vistas-arquitectonicas/perspectivas-arquitectonicas`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
