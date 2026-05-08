.. _modelo-rbac-iact-resumen:

==============================
Modelo RBAC IACT — Resumen
==============================

11. MIGRACIÓN DESDE v5.2.0
==========================



11.1 Cambios Breaking
---------------------



.. list-table::
 :widths: 33 33 33
 :header-rows: 1

 * - Aspecto
   - v5.2.0
   - v5.2.1
 * - **Nombres funciones**
   - Español
   - Inglés
 * - **Nombres grupos**
   - Español con `agr_`
   - Inglés sin prefijo
 * - **Nombres reglas de separacion**
   - Español con `sod_`
   - Inglés sin prefijo
 * - **Campos**
   - `assigned_date`
   - `assigned_at`



11.2 Script de Migración SQL
----------------------------



.. note::

 Los detalles de implementacion de esta operacion estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.

----

12. RESUMEN
===========



12.1 Métricas del Modelo v5.6.0
-------------------------------



.. list-table::
 :widths: 50 50
 :header-rows: 1

 * - Aspecto
   - Valor
 * - **Filosofía**
   - Sin Pretensiones
 * - **Módulos activos (in-scope)**
   - 9 (Auth, Users, Access, Pipeline, Reports, Alerts, Audit, Logs, **Admin**)
 * - **Módulos reservados (open-closed)**
   - 2 (Operator, Supervision)
 * - **Funciones atómicas activas**
   - **64**
 * - **Funciones reservadas**
   - 13
 * - **Total catálogo declarado**
   - 77
 * - **Grupos**
   - 12
  * - **Restricciones de Separacion**
   - 3
 * - **Segmentos de datos**
   - 0
 * - **Restricciones CNST**
   - 8
 * - **Nomenclatura**
   - Inglés (Clean Code v2.0.0)
 * - **Consistencia**
   - 100%



12.2 Cambios Clave v5.2.1
-------------------------


1. **[OK] 100% Inglés en código:**
   - Funciones: ``manage_sessions``, ``view_reports``, ``export_csv``
   - Grupos: ``basic_operator_group``, ``user_admin_group``
   - Reglas de Separacion: ``pipeline_audit_separation``

2. **[OK] Clean Code completo:**
   - Sin prefijos redundantes (``agr_``, ``sod_``)
   - Sin acrónimos en nombres (ETL en descripción OK)
   - Nombres descriptivos completos

3. **[OK] Convenciones SQL:**
   - ``assigned_at`` (NO ``assigned_date``)
   - ``rule_group`` (NO ``separation_group``)

4. **[OK] Comentarios español:**
   - Docstrings en español
   - ``help_text`` en español
   - ``description`` en español

----

**FIN DEL DOCUMENTO**

**Versión:** 5.6.0

**Fecha:** 6 de mayo de 2026

**Estado:** [OK] Listo para Implementación

**Changelog:**

- v5.5.0 → v5.6.0: NUEVO MOD_Admin (3 funciones) que formaliza el plano de configuración RBAC (catálogo, separacion de deberes, asignaciones a grupos del sistema). MOD_Operator y MOD_Supervision reclasificados como reservados open-closed (out-of-scope para esta release).
- v5.4.0 → v5.5.0: alta de MOD_Operator (10) y MOD_Supervision (3) derivados de UC_OPR_01..10 y UC_SUP_01..03 (luego reservados en v5.6.0).
- v5.3.0 → v5.4.0: splits SRP en MOD_Auth, MOD_Users, MOD_Access, MOD_Alerts, MOD_Logs (renames + 5 nuevas en MOD_Logs).
- v5.2.1 → v5.3.0: nuevas funciones en MOD_Access, MOD_Reports y MOD_Logs (custom groups, schedule, comparte, search).
- v5.2.0 → v5.2.1: consistencia 100% inglés en código (funciones, grupos, reglas de separacion); ``assigned_date`` → ``assigned_at``; ``separation_group`` → ``rule_group``.
- Base: Clean Code v2.0.0 + MODELO_RBAC_IACT_v5_1_1.rst
