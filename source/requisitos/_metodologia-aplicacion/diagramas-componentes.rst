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
