.. meta::
 :artefacto: INDEX_MODELO_RBAC_IACT
 :tipo: Indice
 :dominio: arquitectura_tecnica
 :subdominio: rbac/modelo-rbac-iact
 :estado: Vigente
 :version: 5.6.0
 :fecha_creacion: 2026-01-13
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Critico

.. _modelo-rbac-iact:

================
Modelo RBAC IACT
================

Modelo conceptual canonico del control de acceso basado en funciones
atomicas (RBAC) del sistema IACT — version 5.6.0.

**Version:** 5.6.0 — Nuevo modulo **MOD_Admin** (3 funciones) que
formaliza el plano de configuracion del modelo RBAC. Catalogo declara
77 funciones distribuidas en:

- **In-scope / activo (9 modulos · 64 funciones):** MOD_Auth (4),
  MOD_Users (9), MOD_Access (12), MOD_Pipeline (4), MOD_Reports (11),
  MOD_Alerts (10), MOD_Audit (4), MOD_Logs (7), **MOD_Admin (3)**.
- **Reservado / open-closed (2 modulos · 13 funciones):**
  MOD_Operator (10) y MOD_Supervision (3) — declarados en el catalogo
  como extension points; out-of-scope para esta release. Se
  mencionan para preservar el principio open/closed: el catalogo
  esta cerrado para modificacion del set activo, abierto para
  extension a estos dos modulos cuando se decida activarlos.

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
