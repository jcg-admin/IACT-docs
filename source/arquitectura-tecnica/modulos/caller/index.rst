.. _arq-mod-011:

================================================
ARQ_MOD_011 — Experiencia del Cliente IVR
================================================

.. meta::
 :artefacto: ARQ_MOD_011_INDEX
 :tipo: Modulo Arquitectonico
 :dominio: arquitectura_tecnica
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-02
 :autor: NestorMonroy

Proposito
=========

Modela el comportamiento del llamante externo (Caller) dentro del
flujo IVR: llamada entrante, navegacion de menus, espera en cola,
recepcion de callback y respuesta a encuesta CSAT post-llamada.

Responsabilidades
=================

- Recibir y enrutar llamadas al sistema IVR (tbl_historico_*)
- Gestionar menus de navegacion IVR
- Manejar cola de atencion y callbacks automaticos
- Recolectar respuestas CSAT para analisis de abandono (BR-016)

Actores
=======

``Caller`` — usuario externo sin RBAC (no autenticado en el sistema).
El Caller interactua con la infraestructura telefonica, no con la
API REST del sistema IACT.

Casos de Uso
============

UC_CLI_01..05 — ver :doc:`/requisitos/casos-uso/caller/index`

Nota Arquitectonica
===================

Este modulo no expone API REST publica. La interaccion del Caller
ocurre a traves de la infraestructura IVR (PBX/Asterisk). Los datos
se persisten en ``tbl_historico_detalle`` y ``tbl_historico_clientes``
del Repositorio IVR (MariaDB, solo lectura para IACT).

El ETL nocturno (ARQ_MOD_004) transforma estos datos hacia la Base
Analitica para reportes y alertas.

Dependencias
============

- ARQ_MOD_004 ETL_MONITORING — consume datos de llamadas
- ARQ_MOD_005 VIS_REPORTS — reportes sobre comportamiento del Caller
- ARQ_MOD_006 ALERTS — alerta BR-016 tasa de abandono

.. toctree::
 :maxdepth: 1

 diagramas/index
