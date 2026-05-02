.. _modelo-rbac-iact-arquitectura:

=================================
Modelo RBAC IACT — Arquitectura
=================================

2. ARQUITECTURA IACT
====================



2.1 Distribución de 61 Funciones (v5.4.0)
-----------------------------------------



.. list-table::
 :widths: 20 20 20 20 20
 :header-rows: 1

 * - Módulo
   - Código
   - Funciones
   - %
   - Propósito
 * - MOD_Auth
   - AUTH
   - 4
   - 6.6%
   - Sesiones y autenticación
 * - MOD_Users
   - USR
   - 9
   - 14.8%
   - Gestión de identidades
 * - MOD_Access
   - ACC
   - 12
   - 19.7%
   - RBAC core + SEC_RULES
 * - MOD_Pipeline
   - PIP
   - 4
   - 6.6%
   - Supervisión ETL
 * - **MOD_Reports**
   - **RPT**
   - **11**
   - **18.0%**
   - **Reportes/Dashboards**
 * - MOD_Alerts
   - ALR
   - 10
   - 16.4%
   - Alertas internas
 * - MOD_Audit
   - AUD
   - 4
   - 6.6%
   - Auditoría funcional
 * - MOD_Logs
   - LOG
   - 7
   - 11.5%
   - Logs técnicos + health + métricas
 * - **TOTAL**
   - -
   - **61**
   - **100%**
   - -


