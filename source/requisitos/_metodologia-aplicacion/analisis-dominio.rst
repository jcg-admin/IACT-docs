.. meta::
 :artefacto: EJEMPLOS_ANALISIS_DOMINIO_IACT
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
Análisis de dominio aplicado al ecosistema IACT (PlantUML)
==================================================================

.. note::

 Compañero del :doc:`/requisitos/_metodologia-aplicacion/plan-documentacion-uc`
 y de
 :doc:`/normativa/estandares/metodologia-analisis-dominio-ucs`.

 Muestra la técnica **sustantivos → clases / verbos →
 operaciones / adjetivos → atributos** aplicada al **dominio
 real del proyecto IACT** (call center IVR + analytics +
 supervisión ETL + RBAC granular).

 Sirve como **referencia de precedente**: cada UC documentado
 debe partir de un análisis similar en estilo y nivel de
 detalle.

 Diagramas en **PlantUML** (política del proyecto, no Mermaid).

 Para la teoría genérica ver
 :doc:`/base-cognitiva/_uml/uml-03-uso-orientacion-objetos`
 (Schmuller Hora 3) y la metodología completa
 :doc:`/normativa/estandares/metodologia-analisis-dominio-ucs`.

----

1. Del lenguaje natural al modelo UML
=====================================

Cuando hablamos con un stakeholder sobre el dominio IACT, usa
**lenguaje natural**:

  *"Nuestros operadores y supervisores acceden al dashboard
  para ver métricas de las llamadas del IVR. Pueden buscar y
  filtrar por centro, campaña, servicio o región. Cada usuario
  está restringido a su segmento de datos. Las llamadas se
  cargan desde el IVR vía un pipeline ETL nocturno (ventana de
  6 a 12 horas). Calculamos métricas como tasa de abandono,
  tiempo promedio de espera, índice de eficiencia. Las alertas
  se disparan cuando las métricas superan umbrales configurados.
  Sin email — sólo buzón interno. Los administradores asignan
  funciones a usuarios; cada función es una capacidad atómica
  del RBAC. Los auditores consultan la auditoría inmutable de
  todas las acciones."*

**Regla de oro:**

::

 SUSTANTIVOS → CLASES
 VERBOS      → OPERACIONES
 ADJETIVOS   → ATRIBUTOS

----

2. Estructura UML de una clase
==============================

Una clase tiene 4 áreas: **nombre**, **atributos**,
**operaciones** y **responsabilidades**.

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class Llamada {
     - id : Integer
     - centro_id : Integer
     - duracion_seg : Integer
     - resultado : Enum
     + getDuracion() : Integer
     + esAbandonada() : Boolean
     -- responsabilidades --
     Representar una llamada del IVR
     consumida por reportes y alertas.
   }
   note right of Llamada
     {duracion_seg ≥ 0}
     {resultado ∈ ATENDIDA |
                  ABANDONADA |
                  TRANSFERIDA}
   end note
   @enduml

**Convenciones:**

- **Nombre:** ``PascalCase`` (``Llamada``,
  ``EjecucionETL``, ``SegmentoDatos``).
- **Atributos:** ``camelCase`` con visibilidad ``-`` privado /
  ``+`` público / ``#`` protegido.
- **Operaciones:** ``camelCase`` con paréntesis y firma.
- **Restricciones:** entre llaves ``{…}`` en notas.

----

3. Sustantivos del dominio IACT → clases
========================================

3.1 Sustantivos identificados en la conversación
------------------------------------------------

::

 USUARIOS:        Operador, Supervisor, Administrador,
                  Auditor, Usuario, Sesion, SegmentoDatos,
                  Funcion, Grupo, Permiso, PermisoExcepcional
 LLAMADAS / IVR:  Llamada, Centro, Campaña, Servicio, Region
 MÉTRICAS:        Metrica, TasaAbandono,
                  TiempoPromedioEspera, IndiceEficiencia,
                  Reporte, Dashboard, Filtro
 PIPELINE:        EjecucionETL, ErrorETL, FilaCargada,
                  Scheduler
 ALERTAS:         Alerta, Umbral, Suscripcion, BuzonInterno,
                  Mensaje
 AUDITORÍA:       EventoAuditoria, AuditoriaPermiso,
                  AuditoriaAcceso

3.2 Conversión a clases (vista global del dominio)
--------------------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   package "Acceso & RBAC" as PA {
     class Usuario
     class Sesion
     class SegmentoDatos
     class Funcion
     class Grupo
     class PermisoExcepcional
   }

   package "Llamadas / IVR" as PL {
     class Llamada
     class Centro
     class Campana
     class Servicio
     class Region
   }

   package "Reportes / Métricas" as PR {
     class Reporte
     class Dashboard
     class Metrica
     class Filtro
   }

   package "Pipeline ETL" as PE {
     class EjecucionETL
     class ErrorETL
     class FilaCargada
     class Scheduler
   }

   package "Alertas / Notificaciones" as PN {
     class Alerta
     class Umbral
     class Suscripcion
     class BuzonInterno
   }

   package "Auditoría" as PD {
     class EventoAuditoria
     class AuditoriaPermiso
     class AuditoriaAcceso
   }
   @enduml

----

4. Verbos del dominio IACT → operaciones
========================================

De la misma conversación extraemos los verbos y los asignamos
preguntando *"¿quién realiza esta acción?"*:

.. list-table::
 :widths: 22 30 48
 :header-rows: 1

 * - Verbo
   - ¿Quién lo hace?
   - Operación
 * - acceder
   - Operador / Supervisor
   - ``Usuario.login()`` (UC_AUTH_01)
 * - ver
   - Operador / Supervisor
   - ``Dashboard.refresh()`` (UC_RPT_01),
     ``Reporte.getResultados()``
 * - buscar / filtrar
   - Sistema / Reporte
   - ``Reporte.aplicarFiltros(filtro : Filtro)``
 * - calcular
   - Métrica
   - ``Metrica.calcularValor(periodo : Rango)``
 * - cargar
   - Pipeline ETL
   - ``EjecucionETL.cargarDesdeIVR()`` (UC_PIP_01)
 * - reintentar
   - AdminPipeline
   - ``EjecucionETL.solicitarReintento()`` (UC_PIP_04)
 * - configurar umbral
   - Supervisor
   - ``Alerta.configurarUmbral(u : Umbral)`` (UC_ALR_01)
 * - disparar
   - Sistema (cron / evaluador)
   - ``Alerta.evaluar()``, ``Alerta.disparar()``
 * - reconocer
   - Supervisor
   - ``Alerta.reconocer()`` (UC_ALR_03)
 * - notificar
   - BuzonInterno
   - ``BuzonInterno.entregar(mensaje)`` (CNST_001)
 * - asignar funciones
   - AdminAcceso
   - ``Usuario.asignarFunciones(funciones)`` (UC_ACC_01)
 * - revocar
   - AdminAcceso
   - ``Usuario.revocarFunciones(funciones)`` (UC_ACC_02)
 * - verificar permiso
   - SecRules
   - ``SecRules.verificarPermiso(funcion)`` (UC_PERM_07)
 * - registrar
   - AuditService
   - ``AuditLog.registrar(evento)`` (CNST_025)
 * - consultar auditoría
   - Auditor
   - ``EventoAuditoria.consultar(filtros)`` (UC_AUD_01)
 * - exportar
   - Operador / Auditor
   - ``Reporte.exportar(formato)`` (UC_RPT_04, UC_AUD_03)

----

5. Adjetivos / contexto → atributos
===================================

De la conversación y restricciones canónicas:

::

 Llamada:
   id, centro_id, campana_id, servicio_id, tipo,
   duracion_seg, tiempo_espera_seg, resultado, fecha
   → "abandonada" / "atendida" → atributo `resultado` (Enum)

 Usuario:
   id, email, password_hash, is_active, segmento,
   created_at, last_login
   → "activo" → `is_active : Boolean`
   → "restringido" → `segmento : SegmentoDatos`

 EjecucionETL:
   id, fecha_inicio, fecha_fin, filas_cargadas,
   errores_count, estado, intentos
   → "fallida" → `estado ∈ {EXITOSA, CON_ERRORES, REINTENTADA}`

 Alerta:
   id, nombre, umbral, severidad, estado,
   fecha_disparo, fecha_reconocimiento
   → "activa / reconocida" → `estado ∈ {ACTIVA, RECONOCIDA}`
   → "INFO / WARNING / CRITICAL" → `severidad : Enum`

 EventoAuditoria:
   id, usuario_id, accion, recurso, detalles_json,
   ip_address, timestamp
   → "inmutable" → CNST_025 (no `update()` / `delete()` ops)

----

6. Ejemplo completo — clase ``Reporte``
=======================================

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class Reporte {
     - id : Integer
     - tipo : Enum
     - nombre : String
     - filtros : Filtro
     - segmento_aplicado : SegmentoDatos
     - generado_at : DateTime
     - ttl_cache : Integer
     + generar(filtros : Filtro) : Reporte
     + exportar(formato : Enum) : Archivo
     + getResultados() : List<Fila>
     + getMetadatos() : Metadatos
     -- responsabilidades --
     Representar un reporte de métricas
     operativas con filtros y segmentación
     aplicados (per BR_012, CNST_008).
   }
   note right of Reporte
     {tipo ∈ DASHBOARD | REAL_TIME |
              HISTORICO | AGENTES |
              COLAS | CAMPANIAS}
     {segmento_aplicado != null}
     {ttl_cache ≤ CNST_017 SLA}
   end note
   @enduml

----

7. Diagrama de clases integrado del dominio IACT
================================================

Vista global con relaciones (extracto cubriendo los seis
paquetes):

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class Usuario
   class Sesion
   class SegmentoDatos
   class Funcion
   class Grupo
   class Llamada
   class Reporte
   class Metrica
   class EjecucionETL
   class ErrorETL
   class Alerta
   class Umbral
   class BuzonInterno
   class EventoAuditoria

   ' RBAC
   Usuario "1" -- "0..1" Sesion           : posee
   Usuario "1" -- "1"   SegmentoDatos     : restringido_por
   Usuario "*" -- "*"   Grupo             : asignado_a
   Grupo   "*" -- "*"   Funcion           : contiene

   ' Llamadas → reportes
   Llamada "0..*" -- "1" SegmentoDatos    : pertenece_a
   Reporte "1"    -- "1..*" Metrica       : contiene
   Reporte "*"    -- "0..*" Llamada       : agrega

   ' Pipeline
   EjecucionETL "1" *-- "0..*" ErrorETL   : compone
   EjecucionETL "0..*" -- "1..*" Llamada  : carga

   ' Alertas
   Alerta "1" -- "1" Umbral               : usa
   Alerta "1" -- "0..*" Usuario           : suscriptos
   Alerta -- BuzonInterno                 : notifica_via

   ' Auditoría
   Usuario "1" -- "0..*" EventoAuditoria  : genera

   note bottom of EventoAuditoria
     CNST_025 — append-only,
     inmutable, sin delete().
   end note
   note right of BuzonInterno
     CNST_001 — sólo buzón
     interno, NO email.
   end note
   @enduml

----

8. Responsabilidades canónicas de las clases IACT
=================================================

::

 Usuario        : representar identidad operativa con segmento
                  y permisos.
 Llamada        : capturar evento del IVR (operacional).
 Reporte        : agregar métricas filtradas por segmento del
                  usuario.
 Metrica        : encapsular cálculo (BR_016/017/018) sobre
                  Llamadas.
 EjecucionETL   : registrar carga del IVR a la BD analítica
                  (ventana 6-12h, CNST_006/008).
 Alerta         : evaluar umbrales y notificar suscriptores
                  vía buzón.
 EventoAuditoria: registrar acciones sensibles, append-only
                  e inmutable (CNST_025).

----

9. Restricciones canónicas del dominio IACT
===========================================

Las restricciones del proyecto se enuncian entre llaves ``{…}``
junto a la clase a la que aplican:

::

 Usuario:
   {email tiene formato válido RFC5322}
   {email es único en el sistema}
   {segmento != null si rol es operativo}        ← BR_012
   {sólo 1 sesión activa por usuario}            ← CNST_002

 Reporte:
   {ttl_cache ≤ SLA según CNST_017}
   {SQL siempre filtrado por segmento}           ← CNST_008
   {throttling distinto por formato}             ← CNST_019/020

 EjecucionETL:
   {ventana de carga: 6 a 12 horas}              ← CNST_008
   {fuente IVR es read-only}                     ← CNST_007
   {no real-time / WS / SSE}                     ← CNST_006

 Alerta:
   {notificación vía buzón interno, no email}    ← CNST_001
   {severidad ∈ INFO | WARNING | CRITICAL}

 EventoAuditoria:
   {append-only — no update / delete}            ← CNST_025
   {sin PII en logs}                             ← CNST_026

----

10. Aplicación a UCs específicos del catálogo
=============================================

Para cada UC del catálogo IACT, el análisis de dominio produce:

**UC_RPT_01 (Ver Dashboard)**
::

 Sustantivos: Operador, Dashboard, Reporte, Metrica, Llamada,
              SegmentoDatos
 Verbos:      ver, refrescar, calcular, filtrar
 Clases:      Dashboard, Reporte, Metrica, Filtro
 Operaciones: Dashboard.refresh(), Reporte.generar(filtros)

**UC_PIP_01 (Supervisar ETL)**
::

 Sustantivos: AdminPipeline, EjecucionETL, ErrorETL,
              Scheduler, IVR
 Verbos:      supervisar, consultar, ver estado
 Clases:      EjecucionETL, ErrorETL, SupervisorETL
 Operaciones: EjecucionETL.estado(),
              SupervisorETL.ultimaEjecucion()

**UC_ALR_03 (Reconocer Alerta)**
::

 Sustantivos: Supervisor, Alerta, BuzonInterno,
              Suscriptor, AuditLog
 Verbos:      reconocer, notificar, registrar
 Clases:      Alerta, BuzonInterno, EventoAuditoria
 Operaciones: Alerta.reconocer(), BuzonInterno.entregar()

**UC_PERM_07 (Verificar Permiso de Usuario)**
::

 Sustantivos: SecRules, Usuario, Funcion, Grupo,
              PermisoExcepcional, AuditoriaPermiso
 Verbos:      verificar, evaluar, registrar
 Clases:      SecRules, AuditoriaPermiso
 Operaciones: SecRules.verificarPermiso(usuario, funcion)
              → SQL nativa usuario_tiene_permiso()

**UC_AUD_01 (Consultar Auditoría)**
::

 Sustantivos: Auditor, EventoAuditoria, Filtro
 Verbos:      consultar, filtrar, exportar
 Clases:      EventoAuditoria, AuditService
 Operaciones: EventoAuditoria.consultar(filtros),
              AuditService.exportar(formato)

----

11. Decisiones por aplicar a cada uno de los 97 UCs
===================================================

Para cada UC, ejecutar la metodología:

1. **Recopilación** — entrevista con stakeholder o lectura
   del UC original.
2. **Sustantivos → clases** — listar todos los sustantivos
   relevantes al dominio IACT (no incluir detalle físico del
   IVR).
3. **Verbos → operaciones** — extraer y asignar a la clase
   responsable de cada acción.
4. **Adjetivos → atributos** — incluir tipo y valor por
   defecto donde aplique.
5. **Asociaciones** — definir cardinalidad (1:1, 1:*, *:*).
6. **Responsabilidades + restricciones** — citar BRs y CNSTs
   aplicables.

  Estos seis pasos son **idénticos** a los del checklist § 8 de
  :doc:`/normativa/estandares/metodologia-analisis-dominio-ucs`.
  Este documento provee los **ejemplos canónicos del dominio
  IACT**.

----

12. Trazabilidad
================

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Skill aplicada**
   - ``ba-elicitation`` (BABOK — Elicitation and Collaboration)
 * - **Origen del documento**
   - Reescrito de "GUÍA-ANÁLISIS-DOMINIO-SUSTANTIVOS-VERBOS"
     (cheat-sheet aplicado interno con dominio ecommerce),
     **reorientado al dominio real IACT** (call center IVR +
     analytics + RBAC + ETL).
 * - **Teoría genérica**
   - :doc:`/base-cognitiva/_uml/uml-03-uso-orientacion-objetos`
     (Schmuller Hora 3)
 * - **Metodología del proyecto**
   - :doc:`/normativa/estandares/metodologia-analisis-dominio-ucs`
 * - **Catálogo modular del dominio IACT**
   - :doc:`/gestion/evidencia/arquitectura-modular/analisis-catalogo-modular-iact`
 * - **Modelo RBAC vigente**
   - :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact`
 * - **Ejemplos hermanos aplicados a IACT**
   - :doc:`diagramas-uml`,
     :doc:`orientacion-objetos`
 * - **Plan de documentación**
   - :doc:`plan-documentacion-uc`
 * - **Plantilla canónica de UC**
   - :doc:`/normativa/estandares/plantillas/tpl-uc-spec-con-diagramas-uml`
 * - **BRs aplicables citadas**
   - BR_012 (segmento único), BR_016 (tasa abandono),
     BR_017 (tiempo promedio espera), BR_018 (índice
     eficiencia).
 * - **CNSTs aplicables citadas**
   - CNST_001 (no email), CNST_002 (sesión única),
     CNST_006/007/008 (BD dual + IVR readonly + ventana ETL),
     CNST_017 (SLA), CNST_019/020 (export async + throttling),
     CNST_025 (auditoría inmutable), CNST_026 (no PII).
 * - **Política de diagramación**
   - :doc:`/base-cognitiva/plantuml-guide/guidelines`
