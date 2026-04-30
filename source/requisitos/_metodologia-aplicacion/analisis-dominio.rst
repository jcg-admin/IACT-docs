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

15.10 Relación con el resto del documento
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

16. Trazabilidad
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
