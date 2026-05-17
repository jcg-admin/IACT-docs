.. meta::
 :artefacto: STD_010
 :tipo: Estándar
 :dominio: normativa
 :subdominio: estandares
 :estado: Aprobado
 :version: 1.3.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Interno

.. _std-010:

==========================================================
STD_010: Vocabulario Abstracto en Narrativa de Requisitos
==========================================================

.. contents:: Contenido
 :depth: 3
 :local:

----

1. Propósito
============

Este estándar define el vocabulario canónico para la narrativa de
requisitos del proyecto IACT. Los documentos de requisitos
(``source/requisitos/``) deben describir el sistema en términos de
**rol** y**responsabilidad**, no en términos de tecnología de
implementación.

**Regla central:**

  Los documentos de requisitos describen **LO QUE HACE** el sistema,
  no **CÓMO LO IMPLEMENTA**. Los nombres de bibliotecas, frameworks,
  algoritmos concretos y excepciones de lenguaje pertenecen a
  ``implementacion-tecnica.rst`` y a ``source/arquitectura-tecnica/``.

----

2. Ámbito de Aplicación
=======================

2.1 Tabla de archivos
---------------------

+----------------------------------------------+--------------------------+
| Archivos                                     | Aplica                   |
+==============================================+==========================+
| flujo-principal.rst                          | Sí                       |
+----------------------------------------------+--------------------------+
| actores-precondiciones.rst                   | Sí                       |
+----------------------------------------------+--------------------------+
| criterios-aceptacion.rst                     | Sí                       |
+----------------------------------------------+--------------------------+
| datos-involucrados.rst                       | Sí                       |
+----------------------------------------------+--------------------------+
| informacion-general.rst                      | Sí                       |
+----------------------------------------------+--------------------------+
| patrones-diseno.rst                          | Sí                       |
+----------------------------------------------+--------------------------+
| requisitos-no-funcionales.rst                | Sí                       |
+----------------------------------------------+--------------------------+
| excepciones.rst                              | Sí                       |
+----------------------------------------------+--------------------------+
| diagramas-uml.rst (participantes)            | Sí                       |
+----------------------------------------------+--------------------------+
| source/requisitos/reglas-negocio/**          | Sí                       |
+----------------------------------------------+--------------------------+
| source/base-cognitiva/**                     | Sí (vocabulario)         |
+----------------------------------------------+--------------------------+
| source/index.rst (raíz)                      | Por contenido (§2.2)     |
+----------------------------------------------+--------------------------+
| implementacion-tecnica.rst                   | No — libre               |
+----------------------------------------------+--------------------------+
| source/arquitectura-tecnica/**               | No — libre               |
+----------------------------------------------+--------------------------+
| source/backend/**                            | No — libre               |
+----------------------------------------------+--------------------------+
| source/requisitos/_metodologia-aplicacion/** | No — exenta (§2.3)       |
+----------------------------------------------+--------------------------+
| source/base-cognitiva/_metadata/**           | No — exenta (§2.5.1)     |
+----------------------------------------------+--------------------------+
| ``casos-uso/**/testing.rst``                 | No — exenta (§2.5.3)     |
+----------------------------------------------+--------------------------+
| source/normativa/procedimientos/**           | No — exenta (§2.5.4)     |
+----------------------------------------------+--------------------------+
| source/normativa/gobernanza/adr-\*           | No — exenta (§2.5.5)     |
+----------------------------------------------+--------------------------+
| source/normativa/estandares/plantillas/**    | No — exenta (§2.5.6)     |
+----------------------------------------------+--------------------------+
| source/gestion/evidencia/arquitectura-modular/** | No — exenta (§2.5.7) |
+--------------------------------------------------+----------------------+

2.2 ``index.rst`` raíz — aplicación por contenido
-------------------------------------------------

El archivo ``source/index.rst`` puede contener tanto narrativa
de presentación arquitectónica del sistema como navegación
de índice. La aplicación de STD-010 a este archivo es **por
contenido**, no por nombre:

- Si una sección describe **comportamiento o capacidades del
  sistema IACT** (vocabulario controlado por el proyecto):
  aplica STD-010.
- Si una sección describe **hechos arquitectónicos del
  entorno del cliente** (ver §2.4) o es solo navegación de
  toctree: exenta.

Cuando se mezclan ambos casos en el mismo archivo, marcar
explícitamente la sección exenta con un comentario RST.

2.3 ``_metodologia-aplicacion/`` — exenta
-----------------------------------------

El directorio ``source/requisitos/_metodologia-aplicacion/``
contiene documentación **de proceso de trabajo del proyecto**
(plantillas, guías, patrones de aplicación de la metodología,
ejemplos pedagógicos). No es especificación del sistema IACT.

Aplicar STD-010 a documentación sobre cómo trabajar sería un
error de categoría: el vocabulario canónico controla cómo
describimos el sistema, no cómo describimos nuestro proceso.

Esta exención queda formalmente establecida en v1.1.0 tras
detección en WP ``clean-code-naming-audit``.

2.4 Nombres propios de sistemas externos — exentos
--------------------------------------------------

Los sistemas externos del cliente del que IACT consume datos
o con el que se integra (sistema IVR del cliente, sistemas
operacionales heredados, brokers de mensajería del entorno)
tienen **nombres propios reales**. Estos nombres no son
reemplazables por vocabulario canónico porque la abstracción
oculta información factual relevante para el lector.

Ejemplo legítimo:

  "El sistema IVR del cliente usa MySQL como base de datos
  operacional, modo solo-lectura para IACT."

El término ``MySQL`` aquí describe un hecho arquitectónico
del sistema externo (no del comportamiento de IACT). Es
informativo y no puede ser reemplazado por "el repositorio
operacional" sin pérdida.

**Criterio de aplicación:**

- Si la tecnología describe comportamiento del sistema IACT
  (lo que el proyecto controla): aplica STD-010 con
  vocabulario canónico.
- Si la tecnología describe un sistema externo factual del
  entorno del cliente: exento.

Esta exención queda formalmente establecida en v1.1.0.

2.5 Archivos de identidad y técnicos análogos a §5.1
----------------------------------------------------

Tres categorías adicionales de archivos quedan exentas porque
aplicar STD-010 sobre ellos genera **circularidad semántica**:
el archivo existe precisamente para comunicar la información
que el vocabulario canónico abstrae.

2.5.1 Identity files — declaración del stack del proyecto
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Archivos cuyo propósito documental es **declarar la identidad
tecnológica del proyecto** — qué tecnologías concretas se
adoptan como Backend, Frontend, Base de Datos, Cache,
Mensajería, etc. Aplicar STD-010 a estos archivos produce
absurdo: el archivo declara qué tecnología ES el rol abstracto.

::

   ✓ EXENTO:  "Backend: Django REST Framework (Python 3.11+)"
   ✗ ABSURDO: "Backend: el Framework de Aplicación"

Archivos exentos:

- ``source/base-cognitiva/_metadata/meta-01-identidad-proyecto.rst``
- ``source/base-cognitiva/_metadata/meta-05-estructura-documental.rst``

**Criterio de aplicación:**

Cualquier archivo cuyo propósito documental sea **identidad
del proyecto** (no narrativa de requisitos, no diseño
operacional, no análisis de proceso, no decisión arquitectónica
de un caso de uso). En la práctica, todo el directorio
``source/base-cognitiva/_metadata/`` cae bajo este criterio.

2.5.2 Landing page arquitectónica — ``source/index.rst``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``source/index.rst`` raíz ya tenía tratamiento "por contenido"
en §2.2. Esta cláusula clarifica que la **sección de presentación
arquitectónica** (párrafos de bienvenida que contextualizan el
sistema con su stack tecnológico para nuevos lectores) opera
bajo el mismo criterio que identity files: declarar el stack
es el propósito documental, no abstraerlo.

Aplica a:

- Párrafos introductorios de ``source/index.rst`` que presentan
  el sistema y nombran su stack tecnológico para orientación
  inicial del lector.
- Bullet lists de stack en la sección "Características" o
  análoga.

NO aplica a:

- Toctree y navegación (ya cubierto por §2.2).
- Cualquier prosa de requisitos, decisiones o análisis dentro
  del mismo archivo que no sea la presentación arquitectónica
  de aterrizaje.

2.5.3 Testing files — paralelo de §5.1
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Los archivos ``casos-uso/**/testing.rst`` documentan
infraestructura de tests: configuración de fixtures,
``factory_boy``, ``pytest``, herramientas de coverage. Son
análogos a ``implementacion-tecnica.rst`` (§5.1 ya exento)
pero la tabla §2.1 v1.0.0 no los listaba explícitamente.

Esta cláusula clarifica que ``testing.rst`` es **explícitamente
exento por la misma razón** que ``implementacion-tecnica.rst``:
el archivo es técnico por propósito documental — describe cómo
se prueba el sistema, no qué hace el sistema desde la
perspectiva del requisito.

Archivos exentos:

- ``source/requisitos/casos-uso/**/testing.rst``

Esta exención queda formalmente establecida en v1.2.0 tras
detección en WP ``2026-05-08-03-08-21-wpg-std010-cleanup``
(WP-G).

2.5.4 Procedimientos operativos — instrucciones ejecutables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Archivos en ``source/normativa/procedimientos/`` documentan
procesos operativos del proyecto: DevOps automation, gobernanza
SDLC, generación de artefactos, despliegue, seguridad, QA. Son
**instrucciones ejecutables** que requieren nombres tecnológicos
concretos para ser ejecutables.

::

   ✓ EXENTO:  "Configurar el job de CI con
              ``runs-on: ubuntu-latest`` ejecutando
              ``pytest --django-settings=...``"
   ✗ ABSURDO: "el Procesador Asíncrono ejecutando el
              Framework de Tests con configuración del
              Framework de Aplicación"

El propósito documental del procedimiento es ser **ejecutable
literalmente** por el operador; abstraer las herramientas
elimina la utilidad operativa del documento.

NO aplica:

- Las decisiones de fondo dentro del procedimiento que se
  describen como conceptos arquitectónicos siguen STD-010
  cuando son narrativa de requisitos (no instrucción
  ejecutable).

2.5.5 ADRs (Architecture Decision Records)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Archivos ``source/normativa/gobernanza/adr-*.rst`` y
``source/arquitectura-tecnica/modulos/*/decisiones/adr-*.rst``
registran **decisiones tecnológicas documentadas**: por qué se
eligió X tecnología vs alternativa Y, con sus trade-offs. El
propósito del ADR es **nombrar explícitamente la tecnología
elegida y la descartada** — abstraer elimina la decisión.

::

   ✓ EXENTO:  "Decisión: usar PostgreSQL para ``audit_log``,
              no MySQL, porque PostgreSQL soporta CHECK
              constraints sobre row immutability y MySQL no
              lo hace consistentemente."
   ✗ ABSURDO: "Decisión: usar el Almacén de Datos analítico
              en vez del Repositorio operativo, porque uno
              soporta constraints y el otro no"
              (la decisión pierde su trazabilidad: ¿cuál era
              la alternativa real?)

Aplica al árbol completo de ADRs en
``source/normativa/gobernanza/adr-*`` y a los ADRs anidados
bajo ``source/arquitectura-tecnica/modulos/*/decisiones/``.

2.5.6 Plantillas técnicas con ejemplos concretos
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Archivos en ``source/normativa/estandares/plantillas/**``
proveen **plantillas con ejemplos concretos** que el usuario
copia y rellena. Los ejemplos requieren nombres tecnológicos
para ilustrar el patrón correctamente.

::

   ✓ EXENTO:  Plantilla ``tpl-uc-larman-contratos.rst``:
              "Stack: Django REST Framework + PostgreSQL,
               Cache Redis (TTL 300s)"
   ✗ ABSURDO: Plantilla con stack abstracto que el usuario
              tendría que re-abstraer en cada uso (los
              ejemplos pierden su valor pedagógico).

El usuario que rellena la plantilla copia el patrón concreto;
abstraer los ejemplos lo deja sin guía.

2.5.7 Análisis de arquitectura modular
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Archivos en ``source/gestion/evidencia/arquitectura-modular/**``
son **evidencia de análisis arquitectónico real** del sistema:
documentan qué tecnologías se eligieron, cómo se modularizó el
código, qué librerías se importaron en cada módulo. Tienen el
mismo carácter que identity files (§2.5.1) pero a granularidad
de módulo.

Aplicar STD-010 a un análisis de cómo está modularizado el
backend Django destruye la información factual: el análisis
existe precisamente para describir el stack real adoptado.

Estas exenciones (§2.5.4 — §2.5.7) quedan formalmente
establecidas en v1.3.0 tras decisión TD-D6 que cierra el
roadmap de remediación CLEAN_CODE iniciado en WP
``clean-code-naming-audit``.

----

3. Tabla de Vocabulario Canónico
=================================

Cada nombre tecnológico concreto tiene su equivalente semántico.
Usar el término canónico en toda la narrativa de requisitos.

3.1 Infraestructura y Servidor
-------------------------------

.. list-table::
 :widths: 35 40 25
 :header-rows: 1

 * - Término Tecnológico (PROHIBIDO)
   - Término Canónico (CORRECTO)
   - Contexto
 * - ``Apache 2.4``
   - el servidor web
   - en narrativa de flujo
 * - ``Apache + mod_wsgi``
   - el Servidor de Aplicacion
   - en arquitectura abstracta
 * - ``mod_wsgi``
   - el Servicio de Aplicacion
   - en narrativa de requisito
 * - ``nginx``
   - el servidor web
   - (no aplicable — IACT usa Apache)
 * - ``gunicorn``
   - el servidor web
   - (no aplicable — IACT usa mod_wsgi)
 * - ``Vagrant``
   - el entorno de despliegue
   - en narrativa de requisito

3.2 Base de Datos
-----------------

.. list-table::
 :widths: 35 40 25
 :header-rows: 1

 * - Término Tecnológico (PROHIBIDO)
   - Término Canónico (CORRECTO)
   - Contexto
 * - ``MySQL``
   - el repositorio / la base de datos
   - en narrativa de flujo
 * - ``MariaDB``
   - el repositorio / el Almacen de Datos
   - en narrativa (libre en arch-tecnica)
 * - ``PostgreSQL``
   - el repositorio operacional
   - en narrativa de requisito
 * - ``Redis``
   - el servicio de cache / la cache de sesiones
   - en narrativa de requisito
 * - ``OperationalError``
   - error del repositorio
   - en manejo de excepciones
 * - ``IntegrityError``
   - error de integridad de datos
   - en manejo de excepciones

3.3 Autenticación y Seguridad
------------------------------

.. list-table::
 :widths: 35 40 25
 :header-rows: 1

 * - Término Tecnológico (PROHIBIDO)
   - Término Canónico (CORRECTO)
   - Contexto
 * - ``bcrypt``
   - el algoritmo de hash seguro de contraseñas
   - en flujo de autenticación
 * - ``bcrypt.checkpw()``
   - verifyHash()
   - en pseudocódigo / diagramas
 * - ``bcrypt.hashpw()``
   - generateHash()
   - en pseudocódigo / diagramas
 * - ``bcrypt cost N``
   - costo de hash configurado
   - en criterios de rendimiento
 * - ``PBKDF2``
   - el algoritmo de derivación de clave
   - en narrativa de seguridad
 * - ``argon2``
   - el algoritmo de hash seguro
   - en narrativa de seguridad
 * - ``simplejwt``
   - el Servicio de Autenticacion
   - en flujo de tokens
 * - ``djangorestframework-simplejwt``
   - el Servicio de Tokens JWT
   - en narrativa de dependencias
 * - ``JWT``
   - el token de sesion
   - permitido (es vocabulario de dominio)
 * - ``secrets.token_urlsafe(32)``
   - el generador criptograficamente seguro
   - en narrativa de generación

3.4 Frontend y UI
-----------------

.. list-table::
 :widths: 35 40 25
 :header-rows: 1

 * - Término Tecnológico (PROHIBIDO)
   - Término Canónico (CORRECTO)
   - Contexto
 * - ``React``
   - la Interfaz de Usuario
   - en participantes de secuencia
 * - ``React 18``
   - el Framework de Interfaz
   - en narrativa de dependencias
 * - ``Frontend (React)``
   - Interfaz de Usuario
   - en diagramas y descripciones
 * - ``Redux Toolkit``
   - el Gestor de Estado
   - en narrativa
 * - ``React Router``
   - el Enrutador de Interfaz
   - en narrativa
 * - ``Vue.js``
   - el Framework de Interfaz
   - en narrativa

3.5 Procesamiento Asíncrono
----------------------------

.. list-table::
 :widths: 35 40 25
 :header-rows: 1

 * - Término Tecnológico (PROHIBIDO)
   - Término Canónico (CORRECTO)
   - Contexto
 * - ``Celery``
   - el Procesador Asincrono
   - en narrativa de flujo
 * - ``RabbitMQ``
   - el Broker de Mensajes
   - en narrativa
 * - ``APScheduler``
   - el Planificador de Tareas
   - en narrativa
 * - ``Cron``
   - el Planificador de Tareas
   - en narrativa (libre en arch-tecnica)

3.6 Bibliotecas de Utilidad
----------------------------

.. list-table::
 :widths: 35 40 25
 :header-rows: 1

 * - Término Tecnológico (PROHIBIDO)
   - Término Canónico (CORRECTO)
   - Contexto
 * - ``Pillow``
   - la libreria de procesamiento de imagenes
   - en narrativa
 * - ``openpyxl`` / ``xlrd``
   - la libreria de exportacion Excel
   - en narrativa
 * - ``pandas``
   - la libreria de procesamiento de datos
   - en narrativa

----

4. Regla de Diagramas UML
==========================

En los diagramas PlantUML dentro de la narrativa de requisitos
(``diagramas-uml.rst``), los participantes siguen los mismos
principios de abstracción:

**Participantes de secuencia:**

.. code-block:: text

   ' CORRECTO
   participant "Interfaz de Acceso" as Iface
   participant "Servicio de Autenticacion" as Svc
   database "Almacen de Datos" as Store

   ' PROHIBIDO
   participant "Frontend\n(React)" as F
   participant "Django API" as API
   database "MariaDB" as DB

**Actores:** Los actores SÍ usan el nombre exacto de la función RBAC
del catálogo (D-DIAG-001). No son nombres institucionales.

.. code-block:: text

   ' CORRECTO
   actor "view_reports" as view_reports
   actor "assign_functions" as assign_functions

   ' PROHIBIDO
   actor "Analista de Datos" as U
   actor "Administrador" as A

----

5. Excepciones Documentadas
============================

Las siguientes situaciones permiten el uso de nombres tecnológicos
o acronimos en documentos donde STD-010 aplica:

5.1 ``implementacion-tecnica.rst``
-----------------------------------

Este archivo es explícitamente técnico. Puede y debe referenciar
tecnologías concretas: Apache, bcrypt, Django versión, mod_wsgi, etc.

5.2 Identificadores de datos concretos
---------------------------------------

Los identificadores de tablas/campos específicos que son parte del
contrato de datos son permitidos cuando el documento los necesita para
precisión:

- ``pipeline_runs.estado`` — nombre de campo de tabla real
- ``sp_etl_maestro`` — nombre de stored procedure (vocabulario de dominio)
- ``tbl_historico_tN_YYYY`` — nombre de tabla fuente (vocabulario de dominio)

5.3 Criterios de rendimiento con algoritmo específico
------------------------------------------------------

Cuando el criterio de rendimiento es específico al algoritmo (e.g.,
"P50 ≤ 250 ms incluyendo verificación de hash"), se puede mencionar
el algoritmo en una nota técnica dentro de ``implementacion-tecnica.rst``,
pero el criterio en ``requisitos-no-funcionales.rst`` usa el término
canónico.

5.4 Acronimos de disciplina aceptados en prosa
-----------------------------------------------

Algunos acrónimos son **vocabulario establecido de la disciplina**
de seguridad informática y arquitectura, equivalentes a JWT
(STD-010 §3.3) que ya estaba documentado como aceptable. Su
uso en prosa explicativa es legítimo y no constituye
violación.

**Acrónimo aceptado: RBAC (Role-Based Access Control)**

  RBAC como término disciplinar es aceptado en prosa
  explicativa de documentos normativos y arquitectónicos
  cuando se usa para referirse al modelo de control de
  acceso basado en roles **como concepto de la disciplina**,
  no como identificador técnico del proyecto.

**Aplica a:**

- Prosa explicativa: "el modelo RBAC del sistema",
  "la matriz RBAC", "RBAC v5.6.x" como referencia a la
  versión del modelo.
- Cross-refs y nombres de directorios: ``rbac/``,
  ``modelo-rbac-iact``.
- Referencias en headers, títulos y captions cuando se
  alude al concepto disciplinar.

**NO aplica (sigue siendo violación):**

- ``RBAC_check`` como nombre de método o variable —
  reemplazar por ``permission_check``.
- ``RBACBackend``, ``RBACPermission`` como nombre de clase
  — viola CLEAN_CODE §6.2 (sufijos técnicos del framework)
  además del uso de acrónimo. Reemplazar por
  ``AuthProvider``, ``AccessPolicy``.
- ``RBAC_id``, ``rbac_data`` como nombre de variable.
- ``RBAC-gated`` como atributo de UC — preferir
  "controlado por permisos" o "requiere capability".

**Criterio de distinción:**

- Si el lector entiende que se está hablando del concepto
  disciplinar de control de acceso por roles: prosa
  aceptable.
- Si el lector tendría que mirar el código/clase para
  saber qué identifica: violación, requiere expansión
  o reemplazo.

5.5 Identificadores opacos con dependencias externas
----------------------------------------------------

Por extensión del principio de §5.2 al dominio de RBAC:

- Tokens de capability del backend: ``access:view_sod``,
  ``access:update_sod``, ``access:disable_sod`` —
  contrato de integración persistido en backend.
- Códigos de regla en BD: ``SOD-001``, ``SOD-002``,
  ``SOD-003``, ``AGR-001..010`` — IDs persistidos en
  ``SeparationRule.code`` y catálogo RBAC.

Cambiarlos requiere migración de datos coordinada con
backend y BD. Hasta que esa migración ocurra, son
referencias factuales al estado actual del sistema y se
preservan tal cual.

----

6. Validación
=============

Antes de aprobar un documento de requisitos, verificar:

.. code-block:: bash

 # Buscar violaciones de vocabulario en narrativa UC
 grep -rl "bcrypt\|React\|MySQL\|Celery\|mod_wsgi\|simplejwt\|OperationalError\|Pillow" \
   source/requisitos/casos-uso/ \
   --include="*.rst" \
   --exclude="implementacion-tecnica.rst"

Un resultado vacío indica que la narrativa está conforme al estándar.

----

7. Relación con otros estándares
=================================

- **STD_002** — Nomenclatura del proyecto: define IDs y códigos de módulo
- **STD_007** — Convención de naming: kebab-case en archivos y directorios
- **STD_009** — Profesionalismo en documentación: prosa formal sin emojis
- **D-ETL-005** (WP source-corrections-pipeline): decisión original del
  principio de abstracción de vocabulario ("soda machine rule")
- **D-KRUCHTEN-004** (WP kruchten-view-diagram-types): aplicación del
  principio a participantes de diagramas de vistas Kruchten

Véase también: :doc:`clean-code-naming-principles` y
:doc:`clean-code-naming-principles-frontend` para la aplicación
de este vocabulario en identificadores de código (mientras
STD-010 rige la narrativa de requisitos, las normas Clean Code
rigen los nombres de clase, método, atributo y variable).

----

8. Historial de Cambios
=======================

.. list-table::
 :widths: 12 12 20 56
 :header-rows: 1

 * - Versión
   - Fecha
   - Autor
   - Cambios
 * - 1.0.0
   - 2026-05-04
   - NestorMonroy
   - Versión inicial — formaliza D-ETL-005 como estándar normativo
 * - 1.1.0
   - 2026-05-08
   - NestorMonroy
   - MINOR — amplia ámbito (§2.1 con metodología exenta,
     §2.2 index.rst por contenido, §2.3 _metodologia-aplicacion
     exenta, §2.4 sistemas externos exentos por nombre propio).
     Agrega §5.4 RBAC como acrónimo disciplinar aceptado en
     prosa con criterio explícito. Agrega §5.5 identificadores
     opacos con dependencias externas (tokens RBAC backend +
     códigos BD). Resoluciones D2 y D4 del WP
     ``naming-rules-resolution``.
 * - 1.2.0
   - 2026-05-08
   - NestorMonroy
   - MINOR — agrega §2.5 con tres exenciones por circularidad
     semántica: §2.5.1 identity files (``_metadata/meta-01``,
     ``meta-05``), §2.5.2 landing arquitectónica de
     ``source/index.rst``, §2.5.3 testing files paralelos a
     §5.1. Tabla §2.1 actualizada con dos filas adicionales.
     Cubre 21 referencias diferidas en WP-G
     ``2026-05-08-03-08-21-wpg-std010-cleanup``. TD-D5.
 * - 1.3.0
   - 2026-05-08
   - NestorMonroy
   - MINOR — extiende §2.5 con cuatro exenciones adicionales:
     §2.5.4 procedimientos operativos (instrucciones
     ejecutables), §2.5.5 ADRs (decisiones tecnológicas con
     trade-offs), §2.5.6 plantillas técnicas con ejemplos
     concretos, §2.5.7 análisis de arquitectura modular.
     Tabla §2.1 actualizada con cuatro filas adicionales.
     Cubre 230 referencias diferidas tras TD-D5; cierra el
     roadmap de remediación CLEAN_CODE sin deuda activa
     pendiente. TD-D6.
