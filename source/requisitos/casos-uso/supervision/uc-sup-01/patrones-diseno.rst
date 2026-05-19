.. _uc-sup-01-parte-10:

==========================================
Parte 10 — Patrones de diseño aplicados
==========================================

10.1 Patrones de diseño aplicados en UC_SUP_01
================================================

P-15 — Transactional Outbox (audit + session atómica)
-------------------------------------------------------

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Patrón**
   - Transactional Outbox / Unit of Work.
 * - **Aplicación en UC_SUP_01**
   - ``MonitorSession`` (INSERT) y ``AuditEvent(CALL_MONITORED)``
     (INSERT) se crean dentro de la misma transacción de BD
     (PASOS 8 + 11 — ver 3.3 Atomicidad en flujo-principal).
 * - **Beneficio**
   - Garantía de consistencia: si la sesión existe, el audit trail
     existe. Imposible tener una sesión de monitoreo sin registro
     de auditoría ni viceversa.
 * - **Compensación post-commit**
   - El bridge de audio (PASO 9) se activa post-COMMIT.
     Si falla, se escribe ``MONITOR_FAILED`` en un segundo
     commit de compensación — el estado de la sesión refleja
     la realidad del sistema.

----

P-32 — Guard Clause / Early Return
------------------------------------

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Patrón**
   - Guard Clauses en el handler del endpoint.
 * - **Aplicación en UC_SUP_01**
   - Los PASOS 3-7 son validaciones en cascada: JWT → SUP-001
     → segmento → llamada activa → reason. Cada validación
     fallida retorna inmediatamente con el error apropiado
     sin llegar a crear registros en BD.
 * - **Beneficio**
   - Código lineal, legible. Sin anidamiento de ifs.
     Cada error tiene un único punto de salida.

----

P-39 — Separation of Concerns (AuthGuard / SegmentFilter / Handler)
---------------------------------------------------------------------

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Patrón**
   - Middleware chain con responsabilidades separadas.
 * - **Aplicación en UC_SUP_01**
   - ``AuthGuard``: JWT + RBAC (``SUP-001``).
   - ``SegmentFilter``: validación de segmento (CNST-008).
   - ``MonitorEndpoint`` handler: lógica de negocio (PASOS 6-12).
   - ``TelephonyClient``: abstracción del sistema externo.
   - ``AuditService`` (implícito): escritura de ``AuditEvent``.
 * - **Beneficio**
   - Cada componente es testeable en aislamiento.
     ``SegmentFilter`` se puede cambiar sin tocar el handler.
     ``TelephonyClient`` se puede mockear en tests.

----

P-88 — Mandatory Audible Notification on Monitoring (nuevo)
-------------------------------------------------------------

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Patrón**
   - Compliance hook — notificación obligatoria no-omitible.
 * - **Aplicación en UC_SUP_01**
   - El PASO 10 (tono audible al agente) es parte del flujo
     principal y del flujo de switch de modo (FA-01).
     No existe flag de configuración para desactivarlo.
     Si el tono falla, el bridge no se activa (EX-07).
 * - **Justificación legal**
   - LFPDPPP y política interna requieren que el agente
     sepa que está siendo supervisado. El cliente NO es
     notificado (supervisión interna de calidad).
 * - **Propagación**
   - Este patrón aplica también a UC_SUP_02 (barge-in).
     Todo UC que establezca presencia del supervisor en
     el canal del agente DEBE emitir la notificación audible.
 * - **Documentación canónica**
   - Referenciado desde UC_SUP_01 y UC_SUP_02.
     La regla de negocio raíz es BR-010 (auditoría inmutable)
     y la obligación legal LFPDPPP sección aplicable.

10.2 Patrones NO aplicados (y por qué)
========================================

.. list-table::
 :widths: 30 70
 :header-rows: 1

 * - Patrón descartado
   - Razón
 * - **Event Sourcing**
   - La sesión de monitoreo no requiere reconstrucción de
     estado desde eventos. El estado actual en BD es
     suficiente. Los ``AuditEvent`` son el trail, no la
     fuente de estado.
 * - **Saga / compensating transactions**
   - El rollback por fallo de telefonía (EX-07) es simple:
     marcar la sesión como ``FAILED``. No hay pagos ni
     recursos distribuidos que requieran saga compleja.
 * - **CQRS**
   - El volumen de lecturas y escrituras de ``MonitorSession``
     no justifica la complejidad de CQRS en este UC.
     Las consultas de auditoría usan ``AuditEvent`` directamente.
