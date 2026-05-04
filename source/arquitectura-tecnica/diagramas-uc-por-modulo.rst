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
 actor "User\n(autenticado)" as user_autenticado
 actor "view_all_active_sessions" as view_all_active_sessions

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
 user_autenticado --> A02
 user_autenticado --> A04
 view_all_active_sessions --> A05
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

 actor "create_users" as create_users
 actor "update_users" as update_users
 actor "deactivate_users" as deactivate_users
 actor "list_users" as list_users

 rectangle "MOD_Users" {
   usecase "UC_USR_01\nCrear Usuario" as U01
   usecase "UC_USR_02\nConsultar Usuarios" as U02
   usecase "UC_USR_03\nModificar Usuario" as U03
   usecase "UC_USR_04\nEliminar Usuario\n(baja logica)" as U04
 }

 create_users --> U01
 list_users --> U02
 update_users --> U02
 update_users --> U03
 deactivate_users --> U04
 deactivate_users --> U02

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

 actor "assign_functions" as assign_functions
 actor "revoke_functions" as revoke_functions
 actor "view_assignments" as view_assignments
 actor "assign_function_groups" as assign_function_groups
 actor "view_separation_rules" as view_separation_rules
 actor "view_audit_log" as view_audit_log

 rectangle "MOD_Access" {
   usecase "UC_ACC_01\nAsignar Funciones\na Usuario" as AC01
   usecase "UC_ACC_02\nRevocar Funciones\nde Usuario" as AC02
   usecase "UC_ACC_03\nConsultar Permisos\nEfectivos" as AC03
   usecase "UC_ACC_04\nAsignar Agrupador\na Usuario" as AC04
   usecase "UC_ACC_05\nGestionar Reglas SoD" as AC05
   usecase "UC_ACC_08\nOtorgar Permiso\nTemporal Excepcional" as AC08
   usecase "UC_ACC_09\nAuditar Cambios\nde Acceso" as AC09
 }

 assign_functions --> AC01
 assign_functions --> AC08
 revoke_functions --> AC02
 view_assignments --> AC03
 assign_function_groups --> AC04
 view_separation_rules --> AC05
 view_audit_log --> AC09
 view_assignments --> AC09

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

 actor "assign_function_groups" as assign_function_groups
 actor "revoke_function_group" as revoke_function_group
 actor "create_function_group" as create_function_group
 actor "assign_functions_to_group" as assign_functions_to_group
 actor "view_assignments" as view_assignments
 actor "view_audit_log" as view_audit_log
 actor "User\n(autenticado)" as user_autenticado

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

 assign_function_groups --> P01
 revoke_function_group --> P02
 assign_function_groups --> P03
 assign_function_groups --> P04
 create_function_group --> P05
 assign_functions_to_group --> P06
 view_assignments --> P07
 user_autenticado --> P08
 view_audit_log --> P10

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

 actor "view_dashboard" as view_dashboard
 actor "view_kpis" as view_kpis
 actor "view_reports" as view_reports
 actor "export_csv\n(export_pdf/excel)" as export_csv
 actor "schedule_report" as schedule_report
 actor "save_view" as save_view
 actor "share_report" as share_report

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

 view_dashboard --> R01
 view_kpis --> R02
 view_reports --> R03
 export_csv --> R04
 schedule_report --> R07
 schedule_report --> R08
 save_view --> R10
 share_report --> R11
 view_reports --> R12
 view_reports --> R13
 view_reports --> R14
 view_reports --> R15
 view_reports --> R16
 view_reports --> R17

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

 actor "configure_team_alerts" as configure_team_alerts
 actor "view_alerts" as view_alerts
 actor "acknowledge_alert" as acknowledge_alert
 actor "view_alert_history" as view_alert_history

 rectangle "MOD_Alerts" {
   usecase "UC_ALR_01\nConfigurar Umbrales\nde Alertas" as AL01
   usecase "UC_ALR_02\nVer Alertas Activas" as AL02
   usecase "UC_ALR_03\nReconocer Alerta" as AL03
   usecase "UC_ALR_04\nVer Historial\nde Alertas" as AL04
   usecase "UC_ALR_05\nNotificacion\nAutomatica ETL" as AL05
   usecase "Motor de Alertas\n(automatico)" as MOTOR
 }

 configure_team_alerts --> AL01
 view_alerts --> AL02
 acknowledge_alert --> AL03
 view_alert_history --> AL04
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

 actor "view_pipeline_status" as view_pipeline_status
 actor "view_pipeline_errors" as view_pipeline_errors
 actor "view_data_availability" as view_data_availability
 actor "request_pipeline_retry" as request_pipeline_retry
 actor "APScheduler\n/ Cron" as APScheduler

 rectangle "MOD_Pipeline" {
   usecase "UC_PIP_01\nVer Estado ETL\n(etl_runs)" as P01
   usecase "UC_PIP_02\nVer Errores ETL\n(etl_runs.estado=fallido)" as P02
   usecase "UC_PIP_03\nVer Disponibilidad\nde Datos" as P03
   usecase "UC_PIP_04\nReintentar ETL\n(sp_etl_historico)" as P04
   usecase "Ejecutar ETL\nAutomatico\n(sp_etl_maestro)" as AUTO
 }

 view_pipeline_status --> P01
 view_pipeline_errors --> P02
 view_data_availability --> P03
 request_pipeline_retry --> P04
 APScheduler --> AUTO

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

 actor "view_audit_log" as view_audit_log
 actor "search_audit_log" as search_audit_log
 actor "export_audit_log" as export_audit_log
 actor "generate_compliance_report" as generate_compliance_report

 rectangle "MOD_Audit" {
   usecase "UC_AUD_01\nVer Auditoria\nGeneral" as A01
   usecase "UC_AUD_02\nBuscar en\nAuditoria" as A02
   usecase "UC_AUD_03\nExportar\nAuditoria" as A03
   usecase "UC_AUD_04\nGenerar Reporte\nCompliance" as A04
 }

 view_audit_log --> A01
 search_audit_log --> A02
 export_audit_log --> A03
 generate_compliance_report --> A04

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

 actor "view_application_logs" as view_application_logs
 actor "view_etl_logs" as view_etl_logs
 actor "search_logs" as search_logs
 actor "export_logs" as export_logs
 actor "view_infrastructure_logs" as view_infrastructure_logs
 actor "view_system_health" as view_system_health
 actor "view_technical_metrics" as view_technical_metrics

 rectangle "MOD_Logs" {
   usecase "UC_LOG_01\nVer Logs\ndel Sistema" as L01
   usecase "UC_LOG_02\nVer Logs ETL\n(etl_runs)" as L02
   usecase "UC_LOG_03\nBuscar Logs" as L03
   usecase "UC_LOG_04\nExportar Logs" as L04
   usecase "UC_LOG_05\nVer Logs de\nInfraestructura" as L05
   usecase "UC_LOG_06\nVer Estado\ndel Sistema" as L06
   usecase "UC_LOG_07\nVer Metricas\nTecnicas" as L07
 }

 view_application_logs --> L01
 view_etl_logs --> L02
 search_logs --> L03
 export_logs --> L04
 view_infrastructure_logs --> L05
 view_system_health --> L06
 view_technical_metrics --> L07

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

 actor "manage_own_agent_state" as manage_own_agent_state
 actor "answer_inbound_calls" as answer_inbound_calls
 actor "make_outbound_calls" as make_outbound_calls
 actor "hold_calls" as hold_calls
 actor "transfer_calls" as transfer_calls
 actor "enter_call_disposition" as enter_call_disposition
 actor "request_break" as request_break
 actor "view_own_performance_dashboard" as view_own_performance_dashboard
 actor "view_own_call_history" as view_own_call_history
 actor "read_own_mailbox" as read_own_mailbox

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

 manage_own_agent_state --> O01
 answer_inbound_calls --> O02
 make_outbound_calls --> O03
 hold_calls --> O04
 transfer_calls --> O05
 enter_call_disposition --> O06
 request_break --> O07
 view_own_performance_dashboard --> O08
 view_own_call_history --> O09
 read_own_mailbox --> O10

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

 actor "monitor_live_calls" as monitor_live_calls
 actor "barge_in_calls" as barge_in_calls
 actor "broadcast_team_messages" as broadcast_team_messages

 rectangle "MOD_Supervision" {
   usecase "UC_SUP_01\nMonitorear Llamadas\nen Vivo" as S01
   usecase "UC_SUP_02\nIntervenir en\nLlamada\n(barge in)" as S02
   usecase "UC_SUP_03\nEnviar Mensaje\nal Equipo" as S03
 }

 monitor_live_calls --> S01
 barge_in_calls --> S02
 broadcast_team_messages --> S03

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
