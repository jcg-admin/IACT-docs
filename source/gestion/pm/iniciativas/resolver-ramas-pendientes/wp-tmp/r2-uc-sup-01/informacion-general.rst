.. _uc-sup-01-parte-01:

============================================
Parte 1 — Informacion general de UC_SUP_01
============================================

1.1 Identificacion
==================

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **ID UC**
   - UC_SUP_01
 * - **Nombre**
   - Monitorear Llamada (Whisper / Silent)
 * - **Version spec**
   - 5.1.0 (12-partes — profundidad completa)
 * - **Fecha**
   - 2026-05-02
 * - **Autor**
   - NestorMonroy
 * - **Clasificacion**
   - CRITICA (impacto legal + compliance)
 * - **Modulo**
   - MOD_Supervision
 * - **Funcion RBAC canonica**
   - ``SUP-001 monitor_live_calls``

1.2 Proposito
=============

UC_SUP_01 permite a un supervisor escuchar una llamada activa en
dos modos mutuamente excluyentes:

- **silent**: escucha sin intervenir. Ni el agente ni el cliente
  saben que el supervisor está escuchando.
- **whisper**: habla al oído del agente sin que el cliente pueda
  oír. Solo el agente recibe el mensaje del supervisor.

El UC garantiza tres condiciones no negociables:

1. **Función RBAC explícita** — el invocante debe poseer
   ``SUP-001 monitor_live_calls`` (otorgada via AGR-012 o
   asignación directa).
2. **Segmento validado** — el supervisor solo puede monitorear
   agentes de su segmento (CNST-008).
3. **Auditoría obligatoria** — cada monitoreo genera
   ``AuditEvent(CALL_MONITORED)`` con modo, razón, timestamps
   y IDs del supervisor y agente (CNST-025).

.. note::

 **Obligación legal:** El sistema emite un tono audible al agente
 cuando el supervisor activa el modo silent o whisper. Esta
 notificación al agente es requerida por compliance LFPDPPP y
 políticas internas. El cliente **no** recibe ninguna notificación.

1.3 Alcance
===========

1.3.1 IN (incluido)
-------------------

- Activación de sesión de monitoreo en modo ``silent``.
- Activación de sesión de monitoreo en modo ``whisper``.
- Validación de que el call_id corresponde a una llamada activa
  en el segmento del supervisor.
- Validación de justificación (``reason`` ≥ 20 caracteres).
- Puente de audio en TelephonyClient (tripartito en ambos modos).
- Tono de notificación al agente (automático, no omitible).
- Emisión de ``AuditEvent(CALL_MONITORED)`` con detalle completo.
- Response 200 con session_id de monitoreo activo.

1.3.2 OUT (excluido)
--------------------

- Barge-in (conversación tripartita visible al cliente) → UC_SUP_02.
- Envío de mensajes de texto al equipo → UC_SUP_03.
- Terminación de la llamada monitoreada (el supervisor observa,
  no controla).
- Grabación de la llamada (función separada del sistema de
  telefonia; fuera de scope IACT).
- Gestión de SLA/adherencia de agente → pertenece a MOD_Reports.

1.3.3 Posicion en el flujo
--------------------------

UC_SUP_01 es una operación de supervisión **reactiva y continua**:

- El supervisor identifica una llamada de interés (por alertas,
  por métricas de dashboard, o por solicitud directa del agente).
- Activa UC_SUP_01 para observar la interacción.
- Puede escalar a UC_SUP_02 (barge-in) si la situación lo requiere.

No requiere acción previa del agente ni del cliente.

1.4 Trazabilidad
================

.. list-table::
 :widths: 30 70
 :header-rows: 0

 * - **BReq satisfecho**
   - :doc:`/requisitos/business-requirements/breq-006-operacion-continua-sla`
     (BReq-006) — calidad operativa del call center
 * - **Reglas de Negocio**
   - BR-010 (Auditoría Inmutable) — cada monitoreo se registra
     permanentemente. Sin excepción, sin flag de "sin auditoría".
 * - **Restricciones (CNST)**
   - CNST-008 segmento supervisor valida acceso a llamada;
     CNST-009 autenticación;
     CNST-013 manejo de errores;
     CNST-025 auditoría inmutable.
 * - **Funcion RBAC canonica**
   - ``SUP-001 monitor_live_calls`` — otorgada via
     AGR-012 (call_center_supervisor_group) o asignación directa.
     Sin esta función → 403 Forbidden.
 * - **UC Relacionados**
   - UC_SUP_02 (barge-in — escalada desde este UC),
     UC_OPR_02 (el agente monitoreado está en este flujo),
     UC_OPR_10 (el agente puede recibir notificación post-monitoreo)
 * - **Clase primaria**
   - ``MonitorSession`` (escritura — INSERT al iniciar)
 * - **Clases secundarias**
   - ``User`` (lectura — supervisor + agente),
     ``ActiveCall`` (lectura — validar que la llamada existe y
     está activa),
     ``AuditEvent`` (escritura — registro inmutable),
     ``TelephonyClient`` (operación — bridge de audio)
