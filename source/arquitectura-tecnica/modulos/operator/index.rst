.. _arq-mod-009:

==============================================
ARQ_MOD_009 — Panel del Operador
==============================================

.. meta::
 :artefacto: ARQ_MOD_009_INDEX
 :tipo: Modulo Arquitectonico
 :dominio: arquitectura_tecnica
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-02
 :autor: NestorMonroy

Proposito
=========

Gestiona el panel de trabajo del operador de call center: cambio de
estado de disponibilidad, atencion de llamadas entrantes y salientes,
hold/transfer, registro de disposicion post-llamada, solicitud de
breaks, y consulta de estadisticas e historial propios.

Responsabilidades
=================

- Gestionar el ciclo de estado del agente (available/busy/break/offline)
- Controlar el flujo de llamadas activas (answer, hold, transfer)
- Registrar disposicion post-llamada en ``etl_runs`` / CRM
- Exponer dashboard de desempeno propio al operador
- Proveer acceso al buzon de mensajes internos (InternalMailbox)

Funciones RBAC
==============

AGR-011 ``call_center_operator_group`` — 10 funciones:

- OPR-001 ``manage_own_agent_state``
- OPR-002 ``answer_inbound_calls``
- OPR-003 ``make_outbound_calls``
- OPR-004 ``hold_calls``
- OPR-005 ``transfer_calls``
- OPR-006 ``enter_call_disposition``
- OPR-007 ``request_break``
- OPR-008 ``view_own_performance_dashboard``
- OPR-009 ``view_own_call_history``
- OPR-010 ``read_own_mailbox``

Casos de Uso
============

UC_OPR_01..10 — ver :doc:`/requisitos/casos-uso/operator/index`

Dependencias
============

- ARQ_MOD_001 AUTH — sesion JWT obligatoria
- ARQ_MOD_003 RBAC_CORE — verificacion de permisos OPR
- ARQ_MOD_007 AUDIT — registro de acciones del operador
- ARQ_MOD_008 SYS_LOGS — logs de conectividad telefonica

.. toctree::
 :maxdepth: 1

 diagramas
