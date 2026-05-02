.. _modelo-rbac-iact-arquitectura:

=================================
Modelo RBAC IACT — Arquitectura
=================================

2. ARQUITECTURA IACT
====================



2.1 Distribución de 73 Funciones (v5.5.0)
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
   - 5.5%
   - Sesiones y autenticación
 * - MOD_Users
   - USR
   - 9
   - 12.3%
   - Gestión de identidades
 * - MOD_Access
   - ACC
   - 12
   - 16.4%
   - RBAC core + SEC_RULES
 * - MOD_Pipeline
   - PIP
   - 4
   - 5.5%
   - Supervisión ETL
 * - **MOD_Reports**
   - **RPT**
   - **11**
   - **15.1%**
   - **Reportes/Dashboards**
 * - MOD_Alerts
   - ALR
   - 10
   - 13.7%
   - Alertas internas
 * - MOD_Audit
   - AUD
   - 4
   - 5.5%
   - Auditoría funcional
 * - MOD_Logs
   - LOG
   - 7
   - 9.6%
   - Logs técnicos + health + métricas
 * - MOD_Operator
   - OPR
   - 9
   - 12.3%
   - Acciones de agentes call center
 * - MOD_Supervision
   - SUP
   - 3
   - 4.1%
   - Supervisión en tiempo real
 * - **TOTAL**
   - -
   - **73**
   - **100%**
   - -


