.. meta::
 :artefacto: FR-031.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/operator
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-031-01:

=================================================================
FR-031.01: Leer y gestionar mensajes del buzón interno del agente
=================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-031.01
 * - **Nombre**
   - Leer y gestionar mensajes del buzón interno del agente
 * - **UC Origen**
   - UC_OPR_10: Leer Buzón Interno
 * - **Paso UC**
   - Pasos 1-5 del flujo principal (lectura y marcar leído)
 * - **Módulo**
   - MOD_Operator
 * - **Prioridad**
   - Alta
 * - **Tipo**
   - Funcional

----

2. Especificación
-----------------

**Declaración:**

 El sistema DEBE retornar los mensajes del buzón interno del agente autenticado CUANDO los solicita, y permitir marcarlos como leídos CUANDO el agente confirma la lectura.

**Descripción:**

 Lectura: valida JWT, query MailboxRepo WHERE recipient = invoker.id filtrado por status. Retorna lista de mensajes (sin PII del remitente según CNST-026). Marcar leído: POST /{id}/read/ → UPDATE status=read + AuditEvent. La comunicación exclusivamente por buzón interno (CNST-001 prohíbe email externo).

----

3. Criterio de Aceptación
-------------------------

::

 DADO un agente solicita su bandeja de entrada
 CUANDO GET /api/me/inbox/
 ENTONCES 200 con lista de mensajes filtrados por status
 
 Escenario 1: Con mensajes no leídos
 DADO 3 mensajes con status=unread
 ENTONCES lista de 3 mensajes
 
 Escenario 2: Marcar como leído
 DADO POST /{id}/read/
 ENTONCES UPDATE status=read + AuditEvent

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-001, CNST-002, CNST-009, CNST-025, CNST-026

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-007
 * - **UC**
   - UC_OPR_10: Leer Buzón Interno
 * - **Depende de**
   - Ninguno
 * - **Requerido por**
   - Ninguno
 * - **TEST**
   - TST-fr-031-01 (pendiente)

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
   - Versión inicial derivada de UC_OPR_10
