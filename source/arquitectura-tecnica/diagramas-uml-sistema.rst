.. meta::
 :artefacto: DIAGRAMAS_UML_SISTEMA_IACT
 :tipo: Diagramas UML del Sistema
 :dominio: arquitectura_tecnica
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-02
 :ultimo_cambio: 2026-05-02
 :autor: NestorMonroy
 :clasificacion: Interno

.. _diagramas-uml-sistema:

=========================
Diagramas UML del Sistema
=========================

Coleccion de diagramas UML que documentan la arquitectura, comportamiento
e interacciones del sistema IACT. Los actores se nombran por su grupo
RBAC en ingles (``view_reports``, ``request_pipeline_retry``, etc.)
conforme al catalogo de funciones del sistema.

----

1. Especificacion de Actores (Funciones RBAC)
=============================================

**view_reports**
  Usuario con funcion ``view_reports`` y ``view_dashboard``. Puede
  visualizar el Dashboard IVR y todos los reportes del MOD_Reports.
  Accede via ``GET /api/reportes/`` con filtrado automatico por
  segmento IVR (``UC_INC_RPT_01``).

**view_pipeline_status**
  Usuario con funciones ``view_reports``, ``view_alerts`` y
  ``view_pipeline_status``. Supervisa KPIs de calidad, alertas de umbral
  BR-016 y el estado del pipeline ETL en tiempo real.

**request_pipeline_retry**
  Usuario con funciones ``view_pipeline_status``, ``view_pipeline_errors``,
  ``view_data_availability`` y ``request_pipeline_retry``. Dispara,
  monitorea y reintenta el proceso ETL via ``sp_etl_maestro``.

**assign_functions**
  Usuario con funciones ``create_users``, ``update_users``,
  ``deactivate_users``, ``assign_functions``, ``revoke_functions``.
  Es el unico que puede modificar ``AccessGroup`` y
  ``AccessFunction`` en PostgreSQL.

**view_audit_log**
  Usuario con funciones ``view_audit_log``, ``search_audit_log_log``,
  ``export_audit_log_log``. Solo lectura sobre ``audit_log``
  (PostgreSQL). SoD: no puede tener funciones de AGR-006.

**Sistema IVR (Fuente de Datos)**
  Entidad externa. Provee datos de llamadas en ``tbl_historico_*``
  dentro de MariaDB. No interactua directamente con IACT — sus
  tablas son leidas por ``sp_etl_*``.

**APScheduler / Cron**
  Disparador automatico del pipeline ETL. Invoca el management
  command ``sync_etl`` segun CNST-008 (ventana de 6 a 12 horas).

----

2. Especificacion de Casos de Uso
===================================

**Autenticar JWT**

  *Descripcion:* Autentica al usuario mediante credenciales (username
  y password), emite un token JWT y carga sus funciones RBAC.

  *Flujo basico:* El sistema valida en PostgreSQL, genera JWT con
  payload RBAC y retorna token al cliente.

  *Flujo alternativo:* Tras 3 intentos fallidos: bloqueo temporal.

  *Precondicion:* No hay precondicion — es el primer caso de uso.

  *Postcondicion:* El token JWT contiene las funciones RBAC activas.

**Acceder a Modulos**

  *Descripcion:* El sistema filtra los modulos visibles segun las
  funciones RBAC del JWT activo del usuario.

  *Flujo basico:* El frontend consulta las funciones del JWT y
  renderiza solo los modulos autorizados.

  *Flujo alternativo:* El usuario puede cerrar sesion.

  *Precondicion:* Token JWT valido con al menos una funcion RBAC.

  *Postcondicion:* El usuario accede al modulo elegido.

**Ver Dashboard IVR** (UC_RPT_01)

  *Descripcion:* Vista ejecutiva con KPIs del IVR — TMO, nivel
  de servicio y tasa de abandono filtrados por segmento.

  *Flujo basico:* ``<<include>> UC_INC_RPT_01`` → resolver
  segmentos → ``callproc(sp_rpt_centros_xsegmento)``.

  *Flujo alternativo:* Auto-refresh cada 30 segundos via cache.

  *Precondicion:* Funcion ``view_dashboard`` en JWT activo.

  *Postcondicion:* KPIs del trimestre actual mostrados.

**Ver Reportes IVR** (UC_RPT_02..17)

  *Descripcion:* Modulo de 17 reportes. Todos incluyen
  ``<<include>> UC_INC_RPT_01`` (Resolver Segmento).

  *Flujo basico:* Usuario elige trimestre y tipo; el sistema
  llama al ``sp_rpt_*`` correspondiente filtrando por segmentos.

  *Flujo alternativo:* Cambiar trimestre y re-consultar.

  *Precondicion:* Funcion ``view_reports`` en JWT activo.

  *Postcondicion:* Datos del reporte disponibles para exportar.

**Resolver Segmento** (UC_INC_RPT_01)

  *Descripcion:* Comportamiento comun a todos los reportes. Mapea
  los DIDs RBAC del usuario a segmentos IVR.

  *Flujo basico:* Lee DIDs del JWT → mapea via ``DID_MAP``
  (``19028031:nacional_A``, ``19020001:nacional_B``,
  ``19020084:Puebla``) → retorna lista de segmentos activos.

  *Flujo alternativo:* Sin DIDs → 400 ``USER_WITHOUT_SEGMENT``.

  *Precondicion:* Token JWT valido.

  *Postcondicion:* Lista de segmentos disponible para filtrar.

**Gestionar Pipeline ETL** (UC_PIP_01..04)

  *Descripcion:* Disparar, monitorear y reintentar el ETL via
  ``sp_etl_maestro``. Registro en ``etl_runs``.

  *Flujo basico:* Usuario dispara ETL → se crea registro
  ``en_ejecucion`` en ``etl_runs`` → ``sp_etl_maestro`` ejecuta
  → estado actualizado a ``exitoso`` o ``fallido``.

  *Flujo alternativo:* Si falla: ``request_pipeline_retry`` (UC_PIP_04)
  via ``sp_etl_historico``.

  *Precondicion:* Funcion ``view_pipeline_status`` o ``request_pipeline_retry``.

  *Postcondicion:* Estado de ejecucion en ``etl_runs``.

**Consultar Logs** (UC_LOG_*)

  *Descripcion:* Acceso a logs del sistema IVR y al registro de
  auditoria de acciones de usuarios.

  *Flujo basico:* Consultar ``audit_log`` (PostgreSQL) para el
  rango de fechas solicitado.

  *Flujo alternativo:* No hay flujo alternativo.

  *Precondicion:* Funcion ``view_audit_log`` en JWT activo.

  *Postcondicion:* Logs mostrados con paginacion.

**Cerrar Sesion**

  *Descripcion:* Invalida el JWT activo y registra en
  ``audit_log`` (PostgreSQL).

  *Flujo basico:* Termina el acceso a todos los recursos.

  *Flujo alternativo:* No hay flujo alternativo.

  *Precondicion:* Token JWT valido.

  *Postcondicion:* Usuario sin acceso a los recursos.

----

3. Diagrama de Casos de Uso
=============================

.. uml::
 :caption: Figura 4 — Diagrama de casos de uso del Sistema IACT

 @startuml
 left to right direction

 actor "view_reports\n(view_dashboard)" as RVG
 actor "view_pipeline_status\n(view_alerts)" as QSG
 actor "request_pipeline_retry" as PAG
 actor "assign_functions\n(create_users)" as UAG
 actor "view_audit_log" as AUG
 actor "APScheduler\n/ Cron" as SCH
 actor "Sistema IVR\n(fuente datos)" as IVR

 rectangle "Sistema IACT" {
   usecase "Autenticar JWT" as UC_AUTH
   usecase "Acceder a\nModulos" as UC_ACC
   usecase "Ver Dashboard IVR" as UC_DASH
   usecase "Ver Reportes IVR" as UC_RPT
   usecase "Resolver Segmento\nUC_INC_RPT_01" as UC_INC
   usecase "Ver Llamadas\nAbandonadas\n(sp_rpt_llamadas_abandonadas)" as UC_R13
   usecase "Ver\nTransferencias\n(sp_rpt_centros_transferencia)" as UC_R15
   usecase "Ver Menus IVR\n(sp_rpt_menu_redirigidos)" as UC_R16
   usecase "Ver Clientes\nUnicos\n(sp_rpt_clientes)" as UC_R17
   usecase "Gestionar\nPipeline ETL" as UC_PIP
   usecase "Ver Disponibilidad\nde Datos" as UC_DISP
   usecase "Consultar Logs\n(view_audit_log)" as UC_LOG
   usecase "Gestionar\nFunciones RBAC" as UC_RBAC
   usecase "Cerrar Sesion" as UC_LOGOUT
 }

 RVG --> UC_AUTH
 QSG --> UC_AUTH
 PAG --> UC_AUTH
 UAG --> UC_AUTH
 AUG --> UC_AUTH
 SCH --> UC_PIP
 IVR --> UC_PIP

 UC_AUTH ..> UC_ACC : <<include>>
 UC_ACC ..> UC_DASH : <<extend>>
 UC_ACC ..> UC_RPT : <<extend>>
 UC_ACC ..> UC_PIP : <<extend>>
 UC_ACC ..> UC_LOG : <<extend>>
 UC_ACC ..> UC_LOGOUT : <<extend>>
 UAG --> UC_RBAC
 UC_RBAC ..> UC_AUTH : <<include>>

 UC_RPT ..> UC_INC : <<include>>
 UC_DASH ..> UC_INC : <<include>>

 UC_RPT ..> UC_R13 : <<extend>>
 UC_RPT ..> UC_R15 : <<extend>>
 UC_RPT ..> UC_R16 : <<extend>>
 UC_RPT ..> UC_R17 : <<extend>>

 UC_PIP ..> UC_DISP : <<extend>>

 @enduml

----

4. Diagrama de Clases
======================

Los actores (grupos RBAC) acceden a los recursos del sistema
a traves de sus clases de servicio. ``SistemaIACT`` centraliza
la autenticacion y carga de funciones RBAC. ``ServicioReportes``
encapsula las llamadas ``cursor.callproc(sp_rpt_*)``. La
composicion entre ``SistemaIACT`` y ``AuditoriaAcceso`` garantiza
que toda accion quede registrada en ``audit_log``.

.. uml::
 :caption: Figura 5 — Diagrama de clases del Sistema IACT

 @startuml

 class SistemaIACT {
   +username: str
   +password: str
   +rbac_functions: list
   +receiveCredentials(): void
   +checkCredentials(): bool
   +loadRBACFunctions(): list
 }

 class SegmentResolver {
   +DID_MAP: dict
   +segments_for(user_id: int): list
 }

 class ServicioReportes {
   +trimestre: str
   +segmentos: list
   +callproc(sp_name, params): list
   +centros_transferencia(trimestre): list
   +llamadas_abandonadas(trimestre): list
   +menu_redirigidos(trimestre): list
   +clientes(trimestre): list
   +centros_xsegmento(trimestre): list
   +menu_centro(trimestre): list
   +cMENU_ERROR(trimestre): list
 }

 class ETLEjecucion {
   +tabla_origen: str
   +trimestre: str
   +estado: EstadoEnum
   +iniciado_en: datetime
   +finalizado_en: datetime
   +registros_base: int
   +disparar(): void
   +reintentar(): void
 }

 class DisparadorETL {
   +trimestre: str
   +ejecutado_por: str
   +receiveData(): void
   +sendToETL(): void
 }

 class ReporteLlamadasAbandonadas {
   +trimestre: str
   +segmento: str
   +total_abandonadas: int
   +tasa_abandono: float
   +receiveInput(): void
   +getReport(): void
 }

 class ReporteTransferencias {
   +trimestre: str
   +segmento: str
   +total_transferencias: int
   +receiveInput(): void
   +getReport(): void
 }

 class AuditoriaAcceso {
   +user_id: int
   +accion: str
   +timestamp: datetime
   +ip_origen: str
   +receiveData(): void
   +addToAuditLog(): void
 }

 class CancelEjecucionETL {
   +removeFromETLQueue(): void
 }

 class ReintentoETL {
   +editEjecucion(): void
 }

 enum EstadoEnum {
   en_ejecucion
   exitoso
   fallido
 }

 SistemaIACT --> SegmentResolver : usa
 SistemaIACT --> ServicioReportes : invoca
 SistemaIACT --> ETLEjecucion : gestiona
 DisparadorETL --> ETLEjecucion : crea
 ReporteLlamadasAbandonadas --> ServicioReportes
 ReporteTransferencias --> ServicioReportes
 AuditoriaAcceso *-- SistemaIACT
 ReintentoETL --> ETLEjecucion
 CancelEjecucionETL --> ETLEjecucion
 ETLEjecucion --> EstadoEnum

 @enduml

----

5. Diagrama de Actividad — Flujo Principal
============================================

Carriles por grupo RBAC. El proceso inicia con la autenticacion
JWT de cada grupo. Tras el login exitoso el flujo se bifurca segun
las funciones propias de cada grupo. Todos convergen en el cierre
de sesion.

.. uml::
 :caption: Figura 6 — Diagrama de actividad (flujo principal por grupo RBAC)

 @startuml

 |view_reports|
 start

 |request_pipeline_retry|

 |assign_functions|

 |view_reports|
 :POST /api/auth/login — JWT;

 |request_pipeline_retry|
 :POST /api/auth/login — JWT;

 |assign_functions|
 :POST /api/auth/login — JWT;

 |view_reports|
 note right: funciones activas: view_reports / view_dashboard

 fork

   |view_reports|
   :GET /api/reportes/?trimestre=;
   :UC_INC_RPT_01 — Resolver Segmento;
   :callproc(sp_rpt_*);
   :Visualizar Reporte;

 fork again

   |request_pipeline_retry|
   :GET /api/dashboard/;
   :callproc(sp_rpt_centros_xsegmento);
   :Revisar KPIs;
   :POST /api/pipeline/ejecutar/;
   :CALL sp_etl_maestro(trimestre);
   if (ETL exitoso?) then
     :etl_runs.estado = exitoso;
   else
     :etl_runs.estado = fallido;
     :Generar Alerta BR-016;
   endif

 fork again

   |assign_functions|
   :Gestionar Funciones RBAC;
   :assign_functions / revoke_functions;
   :Asignar DIDs a Usuario;
   :Actualizar AccessGroup en PostgreSQL;

 end fork

 |request_pipeline_retry|
 :DELETE /api/auth/logout/;
 :Registrar en audit_log;
 stop

 @enduml

----

6. Diagrama de Actividad — Sub-actividad Autenticacion
========================================================

Flujo interno de la funcion de autenticacion. El usuario ingresa
credenciales; el sistema las valida en PostgreSQL, genera el JWT
con payload RBAC y carga las funciones del usuario. Si las
credenciales son incorrectas se retorna 401.

.. uml::
 :caption: Figura 7 — Diagrama de actividad (sub-actividad autenticacion)

 @startuml

 |User|
 start
 :Ingresar username y password;

 |Sistema IACT|
 :Recibir POST /api/auth/login/;
 :Consultar auth_user en PostgreSQL;
 if (Credenciales correctas?) then (si)
   :Cargar funciones RBAC del usuario;
   :Generar JWT con payload RBAC;
   |User|
   :Acceder al sistema;
   :Autenticacion exitosa;
 else (no)
   :Retornar 401 Unauthorized;
   |User|
   if (Reintentar?) then (si)
     :Ingresar credenciales nuevamente;
   else (no)
     stop
   endif
 endif

 @enduml

----

7. Diagrama de Maquina de Estados
===================================

Ciclo de vida de la sesion de un usuario IACT. El estado inicial
es ``Autenticacion JWT``. Una vez autenticado, el usuario entra al
estado compuesto ``Dashboard IACT`` que contiene los sub-estados de
cada modulo. El modulo visible depende de las funciones RBAC del
JWT activo. Al cerrar sesion (o expirar el JWT) transita al estado
final.

.. uml::
 :caption: Figura 8 — Diagrama de maquina de estados (sesion IACT)

 @startuml

 state "Autenticacion JWT" as AUTH {
   entry/usuario ingresa username y password
   do/validar credenciales + cargar RBAC en PostgreSQL
   exit/JWT generado con payload de funciones
 }

 state "Dashboard IACT" as DASH {
   entry/JWT valido recibido
   do/filtrar modulos segun funciones RBAC del JWT
   exit/cierre de sesion o JWT expirado

   state "Ver Dashboard IVR\n[view_dashboard]" as S_DASH {
     entry/usuario selecciona dashboard
     do/callproc(sp_rpt_centros_xsegmento, [trimestre])
     exit/KPIs mostrados en frontend
   }

   state "MOD Reports\n[view_reports]" as S_RPT {
     entry/usuario selecciona reporte
     do/UC_INC_RPT_01 + callproc(sp_rpt_*, [trimestre])
     exit/datos del reporte mostrados
   }

   state "Gestion Pipeline ETL\n[view_pipeline_status / request_pipeline_retry]" as S_ETL {
     entry/usuario selecciona pipeline
     do/CALL sp_etl_maestro(trimestre) via DisparadorETL
     exit/estado registrado en etl_runs
   }

   state "Consulta de Logs\n[view_audit_log]" as S_LOG {
     entry/usuario selecciona logs
     do/consultar audit_log en PostgreSQL
     exit/logs mostrados con paginacion
   }

   state "Gestion RBAC\n[assign_functions / revoke_functions]" as S_RBAC {
     entry/assign_functions selecciona administracion
     do/modificar AccessGroup y DIDs en PostgreSQL
     exit/cambios guardados y propagados
   }

   [*] --> S_DASH
   S_DASH --> S_RPT : choice=reportes
   S_DASH --> S_ETL : choice=pipeline
   S_DASH --> S_LOG : choice=logs
   S_DASH --> S_RBAC : choice=admin\n[assign_functions en JWT]
   S_RPT --> S_DASH : volver
   S_ETL --> S_DASH : volver
   S_LOG --> S_DASH : volver
   S_RBAC --> S_DASH : volver
 }

 state "Cierre de Sesion" as FINAL {
   entry/usuario cierra sesion o JWT expira
   do/invalidar JWT + registrar en audit_log
   exit/fin de sesion
 }

 [*] --> AUTH
 AUTH --> DASH : [credenciales validas]
 AUTH --> FINAL : [3 intentos fallidos]
 DASH --> FINAL : [DELETE /api/auth/logout/]
 DASH --> FINAL : [JWT expirado]
 FINAL --> [*]

 @enduml

----

8. Diagrama de Secuencia
=========================

Muestra la interaccion entre el usuario y el Sistema IACT. El
fragmento ``alt`` verifica si hay JWT valido o si es nueva sesion.
El fragmento ``loop`` contiene todos los accesos posibles durante
la sesion. Un fragmento ``neg`` muestra el caso de fallo del ETL
y ``opt`` permite el reintento.

.. uml::
 :caption: Figura 9 — Diagrama de secuencia del Sistema IACT

 @startuml

 actor "User" as USR
 participant "AuthEndpoint" as AE
 participant "DashboardEndpoint" as DE
 participant "SegmentResolver" as SR
 participant "ServicioReportes\n(sp_rpt_*)" as SRP
 participant "DisparadorETL" as ETL
 actor "Sistema IVR\n(fuente)" as IVR

 alt [autenticacion exitosa: status=TRUE]

   alt [Nueva sesion]
     USR -> AE : 1: POST /api/auth/login()
     AE -> AE : 2: ValidarCredenciales()
     AE --> USR : 3: status := GenerarJWT(rbac_functions)
   else [JWT valido existente]
     USR -> DE : 4: GET /api/dashboard/ (JWT)
     DE -> DE : 5: ValidarJWT_RBAC(view_dashboard)
     DE --> USR : 6: sesion_confirmada
   end

   loop [sesion activa]

     opt [view_dashboard en JWT]
       USR -> DE : 7: GET /api/dashboard/
       DE -> SR : 8: segments_for(user_id)
       SR --> DE : 9: segmentos
       DE -> SRP : 10: callproc(sp_rpt_centros_xsegmento)
       SRP --> DE : 11: KPIs IVR
       DE --> USR : 12: dashboard mostrado
     end

     opt [view_reports en JWT]
       USR -> DE : 13: GET /api/reportes/?trimestre=
       DE -> SR : 14: segments_for(user_id)
       SR --> DE : 15: segmentos
       DE -> SRP : 16: callproc(sp_rpt_*, [trimestre])
       SRP --> DE : 17: rows reporte
       DE --> USR : 18: reporte mostrado
     end

     opt [view_pipeline_status en JWT]
       USR -> ETL : 19: POST /api/pipeline/ejecutar/
       ETL -> IVR : 20: leer tbl_historico_*
       ETL -> ETL : 21: CALL sp_etl_maestro(trimestre)
       ETL --> USR : 22: estado_ejecucion

       neg [ETL fallido]
         ETL --> USR : 23: estado = fallido
         USR --> ETL : 24: error en ejecucion
       end

       opt [request_pipeline_retry en JWT]
         par
           USR -> ETL : 25: reintentar(trimestre)
           ETL --> USR : 26: ejecucion_reintentada
         also
           USR -> ETL : 27: cancelar_reintento()
           ETL --> USR : 28: reintento_cancelado
         end
       end
     end

   end

 else [autenticacion fallida: status=FALSE]
   USR -> AE : 29: login_fallido()
   AE -->x USR : 30: <<destroy>> 401 Unauthorized
 end

 @enduml

----

9. Diagrama de Comunicacion
=============================

Focaliza en la interaccion entre los objetos del sistema. Los
mensajes numerados representan los condicionales e iteraciones.
Los mensajes con ``*`` indican iteracion; con ``[condicion]``
indican guarda basada en funcion RBAC del JWT activo.

.. uml::
 :caption: Figura 10 — Diagrama de comunicacion del Sistema IACT

 @startuml

 object ": User (RBAC group)" as USR
 object ": AuthEndpoint" as AE
 object ": DashboardEndpoint" as DE
 object ": SegmentResolver" as SR
 object ": ServicioReportes" as SRP
 object ": DisparadorETL" as ETL
 object "AutenticacionFallida" as FAIL

 USR --> AE : 1: check_credentials()
 AE --> AE : 2: status := ValidarJWT(rbac_functions)
 AE --> USR : 3: [status==TRUE] GenerarJWT()
 AE --> DE : 4 *[status==TRUE]: dashboard_data()
 DE --> SR : 5 *[view_dashboard]: segments_for(user_id)
 SR --> DE : 6: segmentos
 DE --> SRP : 7 *[view_dashboard]: callproc(sp_rpt_centros_xsegmento)
 SRP --> DE : 8: KPIs IVR
 DE --> USR : 9: dashboard_mostrado
 USR --> DE : 10 *[view_reports]: reporte(trimestre)
 DE --> SRP : 11 *[view_reports]: callproc(sp_rpt_*)
 SRP --> DE : 12: rows_reporte
 DE --> USR : 13: reporte_mostrado
 USR --> ETL : 14 *[view_pipeline_status]: disparar_etl(trimestre)
 ETL --> ETL : 15: CALL sp_etl_maestro(trimestre)
 ETL --> USR : 16: estado_ejecucion
 USR --> ETL : 17 *[request_pipeline_retry]: request_pipeline_retry()
 ETL --> USR : 18 *[success==TRUE]: ejecucion_reintentada
 ETL --> USR : 19: receiptStatus := cancelar_reintento
 USR --> AE : 20 *[status==FALSE]: AutenticacionFallida() <<destroy>>
 FAIL --> USR : 21 *[status==FALSE]: AutenticacionFallida()

 @enduml

----

10. Diagrama de Componentes
=============================

El componente ``view_reports`` accede a los modulos de
reportes y dashboard. El componente ``Backend IACT`` (Django)
gestiona autenticacion, reportes y ETL. ``MariaDB`` contiene
los 7 stored procedures de reporte (``sp_rpt_*``) y los 4 de
ETL (``sp_etl_*``). ``PostgreSQL`` gestiona usuarios y auditoria.

.. uml::
 :caption: Figura 11 — Diagrama de componentes del Sistema IACT

 @startuml

 component "<<System>>\nview_reports\n(view_reports / view_dashboard)" as COMP_RVG {
   artifact "<<artifact>>\nReport Request Buffer\n(JWT + trimestre)" as ART_REQ
 }

 component "<<System>>\nBackend IACT (Django)" as COMP_BACK {
   component "Suggestion\nServicio de Reportes" as SVC_OUTER {
     artifact "<<artifact>>\nsp_rpt_llamadas_abandonadas" as ART_R1
     artifact "<<artifact>>\nsp_rpt_centros_transferencia" as ART_R2
     artifact "<<artifact>>\nsp_rpt_menu_redirigidos" as ART_R3
     artifact "<<artifact>>\nsp_rpt_clientes" as ART_R4
     artifact "<<artifact>>\nsp_rpt_centros_xsegmento" as ART_R5
     artifact "<<artifact>>\nsp_rpt_menu_centro" as ART_R6
     artifact "<<artifact>>\nsp_rpt_cMENU_ERROR" as ART_R7
   }
   component "<<process>>\nAuthService\n(JWT + RBAC)" as SVC_AUTH
   component "<<process>>\nSegmentResolver\n(DID_MAP)" as SVC_SEG
   component "<<process>>\nDisparadorETL\n(management command)" as SVC_ETL
 }

 database "<<subsystem>>\nMariaDB 10.1.48" as DB_MARIA {
   artifact "tbl_historico_*\n(Repositorio IVR)" as ART_HIST
   artifact "base_ivr_detalle\nbase_ivr_clientes\n(Base Analitica)" as ART_BASE
   artifact "etl_runs\n(Registro ETL)" as ART_ETLRUNS
 }

 database "<<subsystem>>\nPostgreSQL" as DB_PG {
   artifact "auth_user\n(AccessGroup / AccessFunction)" as ART_USERS
   artifact "audit_log" as ART_AUDIT
 }

 COMP_RVG --> COMP_BACK : +Request\n1..* a 1\nHTTPS
 COMP_BACK --> DB_MARIA : communicates\nSQL/TCP :3306
 COMP_BACK --> DB_PG : communicates\nSQL/TCP :5432

 SVC_ETL --> ART_HIST : lee (fuente IVR)
 SVC_ETL --> ART_BASE : escribe via sp_etl_*
 SVC_ETL --> ART_ETLRUNS : registra ejecucion
 SVC_OUTER --> ART_BASE : lee via sp_rpt_*
 SVC_SEG --> ART_USERS : lee DIDs RBAC
 SVC_AUTH --> ART_USERS : valida usuario
 SVC_AUTH --> ART_AUDIT : registra acciones

 @enduml

----

11. Diagrama de Despliegue
===========================

Los nodos representan el OS, las bases de datos y el servidor de
aplicacion. La base de datos MariaDB reside en el mismo servidor
de aplicacion por proximidad con el proceso ETL. PostgreSQL
gestiona datos operacionales Django. El protocolo entre cliente
y servidor es HTTPS. El acceso de Django a MariaDB usa la
conexion nombrada ``ivr`` en ``DATABASES`` de Django settings.

.. uml::
 :caption: Figura 12 — Diagrama de despliegue del Sistema IACT

 @startuml

 node "<<server>>\nServidor de Aplicacion" as NODE_APP {
   node "<<OS>>\nLinux" as OS_LINUX {
     node "<<WebServer>>\nGunicorn + Nginx" as WEB_SERVER {
       node "<<service>>\nBackend IACT" as IACT_SVC {
         artifact "<<artifact>>\niact-app.wsgi" as ART_WSGI
         artifact "<<artifact>>\nsettings.py\n(DATABASES: ivr + default)" as ART_SETTINGS
       }
     }
     node "<<database system>>\nMariaDB 10.1.48" as NODE_MARIA {
       node "Website data\nbase_ivr" as SCH_BASE {
         artifact "base_ivr_detalle" as DB_DETALLE
         artifact "base_ivr_clientes" as DB_CLIENTES
       }
       node "ETL control\netl_control" as SCH_ETL {
         artifact "etl_runs" as DB_ETLR
       }
       node "IVR source\nivr_fuente" as SCH_FUENTE {
         artifact "tbl_historico_*" as DB_HIST
       }
     }
     node "<<database system>>\nPostgreSQL" as NODE_PG {
       node "operational\niact_operational" as SCH_PG {
         artifact "auth_user\nAccessGroup / AccessFunction" as DB_USERS
         artifact "audit_log" as DB_AUDIT
       }
     }
   }
 }

 node "<<client>>\nview_reports\n(PC / Navegador)" as NODE_RVG {
   node "<<app>>\nNavegador Web" as BROWSER_RVG {
     artifact "<<artifact>>\nJWT Token (LocalStorage)" as ART_JWT_RVG
     artifact "<<artifact>>\nCache Reportes (30s)" as ART_CACHE_RVG
   }
 }

 node "<<client>>\nrequest_pipeline_retry\n(PC / Navegador)" as NODE_PAG {
   node "<<app>>\nNavegador Web" as BROWSER_PAG {
     artifact "<<artifact>>\nJWT Token (LocalStorage)" as ART_JWT_PAG
   }
 }

 NODE_RVG -- NODE_APP : +receive\nFetch\n1..* a 1\nHTTPS
 NODE_PAG -- NODE_APP : +receive\nFetch\n1..* a 1\nHTTPS
 IACT_SVC -- NODE_MARIA : SQL/TCP (puerto 3306)
 IACT_SVC -- NODE_PG : SQL/TCP (puerto 5432)

 @enduml

----

12. Sub-maquina de Estados — Ejecucion ETL
============================================

Sub-estado interno de ``Gestion Pipeline ETL``. Muestra la
ejecucion paralela de ``sp_etl_base_detalle`` y
``sp_etl_base_clientes`` (disparados internamente por
``sp_etl_maestro``) con fork/join antes de actualizar el
estado en ``etl_runs``.

.. uml::
 :caption: Figura 13 — Sub-maquina de estados: Ejecucion ETL

 @startuml

 state "Ejecucion ETL" as ETL_EXEC {

   state "Recibir Solicitud ETL" as S1
   S1 : entry / validar funcion view_pipeline_status en JWT
   S1 : do / INSERT etl_runs (estado=en_ejecucion)
   S1 : exit / ID de ejecucion asignado

   state fork_etl <<fork>>

   state "sp_etl_base_detalle" as S2A
   S2A : entry / leer tbl_historico_detalle (fuente IVR)
   S2A : do / TRUNCATE + INSERT base_ivr_detalle
   S2A : exit / rows_detalle registrados en etl_runs

   state "sp_etl_base_clientes" as S2B
   S2B : entry / leer tbl_historico_clientes (fuente IVR)
   S2B : do / TRUNCATE + INSERT base_ivr_clientes
   S2B : exit / rows_clientes registrados en etl_runs

   state join_etl <<join>>

   state "Verificar Resultado" as S3
   S3 : entry / consolidar resultado de ambos sp_etl_*
   S3 : do / UPDATE etl_runs SET estado, finalizado_en
   S3 : exit / fin de cadena ETL

   state "ETL Exitoso" as SUCC
   SUCC : entry / estado = exitoso
   SUCC : do / notificar request_pipeline_retry
   SUCC : exit / datos disponibles en base_ivr_*

   state "ETL Fallido" as FAIL
   FAIL : entry / estado = fallido
   FAIL : do / generar alerta BR-016 si aplica
   FAIL : exit / reintento disponible via sp_etl_historico

   [*] --> S1
   S1 --> fork_etl
   fork_etl --> S2A
   fork_etl --> S2B
   S2A --> join_etl
   S2B --> join_etl
   join_etl --> S3
   S3 --> SUCC : [sp_etl exitosos]
   S3 --> FAIL : [sp_etl fallido]
   SUCC --> [*]
   FAIL --> [*]
 }

 [*] --> ETL_EXEC
 ETL_EXEC --> [*]

 @enduml

----

13. Sub-maquina de Estados — Consulta de Reporte
=================================================

Sub-estado interno de ``MOD Reports``. Muestra el flujo de
``UC_INC_RPT_01`` (Resolver Segmento) seguido de la resolucion
paralela por segmento activo del usuario y la llamada al
``sp_rpt_*`` correspondiente con join antes de renderizar.

.. uml::
 :caption: Figura 14 — Sub-maquina de estados: Consulta de Reporte IVR

 @startuml

 state "Consulta de Reporte IVR" as RPT_EXEC {

   state "Solicitar Reporte" as R1
   R1 : entry / validar funcion view_reports en JWT
   R1 : do / enviar GET /api/reportes/?trimestre=
   R1 : exit / solicitud aceptada por DashboardEndpoint

   state "Resolver Segmento\nUC_INC_RPT_01" as R2
   R2 : entry / leer DIDs RBAC del usuario en PostgreSQL
   R2 : do / mapear DIDs via DID_MAP a segmentos IVR
   R2 : exit / lista de segmentos activos disponible

   state fork_seg <<fork>>

   state "Segmento nacional_A\n(DID 19028031)" as R3A
   R3A : entry / DID 19028031 activo en usuario
   R3A : do / filtrar rows por nacional_A
   R3A : exit / atributos de segmento disponibles

   state "Segmento nacional_B\n(DID 19020001)" as R3B
   R3B : entry / DID 19020001 activo en usuario
   R3B : do / filtrar rows por nacional_B
   R3B : exit / atributos de segmento disponibles

   state "Segmento Puebla\n(DID 19020084)" as R3C
   R3C : entry / DID 19020084 activo en usuario
   R3C : do / filtrar rows por Puebla
   R3C : exit / atributos de segmento disponibles

   state join_seg <<join>>

   state "Llamar sp_rpt_*" as R4
   R4 : entry / consolidar segmentos activos del usuario
   R4 : do / cursor.callproc(sp_rpt_*, [trimestre, segmentos])
   R4 : exit / rows de reporte disponibles

   state "Renderizar Reporte" as R5
   R5 : entry / recibir rows del sp_rpt_*
   R5 : do / enviar datos al frontend
   R5 : exit / reporte renderizado al usuario

   [*] --> R1
   R1 --> R2
   R2 --> fork_seg
   fork_seg --> R3A
   fork_seg --> R3B
   fork_seg --> R3C
   R3A --> join_seg
   R3B --> join_seg
   R3C --> join_seg
   join_seg --> R4
   R4 --> R5
   R5 --> [*]
 }

 [*] --> RPT_EXEC
 RPT_EXEC --> [*]

 @enduml

.. note::

 El fork/join de segmentos es logico — el ``SegmentResolver``
 evalua en paralelo todos los segmentos del usuario. Solo los
 segmentos con DID asignado al usuario contribuyen rows al join.
 Si el usuario no tiene ningun DID activo, el flujo retorna
 400 ``USER_WITHOUT_SEGMENT`` antes del fork.

----

14. Diagrama de Despliegue — Vista Multi-cliente
=================================================

Vista extendida del despliegue mostrando los distintos tipos de
cliente (grupos RBAC) conectados al servidor de aplicacion.
Cada grupo accede al servidor con su propio JWT y conjunto de
funciones. El servidor organiza sus modulos por area funcional
con los artefactos correspondientes.

.. uml::
 :caption: Figura 15 — Diagrama de despliegue (vista multi-cliente)

 @startuml

 node "view_reports\nos WINDOWS / MacOS" as CLI_RVG {
   node "<<app>>\nNavegador (Chrome / Firefox)" as BR_RVG {
     artifact "<<artifact>>\nUser_View\n(JWT + view_reports)" as ART_RVG
   }
 }

 node "request_pipeline_retry\nos WINDOWS / Linux" as CLI_PAG {
   node "<<app>>\nNavegador (Chrome / Firefox)" as BR_PAG {
     artifact "<<artifact>>\nUser_View\n(JWT + view_pipeline_status)" as ART_PAG
   }
 }

 node "assign_functions\nos WINDOWS" as CLI_UAG {
   node "<<app>>\nNavegador (Chrome / Firefox)" as BR_UAG {
     artifact "<<artifact>>\nUser_View\n(JWT + assign_functions)" as ART_UAG
   }
 }

 node "<<server>>\nServidor IACT" as NODE_SRV {

   node "MOD_Reports\n(view_reports / view_dashboard)" as MOD_RPT {
     artifact "<<artifact>>\nsp_rpt_centros_xsegmento" as ART_S1
     artifact "<<artifact>>\nsp_rpt_llamadas_abandonadas" as ART_S2
   }

   node "MOD_Pipeline ETL\n(view_pipeline_status / request_pipeline_retry)" as MOD_ETL {
     artifact "<<artifact>>\nsp_etl_maestro" as ART_E1
     artifact "<<artifact>>\netl_runs" as ART_E2
   }

   node "MOD_Logs\n(view_audit_log)" as MOD_LOG {
     artifact "<<artifact>>\naudit_log" as ART_L1
   }

   node "MOD_Admin\n(assign_functions / create_users)" as MOD_ADM {
     artifact "<<artifact>>\nAccessGroup" as ART_A1
     artifact "<<artifact>>\nAccessFunction" as ART_A2
   }

 }

 node "Database" as NODE_DB {
   artifact "<<artifact>>\nbase_ivr_detalle\nbase_ivr_clientes" as DB_IVR
   artifact "<<artifact>>\nauth_user\naudit_log" as DB_AUTH
   artifact "<<artifact>>\ntbl_historico_*" as DB_HIST
 }

 CLI_RVG --> NODE_SRV : +receive Fetch\n1..* 1 +send
 CLI_PAG --> NODE_SRV : +receive Fetch\n1..* 1 +send
 CLI_UAG --> NODE_SRV : +receive Fetch\n1..* 1 +send
 NODE_SRV --> NODE_DB : +receive/send\nFetch 1 1 +receive/send

 @enduml
