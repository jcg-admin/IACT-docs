.. meta::
 :artefacto: DIAGRAMAS_UC_POR_MODULO_IACT
 :tipo: Diagramas UC por Modulo
 :dominio: arquitectura_tecnica
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-02
 :ultimo_cambio: 2026-05-02
 :autor: NestorMonroy
 :clasificacion: Interno

.. _diagramas-uc-por-modulo:

===============================
Diagramas UC por Modulo — IACT
===============================

Un diagrama de casos de uso por cada modulo funcional del sistema IACT.
Los actores se nombran por su funcion RBAC en ingles. Cada UC referencia
su especificacion completa en
:doc:`/requisitos/casos-uso/index`.

----

MOD_Auth — Autenticacion y Sesiones
=====================================

Gestiona el ciclo de vida de la sesion del usuario: login, logout,
recuperacion y cambio de contrasena, y gestion de sesiones activas.

.. uml::
 :caption: Figura 16 — MOD_Auth: casos de uso

 @startuml
 left to right direction

 actor "User\n(no autenticado)" as UNAUTH
 actor "User\n(autenticado)" as AUTH
 actor "view_all_active_sessions" as SESS_ADM

 rectangle "MOD_Auth" {
   usecase "UC_AUTH_01\nIniciar Sesion" as A01
   usecase "UC_AUTH_02\nCerrar Sesion" as A02
   usecase "UC_AUTH_03\nRecuperar Contrasena" as A03
   usecase "UC_AUTH_04\nCambiar Contrasena" as A04
   usecase "UC_AUTH_05\nGestionar Sesiones" as A05
   usecase "UC_PERM_08\nGenerar Menu Dinamico\n[view_own_navigation]" as P08
 }

 UNAUTH --> A01
 UNAUTH --> A03
 AUTH --> A02
 AUTH --> A04
 SESS_ADM --> A05
 A01 ..> P08 : <<include>>

 @enduml

----

MOD_Users — Gestion de Usuarios
==================================

Altas, consultas, modificaciones y bajas logicas de usuarios IACT.
Solo usuarios con ``create_users`` o ``update_users`` pueden modificar.

.. uml::
 :caption: Figura 17 — MOD_Users: casos de uso

 @startuml
 left to right direction

 actor "create_users" as CU
 actor "update_users" as UU
 actor "deactivate_users" as DU
 actor "list_users" as LU

 rectangle "MOD_Users" {
   usecase "UC_USR_01\nCrear Usuario" as U01
   usecase "UC_USR_02\nConsultar Usuarios" as U02
   usecase "UC_USR_03\nModificar Usuario" as U03
   usecase "UC_USR_04\nEliminar Usuario\n(baja logica)" as U04
 }

 CU --> U01
 LU --> U02
 UU --> U02
 UU --> U03
 DU --> U04
 DU --> U02

 @enduml

----

MOD_Access — Asignacion de Accesos
=====================================

Vista funcional del RBAC: asignar y revocar funciones individuales,
gestionar agrupadores y reglas SoD. Coexiste con MOD_Permissions
(Hipotesis 1 — decision arquitectonica aprobada).

.. uml::
 :caption: Figura 18 — MOD_Access: casos de uso

 @startuml
 left to right direction

 actor "assign_functions" as AF
 actor "revoke_functions" as RF
 actor "view_assignments" as VA
 actor "assign_function_groups" as AFG
 actor "view_separation_rules" as VSR
 actor "view_audit_log" as VAA

 rectangle "MOD_Access" {
   usecase "UC_ACC_01\nAsignar Funciones\na Usuario" as AC01
   usecase "UC_ACC_02\nRevocar Funciones\nde Usuario" as AC02
   usecase "UC_ACC_03\nConsultar Permisos\nEfectivos" as AC03
   usecase "UC_ACC_04\nAsignar Agrupador\na Usuario" as AC04
   usecase "UC_ACC_05\nGestionar Reglas SoD" as AC05
   usecase "UC_ACC_08\nOtorgar Permiso\nTemporal Excepcional" as AC08
   usecase "UC_ACC_09\nAuditar Cambios\nde Acceso" as AC09
 }

 AF --> AC01
 AF --> AC08
 RF --> AC02
 VA --> AC03
 AFG --> AC04
 VSR --> AC05
 VAA --> AC09
 VA --> AC09

 AC08 ..> AC01 : <<extend>>

 @enduml

----

MOD_Permissions — Gestion Granular de Permisos
================================================

Vista tecnica del RBAC: gestion de grupos de permisos, funciones a
grupos, verificacion efectiva y generacion del menu dinamico basado
en ``effective_set``.

.. uml::
 :caption: Figura 19 — MOD_Permissions: casos de uso

 @startuml
 left to right direction

 actor "assign_function_groups" as AFG
 actor "revoke_function_group" as RFG
 actor "create_function_group" as MAG
 actor "assign_functions_to_group" as MAGC
 actor "view_assignments" as VA
 actor "view_audit_log" as AUD
 actor "User\n(autenticado)" as AUTH

 rectangle "MOD_Permissions" {
   usecase "UC_PERM_01\nAsignar Grupo\na Usuario" as P01
   usecase "UC_PERM_02\nRevocar Grupo\na Usuario" as P02
   usecase "UC_PERM_03\nConceder Permiso\nExcepcional" as P03
   usecase "UC_PERM_04\nRevocar Permiso\nExcepcional" as P04
   usecase "UC_PERM_05\nCrear / Modificar /\nRetirar Grupo" as P05
   usecase "UC_PERM_06\nAsignar Funciones\na Grupo" as P06
   usecase "UC_PERM_07\nVerificar Permiso\nde Usuario" as P07
   usecase "UC_PERM_08\nGenerar Menu\nDinamico\n[view_own_navigation]" as P08
   usecase "UC_PERM_09\nAuditar Acceso\n(write side)" as P09
   usecase "UC_PERM_10\nConsultar Auditoria\nde Permisos" as P10
 }

 AFG --> P01
 RFG --> P02
 AFG --> P03
 AFG --> P04
 MAG --> P05
 MAGC --> P06
 VA --> P07
 AUTH --> P08
 AUD --> P10

 P01 ..> P09 : <<include>>
 P02 ..> P09 : <<include>>
 P03 ..> P09 : <<include>>
 P04 ..> P09 : <<include>>
 P06 ..> P09 : <<include>>
 P08 ..> P07 : <<include>>

 @enduml

----

MOD_Reports — Reportes IVR
=============================

Modulo principal de analisis. 16 UCs de reporte + 1 UC <<include>>
compartido (Resolver Segmento). Todos los reportes filtran datos
por segmento IVR del usuario via ``UC_INC_RPT_01``.

.. uml::
 :caption: Figura 20 — MOD_Reports: casos de uso

 @startuml
 left to right direction

 actor "view_dashboard" as VD
 actor "view_kpis" as VK
 actor "view_reports" as VR
 actor "export_csv\n(export_pdf/excel)" as EXP
 actor "schedule_report" as SRPT
 actor "save_view" as SV
 actor "share_report" as SHR

 rectangle "MOD_Reports" {
   usecase "UC_INC_RPT_01\nResolver Segmento" as INC
   usecase "UC_RPT_01\nVer Dashboard IVR" as R01
   usecase "UC_RPT_02\nVer Metricas\nTiempo Real" as R02
   usecase "UC_RPT_03\nVer Reportes\nHistoricos" as R03
   usecase "UC_RPT_04\nExportar Reporte" as R04
   usecase "UC_RPT_07\nProgramar Reporte" as R07
   usecase "UC_RPT_08\nVer Reportes\nProgramados" as R08
   usecase "UC_RPT_10\nGuardar Vista" as R10
   usecase "UC_RPT_11\nCompartir Reporte" as R11
   usecase "UC_RPT_12\nReporte de Agentes\n(sp_rpt_centros_xsegmento)" as R12
   usecase "UC_RPT_13\nReporte de Colas\n(sp_rpt_llamadas_abandonadas)" as R13
   usecase "UC_RPT_14\nReporte de Campanas" as R14
   usecase "UC_RPT_15\nReporte de\nTransferencias\n(sp_rpt_centros_transferencia)" as R15
   usecase "UC_RPT_16\nReporte de Menus IVR\n(sp_rpt_menu_redirigidos)" as R16
   usecase "UC_RPT_17\nReporte de Clientes\nUnicos\n(sp_rpt_clientes)" as R17
 }

 VD --> R01
 VK --> R02
 VR --> R03
 EXP --> R04
 SRPT --> R07
 SRPT --> R08
 SV --> R10
 SHR --> R11
 VR --> R12
 VR --> R13
 VR --> R14
 VR --> R15
 VR --> R16
 VR --> R17

 R01 ..> INC : <<include>>
 R02 ..> INC : <<include>>
 R03 ..> INC : <<include>>
 R12 ..> INC : <<include>>
 R13 ..> INC : <<include>>
 R14 ..> INC : <<include>>
 R15 ..> INC : <<include>>
 R16 ..> INC : <<include>>
 R17 ..> INC : <<include>>

 R03 ..> R04 : <<extend>>
 R03 ..> R07 : <<extend>>

 @enduml

----

MOD_Alerts — Alertas y Notificaciones
========================================

Configuracion de umbrales criticos, recepcion y reconocimiento de
alertas del sistema IVR (BR-016: tasa de abandono >30%). Las alertas
se generan automaticamente por el motor de alertas y por el ETL.

.. uml::
 :caption: Figura 21 — MOD_Alerts: casos de uso

 @startuml
 left to right direction

 actor "configure_team_alerts" as MAT
 actor "view_alerts" as VAA
 actor "acknowledge_alert" as ACA
 actor "view_alert_history" as VAH

 rectangle "MOD_Alerts" {
   usecase "UC_ALR_01\nConfigurar Umbrales\nde Alertas" as AL01
   usecase "UC_ALR_02\nVer Alertas Activas" as AL02
   usecase "UC_ALR_03\nReconocer Alerta" as AL03
   usecase "UC_ALR_04\nVer Historial\nde Alertas" as AL04
   usecase "UC_ALR_05\nNotificacion\nAutomatica ETL" as AL05
   usecase "Motor de Alertas\n(automatico)" as MOTOR
 }

 MAT --> AL01
 VAA --> AL02
 ACA --> AL03
 VAH --> AL04
 MOTOR --> AL05

 AL02 ..> AL03 : <<extend>>
 AL05 ..> AL02 : <<extend>>
 AL01 ..> MOTOR : <<include>>

 @enduml

----

MOD_Pipeline — Gestion del ETL
=================================

Supervision, monitoreo y reintento del pipeline ETL IVR. El ETL
transforma los datos del Repositorio IVR a la Base Analitica IVR
via ``sp_etl_maestro``. El registro de ejecuciones vive en ``etl_runs``.

.. uml::
 :caption: Figura 22 — MOD_Pipeline: casos de uso

 @startuml
 left to right direction

 actor "view_pipeline_status" as VEE
 actor "view_pipeline_errors" as VEER
 actor "view_data_availability" as VDD
 actor "request_pipeline_retry" as RE
 actor "APScheduler\n/ Cron" as SCH

 rectangle "MOD_Pipeline" {
   usecase "UC_PIP_01\nVer Estado ETL\n(etl_runs)" as P01
   usecase "UC_PIP_02\nVer Errores ETL\n(etl_runs.estado=fallido)" as P02
   usecase "UC_PIP_03\nVer Disponibilidad\nde Datos" as P03
   usecase "UC_PIP_04\nReintentar ETL\n(sp_etl_historico)" as P04
   usecase "Ejecutar ETL\nAutomatico\n(sp_etl_maestro)" as AUTO
 }

 VEE --> P01
 VEER --> P02
 VDD --> P03
 RE --> P04
 SCH --> AUTO

 P01 ..> P02 : <<extend>>
 P04 ..> P01 : <<include>>
 AUTO ..> P01 : <<extend>>

 @enduml

----

MOD_Audit — Auditoria de Acciones
=====================================

Consulta inmutable del registro de acciones de modificacion en
``audit_log`` (PostgreSQL). Cubre altas/bajas de usuarios, cambios
RBAC, disparos de ETL y cualquier accion de escritura.

.. uml::
 :caption: Figura 23 — MOD_Audit: casos de uso

 @startuml
 left to right direction

 actor "view_audit_log" as VGA
 actor "search_audit_log" as SA
 actor "export_audit_log" as EA
 actor "generate_compliance_report" as GCR

 rectangle "MOD_Audit" {
   usecase "UC_AUD_01\nVer Auditoria\nGeneral" as A01
   usecase "UC_AUD_02\nBuscar en\nAuditoria" as A02
   usecase "UC_AUD_03\nExportar\nAuditoria" as A03
   usecase "UC_AUD_04\nGenerar Reporte\nCompliance" as A04
 }

 VGA --> A01
 SA --> A02
 EA --> A03
 GCR --> A04

 A01 ..> A02 : <<extend>>
 A02 ..> A03 : <<extend>>
 A04 ..> A02 : <<include>>

 @enduml

----

MOD_Logs — Consulta de Logs
==============================

Acceso a los logs operativos del sistema: logs de aplicacion, ETL,
infraestructura, estado del sistema y metricas tecnicas. Distintas
funciones RBAC controlan que tipo de log puede ver cada usuario.

.. uml::
 :caption: Figura 24 — MOD_Logs: casos de uso

 @startuml
 left to right direction

 actor "view_application_logs" as VSL
 actor "view_etl_logs" as VEL
 actor "search_logs" as SL
 actor "export_logs" as EL
 actor "view_infrastructure_logs" as VIL
 actor "view_system_health" as VSS
 actor "view_technical_metrics" as VTM

 rectangle "MOD_Logs" {
   usecase "UC_LOG_01\nVer Logs\ndel Sistema" as L01
   usecase "UC_LOG_02\nVer Logs ETL\n(etl_runs)" as L02
   usecase "UC_LOG_03\nBuscar Logs" as L03
   usecase "UC_LOG_04\nExportar Logs" as L04
   usecase "UC_LOG_05\nVer Logs de\nInfraestructura" as L05
   usecase "UC_LOG_06\nVer Estado\ndel Sistema" as L06
   usecase "UC_LOG_07\nVer Metricas\nTecnicas" as L07
 }

 VSL --> L01
 VEL --> L02
 SL --> L03
 EL --> L04
 VIL --> L05
 VSS --> L06
 VTM --> L07

 L01 ..> L03 : <<extend>>
 L02 ..> L03 : <<extend>>
 L03 ..> L04 : <<extend>>

 @enduml

----

MOD_Operator — Panel del Operador
====================================

Funcionalidades del agente de call center: cambio de estado,
atencion y transferencia de llamadas, disposicion, breaks y
consulta de estadisticas personales.

.. uml::
 :caption: Figura 25 — MOD_Operator: casos de uso

 @startuml
 left to right direction

 actor "manage_own_agent_state" as MGS
 actor "answer_inbound_calls" as AIC
 actor "make_outbound_calls" as MOC
 actor "hold_calls" as HC
 actor "transfer_calls" as TC
 actor "enter_call_disposition" as ECD
 actor "request_break" as RBK
 actor "view_own_performance_dashboard" as VOPD
 actor "view_own_call_history" as VOCH
 actor "read_own_mailbox" as ROM

 rectangle "MOD_Operator" {
   usecase "UC_OPR_01\nCambiar Estado\ndel Agente" as O01
   usecase "UC_OPR_02\nAtender Llamada\nEntrante" as O02
   usecase "UC_OPR_03\nIniciar Llamada\nOutbound" as O03
   usecase "UC_OPR_04\nHold/Unhold\nLlamada" as O04
   usecase "UC_OPR_05\nTransferir\nLlamada" as O05
   usecase "UC_OPR_06\nDisposicion\npost-Llamada" as O06
   usecase "UC_OPR_07\nTomar Break" as O07
   usecase "UC_OPR_08\nVer Dashboard\nde Desempeno" as O08
   usecase "UC_OPR_09\nVer Historial\nde Llamadas" as O09
   usecase "UC_OPR_10\nVer Buzon\nde Mensajes" as O10
 }

 MGS --> O01
 AIC --> O02
 MOC --> O03
 HC --> O04
 TC --> O05
 ECD --> O06
 RBK --> O07
 VOPD --> O08
 VOCH --> O09
 ROM --> O10

 O02 ..> O01 : <<include>>
 O06 ..> O02 : <<include>>
 O04 ..> O02 : <<include>>
 O05 ..> O02 : <<include>>

 @enduml

----

MOD_Supervision — Supervision en Vivo
========================================

Monitoreo en tiempo real de llamadas activas, intervencion de
supervisor y comunicacion con el equipo de agentes. Requiere
funciones de supervision especificas.

.. uml::
 :caption: Figura 26 — MOD_Supervision: casos de uso

 @startuml
 left to right direction

 actor "monitor_live_calls" as MLC
 actor "barge_in_calls" as BIC
 actor "broadcast_team_messages" as BTM

 rectangle "MOD_Supervision" {
   usecase "UC_SUP_01\nMonitorear Llamadas\nen Vivo" as S01
   usecase "UC_SUP_02\nIntervenir en\nLlamada\n(barge in)" as S02
   usecase "UC_SUP_03\nEnviar Mensaje\nal Equipo" as S03
 }

 MLC --> S01
 BIC --> S02
 BTM --> S03

 S02 ..> S01 : <<include>>

 @enduml

----

MOD_Caller — Experiencia del Cliente IVR
==========================================

Comportamiento del cliente (llamante externo) dentro del flujo
IVR: llamar, navegar menus, esperar en cola, recibir callback y
responder encuesta CSAT post-llamada.

.. uml::
 :caption: Figura 27 — MOD_Caller: casos de uso

 @startuml
 left to right direction

 actor "Caller\n(externo)" as CALLER

 rectangle "MOD_Caller" {
   usecase "UC_CLI_01\nLlamar al\nSistema IVR" as C01
   usecase "UC_CLI_02\nNavegar Menu\nIVR" as C02
   usecase "UC_CLI_03\nEsperar en Cola\nde Atencion" as C03
   usecase "UC_CLI_04\nRecibir\nCallback" as C04
   usecase "UC_CLI_05\nResponder Encuesta\nCSAT post-llamada\n[offer_csat_post_call]" as C05
 }

 CALLER --> C01
 CALLER --> C02
 CALLER --> C03
 CALLER --> C04
 CALLER --> C05

 C01 ..> C02 : <<include>>
 C02 ..> C03 : <<extend>>
 C03 ..> C04 : <<extend>>
 C05 ..> C01 : <<include>>

 @enduml

----

Vista Consolidada — Todas las Funciones RBAC por Modulo
=========================================================

Mapa de funciones RBAC del sistema IACT y los modulos que
las requieren. Referencia cruzada entre UC y funcion RBAC.

.. uml::
 :caption: Figura 28 — Mapa de funciones RBAC por modulo

 @startuml

 package "MOD_Auth" {
   artifact "view_all_active_sessions" as F_SESS
 }

 package "MOD_Users" {
   artifact "create_users" as F_CU
   artifact "list_users" as F_LU
   artifact "update_users" as F_UU
   artifact "deactivate_users" as F_DU
 }

 package "MOD_Access / MOD_Permissions" {
   artifact "assign_functions" as F_AF
   artifact "revoke_functions" as F_RF
   artifact "view_assignments" as F_VA
   artifact "assign_function_groups" as F_AFG
   artifact "revoke_function_group" as F_RFG
   artifact "create_function_group" as F_MAG
   artifact "assign_functions_to_group" as F_MAGC
   artifact "view_separation_rules" as F_VSR
   artifact "view_audit_log" as F_VAA
   artifact "view_own_navigation" as F_VON
 }

 package "MOD_Reports" {
   artifact "view_dashboard" as F_VD
   artifact "view_reports" as F_VR
   artifact "view_kpis" as F_VK
   artifact "view_charts" as F_VCH
   artifact "filter_reports" as F_FR
   artifact "export_csv" as F_ECSV
   artifact "export_excel" as F_EXL
   artifact "export_pdf" as F_EPDF
   artifact "schedule_report" as F_SCH
   artifact "save_view" as F_SV
   artifact "share_report" as F_SHR
 }

 package "MOD_Pipeline" {
   artifact "view_pipeline_status" as F_VEE
   artifact "view_pipeline_errors" as F_VEER
   artifact "view_data_availability" as F_VDD
   artifact "request_pipeline_retry" as F_RE
 }

 package "MOD_Alerts" {
   artifact "configure_team_alerts" as F_MAT
   artifact "view_alerts" as F_VAA2
   artifact "acknowledge_alert" as F_ACA
   artifact "view_alert_history" as F_VAH
 }

 package "MOD_Audit / MOD_Logs" {
   artifact "view_audit_log" as F_VGA
   artifact "search_audit_log" as F_SA
   artifact "export_audit_log" as F_EA
   artifact "generate_compliance_report" as F_GCR
   artifact "view_application_logs" as F_VSL
   artifact "view_etl_logs" as F_VEL
   artifact "search_logs" as F_SL
   artifact "export_logs" as F_EL
   artifact "view_infrastructure_logs" as F_VIL
   artifact "view_system_health" as F_VSS
   artifact "view_technical_metrics" as F_VTM
 }

 package "MOD_Supervision" {
   artifact "monitor_live_calls" as F_MLC
   artifact "barge_in_calls" as F_BIC
   artifact "broadcast_team_messages" as F_BTM
 }

 package "MOD_Operator" {
   artifact "manage_own_agent_state" as F_MOAS
   artifact "answer_inbound_calls" as F_AIC
   artifact "make_outbound_calls" as F_MOC
   artifact "hold_calls" as F_HC
   artifact "transfer_calls" as F_TC
   artifact "enter_call_disposition" as F_ECD
   artifact "request_break" as F_RBK
   artifact "view_own_performance_dashboard" as F_VOPD
   artifact "view_own_call_history" as F_VOCH
   artifact "read_own_mailbox" as F_ROM
 }

 @enduml
