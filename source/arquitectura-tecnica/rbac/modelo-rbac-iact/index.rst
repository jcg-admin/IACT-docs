.. meta::
 :artefacto: INDEX_MODELO_RBAC_IACT
 :tipo: Indice
 :dominio: arquitectura_tecnica
 :subdominio: rbac/modelo-rbac-iact
 :estado: Vigente
 :version: 5.4.0
 :fecha_creacion: 2026-01-13
 :ultimo_cambio: 2026-05-02
 :autor: NestorMonroy
 :clasificacion: Critico

.. _modelo-rbac-iact:

================
Modelo RBAC IACT
================

Modelo conceptual canonico del control de acceso basado en funciones
atomicas (RBAC) del sistema IACT — version 5.4.0.

**Version:** 5.4.0 — SRP audit + 61 funciones.

Las reglas operativas formales viven en:

- :doc:`/normativa/restricciones/cnst-029-rbac-modelo-plano` — CNST_029
- :doc:`/normativa/restricciones/cnst-030-reglas-de-separacion-de-funciones-sod` — CNST_030
- :doc:`/normativa/restricciones/cnst-031-permisos-temporales-maximo-6-meses` — CNST_031

.. toctree::
 :maxdepth: 1
 :caption: Modelo RBAC IACT

 filosofia
 arquitectura
 catalogo-funciones
 grupos-funciones
 sod
 permisos-temporales
 modelo-datos
 implementacion
 mapeo-uc
 diagramas
 resumen
