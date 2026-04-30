.. meta::
 :artefacto: METODOLOGIA_DIAGRAMAS_COMPONENTES
 :tipo: Guia-Metodologica
 :dominio: requisitos
 :subdominio: _metodologia-aplicacion
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-04-30
 :ultimo_cambio: 2026-04-30
 :autor: NestorMonroy
 :clasificacion: Interno

==========================================================
Diagramas de componentes — arquitectura física IACT (H12)
==========================================================

Propósito
=========

Modelar **la estructura física** del sistema IACT: qué
artefactos ejecutables existen, qué interfaces exportan o
importan, y cómo dependen entre sí.

Diferencia con diagramas previos:

- **Clases / OOP** → conceptos en el código fuente.
- **Componentes** → archivos reales en disco/servidor:
  módulos Django, paquetes WSGI, librerías, scripts ETL,
  bases de datos.

Pregunta que responde:

   *¿Cómo se organiza el código y los binarios en los
   servidores de IACT, y qué contratos los unen?*

Marco metodológico
==================

- Skill principal: ``rm-specification``
- Skill complementario: ``rm-analysis``
- Stack canónico: ADR_DEVOPS_001 → Vagrant + Apache +
  ``mod_wsgi`` + Django + MySQL + Redis. **No** Docker, K8s,
  Nginx, Gunicorn.
- Política de diagramación:
  :doc:`/base-cognitiva/plantuml-guide/guidelines`

Preludio — modelar la arquitectura
==================================

Tras documentar el dominio (:doc:`analisis-dominio`) y
visualizar los flujos de aplicación
(:doc:`diagramas-secuencias`), el siguiente paso natural
es **modelar la arquitectura**: cómo los componentes y
nodos físicos se organizan más allá del flujo puntual de
un UC.

La regla operativa, alineada con § 12 de
:doc:`plan-documentacion-uc` (JEDUF):

   *Hacer suficiente diseño inicial para validar el
   enfoque, pero no tanto que no quede espacio para que
   el diseño evolucione.*

Cuando se diseña un sistema, el objetivo no es producir
un plano completo y entregárselo a los implementadores
para que lo "ejecuten". Es **embeberse en el equipo que
lo construye**, buscar feedback regular, evolucionar el
diseño colaborativamente.

Por qué los diagramas-como-código importan aquí
-----------------------------------------------

Antes de PlantUML / Mermaid, cambiar un diagrama
arquitectónico era doloroso: mover cajas, redibujar
líneas, recolocar etiquetas — horas de trabajo manual
para un cambio significativo.

Con **PlantUML + Sphinx** (la combinación IACT) los
diagramas son texto: editarlos en una reunión es
factible, probar una idea toma minutos y, si no aporta,
se descarta sin gran inversión. Esa **agilidad
arquitectónica** es uno de los argumentos más fuertes
para diagramas-como-código (ver "Historia de la
diagramación" en :doc:`diagramas-uml`).

Cuándo usar diagramas de arquitectura
-------------------------------------

Tres usos canónicos en IACT:

1. **README del proyecto / submódulo** — cuando alguien
   llega nuevo o un equipo distinto recibe el sistema,
   un diagrama arquitectónico claro reemplaza páginas
   de documentación textual.
2. **ADRs del proyecto**
   (``.thyrox/context/decisions/``) — al proponer un
   diseño o un cambio mayor, el diagrama itera junto
   con la decisión. Crear un ADR es esencialmente
   proponer una arquitectura.
3. **Onboarding / handoff** — cuando un servicio se
   reasigna entre equipos o ingresa un nuevo
   colaborador, el diagrama de componentes y
   despliegue cuenta la historia que un walkthrough
   verbal tardaría días en transmitir.

Cómo este cajón cubre la arquitectura
-------------------------------------

Tres documentos del cajón colaboran en este nivel:

.. list-table::
 :widths: 28 35 37
 :header-rows: 1

 * - Documento
   - Aspecto
   - Equivale en C4 a…
 * - **Este documento**
     (:doc:`diagramas-componentes`)
   - Apps Django como componentes desplegables y sus
     interfaces.
   - **Component view** (nivel 3 de C4).
 * - :doc:`diagramas-distribucion`
   - Nodos físicos (vm-iact, ldap, bd-operativa,
     ivr-host) y protocolos.
   - **Container / Deployment view** (niveles 2 y
     físico de C4).
 * - El SAD futuro
     (:doc:`plan-documentacion-uc` § 11)
   - Vista holística que integra dominio + flujos +
     componentes + distribución.
   - **Context** + síntesis (nivel 1 + integración).

El **modelo C4** se trata como técnica complementaria
en la sección "Técnica complementaria: el modelo C4"
de :doc:`diagramas-uml`. La política IACT mantiene UML
como técnica principal con C4 como lente para audiencias
no técnicas o material de aprobación.

Mensaje del capítulo
--------------------

A partir de aquí el cajón se centra en la **vista
arquitectónica**. Las secciones siguientes (§§ 1-12 de
este documento + las secciones de
:doc:`diagramas-distribucion`) construyen ese cuadro:
qué componentes existen, qué contratos los unen, dónde
viven y cómo se comunican.

----

1. Qué es un componente en IACT
===============================

Un componente es una pieza física desplegable o referenciada
en el sistema. En el stack IACT los más típicos son:

- Apps Django: ``auth_app``, ``usr_app``, ``acc_app``,
  ``perm_app``, ``rpt_app``, ``alr_app``, ``pip_app``,
  ``aud_app``, ``log_app``.
- WSGI entry point: ``iact.wsgi``.
- Bundle frontend: ``iact-admin.bundle.js``.
- Scripts ETL: ``etl_runner.py``, ``etl_window.cron``.
- Bases de datos físicas: ``bd_operativa`` (read-only),
  ``bd_analytics``, ``audit_log``.
- Servicios de runtime: Apache + ``mod_wsgi``, Redis.
- Integraciones: LDAP corporativo, IVR (read-only).

Una clase OOP de IACT (``Reporte``, ``Sesion``, ``Permiso``)
se materializa como módulo Python dentro de una app Django,
y esa app se distribuye como componente.

2. Interfaces: exportación e importación
========================================

Cada componente IACT define sus interfaces explícitas. Las
relevantes para nuestro dominio:

.. list-table::
 :widths: 25 35 40
 :header-rows: 1

 * - Interfaz
   - Operaciones clave
   - Quién la realiza
 * - ``ISecurity``
   - ``verificar_permiso``, ``validar_sesion``,
     ``aplicar_sod``
   - ``perm_app`` (CNST_030)
 * - ``IAuditLog``
   - ``registrar_evento``, ``consultar`` (read-only)
   - ``aud_app`` (CNST_025, immutable)
 * - ``IReporte``
   - ``generar``, ``exportar_async``
   - ``rpt_app`` (CNST_019/020)
 * - ``IAlerta``
   - ``evaluar``, ``publicar``, ``reconocer``
   - ``alr_app``
 * - ``INotificacion``
   - ``enviar_a_buzon`` (CNST_001 — sin email)
   - ``log_app``
 * - ``IDatosOperativos``
   - ``leer`` (read-only, CNST_007)
   - ``bd_operativa``
 * - ``IDatosAnalytics``
   - ``leer``, ``insertar``, ``agregar``
   - ``bd_analytics``
 * - ``IETL``
   - ``ejecutar_ventana`` (CNST_006/008)
   - ``pip_app`` + ``etl_runner``

Regla: un componente IACT **solo** se comunica con otro a
través de una interfaz declarada. Las llamadas directas a
ORM o tablas de otra app rompen el contrato.

3. Vista física global de IACT
==============================

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   skinparam componentStyle rectangle

   package "Cliente (navegador del supervisor)" {
     [iact-admin.bundle.js] as UI
   }

   package "Apache + mod_wsgi" {
     [iact.wsgi] as WSGI
     package "Apps Django" {
       [auth_app]
       [perm_app]
       [rpt_app]
       [alr_app]
       [pip_app]
       [aud_app]
       [log_app]
     }
   }

   package "Datos" {
     database "bd_operativa\n(read-only, CNST_007)" as BDO
     database "bd_analytics" as BDA
     database "audit_log\n(immutable, CNST_025)" as AUDIT
     database "Redis\n(sesiones, throttling)" as REDIS
   }

   package "Integraciones" {
     [LDAP corporativo] as LDAP
     [IVR (read-only)] as IVR
     [etl_runner.py] as ETL
   }

   UI --> WSGI : HTTPS
   WSGI --> auth_app
   WSGI --> perm_app
   WSGI --> rpt_app
   WSGI --> alr_app
   WSGI --> aud_app
   WSGI --> log_app
   auth_app --> LDAP
   auth_app --> REDIS : sesion (CNST_002)
   perm_app --> aud_app : ISecurity → IAuditLog
   rpt_app --> BDA : IDatosAnalytics
   rpt_app --> aud_app
   alr_app --> BDA
   alr_app --> log_app : INotificacion
   pip_app --> ETL
   ETL --> BDO : IDatosOperativos
   ETL --> IVR
   ETL --> BDA : IDatosAnalytics
   aud_app --> AUDIT : IAuditLog
   @enduml

4. Vista detallada con interfaces (lollipop)
============================================

Ejemplo: flujo de exportación de reporte UC_RPT_04.

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   skinparam componentStyle rectangle

   [rpt_app] as RPT
   [perm_app] as PERM
   [aud_app] as AUD
   [log_app] as LOG
   database "bd_analytics" as BDA

   PERM -( ISecurity
   AUD  -( IAuditLog
   LOG  -( INotificacion
   RPT  -( IReporte
   BDA  -( IDatosAnalytics

   RPT ..> ISecurity : usa
   RPT ..> IDatosAnalytics : usa
   RPT ..> IAuditLog : usa
   RPT ..> INotificacion : usa (buzon CNST_001)
   @enduml

Lectura: ``rpt_app`` *realiza* ``IReporte`` e *importa*
``ISecurity``, ``IDatosAnalytics``, ``IAuditLog`` e
``INotificacion``. Cualquier cambio interno en ``perm_app``
es transparente para ``rpt_app`` mientras ``ISecurity`` se
mantenga estable.

5. Tipos de componentes en IACT
===============================

.. list-table::
 :widths: 25 35 40
 :header-rows: 1

 * - Categoría
   - Qué incluye
   - Ejemplos IACT
 * - **Distribución**
   - Lo desplegado en el VM Vagrant.
   - ``iact.wsgi``, apps Django empaquetadas,
     ``iact-admin.bundle.js``.
 * - **Trabajo**
   - Lo que el desarrollador edita.
   - ``*.py`` de cada app, migraciones,
     ``plantuml-styles.puml``, plantillas RST.
 * - **Ejecución**
   - Lo que se materializa en runtime.
   - Sesiones Redis, archivos temporales de export
     (CNST_019), logs de Apache, ``audit_log`` rows.

6. Sustitución y reutilización
==============================

Casos reales en IACT:

- **Cambiar el origen de datos operativos** (de la BD
  legacy a una réplica): siempre que el nuevo backend
  realice ``IDatosOperativos`` con la misma semántica
  read-only (CNST_007), ``pip_app`` no requiere cambios.
- **Reemplazar el evaluador de alertas** por uno con
  reglas dinámicas: aceptable si sigue realizando
  ``IAlerta`` y respeta el flujo de auditoría
  (UC_ALR_03).
- **Cambiar el mecanismo de notificación** está
  restringido por CNST_001 (solo buzón interno). Cualquier
  implementación que pretenda realizar ``INotificacion``
  via email queda fuera del contrato.

7. Diseño para reutilización en IACT
====================================

Reglas que aplican a este proyecto:

1. Las interfaces se versionan en ``adr-std-*`` cuando
   cambian — no se rompen sin migración explícita.
2. ``aud_app`` y ``perm_app`` son los componentes con más
   consumidores; mantenerlos con superficie mínima y
   altamente cohesiva.
3. ``pip_app`` y ``etl_runner`` deben poder ejecutarse en
   modo dry-run para diagnóstico sin tocar
   ``bd_analytics``.
4. Cada app Django expone su contrato como módulo
   ``services.py`` — nadie consume modelos cruzados
   directamente.
5. Las dependencias prohibidas se documentan en
   ``adr-cross-app-dependencies`` y se validan en CI.

8. Mapeo componente ↔ UCs IACT
==============================

.. list-table::
 :widths: 22 28 50
 :header-rows: 1

 * - Componente
   - Interfaces que realiza
   - UCs principales
 * - ``auth_app``
   - ``IAutenticacion``
   - UC_AUTH_01 Login, UC_AUTH_02 Logout
 * - ``perm_app``
   - ``ISecurity``
   - UC_PERM_07 Verificar permiso, UC_PERM_* SoD
 * - ``rpt_app``
   - ``IReporte``
   - UC_RPT_04 Export, UC_RPT_07 Programado
 * - ``alr_app``
   - ``IAlerta``
   - UC_ALR_03 Reconocer crítica
 * - ``pip_app`` + ``etl_runner``
   - ``IETL``
   - UC_PIP_01 Carga ETL
 * - ``aud_app``
   - ``IAuditLog``
   - Todos los UCs (audit cruzado, CNST_025)
 * - ``log_app``
   - ``INotificacion``
   - UC_RPT_04, UC_ALR_03 (buzón CNST_001)

9. Cuándo usar diagramas de componentes
=======================================

.. list-table::
 :widths: 50 50
 :header-rows: 1

 * - Usar cuando…
   - No usar cuando…
 * - Documentamos arquitectura física para deployment.
   - El foco es flujo dinámico (usar secuencias o
     actividades).
 * - Hay riesgo de acoplamiento cruzado entre apps Django.
   - Solo hay un único módulo monolítico sin contratos.
 * - Se evalúa sustituir un proveedor (datos, ETL, alertas).
   - Aún no existe el componente — primero modelar clases.
 * - Se planea un release o despliegue (ver también
     :doc:`/requisitos/_metodologia-aplicacion/index` y, en
     el futuro, diagramas de despliegue).
   - El cambio es solo cosmético en UI.

10. Buenas prácticas
====================

1. Cada componente declara explícitamente sus interfaces
   exportadas e importadas — nada implícito.
2. No mezclar en un mismo diagrama componentes de
   distribución y de trabajo; separar vistas.
3. Etiquetar todas las dependencias con la interfaz
   relevante (``..> ISecurity : usa``).
4. Mantener un único diagrama global de IACT (sección 3) y
   varios diagramas de detalle por subdominio (sección 4).
5. Vincular cada componente a su CNST/BR/ADR principal en
   el texto, no dentro del diagrama.
6. Cuando aparezca un componente externo (LDAP, IVR),
   marcarlo claramente y declarar si es read-only.

11. Patrones de backup desde la perspectiva cohesión/acoplamiento
=================================================================

El backup de datos en IACT (especialmente ``audit_log``,
``bd_analytics`` y configuración del catálogo RBAC) admite
distintos patrones arquitectónicos. Cada uno tiene un perfil
distinto en términos de **cohesión** y **acoplamiento** —
los principios que el documento §§ 10-11 de
:doc:`orientacion-objetos` aplica a clases también valen
para componentes.

11.1 Backup distribuido / descentralizado
-----------------------------------------

Cada componente IACT realiza su propio backup según sus
necesidades. ``aud_app`` exporta ``audit_log``,
``rpt_app`` snapshots agregados, ``pip_app`` registros de
ventana ETL, ``perm_app`` exporta el catálogo RBAC.

Cohesión
~~~~~~~~

Alta cohesión funcional: cada módulo encapsula su lógica
de backup, principio de responsabilidad única por
operación, fácil testing aislado.

Acoplamiento
~~~~~~~~~~~~

Bajo: módulos autónomos, interfaces minimalistas, cambios
localizados, fallos aislados.

Ventajas
~~~~~~~~

- **Inmediatez** — backup disponible justo antes de cada
  cambio, rollback granular, contexto claro.
- **Simplicidad** — directo, autocontenido, pocas
  dependencias.
- **Granularidad** — control preciso por operación,
  trazabilidad de cambios, debugging directo.
- **Resiliencia local** — fallo de un componente no
  afecta backups de otros.

Desventajas
~~~~~~~~~~~

- **Desorganización** — backups dispersos, inventario
  difícil, posible duplicación.
- **Inconsistencia** — formatos y ubicaciones distintos,
  política única difícil de aplicar.
- **Recursos** — espacio fragmentado, overhead por
  múltiples backups, limpieza compleja.
- **Vista global limitada** — recuperar un punto en el
  tiempo del **sistema completo** exige coordinar
  recuperaciones independientes.

11.2 Backup centralizado / monolítico
-------------------------------------

Un único subsistema toma snapshots completos del estado
de IACT (volúmenes MySQL, dumps de Redis, configuración).
Una sola política, una sola programación, una sola fuente
de verdad para restauración.

Cohesión
~~~~~~~~

Alta **cohesión de control** pero responsabilidades
mezcladas: el subsistema toca audit, analytics, RBAC y
sesiones a la vez. Boundaries poco definidos entre lo
que respalda.

Acoplamiento
~~~~~~~~~~~~

Alto: dependencias fuertes con todas las apps Django,
testing extensivo, cambios en el subsistema afectan al
resto.

Ventajas
~~~~~~~~

- **Organización** — estructura clara, política unificada,
  control centralizado.
- **Consistencia** — un único formato, política única.
- **Eficiencia de recursos** — optimización global,
  menos overhead, gestión unificada.
- **Auditoría** — fácil demostrar conformidad con
  CNST_025 / regulaciones — un solo punto de evidencia.

Desventajas
~~~~~~~~~~~

- **Complejidad inicial** — diseño y configuración del
  subsistema más laboriosa.
- **Rigidez** — cambios parciales difíciles, actualización
  global.
- **Punto único de fallo** — si el subsistema cae, ningún
  backup nuevo se hace; requiere redundancia.
- **Escalabilidad limitada** — crecimiento de un
  componente puede saturar el sistema central.

11.3 Backup híbrido
-------------------

Combina distribuido + centralizado: cada app mantiene su
backup local granular para rollback inmediato, y un
subsistema central toma snapshots periódicos consolidados
para política y recuperación de sistema.

Cohesión
~~~~~~~~

**Multinivel**: cohesión modular en cada app + cohesión
de sistema en el orquestador. Separación clara de
concerns; jerarquía de responsabilidades.

Acoplamiento
~~~~~~~~~~~~

**Controlado**: *loose coupling* temporal con
sincronización asíncrona, interfaces bien definidas entre
los dos niveles.

Ventajas
~~~~~~~~

- **Balance** entre inmediatez (local) y orden (central).
- **Resiliencia** — redundancia selectiva, fallback entre
  niveles.
- **Escalabilidad controlada** — cada nivel evoluciona
  según su carga.

Desventajas
~~~~~~~~~~~

- **Complejidad arquitectónica** — diseño inicial más
  elaborado, planificación detallada.
- **Sincronización** — coordinar dos niveles introduce
  estados distribuidos.
- **Costos** — inversión inicial mayor, expertise
  variado, mantenimiento más sofisticado.

11.4 Comparativa
----------------

.. list-table::
 :widths: 22 26 26 26
 :header-rows: 1

 * - Aspecto
   - Distribuido
   - Centralizado
   - Híbrido
 * - Cohesión
   - Alta funcional, por app.
   - Alta de control, mezclada.
   - Multinivel.
 * - Acoplamiento
   - Bajo.
   - Alto.
   - Controlado.
 * - Inmediatez
   - Excelente.
   - Limitada.
   - Buena (capa local).
 * - Política única
   - Difícil.
   - Natural.
   - Por orquestador.
 * - Punto único de fallo
   - No.
   - Sí (mitigable).
   - No (con fallback).
 * - Inversión inicial
   - Baja.
   - Media.
   - Alta.
 * - Adherencia a principios
   - Óptima.
   - Comprometida.
   - Pragmática.

11.5 Recomendación para IACT
----------------------------

- **``audit_log`` (CNST_025 immutable)** — exigir un
  componente de backup **dedicado** y consistente
  (centralizado o capa central del híbrido). El audit
  debe poder restaurarse íntegro y verificarse contra
  hash; la dispersión distribuida lo dificulta.
- **``bd_analytics``** — admite distribuido si cada
  ventana ETL persiste su backup; conviene una capa
  central periódica para recuperación a un punto en el
  tiempo.
- **Catálogo RBAC y reglas SoD (CNST_030)** — backup
  versionado **distribuido** dentro de ``perm_app`` con
  inclusión periódica en el snapshot central; cualquier
  cambio en el catálogo es un evento que debe auditarse.
- **Configuración runtime** (umbrales de alerta,
  parámetros de export) — distribuido, dentro del
  componente que lo posee.

Recomendación general: **híbrido con sesgo distribuido**.
Esto combina la inmediatez y bajo acoplamiento del
distribuido con la consistencia y trazabilidad que
exigen las restricciones del proyecto. Cualquier
desviación (e.g. centralizado puro) debe registrarse en
un ADR de subdominio.

Conclusión de diseño
~~~~~~~~~~~~~~~~~~~~

Desde la perspectiva pura de diseño:

1. **Distribuido** — mejor alineación con cohesión y
   acoplamiento bajo.
2. **Centralizado** — desviación significativa, pero a
   veces inevitable por necesidades operativas.
3. **Híbrido** — balance pragmático para requerimientos
   complejos.

Como con todo patrón, la elección debe considerar no
solo los principios de diseño sino los **requisitos
específicos** del sistema, los recursos y el contexto.
Documentar la elección en un ADR.

----

12. Principios de cohesión y acoplamiento entre componentes
===========================================================

Los principios SOLID (ver §§ 16-20 de
:doc:`orientacion-objetos`) aplican a **clases**. Existe
un conjunto complementario de principios para
**componentes / paquetes**, formulado por Robert C.
Martin. Tres son **principios de cohesión** (qué clases
agrupar dentro de un componente) y tres son **principios
de acoplamiento** (cómo deben relacionarse los
componentes entre sí).

12.1 Principios de cohesión de paquete
--------------------------------------

REP — Reuse / Release Equivalence Principle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   *La granularidad de la reutilización es la misma que
   la granularidad de la liberación. Solo se pueden
   reutilizar efectivamente los componentes que se
   liberan a través de un sistema de seguimiento.*

Implicaciones:

- Una clase rara vez se reutiliza sola; necesita sus
  colaboradoras → liberar el conjunto como **componente**.
- El componente debe tener **número de versión** para
  que los reutilizadores puedan decidir cuándo adoptar
  versiones nuevas.
- Copiar código no es reutilización efectiva; viola DRY
  (§ 13 de :doc:`orientacion-objetos`).

En IACT: cada app Django se libera con su versión
SemVer (ver `metadata-standards.md`); reutilizar
``perm_app`` exige tomar también su catálogo de
funciones, sus modelos y sus servicios — no solo una
clase suelta.

CCP — Common Closure Principle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   *Las clases dentro de un componente liberado deben
   compartir un cierre común. Si una necesita ser
   cambiada, es probable que todas necesiten ser
   cambiadas.*

Es **SRP a nivel de componente**: un cambio típico debe
afectar a **un solo componente**, no a varios.

En IACT: un cambio en CNST_030 (SoD) toca solo
``perm_app``; un cambio en CNST_031 (rango export) toca
solo ``rpt_app``. Si un cambio toca tres apps, hay
agrupación incorrecta.

CRP — Common Reuse Principle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   *Las clases dentro de un componente liberado deben
   reutilizarse juntas. Debe ser imposible separar el
   componente para reutilizar menos que el total.*

Es **ISP a nivel de componente**: si un componente
contiene clases que **no se reutilizan juntas**, sus
consumidores se ven obligados a aceptar versiones
nuevas debido a cambios que no les afectan.

En IACT: ``rpt_app`` solo expone clases que conviven en
todos los reportes; clases que solo aplican a un caso
específico se mueven a un sub-paquete o app distinta.

Tensión entre los tres
~~~~~~~~~~~~~~~~~~~~~~

REP, CCP y CRP **tensionan**:

- REP y CCP empujan a componentes **grandes**
  (todo lo que se reutiliza junto y cambia junto).
- CRP empuja a componentes **pequeños**
  (no obligar a aceptar lo que no se usa).

El equilibrio se ajusta con la madurez del proyecto:
en IACT (proyecto en construcción) **CCP domina** —
agrupar por cierre de cambio. Cuando una app madure y
sea reutilizada externamente, CRP tomará protagonismo.

12.2 Principios de acoplamiento entre paquetes
----------------------------------------------

ADP — Acyclic Dependency Principle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   *La estructura de dependencia entre componentes debe
   ser un Grafo Dirigido Acíclico (DAG). No puede haber
   ciclos.*

Los ciclos son problemáticos:

- Mantenimiento difícil — los cambios se propagan a
  través del ciclo.
- Imposibilidad de liberar componentes en pequeños
  incrementos.

En IACT, las dependencias canónicas forman un DAG:

::

   log_app ←  alr_app  ← rpt_app  ←  ...
                ↓
              aud_app  ← perm_app ← auth_app
                ↑
              pip_app

(El sentido exacto puede consultarse en § 3 de este
documento). Cualquier ciclo entre apps es un defecto a
corregir; típicamente se rompe extrayendo la dependencia
común a una nueva app o invirtiendo con DIP (§ 20 de
:doc:`orientacion-objetos`).

SDP — Stable Dependency Principle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   *Las dependencias deben ir en la dirección de la
   estabilidad. Un componente nunca debe ser más estable
   que aquel del que depende.*

**Métrica de inestabilidad** I:

::

   I = Ce / (Ca + Ce)

donde:

- ``Ca`` = clases externas que **dependen del** componente
  (afferent coupling).
- ``Ce`` = clases externas **de las que el componente
  depende** (efferent coupling).

``I = 0`` → componente máximamente estable; ``I = 1`` →
máximamente inestable.

Las dependencias deben ir de **alto I** a **bajo I**. En
IACT, ``aud_app`` debe ser uno de los componentes con I
más bajo (todos dependen de él, él depende de pocos);
violar esto rompe CNST_025.

SAP — Stable Abstraction Principle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   *Mientras más estable sea un componente, más debe estar
   compuesto por clases abstractas.*

**Métrica de abstracción** A:

::

   A = (clases abstractas + interfaces) / (total de clases)

``A = 0`` → todo concreto; ``A = 1`` → todo abstracto.

Un componente máximamente estable y máximamente concreto
es **rígido** (cambios duros). Un componente máximamente
abstracto e inestable es **inutilizable**.

Distancia a la secuencia principal
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

La métrica que combina I y A:

::

   D = | A + I − 1 |
   (rango 0 ≤ D ≤ 1; deseable D ≈ 0)

D ≈ 0 → el componente está en la **secuencia principal**:
estable y abstracto, o inestable y concreto, en
equilibrio.

D lejano de 0 → componente mal balanceado:

- A=0, I=0 (estable y concreto): rígido.
- A=1, I=1 (abstracto e inestable): inútil — abstracción
  sin clientes.

Estos dos extremos son los **dolorosos**.

Cuadrante I/A — interpretación canónica
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Visualizando el plano (eje horizontal = ``I``, eje
vertical = ``A``), las cuatro esquinas tienen lectura
distinta:

.. list-table::
 :widths: 18 18 32 32
 :header-rows: 1

 * - Esquina
   - (I, A)
   - Significado
   - Diagnóstico
 * - **Inferior-izquierda**
   - (0, 0)
   - Máximamente estable y concreto.
   - **Zona de dolor — rígido.** Muchos clientes
     dependen de implementaciones concretas; cualquier
     cambio rompe a todos. Refactorizar a interfaces.
 * - **Superior-izquierda**
   - (0, 1)
   - Máximamente estable y abstracto.
   - **Ideal.** Es lo que queremos para los
     componentes núcleo (``aud_app``, ``perm_app`` con
     sus interfaces ``IAuditLog`` / ``ISecurity``).
 * - **Superior-derecha**
   - (1, 1)
   - Máximamente inestable y abstracto.
   - **Zona de dolor — inutilidad.** Abstracciones
     sin implementación concreta o sin consumidores.
     Borrar o consolidar.
 * - **Inferior-derecha**
   - (1, 0)
   - Máximamente inestable y concreto.
   - Aceptable si es un **componente cliente final**
     (vistas Django, plantillas RST). No debería
     servir de base a otros.

La **secuencia principal** es la diagonal que conecta
(0, 1) con (1, 0): los componentes en esa línea están
balanceados — los estables son abstractos (servir de
base), los inestables son concretos (uso final).

Implicaciones IACT
~~~~~~~~~~~~~~~~~~

- ``aud_app``, ``perm_app`` → meta: cerca de (0, 1).
  Bajo I (todos dependen de ellos), alto A (interfaces
  estables).
- ``rpt_app``, ``alr_app``, ``pip_app`` → meta:
  intermedio. Algunos consumidores, dependen de varias
  interfaces, mezclan abstracto y concreto.
- Vistas Django, templates, plantillas RST → meta:
  cerca de (1, 0). Inestables (cambian con la UI),
  concretas (no son base de nada).
- Cualquier componente que aparezca cerca de (0, 0) o
  (1, 1) durante una medición es candidato a refactor.

Aplicación IACT
~~~~~~~~~~~~~~~

Aplicación recomendada (sin medirla todavía formalmente):

- ``aud_app`` y ``perm_app`` → bajo I (todos los demás
  dependen de ellos), alto A (interfaces ``IAuditLog``,
  ``ISecurity``). D cercano a 0.
- ``rpt_app`` y ``alr_app`` → I medio, A medio. Razonable.
- Vistas Django y plantillas → alto I (dependen de todo),
  A bajo (concretas). D ≈ 0 esperado.

Si en algún momento se mide D y aparece un componente
con D > 0.5, abrir un WP de refactor.

12.3 Resumen
------------

.. list-table::
 :widths: 15 25 60
 :header-rows: 1

 * - Sigla
   - Nombre
   - En una línea
 * - REP
   - Reuse/Release Equivalence
   - Liberar lo que se reutiliza junto.
 * - CCP
   - Common Closure
   - Agrupar lo que cambia por las mismas razones (SRP
     a nivel de componente).
 * - CRP
   - Common Reuse
   - Agrupar lo que se reutiliza junto (ISP a nivel de
     componente).
 * - ADP
   - Acyclic Dependency
   - Sin ciclos entre componentes.
 * - SDP
   - Stable Dependency
   - Las dependencias van hacia los más estables.
 * - SAP
   - Stable Abstraction
   - Los más estables son los más abstractos.

Estos seis principios complementan SOLID a nivel de
arquitectura. Aplicarlos en IACT es la diferencia entre
un conjunto de apps Django **sueltas** y una arquitectura
**modular y mantenible**.

----

13. Vista Context (C4 nivel 1) aplicada a IACT
==============================================

El **diagrama de contexto del sistema** es la vista a
50 000 pies: contiene el **mínimo nivel de detalle** y
es deliberadamente **no técnico**. Su función es
modelar las interacciones entre los usuarios del
sistema y los demás sistemas externos involucrados.

Test de validación
~~~~~~~~~~~~~~~~~~

Una prueba operativa para saber si el nivel de detalle
es el correcto: **mostrarlo a un PM o a alguien no
técnico**. Si pueden entender qué quiere comunicar el
diagrama, está bien. Si necesitan que se les explique
con jerga técnica, hay demasiado detalle — pertenece a
los niveles 2 o 3.

El diagrama Context responde de un vistazo:

- **Quién** usa el sistema (actores).
- **Qué hace** el sistema en el contexto del negocio.
- **Con qué otros sistemas** interactúa para cumplir
  sus responsabilidades.

Tres elementos canónicos
~~~~~~~~~~~~~~~~~~~~~~~~

1. **Personas** (actores humanos) — quien interactúa
   con el sistema.
2. **El software del sistema** que se está
   diseñando — caja única, sin descomponer.
3. **Software de apoyo** — sistemas externos con los
   que interactúa.

Notación libre — convención IACT
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

C4 no impone notación canónica (ver § "C4 no impone
una notación específica" en :doc:`diagramas-uml`). La
convención IACT, alineada con la propuesta de Simon
Brown:

- **Personas** — actor con figura humanoide
  (``actor`` en PlantUML).
- **Sistema en diseño** — caja con borde más grueso o
  color destacado.
- **Sistemas externos** — cajas con color distinto,
  para diferenciarlos visualmente.
- **Flechas** etiquetadas con el **propósito** de la
  interacción, en términos de negocio (no
  protocolo).

Vista Context de IACT
~~~~~~~~~~~~~~~~~~~~~

Aplicada al sistema completo de IACT, la vista
Context muestra el sistema como una sola caja que
interactúa con sus actores humanos y los sistemas
corporativos externos:

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   title IACT — Vista Context (C4 nivel 1)

   skinparam actorBackgroundColor #E0E7FF
   skinparam rectangleBackgroundColor<<sistema>> #C7D2FE
   skinparam rectangleBorderColor<<sistema>> #1E40AF
   skinparam rectangleBackgroundColor<<externo>> #E0F2F1

   actor Supervisor as S
   actor Auditor as Aud
   actor "Operador ETL" as OETL

   rectangle "IACT\n(Plataforma de analitica\nde call center)" as IACT <<sistema>>

   rectangle "LDAP corporativo" as LDAP <<externo>>
   rectangle "BD operativa\n(call center)" as BDO <<externo>>
   rectangle "IVR-host" as IVR <<externo>>

   S --> IACT : consulta dashboards,\nreconoce alertas
   Aud --> IACT : consulta auditoria,\nverifica SoD
   OETL --> IACT : monitorea ventana ETL

   IACT --> LDAP : autentica usuarios
   IACT --> BDO : lee datos de llamadas\n(read-only)
   IACT --> IVR : lee eventos del IVR\n(read-only)
   @enduml

Lectura del diagrama
~~~~~~~~~~~~~~~~~~~~

- **Tres tipos de actor humano** — Supervisor (uso
  cotidiano), Auditor (revisión periódica), Operador
  ETL (monitoreo).
- **Una caja IACT** — el sistema completo, sin
  detallar internamente.
- **Tres sistemas externos**: LDAP corporativo
  (autenticación), BD operativa (origen de datos),
  IVR-host (eventos de telefonía).
- **Flechas etiquetadas en términos de negocio** —
  "consulta dashboards", "lee datos de llamadas",
  no "HTTP GET" ni "SQL SELECT". Esos detalles
  pertenecen al nivel Container.

Lo que el diagrama Context **no** muestra
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Apps Django internas (eso es nivel 3 Component).
- Stack canónico (mod_wsgi, MySQL, Redis) (nivel 2
  Container y físico).
- Protocolos exactos (HTTPS, LDAPS, SQL TCP) (nivel 2
  Container).
- Ciclo de vida de UCs específicos (eso son
  diagramas de secuencia / actividades).
- Restricciones técnicas detalladas (CNST_002 sesión
  única, CNST_006/008 ventana ETL) — solo aparecen
  como notas si son **vinculantes para entender el
  contexto** y a un PM le dicen algo.

Usos del Context en IACT
~~~~~~~~~~~~~~~~~~~~~~~~

1. **README del repositorio** — primera imagen para
   quien aterriza en el proyecto.
2. **Onboarding** de nuevos miembros (técnicos y no
   técnicos) — entender en 30 segundos qué es IACT y
   con quién dialoga.
3. **Presentaciones a comités** — replicar el sistema
   ante stakeholders sin entrar en stack ni
   topología.
4. **ADRs** que afectan integraciones externas
   (cambiar LDAP, agregar nueva fuente operativa) —
   discutir el cambio en su contexto antes de tocar
   niveles inferiores.

Cuándo crear o actualizar el diagrama Context
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Al inicio del proyecto (ya hecho).
- Cuando aparece o desaparece un **actor humano**
  (e.g., un nuevo rol de auditor externo).
- Cuando aparece o desaparece un **sistema
  externo** (e.g., reemplazo de LDAP por SSO
  corporativo, integración con un nuevo IVR).
- Cuando cambia la **misión del sistema** — raro,
  pero posible si el alcance del producto se
  redefine.

Política IACT
~~~~~~~~~~~~~

1. **Una sola caja** para IACT — no descomponer en
   este nivel. Si la audiencia necesita ver apps
   Django, pasar al nivel Component
   (§§ 1-9 de este documento).
2. **Etiquetas en lenguaje del dominio** — sin
   protocolos ni código.
3. **Mantener < 7 elementos** en total (actores +
   sistemas) — más de eso satura la vista a alto
   nivel.
4. **Coherencia con el modelo de dominio**
   (:doc:`analisis-dominio`) — los actores aquí son
   los mismos que aparecen en los UCs.
5. **Actualizar al README** del proyecto cuando
   cambie.

Próximos niveles
~~~~~~~~~~~~~~~~

- **C4 nivel 2 Container** → :doc:`diagramas-distribucion`
  detalla los nodos físicos y los protocolos.
- **C4 nivel 3 Component** → §§ 1-9 de este
  documento detallan las apps Django internas y sus
  interfaces.
- **C4 nivel 4 Code** → omitido en IACT (los
  diagramas de clases UML lo cubren naturalmente).

13.1 Construir el diagrama paso a paso — agregar nodos
------------------------------------------------------

La obra citada construye el Context incrementalmente:
primero un nodo (el actor humano), luego el sistema en
diseño, luego los sistemas de apoyo. PlantUML permite
seguir esa misma metodología, con la ventaja de que las
piezas se agregan en pocas líneas.

Convención de Simon Brown — tres líneas por nodo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cada nodo del diagrama Context contiene **tres
elementos** según la convención de Brown:

1. **Título** — nombre claro del nodo.
2. **Etiqueta** — el **tipo** del nodo entre corchetes
   (``[Person]``, ``[Software System]``, ``[External
   System]``).
3. **Descripción** — frase breve que describe qué
   representa el nodo.

A nivel Context la etiqueta ``[Software System]`` puede
parecer redundante, pero **mantenerla** asegura
**consistencia** entre los cuatro niveles del modelo
(en el nivel Component aparecen también ``[Container]``,
``[Component]``).

Sintaxis PlantUML para nodos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PlantUML soporta texto multilínea con ``\n`` o con
bloques explícitos. Para mantener legibilidad del
código fuente, preferir ``\n``:

.. code-block:: plantuml

   actor "Supervisor\n[Person]\n\nUsuario que monitorea\nllamadas y reportes" as Supervisor

O con sintaxis multilínea de PlantUML:

.. code-block:: plantuml

   rectangle "IACT\n[Software System]\n\nPlataforma de analitica\nde call center" as IACT

Equivalencia con Mermaid del libro:

.. list-table::
 :widths: 36 36 28
 :header-rows: 1

 * - Mermaid
   - PlantUML
   - Notas
 * - ``id["título\nlabel\ndescripción"]``
   - ``rectangle "título\n[label]\n\ndescripción" as id``
   - PlantUML separa con ``\n`` igual que Mermaid.
 * - ``flowchart TD``
   - Sin equivalente directo
     (PlantUML decide layout)
   - PlantUML respeta el orden de declaración y la
     dirección de las flechas.

Construcción incremental — IACT
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Paso 1**: declarar el primer actor.

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   title IACT — paso 1: actor

   actor "Supervisor\n[Person]\n\nMonitorea llamadas\ny reportes" as Supervisor
   @enduml

**Paso 2**: agregar el sistema en diseño.

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   title IACT — paso 2: actor + sistema

   actor "Supervisor\n[Person]\n\nMonitorea llamadas\ny reportes" as Supervisor

   rectangle "IACT\n[Software System]\n\nPlataforma de analitica\nde call center" as IACT
   @enduml

**Paso 3**: agregar sistemas externos.

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   title IACT — paso 3: con sistemas externos

   actor "Supervisor\n[Person]\n\nMonitorea llamadas\ny reportes" as Supervisor

   rectangle "IACT\n[Software System]\n\nPlataforma de analitica\nde call center" as IACT

   rectangle "LDAP corporativo\n[External System]\n\nDirectorio de usuarios" as LDAP
   rectangle "BD operativa\n[External System]\n\nDatos del call center\n(read-only)" as BDO
   rectangle "IVR-host\n[External System]\n\nEventos de telefonia\n(read-only)" as IVR
   @enduml

En este punto los nodos están aislados; el siguiente
paso (subsección siguiente) es **conectarlos** con
flechas etiquetadas.

ID corto vs título completo
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Como en Mermaid, conviene usar un **ID corto** (alias
PlantUML con ``as``) y reservar el texto largo para el
contenido visible. Esto evita repetir frases largas al
declarar las relaciones:

.. code-block:: plantuml

   ' Mejor:
   rectangle "Servicio de listados\n[Software System]" as LS
   Supervisor --> LS : consulta titulos

   ' Peor:
   "Servicio de listados\n[Software System]" --> ...

Política IACT para nodos del Context
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Tres elementos por nodo** — título + etiqueta
   ``[Person]`` / ``[Software System]`` /
   ``[External System]`` + descripción breve.
2. **Alias cortos con ``as``** — ``LDAP``, ``BDO``,
   ``IVR``, ``IACT``. Evita repetir el texto largo.
3. **Descripción de máximo 2-3 líneas** — el
   diagrama es Context, no documentación.
4. **Coherencia con el dominio** — los actores y
   nombres deben coincidir con :doc:`analisis-dominio`
   y los UCs (``Supervisor``, no
   ``UsuarioFinal``).
5. **Construcción incremental** — declarar los
   actores primero, el sistema después, los externos
   al final. Facilita la lectura del código fuente
   PlantUML y se alinea con la convención del
   capítulo.

13.2 Conectar los nodos
-----------------------

Una vez declarados los nodos (§ 13.1), el siguiente
paso es **conectarlos** con flechas etiquetadas que
indiquen la dependencia o interacción entre ellos.

Sintaxis PlantUML para flechas etiquetadas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PlantUML usa ``-->`` con la etiqueta separada por
``:``:

.. code-block:: plantuml

   Supervisor --> IACT : consulta dashboards,\nreconoce alertas

La sintaxis admite también:

- **Flecha derecha-izquierda**: ``A <-- B``.
- **Línea sin flecha**: ``A -- B``.
- **Línea punteada**: ``A ..> B`` (útil para
  dependencias suaves).
- **Forzar dirección**: ``A -down-> B``,
  ``A -right-> B`` para dirigir el layout.

Equivalencia con Mermaid del libro:

.. list-table::
 :widths: 36 36 28
 :header-rows: 1

 * - Mermaid
   - PlantUML
   - Notas
 * - ``A-- "etiqueta" -->B``
   - ``A --> B : etiqueta``
   - PlantUML usa ``:`` en lugar de comillas.
 * - ``A-->|"etiqueta"|B``
   - ``A --> B : etiqueta``
   - Equivalente directo.

Convención IACT — etiquetas como dependencias
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Como recomienda el libro, en un Context las flechas
modelan **dependencias**: el nodo padre depende de
algo del nodo hijo. La etiqueta describe **qué**
necesita el padre del hijo, no el protocolo ni los
detalles técnicos.

Buenas etiquetas IACT:

- ``consulta dashboards``
- ``autentica usuarios``
- ``lee datos del call center``
- ``recibe eventos del IVR``

Etiquetas a evitar en Context:

- ``HTTPS GET /reportes/04`` (protocolo, no
  Context).
- ``ldap://...`` (URL, no Context).
- ``query analytics_db.sql`` (detalle de
  implementación).

Construcción incremental — IACT (continuación)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Paso 4**: conectar el actor con el sistema en
diseño.

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   title IACT — paso 4: actor conectado al sistema

   actor "Supervisor\n[Person]" as Supervisor
   rectangle "IACT\n[Software System]" as IACT

   Supervisor --> IACT : consulta dashboards,\nreconoce alertas
   @enduml

**Paso 5**: agregar las dependencias del sistema en
diseño hacia los sistemas externos.

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   title IACT — paso 5: con sistemas externos conectados

   actor "Supervisor\n[Person]" as Supervisor
   actor "Auditor\n[Person]" as Auditor
   actor "Operador ETL\n[Person]" as OETL

   rectangle "IACT\n[Software System]\n\nPlataforma de analitica\nde call center" as IACT

   rectangle "LDAP corporativo\n[External System]" as LDAP
   rectangle "BD operativa\n[External System]" as BDO
   rectangle "IVR-host\n[External System]" as IVR

   Supervisor --> IACT : consulta dashboards,\nreconoce alertas
   Auditor --> IACT : consulta auditoria,\nverifica SoD
   OETL --> IACT : monitorea ventana ETL

   IACT --> LDAP : autentica usuarios
   IACT --> BDO : lee datos del call center\n(read-only)
   IACT --> IVR : recibe eventos del IVR\n(read-only)
   @enduml

Resultado: el Context diagram completo, equivalente a
la imagen final de la sección "Vista Context de IACT"
de § 13. Cualquier colega técnico o no técnico puede
leerlo y entender quién usa IACT, qué hace y con qué
sistemas dialoga.

Enlaces en nodos del flowchart
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Como en los diagramas de clases (§ 16.8 de
:doc:`analisis-dominio`), los nodos del Context pueden
llevar enlaces externos. PlantUML usa ``[[url]]``:

.. code-block:: plantuml

   rectangle "LDAP corporativo\n[External System]" as LDAP [[https://corp.example/ldap-docs]]

Pero la política IACT (§ 16.8 de
:doc:`analisis-dominio`) prefiere mantener las
referencias en el **texto RST adyacente** con
``:doc:`` / ``:ref:``, donde Sphinx valida los
destinos. ``[[url]]`` se reserva para URLs externas
persistentes (RFCs, especificaciones oficiales).

Política IACT para conexiones del Context
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Toda conexión etiquetada** — sin etiqueta el
   diagrama miente sobre la naturaleza de la
   dependencia.
2. **Etiqueta en lenguaje del dominio** — verbos del
   ubiquitous language (consulta, autentica, lee,
   recibe).
3. **Conexiones desde el padre al hijo** — el padre
   depende del hijo. Si la dependencia es mutua,
   modelar dos flechas o usar ``--`` (sin dirección)
   con justificación.
4. **Sin protocolos** en este nivel — pertenecen a
   Container.
5. **Forzar dirección** (``-down->``, ``-right->``)
   solo cuando el layout automático produce cruces.

----

Trazabilidad
============

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Skill principal**
   - ``rm-specification``
 * - **Skill complementario**
   - ``rm-analysis``
 * - **Diagramas hermanos**
   - :doc:`diagramas-secuencias`,
     :doc:`diagramas-colaboraciones`,
     :doc:`diagramas-actividades`
 * - **Stack canónico**
   - ADR_DEVOPS_001 (Vagrant + Apache + mod_wsgi + Django
     + MySQL + Redis)
 * - **Política de diagramación**
   - :doc:`/base-cognitiva/plantuml-guide/guidelines`
 * - **Teoría UML**
   - :doc:`/base-cognitiva/_uml/index`
