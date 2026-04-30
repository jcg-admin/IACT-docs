.. meta::
 :artefacto: EJEMPLOS_OOP_APLICADOS_IACT
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
Principios OOP aplicados al dominio IACT (PlantUML)
==================================================================

.. note::

 Compañero del :doc:`/gestion/pm/plan-documentacion-uc-con-uml`
 y de :doc:`/normativa/estandares/metodologia-oop-para-ucs`.

 Muestra los **6 principios OOP** aplicados al **dominio real
 del proyecto IACT**: call center IVR + analytics +
 supervisión ETL + RBAC granular. **No** es ecommerce.

 Sirve como **referencia de precedente**: cada UC documentado
 debe aplicar las 6 dimensiones OOP con el nivel de detalle
 mostrado en estos ejemplos, usando la nomenclatura real del
 catálogo (``UC_ACC``, ``UC_AUTH``, ``UC_USR``, ``UC_PERM``,
 ``UC_RPT``, ``UC_ALR``, ``UC_PIP``, ``UC_AUD``, ``UC_LOG``).

 Diagramas en **PlantUML** (política del proyecto, no Mermaid).

----

1. Dominio IACT — vocabulario base
==================================

Antes de aplicar los 6 principios, recordá los conceptos del
dominio (per
:doc:`/gestion/evidencia/arquitectura-modular/analisis-catalogo-modular-iact`):

.. list-table::
 :widths: 22 78
 :header-rows: 1

 * - Concepto
   - Significado en IACT
 * - **Llamada / IVR**
   - Interacción telefónica capturada por el conmutador IVR;
     fuente operacional de los datos.
 * - **Métrica operativa**
   - Indicador derivado de las llamadas (tasa de abandono,
     tiempo promedio de espera, índice de eficiencia).
 * - **Función**
   - Capacidad atómica del RBAC (``view_dashboard``,
     ``manage_sessions``, ``export_csv``, etc.). 42 en total.
 * - **Grupo de funciones**
   - Conjunto agrupado de funciones (predefinido AGR-001..010
     o creable por admin).
 * - **Permiso temporal / excepcional**
   - Asignación con justificación + vencimiento ≤ 6 meses.
 * - **Segmento de datos**
   - Subconjunto de IVR autorizado a un usuario (centro,
     campaña, servicio, región).
 * - **Pipeline ETL**
   - Proceso batch que carga IVR → BD analítica (ventana 6-12 h,
     no real-time).
 * - **Auditoría**
   - Registro inmutable append-only de acciones (UC_AUD) y de
     verificaciones de permiso (``AuditoriaPermiso``,
     UC_PERM_09).

----

2. Abstracción
==============

**Definición:** quitar propiedades y acciones innecesarias,
dejar sólo lo esencial al problema que se resuelve.

2.1 Antipatrón — exceso de detalle físico
-----------------------------------------

Si quisieras modelar EXACTAMENTE cada llamada IVR con todo su
detalle eléctrico:

::

 Llamada (modelo perfectamente físico):
   - Códec usado en cada tramo
   - Latencia milisegundo a milisegundo
   - Pérdida de paquetes en cada hop
   - Voltaje de la línea
   - Modulación del DTMF
   - Frecuencia de muestreo del audio
   - Buffer del jitter
   - ... 50 atributos más

**Problema:** excesivo para un sistema de **analytics**. Estos
datos pertenecen al operador IVR, no al consumidor de
métricas.

2.2 Abstracción correcta para IACT
----------------------------------

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
     + getTipo() : Enum
     + esAbandonada() : Boolean
   }
   note right of Llamada
     Abstracción para analytics:
     sólo atributos relevantes para
     calcular métricas (BR_016 tasa
     de abandono, BR_017 tiempo
     promedio de espera, BR_018
     índice de eficiencia).
   end note
   @enduml

2.3 Decisiones de abstracción en IACT (97 UCs)
----------------------------------------------

**Pregunta para cada clase del dominio:**

- ¿Es relevante para calcular métricas operativas? → incluir.
- ¿Es relevante para verificar permisos en runtime? → incluir.
- ¿Es relevante para auditar acciones? → incluir.
- ¿Es detalle de la red telefónica / del IVR físico? →
  **excluir**.

**Modelos abstraídos:**

- ``Usuario`` (UC_USR / UC_AUTH) — sólo email, hash de
  contraseña, segmento, sesiones activas. **No** cifrado de
  línea.
- ``Llamada`` (consumida por UC_RPT / UC_ALR) — sólo
  duración, tipo, resultado, segmento. **No** códecs ni
  voltajes.
- ``Funcion`` (UC_PERM / UC_ACC) — sólo código, descripción,
  módulo. **No** representación SQL interna.
- ``EjecucionETL`` (UC_PIP) — sólo fecha de inicio, duración,
  filas cargadas, errores. **No** logs de cada query
  individual.

----

3. Herencia
===========

**Definición:** una subclase reutiliza atributos y operaciones
de su superclase. *"Es un tipo de"*.

3.1 Jerarquía de actores IACT
-----------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class Usuario {
     - id : Integer
     - email : String
     - password_hash : String
     - is_active : Boolean
     - segmento : SegmentoDatos
     - created_at : DateTime
     + login(email, password) : Boolean
     + logout() : void
     + changePassword(old, new) : void
   }

   class Operador {
     + verDashboard() : Dashboard
     + verAlertasActivas() : List<Alerta>
   }

   class Supervisor {
     - centros : List<Integer>
     + verReportesHistoricos() : List<Reporte>
     + reconocerAlerta(id) : void
   }

   class AdminAcceso {
     + asignarFunciones(usuario, funciones) : void
     + asignarAgrupador(usuario, AGR_id) : void
     + concederPermisoTemporal(...) : void
   }

   class AdminPipeline {
     + supervisarETL() : EstadoETL
     + solicitarReintento(ejecucion_id) : void
   }

   class Auditor {
     + consultarAuditoria(filtros) : List<EventoAud>
     + generarReporteCompliance() : Reporte
   }

   Usuario <|-- Operador
   Usuario <|-- Supervisor
   Usuario <|-- AdminAcceso
   Usuario <|-- AdminPipeline
   Usuario <|-- Auditor

   note right of Usuario
     Herencia: cada rol "es un tipo
     de" Usuario. Todos heredan
     login(), logout(),
     changePassword(). El segmento
     restringe los datos visibles
     (BR_012).
   end note
   @enduml

3.2 Ventaja en IACT
-------------------

::

 Sin herencia (repetición):
   Operador:        email, password, segmento, login(), logout()
   Supervisor:      email, password, segmento, login(), logout()
   AdminAcceso:     email, password, segmento, login(), logout()
   ...

 Con herencia (reutilización):
   Usuario:        email, password, segmento, login(), logout()
     Operador     (+ verDashboard, verAlertas)
     Supervisor   (+ reportes históricos, reconocer)
     AdminAcceso  (+ asignar/revocar funciones)
     AdminPipeline(+ supervisar ETL, reintento)
     Auditor      (+ consultar / exportar auditoría)

3.3 Otras jerarquías canónicas IACT
-----------------------------------

- ``Reporte`` (base) → ``ReporteRealTime`` (UC_RPT_02),
  ``ReporteHistorico`` (UC_RPT_03), ``ReporteAgentes``
  (UC_RPT_12), ``ReporteColas`` (UC_RPT_13),
  ``ReporteCampanias`` (UC_RPT_14).
- ``Alerta`` (base) → ``AlertaUmbral``, ``AlertaTendencia``,
  ``AlertaConsolidada`` con severidades ``INFO`` /
  ``WARNING`` / ``CRITICAL``.
- ``EventoAuditoria`` (base) → ``AuditoriaAcceso`` (UC_AUD),
  ``AuditoriaPermiso`` (UC_PERM_09),
  ``AuditoriaCambioAcceso`` (UC_ACC_09) — distinguidos por
  origen pero con misma política inmutable per CNST_025.
- ``EjecucionETL`` (base) → ``EjecucionExitosa``,
  ``EjecucionConErrores``, ``EjecucionReintentada``.

----

4. Polimorfismo
===============

**Definición:** mismo nombre de operación, diferente
implementación según la clase.

4.1 ``calcularValor()`` polimórfico en métricas IACT
----------------------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   abstract class Metrica {
     - nombre : String
     - segmento : SegmentoDatos
     + calcularValor(periodo : Rango) : Decimal
   }

   class TasaAbandono {
     + calcularValor(periodo : Rango) : Decimal
   }

   class TiempoPromedioEspera {
     + calcularValor(periodo : Rango) : Decimal
   }

   class IndiceEficiencia {
     - peso_atendidas : Decimal
     - peso_tiempo : Decimal
     + calcularValor(periodo : Rango) : Decimal
   }

   Metrica <|-- TasaAbandono
   Metrica <|-- TiempoPromedioEspera
   Metrica <|-- IndiceEficiencia

   note right of Metrica
     Polimorfismo (BR_016, BR_017, BR_018):
       TasaAbandono           → abandonadas / total × 100
       TiempoPromedioEspera   → SUM(esperas) / N
       IndiceEficiencia       → fórmula compuesta
                                ponderada por servicio
   end note
   @enduml

4.2 ``exportar()`` polimórfico per CNST_019/020
-----------------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   abstract class Exportador {
     - reporte : Reporte
     + exportar() : Archivo
   }

   class ExportadorCSV {
     + exportar() : Archivo
   }
   class ExportadorExcel {
     + exportar() : Archivo
   }
   class ExportadorPDF {
     + exportar() : Archivo
   }

   Exportador <|-- ExportadorCSV
   Exportador <|-- ExportadorExcel
   Exportador <|-- ExportadorPDF

   note right of Exportador
     CNST_019 — exportaciones
     asíncronas para sets > 10k filas.
     CNST_020 — throttling distinto
     por formato:
       CSV   100k/10 día
       Excel  50k/5 día
       PDF    10k/3 día
   end note
   @enduml

4.3 Operaciones polimórficas en IACT (97 UCs)
---------------------------------------------

- ``calcularValor()`` — distinto por tipo de métrica
  (UC_RPT_01, UC_RPT_02, UC_RPT_03).
- ``exportar()`` — distinto por formato CSV/Excel/PDF
  (UC_RPT_04..06, CNST_019/020).
- ``verificar_permiso()`` — distinto si la fuente es
  asignación de grupo, asignación directa o permiso
  excepcional (UC_PERM_07).
- ``notificar()`` — distinto para alerta de umbral, alerta de
  tendencia, alerta de pipeline (UC_ALR_02, UC_PIP_02). Sin
  email, **sólo buzón interno** per CNST_001.

----

5. Encapsulamiento
==================

**Definición:** ocultar la complejidad interna y mostrar sólo
la interfaz pública.

5.1 Clase ``Reporte`` (UC_RPT)
------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class Reporte {
     == interfaz pública ==
     + generar(filtros : FiltroReporte) : Reporte
     + exportar(formato : Enum) : Archivo
     + getResultados() : List<Fila>
     + getMetadatos() : Metadatos
     == privado / oculto ==
     - validarSegmentoUsuario()
     - construirQuerySQL()
     - aplicarFiltrosPorSegmento()
     - cachearResultado()
     - registrarConsulta()
     - aplicarThrottling(formato)
   }
   note right of Reporte
     El cliente sólo ve:
       generar(), exportar(),
       getResultados(),
       getMetadatos()
     El sistema gestiona internamente:
       segmentación (CNST_008), SQL,
       cache, auditoría, throttling
       (CNST_020).
   end note
   @enduml

5.2 Ventaja del encapsulamiento en IACT
---------------------------------------

::

 Reporte v1.0:
   resultados = ejecutar SQL crudo

 Reporte v2.0 (cambio interno tras CNST_017 — SLAs):
   resultados = ejecutar SQL → cache → throttling
                → segmentación CNST_008

 Resultado: el código de UC_RPT_01..14 NO CAMBIA,
 porque getResultados() siempre devuelve la lista
 correcta independientemente del mecanismo interno.

5.3 Interfaz pública vs privada — dominio IACT
----------------------------------------------

**Lo que ve el operador (interfaz pública):**

::

 Operador (UC_RPT):
   reporte.generar(filtros)
   reporte.exportar("csv")
   reporte.getResultados()

 Admin acceso (UC_ACC):
   asignarFunciones(usuario, funciones)
   asignarAgrupador(usuario, AGR-007)

 Auditor (UC_AUD):
   consultarAuditoria(filtros)
   exportarAuditoria(formato)

**Lo que NO ve (complejidad privada del backend):**

- Validación del segmento del usuario contra el dato
  consultado (CNST_008, BR_012).
- Construcción y caching de queries SQL.
- Throttling por formato (CNST_019/020).
- Verificación SoD en cada asignación (CNST_030).
- Persistencia inmutable de auditoría (CNST_025) — no se
  puede borrar.
- Hasheo de PII en logs (CNST_026).

----

6. Envío de mensajes
====================

**Definición:** un objeto solicita a otro que ejecute una
operación.

6.1 Generar reporte — UC_RPT_01 (ver dashboard)
-----------------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   participant ":Operador"   as O
   participant ":Dashboard"  as D
   participant ":Reporte"    as R
   participant ":SecRules"   as SR
   participant ":BDAnalytics" as BD

   O  -> D  : 1. abrirDashboard()
   D  -> R  : 2. generar(filtros)
   R  -> SR : 3. verificarPermiso(view_dashboard)
   SR --> R : 4. autorizado + segmento del usuario
   R  -> BD : 5. SELECT con filtro de segmento
   BD --> R : 6. filas
   R  --> D : 7. resultados
   D  --> O : 8. dashboard renderizado
   @enduml

6.2 Solicitar reintento ETL — UC_PIP_04
---------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   participant ":AdminPipeline" as AP
   participant ":SupervisorETL" as Sup
   participant ":SchedulerETL" as Sch
   participant ":AuditLog"     as AL

   AP  -> Sup  : 1. solicitarReintento(ejecucion_id)
   Sup -> Sup  : 2. validarEstado(FALLIDA)
   Sup -> Sch  : 3. enqueueReintento(jobId)
   Sch --> Sup : 4. jobEncolado
   Sup -> AL   : 5. registrar(REINTENTO_SOLICITADO)
   Sup --> AP  : 6. confirmación + ETA
   @enduml

6.3 Múltiples interfaces, mismo mensaje
---------------------------------------

Un objeto puede recibir el mismo mensaje por **diferentes
interfaces**:

::

 Reporte:
   Interfaz Web    — operador clic "Generar"      → generar()
   Interfaz API    — sistema externo POST /reports → generar()
   Interfaz Cron   — scheduler dispara reporte
                     programado (UC_RPT_07)        → generar()

 Resultado: 3 interfaces, 1 operación generar().

6.4 Flujos de mensajes en los 97 UCs
------------------------------------

- UC_AUTH_01 (Iniciar sesión) → ``AuthService.login()`` →
  ``SessionStore.create()`` con throttling CNST_011.
- UC_RPT_01 (Ver dashboard) → ``Dashboard.refresh()`` →
  ``Reporte.generar()`` con filtro de segmento BR_012.
- UC_PIP_01 (Supervisar ETL) → ``SupervisorETL.estado()`` →
  ``SchedulerETL.last_run()``.
- UC_PERM_07 (Verificar permiso) → función SQL nativa
  ``usuario_tiene_permiso()``.
- UC_ALR_03 (Reconocer alerta) → ``Alerta.reconocer()`` →
  ``BuzonInterno.notificar()`` (CNST_001 sin email).

----

7. Asociaciones y agregación
============================

7.1 Asociaciones canónicas IACT
-------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class Usuario
   class Sesion
   class Grupo
   class Funcion
   class SegmentoDatos
   class Reporte
   class Alerta

   Usuario "1" -- "0..1" Sesion          : posee
   Usuario "1" -- "1"   SegmentoDatos    : restringido_por
   Usuario "*" -- "*"   Grupo            : asignado_a
   Grupo   "*" -- "*"   Funcion          : contiene
   Usuario "1" -- "0..*" Reporte         : consulta
   Usuario "1" -- "0..*" Alerta          : suscrito_a

   note right of Usuario
     - Usuario posee 0..1 Sesion          (CNST_002)
     - Usuario tiene 1 segmento           (BR_012)
     - Usuario en 0..* grupos             (UC_PERM_01)
     - Grupo contiene 0..* funciones      (UC_PERM_06)
     - Usuario consulta 0..* reportes     (UC_RPT)
     - Usuario suscrito a 0..* alertas    (UC_ALR_05)
   end note
   @enduml

7.2 Agregación vs composición en IACT
-------------------------------------

**Agregación** — las partes pueden existir sin el todo:

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class Grupo
   class Funcion
   Grupo "*" o-- "*" Funcion : contiene
   note right of Funcion
     Una función (capacidad atómica)
     puede ser parte de varios grupos
     (predefinidos AGR-001..010 o
     creados via UC_PERM_05). Si un
     grupo se elimina, las funciones
     siguen existiendo en el catálogo.
   end note
   @enduml

**Composición** — las partes no pueden existir sin el todo:

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class EjecucionETL
   class ErrorETL
   class FilaCargada
   EjecucionETL "1" *-- "0..*" ErrorETL    : compone
   EjecucionETL "1" *-- "0..*" FilaCargada : compone
   note right of EjecucionETL
     Si la EjecucionETL se purga
     (UC_PIP), sus errores y filas
     cargadas no tienen sentido
     fuera de ella.
   end note
   @enduml

7.3 Aplicación en el proyecto IACT
----------------------------------

**Agregación** (parte puede existir sin el todo):

- ``Grupo`` ↔ ``Funcion`` — la función vive en el catálogo
  aunque el grupo se borre.
- ``Suscripcion`` ↔ ``Alerta`` — la alerta sigue activa
  aunque un suscriptor se desuscriba (UC_ALR_05).

**Composición** (parte no existe sin el todo):

- ``EjecucionETL`` → ``ErrorETL`` (UC_PIP_02): errores ligados
  a una ejecución concreta.
- ``Reporte`` → ``FilaResultado`` — una fila no tiene sentido
  fuera del reporte que la generó.
- ``EventoAuditoria`` → ``DetalleAuditoria`` — el detalle
  inmutable se ata al evento (CNST_025).

----

8. Resumen visual de los 6 principios
=====================================

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   skinparam packageStyle rectangle
   rectangle "Orientación a Objetos en IACT" as OOP {
     rectangle "1. ABSTRACCIÓN\nLlamada / Métrica / Función\nsin ruido físico"             as P1
     rectangle "2. HERENCIA\nUsuario → Operador,\nSupervisor, Auditor..."                  as P2
     rectangle "3. POLIMORFISMO\ncalcularValor() por métrica\nexportar() por formato"      as P3
     rectangle "4. ENCAPSULAMIENTO\ngenerar() público,\nsegmentación interna"              as P4
     rectangle "5. MENSAJES\nOperador → Dashboard\n→ Reporte → SecRules → BD"              as P5
     rectangle "6. ASOCIACIONES\nUsuario 1:1 Sesion;\nGrupo *:* Funcion (agregación);\nEjecucionETL 1:* ErrorETL (composición)" as P6
   }
   @enduml

----

9. Cómo se aplica todo en conjunto — UC ejemplo
===============================================

UC_RPT_01 (Ver Dashboard) en términos OOP:

::

 1. ABSTRACCIÓN
    Reporte modela sólo lo necesario para mostrar métricas
    al operador (no detalles de ETL ni del IVR físico).

 2. HERENCIA
    Reporte (base) → ReporteRealTime, ReporteHistorico,
    ReporteAgentes, ReporteColas, ReporteCampanias.

 3. POLIMORFISMO
    calcularValor() distinto por métrica (BR_016 / BR_017 /
    BR_018). exportar() distinto por formato (CSV / Excel /
    PDF, CNST_019/020).

 4. ENCAPSULAMIENTO
    Operador ve: generar(), exportar(), getResultados().
    Backend gestiona: validación de segmento (CNST_008),
    construcción de SQL, caching, throttling, auditoría.

 5. MENSAJES
    Operador → Dashboard → Reporte → SecRules → BDAnalytics.

 6. ASOCIACIONES
    Usuario 1:1 SegmentoDatos (BR_012);
    Reporte 0..* FilaResultado (composición);
    Usuario 0..* Reporte (consulta).

----

10. Decisiones por aplicar a cada UC del catálogo IACT
======================================================

Para cada uno de los UCs del catálogo (UC_ACC, UC_AUTH,
UC_USR, UC_PERM, UC_RPT, UC_ALR, UC_PIP, UC_AUD, UC_LOG),
preguntarse:

1. **Abstracción** — ¿qué del dominio IVR / RBAC / ETL incluir
   o excluir?
2. **Herencia** — ¿hay reutilización con otros UC? (ej.: todos
   los UC_RPT comparten ``generar()`` / ``exportar()``).
3. **Polimorfismo** — ¿hay variantes del comportamiento?
   (formato de exportación, fuente de permiso, tipo de
   métrica).
4. **Encapsulamiento** — ¿qué expone la interfaz pública vs
   qué gestiona el backend (segmentación, SoD, auditoría)?
5. **Mensajes** — ¿qué objetos se comunican y en qué orden?
6. **Asociaciones** — ¿qué relaciones con otros UCs?
   (UC_AUTH precede UC_RPT; UC_PERM_07 valida cada acceso).

  Estas seis preguntas son **idénticas** a las dimensiones del
  checklist § 6 de
  :doc:`/normativa/estandares/metodologia-oop-para-ucs`. Este
  documento provee los **ejemplos canónicos del dominio IACT**
  que cada UC debe emular en estilo y nivel de detalle.

----

11. Trazabilidad
================

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Skill aplicada**
   - ``ba-requirements-analysis`` (BABOK — RADD)
 * - **Origen del documento**
   - Adaptado de "GUÍA-OOP-PRINCIPIOS-CORE — Aplicados al
     dominio E-commerce" (cheat-sheet aplicado interno),
     reescrito en PlantUML **y reorientado al dominio real
     IACT** (call center IVR + analytics + RBAC + ETL).
 * - **Teoría OOP genérica**
   - :doc:`/base-cognitiva/_uml/uml-02-orientacion-objetos`
     (Schmuller Hora 2)
 * - **Metodología OOP del proyecto**
   - :doc:`/normativa/estandares/metodologia-oop-para-ucs`
 * - **Catálogo modular del dominio IACT**
   - :doc:`/gestion/evidencia/arquitectura-modular/analisis-catalogo-modular-iact`
 * - **Modelo RBAC vigente**
   - :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact`
 * - **Plan de documentación**
   - :doc:`plan-documentacion-uc-con-uml`
 * - **Plantilla canónica de UC**
   - :doc:`/normativa/estandares/plantillas/tpl-uc-spec-con-diagramas-uml`
 * - **BRs aplicables citadas**
   - BR_012 (segmento único), BR_016 (tasa abandono),
     BR_017 (tiempo promedio espera), BR_018 (índice
     eficiencia).
 * - **CNSTs aplicables citadas**
   - CNST_001 (no email), CNST_002 (sesión única), CNST_008
     (filtrado por segmento), CNST_011 (throttling), CNST_017
     (SLA), CNST_019/020 (export async + throttling),
     CNST_025 (auditoría inmutable), CNST_026 (no PII),
     CNST_030 (SoD).
 * - **Política de diagramación**
   - :doc:`/base-cognitiva/plantuml-guide/guidelines`
