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

 Compañero del :doc:`/requisitos/_metodologia-aplicacion/plan-documentacion-uc`.
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

Clasificación de los diagramas UML
==================================

Antes de entrar en los ejemplos del dominio IACT conviene
fijar el mapa: UML organiza sus diagramas en dos grandes
familias según representen estructura estática o
comportamiento dinámico.

1. Diagramas estructurales
--------------------------

Representan la **organización estática** del sistema: qué
piezas existen y cómo están conectadas.

- **Diagrama de clases** — estructura estática del
  sistema (entidades, atributos, operaciones,
  asociaciones).
- **Diagrama de objetos** — instancias concretas de
  clases en un momento específico (snapshot).
- **Diagrama de componentes** — organización y
  dependencias entre componentes desplegables.
- **Diagrama de despliegue** — distribución física del
  sistema en nodos y conexiones.
- **Diagrama de paquetes** — organización en
  agrupaciones lógicas y dependencias entre ellas.

2. Diagramas de comportamiento
------------------------------

Muestran **cómo el sistema actúa y cambia dinámicamente**.
Se subdividen en dos sub-familias.

2.A Diagramas generales de comportamiento
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Diagrama de casos de uso** — interacciones
  usuario-sistema (qué hace el sistema, no cómo).
- **Diagrama de actividades** — flujo de trabajo y
  procesos: pasos, decisiones, paralelismo,
  responsabilidades.
- **Diagrama de estados** — ciclo de vida de un objeto:
  estados y transiciones disparadas por eventos.

2.B Diagramas de interacción
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Subconjunto de los diagramas de comportamiento, centrados
en cómo los elementos colaboran:

- **Diagrama de secuencia** — interacción entre objetos
  ordenada en el **tiempo** (eje vertical).
- **Diagrama de colaboración/comunicación** — relaciones
  y colaboración entre objetos en el **espacio** (énfasis
  en los enlaces).
- **Diagrama de tiempo (*timing*)** — comportamiento de
  uno o más objetos en períodos específicos, con foco en
  duraciones y restricciones temporales.

Naturaleza de cada familia
--------------------------

- **Estructurales** → organización estática del sistema.
- **Comportamiento** → cómo el sistema actúa y cambia.
- **Interacción** (sub-familia) → cómo los elementos
  colaboran entre sí.

Cobertura de esta guía aplicada a IACT
--------------------------------------

.. list-table::
 :widths: 30 25 45
 :header-rows: 1

 * - Diagrama UML
   - Familia
   - Documento que lo aplica a IACT
 * - Clases
   - Estructural
   - § 1 de este documento;
     :doc:`relaciones-uml`,
     :doc:`agregacion-interfaces`
 * - Objetos
   - Estructural
   - § 2 de este documento;
     :doc:`diagramas-colaboraciones`
 * - Componentes
   - Estructural
   - :doc:`diagramas-componentes` (H12)
 * - Despliegue
   - Estructural
   - :doc:`diagramas-distribucion` (H13)
 * - Paquetes
   - Estructural
   - Cubierto implícitamente por la jerarquía de apps
     Django (ver :doc:`diagramas-componentes`).
 * - Casos de uso
   - Comportamiento (general)
   - :doc:`casos-uso-especificacion`,
     :doc:`casos-uso-diagramas`
 * - Actividades
   - Comportamiento (general)
   - :doc:`diagramas-actividades` (H11)
 * - Estados
   - Comportamiento (general)
   - :doc:`diagramas-estados` (H8)
 * - Secuencias
   - Interacción
   - :doc:`diagramas-secuencias` (H9)
 * - Colaboración/Comunicación
   - Interacción
   - :doc:`diagramas-colaboraciones` (H10)
 * - Tiempo (*timing*)
   - Interacción
   - :doc:`diagramas-tiempo` (preliminar, v0.1.0).
     Desarrollo definitivo abierto en WP — usar solo
     cuando un UC requiere razonamiento sobre duraciones
     o restricciones temporales (SLA CNST_017, ventana
     ETL CNST_006/008, throttling CNST_011).

Las secciones que siguen muestran cada diagrama relevante
aplicado al dominio IACT, en el orden histórico (Schmuller
H1-H13). Para localizar un diagrama por familia, usar la
tabla anterior.

Reformulación canónica de las tres familias
-------------------------------------------

Una formulación más concisa (común en literatura
moderna):

- **Diagramas de estructura** representan la
  composición de los sistemas y se usan para
  **visualizar clases y componentes**.
- **Diagramas de comportamiento** modelan los aspectos
  más dinámicos del sistema; útiles para **entender qué
  comportamiento debe manejar el sistema**, en
  particular durante el diseño.
- **Diagramas de interacción** muestran **flujos
  específicos entre procesos** (por ejemplo, sistemas),
  componentes o clases.

Cada familia tiene casos de uso específicos: la decisión
de qué diagrama elegir se guía por la pregunta de qué
aspecto del sistema se quiere comunicar.

Técnica complementaria: el modelo C4
------------------------------------

UML no es la única técnica de diagramación arquitectónica
útil. El **modelo C4** (de Simon Brown) propone una
manera **simple y legible** de modelar la arquitectura
del software, complementaria a UML.

C4 organiza los diagramas en **cuatro niveles de
abstracción**, cada uno respondiendo a una pregunta
distinta:

.. list-table::
 :widths: 18 28 30 24
 :header-rows: 1

 * - Nivel C4
   - Pregunta que responde
   - Audiencia
   - Equivalente UML
 * - **1. Context**
   - ¿Qué es el sistema y cómo encaja en su entorno?
   - Stakeholders no técnicos.
   - Diagrama de casos de uso a alto nivel.
 * - **2. Container**
   - ¿Qué aplicaciones / servicios / bases de datos
     existen y cómo se comunican?
   - Equipo técnico, ops.
   - Diagrama de despliegue (cap. 13) +
     componentes (cap. 12).
 * - **3. Component**
   - ¿Qué componentes hay dentro de cada container y
     cómo interactúan?
   - Desarrolladores.
   - Diagrama de componentes (cap. 12).
 * - **4. Code**
   - ¿Cómo se materializa cada componente en clases /
     módulos?
   - Desarrolladores en mantenimiento.
   - Diagrama de clases (cap. 1) — opcional, suele
     auto-generarse.

Por qué C4 puede complementar a UML en IACT
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

UML es **rico en notación** pero puede ser exhaustivo
para audiencias no técnicas. C4 sacrifica notación a
cambio de **legibilidad** y un **mapeo claro de
audiencias** (de stakeholder a desarrollador conforme se
desciende de nivel 1 a 4).

Para un SAD futuro de IACT (ver § 11 de
:doc:`plan-documentacion-uc`), una combinación viable:

- **C4 nivel 1 (Context)** — para presentar IACT a
  comités no técnicos: el sistema como caja única con
  sus actores (supervisores, auditores) y sistemas
  externos (LDAP, IVR, BD operativa).
- **C4 nivel 2 (Container)** — para discutir
  arquitectura: ``vm-iact``, ``ldap-corporativo``,
  ``bd-operativa``, ``ivr-host`` y los protocolos entre
  ellos. Ya cubierto en
  :doc:`diagramas-distribucion`.
- **C4 nivel 3 (Component)** — para entender la
  estructura interna de ``vm-iact``: las apps Django y
  sus interfaces. Ya cubierto en
  :doc:`diagramas-componentes`.
- **C4 nivel 4 (Code)** — opcional; los diagramas de
  clases UML (este documento, § 1) suelen ser
  suficientes.

El uso conjunto de UML y C4 no exige reescribir nada:
los diagramas de :doc:`diagramas-componentes` y
:doc:`diagramas-distribucion` ya producen niveles 2 y 3
de C4 con notación PlantUML estándar.

Recomendación IACT: **mantener UML como técnica
principal** del proyecto; usar C4 como **lente
explicativo** cuando la audiencia lo justifique
(stakeholders, comités, onboarding rápido). Decisión
final del SAD futuro.

Historia de la diagramación y por qué IACT eligió PlantUML
----------------------------------------------------------

Diagramar software ha pasado por tres etapas:

1. **Dibujo manual** — había que encontrar un programa
   (Visio, Dia, etc.), instalarlo y dibujar
   meticulosamente cajas y líneas asegurando
   alineación. Crear diagramas complejos podía llevar
   horas.
2. **Herramientas web visuales** — eliminaron parte del
   dolor pero aún exigían arrastrar formas y trazar
   conexiones a mano.
3. **Diagramas como código** — herramientas como
   PlantUML y Mermaid permiten describir diagramas en
   sintaxis textual (similar a Markdown) y dejar el
   layout al renderer. Lo que antes tomaba horas hoy
   toma diez o quince minutos.

Esta evolución es lo que muchos llaman una **revolución
de diagramación**: la barrera de entrada bajó tanto que
diagramar dejó de ser una actividad costosa y se volvió
parte natural del flujo de trabajo del desarrollador.

Mermaid vs PlantUML — el debate moderno
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Mermaid** ha ganado tracción rápidamente: **GitHub** y
**GitLab** soportan renderizado nativo en Markdown sin
herramientas adicionales. Eso lo hace particularmente
atractivo para README, issues y PRs.

**PlantUML** es más antiguo, más expresivo y soporta más
tipos de diagrama UML (incluyendo diagramas de tiempo,
estados complejos, despliegue con notación rica), pero
requiere una toolchain (servidor PlantUML o plugin
Sphinx ``sphinxcontrib-plantuml``) para renderizar.

Por qué IACT eligió PlantUML
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A pesar de la popularidad creciente de Mermaid, el
proyecto IACT eligió **PlantUML** por razones
documentadas en
:doc:`/base-cognitiva/plantuml-guide/guidelines`. Las
razones operativas:

1. **Cobertura UML completa** — los diagramas que este
   cajón necesita (estados con sub-estados, secuencias
   con activaciones complejas, despliegue con
   ``mod_wsgi`` + Apache + bases de datos físicas,
   colaboraciones con numeración jerárquica de
   mensajes) tienen mejor soporte en PlantUML que en
   Mermaid.
2. **Sphinx como motor único** — la documentación IACT
   se publica con Sphinx; ``sphinxcontrib-plantuml`` ya
   está integrado al pipeline. Mermaid requeriría
   tooling adicional.
3. **Estilos centralizados** — los diagramas
   referencian ``source/_static/plantuml-styles.puml``
   para uniformidad visual; ese mecanismo no existe en
   Mermaid.
4. **Política del proyecto** — registrada y aplicada
   sistemáticamente por ``.claude/rules/`` y revisada
   en cada commit. Los diagramas Mermaid no pasan la
   guideline.

Esta decisión es deliberada y consistente con
ADR_DEVOPS_001 (un solo stack canónico) y con I-002
(una sola fuente de verdad). Las nuevas guías y UCs del
proyecto **deben usar PlantUML** — convertir diagramas
Mermaid existentes a PlantUML antes de integrarlos.

Reconocimiento de la limitación
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PlantUML tiene un costo: la toolchain. Si en el futuro
el proyecto necesita diagramas embebidos en GitHub
issues / discussions / READMEs públicos sin el pipeline
Sphinx, el equipo puede evaluar Mermaid **solo en esos
contextos** (documentación pública del repositorio en
GitHub) sin alterar las guías internas, que seguirán en
PlantUML. Esa decisión exigiría un ADR explícito.

Cómo crear diagramas — flujo de trabajo PlantUML en IACT
--------------------------------------------------------

El equivalente al ecosistema "Mermaid Live + VS Code
plugin" en PlantUML cubre las mismas necesidades:
**bocetos rápidos**, **edición con preview** y
**publicación final integrada al pipeline**.

Tres rutas según el caso de uso
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
 :widths: 28 36 36
 :header-rows: 1

 * - Ruta
   - Cuándo usarla
   - Herramienta recomendada
 * - **Online (boceto rápido)**
   - Esbozo de un diagrama nuevo, explicación rápida a
     un colega, prototipo antes de pulir.
   - **PlantText** (``planttext.com``) o el servidor
     público ``plantuml.com``. Render en el navegador
     mientras se escribe el código.
 * - **Editor con preview en vivo**
   - Trabajo cotidiano sobre los archivos ``.rst`` del
     repositorio.
   - **VS Code** + extensión "PlantUML" (de jebbs)
     con preview en split panel; o
     **IntelliJ** + plugin "PlantUML Integration".
 * - **Pipeline Sphinx (publicación)**
   - Diagrama final integrado al sitio
     publicado.
   - ``sphinxcontrib-plantuml`` ya configurado en
     ``conf.py``. Render automático en
     ``make html``.

Bocetos rápidos
~~~~~~~~~~~~~~~

Para bocetos descartables ("explicar un flujo a un
colega", "discutir un cambio en una llamada"), abrir
``planttext.com`` y pegar el siguiente esqueleto:

.. code-block:: plantuml

   @startuml
   skinparam shadowing false
   skinparam roundCorner 8

   rectangle a
   rectangle b
   rectangle c
   rectangle d

   a --> b
   a --> c
   b --> d
   c --> d
   @enduml

Render inmediato en el navegador, exportable a PNG / SVG
con un clic. Equivalente al ejemplo "flowchart LR
a --> b & c --> d" de la literatura Mermaid: el mismo
grafo de cuatro nodos diamante (a → b/c → d), expresado
en sintaxis PlantUML.

Edición con preview en VS Code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Para diagramas que terminarán en el repositorio:

1. Abrir el archivo ``.rst`` en VS Code.
2. Instalar la extensión **"PlantUML" by jebbs**.
3. Posicionar el cursor sobre un bloque ``.. uml::``.
4. ``Alt+D`` (o ``Cmd+D`` en macOS) → preview en
   split panel.
5. El preview se actualiza al guardar.

Esta ruta cubre el caso de uso del autor de la obra
("Markdown Preview Mermaid Support para VS Code" —
preview en tiempo real) con un equivalente directo para
PlantUML.

Publicación con Sphinx
~~~~~~~~~~~~~~~~~~~~~~

El pipeline canónico del proyecto:

1. Diagrama embebido en ``.rst`` con
   ``.. uml::`` (Sphinx directive).
2. Estilos compartidos vía
   ``!include ../../_static/plantuml-styles.puml``.
3. ``make html`` invoca ``sphinxcontrib-plantuml`` →
   genera SVG/PNG → embebe en el sitio.

Ver :doc:`/base-cognitiva/plantuml-guide/guidelines`
para detalles de configuración.

CLI para automatización
~~~~~~~~~~~~~~~~~~~~~~~

Si se necesita generación batch o pre-render fuera de
Sphinx:

.. code-block:: bash

   # render una vez
   plantuml diagrama.puml

   # watch mode (re-renderiza al cambiar)
   plantuml -gui diagrama.puml

El JAR se descarga desde el sitio oficial
(``plantuml.com``) y requiere Java 8+.

Recomendación operativa para IACT
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Boceto** → ``planttext.com``.
- **Diseño iterativo** → VS Code + plugin jebbs.
- **Publicación** → ``make html`` (Sphinx).
- **Compartir un diagrama suelto con alguien sin acceso
  al repo** → exportar SVG desde VS Code o
  ``planttext.com``; **no** pegar PNG sin el código
  fuente al lado (rompe DRY: la imagen y el código son
  la misma información).

Historia de la diagramación, en perspectiva
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

La observación del autor citado en la sección anterior
("lo que antes tomaba horas hoy toma diez o quince
minutos") aplica idénticamente a PlantUML: la
combinación **online editor + plugin de IDE + pipeline
Sphinx** elimina la fricción de la diagramación manual
y vuelve viable mantener los diagramas **sincronizados
con el código**, no como artefactos puntuales que
envejecen.

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
   - :doc:`plan-documentacion-uc`
 * - **Ejemplos OOP aplicados al dominio (compañero)**
   - :doc:`orientacion-objetos`
 * - **Modelo RBAC vigente**
   - :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact`
 * - **Restricciones citadas**
   - CNST_001 (no email), CNST_006/008 (ventana ETL 6-12h),
     CNST_019/020 (export async + throttling), CNST_025
     (auditoría inmutable), BR_012 (segmento único),
     ADR_DEVOPS_001 (Vagrant + Apache + mod_wsgi).
 * - **Política de diagramación**
   - :doc:`/base-cognitiva/plantuml-guide/guidelines`
