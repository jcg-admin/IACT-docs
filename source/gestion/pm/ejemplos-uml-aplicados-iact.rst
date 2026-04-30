.. meta::
 :artefacto: EJEMPLOS_UML_APLICADOS_IACT
 :tipo: Guia
 :dominio: gestion
 :subdominio: pm
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-04-30
 :ultimo_cambio: 2026-04-30
 :autor: NestorMonroy
 :clasificacion: Interno

==================================================================
Ejemplos UML aplicados al dominio IACT (PlantUML)
==================================================================

.. note::

 Compañero del :doc:`/gestion/pm/plan-documentacion-uc-con-uml`.
 Muestra cómo lucen los **9 diagramas UML** cuando se aplican al
 **dominio real del proyecto IACT** — call center IVR +
 analytics + supervisión ETL + RBAC granular.

 Sirve como **referencia de precedente** para los autores que
 generen los 13 documentos del plan.

 Diagramas en **PlantUML** (política del proyecto, no Mermaid).

 Para la teoría genérica de cada diagrama ver
 :doc:`/base-cognitiva/_uml/cuando-usar-cada-diagrama` (cheat-
 sheet) y la serie pedagógica :doc:`/base-cognitiva/_uml/index`.

----

1. Diagrama de clases — entidad ``Llamada`` (UC_RPT)
====================================================

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class Llamada {
     - id : Integer
     - centro_id : Integer
     - campana_id : Integer
     - servicio_id : Integer
     - tipo : Enum
     - duracion_seg : Integer
     - tiempo_espera_seg : Integer
     - resultado : Enum
     - fecha : DateTime
     + getDuracion() : Integer
     + esAbandonada() : Boolean
     + perteneceA(segmento : SegmentoDatos) : Boolean
   }
   @enduml

**Aplicación:** UC_RPT_01..14 consumen ``getDuracion()`` y
``esAbandonada()`` para calcular métricas. BR_012 valida
``perteneceA(segmento)`` antes de devolver filas. DOC-24
integra ésta con todas las demás clases.

**Perspectiva:** ESTÁTICA. **Audiencia:** Devs / Arquitectos.

----

2. Diagrama de objetos — instancia concreta de llamada
======================================================

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   object "llamada_001 : Llamada" as L {
     id = 4732112
     centro_id = 7
     campana_id = 22
     servicio_id = 3
     tipo = "INBOUND"
     duracion_seg = 184
     tiempo_espera_seg = 23
     resultado = "ATENDIDA"
     fecha = "2026-04-29 10:14:32"
   }
   @enduml

**Aplicación:** los casos de prueba de UC_RPT y UC_ALR deben
usar instancias concretas como ésta.

----

3. Diagrama de casos de uso — UC_RPT (reportes, 14 UCs)
=======================================================

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   left to right direction
   actor Operador
   actor Supervisor

   rectangle "UC_RPT — Reportes (14 UCs)" {
     usecase "UC_RPT_01\nVer Dashboard"             as U01
     usecase "UC_RPT_02\nVer Métricas Tiempo Real"  as U02
     usecase "UC_RPT_03\nVer Reportes Históricos"   as U03
     usecase "UC_RPT_04\nExportar Reporte"          as U04
     usecase "UC_RPT_07\nProgramar Reporte"         as U07
     usecase "UC_RPT_08\nVer Programados"           as U08
     usecase "UC_RPT_09\nConfigurar Filtros"        as U09
     usecase "UC_RPT_10\nGuardar Vista"             as U10
     usecase "UC_RPT_11\nCompartir Reporte"         as U11
     usecase "UC_RPT_12\nReporte Agentes"           as U12
     usecase "UC_RPT_13\nReporte Colas"             as U13
     usecase "UC_RPT_14\nReporte Campañas"          as U14
   }

   Operador   --> U01
   Operador   --> U02
   Operador   --> U09
   Operador   --> U10

   Supervisor --> U03
   Supervisor --> U04
   Supervisor --> U07
   Supervisor --> U08
   Supervisor --> U11
   Supervisor --> U12
   Supervisor --> U13
   Supervisor --> U14

   U01 ..> U09 : <<include>>
   U03 ..> U09 : <<include>>
   U04 ..> U03 : <<include>>
   U07 ..> U03 : <<include>>
   @enduml

**Aplicación:** DOC-20 (UC_RPT + UC_NOT) usa este diagrama como
vista global de su dominio.

**Perspectiva:** DINÁMICA (POV usuario). **Audiencia:** Product
Owners / Analistas.

----

4. Diagrama de estados — ``EjecucionETL`` (UC_PIP)
==================================================

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   [*] --> Programada

   Programada --> Ejecutando : scheduler.dispara()
   Ejecutando --> Cargando : conexion_ivr_ok
   Cargando --> Validando : filas_cargadas

   Validando --> Exitosa : sin_errores
   Validando --> ConErrores : errores_detectados

   ConErrores --> Reintentada : admin.solicitarReintento\n(UC_PIP_04)
   Reintentada --> Ejecutando

   Exitosa --> [*]
   ConErrores --> [*] : si admin descarta

   note right of Cargando
     Ventana CNST_008 (6-12 horas).
     No real-time per CNST_006.
   end note

   note right of Reintentada
     UC_PIP_04 — sólo funciones
     autorizadas. Auditado en
     CNST_025 (inmutable).
   end note
   @enduml

**Aplicación:** UC_PIP — supervisión del ETL nocturno.

----

5. Diagrama de secuencias — UC_RPT_01 (ver dashboard)
=====================================================

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   actor Operador
   participant ":Frontend\n(React)"   as F
   participant ":Backend\n(Django)"   as B
   participant ":SecRules"            as SR
   participant ":AuditLog"            as AL
   participant ":BD Analytics"        as DB

   Operador -> F  : 1. Click "Ver Dashboard"
   F -> B         : 2. GET /api/reports/dashboard

   B -> SR        : 3. verificarPermiso(view_dashboard)

   alt Permiso aprobado
     SR --> B     : 4a. autorizado + segmento
     B -> AL      : 5. registrar(VIEW_DASHBOARD)
     B -> DB      : 6. SELECT con filtro de segmento
     DB --> B     : 7. filas
     B --> F      : 8. {datos, métricas, ts}
     F --> Operador : 9. dashboard renderizado
   else Permiso denegado
     SR --> B     : 4b. denegado
     B -> AL      : 5. registrar(VIEW_DASHBOARD_DENIED)
     B --> F      : 6. {error: 403}
     F --> Operador : 7. ✗ "Sin permiso"
   end
   @enduml

**Aplicación:** DOC-25 (Secuencias críticas).

----

6. Diagrama de actividades — UC_RPT_04 (exportar reporte)
=========================================================

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   start
   :Operador solicita exportar\n(formato: CSV / Excel / PDF);
   :Verificar permiso export_<formato>;

   if ([permiso ok]) then (sí)
   else (no)
     :Mostrar 403 + auditar;
     stop
   endif

   :Aplicar filtros BR_012\n(segmento del usuario);
   :Estimar # filas resultado;

   if ([throttling CNST_020 alcanzado]) then (sí)
     :Mostrar "Límite del día";
     stop
   endif

   if ([filas > 10k → CNST_019]) then (sí)
     :Encolar export asíncrono;
     :Notificar al buzón cuando listo;
     :Operador descarga desde panel;
   else ([≤ 10k])
     :Generar archivo en línea;
     :Devolver descarga directa;
   endif

   :Registrar export en AuditLog;
   :Fin: archivo entregado;
   stop
   @enduml

**Aplicación:** DOC-20 (UC_RPT) y otros UCs con exportación.

----

7. Diagrama de colaboraciones — UC_ALR_03 reconocer alerta
==========================================================

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   actor Supervisor
   object ":Alerta"        as A
   object ":SecRules"      as SR
   object ":BuzonInterno"  as BI
   object ":AuditLog"      as AL
   object ":Suscriptores"  as S

   Supervisor -> SR : "1: verificarPermiso(ack_alert)"
   SR -> Supervisor : "2: autorizado"
   Supervisor -> A  : "3: reconocer()"
   A -> A           : "4: actualizar estado"
   A -> AL          : "5: registrar(ALERT_ACK)"
   A -> BI          : "6: notificarSuscriptores()"
   BI -> S          : "7: entregar mensaje\n(buzón, no email)"
   @enduml

**Aplicación:** DOC-20 (UC_NOT + UC_ALR). Sin email per
CNST_001.

----

8. Diagrama de componentes — arquitectura del sistema IACT
==========================================================

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   package "Frontend (React + Webpack)" {
     component "UI Components\nDashboards, Reportes" as UI
     component "Redux Store\nState Management"      as Redux
     component "HTTP Client\nAxios + JWT"           as HTTP
   }

   package "Backend (Django + DRF)" {
     component "REST API\nViewSets"                  as REST
     component "Auth Service\nJWT, Sessions"         as Auth
     component "RBAC Service\nFunciones, Grupos"     as RBAC
     component "Reports Service\nMétricas, Export"   as RPT
     component "Alerts Service\nUmbrales, Notif"     as ALR
     component "ETL Supervisor\nestado, reintento"   as PIP
     component "Audit Service\nInmutable"            as AUD
   }

   database "MySQL Analytics\nDatos IVR + RBAC + Audit" as DB

   package "Infraestructura externa" {
     component "IVR Conmutador\n(read-only)" as IVR
     component "Scheduler\nAPScheduler"      as Sched
     component "Buzón Interno\n(no email)"   as Buzon
   }

   UI    --> Redux : state
   UI    --> HTTP  : fetch / post
   HTTP  --> REST  : REST + JWT

   REST  --> Auth : usa
   REST  --> RBAC : usa
   REST  --> RPT  : usa
   REST  --> ALR  : usa
   REST  --> PIP  : usa
   REST  --> AUD  : usa

   Auth --> DB : queries
   RBAC --> DB : queries
   RPT  --> DB : queries
   ALR  --> DB : queries
   PIP  --> DB : queries
   AUD  --> DB : append-only

   PIP   ..> IVR   : ETL nocturno (read-only)
   PIP   ..> Sched : programación
   ALR   ..> Buzon : notifica (CNST_001)
   @enduml

**Aplicación:** DOC-26 (Componentes + Distribución).

----

9. Diagrama de distribución — despliegue del proyecto IACT
==========================================================

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   node "Cliente Web" <<dispositivo>> as Browser {
     component "Chrome / Firefox"
   }

   node "Servidor IACT" <<procesador>> as Web {
     component "Apache 2.4"
     component "mod_wsgi"
     component "Django 4 (App IACT)"
   }

   node "BD Analytics" <<procesador>> as DB {
     database "MySQL\nDatos IVR + RBAC + Auditoría"
   }

   node "IVR Conmutador" <<dispositivo>> as IVR {
     component "BD IVR (read-only)"
   }

   node "Scheduler" <<procesador>> as Sched {
     component "APScheduler / Cron"
   }

   Browser -- Web   : HTTPS / SSL
   Web     -- DB    : TCP 3306
   Web     -- IVR   : TCP 3306\n(read-only,\nventana 6-12h\nCNST_006/008)
   Sched   -- Web   : disparo ETL\n(UC_PIP_01)
   @enduml

**Aplicación:** DOC-26. Stack per
:doc:`/devops/adr-devops-001-vagrant-mod-wsgi-importante-produc`
— **sin** Docker / K8s / Nginx / Gunicorn.

----

10. Tabla resumen — qué diagrama va en qué documento
====================================================

.. list-table::
 :widths: 22 16 32 30
 :header-rows: 1

 * - Diagrama
   - Tipo
   - Propósito
   - DOC del plan
 * - Clases
   - Estático
   - Estructura
   - DOC-24
 * - Objetos
   - Estático
   - Instancias
   - Casos de prueba (cada UC)
 * - Casos de uso
   - Dinámico
   - Requisitos
   - DOC-14..DOC-23
 * - Estados
   - Dinámico
   - Ciclo de vida
   - DOC pipeline / DOC alertas
 * - Secuencias
   - Dinámico
   - Interacciones
   - DOC-25 (críticas)
 * - Actividades
   - Dinámico
   - Flujos
   - UCs complejos (export, ETL)
 * - Colaboraciones
   - Dinámico
   - Arquitectura
   - DOC-25
 * - Componentes
   - Estático
   - Módulos
   - DOC-26
 * - Distribución
   - Estático
   - Infraestructura
   - DOC-26

----

11. Trazabilidad
================

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Skill aplicada**
   - ``pm-planning`` (PMBOK — Planning, supporting examples)
 * - **Origen del documento**
   - Reescrito de "GUÍA-UML-DIAGRAMAS-FUNDAMENTALES — Aplicados
     al dominio E-commerce" (cheat-sheet aplicado interno),
     **reorientado al dominio real IACT** (call center IVR +
     analytics + RBAC + ETL nocturno).
 * - **Cheat-sheet genérica complementaria**
   - :doc:`/base-cognitiva/_uml/cuando-usar-cada-diagrama`
 * - **Lecciones completas (Schmuller)**
   - :doc:`/base-cognitiva/_uml/index`
 * - **Plan de documentación que aplica estos ejemplos**
   - :doc:`plan-documentacion-uc-con-uml`
 * - **Ejemplos OOP aplicados al dominio (compañero)**
   - :doc:`ejemplos-oop-aplicados-iact`
 * - **Modelo RBAC vigente**
   - :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact`
 * - **Restricciones citadas**
   - CNST_001 (no email), CNST_006/008 (ventana ETL 6-12h),
     CNST_019/020 (export async + throttling), CNST_025
     (auditoría inmutable), BR_012 (segmento único),
     ADR_DEVOPS_001 (Vagrant + Apache + mod_wsgi).
 * - **Política de diagramación**
   - :doc:`/base-cognitiva/plantuml-guide/guidelines`
