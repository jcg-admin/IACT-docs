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
