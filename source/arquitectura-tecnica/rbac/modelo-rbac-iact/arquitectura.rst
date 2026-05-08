.. _modelo-rbac-iact-arquitectura:

=================================
Modelo RBAC IACT — Arquitectura
=================================

2. ARQUITECTURA IACT
====================



2.1 Distribución de 64 Funciones Activas (v5.6.0)
-------------------------------------------------



In-scope para esta release. 9 modulos activos.

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
   - 6.3%
   - Sesiones y autenticación
 * - MOD_Users
   - USR
   - 9
   - 14.1%
   - Gestión de identidades
 * - MOD_Access
   - ACC
   - 12
   - 18.8%
   - RBAC core + SEC_RULES
 * - MOD_Pipeline
   - PIP
   - 4
   - 6.3%
   - Supervisión ETL
 * - **MOD_Reports**
   - **RPT**
   - **11**
   - **17.2%**
   - **Reportes/Dashboards**
 * - MOD_Alerts
   - ALR
   - 10
   - 15.6%
   - Alertas internas
 * - MOD_Audit
   - AUD
   - 4
   - 6.3%
   - Auditoría funcional
 * - MOD_Logs
   - LOG
   - 7
   - 10.9%
   - Logs técnicos + health + métricas
 * - **MOD_Admin** (NUEVO v5.6.0)
   - **ADM**
   - **3**
   - **4.7%**
   - **Plano de configuración RBAC (catálogo, separacion de deberes, asignaciones a grupos del sistema)**
 * - **TOTAL ACTIVO**
   - -
   - **64**
   - **100%**
   - -


2.2 Extension Points Reservados (open-closed)
---------------------------------------------



Out-of-scope para esta release. Declarados en el catálogo como
puntos de extensión: el set activo está cerrado para modificación,
abierto para extensión a estos dos módulos cuando se decida
activarlos.

.. list-table::
 :widths: 20 20 20 40
 :header-rows: 1

 * - Módulo
   - Código
   - Funciones
   - Propósito
 * - MOD_Operator
   - OPR
   - 10
   - Acciones de agentes call center (UC_OPR_01..10) —
     reservado, no implementable en v5.6.0
 * - MOD_Supervision
   - SUP
   - 3
   - Supervisión en tiempo real (UC_SUP_01..03) —
     reservado, no implementable en v5.6.0
 * - **TOTAL RESERVADO**
   - -
   - **13**
   - -


2.3 Total catálogo declarado
----------------------------



**77 funciones** = 64 activas + 13 reservadas. El conteo total
sirve para dimensionar el catálogo cuando se referencia el modelo
completo; las afirmaciones operativas (instalación, RBAC enforcement,
RACI) usan el set activo de **64**.


