.. meta::
 :artefacto: METODOLOGIA_DIAG_SECUENCIAS_IACT
 :tipo: Guia
 :dominio: requisitos
 :subdominio: _metodologia-aplicacion
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-04-30
 :ultimo_cambio: 2026-04-30
 :autor: NestorMonroy
 :clasificacion: Interno

==================================================================
Diagramas de secuencias — interacciones temporales aplicadas a IACT
==================================================================

.. note::

 Adapta la **Hora 9 de Schmuller** ("Diagramas de
 secuencias") al dominio real del proyecto IACT (call
 center IVR + analytics + RBAC + ETL).

 Diagramas en **PlantUML** (política del proyecto, no Mermaid).

 Para la teoría genérica ver
 :doc:`/base-cognitiva/_uml/uml-09-diagramas-secuencias`.

----

Preludio — visualizar flujos de aplicación y usuario
====================================================

Una vez **modelado el dominio** (ver :doc:`analisis-dominio`),
el siguiente artefacto natural es **visualizar los flujos**
entre los sistemas y entre el usuario y la aplicación.

El diagrama de secuencias es la herramienta canónica para
este caso de uso: muestra **interacciones de alto nivel**
antes de bajar al detalle de implementación.

Por qué visualizar flujos antes de implementar
----------------------------------------------

- **Discusión con colegas no técnicos**: los flujos son
  el puente más cercano que tiene un ingeniero con un
  PM, un auditor, un supervisor. Confirman si lo que se
  va a construir cumple los criterios del proyecto.
- **Aprobaciones arquitectónicas**: cuando un nuevo
  sistema o un cambio mayor necesita autorización de
  un arquitecto o comité, presentar **diagramas de
  secuencia** suele ser más efectivo que muros de
  texto. La experiencia recurrente de quienes han
  presentado propuestas: el documento puede acompañar
  con secuencias claras, y la mayor parte de la
  presentación se vuelve "leer el diagrama" — la
  aprobación llega más rápido.
- **Comunicación entre ingenieros**: cuando un
  desarrollador junior se incorpora, una secuencia
  responde "¿cómo funciona X?" en segundos.
- **Detección temprana de inconsistencias**: dibujar
  el flujo expone supuestos no validados (orden de
  llamadas, mensajes faltantes, dependencias no
  declaradas).

Cuándo usar secuencias en el ciclo de vida del WP
-------------------------------------------------

En el flujo THYROX del proyecto:

- **Phase 1 DISCOVER**: bocetos rápidos para entender
  el flujo del problema reportado.
- **Phase 5 STRATEGY**: comparar alternativas
  presentándolas como dos secuencias paralelas.
- **Phase 7 DESIGN/SPECIFY**: secuencias formales
  como parte del entregable.
- **Phase 9 PILOT**: validar la secuencia diseñada
  antes de construir.
- **Phase 10 EXECUTE**: la secuencia es referencia
  para implementar y revisar PRs.

Equivalente IACT del ejemplo Streamy del libro
----------------------------------------------

El libro citado modela el flujo de **registro
(``sign-up``)** de un usuario en Streamy. En IACT no
hay registro público — los usuarios provienen del
**LDAP corporativo** y el flujo equivalente más
cercano es **UC_AUTH_01: Login del supervisor**.
Ese flujo ya está modelado en § 1 de este documento
y en § 2 de :doc:`diagramas-actividades`.

Otros flujos IACT canónicos para diagramar como
secuencia:

- **UC_RPT_01** — supervisor consulta dashboard (vs
  SLA CNST_017).
- **UC_RPT_04** — exportar reporte async (CNST_019).
- **UC_PIP_01** — carga ETL (ventana CNST_006/008).
- **UC_ALR_03** — reconocer alerta crítica con
  sincronización audit + notify.
- **UC_PERM_07** — verificar permiso con SoD
  (CNST_030).

Política general
----------------

**Casi cualquier presentación se beneficia de un
diagrama**. Antes de redactar un documento extenso o
defenderlo en reunión, evaluar si una secuencia
explicaría más rápido lo que se quiere comunicar — la
respuesta es "sí" más a menudo de lo que parece.

Las secciones siguientes detallan la sintaxis y los
ejemplos IACT.

----

1. Comunicación entre objetos en el tiempo
==========================================

  El diagrama de secuencias muestra cómo los objetos se
  comunican entre sí al transcurrir el tiempo.

::

 Diagrama de ESTADOS:    cómo CAMBIA UN OBJETO
 Diagrama de SECUENCIAS: cómo SE COMUNICAN VARIOS OBJETOS

**Pregunta clave:** ¿qué mensajes se intercambian los objetos
y en qué orden?

----

2. Componentes básicos
======================

2.1 Elementos del diagrama
--------------------------

Cinco elementos canónicos: **participantes** (rectángulos
arriba), **línea de vida** (punteada vertical), **activación**
(rectángulo en línea de vida), **mensaje** (flecha horizontal
etiquetada), **tiempo** (eje vertical, arriba → abajo).

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   participant Objeto1
   participant Objeto2
   participant Objeto3

   Objeto1 -> Objeto2 : mensaje 1
   activate Objeto2
   Objeto2 -> Objeto3 : mensaje 2
   activate Objeto3
   Objeto3 --> Objeto2 : retorno
   deactivate Objeto3
   Objeto2 --> Objeto1 : retorno
   deactivate Objeto2
   @enduml

2.1.bis Definir actores y participantes
---------------------------------------

Todo diagrama de secuencia debe tener **actores** y
**participantes**:

- **Actor** — representa un **humano** que interactúa
  con el sistema (supervisor, auditor, agente).
- **Participante** — representa un **proceso** o
  componente del sistema (servicio, base de datos,
  cola de mensajes, integración externa).

Sintaxis PlantUML
~~~~~~~~~~~~~~~~~

PlantUML diferencia los dos tipos con palabras clave
explícitas:

.. code-block:: plantuml

   @startuml
   !include ../../_static/plantuml-styles.puml
   title User Sign Up Flow

   actor Browser
   participant "Sign Up Service" as SUS
   participant "User Service" as US
   queue Kafka
   @enduml

Lectura del fragmento:

- ``actor Browser`` — figura humanoide (stick figure).
- ``participant "Sign Up Service" as SUS`` — caja
  rectangular con alias corto ``SUS`` para mensajes.
- ``queue Kafka`` — PlantUML ofrece tipos
  especializados (``database``, ``queue``, ``boundary``,
  ``control``, ``entity``, ``collections``) que cambian
  el icono.

Esto es **más rico** que Mermaid, donde solo existen
``actor`` y ``participant``. Para IACT esa expresividad
ayuda a comunicar la naturaleza del componente sin
explicarlo en una nota.

Equivalente IACT del flujo del libro
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El libro modela un flujo de registro genérico con
``Browser`` → ``Sign Up Service`` → ``User Service`` →
``Kafka``. En IACT no hay registro público (los
usuarios provienen del LDAP corporativo, ver § 16.7 de
:doc:`analisis-dominio`). El flujo análogo más cercano
es **UC_AUTH_01** (login del supervisor):

.. code-block:: plantuml

   @startuml
   !include ../../_static/plantuml-styles.puml
   title UC_AUTH_01 — Login del supervisor

   actor Supervisor
   participant "Browser" as B
   participant "auth_app" as Auth
   participant "perm_app" as Perm
   database "ldap-corporativo" as LDAP
   database "Redis (sesiones)" as Redis
   database "audit_log" as Audit
   @enduml

Esto declara los **lifelines** sin mensajes — solo el
elenco. El renderizado muestra los participantes
alineados horizontalmente con sus líneas de vida
descendiendo, listas para recibir mensajes en las
secciones siguientes.

Tipos de participante en IACT
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
 :widths: 22 30 48
 :header-rows: 1

 * - PlantUML keyword
   - Cuándo usarlo
   - Ejemplo IACT
 * - ``actor``
   - Persona física que opera la UI.
   - ``Supervisor``, ``Auditor``,
     ``OperadorETL``, ``AdministradorRBAC``.
 * - ``participant``
   - App Django, servicio, vista.
   - ``auth_app``, ``perm_app``, ``rpt_app``,
     ``alr_app``.
 * - ``database``
   - Base de datos o almacén persistente.
   - ``bd_operativa``, ``bd_analytics``,
     ``audit_log``, ``Redis``.
 * - ``queue``
   - Cola de mensajes (raro en IACT por
     ADR_DEVOPS_001).
   - Solo si se introduce alguna cola futura;
     requiere ADR.
 * - ``entity``
   - Entidad del dominio (modelo Django).
   - ``Reporte``, ``Sesion``, ``Alerta`` cuando
     son objetos del dominio que reciben mensajes.
 * - ``boundary``
   - Frontera del sistema, integración externa.
   - ``ldap-corporativo``, ``ivr-host``.
 * - ``control``
   - Componente coordinador / orquestador.
   - ``ExportarReporteFacade`` (ver § 6 de
     :doc:`patrones-diseno`).

Aliases para legibilidad
~~~~~~~~~~~~~~~~~~~~~~~~

PlantUML soporta alias con la sintaxis ``as``, igual
que Mermaid:

.. code-block:: plantuml

   participant "ExportarReporteFacade" as Facade

En el resto del diagrama se puede usar ``Facade`` para
mensajes; el render mostrará el nombre completo.

¿Es obligatoria la declaración explícita?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

No. PlantUML acepta usar el nombre del participante
directamente en un mensaje sin declararlo antes — lo
crea como ``participant`` por defecto. Pero hay tres
razones para declararlo explícitamente:

1. **Forzar el icono correcto** — para tener un actor
   con figura humanoide hay que declararlo como
   ``actor``.
2. **Controlar el orden** de izquierda a derecha — el
   orden de declaración determina el orden visual.
3. **Definir aliases** que se reutilizan en todos los
   mensajes.

Política IACT
~~~~~~~~~~~~~

1. **Siempre declarar explícitamente** los lifelines en
   las primeras líneas del diagrama. Fija orden e
   iconos sin ambigüedad.
2. **Usar el tipo más específico** disponible: prefiere
   ``database`` para BD, ``actor`` para humanos,
   ``boundary`` para integraciones externas.
3. **Aliases para nombres largos** — ``auth_app`` se
   queda corto pero ``ExportarReporteFacade`` se
   abrevia con ``as Facade`` para que los mensajes
   queden legibles.
4. **No abusar de tipos exóticos** — si el equipo no
   conoce ``boundary`` / ``control``, usar
   ``participant`` con una nota explicativa.
5. **Coherencia con el modelo de dominio** — los
   participantes deben coincidir con entidades de
   :doc:`analisis-dominio` o componentes de
   :doc:`diagramas-componentes`.

2.1.ter Agregar la primera interacción
--------------------------------------

Una vez declarados actores y participantes (§ 2.1.bis),
el siguiente paso es agregar **la primera interacción**
del flujo. Las interacciones se modelan como **mensajes**
entre lifelines.

Sintaxis PlantUML para mensajes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PlantUML diferencia entre síncronos y asíncronos /
respuestas con tres flechas básicas:

.. list-table::
 :widths: 22 28 50
 :header-rows: 1

 * - Sintaxis
   - Tipo
   - Cuándo usarla
 * - ``->``
   - Síncrono (request).
   - Llamada que espera respuesta.
 * - ``-->``
   - Respuesta o asíncrono.
   - Línea punteada para retorno o callback.
 * - ``->>``
   - Asíncrono explícito (sin retorno
     inmediato).
   - Eventos, fire-and-forget, mensajes en cola.

Equivalencia con Mermaid del libro:

.. list-table::
 :widths: 30 30 40
 :header-rows: 1

 * - Mermaid (libro)
   - PlantUML (IACT)
   - Significado
 * - ``->>``
   - ``->``
   - Llamada síncrona request.
 * - ``-->>``
   - ``-->``
   - Respuesta (línea punteada).

Estructura de un mensaje
~~~~~~~~~~~~~~~~~~~~~~~~

::

   <emisor> <flecha> <receptor> : <descripción breve>

- **Emisor** a la izquierda; **receptor** a la derecha.
- **Descripción breve** después de los dos puntos.
- El **tiempo avanza hacia abajo** — el orden de las
  líneas en el código es el orden cronológico.

Equivalente IACT del primer mensaje del libro
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El libro abre con ``Browser`` → ``Sign Up Service``
pidiendo la página de registro y la respuesta 200 OK
con el HTML. En IACT, el flujo análogo de primera
interacción para UC_AUTH_01 es la solicitud de la
página de login:

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   title UC_AUTH_01 — primer intercambio

   actor Supervisor
   participant "Browser" as B
   participant "auth_app" as Auth

   Supervisor -> B : abre URL del panel
   B -> Auth : GET /login
   Auth --> B : 200 OK (formulario login)
   B --> Supervisor : muestra formulario
   @enduml

Lectura:

- **Mensaje síncrono** (``->``) — el navegador hace
  ``GET /login`` y espera respuesta.
- **Respuesta** (``-->``) — ``auth_app`` retorna el
  HTML; línea punteada para distinguir del request.
- **Mensaje del actor al sistema** y **del sistema al
  actor** — capturados con sintaxis idéntica.

El render muestra mensajes con flechas distintas
(continua para síncronos, punteada para respuestas) que
permiten al lector distinguir requests de responses sin
leer las etiquetas.

Etiquetas — alto nivel siempre
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El libro lo enfatiza: los diagramas de secuencia son
**vistas de alto nivel** del proceso. Las etiquetas
deben mantenerse al mismo nivel.

Buenas etiquetas IACT:

- ``GET /reportes/04/exportar`` — claro, identifica el
  endpoint.
- ``verificar_permiso(user, "exportar")`` — operación
  del dominio.
- ``encolar tarea async`` — descripción funcional.
- ``200 OK (JSON)`` o ``403 Forbidden`` — respuesta
  con código.

Etiquetas que **deberían evitarse**:

- ``serializer = ReporteSerializer(context={...}); ...
  return Response(serializer.data, ...)`` — código
  detallado, pertenece a la implementación, no al
  diagrama.
- ``hacer cosas con la BD`` — vago, no comunica nada.
- ``proceso interno`` — opaco; mejor descomponer en
  varios mensajes específicos.

Reglas IACT para mensajes
~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Síncrono** (``->``) por defecto; **respuesta**
   (``-->``) siempre que el receptor responde.
2. **Asíncrono explícito** (``->>``) solo cuando hay
   un evento sin respuesta inmediata (e.g.
   ``log_app.notificar`` puesta en cola).
3. **Etiqueta breve** y de alto nivel — máximo una
   línea, idealmente verbo + objeto.
4. **Mensajes a un actor** (``Auth -> Supervisor : ...``)
   son legítimos cuando el sistema **muestra** o
   **notifica** algo al humano.
5. **No esconder mensajes implícitos** críticos —
   especialmente la auditoría: si una operación
   dispara un evento de ``aud_app``, ese mensaje
   **debe** aparecer (CNST_025).
6. **Orden cronológico estricto** — leer de arriba
   hacia abajo debe contar la historia del flujo
   completo.

Ejemplo IACT — primer intercambio UC_RPT_01
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Aplicado al UC_RPT_01 (consultar dashboard) con SLA
CNST_017:

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   title UC_RPT_01 — primer intercambio dashboard

   actor Supervisor
   participant "Browser" as B
   participant "rpt_app" as Rpt

   Supervisor -> B : selecciona dashboard
   B -> Rpt : GET /dashboard?segmento=N
   Rpt --> B : 200 OK (HTML + datos)
   B --> Supervisor : renderiza dashboard
   note right of Rpt
     SLA CNST_017: respuesta <= 10s
   end note
   @enduml

La nota referencia explícitamente la restricción
temporal sin saturar la etiqueta del mensaje. Este
patrón (mensaje + nota explicativa) se repite a lo
largo de la documentación IACT.

2.1.quater Mostrar lógica de bifurcación
----------------------------------------

La mayoría de los flujos tiene al menos un **happy
path** (todo sale bien) y uno o más **unhappy paths**
(algo falla). Modelar al menos un unhappy path crítico
en la misma secuencia ayuda a identificar dónde
concentrar el manejo de errores.

Sin embargo: **no detallar todo lo que puede salir
mal** en una sola secuencia — se vuelve ilegible. Si
hay varios unhappy paths importantes, hacer **diagramas
separados** para cada uno.

Sintaxis PlantUML — alt / else / end
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PlantUML usa **exactamente la misma sintaxis** que
Mermaid para alternativas:

.. code-block:: plantuml

   alt invalid input
       Sign_Up_Service --> Browser : Error
   else valid input
       Sign_Up_Service -> User_Service : POST /users
       User_Service --> Sign_Up_Service : 201 Created
       Sign_Up_Service --> Browser : 301 Redirect
   end

Lectura: ``alt`` abre la primera rama con su guarda
``[invalid input]``; ``else`` abre la rama alternativa;
``end`` cierra el bloque. Se admiten múltiples ``else``
para más de dos ramas, pero conviene mantenerlo bajo.

Equivalente IACT del flujo del libro
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El libro modela ``Sign Up Service`` validando input,
con rama ``invalid → Error`` y rama ``valid → POST
/users → 201 Created → 301 Redirect``. En IACT el
flujo análogo es **UC_AUTH_01 Login** con validación
de credenciales:

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   title UC_AUTH_01 — Login con bifurcacion happy/unhappy

   actor Supervisor
   participant "Browser" as B
   participant "auth_app" as Auth
   database "ldap-corporativo" as LDAP
   database "Redis" as Redis
   database "audit_log" as Audit

   Supervisor -> B : envia credenciales
   B -> Auth : POST /login (user, pass)
   Auth -> Auth : validar formato

   alt [credenciales invalidas]
     Auth -> Audit : registrar intento fallido (CNST_011)
     Auth --> B : 401 Unauthorized
     B --> Supervisor : muestra error
   else [credenciales validas]
     Auth -> LDAP : authenticate(user, pass)
     LDAP --> Auth : OK + atributos
     Auth -> Redis : crear sesion (CNST_002)
     Auth -> Audit : registrar acceso exitoso
     Auth --> B : 302 Redirect (panel)
     B --> Supervisor : muestra panel
   end
   @enduml

Análisis del diagrama
~~~~~~~~~~~~~~~~~~~~~

- **Happy path** = `[credenciales válidas]`: validación
  → autenticación LDAP → creación de sesión en Redis
  (CNST_002) → registro en ``audit_log`` (CNST_025) →
  redirect al panel.
- **Unhappy path** = `[credenciales inválidas]`:
  registro del intento fallido (CNST_011 throttling) +
  401 al navegador.
- **Audit en ambas ramas**: cada rama dispara un
  registro en ``aud_app``. Ningún flujo IACT debe
  tener un alt sin auditoría asociada.

Múltiples alternativas
~~~~~~~~~~~~~~~~~~~~~~

PlantUML soporta varios ``else`` para flujos con más
de dos ramas:

.. code-block:: plantuml

   alt [caso 1]
     A -> B : caso 1
   else [caso 2]
     A -> C : caso 2
   else [caso 3]
     A -> D : caso 3
   end

En IACT esto puede aparecer en UC_RPT_04 export con
tres caminos: cuota agotada, throttling, OK.

Reglas IACT para bifurcaciones
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Modelar al menos un unhappy path crítico** en la
   secuencia principal — refuerza la disciplina de
   manejo de errores.
2. **Si hay más de dos unhappy paths importantes**,
   crear **diagramas separados** uno por escenario,
   no anidar.
3. **Cada rama debe registrar audit** cuando aplique
   (CNST_025) — no esconder eventos auditables en el
   "if no falla".
4. **Etiquetar las guardas** entre corchetes
   (``[credenciales válidas]``) o con el texto entre
   ``alt``/``else`` directamente. Sin guarda, el
   diagrama miente sobre qué rama se ejecuta.
5. **Mantener máximo 3-4 ramas** — más de eso es
   señal de descomponer en flujos separados.

Política de espaciado
~~~~~~~~~~~~~~~~~~~~~

Como recomienda el autor citado, separar visualmente
**bloques de mensajes distintos** con líneas en blanco
en el código fuente PlantUML. No afecta el render pero
facilita el mantenimiento. Aplicar al alt: dejar línea
en blanco antes de ``alt`` y después de ``end``.

----

2.1.quinquies Mostrar mensajes asíncronos
-----------------------------------------

Hasta aquí los mensajes han sido **síncronos** (request
con respuesta esperada). En arquitecturas modernas es
común el **mensaje asíncrono** *fire-and-forget*: el
emisor publica un evento y continúa sin esperar
respuesta.

Sintaxis PlantUML
~~~~~~~~~~~~~~~~~

PlantUML usa ``->>`` para mensajes asíncronos
(equivalente a ``--)`` en Mermaid del libro citado).

.. list-table::
 :widths: 30 30 40
 :header-rows: 1

 * - Mermaid (libro)
   - PlantUML (IACT)
   - Render
 * - ``->>``
   - ``->``
   - Línea continua, flecha rellena (sync request).
 * - ``-->>``
   - ``-->``
   - Línea punteada, flecha rellena (sync response).
 * - ``--)``
   - ``->>``
   - Línea punteada, flecha abierta (async).

Importante: la flecha ``->>`` significa **distinto** en
Mermaid (sync) y en PlantUML (async). La política IACT
usa la convención PlantUML.

Cuándo usar mensajes asíncronos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Eventos del dominio que no requieren respuesta
  inmediata.
- Notificaciones a buzón interno (CNST_001).
- Encolado de tareas async (CNST_019 export).
- Triggers de auditoría — el caller no espera el
  ack del registro (CNST_025).
- Publicación de alertas — el evaluador no espera
  acuse del supervisor.

Stack IACT y mensajes asíncronos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Por **ADR_DEVOPS_001**, el stack canónico no incluye
Kafka. Los mecanismos asíncronos disponibles en IACT
son más simples:

- **Apache + mod_wsgi worker pool** — concurrencia de
  requests.
- **Tareas async vía cron** o **Django management
  commands** — para batches.
- **Buzón interno** (``log_app``) — publicación a un
  destinatario.
- **Bus de eventos in-process** (Observer pattern,
  ver § 8 de :doc:`patrones-diseno`) — propagación de
  eventos auditables sin red.

Cualquier uso futuro de un broker externo (Kafka,
RabbitMQ, Redis Streams) requiere un ADR explícito —
no es la posición por defecto del proyecto.

Equivalente IACT del ejemplo del libro
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El libro publica un evento ``User Created`` en Kafka
desde ``User Service``. En IACT el evento equivalente
es un **registro de auditoría** disparado desde
``aud_app`` cuando una sesión se crea, sin que el
flujo principal espere acuse:

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   title UC_AUTH_01 — registro auditable async (CNST_025)

   actor Supervisor
   participant "Browser" as B
   participant "auth_app" as Auth
   participant "log_app" as Log
   database "Redis" as Redis
   database "audit_log" as Audit

   Supervisor -> B : envia credenciales
   B -> Auth : POST /login
   Auth -> Redis : crear sesion (CNST_002)
   Auth ->> Audit : registrar evento (async)
   Auth ->> Log : notificar buzon supervisor (async, CNST_001)
   Auth --> B : 302 Redirect (panel)
   B --> Supervisor : muestra panel
   @enduml

Análisis:

- ``Auth ->> Audit`` — flecha asíncrona; el flujo
  principal no espera la confirmación de
  ``audit_log``. La invariante CNST_025 (audit
  inmutable) se preserva por construcción del bus de
  eventos: si la persistencia falla, se reintenta sin
  detener el login.
- ``Auth ->> Log`` — la notificación al buzón interno
  no bloquea la respuesta al supervisor.
- ``Auth --> B`` — síncrono (línea punteada con flecha
  rellena) porque el navegador sí espera la
  redirección.

Cambiar el orden de los participantes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Como menciona el autor citado, el orden de declaración
de los participantes determina el orden visual de
izquierda a derecha. Esa es la **tercera razón**
(complementando § 2.1.bis) para declararlos
explícitamente al inicio.

En IACT esto se aprovecha para dar protagonismo al
componente más relevante del flujo. Para UC_AUTH_01
ponemos ``auth_app`` cerca del actor; para UC_RPT_04
ponemos ``rpt_app`` central; para UC_PIP_01 ponemos
``etl_runner`` al frente. La regla informal:
**componentes más relevantes a la izquierda**, después
del actor.

Reglas IACT para mensajes asíncronos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Asíncrono solo cuando realmente lo es** — si el
   caller usa el resultado, es síncrono.
2. **Audit típicamente async** — el bus
   ``aud_app`` no debe bloquear el flujo del UC.
3. **Notificaciones al buzón interno (CNST_001) async**
   — el supervisor revisa cuando puede.
4. **Sin Kafka / RabbitMQ por defecto** — cualquier
   broker externo requiere ADR.
5. **Etiquetar cada mensaje async** con su naturaleza:
   "registrar evento (async)", "notificar buzón
   (async)" — quien lee el diagrama no debe inferir
   solo de la flecha.

----

2.1.sexies Mostrar duración con activaciones
--------------------------------------------

Las **activaciones** son rectángulos angostos sobre la
línea de vida que indican **desde cuándo** un
participante está procesando un mensaje hasta **cuándo**
devuelve la respuesta. No representan tiempo absoluto,
pero comunican visualmente:

- Dónde **empieza y termina** cada interacción.
- Qué participante tiene la **complejidad mayor**
  (activaciones más largas).
- Cuándo un mensaje **anida** dentro de otro
  (activaciones encajadas).

Sintaxis PlantUML
~~~~~~~~~~~~~~~~~

PlantUML soporta dos formas, igual que Mermaid:

**Forma explícita** — ``activate`` / ``deactivate``:

.. code-block:: plantuml

   Browser -> Auth : GET /login
   activate Auth
   Auth --> Browser : 200 OK
   deactivate Auth

**Forma inline** — sufijo ``++`` para activar y
``--`` para desactivar:

.. code-block:: plantuml

   Browser -> Auth ++ : GET /login
   Auth --> Browser -- : 200 OK

Equivalencia con Mermaid del libro:

.. list-table::
 :widths: 32 32 36
 :header-rows: 1

 * - Mermaid (libro)
   - PlantUML (IACT)
   - Significado
 * - ``activate X`` / ``deactivate X``
   - ``activate X`` / ``deactivate X``
   - Forma explícita en líneas separadas.
 * - ``->>+`` / ``-->>-``
   - ``->>++`` / ``-->>--`` o
     ``-> X ++`` / ``-->`` con ``--``
   - Forma inline (sufijo en la flecha).

PlantUML acepta ambas; el render genera rectángulos
sobre la línea de vida del participante activo.

Cuándo usar cada forma
~~~~~~~~~~~~~~~~~~~~~~

- **Explícita** (``activate``/``deactivate`` en líneas
  propias): más legible cuando hay activaciones
  encajadas o cuando el flujo es complejo. El
  ``activate`` aparece como una línea distinta y es
  más fácil de localizar al editar.
- **Inline** (``++`` / ``--``): más conciso, mejor
  para flujos simples o cuando se quiere reducir el
  ruido del código fuente.

Equivalente IACT del flujo del libro
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El libro muestra activaciones encajadas en el flujo
sign-up con tres niveles: ``Sign Up Service`` activo
durante el POST, dentro del cual ``User Service`` se
activa para el ``POST /users``. Aplicado a UC_AUTH_01
con activaciones encajadas:

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   title UC_AUTH_01 — activaciones encajadas

   actor Supervisor
   participant "Browser" as B
   participant "auth_app" as Auth
   database "ldap-corporativo" as LDAP
   database "Redis" as Redis
   database "audit_log" as Audit

   Supervisor -> B : envia credenciales
   B -> Auth ++ : POST /login

   Auth -> Auth : validar formato

   alt [credenciales invalidas]
     Auth ->> Audit : registrar intento (CNST_011)
     Auth --> B -- : 401 Unauthorized
   else [credenciales validas]
     Auth -> LDAP ++ : authenticate(user, pass)
     LDAP --> Auth -- : OK + atributos
     Auth -> Redis : crear sesion (CNST_002)
     Auth ->> Audit : registrar acceso
     Auth --> B -- : 302 Redirect (panel)
   end
   B --> Supervisor : muestra panel
   @enduml

Lectura del diagrama
~~~~~~~~~~~~~~~~~~~~

- ``B -> Auth ++`` — activa ``auth_app`` desde el
  POST hasta su respuesta.
- ``Auth -> LDAP ++`` — activa ``LDAP`` solo durante
  ``authenticate``.
- ``LDAP --> Auth --`` — desactiva ``LDAP`` al
  retornar.
- ``Auth --> B --`` — desactiva ``auth_app`` al
  responder al navegador (cierra la activación
  exterior).
- Mensajes asíncronos (``->> Audit``) **no activan**
  al destinatario en este modelo simple — el bus de
  audit es fire-and-forget.

A simple vista, el rectángulo de ``auth_app`` cubre
todo el procesamiento del login, y el rectángulo
interno de ``LDAP`` muestra que la autenticación es la
operación de mayor latencia dentro del flujo. Eso es
lo que las activaciones comunican.

Política IACT — cuándo usar activaciones
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Diagramas pedagógicos cortos**: opcional. Si el
   flujo tiene 3-5 mensajes lineales, las activaciones
   añaden más ruido que valor.
2. **Diagramas con bifurcación o anidamiento**:
   recomendado. Las activaciones hacen visible el
   **scope** de cada llamada y dónde anida una dentro
   de otra.
3. **Diagramas para revisión arquitectónica o
   aprobación**: obligatorio. Comunican la
   complejidad relativa y el alcance temporal.
4. **Mezcla síncrono / asíncrono**: las activaciones
   refuerzan la diferencia visual — un async no
   genera rectángulo del receptor.
5. **Forma elegida**: si todas las activaciones del
   diagrama son encajadas, preferir la **inline**
   (más conciso). Si solo unas pocas activaciones son
   relevantes, la **explícita** facilita destacar
   esas ubicaciones.

Reglas IACT adicionales
~~~~~~~~~~~~~~~~~~~~~~~

- Toda **bifurcación crítica** debe cerrar todas sus
  activaciones — un ``alt`` con ``activate`` sin su
  ``deactivate`` correspondiente produce diagramas
  defectuosos.
- En flujos con **SLA** (CNST_017) el rectángulo de
  activación visualiza dónde puede estar el cuello de
  botella; complementar con una nota que cite el SLA.
- Para flujos con **export async** (CNST_019), no
  activar al worker de export más allá del momento
  del encolado — el procesamiento posterior pertenece
  a un diagrama de secuencia separado.

----

2.1.septies Agregar contexto con notas
--------------------------------------

Las **etiquetas** de los mensajes deben mantenerse
breves (§ 2.1.ter). Cuando se necesita **contexto
adicional** —un detalle que el lector debe ver pero
que satura la etiqueta— el mecanismo correcto es la
**nota**.

Sintaxis PlantUML
~~~~~~~~~~~~~~~~~

PlantUML soporta tres formas de nota:

.. code-block:: plantuml

   note left of Auth : detalle a la izquierda
   note right of Auth : detalle a la derecha
   note over Auth : detalle sobre el participante
   note over Auth, Audit : abarca dos participantes

Equivalencia con Mermaid del libro:

.. list-table::
 :widths: 36 36 28
 :header-rows: 1

 * - Mermaid (libro)
   - PlantUML (IACT)
   - Posición
 * - ``Note left of X``
   - ``note left of X``
   - Pegada al lado izquierdo de X.
 * - ``Note right of X``
   - ``note right of X``
   - Pegada al lado derecho de X.
 * - ``Note over X``
   - ``note over X``
   - Centrada sobre X.
 * - ``Note over X, Y``
   - ``note over X, Y``
   - Atraviesa de X a Y.

PlantUML también admite notas multilínea con
``note ... end note`` y formato:

.. code-block:: plantuml

   note right of Auth
     Detalle de la operación.
     Multiple líneas posibles.
   end note

Cuándo usar notas
~~~~~~~~~~~~~~~~~

- Resaltar una **restricción del proyecto** que aplica
  al mensaje (CNST_*, BR_*).
- Documentar un **detalle de seguridad o autenticación**
  que no cabe en la etiqueta (e.g. paso de token,
  encriptación).
- Indicar que un **evento publicado** será consumido
  por otros servicios o componentes.
- Marcar **deuda técnica**, **TODO crítico** o
  **WORKAROUND** localizados — anclados a un ADR si
  son permanentes.

Equivalente IACT del ejemplo del libro
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El libro agrega ``Note left of Kafka: other services
take action based on this event`` para señalar el
fan-out del evento. En IACT el fan-out equivalente es
el bus interno de auditoría: un evento auditable
disparado desde una app es consumido por
``aud_app`` y, en algunos UCs, también por
``log_app`` para notificar al supervisor.

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   title UC_AUTH_01 — fan-out auditable

   actor Supervisor
   participant "Browser" as B
   participant "auth_app" as Auth
   participant "log_app" as Log
   database "audit_log" as Audit

   Supervisor -> B : envia credenciales
   B -> Auth : POST /login

   Auth ->> Audit : registrar evento (CNST_025)
   note right of Audit
     audit_log es immutable;
     no se reasigna ni borra
   end note

   Auth ->> Log : notificar buzon supervisor
   note over Log : entrega via buzon interno (CNST_001)

   Auth --> B : 302 Redirect (panel)
   B --> Supervisor : muestra panel
   @enduml

Análisis:

- **``note right of Audit``** — recuerda al lector la
  invariante CNST_025 sin saturar la etiqueta del
  mensaje. La nota se queda al lado del destino
  relevante.
- **``note over Log``** — ubica el comentario sobre el
  participante; útil cuando el detalle es **del
  participante**, no del mensaje específico.
- **Notas atravesando dos lifelines** son útiles para
  describir un **acuerdo entre componentes** (ej. un
  contrato de retry, una garantía de orden).

Política IACT — uso de notas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Notas para CNST/BR** que aplican al mensaje pero
   no caben en la etiqueta. Citar la sigla
   (``CNST_025``, ``BR_012``) explícitamente.
2. **Notas para fan-out** cuando un mensaje async
   detona múltiples consumidores; describir
   brevemente quiénes consumen.
3. **Notas para autenticación / seguridad** —
   resaltar que un endpoint requiere un token, una
   firma o un canal específico (LDAPS, mTLS).
4. **Notas para SLA** — referenciar CNST_017 cerca
   del rectángulo de activación que cubre el flujo
   crítico.
5. **No saturar** — un diagrama con más de 3-4 notas
   probablemente está mezclando varios niveles de
   detalle. Considerar separar en varios diagramas o
   mover detalles al texto RST adyacente.

Notas vs documentación adyacente
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Para detalles **largos** (más de dos líneas) preferir
el **texto RST circundante**. Las notas dentro del
diagrama PlantUML deben ser **comentarios cortos** que
se leen junto a la línea relevante. Si la explicación
necesita un párrafo, no es una nota — es texto del
documento.

----

2.1.octies Anotar el diagrama con números de secuencia
------------------------------------------------------

Anotar cada mensaje con un **número** facilita
discutir el diagrama: en lugar de describir un
mensaje, basta con citarlo por su número (*"el paso
3 es donde validamos throttling"*).

Sintaxis PlantUML
~~~~~~~~~~~~~~~~~

PlantUML usa la directiva ``autonumber`` igual que
Mermaid:

.. code-block:: plantuml

   @startuml
   !include ../../_static/plantuml-styles.puml
   autonumber
   B -> Auth : POST /login
   Auth -> LDAP : authenticate
   LDAP --> Auth : OK
   Auth --> B : 302 Redirect
   @enduml

El render agrega ``1``, ``2``, ``3``, ``4`` al inicio
de cada mensaje. PlantUML extiende lo básico:

.. list-table::
 :widths: 32 68
 :header-rows: 1

 * - Forma
   - Efecto
 * - ``autonumber``
   - Numeración 1, 2, 3, …
 * - ``autonumber 10``
   - Empieza en 10.
 * - ``autonumber 10 5``
   - Empieza en 10, incremento 5 (10, 15, 20, …).
 * - ``autonumber "<b>[000]"``
   - Formato con padding y estilo (negrita, ceros).
 * - ``autonumber stop``
   - Detiene la numeración.
 * - ``autonumber resume``
   - Reanuda la numeración previa.

Equivalente IACT del ejemplo del libro
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Aplicado a UC_AUTH_01 con ``autonumber``:

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   title UC_AUTH_01 — login con numeracion automatica

   autonumber

   actor Supervisor
   participant "Browser" as B
   participant "auth_app" as Auth
   database "ldap-corporativo" as LDAP
   database "Redis" as Redis
   database "audit_log" as Audit

   Supervisor -> B : envia credenciales
   B -> Auth : POST /login
   Auth -> Auth : validar formato
   Auth -> LDAP : authenticate(user, pass)
   LDAP --> Auth : OK + atributos
   Auth -> Redis : crear sesion (CNST_002)
   Auth ->> Audit : registrar acceso (CNST_025)
   Auth --> B : 302 Redirect (panel)
   B --> Supervisor : muestra panel
   @enduml

Referirse al diagrama es directo: *"el paso 4 es la
autenticación contra LDAP"*, *"el paso 7 es donde
disparamos audit"*. Esa precisión vale especialmente
en revisiones de PR, en sesiones de design review y
en aprobaciones arquitectónicas.

Política IACT — cuándo numerar
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Diagramas con más de 5 mensajes**: numerar
   ayuda a la discusión.
2. **Diagramas para revisión / aprobación**:
   numerar siempre — facilita las actas y los
   feedback comments.
3. **Diagramas pedagógicos cortos** (3-4
   mensajes): no numerar; las flechas hablan por sí
   solas.
4. **Diagramas con bifurcación**: la numeración
   continúa **a través** de las ramas — los pasos
   3a, 3b, etc. no son nativos. Si el lector
   necesita distinguir ramas, agregar una **nota**
   con la guarda.
5. **No reutilizar números entre diagramas**: cada
   diagrama tiene su propia numeración local. Las
   referencias cruzadas usan el ID del diagrama o
   el UC, no el número de paso.

Combinación con activaciones y notas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

La numeración se combina sin conflicto con las
demás técnicas:

- **Activaciones** (§ 2.1.sexies) — los rectángulos
  de activación coexisten con los números.
- **Notas** (§ 2.1.septies) — las notas pueden
  referenciar números de paso ("ver paso 3").
- **alt / else** (§ 2.1.quater) — los bloques
  alternativos siguen numerando dentro de cada rama.

Para diagramas críticos del proyecto (UC_RPT_04
export, UC_PIP_01 ETL, UC_AUTH_01 login,
UC_ALR_03 reconocimiento), aplicar **todos los
enriquecimientos**: actores y participantes
explícitos + activaciones + alt + notas para
CNST/BR + ``autonumber``. Esa combinación produce
diagramas listos para revisión y onboarding.

----

2.1.nonies Enlaces y menús en participantes
-------------------------------------------

Mermaid soporta **menús desplegables** (drop-down) en
actores y participantes con un formato tipo JSON que
asocia varias claves-valor (por ejemplo, "Repository",
"Domain Model", "ADR"). Al renderizar y pasar el mouse
sobre el participante, aparece el menú con los enlaces.

PlantUML no ofrece menús desplegables nativos, pero sí
permite **enlazar un participante a una URL única** con
``[[url]]``, lo cual cubre el 80% del caso de uso.

Sintaxis PlantUML
~~~~~~~~~~~~~~~~~

Enlace simple en un participante:

.. code-block:: plantuml

   participant "auth_app" as Auth [[https://repo.iact.local/auth_app]]

Con tooltip:

.. code-block:: plantuml

   participant "auth_app" as Auth [[https://repo.iact.local/auth_app{repositorio}]]

Equivalencia funcional con Mermaid del libro
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
 :widths: 36 36 28
 :header-rows: 1

 * - Mermaid (libro)
   - PlantUML (IACT)
   - Diferencia
 * - ``links X: {"Repo": "...", "Doc": "..."}``
   - ``participant X [[url]]``
   - PlantUML solo admite **una URL** por
     participante.
 * - Menú con varios enlaces al hover.
   - Tooltip simple al hover; click abre la URL.
   - Menú multilink solo en Mermaid.

Cuando el participante necesita **varios enlaces**
(repositorio + ADR + documentación), la solución
PlantUML / Sphinx es **mantenerlos en el texto RST
adyacente** al diagrama, donde Sphinx puede gestionar
referencias cruzadas internas (``:doc:``, ``:ref:``).

Política IACT
~~~~~~~~~~~~~

1. **Preferir referencias en el texto RST** al
   diagrama, no inline en PlantUML. Sphinx valida los
   destinos y los renderiza con la apariencia
   estándar del proyecto.
2. **Reservar ``[[url]]`` PlantUML** para casos donde
   tenga sentido convertir un participante en
   clickeable directo a documentación externa
   persistente (RFC, especificación oficial,
   documentación de un servicio externo).
3. **No enlazar a recursos efímeros** —
   issues, branches, borradores. La URL puede morir;
   el diagrama sobrevive.
4. **Si un participante merece varios enlaces**,
   listarlos en el párrafo introductorio del
   diagrama:

   .. code-block:: rst

      El siguiente diagrama modela UC_AUTH_01.

      Componentes referenciados:

      - :doc:`auth_app — modelo de dominio </requisitos/_metodologia-aplicacion/analisis-dominio>`
      - :doc:`Decisión de stack — ADR_DEVOPS_001 </normativa/...>`
      - :doc:`Restricciones aplicables — CNST_002, CNST_011, CNST_025 </requisitos/...>`

Limitaciones del enfoque PlantUML
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **No hay menú multilink** en el render PlantUML de
  Sphinx. Si esa funcionalidad fuera crítica para un
  caso específico, se podría considerar Mermaid solo
  para ese contexto (issue/discussion en GitHub) sin
  alterar la política general — pero esa decisión
  requeriría ADR (ver § "Reconocimiento de la
  limitación" en :doc:`diagramas-uml`).
- Los **menús/links no aparecen en PDF, presentaciones
  exportadas ni capturas de pantalla**. Como bien
  señala el autor citado, esto vale tanto para
  Mermaid como para PlantUML — los enlaces solo
  funcionan en HTML interactivo.

Recomendación práctica
~~~~~~~~~~~~~~~~~~~~~~

Para IACT, la combinación más robusta es:

- **Diagrama PlantUML autocontenido** sin enlaces
  inline.
- **Texto RST adyacente** con la lista de referencias
  cruzadas (UCs, ADRs, BRs, CNSTs, modelos de dominio).
- **El lector** que necesite "saltar al repositorio
  de auth_app" sigue las referencias del párrafo —
  la experiencia es similar al menú desplegable, pero
  más predecible y validable por Sphinx.

----

2.2 Convenciones
----------------

::

 Participante:    rectángulo en la parte superior
 Línea de vida:   línea vertical descendente desde el
                  participante (punteada)
 Activación:      rectángulo angosto sobrepuesto a la
                  línea de vida (representa ejecución)
 Mensaje:         flecha horizontal entre líneas de vida
 Auto-mensaje:    flecha que sale y vuelve al mismo
                  participante
 Tiempo:          progresa de arriba hacia abajo

----

3. Tipos de mensajes
====================

3.1 Mensaje simple (transferencia de control)
---------------------------------------------

::

 Objeto1 → Objeto2
   - Transferencia de control
   - No espera respuesta explícita
   - Flecha abierta

3.2 Mensaje sincrónico (bloqueante)
-----------------------------------

::

 Objeto1 ⇒ Objeto2
   - Espera respuesta antes de continuar
   - Llamada a función bloqueante
   - Flecha rellena
   - El más común en programación

3.3 Mensaje asincrónico (no bloqueante)
---------------------------------------

::

 Objeto1 ⇢ Objeto2
   - NO espera respuesta
   - El emisor continúa inmediatamente
   - Cola de mensajes / event bus
   - Flecha abierta de medio trazo

3.4 Ejemplo IACT — los tres tipos en UC_RPT_01
----------------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   actor Operador
   participant ":Frontend"   as F
   participant ":Backend"    as B
   participant ":SecRules"   as SR
   participant ":BDAnalytics" as BD
   participant ":AuditLog"   as AL

   Operador -> F   : 1. clic "Ver Dashboard"        (simple)
   F -> B          : 2. GET /api/dashboard          (sincrónico)
   activate B
   B -> SR         : 3. verificarPermiso(view_dashboard)\n  (sincrónico)
   activate SR
   SR --> B        : 4. autorizado + segmento
   deactivate SR
   B -> BD         : 5. SELECT con filtro segmento  (sincrónico)
   activate BD
   BD --> B        : 6. filas
   deactivate BD
   B ->> AL        : 7. registrar(VIEW_DASHBOARD)   (asincrónico,\n     CNST_025)
   B --> F         : 8. {datos, métricas, ts}
   deactivate B
   F --> Operador  : 9. dashboard renderizado
   @enduml

----

4. Diagrama de instancia — escenario feliz
==========================================

Una **instancia** es un escenario específico de un UC sin
condiciones alternativas.

4.1 Ejemplo IACT — UC_PIP_01 (Supervisar ETL, escenario OK)
-----------------------------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   actor "Admin\nPipeline" as AP
   participant ":SupervisorETL" as Sup
   participant ":SchedulerETL"  as Sch
   participant ":BDAnalytics"   as BD
   participant ":AuditLog"      as AL

   AP -> Sup  : abrirSupervision()
   activate Sup

   Sup -> Sch : ultimoRun()
   activate Sch
   Sch --> Sup : run_id, fecha_inicio, estado
   deactivate Sch

   Sup -> BD  : SELECT errores WHERE run_id=?
   activate BD
   BD --> Sup : []  (sin errores)
   deactivate BD

   Sup -> AL  : registrar(VIEW_ETL_STATUS)
   activate AL
   AL --> Sup : ok
   deactivate AL

   Sup --> AP : panel ETL: estado OK,\nprox_ejecucion=02:00 AM
   deactivate Sup

   note over AP,AL
     Escenario feliz:
     última ejecución exitosa,
     CNST_008 ventana 6-12h
     respetada.
   end note
   @enduml

----

5. Diagrama genérico — múltiples escenarios
===========================================

Un diagrama **genérico** muestra varios escenarios alternos
en uno solo, usando ``alt`` / ``else`` (condiciones) y
``loop`` (ciclos).

5.1 Ejemplo IACT — UC_AUTH_01 (Iniciar sesión, todos los caminos)
-----------------------------------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   actor Usuario
   participant ":Frontend"     as F
   participant ":AuthService"  as A
   participant ":SecRules"     as SR
   participant ":SessionStore" as SS
   participant ":AuditLog"     as AL

   Usuario -> F : 1. submit (email, password)
   F -> A       : 2. POST /api/auth/login
   activate A

   A -> SR : 3. verificarThrottling(IP)\n   (CNST_011: 5 / 5min)

   alt [throttling alcanzado]
     SR --> A : 4a. denegado
     A ->> AL : 5a. registrar(LOGIN_BLOCKED_IP)
     A --> F  : 6a. {error: "IP bloqueada"}
     F --> Usuario : 7a. ✗ "Intentos máximos"
   else [throttling ok]
     SR --> A : 4b. autorizado

     A -> SS  : 5b. validarCredenciales(email, hash)

     alt [credenciales válidas]
       SS --> A : 6b1. user_record (is_active=true)

       alt [sesión existente — CNST_002]
         A -> SS : 7b1. invalidarSesionAnterior()
         SS --> A : 7b2. ok
       end

       A -> SS  : 8b. crearSesion(user_id, segmento)
       SS --> A : 9b. session_id, jwt
       A ->> AL : 10b. registrar(LOGIN_SUCCESS)
       A --> F  : 11b. {jwt, refresh_token, user}
       F --> Usuario : 12b. ✓ Redirect /dashboard
     else [credenciales inválidas]
       SS --> A : 6c. user_not_found
       A -> SS  : 7c. incrementarIntentos(IP)
       A ->> AL : 8c. registrar(LOGIN_FAILED)
       A --> F  : 9c. {error: "Credenciales"}
       F --> Usuario : 10c. ✗ Mostrar error
     end
   end
   deactivate A
   @enduml

----

6. Activaciones y duración — SLA CNST_017
=========================================

La **altura** de la activación representa la **duración**.
Útil para visualizar SLAs (CNST_017 — latencia ≤ 10 s).

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   participant ":Backend" as B
   participant ":CacheRedis" as C
   participant ":BDAnalytics" as BD

   B -> C : GET reporte:dash:user_42
   activate C
   note left of C
     Cache lookup
     ~5 ms
   end note
   C --> B : MISS
   deactivate C

   B -> BD : SELECT métricas WHERE segmento=?
   activate BD
   note right of BD
     Query con filtro
     CNST_008 ~ 800 ms
   end note
   BD --> B : filas
   deactivate BD

   B -> C : SET reporte:dash:user_42 TTL=300
   activate C
   C --> B : ok
   deactivate C

   note over B
     Total ≈ 850 ms
     ≤ CNST_017 (10 s) ✓
   end note
   @enduml

----

7. Creación de objetos
======================

Los objetos pueden ser **creados durante la secuencia**.
Notación: mensaje ``<<create>>``. La posición en el eje
vertical indica el momento de creación.

7.1 Ejemplo IACT — Sesion creada en login
-----------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   actor Usuario
   participant ":AuthService" as A
   participant ":SessionStore" as SS

   Usuario -> A : login(email, password)
   activate A
   A -> A : validarCredenciales()

   create participant ":Sesion" as S
   A -> S : <<create>> nueva(user_id, segmento)
   activate S
   S -> S : generarTokenJWT()
   S -> S : generarTokenRefresh()
   S --> A : token + session_id

   A -> SS : guardar(session)
   activate SS
   SS --> A : ok
   deactivate SS

   A --> Usuario : {jwt, refresh}
   deactivate A

   note right of S
     Objeto Sesion creado
     en este punto del tiempo.
     Vive hasta logout o
     timeout 15 min (CNST_002).
   end note
   @enduml

----

8. Destrucción de objetos
=========================

Los objetos pueden ser **destruidos** durante la secuencia.
Notación: ``destroy`` o una **X** al final de la línea de
vida.

8.1 Ejemplo IACT — Sesion destruida en logout
---------------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   actor Usuario
   participant ":Frontend"     as F
   participant ":AuthService"  as A
   participant ":Sesion"       as S
   participant ":AuditLog"     as AL

   Usuario -> F : clic "Cerrar sesión"
   F -> A       : POST /api/auth/logout
   activate A

   A -> S : invalidar()
   activate S
   S -> S : marcarRevocada()
   S --> A : ok
   deactivate S

   A ->> AL : registrar(LOGOUT)

   destroy S
   note over S
     Objeto Sesion destruido —
     tokens marcados revocados,
     entrada eliminada del
     SessionStore.
   end note

   A --> F : {ok}
   deactivate A
   F --> Usuario : redirigir a /login
   @enduml

----

9. Recursividad
===============

Un objeto puede **enviarse un mensaje a sí mismo**. Útil
cuando una operación se invoca recursivamente.

9.1 Ejemplo IACT — verificación de permiso heredado
---------------------------------------------------

UC_PERM_07: una macro-función puede implicar otras (catálogo
con relaciones reflexivas, ver
:doc:`relaciones-uml` § 5.2). El verificador recursivo debe
expandir cada función hasta llegar a las atómicas.

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   participant ":SecRules"  as SR
   participant ":BDAnalytics" as BD

   [-> SR : verificarPermiso(usuario, "manage_users")
   activate SR

   SR -> BD : SELECT funciones_implicadas("manage_users")
   activate BD
   BD --> SR : [view_users, create_users, modify_users, delete_users]
   deactivate BD

   loop para cada función implicada
     SR -> SR : verificarPermiso(usuario, sub_funcion)
     activate SR
     SR --> SR : true | false
     deactivate SR
   end

   SR --> [ : true (todas las atómicas\nestán autorizadas)
   deactivate SR
   @enduml

----

10. Ciclos y condicionales
==========================

10.1 Ciclo ``loop``
-------------------

::

 loop [condición]
   ... mensajes que se repiten ...
 end

10.2 Ejemplo IACT — UC_PIP_04 reintento ETL
-------------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   actor "Admin\nPipeline" as AP
   participant ":SupervisorETL" as Sup
   participant ":SchedulerETL" as Sch
   participant ":BDAnalytics" as BD
   participant ":AuditLog" as AL

   AP -> Sup : solicitarReintento(run_id)
   activate Sup

   loop [intentos < 3 AND estado != EXITOSA]
     Sup -> Sch : enqueueReintento(run_id, intentos)
     activate Sch
     Sch -> BD : ejecutarCarga()
     activate BD

     alt [carga exitosa]
       BD --> Sch : commit_ok
       Sch --> Sup : EXITOSA
       Sup ->> AL : registrar(ETL_RETRY_SUCCESS)
     else [error temporal — timeout IVR]
       BD --> Sch : timeout
       Sch --> Sup : CON_ERRORES (temporal)
       Sup ->> AL : registrar(ETL_RETRY_FAILED_TEMP)
     else [error permanente]
       BD --> Sch : ERROR_PERM
       Sch --> Sup : ERROR_PERMANENTE
       Sup ->> AL : registrar(ETL_RETRY_FAILED_PERM)
     end
     deactivate BD
     deactivate Sch
   end

   alt [estado == EXITOSA]
     Sup --> AP : ✓ ETL recuperado
   else [3 intentos fallidos]
     Sup ->> AL : registrar(ETL_RETRY_GAVE_UP)
     Sup --> AP : ✗ Requiere intervención manual
   end
   deactivate Sup
   @enduml

----

11. Ejemplo completo crítico — UC_RPT_04 (Exportar reporte)
===========================================================

Combina todo: instancia + alternativas + creación de objeto +
loop + asincrónico + auditoría inmutable.

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   actor Supervisor
   participant ":Frontend"      as F
   participant ":Backend"       as B
   participant ":SecRules"      as SR
   participant ":Reporte"       as R
   participant ":BDAnalytics"   as BD
   participant ":ExportQueue"   as EQ
   participant ":BuzonInterno"  as BI
   participant ":AuditLog"      as AL

   == UC_RPT_04: Exportar reporte ==

   Supervisor -> F : clic "Exportar (Excel)"
   F -> B          : POST /api/reports/{id}/export?fmt=xlsx
   activate B

   B -> SR : verificarPermiso(export_excel)\n           + throttling CNST_020
   alt [permiso denegado o throttling]
     SR --> B : denegado
     B ->> AL : registrar(EXPORT_DENIED)
     B --> F  : 403
     F --> Supervisor : ✗ "Sin permiso o límite del día"
     deactivate B
   else [autorizado]
     SR --> B : ok + segmento

     B -> R : aplicarFiltrosSegmento(BR_012, CNST_008)
     activate R
     R -> BD : SELECT con filtro
     activate BD
     BD --> R : filas
     deactivate BD

     alt [filas ≤ 10k → síncrono]
       create participant ":Archivo" as A
       R -> A : <<create>> generarXLSX(filas)
       activate A
       A --> R : archivo
       deactivate A
       R ->> AL : registrar(EXPORT_OK)
       R --> B  : url_descarga
       B --> F  : url
       F --> Supervisor : descarga directa
       deactivate R
     else [filas > 10k → asincrónico CNST_019]
       R -> EQ : encolar(filtros, fmt, supervisor_id)
       activate EQ
       EQ --> R : job_id
       deactivate EQ
       R ->> AL : registrar(EXPORT_QUEUED)
       R --> B  : job_id
       B --> F  : "Procesando, te avisaremos"
       F --> Supervisor : aviso

       deactivate R

       loop [hasta job listo]
         EQ -> EQ : procesar(job)
         activate EQ
       end
       deactivate EQ

       EQ ->> BI : entregar(supervisor_id,\n            "Tu export está listo")
       BI ->> Supervisor : aviso al buzón\n(CNST_001)
     end
   end
   deactivate B
   @enduml

----

12. Relación con casos de uso
=============================

::

 Cada UC contiene UNO O MÁS diagramas de secuencias —
 uno por escenario relevante (principal + alternativas
 críticas).

 Ejemplo: UC_RPT_04 (Exportar reporte)
   ├─ Diagrama secuencia: escenario principal
   │  (≤ 10k filas, descarga directa)
   ├─ Diagrama secuencia: > 10k filas
   │  (export asíncrono via cola)
   ├─ Diagrama secuencia: throttling CNST_020 alcanzado
   └─ Diagrama secuencia: BD analytics no disponible

----

13. En el proyecto IACT — qué UCs requieren secuencias
======================================================

**Obligatorio (secuencias detalladas + alternativas):**

- ``UC_AUTH_01`` — Iniciar sesión (principal + 3
  alternativas: throttling, inválidas, sesión existente).
- ``UC_RPT_04`` — Exportar reporte (principal + async +
  throttling + sin BD).
- ``UC_PIP_04`` — Solicitar reintento ETL (principal +
  loop reintentos + agotamiento).
- ``UC_PERM_07`` — Verificar permiso (principal +
  recursividad para macro-funciones).

**Importante (secuencias medias):**

- ``UC_RPT_01`` — Ver dashboard (principal con CNST_017
  SLA).
- ``UC_ALR_03`` — Reconocer alerta (principal +
  notificación buzón CNST_001).
- ``UC_ACC_01`` — Asignar funciones (principal + SoD
  CNST_030).
- ``UC_AUD_01`` — Consultar auditoría (principal con
  filtros).

**Recomendado (secuencias básicas):**

- ``UC_USR_01`` / ``UC_USR_03`` / ``UC_USR_04`` — CRUD
  usuarios.
- ``UC_LOG_01..07`` — consulta de logs.
- ``UC_PIP_01`` / ``UC_PIP_02`` / ``UC_PIP_03`` —
  supervisión ETL.

  Cada UC incluye su(s) diagrama(s) de secuencia en la
  sección 7 del archivo
  ``casos-uso/<modulo>/uc-<mod>-<NN>-<desc>.rst`` per la
  plantilla
  :doc:`/normativa/estandares/plantillas/tpl-uc-spec-con-diagramas-uml`.

----

14. Trazabilidad
================

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Skills aplicadas**
   - ``rm-specification`` (modelado de la interacción
     entre objetos), ``rm-analysis`` (verificar
     consistencia con UCs)
 * - **Origen del documento**
   - Reescrito de "GUÍA-DIAGRAMAS-SECUENCIAS-INTERACCIONES-
     TEMPORAL" (Hora 9 de Schmuller, cheat-sheet aplicado
     interno con dominio ecommerce), reorientado al
     dominio real IACT.
 * - **Lección teórica**
   - :doc:`/base-cognitiva/_uml/uml-09-diagramas-secuencias`
 * - **Cheat-sheet UML**
   - :doc:`/base-cognitiva/_uml/cuando-usar-cada-diagrama`
 * - **Plantilla canónica de UC**
   - :doc:`/normativa/estandares/plantillas/tpl-uc-spec-con-diagramas-uml`
 * - **Ejemplos hermanos**
   - :doc:`diagramas-uml`,
     :doc:`orientacion-objetos`,
     :doc:`analisis-dominio`,
     :doc:`relaciones-uml`,
     :doc:`agregacion-interfaces`,
     :doc:`casos-uso-especificacion`,
     :doc:`casos-uso-diagramas`,
     :doc:`diagramas-estados`
 * - **Catálogo modular del dominio**
   - :doc:`/gestion/evidencia/arquitectura-modular/analisis-catalogo-modular-iact`
 * - **Restricciones citadas**
   - CNST_001 (no email — sólo buzón interno),
     CNST_002 (sesión única + timeout 15 min),
     CNST_008 (filtro segmento en SQL),
     CNST_011 (throttling 5 / 5 min),
     CNST_017 (SLA ≤ 10 s),
     CNST_019 / 020 (export async + throttling diario),
     CNST_025 (auditoría inmutable),
     CNST_030 (SoD),
     BR_012 (segmento único).
 * - **Política de diagramación**
   - :doc:`/base-cognitiva/plantuml-guide/guidelines`
