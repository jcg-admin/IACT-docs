.. meta::
 :artefacto: FR-077.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/supervision
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-077-01:

=========================================================================
FR-077.01: Enviar mensaje masivo por buzón interno a agentes del segmento
=========================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-077.01
 * - **Nombre**
   - Enviar mensaje masivo por buzón interno a agentes del segmento
 * - **UC Origen**
   - UC_SUP_03: Enviar Mensaje Masivo al Equipo
 * - **Paso UC**
   - Pasos 1-8 del flujo principal
 * - **Módulo**
   - MOD_Supervision
 * - **Prioridad**
   - Alta
 * - **Tipo**
   - Funcional

----

2. Especificación
-----------------

**Declaración:**

 El sistema DEBE enviar un mensaje masivo por buzón interno CUANDO un supervisor lo solicita, resolviendo la lista de destinatarios por segmento y usando push SSE para mensajes urgentes.

**Descripción:**

 Valida JWT + RBAC. Valida que target ⊆ segmentos del supervisor. Resuelve lista de recipients (agentes en el segmento/AGR objetivo). Bulk INSERT MailboxMessage por cada recipient. Si urgente: push SSE a los receptores activos. Audit BROADCAST_SENT con count.

----

3. Criterio de Aceptación
-------------------------

::

 DADO supervisor envía alerta urgente al equipo
 CUANDO POST con message y target=agr_team_alpha
 ENTONCES 200 + N mensajes insertados + SSE push a conectados
 
 Escenario 1: Mensaje urgente
 DADO urgent=true
 ENTONCES SSE push inmediato + BROADCAST_SENT count=N
 
 Escenario 2: Target fuera de segmento
 DADO AGR en segmento no asignado
 ENTONCES 403

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-008, CNST-009, CNST-013, CNST-025

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-007
 * - **UC**
   - UC_SUP_03: Enviar Mensaje Masivo al Equipo
 * - **TEST**
   - TST-fr-077-01 (pendiente)

----

6. Historial
------------

.. list-table::
 :widths: 15 15 70
 :header-rows: 1

 * - Versión
   - Fecha
   - Cambio
 * - 1.0.0
   - 2026-05-04
   - Versión inicial derivada de UC_SUP_03
