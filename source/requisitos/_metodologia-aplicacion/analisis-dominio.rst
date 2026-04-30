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

Concepto: análisis del dominio
==============================

El **análisis del dominio** es el enfoque que se centra en
comprender un área de negocio a través de las personas que
trabajan directamente en ella, identificando los elementos
clave desde su perspectiva práctica y experiencia real. Su
valor no está en la sofisticación técnica sino en
**capturar la realidad operativa** antes de modelarla.

El experto del dominio
----------------------

Es la figura central del proceso. Una persona con
conocimiento profundo del área de negocio que **no
necesariamente tiene formación en desarrollo de software**.
Su valor radica en la experiencia directa y cotidiana con
los procesos, reglas y necesidades del dominio.

En IACT los expertos del dominio típicos son: supervisores
del centro de contacto, responsables de calidad, operadores
ETL, administradores RBAC y auditores. Ellos manejan
naturalmente el vocabulario que aparece en este documento
(segmento, ventana ETL, alerta, SoD, throttling), aunque
no lo conozcan en términos UML.

Tres elementos fundamentales
----------------------------

Los expertos ayudan a identificar:

1. **Objetos relevantes del dominio** — entidades sobre las
   que se trabaja: ``Llamada``, ``Reporte``, ``Alerta``,
   ``Sesion``, ``Usuario``, ``Permiso``,
   ``EjecucionETL``.
2. **Operaciones cotidianas** — acciones y procesos que
   transforman o interactúan con esos objetos: generar un
   reporte, reconocer una alerta crítica, ejecutar la
   ventana ETL, verificar un permiso.
3. **Relaciones entre elementos** — cómo los componentes
   del sistema se conectan y dependen entre sí, formando
   la red de interacciones que refleja la realidad del
   negocio (un ``Reporte`` consume datos de
   ``EjecucionETL``; un ``Permiso`` controla qué
   ``Funcion`` puede invocar un ``Usuario``).

Características clave del enfoque
---------------------------------

- **Conocimiento tácito**: además del explícito en
  manuales, captura el que solo se adquiere con la
  experiencia (qué pasa cuando la ventana ETL no cierra,
  cuándo un supervisor sabe que una alerta es falsa, qué
  excepciones aplica el área de calidad).
- **Vocabulario natural**: usar los términos del dominio
  evita malentendidos por traducción prematura a términos
  técnicos. En IACT esto significa que ``Alerta``,
  ``Segmento`` o ``Throttling`` aparecen con su semántica
  operativa, no como abstracciones genéricas.
- **Necesidades reales**: el sistema se diseña para
  resolver problemas concretos del centro de contacto, no
  problemas teóricos.

Importancia para IACT
---------------------

- Los sistemas que reflejan fielmente el dominio son
  inherentemente más útiles y usables.
- La participación temprana de los expertos del dominio
  conduce a mayor aceptación una vez implementado.
- Los modelos generados sirven como base para
  mantenimiento y evolución futura.
- Reduce el riesgo de desarrollar funcionalidades
  técnicamente correctas pero sin valor para el negocio
  (un riesgo recurrente cuando los UCs se escriben sin
  contraste con un experto operativo).

Las secciones siguientes aplican este enfoque al ecosistema
IACT: traducen el lenguaje natural del experto a un modelo
UML manejable.

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

12. Método de Abbott — descripción informal
===========================================

La técnica que las secciones 1-11 aplican (sustantivos →
clases, verbos → operaciones, adjetivos → atributos)
proviene del **método de Abbott**: escribir una descripción
del problema en lenguaje natural y analizar su estructura
gramatical.

Reglas básicas del método
-------------------------

- Los **sustantivos** se convierten en objetos candidatos.
- Los **verbos** se transforman en operaciones candidatas
  sobre esos objetos.
- Los **adjetivos** y modificadores aportan atributos y
  contexto.

Virtudes del enfoque
--------------------

- **Obliga a usar el vocabulario propio del dominio** —
  la terminología viene del experto, no del desarrollador.
- **Facilita la comunicación** entre desarrolladores y
  expertos del dominio: ambos pueden leer el mismo texto.
- Proporciona un **punto de partida accesible** para el
  análisis.
- **Ayuda a mantener el modelo cercano a la realidad del
  negocio**.

Limitaciones — por qué no basta por sí solo
-------------------------------------------

**Falta de rigor.** El método no es suficientemente
riguroso para problemas complejos. La transición de
lenguaje natural a conceptos de diseño puede ser ambigua y
subjetiva. Ejemplo:

   *"El sistema realiza la gestión de inventario."*

¿``Gestión`` debe ser clase u operación? Sin contexto
adicional el método no responde. En IACT esto aparece con
"reporte" (clase u operación), "alerta" (clase o evento),
"export" (operación o entidad ``TareaExport``).

**Imprecisión del lenguaje humano.** Tres patrones
problemáticos:

- **Sinónimos**: distintas palabras para el mismo
  concepto. En IACT: "supervisor" / "operador de
  monitoreo" / "responsable de turno".
- **Anáforas**: referencias indirectas a conceptos ya
  mencionados ("la alerta crítica recibida... esta luego
  se reconoce"). El "esta" puede inducir confusión sobre
  qué entidad opera el método.
- **Metáforas**: uso figurativo que confunde el análisis
  ("el sistema **levanta** la alerta", "**caen** los
  permisos del grupo").

**Ambigüedad gramatical — cosificación.** El proceso de
convertir verbos en sustantivos y viceversa complica el
análisis:

- "Gestionar" vs "gestión".
- "Oxigenar" vs "oxígeno".
- "Pulsar" vs "pulso".

En IACT: "auditar" vs "auditoría", "exportar" vs
"exportación", "alertar" vs "alerta". Cada par admite
modelado como clase **o** como operación, dependiendo del
nivel de granularidad — la decisión debe ser explícita,
no implícita.

Impacto si se usa Abbott aisladamente
-------------------------------------

- Modelos inconsistentes entre UCs documentados por
  distintos autores.
- Clases mal identificadas (operaciones disfrazadas de
  clase).
- Operaciones incorrectamente asignadas a la clase
  equivocada.
- Relaciones poco claras entre objetos.

Recomendación — uso de Abbott en IACT
-------------------------------------

Por estas razones, el método de Abbott debe considerarse:

- Un **punto de partida útil** para problemas pequeños o
  el primer borrador de un UC.
- Una **herramienta complementaria** dentro del proceso
  de análisis.
- Un **medio para iniciar discusiones** sobre el modelo
  del dominio con el experto.
- **No** como la única estrategia de identificación de
  clases y operaciones.

La sección siguiente presenta tres escuelas que
complementan el método de Abbott reduciendo sus
limitaciones: el análisis clásico (categorización
sistemática), el análisis basado en escenarios y el
análisis dirigido por responsabilidades (RDD).

----

13. Tres escuelas para identificar clases
=========================================

Las secciones 1-11 aplican una técnica concreta
(sustantivos→clases / verbos→operaciones) para extraer un
modelo del lenguaje natural. Esa técnica es solo **una** de
las escuelas reconocidas de análisis OOP. A continuación se
contrastan las tres escuelas más relevantes y cómo se
combinan en IACT.

13.1 Análisis clásico — categorías de fuentes
---------------------------------------------

El análisis clásico es una estrategia más estructurada y
formal que la descripción informal. Categoriza
sistemáticamente los conceptos del dominio según su
naturaleza. Su valor en IACT:

- Proporciona una **base sistemática** para identificar
  clases que sustantivos→clases puede pasar por alto.
- Ayuda a garantizar la **completitud** del modelo.
- Facilita la identificación de **relaciones** entre
  elementos.
- Permite definir **interfaces** apropiadas y **límites**
  del sistema.

Categorías clásicas y su lectura en IACT
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
 :widths: 25 35 40
 :header-rows: 1

 * - Categoría
   - Definición
   - Ejemplo IACT
 * - Cosas tangibles
   - Objetos físicos concretos o grupos de ellos.
   - Equipo del supervisor, servidor ``vm-iact``,
     teléfono físico del agente.
 * - Conceptos abstractos
   - Ideas no tangibles que organizan o rastrean
     actividades; principios o reglas.
   - ``Permiso``, ``Sesion``, ``EventoAuditoria``,
     ``RegistroExportacion``.
 * - Personas y roles
   - Seres humanos con responsabilidades y permisos
     definidos.
   - ``Supervisor``, ``Auditor``, ``OperadorETL``,
     ``AdministradorRBAC``.
 * - Organizaciones
   - Agrupaciones formales con misión y estructura.
   - Centro de contacto, área de calidad, comité SoD.
 * - Lugares
   - Ubicaciones físicas relevantes con propósitos
     específicos.
   - Sala de operaciones, segmento atendido (BR_012).
 * - Dispositivos
   - Hardware con capacidades, protocolos y
     restricciones.
   - IVR (read-only, CNST_006), terminal del agente.
 * - Sistemas externos
   - Otros sistemas con contratos e interfaces propios.
   - LDAP corporativo, BD operativa, IVR-host.
 * - Eventos
   - Sucesos en momentos específicos que provocan
     cambios de estado.
   - ``LlamadaEntrante``, ``UmbralExcedido``,
     ``VentanaETLCerrada``, ``ReconocerAlerta``.

Uso recomendado
~~~~~~~~~~~~~~~

Pasar el dominio IACT por **cada** categoría como checklist
después del análisis sustantivos→clases. Una clase nueva
identificada por la categoría "Eventos" típicamente queda
fuera si solo se mira el lenguaje narrativo del UC.

13.2 Análisis de casos de uso — diseño basado en escenarios
-----------------------------------------------------------

El análisis de casos de uso (*scenario-based design*)
identifica clases a partir de **escenarios concretos**, no
del lenguaje narrativo del dominio. La analogía con la
producción cinematográfica: cada escenario es un
*storyboard* — secuencia de eventos que el equipo recorre
para identificar:

1. **Objetos participantes** — actores, entidades del
   sistema, interfaces, controladores.
2. **Responsabilidades específicas** — qué hace y qué
   información mantiene cada objeto.
3. **Patrones de colaboración** — cómo interactúan los
   objetos para cumplir el objetivo del escenario.

Naturaleza iterativa
~~~~~~~~~~~~~~~~~~~~

El proceso comienza con escenarios básicos (flujo nominal)
y se expande gradualmente para incluir:

- Condiciones excepcionales (errores, situaciones
  inesperadas).
- Comportamientos secundarios.
- Nuevas abstracciones que **emergen** del análisis.
- Modificaciones a responsabilidades existentes.
- Reasignación de responsabilidades entre objetos.

En IACT esto se materializa en los UCs con flujo nominal +
flujos alternativos + flujos de excepción
(ver :doc:`casos-uso-especificacion`).

Escenarios como base de pruebas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cada escenario documentado se convierte en **caso de prueba
potencial**. Esto alinea naturalmente análisis y
verificación: un escenario sin caso de prueba asociado es
una señal de que el análisis está incompleto. En IACT los
escenarios alimentan tanto los diagramas de secuencia
(:doc:`diagramas-secuencias`) como las pruebas de
aceptación derivadas en ``rm-validation``.

13.3 Análisis del comportamiento — RDD
--------------------------------------

La tercera escuela — **Responsibility-Driven Design (RDD)**
de Wirfs-Brock, Wilkerson y Wiener — propone que la
identificación y asignación de **responsabilidades** debe
ser el punto de partida del diseño OOP, antes que la
estructura de datos o las entidades del dominio.

Cita canónica
~~~~~~~~~~~~~

   *El conocimiento que un objeto mantiene y las acciones
   que un objeto puede realizar. Las responsabilidades
   tienen el propósito de transmitir un sentido de la
   finalidad de un objeto y su lugar en el sistema. Las
   responsabilidades de un objeto son todos los servicios
   que presta a todos los contratos que apoya.*
   — Rebecca Wirfs-Brock

Tipos de responsabilidades
~~~~~~~~~~~~~~~~~~~~~~~~~~

RDD distingue dos categorías:

- **Knowing responsibilities** — el conocimiento que el
  objeto debe **mantener**. En IACT, ``Sesion`` conoce su
  ``user_id`` y su instante de creación; ``Reporte``
  conoce su tipo y configuración.
- **Doing responsibilities** — las acciones que el objeto
  puede **realizar**. En IACT, ``Reporte`` calcula y
  exporta; ``Sesion`` se renueva o caduca; ``EvaluadorAlertas``
  evalúa umbrales y publica alertas.

Las responsabilidades no son simplemente una lista de
métodos o atributos: representan el **rol** que el objeto
desempeña en la solución. Definir responsabilidades es
establecer **contratos** que el objeto debe cumplir con
los demás, formando una red de colaboraciones.

Cambio de pregunta
~~~~~~~~~~~~~~~~~~

RDD desplaza la pregunta inicial:

- Enfoque clásico: *"¿Qué objetos necesitamos?"*
- Enfoque RDD: *"¿Qué comportamientos necesitamos? ¿Quién
  debería ser responsable de cada comportamiento?"*

Beneficios en este proyecto
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Cohesión** — cada objeto IACT tiene un propósito claro;
  ``aud_app`` solo hace audit, ``perm_app`` solo decide
  permisos.
- **Encapsulamiento** — las responsabilidades determinan
  qué información debe ser privada y cuál pública.
- **Bajo acoplamiento** — responsabilidades bien definidas
  habilitan interfaces claras (ver
  :doc:`diagramas-componentes`).
- **Evolución localizada** — los cambios se concentran en
  las responsabilidades específicas afectadas, no se
  propagan a través de la jerarquía.

Integración con análisis del comportamiento
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

RDD y el análisis del comportamiento se integran de forma
natural en tres niveles:

**Colaboraciones.** Las responsabilidades identificadas se
traducen en patrones de interacción entre objetos. En IACT
la responsabilidad de ``Reporte`` *generar agregados*
exige analizar la secuencia de interacciones entre
``Reporte``, ``BDAnalytics`` y ``aud_app`` para registrar
el evento de ejecución (ver
:doc:`diagramas-secuencias` y
:doc:`diagramas-colaboraciones`).

**Estados y transiciones.** Las responsabilidades
identifican los estados por los que pasa un objeto y las
transiciones válidas. Una ``Alerta`` IACT tiene la
responsabilidad de gestionar su ciclo de vida —
``publicada → reconocida → cerrada`` (ver
:doc:`diagramas-estados`). Las transiciones inválidas no
existen porque ningún método del objeto las permite.

**Flujos de trabajo.** Las responsabilidades guían cómo se
coordinan múltiples objetos en procesos amplios. La
responsabilidad de cada objeto en el flujo debe estar
claramente definida y el análisis del comportamiento
verifica que las responsabilidades se cumplen
coordinadamente (ver :doc:`diagramas-actividades`).

Cómo se modela RDD con UML en IACT
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Diagramas de secuencia** — cada mensaje materializa
  una responsabilidad previamente identificada. Si un
  mensaje no corresponde a una responsabilidad declarada,
  la responsabilidad falta o el mensaje sobra.
- **Diagramas de estado** — las transiciones se justifican
  por las responsabilidades del objeto, no por
  conveniencia técnica.
- **Diagramas de actividad** — verifican que cada actividad
  está asignada a un objeto **responsable**, evitando
  responsabilidades huérfanas o duplicadas.

Aplicación canónica IACT
~~~~~~~~~~~~~~~~~~~~~~~~

RDD es la base de la § 8 (responsabilidades canónicas) y
de las interfaces declaradas en
:doc:`diagramas-componentes` (``ISecurity``, ``IAuditLog``,
``IReporte``, ``IAlerta``, ``INotificacion``,
``IDatosOperativos``, ``IDatosAnalytics``, ``IETL``). Cada
interfaz es un **contrato** en sentido RDD: define los
servicios que el componente promete prestar.

Ejemplo IACT — ``Cita``-equivalente: ``UC_RPT_07`` reporte
programado:

1. Identificar interacciones necesarias con
   ``Scheduler``, ``rpt_app``, ``BDAnalytics``,
   ``log_app``, ``aud_app``.
2. Definir estados por los que pasa la tarea programada
   (``planificada``, ``en_ejecucion``, ``completada``,
   ``fallida``).
3. Analizar el flujo completo de programación, ejecución y
   notificación al buzón interno (CNST_001).

La disciplina del proyecto exige que toda comunicación
entre apps Django pase por su contrato declarado, nunca
por acceso directo a modelos ajenos (ver § 11 de
:doc:`orientacion-objetos`).

Validaciones que aporta RDD
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ¿Las responsabilidades asignadas son **coherentes** con
  el comportamiento requerido?
- ¿Faltan responsabilidades, o hay redundancias entre
  objetos?
- ¿La distribución actual produce **patrones eficientes y
  mantenibles**?
- ¿Hay problemas detectables **antes** de implementar?

Influencia
~~~~~~~~~~

RDD ha influido en prácticas como **Domain-Driven Design**
y en la OOP en general: un buen diseño OOP equilibra
aspectos estructurales (qué objetos hay, cómo se relacionan)
y comportamentales (qué hacen, qué prometen).

13.4 Combinación de las tres escuelas en IACT
---------------------------------------------

Las tres escuelas no son alternativas excluyentes; son
**lentes complementarios**:

.. list-table::
 :widths: 30 35 35
 :header-rows: 1

 * - Lente
   - Aporta
   - Riesgo si se usa sola
 * - Sustantivos→clases (clásico)
   - Cobertura del lenguaje del dominio.
   - Pierde clases que no aparecen en la narrativa.
 * - Casos de uso (escenarios)
   - Responsabilidades dinámicas, casos límite.
   - Sesgo hacia el flujo nominal del momento.
 * - RDD (comportamiento)
   - Contratos limpios entre componentes.
   - Modela en abstracto sin anclar al dominio real.

Recomendación: aplicar las tres en cada UC IACT —
sustantivos→clases primero, escenarios para validar y
descubrir clases emergentes, RDD para depurar contratos
antes de fijar las interfaces.

----

14. Tarjetas CRC — herramienta operacional
==========================================

Las **tarjetas CRC (Clase-Responsabilidad-Colaboración)**
son la herramienta operativa más conocida para aplicar RDD
(§ 13.3). Tradicionalmente se usaban tarjetas físicas de
**7 × 12,5 cm** divididas en tres secciones:

- **Parte superior** — nombre de la clase.
- **Mitad izquierda** — responsabilidades de la clase.
- **Mitad derecha** — colaboradores necesarios.

Su valor en este proyecto:

- Visualización rápida de las relaciones entre clases.
- Identificación de **responsabilidades redundantes o
  faltantes** antes de que se materialicen en código.
- Discusiones productivas en sesiones con stakeholders y
  expertos del dominio.
- Evolución natural del diseño: las tarjetas son baratas
  de descartar y rehacer.

14.1 Estructura de una tarjeta CRC en IACT
------------------------------------------

::

   +-----------------------------------------------+
   |  Reporte                                      |
   +----------------------+------------------------+
   |  Responsabilidades   |  Colaboradores         |
   |                      |                        |
   |  - generar agregados |  - BDAnalytics         |
   |  - exportar          |  - aud_app             |
   |    (CSV/XLSX/JSON)   |  - log_app             |
   |  - validar rango     |  - perm_app            |
   |    (CNST_031)        |                        |
   |  - aplicar segmento  |                        |
   |    (BR_012)          |                        |
   +----------------------+------------------------+

Cada tarjeta IACT debe respetar dos reglas:

1. **No más de 3-5 responsabilidades** por clase. Si la
   lista crece, la clase está absorbiendo trabajo de
   otra — refactorizar.
2. Cada **colaborador** corresponde a una clase con su
   propia tarjeta. Si un colaborador no tiene tarjeta,
   probablemente falta una clase en el modelo.

14.2 Evolución hacia herramientas CASE y UML
--------------------------------------------

Las CRC han evolucionado e integrado con herramientas
CASE (*Computer-Aided Software Engineering*) que usan
UML, transformando la representación física en digital y
formal:

- Las clases y sus responsabilidades se traducen a
  **nodos** del grafo (clases UML con sus operaciones).
- Las colaboraciones se transforman en **arcos** que
  conectan los nodos (asociaciones, dependencias).
- Las relaciones y dependencias se expresan mediante la
  **notación estándar de UML**.

Ventajas de la evolución:

- Mayor **precisión** en la documentación.
- Facilidad para **mantener y actualizar** el diseño.
- Capacidad para **manejar sistemas más complejos**.
- Mejor **integración** con otras herramientas de
  desarrollo.
- **Estandarización** de la notación.

14.3 Aplicación en IACT
-----------------------

En este proyecto las CRC físicas o digitales se usan en
fase temprana — antes de comprometer un diagrama UML
completo.

Flujo recomendado:

1. **Sesión con experto del dominio** — captura inicial
   en CRC (físicas o en una pizarra digital).
2. **Iteración de equipo** — el equipo redistribuye
   responsabilidades hasta que las tarjetas sean
   coherentes y respeten el principio "≤ 5
   responsabilidades por clase".
3. **Traducción a UML** — las tarjetas se materializan en
   diagramas de clases (:doc:`diagramas-uml`) y de
   componentes (:doc:`diagramas-componentes`).
4. **Verificación cruzada** — las responsabilidades
   declaradas se ejercitan en diagramas de secuencia
   (:doc:`diagramas-secuencias`) y actividades
   (:doc:`diagramas-actividades`); cada mensaje del
   diagrama debe corresponder a una responsabilidad
   declarada en una tarjeta.

Las CRC quedan como artefacto de discovery; el repositorio
guarda los **UML resultantes** como fuente de verdad.

14.4 Mapeo CRC ↔ documentos del proyecto
----------------------------------------

.. list-table::
 :widths: 30 35 35
 :header-rows: 1

 * - Elemento CRC
   - Documento donde se materializa
   - Verificación
 * - Nombre de clase
   - § 7 de este documento;
     :doc:`diagramas-uml` § 1
   - Coherencia con sustantivos del dominio (§ 3).
 * - Responsabilidades
   - § 8 de este documento;
     :doc:`agregacion-interfaces` (interfaces)
   - Cada responsabilidad debe poder ejecutarse en al
     menos un UC del catálogo.
 * - Colaboradores
   - :doc:`relaciones-uml`,
     :doc:`diagramas-colaboraciones`,
     :doc:`diagramas-componentes`
   - Cada colaborador debe ser una clase declarada o un
     componente del sistema (no inventado).

14.5 Por qué CRC sigue siendo útil
----------------------------------

A pesar de las herramientas digitales, los principios
fundamentales de CRC siguen vigentes:

- Obligan a pensar en **responsabilidades** (RDD) antes
  que en estructura de datos.
- Son un instrumento de **comunicación** con stakeholders
  no técnicos.
- Permiten **descartar diseños malos** rápidamente
  (rehacer una tarjeta cuesta segundos).
- Mantienen la **trazabilidad** entre el diseño
  conceptual y la implementación si se transcriben
  fielmente al UML resultante.

Recomendación operativa: usar CRC en cada nueva entidad
IACT donde el dominio aún no es estable; saltar al UML
directamente solo cuando las responsabilidades ya están
claras y validadas con el experto del dominio.

----

15. Documentar el dominio — Domain-Driven Design (DDD)
======================================================

Antes de escribir código de aplicación, **modelar el
dominio**. El modelado de dominio es la forma principal
de determinar los **aspectos importantes** del negocio y
se construye **colaborativamente** entre ingeniería,
producto y stakeholders del negocio para asegurar que
todas las partes están alineadas sobre cómo luce el
modelo del dominio.

Esa naturaleza colaborativa lo convierte en un excelente
candidato para **diagramar**: documentar el modelo del
dominio con un diagrama lo hace cobrar vida y aumenta la
probabilidad de que se use realmente.

15.1 Domain-Driven Design — referencia canónica
-----------------------------------------------

   *Domain-Driven Design: Tackling Complexity in the
   Heart of Software* — Eric Evans, 2003.

DDD propone que el **modelo del dominio** sea el centro
del diseño: el código refleja el dominio, los nombres
del dominio se usan en el código, y la conversación
entre técnicos y negocio sucede en el mismo vocabulario
(*ubiquitous language*).

15.2 Beneficios observados de DDD
---------------------------------

Cuando el modelado de dominio funciona, se observan
patrones consistentes:

- **Momento de claridad colectiva** — durante varias
  sesiones se prueban distintas ideas y aproximaciones;
  llega un punto en que todo encaja, todos comparten la
  misma comprensión del paisaje y hablan el mismo
  idioma.
- **Translación directa a código** — un modelo de
  dominio sólido se traduce con facilidad a clases del
  proyecto. La § 7 de este documento muestra cómo el
  análisis IACT desemboca en un diagrama de clases
  consolidado.
- **Lenguaje compartido** — al final de un proyecto
  bien modelado, los stakeholders no técnicos usan la
  misma terminología que los desarrolladores. En IACT,
  términos como ``segmento``, ``ventana ETL``, ``SoD``
  y ``buzón interno`` ya forman parte del vocabulario
  común.
- **Evolución sostenida** — al estar el modelo
  documentado, puede consultarse cuando aparecen
  nuevos requisitos. Si el modelo encaja, se reutiliza;
  si no, evoluciona puntualmente sin romper lo
  existente.

Caso ilustrativo (citado por Eric Evans y otros autores
DDD): una compañía de seguros que necesitaba determinar
**cómo se vendían sus productos y a quién**. La data
estaba dispersa, los canales eran múltiples y los datos
disponibles variaban por canal. El equipo no sabía cómo
representar el dominio en código; tras varios días de
modelado conjunto llegaron a una síntesis que se tradujo
fácilmente en código. Años después, el núcleo del modelo
seguía intacto — solo se agregaron entidades nuevas.

15.3 Diagrama de clases UML como vehículo del modelo
----------------------------------------------------

Dentro de UML, el **diagrama de clases** es el vehículo
natural del modelo de dominio. Aunque puede usarse para
modelar clases en sentido implementativo, es igualmente
válido para modelar **conceptos del dominio** — y tiene
sentido: el modelo del dominio se materializa en código
mediante clases.

El **poder real** del diagrama se libera cuando se
modelan las **relaciones entre entidades**: asociaciones,
agregaciones, composiciones, generalización (ver
:doc:`relaciones-uml`,
:doc:`agregacion-interfaces`).

15.4 Aplicación al proyecto IACT
--------------------------------

Este documento (``analisis-dominio.rst``) y sus
hermanos forman el **modelo de dominio canónico de
IACT**:

- **§§ 1-7** — extracción del modelo desde el lenguaje
  natural (sustantivos→clases / verbos→operaciones /
  adjetivos→atributos).
- **§ 7** — diagrama de clases consolidado del dominio.
- **§ 8** — responsabilidades canónicas (RDD).
- **§§ 12-14** — métodos complementarios para
  identificar clases (Abbott, escuelas clásica /
  escenarios / RDD, tarjetas CRC).
- **Documentos hermanos** — :doc:`orientacion-objetos`
  desarrolla los seis principios OOP aplicados,
  :doc:`relaciones-uml` y
  :doc:`agregacion-interfaces` profundizan las
  relaciones del modelo, :doc:`patrones-diseno` aplica
  GoF y GRASP.

Ubiquitous language IACT
~~~~~~~~~~~~~~~~~~~~~~~~

El vocabulario común del proyecto, capturado en este
modelo, incluye:

- **Llamada / IVR** — interacción telefónica capturada
  por el conmutador.
- **Segmento** (BR_012) — agrupación de campañas
  atendidas.
- **Ventana ETL** (CNST_006/008) — periodo nocturno de
  carga read-only.
- **SoD** (CNST_030) — separación de responsabilidades
  en el modelo RBAC.
- **Buzón interno** (CNST_001) — único canal de
  notificación; no email.
- **Audit** (CNST_025) — registro inmutable de eventos.

Cualquier conversación, ADR, UC o diagrama del proyecto
**debe usar este vocabulario** — no sus equivalentes
genéricos. Cuando un nuevo término entra al dominio,
agregarlo aquí.

15.5 Evolución del modelo
-------------------------

DDD enfatiza que el dominio y el código **evolucionan
juntos**. La regla operativa para IACT:

1. Cuando aparece un requisito nuevo, **consultar este
   documento**.
2. Si el modelo encaja, **reutilizar las entidades
   existentes**.
3. Si no encaja, **evolucionar el modelo
   explícitamente**: agregar la entidad / la relación /
   la responsabilidad nueva en este documento, registrar
   la decisión en un ADR del subdominio si es central.
4. **No bifurcar** modelos paralelos. Un solo modelo de
   dominio canónico para IACT.

15.6 Diagrama colaborativo en tiempo real
-----------------------------------------

Una ventaja del enfoque diagramas-como-código (ver
:doc:`diagramas-uml` "Historia de la diagramación"):
durante una sesión con stakeholders, el equipo puede
**dibujar el modelo en vivo** a medida que se discuten
los conceptos. Con PlantUML + ``planttext.com`` o un
editor con preview, el ciclo "discusión → boceto →
revisión" toma minutos en vez de días.

Esa práctica es lo que materializa el "momento de
claridad colectiva" — todos viendo el mismo diagrama
mientras se construye.

15.7 Determinar las entidades importantes
-----------------------------------------

Al construir el modelo del dominio, el primer paso es
**pensar en todas las entidades importantes del negocio**.
Una **entidad** es un concepto central del negocio —
típicamente las frases que más se usan en reuniones y en
el código. En la jerga de modelado, las entidades
**contienen datos** y **lógica de negocio**.

Ejemplo del libro citado — una editorial podría tener
entidades como ``Libro``, ``Capítulo`` y ``Autor``. Un
``Libro`` tiene un atributo ``título`` (dato) y una
operación ``calcularConteoPalabras()`` (lógica). Las
entidades capturan tanto **qué sabe** la aplicación como
**qué puede hacer**.

Otro ejemplo — una empresa ficticia *Streamy* del sector
de video streaming. Su entidad más importante sería
``Title`` (representa los videos que se ofrecen). Cada
``Title`` pertenece a un ``Genre``, y cada ``Genre`` tiene
una lista de ``Title`` asociados. Con dos entidades y una
relación ya hay un modelo de dominio embrionario.

Cómo identificar entidades importantes en IACT
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tres preguntas operativas, alineadas con § 13.3 RDD y
con § 12 Método de Abbott:

1. **¿Qué frases aparecen repetidamente** en
   conversaciones con supervisores, auditores, área de
   calidad?
2. **¿Qué sustantivos** dominan los UCs documentados?
3. **¿Qué objetos** sobreviven más allá de un caso de
   uso puntual y se referencian desde varios?

Aplicada al dominio IACT, la pregunta "¿cuál es la
entidad más importante?" tiene una respuesta clara:
**``Llamada``** (la interacción del IVR es la fuente
operacional de toda la analítica). A partir de ahí, las
entidades relacionadas emergen:

.. list-table::
 :widths: 25 35 40
 :header-rows: 1

 * - Entidad ancla
   - Entidades relacionadas inmediatas
   - Naturaleza de la relación
 * - ``Llamada``
   - ``Segmento``, ``EjecucionETL``, ``Reporte``,
     ``Alerta``
   - Una llamada pertenece a un segmento; es cargada
     por una ejecución ETL; alimenta reportes y
     alertas.
 * - ``Usuario``
   - ``Sesion``, ``Grupo``, ``Permiso``,
     ``EventoAuditoria``
   - El usuario tiene sesión, pertenece a grupos,
     ejerce permisos, genera eventos de auditoría.
 * - ``Reporte``
   - ``Filtro``, ``ConfiguracionExport``,
     ``Llamada``, ``BDAnalytics``
   - El reporte aplica filtros, configura su export y
     consume datos derivados de llamadas.
 * - ``Alerta``
   - ``UmbralAlerta``, ``EvaluadorAlertas``,
     ``Supervisor``
   - La alerta se evalúa contra umbrales y se
     reconoce por un supervisor.
 * - ``EjecucionETL``
   - ``VentanaETL``, ``ErrorETL``, ``Llamada``,
     ``BDAnalytics``
   - La ejecución corre dentro de una ventana,
     produce errores potenciales, lee llamadas y
     escribe agregados.

Datos vs lógica en las entidades IACT
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cada entidad importante de IACT combina datos y lógica
canónica:

.. list-table::
 :widths: 22 38 40
 :header-rows: 1

 * - Entidad
   - Datos típicos
   - Lógica de negocio típica
 * - ``Llamada``
   - duración, espera, abandono, segmento.
   - ``esAbandonada()``, ``getDuracion()``,
     ``perteneceASegmento()``.
 * - ``Reporte``
   - tipo, rango, filtros aplicados.
   - ``generar()``, ``exportar(formato)``,
     ``aplicarFiltros()``, ``validarRango()``
     (CNST_031).
 * - ``Alerta``
   - umbral, estado, momento de evaluación.
   - ``evaluar()``, ``reconocer()``, ``cerrar()``,
     ``estaActiva()``.
 * - ``Sesion``
   - usuario, momento de inicio, último acceso.
   - ``estaActiva()``, ``renovar()``, ``cerrar()``,
     ``haCaducado()`` (CNST_002).
 * - ``EjecucionETL``
   - ventana, hora de inicio/fin, estado, errores.
   - ``ejecutar()``, ``registrarError()``,
     ``estaCompleta()``, ``perteneceAVentana()``.

Esta lectura es el contrato RDD (§ 13.3): cada entidad
**conoce** sus datos (knowing) y **hace** sus
operaciones (doing).

Embrión y crecimiento del modelo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El proceso recomendado, aplicable a IACT y a cualquier
dominio nuevo:

1. **Identificar la entidad ancla** (la que más se
   menciona).
2. **Listar 3-5 entidades relacionadas inmediatas** y la
   naturaleza de la relación.
3. **Para cada entidad**, anotar sus datos típicos y su
   lógica de negocio mínima (aunque sea en pseudocódigo).
4. **Diagramar** (PlantUML class diagram) el embrión
   resultante — cinco entidades, relaciones, atributos
   y métodos básicos.
5. **Iterar** con stakeholders hasta que el embrión
   capture el lenguaje compartido.

Ese embrión es el punto de partida del modelo
documentado en §§ 3-7 de este documento. La diferencia
entre un dominio "viable" y uno "estancado" suele ser
si el equipo llegó al paso 5 con disciplina o si se
quedó en el paso 1 con una sola entidad.

Nota sobre profundidad
~~~~~~~~~~~~~~~~~~~~~~

Cuando un autor introduce DDD, no siempre baja al nivel
de implementación detallada — el objetivo es **identificar
el modelo**, no escribir todo el código. Para IACT, el
modelo aquí descrito y los UCs documentados son
suficientes para que el equipo de desarrollo materialice
las entidades en código Django siguiendo las guidelines
del proyecto (ver § 13 ``backend-django`` /
``backend-python`` en ``.thyrox/guidelines/``).

15.8 Documentar la primera relación
-----------------------------------

Una vez identificadas dos o más entidades importantes
(§ 15.7), el siguiente paso es **documentar su primera
relación**. En un modelo de dominio cada línea posterior
a la declaración del diagrama documenta una relación
entre dos entidades.

El equivalente IACT
~~~~~~~~~~~~~~~~~~~

El ejemplo del libro citado usa ``Title -- Genre`` como
primera relación de un dominio de streaming. El
equivalente IACT más natural es ``Llamada`` ↔
``Segmento``: cada llamada pertenece a un segmento, y
cada segmento agrupa muchas llamadas (BR_012). Es la
relación de **asociación** más fundamental del dominio.

Sintaxis PlantUML mínima
~~~~~~~~~~~~~~~~~~~~~~~~

En PlantUML, declarar dos entidades y una asociación es
casi tan simple como en Mermaid:

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   class Llamada
   class Segmento
   Llamada -- Segmento
   @enduml

Análisis del fragmento:

- ``@startuml`` / ``@enduml`` — delimitan el bloque
  PlantUML (equivalente al ``classDiagram`` de Mermaid
  como declaración de tipo).
- ``class Llamada`` y ``class Segmento`` — declaran las
  dos entidades.
- ``Llamada -- Segmento`` — el ``--`` indica una
  **asociación** simple (sin dirección, sin
  multiplicidad explícita).

Cuando cada entidad mantiene una referencia a la otra y
ninguna es parte estructural de la otra, la relación
correcta es **asociación** — la misma noción del libro
("each entity is going to hold a reference to the
other"). El detalle completo de la asociación está en
§ 2 de :doc:`relaciones-uml`.

Multiplicidad mínima del primer modelo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Aunque este es un primer paso, conviene incorporar
multiplicidad desde el inicio. La forma del par
Llamada-Segmento en IACT:

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   class Llamada {
     - id : Integer
     - duracion_seg : Integer
     - fecha : DateTime
   }
   class Segmento {
     - id : Integer
     - nombre : String
   }
   Llamada "1..*" -- "1" Segmento : pertenece a
   @enduml

Lectura: cada ``Llamada`` pertenece a un único
``Segmento`` (un segmento por llamada — BR_012); cada
``Segmento`` puede tener muchas llamadas (1 a varias).
Esa precisión es lo que diferencia un modelo embrionario
de uno operativo.

Crecimiento del modelo a partir de la primera relación
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Una vez documentada la primera relación, el modelo crece
agregando entidades vecinas y sus relaciones — siempre
una línea por relación:

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   class Llamada
   class Segmento
   class EjecucionETL
   class Reporte
   class Usuario

   Llamada "1..*" -- "1" Segmento : pertenece a
   EjecucionETL "1" -- "*" Llamada : carga
   Reporte "*" -- "*" Llamada : agrega
   Usuario "*" -- "*" Reporte : consulta
   @enduml

En cinco líneas, el modelo embrionario ya captura el
flujo central de IACT: el supervisor consulta reportes
que agregan llamadas que pertenecen a segmentos y se
cargaron por ejecuciones ETL.

Iteración recomendada
~~~~~~~~~~~~~~~~~~~~~

1. Empezar con **una** relación entre dos entidades
   ancla.
2. Agregar **una entidad nueva** por iteración.
3. Para cada nueva entidad, declarar **al menos una
   relación** con las existentes.
4. Cuando el embrión tenga 5-7 entidades, evaluar si
   hace sentido modelar tipos de relaciones más fuertes
   (composición, agregación, herencia) en lugar de
   asociación pura — ver :doc:`relaciones-uml` y
   :doc:`agregacion-interfaces`.

Esta progresión convierte el modelo embrionario en el
diagrama consolidado de § 7 de este documento sin saltos
abruptos. Ningún diagrama de clases de IACT debe
construirse "de golpe" — todos parten de una primera
relación clara y crecen iterativamente.

Por qué la asociación es el punto natural de partida
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

La asociación es el tipo de relación con menos
compromisos:

- No impone composición fuerte (no obliga a que la
  parte muera con el todo).
- No impone agregación (no obliga a un sentido todo-parte).
- No impone herencia (no exige "es-un").

Empezar por asociaciones permite explorar el modelo sin
fijar prematuramente decisiones que luego cuesta
revertir. Las relaciones más fuertes (composición,
agregación, herencia) **se ganan** cuando el dominio lo
exige — ver § 13 de :doc:`relaciones-uml` "Comparativa
por contexto" y la advertencia de Rumbaugh.

15.9 Pasar de asociación a composición
--------------------------------------

Una vez documentada la primera relación (§ 15.8) en
forma de asociación, el siguiente paso es identificar
**otras entidades relacionadas con la entidad ancla** y
preguntarse: *¿podrían existir sin ella?*

Si la respuesta es **no**, la relación es **composición**,
no asociación.

Ejemplo del libro citado
~~~~~~~~~~~~~~~~~~~~~~~~

Para la entidad ``Title`` del dominio Streamy:

- ``Title`` ↔ ``Genre`` — **asociación** (un género
  existe aunque no tenga títulos asignados todavía).
- ``Title`` ↔ ``Season`` — **composición** (no tiene
  sentido tener una temporada sin el título al que
  pertenece).
- ``Title`` ↔ ``Review`` — **composición** (la reseña
  pertenece al título; eliminado el título, las reseñas
  ya no tienen referencia).

Y un nivel más:

- ``Season`` ↔ ``Episode`` — **composición** (un episodio
  no tiene sentido sin pertenecer a una temporada).

Lectura: el diamante (``*--`` en Mermaid, equivalente a
``*--`` en PlantUML) indica composición. El lado del
diamante señala al **padre** (poseedor); el otro extremo
es el **hijo** que no puede existir sin él.

Equivalente IACT — ``EjecucionETL`` y sus partes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Aplicada al dominio IACT, la entidad ``EjecucionETL``
juega el rol de ``Title``: tiene relaciones de distinto
tipo con sus vecinas.

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   class EjecucionETL
   class VentanaETL
   class Llamada
   class ErrorETL
   class RegistroIngesta
   class DetalleError

   VentanaETL "1" -- "*" EjecucionETL : contiene
   EjecucionETL "1" *-- "*" ErrorETL : produce
   EjecucionETL "1" *-- "*" RegistroIngesta : produce
   EjecucionETL "*" -- "*" Llamada : carga
   ErrorETL "1" *-- "*" DetalleError : detalla
   @enduml

Lectura del diagrama:

- ``VentanaETL`` ↔ ``EjecucionETL`` — **asociación**.
  Las ventanas existen como conceptos del calendario
  aunque no haya ejecuciones aún.
- ``EjecucionETL`` ↔ ``Llamada`` — **asociación**. Las
  llamadas existen independientemente; una ejecución
  las **carga**, no las posee. Eliminada la ejecución
  (en el sentido del dominio), las llamadas siguen.
- ``EjecucionETL`` ↔ ``ErrorETL`` — **composición**. Un
  error solo tiene sentido si pertenece a una ejecución;
  invalidada la ejecución, el error como entidad de
  dominio desaparece (su rastro en ``audit_log``
  permanece, pero el objeto del dominio no).
- ``EjecucionETL`` ↔ ``RegistroIngesta`` — **composición**.
  Idéntica lógica: los registros de ingesta son partes
  internas de la ejecución.
- ``ErrorETL`` ↔ ``DetalleError`` — **composición** en
  segundo nivel. Análogo al ``Season`` ↔ ``Episode``
  del libro: el detalle no existe sin el error.

Sintaxis PlantUML para composición
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PlantUML usa ``*--`` con el diamante del lado del padre,
exactamente igual que la convención Mermaid presentada
en el libro:

.. code-block:: plantuml

   EjecucionETL "1" *-- "*" ErrorETL : produce

- ``"1"`` y ``"*"`` — multiplicidad (una ejecución
  produce muchos errores potenciales).
- ``*--`` — composición; el diamante se dibuja del lado
  del padre (``EjecucionETL``).
- ``: produce`` — etiqueta opcional de la relación.

Convención de dirección
~~~~~~~~~~~~~~~~~~~~~~~

Aunque PlantUML acepta ``*--`` y ``--*``, conviene
escribir **siempre el padre a la izquierda** y leer de
izquierda a derecha. Reduce carga cognitiva y hace los
diagramas comparables. Esta es la misma recomendación
del autor citado para Mermaid.

DDD es opinionable
~~~~~~~~~~~~~~~~~~

DDD es **opinable**: el modelo presentado aquí refleja
una lectura razonable del dominio IACT, pero otro equipo
podría modelarlo distinto y seguir siendo válido. Lo
importante no es la "respuesta única" — es aplicar
**consistentemente** los criterios:

1. ¿Existe la parte sin el todo? Sí → asociación. No →
   composición.
2. ¿La eliminación del todo destruye la parte como
   entidad del dominio? Sí → composición. No →
   asociación.
3. ¿Hay un ownership claro? Sí → composición. No →
   asociación.

Para IACT, la pregunta operativa adicional es:
*¿la parte tiene huella propia en* ``audit_log`` *que
sobrevive al todo?* Si sí, considerar agregación
(:doc:`agregacion-interfaces` § 2). Si no, composición
(§ 3 del mismo documento).

Resumen del progreso del modelo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tras § 15.7 (entidades importantes), § 15.8 (primera
relación / asociación) y § 15.9 (composiciones), el
modelo de dominio IACT cubre dos de los tres tipos de
relaciones de colaboración:

- **Asociación** — entidades sueltas conectadas por uso.
- **Composición** — entidades fuertemente atadas a un
  contenedor.

Falta el tipo intermedio: **agregación**. La introduce
:doc:`agregacion-interfaces` § 2 y los ejemplos
canónicos IACT son ``Grupo`` ◇ ``Funcion`` y
``Grupo`` ◇ ``Usuario``. La progresión completa de
relaciones de colaboración (las cuatro) está en § 1 de
:doc:`relaciones-uml`.

15.10 Definir agregaciones
--------------------------

Tras asociación (§ 15.8) y composición (§ 15.9), el
modelo aún puede crecer con un tipo intermedio: la
**agregación**. Es el "punto medio" entre las dos: hay
un padre identificable, pero la parte **sí puede existir
sin él**.

Ejemplo del libro citado
~~~~~~~~~~~~~~~~~~~~~~~~

Para el modelo Streamy, la entidad ``Actor`` no encaja
ni en asociación pura ni en composición:

- No es composición porque ``Actor`` puede existir sin
  un ``Title`` (puede pertenecer a varios títulos; si
  uno se elimina, el actor sigue presente en los
  otros).
- Tampoco es asociación pura: hay un ownership
  conceptual del lado de ``Title`` (el título "tiene"
  sus actores).

Esa relación se modela como **agregación**: diamante
**vacío** del lado del padre. En PlantUML se escribe
``o--`` (la letra ``o`` seguida de dos guiones).

Sintaxis PlantUML
~~~~~~~~~~~~~~~~~

.. code-block:: plantuml

   Title o-- Actor

Diferencias visuales con composición:

- Composición — diamante **relleno** (``*--``).
- Agregación — diamante **vacío** (``o--``).

Aplicado al ejemplo Streamy completo:

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   class Title
   class Genre
   class Season
   class Episode
   class Review
   class Actor

   Title -- Genre
   Title *-- Season
   Title *-- Review
   Title o-- Actor
   Season *-- Episode
   @enduml

El equivalente IACT — RBAC y agregaciones canónicas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El cluster RBAC de IACT (ver § 11 de
:doc:`agregacion-interfaces`) está construido sobre
agregaciones, no composiciones:

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   class Grupo
   class Funcion
   class Usuario
   class Permiso
   class ReglaSoD

   Grupo "1" o-- "*" Funcion : agrupa
   Grupo "1" o-- "*" Usuario : asigna
   ReglaSoD "1" -- "2..*" Funcion : restringe
   Permiso ..> Grupo : pertenece
   @enduml

Lectura:

- ``Grupo`` ◇ ``Funcion`` — **agregación**. Las
  funciones del catálogo RBAC existen
  independientemente de cualquier grupo. Eliminar un
  grupo no elimina las funciones (CNST_030 SoD se
  conserva a nivel de catálogo).
- ``Grupo`` ◇ ``Usuario`` — **agregación**. Los
  usuarios existen sin grupos; pueden pertenecer a
  varios; eliminar un grupo no elimina los usuarios.
- ``ReglaSoD`` ↔ ``Funcion`` — asociación: la regla
  referencia funciones del catálogo; ambas existen
  independientemente.

Otros ejemplos IACT de agregación
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``Reporte`` ◇ ``Filtro`` — los filtros pueden
  reutilizarse entre reportes; el reporte no destruye
  los filtros al cerrarse.
- ``Supervisor`` ◇ ``AlertaReconocida`` — el
  supervisor mantiene historial de alertas reconocidas;
  las alertas sobreviven aunque el supervisor cambie de
  rol.
- ``VentanaETL`` ◇ ``EjecucionETL`` — una ventana
  contiene varias ejecuciones; las ejecuciones quedan
  como evidencia auditable aunque la ventana se
  invalide (CNST_025 + CNST_006/008).

Tres tipos de relación de colaboración — resumen
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Con asociación, agregación y composición ya están
cubiertas las tres relaciones principales para modelar
**dominios**:

.. list-table::
 :widths: 22 22 28 28
 :header-rows: 1

 * - Tipo
   - Sintaxis PlantUML
   - Bond
   - Cuándo usarla
 * - **Asociación**
   - ``--``
   - Loose; sin owner.
   - Entidades sueltas conectadas por uso.
 * - **Agregación**
   - ``o--``
   - Medio; padre claro, hijo sobrevive.
   - Padre conceptual, partes reutilizables.
 * - **Composición**
   - ``*--``
   - Strong; hijo no existe sin padre.
   - Partes que mueren con el contenedor.

Cómo elegir entre los tres
~~~~~~~~~~~~~~~~~~~~~~~~~~

La pregunta progresiva de tres pasos:

1. ¿Las dos entidades existen totalmente
   independientes? → **asociación**.
2. Si no, ¿la "parte" puede vivir aunque desaparezca
   el "todo"? → **agregación**.
3. Si tampoco, ¿la parte muere con el todo? →
   **composición**.

Variabilidad de modelado
~~~~~~~~~~~~~~~~~~~~~~~~

Las decisiones de modelado **varían entre equipos** y
ambas pueden ser válidas. El autor citado lo ilustra
con el caso ``Actor``/``Cast``: si modelamos un
``Cast`` que agrupa a los actores específicos de un
``Title``, esa relación pasaría a **composición**
(cuando el título desaparece, el cast deja de tener
sentido), aunque ``Actor`` por sí mismo siga siendo
agregación.

En IACT esto se observa en
``EjecucionETL`` ↔ ``Llamada``:

- En § 15.9 lo modelamos como **asociación** — las
  llamadas existen independientemente de la ejecución
  que las cargó.
- Si introdujéramos un ``LoteIngestaETL`` que agrupe
  específicamente las llamadas cargadas en una
  ejecución particular, esa relación sería
  **composición** (el lote no tiene sentido sin la
  ejecución).

Ambas lecturas son legítimas. La elección depende del
**contexto del UC** (ver § 13 "Comparativa por
contexto" en :doc:`relaciones-uml`).

15.11 Decidir entre asociación, agregación y composición
--------------------------------------------------------

Tras los §§ 15.8-15.10 ya conocemos los **tres tipos**
de relación principales para modelado de dominio. La
pregunta operativa final: **¿cuál usar en cada caso?**

A veces es difícil decidir cuál refleja mejor la
interacción del mundo real, y los criterios **varían
entre colegas**. Si dos equipos modelan el mismo dominio,
casi seguro proponen no solo nombres distintos para las
entidades sino también **relaciones distintas**. Uno de
los beneficios principales del modelado de dominio es
**alinear a todos en los mismos constructos**: como todos
trabajan para la misma empresa, no hay un "correcto" y
un "incorrecto" absolutos — hay **entendimiento mutuo**.

Guía operativa
~~~~~~~~~~~~~~

**Asociación.** Hay relación entre las entidades; al
menos una mantiene una referencia a la otra. **Sin
dueño**. Ambas pueden existir totalmente independientes.

   Ejemplo educativo: ``Profesor`` ↔ ``Estudiante``.
   Ambos existen por su cuenta y se relacionan en
   contextos puntuales (clase concreta, tutoría).

**Agregación.** Relación más directa que una asociación,
pero las entidades **siguen pudiendo existir
independientemente**. Hay **un dueño**; si se elimina el
padre, el hijo permanece y mantiene sentido.

   Ejemplo educativo: ``Profesor`` ↔ ``Clase``. La
   clase tiene un profesor titular (owner), pero si el
   profesor deja la institución la clase puede seguir
   existiendo (con otro profesor).

**Composición.** La relación más estrecha. Hay **un
dueño**, pero a diferencia de la agregación, **eliminar
el padre obliga a eliminar al hijo**: el hijo no tiene
sentido sin el padre.

   Ejemplo educativo: ``Clase`` ↔ ``Calificación``. La
   calificación pertenece a una clase específica; sin
   esa clase, la calificación pierde sentido.

Aplicación al dominio IACT
~~~~~~~~~~~~~~~~~~~~~~~~~~

El mismo trío analógico al ámbito educativo, traducido
al dominio IACT:

.. list-table::
 :widths: 22 30 28 20
 :header-rows: 1

 * - Tipo
   - Pregunta clave
   - Ejemplo IACT
   - PlantUML
 * - **Asociación**
   - ¿Existen ambas independientes y se vinculan por
     uso?
   - ``ReglaSoD`` ↔ ``Funcion`` (la regla referencia
     funciones del catálogo).
   - ``--``
 * - **Agregación**
   - ¿Hay un dueño, pero el hijo sobrevive si se
     elimina el padre?
   - ``Grupo`` ◇ ``Funcion`` — eliminar un grupo no
     elimina las funciones del catálogo.
   - ``o--``
 * - **Composición**
   - ¿El hijo no tiene sentido sin el padre?
   - ``EjecucionETL`` ● ``ErrorETL`` — el error
     pertenece a la ejecución y desaparece como
     entidad de dominio si la ejecución se invalida.
   - ``*--``

Receta de tres preguntas progresivas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **¿Las entidades existen totalmente independientes,
   sin owner?** → asociación.
2. Si no: **¿el "hijo" sobrevive si desaparece el
   "padre"?** → agregación.
3. Si tampoco: **¿el hijo muere con el padre?** →
   composición.

La progresión va de menos a más fuerte. La regla
operativa de IACT (alineada con § 13 de
:doc:`relaciones-uml` y § 15-16 sobre composición vs
herencia): **componer salvo razón clara para
composición fuerte**, y dentro de la composición
preferir agregación si la parte tiene vida propia.

Sobre la subjetividad del modelado
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Una decisión razonable de un equipo puede ser razonable
de otra forma para otro equipo. Lo importante:

- **Aplicar el criterio consistentemente** dentro del
  mismo proyecto.
- **Documentar la elección** cuando hay duda razonable
  (ADR del subdominio).
- **Revisitar el modelo** si las premisas cambian (ver
  § 15.5 Evolución del modelo).

En IACT, el lenguaje compartido (``Llamada``,
``Segmento``, ``Reporte``, ``Alerta``, ``Sesion``,
``EventoAuditoria``) es **el contrato**. Cada relación
documentada es vinculante hasta que se modifique
explícitamente — eso es lo que mantiene el modelo vivo
y útil a lo largo del proyecto.

Cierre del módulo de relaciones
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Con asociación + agregación + composición ya están
cubiertos los tres tipos canónicos para modelar
**relaciones de colaboración**. Los siguientes ejes que
pueden enriquecer el modelo son:

- **Dependencia / uso** (§ 10 de :doc:`relaciones-uml`)
  — relación temporal, cuando dos entidades interactúan
  brevemente.
- **Generalización / herencia** (§§ 14-16 de
  :doc:`relaciones-uml`) — para jerarquías "es-un".
- **Realización** (§ 5 de
  :doc:`agregacion-interfaces`) — para
  implementación de interfaces.

Para crear un diagrama de dominio nuevo en IACT, basta
con seguir el flujo recorrido por §§ 15.7-15.11:

1. Identificar entidades importantes (anchor first).
2. Documentar la primera relación con asociación.
3. Identificar composiciones para partes inseparables.
4. Identificar agregaciones para partes que sobreviven.
5. Iterar agregando entidades vecinas.
6. Aplicar el criterio progresivo de tres preguntas
   para cada nueva relación.

Cuando el embrión esté estable y validado con
stakeholders, integrarlo al diagrama consolidado de
§ 7 de este documento.

15.12 Ejercicio: documentar tu propio dominio
---------------------------------------------

La obra citada cierra el capítulo de modelado con un
ejercicio: **construir tu propio modelo de dominio**.
Recomienda elegir entre cuatro opciones: una empresa
ficticia (como Streamy), una empresa conocida real, una
empresa donde se haya trabajado y que no tuviera modelo
documentado, o un proyecto personal. Sugerencia: empezar
con al menos **siete entidades** y mantener la elección
a lo largo de los capítulos siguientes.

El equivalente en IACT
~~~~~~~~~~~~~~~~~~~~~~

En este proyecto el ejercicio **ya está realizado** — el
dominio elegido es **IACT** (call center IVR + analytics
+ supervisión ETL + RBAC granular). El modelo de dominio
canónico vive en este cajón
``_metodologia-aplicacion/`` y se materializa
principalmente en este documento (``analisis-dominio.rst``)
y en sus hermanos.

Las **siete entidades mínimas** que el libro recomienda
para empezar están desbordadamente cubiertas — el modelo
IACT inventaría más de quince entidades canónicas
distribuidas por el cluster del dominio (§ 11 de
:doc:`agregacion-interfaces`):

.. list-table::
 :widths: 30 70
 :header-rows: 1

 * - Cluster
   - Entidades canónicas
 * - Auth + sesión
   - ``Usuario``, ``Sesion``, ``IntentoLogin``,
     ``ContadorThrottling``.
 * - RBAC + SoD
   - ``Funcion``, ``Grupo``, ``Permiso``, ``ReglaSoD``.
 * - Reportería
   - ``Reporte``, ``ReporteVolumen``,
     ``ReporteAbandono``, ``ConfiguracionExport``,
     ``TareaExport``, ``Filtro``.
 * - Alertas
   - ``Alerta``, ``UmbralAlerta``,
     ``EvaluadorAlertas``, ``EstadoAlerta``.
 * - ETL
   - ``EjecucionETL``, ``VentanaETL``, ``ErrorETL``,
     ``RegistroIngesta``.
 * - Auditoría
   - ``EventoAuditoria``, ``DetalleAuditoria``,
     ``ConsultaAudit``.
 * - Operacional
   - ``Llamada``, ``Segmento``, ``Supervisor``.

Cómo aplicar el ejercicio en este proyecto
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El "ejercicio" en IACT no es construir un modelo desde
cero — eso está hecho. La aplicación es **mantener y
evolucionar** el modelo:

1. Cuando aparezca un UC nuevo, **revisar** las
   entidades de la tabla anterior antes de crear
   nuevas.
2. Si el UC introduce un concepto realmente nuevo,
   **agregarlo** a este documento (§ 3 sustantivos →
   clases, § 7 diagrama consolidado, § 8
   responsabilidades).
3. Si el cambio es central, registrar la decisión en
   un **ADR del subdominio** correspondiente
   (``.thyrox/context/decisions/``).
4. Si una nueva relación entre entidades emerge,
   aplicar la **receta progresiva de tres preguntas**
   (§ 15.11) para clasificarla.
5. Mantener el ``ubiquitous language`` (§ 15.4) — usar
   el vocabulario del modelo en UCs, ADRs y commits.

Para nuevos contribuidores
~~~~~~~~~~~~~~~~~~~~~~~~~~

Quien se incorpora al proyecto puede usar este cajón
como **introducción al dominio**. La ruta recomendada:

1. Leer la sección "Concepto: análisis del dominio" al
   inicio de este documento.
2. Recorrer §§ 3-7 para captar el modelo desde el
   lenguaje natural.
3. Pasar a §§ 15.7-15.11 para entender la metodología
   DDD aplicada.
4. Consultar :doc:`orientacion-objetos` para los seis
   principios OOP en este dominio.
5. Para detalles de relaciones, ver
   :doc:`relaciones-uml` y
   :doc:`agregacion-interfaces`.

Continuidad con el resto de la documentación
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El libro citado anuncia que cada capítulo siguiente
**construye sobre el modelo de dominio** del primero.
Para IACT, esa misma continuidad ya está materializada:

- :doc:`casos-uso-especificacion` y
  :doc:`casos-uso-diagramas` — UCs construidos sobre
  las entidades del modelo.
- :doc:`diagramas-secuencias` y
  :doc:`diagramas-colaboraciones` — interacciones entre
  esas mismas entidades.
- :doc:`diagramas-estados` — ciclos de vida de
  entidades como ``Sesion`` y ``Alerta``.
- :doc:`diagramas-actividades` — flujos que recorren
  varias entidades del modelo.
- :doc:`diagramas-componentes` y
  :doc:`diagramas-distribucion` — proyección física del
  modelo en apps Django y nodos.

El modelo del dominio es el **eje** sobre el que gira
toda la documentación del cajón. Cualquier nuevo
diagrama o UC debe **anclarse** en él.

15.13 Relación con el resto del documento
-----------------------------------------

DDD no es una metodología aislada — se combina con las
escuelas de § 13:

- **Análisis clásico** (§ 13.1) provee la
  categorización sistemática de conceptos del dominio
  (cosas tangibles, eventos, organizaciones).
- **Análisis basado en escenarios** (§ 13.2) refina el
  modelo con casos concretos.
- **RDD** (§ 13.3) asigna responsabilidades a las
  entidades del dominio identificadas.

Las **tarjetas CRC** (§ 14) son la herramienta operativa
para sesiones colaborativas DDD; los **diagramas de
clases UML** son el artefacto persistente del modelo.

----

16. Enriquecer el modelo de dominio
===================================

El § 15 estableció **lo básico** del modelado de dominio:
identificar entidades, primera relación, los tres tipos
de relación (asociación / agregación / composición) y
cómo decidir entre ellos. Pero hay mucho más que el
modelo puede decir.

Esta sección introduce los **enriquecimientos** que
elevan un modelo embrionario a un modelo operativo
maduro, con información más rica para quien lo lea:

- **Herencia** — para mostrar subtipos (variantes
  específicas de una entidad genérica).
- **Descripciones** — atributos y operaciones de cada
  entidad, no solo el nombre y las relaciones.
- **Multiplicidad** — la cardinalidad explícita de las
  relaciones (uno, varios, exacto, rango).

Estos tres enriquecimientos están ya cubiertos en
profundidad en este cajón; esta sección los **encuadra
desde la perspectiva del modelado de dominio** y los
ancla a las secciones donde se desarrolla cada uno.

16.1 Dónde vive cada enriquecimiento en el cajón
------------------------------------------------

.. list-table::
 :widths: 25 30 45
 :header-rows: 1

 * - Enriquecimiento
   - Documento principal
   - Secciones relevantes
 * - **Herencia / subtipos**
   - :doc:`relaciones-uml`
   - § 7 (herencia básica), §§ 14.1-14.4 (cuatro
     tipos de herencia), § 15 (herencia vs
     composición), § 16 (principios fundamentales y
     guía de decisión).
 * - **Atributos y operaciones**
     (descripciones)
   - Este documento (``analisis-dominio.rst``) y
     :doc:`orientacion-objetos`.
   - § 3 (sustantivos→clases), § 4 (verbos→
     operaciones), § 5 (adjetivos→atributos), § 6
     (clase ``Reporte`` completa) +
     :doc:`orientacion-objetos` § 5
     (Encapsulamiento).
 * - **Multiplicidad**
   - :doc:`relaciones-uml`
   - § 3 (multiplicidades canónicas IACT) y § 2.7
     (Aerolínea/Ruta como ejemplo N:M).

16.2 Por qué importan en IACT
-----------------------------

Un modelo de dominio sin estos enriquecimientos es **un
diagrama de cajas y líneas** — útil como punto de
partida pero insuficiente para guiar la implementación.
Con ellos:

- **Herencia** permite distinguir entre ``Reporte``
  base y sus variantes (``ReporteVolumen``,
  ``ReporteAbandono``, ``ReporteSoDCompliance``) —
  fundamental para aplicar Factory y Strategy
  (:doc:`patrones-diseno`).
- **Descripciones** capturan los atributos del dominio
  (``Llamada.duracion_seg``, ``Sesion.creada_en``) y
  las operaciones canónicas
  (``Reporte.exportar(formato)``) — sin ellos los
  consumidores del modelo deben inferir o suponer.
- **Multiplicidad** distingue ``Llamada → 1 Segmento``
  (BR_012) de ``Llamada → * Reporte``: la diferencia
  es operativa, afecta validaciones y queries.

16.3 Progresión recomendada
---------------------------

El orden natural para enriquecer un modelo:

1. **Empezar simple** — entidades + asociaciones
   (§ 15.7-15.8).
2. **Identificar relaciones fuertes** — composiciones y
   agregaciones (§§ 15.9-15.10).
3. **Agregar multiplicidad** — sin números, las
   relaciones son ambiguas
   (:doc:`relaciones-uml` § 3).
4. **Detectar subtipos** — donde varias entidades
   compartan estructura, considerar herencia
   (:doc:`relaciones-uml` § 7 y § 14.1).
5. **Llenar atributos y operaciones** —
   sustantivos→clases, verbos→operaciones (§§ 3-4 de
   este documento).
6. **Validar el modelo** con stakeholders y revisar
   contra los UCs documentados.

Los pasos 3, 4 y 5 son los **enriquecimientos** que el
libro citado introduce en su segundo capítulo. Las
subsecciones siguientes desarrollan cada uno cuando un
mensaje del autor lo amerite.

----

16.4 Describir las relaciones
-----------------------------

Una característica clave de los modelos de dominio en
UML es que **se puede y se debe** describir **cómo
interactúan las entidades** en cada relación. Sin
descripciones, las relaciones quedan en cajas y líneas
ambiguas.

Por defecto, muchas relaciones se pueden describir como
``has`` (tiene). El consejo del libro citado: ser tan
**descriptivo como sea posible** y **evitar** usar
``has`` para todo cuando exista una etiqueta más
precisa.

Sintaxis PlantUML
~~~~~~~~~~~~~~~~~

PlantUML acepta la etiqueta de la relación con dos
puntos al final de la línea, igual que Mermaid:

.. code-block:: plantuml

   Title --  Genre   : is associated with
   Title *-- Season  : has
   Title *-- Review  : has
   Title o-- Actor   : features
   Season *-- Episode : contains
   Viewer --> Title  : watches

Lectura del modelo enriquecido del libro
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El ejemplo Streamy completo con descripciones e
inheritance + Viewer:

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class Title
   class Genre
   class Season
   class Episode
   class Review
   class Actor
   class Viewer
   class TVShow
   class Short
   class Film

   Title -- Genre : is associated with
   Title *-- Season : has
   Title *-- Review : has
   Title o-- Actor : features
   Season *-- Review : has
   Season *-- Episode : contains
   Episode *-- Review : has
   Viewer --> Title : watches

   TVShow --|> Title : implements
   Short --|> Title : implements
   Film --|> Title : implements
   @enduml

Análisis de las decisiones del modelo:

- **``Title -- Genre : is associated with``** —
  asociación bidireccional. La descripción debe ser
  válida en ambos sentidos: un título *está asociado
  con* un género y un género *está asociado con*
  títulos.
- **``Viewer --> Title : watches``** —
  asociación **direccional**. ``Viewer`` mantiene
  referencia a ``Title``; ``Title`` no necesita
  referencia inversa al espectador. Por eso el
  ``-->`` en lugar del ``--`` bidireccional.
- **``Title *-- Season : has``**,
  **``Title *-- Review : has``**,
  **``Season *-- Episode : contains``** — composición
  con etiqueta descriptiva desde el padre. ``contains``
  es más preciso que ``has`` en este caso.
- **``Title o-- Actor : features``** — agregación con
  etiqueta más rica que ``has``: un título no
  simplemente "tiene" actores; los **presenta**.
- **``TVShow --|> Title : implements``** — generalización
  con etiqueta. ``implements`` o ``extends`` clarifican
  para lectores no familiarizados con la flecha de
  herencia que se trata de una jerarquía.

Reglas para escribir descripciones
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Verbos precisos** — preferir ``contains``,
   ``features``, ``watches``, ``implements`` antes que
   un ``has`` genérico.
2. **Bidireccional debe leerse en ambos sentidos** —
   ``is associated with`` cumple; ``has`` aplicado a
   ``Title -- Genre`` no funcionaría en sentido
   inverso ("Genre has Title" suena raro).
3. **Direccional desde el padre** — para
   composición/agregación, el verbo se lee del padre
   hacia la parte (``Season contains Episode``, no
   "Episode is contained in Season").
4. **``-->`` para una sola dirección** — cuando solo un
   lado mantiene referencia. ``Viewer --> Title``: la
   vista del catálogo que el espectador navega.

Aplicación a IACT
~~~~~~~~~~~~~~~~~

Aplicado al diagrama del modelo IACT consolidado (§ 7),
las descripciones precisas refuerzan la legibilidad:

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class Llamada
   class Segmento
   class EjecucionETL
   class VentanaETL
   class ErrorETL
   class Reporte
   class Filtro
   class Alerta
   class Supervisor
   class Usuario
   class Sesion
   class Grupo
   class Funcion
   class EventoAuditoria

   Llamada "1..*" -- "1" Segmento : pertenece a
   VentanaETL "1" -- "*" EjecucionETL : contiene
   EjecucionETL "*" -- "*" Llamada : carga
   EjecucionETL "1" *-- "*" ErrorETL : produce
   Reporte "*" -- "*" Llamada : agrega
   Reporte "1" o-- "*" Filtro : aplica
   Alerta "*" -- "1" Supervisor : es reconocida por
   Sesion "1" *-- "1" Usuario : pertenece a
   Usuario "*" o-- "*" Grupo : asignado a
   Grupo "*" o-- "*" Funcion : agrupa
   Usuario "1" --> "*" EventoAuditoria : genera
   @enduml

Notar:

- **``pertenece a``**, **``contiene``**, **``carga``**,
  **``agrega``**, **``aplica``**, **``es reconocida por``**
  — verbos precisos del dominio en lugar de ``has``
  genérico.
- **``Usuario --> EventoAuditoria : genera``** —
  asociación direccional. El ``EventoAuditoria`` no
  mantiene referencia bidireccional al usuario en
  sentido funcional; el flujo es solo "usuario genera
  evento" (CNST_025: el evento es inmutable y no se
  reasigna).
- **``Alerta -- Supervisor : es reconocida por``** —
  bidireccional, descripción válida en ambos sentidos
  con la misma frase desde el lado de la alerta.

Subtipos con etiqueta ``implements``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Aplicado al cluster de reportes IACT
(:doc:`relaciones-uml` § 14.1):

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   abstract class Reporte
   class ReporteVolumen
   class ReporteAbandono
   class ReporteSoDCompliance

   ReporteVolumen --|> Reporte : implements
   ReporteAbandono --|> Reporte : implements
   ReporteSoDCompliance --|> Reporte : implements
   @enduml

La etiqueta ``implements`` (o ``extends``) hace
explícito para lectores no familiarizados con la
flecha que estamos ante una jerarquía donde ``Reporte``
es el tipo abstracto y los demás son variantes
concretas.

Reglas IACT para descripciones
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Vocabulario del ubiquitous language** (§ 15.4) —
   usar verbos del dominio: ``carga`` (ETL),
   ``reconoce`` (alerta), ``aplica`` (filtro),
   ``audita`` (CNST_025).
2. **Evitar ``has`` cuando exista verbo más preciso**.
3. **``-->`` para asimetrías reales** — cuando solo un
   lado conoce al otro.
4. **Bidireccional debe leerse simétricamente** — si la
   descripción no funciona en ambos sentidos, no es
   bidireccional.
5. **No omitir descripciones** en relaciones críticas
   (audit, SoD, ETL) — la ambigüedad invita a
   malinterpretaciones.

Cuando un equipo tiene dudas sobre la etiqueta correcta,
mirar el **UC** que ejercita la relación: la descripción
del flujo principal del UC suele contener el verbo
adecuado.

16.5 Agregar multiplicidad
--------------------------

El último enriquecimiento del modelo de dominio es la
**multiplicidad**: cuántas instancias de cada entidad
intervienen en una relación. El término suena complejo
pero la idea es la familiar de las bases de datos
relacionales: 1:1, 1:N, N:M, etc.

Por qué importa
~~~~~~~~~~~~~~~

En el modelo escribimos las entidades en **singular**
(``Title``, ``Season``, ``Llamada``, ``Reporte``)
porque el código usará nombres singulares para las
clases. Pero la realidad puede ser plural — un
``Title`` puede tener varias ``Season``, una
``EjecucionETL`` carga varias ``Llamada``. Sin
multiplicidad explícita, el lector tiene que **adivinar**
si la relación es 1:1, 1:N o N:M.

Si escribimos las entidades en plural para "compensar",
caemos en el error opuesto: el lector asume que siempre
hay varias, incluso cuando puede haber una sola.

La multiplicidad resuelve la ambigüedad: deja todas las
entidades en singular y **anota la cardinalidad** del
lado de la relación.

Sintaxis PlantUML
~~~~~~~~~~~~~~~~~

Idéntica a Mermaid: cardinalidad entre comillas a cada
lado del operador.

.. code-block:: plantuml

   Title "1" *-- "0..*" Season : has
   Title "1..*" -- "1..*" Genre : is associated with
   Viewer "0..*" --> "0..*" Title : watches

Cardinalidades canónicas:

.. list-table::
 :widths: 18 32 50
 :header-rows: 1

 * - Notación
   - Significado
   - Ejemplo
 * - ``"1"``
   - Exactamente uno.
   - Una ``Llamada`` pertenece a **un**
     ``Segmento``.
 * - ``"0..1"``
   - Cero o uno (opcional).
   - Una ``Sesion`` puede tener cero o un
     ``TokenRefresh``.
 * - ``"1..*"``
   - Uno o varios (al menos uno).
   - Un ``Segmento`` tiene **al menos una**
     ``Llamada`` (si lo modelamos como obligatorio).
 * - ``"0..*"`` o ``"*"``
   - Ninguno o varios.
   - Un ``Reporte`` puede tener cero o más
     ``Filtro`` aplicados.
 * - ``"n..m"``
   - Rango específico (raro).
   - Una ``ReglaSoD`` involucra exactamente 2 a 3
     ``Funcion``.

Cómo leer una relación con multiplicidad
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

La cardinalidad de una entidad se escribe **en el lado
opuesto** de la relación. Esto puede confundir al
principio porque la primera cardinalidad que se ve al
leer de izquierda a derecha **no es** la del primer
elemento.

Para el ejemplo del libro:

.. code-block:: plantuml

   Title "1" *-- "0..*" Season : has

Lectura correcta:

- ``Title`` tiene **0 o más** ``Season``.
- ``Season`` pertenece a **1** ``Title``.

Truco mnemotécnico (del libro citado): al leer una
relación, **ignorar la primera cardinalidad** y tomar la
**segunda** como la del primer elemento. Funciona en
ambas direcciones.

Decisión 0..* vs 1..*
~~~~~~~~~~~~~~~~~~~~~

La elección depende del dominio:

- **0..*** — admite la entidad sin esa parte. En el
  ejemplo Streamy, un ``Title`` puede tener cero
  ``Season`` (solo tráiler con "próximamente").
- **1..*** — la parte es obligatoria. Una temporada
  con cero episodios no tiene sentido (por eso el libro
  modela ``Season`` ↔ ``Episode`` como ``1..*``).

En IACT esta decisión se toma a la luz de las reglas de
negocio (BR_*) y restricciones (CNST_*).

Ejemplo Streamy completo con multiplicidad
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Reproducción del modelo cerrado del libro:

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class Title
   class Genre
   class Season
   class Episode
   class Review
   class Actor
   class Viewer
   class TVShow
   class Short
   class Film

   Title "1..*" -- "1..*" Genre : is associated with
   Title "1" *-- "0..*" Season : has
   Title "1" *-- "0..*" Review : has
   Title "1..*" o-- "0..*" Actor : has
   Season "1" *-- "0..*" Review : has
   Season "1" *-- "1..*" Episode : has
   Episode "1" *-- "0..*" Review : has
   Viewer "0..*" --> "0..*" Title : watches

   TVShow --|> Title : implements
   Short --|> Title : implements
   Film --|> Title : implements
   @enduml

Cada cardinalidad refleja una decisión de modelado
explícita: un título tiene **al menos un** género, puede
tener **0 a muchas** temporadas, **al menos un** actor;
una temporada tiene **al menos un** episodio (no existe
temporada vacía); los espectadores y títulos se
relacionan **muchos a muchos**.

Aplicación al modelo IACT
~~~~~~~~~~~~~~~~~~~~~~~~~

Modelo IACT consolidado con multiplicidad anclada a las
reglas del dominio:

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class Llamada
   class Segmento
   class EjecucionETL
   class VentanaETL
   class ErrorETL
   class Reporte
   class Filtro
   class Alerta
   class Supervisor
   class Usuario
   class Sesion
   class Grupo
   class Funcion
   class EventoAuditoria
   class ReglaSoD

   Llamada "1..*" -- "1" Segmento : pertenece a
   VentanaETL "1" -- "0..*" EjecucionETL : contiene
   EjecucionETL "1..*" -- "0..*" Llamada : carga
   EjecucionETL "1" *-- "0..*" ErrorETL : produce
   Reporte "1..*" -- "0..*" Llamada : agrega
   Reporte "1" o-- "0..*" Filtro : aplica
   Alerta "0..*" -- "0..1" Supervisor : es reconocida por
   Sesion "1" *-- "1" Usuario : pertenece a
   Usuario "0..*" o-- "0..*" Grupo : asignado a
   Grupo "1..*" o-- "0..*" Funcion : agrupa
   Usuario "1" --> "0..*" EventoAuditoria : genera
   ReglaSoD "0..*" -- "2..3" Funcion : restringe
   @enduml

Decisiones IACT explicadas
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
 :widths: 35 25 40
 :header-rows: 1

 * - Relación
   - Multiplicidad elegida
   - Razón del dominio
 * - ``Llamada → Segmento``
   - ``"1..*" : "1"``
   - BR_012: cada llamada pertenece a **un** único
     segmento; un segmento puede tener muchas
     llamadas.
 * - ``EjecucionETL → ErrorETL``
   - ``"1" : "0..*"``
   - Una ejecución produce **0 o más** errores. El
     caso ideal es 0; con errores la composición se
     materializa.
 * - ``Alerta → Supervisor``
   - ``"0..*" : "0..1"``
   - Una alerta puede no haber sido reconocida (0)
     o haberlo sido por un único supervisor (1). Un
     supervisor reconoce muchas alertas.
 * - ``Sesion → Usuario``
   - ``"1" : "1"``
   - CNST_002: una sesión pertenece a un **único**
     usuario; el usuario puede tener una **única**
     sesión activa.
 * - ``Usuario → Grupo``
   - ``"0..*" : "0..*"``
   - Asignación N:M; un usuario puede pertenecer a
     varios grupos y un grupo puede tener varios
     usuarios.
 * - ``ReglaSoD → Funcion``
   - ``"0..*" : "2..3"``
   - CNST_030: una regla de SoD relaciona típicamente
     entre 2 y 3 funciones que no pueden coexistir
     en el mismo grupo.

Reglas IACT para multiplicidad
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Toda relación documentada debe tener
   multiplicidad** — su omisión es ambigüedad.
2. **Anclar al BR/CNST cuando aplique** — el "1" del
   segmento por llamada viene de BR_012; el "1" en
   ``Sesion → Usuario`` viene de CNST_002.
3. **Preferir 0..* a 1..* cuando la realidad lo
   admita** — el modelo debe permitir el estado
   inicial vacío (un grupo recién creado sin
   funciones asignadas, una ventana ETL sin
   ejecuciones aún).
4. **Documentar rangos específicos** (``2..3``) cuando
   un BR/CNST lo establezca explícitamente.
5. **Diferenciar 0..1 de 1** — opcional vs obligatorio.
   Una ``Alerta`` puede no estar reconocida; una
   ``Sesion`` siempre pertenece a un usuario.

Cierre del módulo de enriquecimiento
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Con descripciones (§ 16.4) y multiplicidad (§ 16.5), un
modelo de dominio pasa de **embrionario** a
**operativo**. Combinado con la herencia (§ 7 y § 14.1
de :doc:`relaciones-uml`) y los atributos/operaciones
(§§ 3-6 de este documento), el modelo está listo para:

- Servir como contrato compartido con stakeholders
  (DDD § 15.2).
- Guiar la implementación en clases Django.
- Detectar inconsistencias antes de que se materialicen
  en código.
- Evolucionar de manera disciplinada (§ 15.5).

Para más detalle sobre multiplicidad, ver el
tratamiento canónico en :doc:`relaciones-uml` § 3 con la
tabla completa de notaciones y los casos canónicos del
proyecto.

16.6 Agregar un título al diagrama
----------------------------------

Una de las primeras buenas prácticas al diagramar es
**siempre poner un título**. La idea viene de los
gráficos: un gráfico sin título tiende a malinterpretarse;
un diagrama UML, igual.

Sintaxis PlantUML
~~~~~~~~~~~~~~~~~

PlantUML acepta títulos directamente con la directiva
``title``, sin necesidad de bloque YAML como Mermaid:

.. code-block:: plantuml

   @startuml
   !include ../../_static/plantuml-styles.puml
   title Modelo de dominio IACT
   ...
   @enduml

También admite títulos con varias líneas y formato
básico:

.. code-block:: plantuml

   title Modelo de dominio IACT\nv1.0 — abril 2026

Cómo se ve aplicado
~~~~~~~~~~~~~~~~~~~

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   title Modelo de dominio IACT — cluster RBAC
   class Usuario
   class Grupo
   class Funcion
   Usuario "0..*" o-- "0..*" Grupo : asignado a
   Grupo "1..*" o-- "0..*" Funcion : agrupa
   @enduml

El título aparece centrado en la parte superior del
diagrama, ofreciendo contexto inmediato sin que el
lector tenga que leer el cuerpo para entender de qué
trata.

Reglas IACT para títulos
~~~~~~~~~~~~~~~~~~~~~~~~

1. **Todo diagrama publicado** en este cajón debe
   tener título — un diagrama sin título es ambiguo
   fuera del contexto inmediato del párrafo que lo
   introduce.
2. **El título debe ser informativo del alcance**:
   "Modelo de dominio IACT" es genérico; "Modelo de
   dominio IACT — cluster RBAC" es específico.
3. **Convención de nombre**: ``[propósito] — [alcance]``.
   Ejemplos:

   - ``Diagrama de clases — entidad Llamada``
   - ``Diagrama de secuencias — UC_RPT_04 export``
   - ``Diagrama de despliegue — vm-iact``
4. **Sin emojis**, sin caracteres decorativos —
   coherencia con la convención general del repositorio.
5. **Coincidencia con el caption del bloque RST** — si
   el bloque ``.. uml::`` está bajo un encabezado
   "Ejemplo IACT — UC_RPT_04", el título del diagrama
   debe ser coherente con ese encabezado.

Excepciones permitidas
~~~~~~~~~~~~~~~~~~~~~~

Los **fragmentos pequeños embebidos en explicaciones de
sintaxis** (como las ilustraciones de "asociación",
"composición", "agregación" usadas en este documento
para mostrar la diferencia visual) pueden omitir el
título: están claramente subordinados al texto
adyacente. La regla aplica a **diagramas que pueden
extraerse y leerse aisladamente** — esos sí requieren
título.

16.7 Mejorar la legibilidad
---------------------------

A medida que un modelo de dominio crece (entidades,
relaciones, multiplicidad, herencia, descripciones), el
**layout** del diagrama puede volverse confuso si se
deja al renderer decidir todo. La obra citada describe
el problema en Mermaid: control limitado, *workarounds*
con líneas en blanco para "agrandar" cajas y depender
de CSS solo si se renderiza el sitio propio.

PlantUML ofrece **más control nativo**. Esta sección
documenta los mecanismos disponibles y la política IACT
para usarlos.

Mecanismos PlantUML para layout y legibilidad
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
 :widths: 28 38 34
 :header-rows: 1

 * - Mecanismo
   - Qué hace
   - Cuándo usarlo
 * - **``skinparam``**
   - Configura estilos globales: padding, tamaño de
     fuente, color, sombras, esquinas redondeadas.
   - Centralizar en
     ``source/_static/plantuml-styles.puml`` y
     reutilizar con ``!include``.
 * - **Dirección de la flecha**
     (``-down->``, ``-up->``, ``-left->``,
     ``-right->``)
   - Fuerza la dirección del enlace; el renderer
     respeta la pista.
   - Cuando el layout automático genera líneas
     cruzadas o entidades importantes apretadas.
 * - **``together { }``**
   - Agrupa varias clases para que el renderer las
     coloque cerca.
   - Cluster con varias clases que pertenecen al
     mismo subdominio.
 * - **``hide ...``** / **``show ...``**
   - Oculta o muestra compartimentos (atributos,
     métodos, encabezados de tipo).
   - En diagramas de dominio, ocultar compartimentos
     vacíos para un look limpio.
 * - **Notas (``note``)**
   - Agrega anotaciones con flecha al elemento que
     describen.
   - Restricciones, justificaciones, referencias a
     CNST/BR.
 * - **``package "Nombre" { }``**
   - Encierra clases en un paquete con caja
     etiquetada.
   - Visualizar clusters del modelo.

Política IACT
~~~~~~~~~~~~~

1. **Usar siempre** ``!include
   ../../_static/plantuml-styles.puml`` al inicio del
   bloque. Concentra todos los ``skinparam`` en un
   archivo único — DRY (§ 13 de
   :doc:`orientacion-objetos`).
2. **No** repetir ``skinparam`` dentro de un diagrama
   individual. Si un diagrama necesita ajustes
   particulares, evaluar si es mejor extender
   ``plantuml-styles.puml`` o si la necesidad es
   excepcional.
3. **Evitar el truco Mermaid** de agregar líneas en
   blanco al cuerpo de la clase para "agrandarla". En
   PlantUML el padding y el tamaño de fuente se
   controlan con ``skinparam`` — usar la herramienta
   correcta.
4. **Ocultar compartimentos vacíos** en diagramas de
   dominio puro:

   .. code-block:: plantuml

      hide empty members

   Esto evita las dos cajas vacías que aparecen bajo
   el nombre cuando la clase no declara atributos ni
   métodos.
5. **Forzar dirección** solo cuando el layout
   automático genera cruces. Por defecto dejar que el
   renderer decida.
6. **Agrupar** clases del mismo cluster con
   ``package`` o ``together`` cuando el diagrama supere
   las 8 entidades.

Ejemplo IACT — diagrama limpio sin compartimentos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Aplicando ``hide empty members``:

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   title Modelo de dominio IACT — vista compacta

   hide empty members

   class Llamada
   class Segmento
   class EjecucionETL
   class Reporte
   class Usuario
   class Sesion
   class EventoAuditoria

   Llamada "1..*" -- "1" Segmento : pertenece a
   EjecucionETL "1..*" -- "0..*" Llamada : carga
   Reporte "1..*" -- "0..*" Llamada : agrega
   Sesion "1" *-- "1" Usuario : pertenece a
   Usuario "1" --> "0..*" EventoAuditoria : genera
   @enduml

Las cajas son más compactas: solo aparece el nombre de
la entidad, sin compartimentos vacíos.

Ejemplo IACT — agrupación con ``package``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cuando el diagrama crece, agrupar clusters facilita la
lectura:

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   title Modelo de dominio IACT — clusters

   hide empty members

   package "Auth + Sesion" {
     class Usuario
     class Sesion
   }

   package "RBAC" {
     class Grupo
     class Funcion
   }

   package "Operacional" {
     class Llamada
     class Segmento
   }

   package "Auditoria" {
     class EventoAuditoria
   }

   Sesion "1" *-- "1" Usuario : pertenece a
   Usuario "0..*" o-- "0..*" Grupo : asignado a
   Grupo "1..*" o-- "0..*" Funcion : agrupa
   Llamada "1..*" -- "1" Segmento : pertenece a
   Usuario "1" --> "0..*" EventoAuditoria : genera
   @enduml

Los clusters se ven inmediatamente como cajas, sin
necesidad de inferirlos del nombre o la posición.

Trade-off legibilidad vs mantenibilidad
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

La obra citada lo nota: a veces hay que **sacrificar
estilo a cambio de un diagrama mantenible y
actualizable**. La política IACT extiende esa premisa:

- Preferir un diagrama **menos pulido pero
  text-as-code** antes que un diagrama "perfecto"
  hecho a mano que diverge del modelo.
- La consistencia entre diagramas (mismo
  ``plantuml-styles.puml``) vale más que la
  optimización individual.
- Si un diagrama es difícil de leer, **dividirlo** en
  varios — uno por cluster, vista, UC — antes que
  comprimir todo en uno solo.

Anti-patrones IACT
~~~~~~~~~~~~~~~~~~

- ``skinparam`` repetidos en cada diagrama (en lugar
  de en el archivo central).
- Líneas en blanco "fantasma" copiando el truco
  Mermaid.
- ``-down->``, ``-up->`` aplicados a todas las
  flechas: rigidiza el layout sin necesidad y
  dificulta el mantenimiento.
- Diagramas con 20+ entidades sin ``package`` ni
  ``together``: ilegibles.
- Mezclar ``hide empty members`` con clases que sí
  declaran atributos: produce diagramas inconsistentes.

16.8 Enriquecer los nodos con enlaces
-------------------------------------

Cada nodo de un diagrama puede convertirse en un
**enlace clickable** hacia documentación externa o
hacia otra parte del cajón. La obra citada destaca este
"toque mágico" para vincular cada entidad con su
documentación correspondiente.

Sintaxis PlantUML
~~~~~~~~~~~~~~~~~

PlantUML soporta enlaces con la directiva ``url``:

.. code-block:: plantuml

   class Reporte [[https://example.com/reporte]]

O con etiqueta y target:

.. code-block:: plantuml

   class Reporte [[https://example.com/reporte Doc]]
   url of Reporte is [[https://example.com/reporte{tooltip} target]]

Sintaxis equivalente en Mermaid (para referencia,
**no para uso en el proyecto**):

.. code-block:: text

   link Reporte "https://example.com/reporte" _blank

Aplicación a IACT — vincular al UC y al ADR
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

En IACT el patrón natural es vincular cada entidad del
modelo a:

1. **El UC** que ejercita la entidad como protagonista
   (por ejemplo ``Reporte`` → UC_RPT_*).
2. **El ADR** que decidió aspectos centrales de su
   modelado (por ejemplo ``EventoAuditoria`` → ADR
   sobre CNST_025).
3. **La sección** del cajón que la trata en
   profundidad.

Sin embargo, **Sphinx ya provee mecanismos nativos**
mejores que el ``url`` de PlantUML:

- **``:doc:```** — links a otros archivos RST.
- **``:ref:```** — links a etiquetas ``.. _label:``
  internas.
- **``:py:class:```** — links a clases Python
  documentadas.

Política IACT
~~~~~~~~~~~~~

1. **Preferir links Sphinx en el texto adyacente al
   diagrama** antes que ``url`` dentro del PlantUML.
   El texto RST captura mejor la intención y participa
   del sistema de referencias cruzadas del proyecto.
2. **Usar ``url`` PlantUML** solo cuando el destino
   sea **externo** y persistente (RFC, IETF, ISO,
   documentación oficial de la organización).
3. **No** apuntar a recursos efímeros (issues,
   borradores, branches) — el diagrama vive más que la
   URL.
4. Si un nodo del diagrama merece varios enlaces
   (UC, ADR, BR, CNST), **dejar la lista en el texto
   adyacente** y mantener el diagrama limpio.

Ejemplo IACT — vinculación textual recomendada
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   title Modelo de dominio IACT — entidades de auditoria
   hide empty members
   class EventoAuditoria
   class DetalleAuditoria
   EventoAuditoria "1" *-- "1..*" DetalleAuditoria : detalla
   @enduml

**Referencias** asociadas a cada entidad (en el texto,
no en el diagrama):

- ``EventoAuditoria`` — definida en § 3 de este
  documento, restricción CNST_025 (auditoría
  inmutable), UCs que la generan: todos los UCs del
  catálogo (audit transversal).
- ``DetalleAuditoria`` — composición fuerte (§ 3 de
  :doc:`agregacion-interfaces`). Usada en
  :doc:`patrones-diseno` § 8 (Observer +
  ``AuditObserver``).

Cuándo sí usar ``url`` PlantUML
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Casos legítimos en IACT:

- Apuntar al **estándar UML** original (``omg.org/uml``)
  desde un diagrama pedagógico introductorio.
- Apuntar a la **documentación oficial Django** desde
  un diagrama de despliegue.
- Apuntar a **RFC** relevantes (LDAP, TLS) desde un
  diagrama de integración.

En todos los demás casos, mantener el diagrama
**autocontenido** y dejar las referencias en el texto
RST circundante donde Sphinx puede gestionarlas.

Cierre del módulo de enriquecimiento
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Con descripciones (§ 16.4), multiplicidad (§ 16.5),
título (§ 16.6), legibilidad (§ 16.7) y enlaces
(§ 16.8), el modelo de dominio queda **completo** desde
la perspectiva de visualización. Los seis enriquecimientos
trabajan juntos:

- **Subtipos / herencia** — para variantes de una
  entidad genérica.
- **Descripciones** — verbos del dominio en cada
  relación.
- **Multiplicidad** — cardinalidad anclada a BR/CNST.
- **Título** — contexto inmediato.
- **Layout limpio** — packages, hide empty members,
  estilos centralizados.
- **Enlaces** (selectivos) — para conectar el diagrama
  al resto de la documentación.

A partir de aquí el modelo es la **fuente de verdad**
operativa del dominio IACT, lista para guiar
implementación, validación, evolución y onboarding
(ver § 15.5 Evolución y § 15.12 Ejercicio).

16.9 Ejercicio: enriquecer tu modelo de dominio
-----------------------------------------------

La obra citada cierra este capítulo con un ejercicio:
**enriquecer el modelo embrionario** del capítulo
anterior agregando los cinco enriquecimientos cubiertos.

Lista del ejercicio
~~~~~~~~~~~~~~~~~~~

1. Si aplica al dominio, agregar **generalizaciones**
   (herencia / subtipos). Aunque no sea perfecto en el
   dominio, hacerlo brevemente para fijar la sintaxis.
2. Agregar **descripciones** a todas las relaciones.
3. Definir **multiplicidad** en todas las relaciones.
4. Probar **ajustes de layout** según lo aprendido en
   "Mejorar la legibilidad".
5. **Vincular** un nodo a una página externa y probar
   el enlace.

Aplicación a IACT
~~~~~~~~~~~~~~~~~

Como en § 15.12, en IACT el ejercicio **ya está
realizado** y mantenido vivo en este cajón:

.. list-table::
 :widths: 30 70
 :header-rows: 1

 * - Punto del ejercicio
   - Cómo está cubierto en IACT
 * - Generalizaciones
   - § 7 de este documento (jerarquía ``Reporte`` con
     subclases) + §§ 14.1-14.4 de
     :doc:`relaciones-uml` (cuatro tipos de herencia)
     + § 16 de :doc:`relaciones-uml` (guía de
     decisión).
 * - Descripciones
   - § 16.4 de este documento — todas las relaciones
     IACT documentadas con verbos del **ubiquitous
     language** (``pertenece a``, ``carga``,
     ``produce``, ``agrega``, ``aplica``,
     ``es reconocida por``, ``genera``).
 * - Multiplicidad
   - § 16.5 de este documento + § 3 de
     :doc:`relaciones-uml` (tabla canónica de
     multiplicidades IACT con anclaje a BR/CNST).
 * - Layout
   - § 16.7 de este documento — política
     ``hide empty members``, ``package``, estilos
     centralizados en
     ``source/_static/plantuml-styles.puml``.
 * - Enlaces
   - § 16.8 de este documento — preferencia por
     ``:doc:`` y ``:ref:`` Sphinx sobre ``url``
     PlantUML inline; uso de ``url`` PlantUML
     reservado a referencias externas persistentes.

Versión operativa del ejercicio
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Para nuevos contribuidores o nuevas iniciativas
(WPs) que necesiten extender el modelo:

1. **Identificar la entidad nueva** y su cluster (§ 11
   de :doc:`agregacion-interfaces`).
2. **Documentarla** en este archivo
   (``analisis-dominio.rst``) — sustantivos en § 3,
   verbos en § 4, atributos en § 5.
3. **Decidir el tipo de relación** con las entidades
   existentes aplicando la receta progresiva de tres
   preguntas (§ 15.11).
4. **Agregar descripción** con verbo del **ubiquitous
   language**; evitar ``has`` genérico.
5. **Anclar la multiplicidad** a un BR o CNST cuando
   exista; documentar la elección si es discrecional.
6. **Si crece**, refactorizar el diagrama en clusters
   con ``package`` o ``together``.
7. **Si la entidad merece referencias múltiples**,
   incluirlas en el texto adyacente con ``:doc:`` /
   ``:ref:``, no como ``url`` PlantUML.

Cierre del capítulo de enriquecimiento
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Con § 15 (DDD básico) + § 16 (enriquecimiento), el
modelo IACT cubre **todas las dimensiones** del
modelado de dominio que la literatura propone:
entidades + relaciones + multiplicidad + descripciones
+ subtipos + layout + enlaces, todo en PlantUML
sostenible y trazable a UCs / BR / CNST / ADRs.

El siguiente paso operativo no es agregar más
enriquecimientos al modelo: es **mantenerlo vivo**
conforme el proyecto evoluciona (§ 15.5).

----

17. Trazabilidad
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
