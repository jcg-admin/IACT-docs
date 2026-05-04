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
 * - **Nombres reglas SoD**
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



12.1 Métricas del Modelo v5.5.0
-------------------------------



.. list-table::
 :widths: 50 50
 :header-rows: 1

 * - Aspecto
   - Valor
 * - **Filosofía**
   - Sin Pretensiones
 * - **Módulos IACT**
   - 11
 * - **Funciones atómicas**
   - 74
 * - **Grupos**
   - 12
 * - **Restricciones SoD**
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
   - Reglas SoD: ``pipeline_audit_separation``

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

**Versión:** 5.2.1 
**Fecha:** 13 de enero de 2026 
**Estado:** [OK] Listo para Implementación 
**Changelog:**
- v5.2.0 → v5.2.1: Consistencia 100% inglés en código
- Nombres funciones: español → inglés
- Nombres grupos: español + ``agr_`` → inglés sin prefijo
- Nombres reglas SoD: español + ``sod_`` → inglés sin prefijo
- Campos: ``assigned_date`` → ``assigned_at``, ``separation_group`` → ``rule_group``
- Base: Clean Code v2.0.0 + MODELO_RBAC_IACT_v5_1_1.rst
