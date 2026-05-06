.. _arq-mod-010:

================================================
ARQ_MOD_010 — Supervision en Vivo
================================================

.. meta::
 :artefacto: ARQ_MOD_010_INDEX
 :tipo: Modulo Arquitectonico
 :dominio: arquitectura_tecnica
 :estado: Reservado
 :version: 1.1.0
 :fecha_creacion: 2026-05-02
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy

.. warning:: Modulo reservado (out-of-scope para v5.6.0)

 ARQ_MOD_010 (Supervision en Vivo) corresponde a **MOD_Supervision**,
 modulo declarado en el catalogo RBAC v5.6.0 pero **out-of-scope
 para esta release** (extension point open-closed). El grupo
 AGR-012 ``call_center_supervisor_group`` y sus funciones
 (incluyendo barge-in y whisper con tono legal de compliance)
 se preservan en el catalogo como puntos de extension; la
 documentacion arquitectonica permanece como base de diseño para
 activacion futura. Ver
 :doc:`/requisitos/casos-uso/supervision/index` y
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`.

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

- ``monitor_live_calls``
- ``barge_in_calls``
- ``broadcast_team_messages``

Casos de Uso
============

UC_SUP_01..03 — ver :doc:`/requisitos/casos-uso/supervision/index`

Consideraciones de Compliance
==============================

``monitor_live_calls`` y ``barge_in_calls`` generan notificacion audible
al agente (tono de supervision) por obligacion legal. El sistema emite el tono
automaticamente; no puede desactivarse por configuracion.

Dependencias
============

- ARQ_MOD_001 AUTH — sesion JWT obligatoria
- ARQ_MOD_003 RBAC_CORE — verificacion de permisos SUP
- ARQ_MOD_007 AUDIT — registro de intervenciones (CNST-025)
- ARQ_MOD_009 OPERATOR — llamadas activas a supervisar

.. toctree::
 :maxdepth: 1

 diagramas/index
