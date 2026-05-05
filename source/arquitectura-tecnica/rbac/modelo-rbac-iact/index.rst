.. meta::
 :artefacto: INDEX_MODELO_RBAC_IACT
 :tipo: Indice
 :dominio: arquitectura_tecnica
 :subdominio: rbac/modelo-rbac-iact
 :estado: Vigente
 :version: 5.5.0
 :fecha_creacion: 2026-01-13
 :ultimo_cambio: 2026-05-02
 :autor: NestorMonroy
 :clasificacion: Critico

.. _modelo-rbac-iact:

================
Modelo RBAC IACT
================

Modelo conceptual canonico del control de acceso basado en funciones
atomicas (RBAC) del sistema IACT — version 5.5.0.

**Version:** 5.5.0 — Nuevos modulos MOD_Operator (10 funciones) y
MOD_Supervision (3 funciones) derivados del analisis de UCs
UC_OPR_01..10 y UC_SUP_01..03 → total 74 funciones.

Las reglas operativas formales viven en:

- :doc:`/normativa/restricciones/cnst-029-rbac-modelo-plano` — CNST_029
- :doc:`/normativa/restricciones/cnst-030-reglas-de-separacion-de-funciones-sod` — CNST_030
- :doc:`/normativa/restricciones/cnst-031-permisos-temporales-maximo-6-meses` — CNST_031

Especificacion de negocio RBAC (movida a requisitos):

- :doc:`/requisitos/reglas-negocio/rbac/catalogo-funciones` — catalogo de funciones
- :doc:`/requisitos/reglas-negocio/rbac/grupos-funciones` — grupos de funciones
- :doc:`/requisitos/reglas-negocio/rbac/sod` — separacion de deberes
- :doc:`/requisitos/reglas-negocio/rbac/mapeo-uc` — mapeo UC→funcion

Matriz RACI (movida a normativa):
:doc:`/normativa/gobernanza/raci-rbac/index`

.. toctree::
 :maxdepth: 1
 :caption: Modelo RBAC IACT — Arquitectura

 filosofia
 arquitectura
 permisos-temporales
 modelo-datos
 implementacion
 diagramas/index
 resumen
