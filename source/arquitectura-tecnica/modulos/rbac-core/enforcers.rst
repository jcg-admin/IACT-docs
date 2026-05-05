.. _arq-mod-003-enforcers:

================================================
ARQ_MOD_003 — Enforcers de Seguridad
================================================

Los enforcers aplican **automaticamente** las restricciones criticas del sistema.
Son parte integral del RBAC_CORE (anteriormente denominados SEC_RULES).

.. list-table::
 :widths: 30 25 45
 :header-rows: 1

 * - Enforcer
   - Tipo
   - Restriccion que Aplica
 * - NoEmailEnforcer
   - Middleware
   - CNST_001: Bloquea cualquier intento de enviar email
 * - ReadOnlyIVREnforcer
   - DB Router
   - CNST_003: BD IVR solo lectura
 * - NoRealTimeEnforcer
   - Middleware
   - CNST_003: Bloquea WebSockets, SSE
 * - SessionDBEnforcer
   - Middleware
   - CNST_002: Sesiones en base de datos relacional
 * - ExportLimitEnforcer
   - Decorator
   - CNST_007: Limites de exportacion
 * - ThrottlingEnforcer
   - Middleware
   - CNST_007: Rate limiting
