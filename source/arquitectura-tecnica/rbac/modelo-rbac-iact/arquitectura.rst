.. _modelo-rbac-iact-arquitectura:

=================================
Modelo RBAC IACT — Arquitectura
=================================

2. ARQUITECTURA IACT
====================



2.1 Distribución de 74 Funciones (v5.5.0)
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
   - 5.4%
   - Sesiones y autenticación
 * - MOD_Users
   - USR
   - 9
   - 12.2%
   - Gestión de identidades
 * - MOD_Access
   - ACC
   - 12
   - 16.2%
   - RBAC core + SEC_RULES
 * - MOD_Pipeline
   - PIP
   - 4
   - 5.4%
   - Supervisión ETL
 * - **MOD_Reports**
   - **RPT**
   - **11**
   - **14.9%**
   - **Reportes/Dashboards**
 * - MOD_Alerts
   - ALR
   - 10
   - 13.5%
   - Alertas internas
 * - MOD_Audit
   - AUD
   - 4
   - 5.4%
   - Auditoría funcional
 * - MOD_Logs
   - LOG
   - 7
   - 9.5%
   - Logs técnicos + health + métricas
 * - MOD_Operator
   - OPR
   - 10
   - 13.5%
   - Acciones de agentes call center
 * - MOD_Supervision
   - SUP
   - 3
   - 4.1%
   - Supervisión en tiempo real
 * - **TOTAL**
   - -
   - **74**
   - **100%**
   - -


