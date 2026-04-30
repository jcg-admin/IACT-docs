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

 Compañero del :doc:`/requisitos/_metodologia-aplicacion/plan-documentacion-uc`
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

11. Acoplamiento — interdependencia entre clases
================================================

El **acoplamiento** mide el grado de interdependencia entre
objetos y clases. Es el complemento de la cohesión: una OOP
sana en IACT busca **alta cohesión dentro** de cada clase
y **bajo acoplamiento entre** clases.

Criterios canónicos
-------------------

1. **Mínimo acoplamiento posible por interacción**
   (uso o paso de mensajes). Si una clase está conectada con
   muchas otras, aunque internamente esté bien aislada, se
   produce el efecto *rippling*: una modificación en esa
   clase resuena en todo el sistema. En IACT esto aparece
   típicamente cuando ``rpt_app`` consume directamente
   modelos internos de ``perm_app`` o ``aud_app`` saltándose
   ``services.py``; lo correcto es comunicarse vía las
   interfaces ``ISecurity`` y ``IAuditLog``
   (ver :doc:`diagramas-componentes`).

2. **Máximo acoplamiento por herencia**. Cuando una clase
   hereda, debe aprovechar **todo** lo del padre y extenderlo
   tanto como sea necesario. Una herencia que solo reutiliza
   una porción mínima del padre es señal de que la jerarquía
   está mal modelada — frecuentemente conviene reemplazarla
   por composición. En IACT: ``ReporteVolumen`` y
   ``ReporteAbandono`` heredan de ``Reporte`` y reutilizan
   ``generar()``, ``exportar()``, ``aplicar_filtros_segmento()``
   (BR_012) — no solo uno de ellos.

3. **Evitar el acoplamiento *pass-through***. Si un objeto
   intermediario solo reenvía mensajes sin agregar lógica,
   un cambio de firma obliga a modificar **tres** clases
   (origen, intermediario y destino). La regla: pedir
   directamente al objeto que tiene la información.

   En IACT este antipatrón aparece cuando una vista llama a
   ``rpt_app`` que llama a ``aud_app`` solo para obtener un
   evento previamente registrado. Lo correcto: la vista
   consulta ``aud_app`` directamente cuando el dato es de
   auditoría — sin intermediario.

Contraste *pass-through* vs acceso directo
-------------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   title Antipatron pass-through (evitar)
   class Vista
   class RptApp {
     + ultimo_evento_aud(user)
   }
   class AudApp {
     + ultimo_evento(user)
   }
   Vista --> RptApp : ultimo_evento_aud(user)
   RptApp --> AudApp : ultimo_evento(user)
   note right of RptApp
     RptApp no agrega logica:
     solo reenvia. Cambio de
     firma obliga a tocar
     Vista, RptApp y AudApp.
   end note
   @enduml

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   title Acceso directo (correcto)
   class Vista
   class AudApp {
     + ultimo_evento(user)
   }
   Vista --> AudApp : ultimo_evento(user)
   note right of Vista
     Cambio de firma solo
     obliga a tocar Vista y
     AudApp. RptApp queda
     fuera del cambio.
   end note
   @enduml

Reglas IACT derivadas
---------------------

- Cada app Django expone su contrato vía ``services.py``;
  el resto del sistema **no consume modelos cruzados** de
  otra app directamente.
- Cualquier intermediario que solo redirija debe ser
  refactorizado o justificarse en un ADR.
- Las herencias de ``Reporte`` / ``Alerta`` / ``EventoAud``
  deben reutilizar la mayor parte del padre. Si no lo
  hacen, romper la jerarquía y modelar con composición.

----

12. Antipatrón: Descomposición funcional
========================================

William Brown, en *AntiPatterns*, describe la
**descomposición funcional** como el antipatrón en el que
el desarrollador estructura un sistema OOP como si fuera un
programa procedural tradicional, ignorando los beneficios y
principios fundamentales de la orientación a objetos.

Síntomas
--------

- **Nombres de clase que reflejan funciones, no entidades**.
  En IACT este síntoma aparece cuando, en lugar de
  ``Reporte`` y ``Permiso`` (entidades del dominio), se
  proponen clases como ``CalcularReporte``,
  ``ProcesarExportacion``, ``ValidarPermiso``.
- **Clases con un único método**, generalmente llamado
  ``ejecutar``, ``procesar`` o ``correr``. Indica que la
  clase es realmente una función disfrazada.
- **Uso excesivo de miembros estáticos** — la clase se
  convierte en un namespace de funciones en lugar de una
  plantilla para crear objetos. En Django esto aparece
  cuando ``services.py`` solo expone ``staticmethod`` sin
  estado, mientras la lógica del dominio (estados,
  invariantes, contratos) queda fuera del modelo.
- **Ausencia de principios OOP**: sin herencia para
  jerarquías "es-un", sin polimorfismo para variantes de
  comportamiento, sin encapsulamiento para proteger
  invariantes.

Consecuencias
-------------

Brown señala que el código en este antipatrón se vuelve:

- **Imposible de comprender** — la lógica está dispersa y
  no refleja el modelo del dominio. En IACT esto rompe la
  trazabilidad UC ↔ código.
- **Difícil de reutilizar** — funcionalidades fuertemente
  acopladas que no encajan en otra app Django sin
  reescritura.
- **Complicado de probar** — sin encapsulamiento y con
  alta dependencia entre componentes, los tests requieren
  fixtures gigantes para cada caso.

En IACT, además, el antipatrón **rompe el contrato del
audit**: si la lógica de negocio vive en funciones sueltas
sin estado, los eventos auditables (CNST_025) se registran
desde múltiples puntos no canónicos y se vuelven
incompletos.

Solución — Modelo del dominio orientado a objetos
-------------------------------------------------

1. Identificar las **entidades reales** del dominio del
   problema (sustantivos del experto del dominio — ver
   :doc:`analisis-dominio`).
2. Modelar esas entidades como clases con
   **responsabilidades bien definidas** (RDD,
   :doc:`analisis-dominio` § 12.3).
3. Establecer **relaciones naturales** entre las clases
   reflejando las relaciones del mundo real
   (asociaciones, agregación, composición — ver
   :doc:`relaciones-uml`,
   :doc:`agregacion-interfaces`).
4. Aplicar **patrones de diseño** apropiados para
   resolver problemas comunes — ver
   :doc:`patrones-diseno`.

Cuándo aparece típicamente en IACT
-----------------------------------

- Migraciones de scripts ETL legados a ``pip_app`` —
  tendencia a copiar el flujo procedural sin modelar
  ``EjecucionETL`` y ``VentanaETL`` como entidades.
- Vistas Django con lógica de negocio inline en lugar
  de delegar al modelo o a ``services.py``.
- Cálculo de métricas BR_016/017/018 implementado como
  funciones sueltas en lugar de en ``Reporte`` y sus
  subclases polimórficas.

Heurística rápida para detectarlo
---------------------------------

Si una clase IACT no tiene atributos de estado y solo
expone un método ``run``/``ejecutar``/``procesar``, casi
seguro es una función disfrazada. Refactorizar a entidad
del dominio o a función pura — pero no dejarla como clase
fingida.

----

13. Ciclo de vida basado en prototipos
======================================

El enfoque sustantivos→clases del documento
:doc:`analisis-dominio` se complementa naturalmente con un
**ciclo de vida basado en prototipos**: construir desde el
inicio un prototipo que se enriquece progresivamente por
herencia y especialización, en vez de redactar
especificaciones extensas antes de cualquier ejecución.

Por qué tiene sentido en IACT
-----------------------------

La especificación textual pura, aplicada por sí sola,
plantea dos problemas:

1. **Es poco precisa**. Dos personas pueden entender un
   concepto aparentemente claro de manera diferente. En
   IACT, "tasa de abandono" puede interpretarse como
   abandono **antes** de cola, **dentro** de cola, o por
   timeout sistémico — la diferencia se vuelve evidente
   solo cuando alguien la implementa.
2. **Los objetivos no son siempre claros**. IACT no es un
   sistema que mecaniza tareas manuales por primera vez;
   es una segunda generación que pretende **mejorar** un
   proceso ya existente. Cuando un stakeholder pide
   "mejor visibilidad de los segmentos" o "alertas más
   accionables", traducir esas peticiones a
   funcionalidades concretas es difícil, y el mejor
   enfoque suele ser la **experimentación**.

Por qué OOP hace viable el prototipado
--------------------------------------

Históricamente, los prototipos se construían en lenguajes
de muy alto nivel y, una vez validados, debían
**desecharse** para reescribir la aplicación en un lenguaje
de producción — un coste que solo se asumía en proyectos
excepcionales.

OOP cambia el balance: con **herencia**, **librerías de
clases** y **refinamiento por especialización**, un
prototipo válido **no tiene que tirarse**. Lo que se valida
en el prototipo se conserva como base; las clases se
extienden o sustituyen sin reescribir el sistema entero.

Aplicación en IACT
------------------

- En cada UC nuevo, antes de invertir en una
  especificación de 13 secciones (ver
  :doc:`casos-uso-especificacion`), conviene un prototipo
  ejecutable mínimo del flujo nominal — incluso si solo
  cubre el escenario feliz.
- El prototipo se construye sobre las clases del dominio
  IACT (``Reporte``, ``Alerta``, ``Sesion``, etc.) y se
  refina por herencia (``ReporteVolumen`` ←
  ``Reporte``).
- Los aprendizajes del prototipo se incorporan a la
  especificación; la especificación deja de ser un acto
  de fe y pasa a documentar comportamiento ya observado.
- El prototipo **no es desechable**: las clases probadas
  pasan a producción tras revisión y ajuste, no tras
  reescritura.

Restricciones
-------------

El prototipado no exime al equipo de:

- Validar contra restricciones del proyecto (CNST_*) y
  reglas de negocio (BR_*).
- Cumplir el stack canónico ADR_DEVOPS_001 — un prototipo
  que solo funciona en Docker o con Nginx no es un
  prototipo válido para IACT.
- Auditar cada iteración (CNST_025) cuando el prototipo
  toca datos reales o réplicas operativas.

Relación con las escuelas de análisis
-------------------------------------

Prototipado y análisis no compiten: el análisis
sustantivos→clases / RDD identifica las entidades y
contratos que el prototipo materializa. El prototipo, a su
vez, **revela clases emergentes** que el análisis no había
previsto — alimentando la siguiente iteración del modelo
(ver :doc:`analisis-dominio` § 12.2 sobre la naturaleza
iterativa del análisis basado en escenarios).

----

14. Ciclo de vida iterativo e incremental
=========================================

Cuando el prototipado (§ 13) se sostiene en el tiempo,
desemboca naturalmente en un **ciclo de vida iterativo e
incremental**. Para software orientado a objetos, el modelo
que mejor refleja esta dinámica es el **modelo de fuente
(*fountain model*) de Henderson-Sellers**.

Características del modelo
--------------------------

- **Arraigado en el mundo real** — modela los sistemas tal
  como evolucionan, no como diagramas idealizados.
- **Alto nivel de iteración** — las etapas no son
  estancos: análisis, diseño y construcción se solapan.
- **Fusión de etapas** del modelo clásico — la separación
  rígida entre "análisis terminado", "diseño terminado" y
  "construcción terminada" se relaja.
- **Lema operativo** (Gilb): *"un poco de análisis, un
  poco de diseño, un poco de programación y
  ¡repitámoslo!"*

Estructura típica de iteraciones
--------------------------------

La variante más frecuente del modelo:

1. **Primera iteración** — más larga (3 a 4 meses según el
   tipo de aplicación). En ella se analiza la aplicación y
   se elige el **núcleo significativo de negocio**: lo que
   representa la actividad básica y los objetos que tienen
   relación con la mayor parte del sistema.
2. **Iteraciones siguientes** — más cortas (~1 mes cada
   una). Cada iteración entrega un **incremento** sobre lo
   anterior; el usuario sigue utilizando la versión previa
   en producción mientras se construye la siguiente.

Los cambios sobre lo entregado son habituales y no
problemáticos: la herencia permite introducirlos sin
"desmontar" la base. La crítica del usuario sobre lo que ya
usa **alimenta** la siguiente iteración en lugar de
bloquearla.

Un beneficio implícito: al final del desarrollo, no hace
falta puesta en producción de pruebas ni formación masiva
de usuarios — ambas tareas se han realizado **gradualmente**
durante todo el ciclo.

Aplicación a IACT
-----------------

Núcleo significativo del proyecto IACT (primera iteración):

- ``Sesion``, ``Usuario`` y ``Permiso`` (auth + RBAC) —
  base sobre la que se apoyan todos los demás UCs.
- ``Llamada`` y ``EjecucionETL`` — entidades centrales del
  flujo de datos operativos hacia analytics.
- ``Reporte`` (clase base) y un par de subclases
  representativas (``ReporteVolumen``,
  ``ReporteAbandono``) — suficientes para validar el
  patrón polimórfico de UC_RPT_*.
- ``EventoAuditoria`` — sin auditoría no se puede entregar
  nada (CNST_025).

Incrementos posteriores típicos:

- Reportes adicionales (UC_RPT_*) y exportación async
  (UC_RPT_04).
- Familia de alertas (UC_ALR_*) con sincronización
  auditoría/notificación.
- Endurecimiento del modelo SoD (CNST_030) y reglas BR
  adicionales.
- Optimización de la ventana ETL (CNST_006/008).

Cada incremento se entrega al supervisor y al equipo de
calidad, que lo prueban en condiciones reales mientras el
siguiente incremento está en construcción.

Riesgos a controlar
-------------------

El modelo iterativo no es licencia para descuidar
disciplinas:

- Cada iteración debe respetar las restricciones del
  proyecto (CNST_*) y reglas de negocio (BR_*).
- Cada cambio sobre lo entregado debe pasar por
  ``rm-validation`` antes de re-publicarse — el hecho de
  que la herencia simplifique el cambio técnico no
  exime de re-validación funcional y de auditoría.
- Cada incremento mantiene los ADRs vigentes
  (especialmente ADR_DEVOPS_001) — un incremento que
  cambie el stack es, por definición, un cambio
  arquitectónico, no un incremento.

Relación con prototipos y escuelas de análisis
----------------------------------------------

- El **prototipo** (§ 13) es el punto de partida de la
  primera iteración del modelo de fuente.
- El **análisis del dominio** y las **escuelas de
  identificación de clases** (ver
  :doc:`analisis-dominio` § 12) se aplican en cada
  iteración, no solo al inicio.
- Los **patrones de diseño** (ver
  :doc:`patrones-diseno`) se incorporan progresivamente,
  conforme las iteraciones revelan los puntos donde
  realmente se necesitan.

----

15. Trazabilidad
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
   - :doc:`plan-documentacion-uc`
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
