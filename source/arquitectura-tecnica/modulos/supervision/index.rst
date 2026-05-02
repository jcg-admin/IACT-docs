.. _arq-mod-010:

================================================
ARQ_MOD_010 — Supervision en Vivo
================================================

.. meta::
 :artefacto: ARQ_MOD_010_INDEX
 :tipo: Modulo Arquitectonico
 :dominio: arquitectura_tecnica
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-02
 :autor: NestorMonroy

Proposito
=========

Habilita la supervision en tiempo real de llamadas activas: modo
silent (escucha sin intervencion), whisper (habla solo al agente)
y barge-in (canal tripartito). Incluye broadcast de mensajes al
equipo de agentes via InternalMailbox.

Responsabilidades
=================

- Monitorear llamadas activas en tiempo real (silent/whisper)
- Intervenir en llamadas activas (barge-in tripartito)
- Emitir tono de supervision obligatorio (compliance legal)
- Transmitir mensajes masivos al equipo via InternalMailbox

Funciones RBAC
==============

AGR-012 ``call_center_supervisor_group`` — incluye:

- SUP-001 ``monitor_live_calls``
- SUP-002 ``barge_in_calls``
- SUP-003 ``broadcast_team_messages``

Casos de Uso
============

UC_SUP_01..03 — ver :doc:`/requisitos/casos-uso/supervision/index`

Consideraciones de Compliance
==============================

SUP-001 y SUP-002 generan notificacion audible al agente (tono de
supervision) por obligacion legal. El sistema emite el tono
automaticamente; no puede desactivarse por configuracion.

Dependencias
============

- ARQ_MOD_001 AUTH — sesion JWT obligatoria
- ARQ_MOD_003 RBAC_CORE — verificacion de permisos SUP
- ARQ_MOD_007 AUDIT — registro de intervenciones (CNST-025)
- ARQ_MOD_009 OPERATOR — llamadas activas a supervisar

.. toctree::
 :maxdepth: 1

 diagramas
