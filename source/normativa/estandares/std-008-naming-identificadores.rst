.. meta::
 :artefacto: STD_008
 :tipo: Estándar
 :dominio: normativa
 :subdominio: estandares
 :estado: Aprobado
 :version: 1.3.0
 :fecha_creacion: 2026-04-28
 :ultimo_cambio: 2026-05-06
 :autor: Equipo IACT
 :clasificacion: Interno

.. _std-008:

==============================================
STD_008: Naming de Identificadores Técnicos
==============================================

.. contents:: Contenido
 :depth: 3
 :local:

----

1. Propósito
============

Establecer los principios obligatorios para nombrar **identificadores
técnicos** del proyecto IACT: funciones, métodos, clases, variables,
constantes, parámetros y tipos. Aplica a todo código generado en
cualquier tier (backend Django REST Framework, frontend React,
scripts de operations, esquemas de bases de datos, etc.) y a la
documentación que cita esos identificadores.

Este estándar **NO sustituye** a STD_007 (que rige naming de
archivos y directorios) ni a STD_002 (nomenclatura general del
proyecto). Es complementario y aplica al nivel de identificadores
dentro del código.

----

2. Alcance
==========

Aplica a:

- Nombres de funciones y métodos en cualquier lenguaje del stack.
- Nombres de clases, interfaces, tipos, traits.
- Nombres de variables locales, atributos de instancia, propiedades.
- Nombres de constantes y parámetros.
- Nombres de columnas y tablas en bases de datos cuando son
  consumidos por el código del proyecto.
- Identificadores citados en la documentación (RST) en bloques
  ``code-block``, ``literal``, ``code:`` y similares.

NO aplica a:

- Nombres de archivos y directorios (rige STD_007).
- IDs de artefactos de documentación: UC-001, BR-001, FND-01, etc.
  (rigen STD_002 y STD_007 §4).

----

3. Principios
=============

3.1 Clean Code Obligatorio
---------------------------

Todo identificador del proyecto sigue las reglas establecidas en
"Clean Code" (Robert C. Martin). Específicamente, los identificadores
deben:

- Revelar intención.
- Evitar desinformación.
- Hacer distinciones significativas.
- Pronunciarse y buscarse fácilmente.
- Evitar codificaciones innecesarias.

3.2 Autoexplicativo
-------------------

**Regla obligatoria:** un identificador debe poder leerse y
comprenderse **sin necesidad de conocer el dominio interno** del
módulo donde aparece.

Si un lector con formación técnica general (sin contexto del
módulo) no puede deducir qué hace una función a partir de su
nombre, el nombre **viola este estándar**.

Ejemplos:

.. list-table::
 :header-rows: 1
 :widths: 35 35 30

 * - Correcto
   - Por qué
   - Incorrecto (anti-patrón)
 * - ``getUserPermissions(userId)``
   - El verbo y el sustantivo describen la operación.
   - ``proc(uid)`` (abreviaturas crípticas, no se entiende qué
     hace)
 * - ``isReportExpired(report)``
   - Predicado claro: "el reporte está expirado".
   - ``check(r)`` (no dice qué se chequea)
 * - ``calculateTotalPrice(items, taxRate)``
   - Operación + objeto + cómo.
   - ``calc(x, y)`` (parámetros sin contexto)

3.3 Sin Abreviaturas de Dominio en Identificadores
---------------------------------------------------

**Regla obligatoria:** las abreviaturas de dominio de negocio o
de framework (``ETL``, ``PII``, ``KPI``, ``RTM``, ``SAML``,
etc.) **NO deben aparecer en identificadores técnicos**.
Las abreviaturas pueden usarse en narrativa (texto explicativo)
**solo cuando estén definidas previamente en el glosario del
proyecto**.

La razón: una abreviatura en un identificador obliga al lector a
conocer el dominio del cual proviene la abreviatura para entender
qué hace el código. Esto es un acoplamiento de conocimiento
implícito que rompe el principio de autoexplicativo (sección 3.2).

Ejemplos:

.. list-table::
 :header-rows: 1
 :widths: 30 35 35

 * - Operación
   - Identificador correcto
   - Identificador incorrecto
 * - Validar identificadores PII
   - ``validatePersonalDataIdentifier(...)``
   - ``validatePII(...)`` (PII es abreviatura de dominio)
 * - Procesar datos del pipeline ETL
   - ``processIncomingData(...)``
   - ``runETL(...)`` (ETL es jerga sin contexto en el
     identificador)
 * - Emitir métrica de KPI
   - ``recordPerformanceMetric(...)``
   - ``emitKPI(...)``
 * - Construir matriz de trazabilidad
   - ``buildTraceabilityMatrix(...)``
   - ``buildRTM(...)``

**Excepción:** los identificadores que **son** el nombre canónico
de un concepto del lenguaje o framework (no del dominio del
producto) sí pueden usar abreviaturas estándar de la industria.
Ejemplos válidos: ``URL``, ``HTTP``, ``HTML``, ``JSON``, ``SQL``,
``UUID``, ``UTF8``. Estas son abreviaturas universales en
ingeniería de software, no de dominio del producto.

3.4 Universal Antes Que Específico
-----------------------------------

Cuando dos nombres son válidos — uno universal y uno específico
del dominio — preferir el **universal**. La especificidad puede
expresarse en el contexto del módulo, no en el nombre del
identificador.

Ejemplo:

- ``hasPermission(permission)`` OK (universal)
- ``hasIACTPermission(permission)`` NO (acoplamiento al producto en
  el nombre).

3.5 Coherencia de Idioma — Identifiers SIEMPRE en Inglés
---------------------------------------------------------

Los identificadores técnicos del proyecto IACT se escriben en
**inglés**, sin excepción. Esto incluye:

- Funciones, métodos, clases, atributos, variables, constantes.
- Nombres de tablas y columnas en PostgreSQL (modelos Django).
- Endpoints REST.
- Eventos, mensajes y nombres de logs estructurados.
- **Ejemplos de código en cualquier artefacto** (lecciones,
  tutoriales, ADRs, ERDs, diagramas de clase), incluyendo
  zonas didácticas y normativa metodológica.

La narrativa de la documentación puede ser en español
(títulos, párrafos explicativos, notas, captions); los
identificadores citados en ella mantienen el inglés.

3.5.1 Sin excepciones por zona
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Esta regla aplica universalmente. **NO existen excepciones**
por zona, prefijo de path o naturaleza del artefacto:

- Lecciones siguiendo Schmuller u otros libros con ejemplos
  en español → traducir los identifiers al inglés. La narrativa
  puede mantenerse en español.
- ADRs descriptivos de código legacy → si el legacy usa
  identifiers en español, el ADR debe documentar
  explícitamente que ese naming **viola** este estándar y
  proponer plan de migración. NO se cita como modelo a seguir.
- Diagramas ERD, UML class, sequence, state, activity →
  identifiers en inglés en TODOS los archivos, incluso
  ejemplos pedagógicos.

3.5.2 Justificación
~~~~~~~~~~~~~~~~~~~

Permitir identifiers en español en zonas didácticas envía un
mensaje implícito incorrecto al lector: "es aceptable nombrar
clases/atributos/funciones en español". Esa interpretación
contradice STD-008 §3.1 (Clean Code obligatorio) y degrada
la consistencia del corpus.

Mantener la narrativa en español preserva el valor pedagógico
para lectores hispanohablantes; traducir identifiers al inglés
preserva el modelo correcto del estándar.

3.5.3 Comentarios y narrativa — español permitido
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Los siguientes elementos **pueden** estar en español:

- Comentarios de código (``# explicacion``, ``// nota``,
  ``-- descripcion``).
- Strings de UI (mensajes al usuario final).
- Captions de figuras y diagramas.
- Texto narrativo de la documentación (RST prosa).
- Nombres de archivos y directorios cuando STD-007 lo
  permite (e.g. paths de capítulos didácticos).
- Texto dentro de notas PlantUML (``note bottom of``,
  ``note over``).

3.5.4 Validación automática
~~~~~~~~~~~~~~~~~~~~~~~~~~~

``scripts/validate-naming-corpus.sh`` (check C-07) audita
TODO el corpus sin exclusiones por zona, detectando
identifiers en español en declaraciones ``class X``,
``entity X``, atributos y métodos.

----

4. Convenciones por Lenguaje
============================

4.1 Python (backend Django REST Framework)
-------------------------------------------

- Funciones y variables: ``snake_case``.
- Clases: ``PascalCase``.
- Constantes: ``UPPER_SNAKE_CASE``.
- Privadas: prefijo ``_`` (``_internal_helper``).
- Tipos: ``PascalCase``, no abreviar (``UserId`` no ``UID``).

4.2 JavaScript / TypeScript (frontend React + Webpack)
-------------------------------------------------------

- Funciones y variables: ``camelCase``.
- Clases y componentes React: ``PascalCase``.
- Constantes: ``UPPER_SNAKE_CASE``.
- Hooks personalizados: prefijo ``use`` + ``camelCase``
  (``useReportData``).
- Booleanos: prefijos ``is``, ``has``, ``should``, ``can``.

4.3 SQL (PostgreSQL + MySQL)
----------------------------

- Tablas y columnas: ``snake_case``, plural para tablas
  (``user_roles``).
- Foreign key: ``{tabla_singular}_id``.
- Índices: ``ix_{tabla}_{columnas}``.
- Constraints unique: ``uq_{tabla}_{columnas}``.

4.4 Bash y scripting de operations
-----------------------------------

- Variables locales: ``snake_case``.
- Variables de entorno y constantes: ``UPPER_SNAKE_CASE``.
- Funciones: ``snake_case``.

----

5. Aplicación a la documentación
================================

Cuando un identificador aparece **citado** en un documento RST
(bloques ``.. code-block::``, ``literal``, ``:code:``), debe
cumplir este estándar. El revisor de documentación verifica que
los identificadores citados sean autoexplicativos y no usen
abreviaturas de dominio.

Si la documentación cita un identificador que el código real
usa pero que viola este estándar, **se documenta como deuda
técnica** en ``risks-technical-debt/`` y se programa su renombrado.

----

6. Cumplimiento
===============

6.1 Estado actual
-----------------

A la creación de este estándar (2026-04-28) el código del producto
IACT está en fase de spec / arquitectura — no hay código de
producción todavía. Este estándar entra en vigor para todo
código nuevo desde su aprobación.

6.2 Validación
--------------

Validación manual en revisión de PR. No se incluye linter
automatizado en CI inicialmente. La adición de un linter de
naming (ej. ``pylint`` con reglas custom para Python; ``eslint``
con reglas para JS/TS) es deuda técnica abierta a futuro.

----

7. Referencias
==============

- :ref:`std-001` — Documentación Sin Emojis.
- :ref:`std-002` — Nomenclatura Estándar del Proyecto.
- :ref:`std-006` — Versionado Semántico.
- :ref:`std-007` — Convención de Naming de Archivos y Carpetas.
- Robert C. Martin: "Clean Code: A Handbook of Agile Software
  Craftsmanship" (capítulo 2: Meaningful Names).

----

8. Historial
============

.. list-table::
 :header-rows: 1
 :widths: 12 15 73

 * - Versión
   - Fecha
   - Cambios
 * - 1.0.0
   - 2026-04-28
   - Versión inicial. Establece principios obligatorios:
     clean code, autoexplicativo, sin abreviaturas de dominio
     en identificadores técnicos. Convenciones por lenguaje
     del stack del producto IACT (Python/DRF, JavaScript/
     TypeScript/React, SQL PostgreSQL+MySQL, Bash).
