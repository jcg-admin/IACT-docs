.. meta::
 :artefacto: STD_011
 :tipo: Estándar
 :dominio: normativa
 :subdominio: estandares
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _std-011:

=========================================================
STD_011: Aliases Auto-documentados en Diagramas PlantUML
=========================================================

.. contents:: Contenido
 :depth: 3
 :local:

----

1. Propósito
============

Este estándar define la convención de nombres para los **aliases**
(parte ``as X``) en todos los diagramas PlantUML del proyecto IACT.

**Principio central:**

  Un diagrama de secuencia, comunicación o actividad es documentación.
  Al leer una flecha ``A -> B : mensaje``, el lector debe entender
  quiénes son A y B **sin buscar la declaración del participante**.

----

2. Regla Principal
==================

**Todo alias debe ser auto-documentado.** Esto significa que el alias
solo por sí mismo revela el rol o nombre del participante.

.. list-table::
 :widths: 45 45 10
 :header-rows: 1

 * - Alias (PROHIBIDO)
   - Alias (CORRECTO)
   - Motivo
 * - ``as U``
   - ``as view_reports``
   - 1 letra, críptico
 * - ``as AE``
   - ``as AuthEndpoint``
   - 2 letras, no identificable
 * - ``as DE``
   - ``as DashboardEndpoint``
   - 2 letras, no identificable
 * - ``as SR``
   - ``as SegmentResolver``
   - 2 letras, no identificable
 * - ``as SRP``
   - ``as ServicioReportes``
   - acrónimo sin significado claro
 * - ``as RVG``
   - ``as view_reports``
   - sigla de grupo, no de función
 * - ``as QSG``
   - ``as view_pipeline_status``
   - sigla de grupo, no de función

----

3. Convenciones por Tipo de Elemento
=====================================

3.1 Actores RBAC
-----------------

El alias es el **nombre exacto de la función RBAC** del catálogo
(snake_case):

.. code-block:: text

   ' CORRECTO
   actor "view_reports" as view_reports
   actor "assign_functions" as assign_functions
   actor "request_pipeline_retry" as request_pipeline_retry

Cuando el actor tiene múltiples funciones en la etiqueta, usar la
**función principal** (la que da nombre al UC) como alias:

.. code-block:: text

   ' CORRECTO — función principal como alias
   actor "view_reports\n(view_dashboard)" as view_reports
   actor "assign_functions\n(create_users)" as assign_functions

3.2 Participantes de Sistema (Secuencia)
-----------------------------------------

El alias es el nombre de la clase/servicio en CamelCase, sin espacios:

.. code-block:: text

   ' CORRECTO
   participant "AuthEndpoint" as AuthEndpoint
   participant "DashboardEndpoint" as DashboardEndpoint
   participant "SegmentResolver" as SegmentResolver
   participant "ServicioReportes" as ServicioReportes
   participant "DisparadorETL" as DisparadorETL

Para nombres semánticos con espacios (vistas Kruchten):

.. code-block:: text

   ' CORRECTO
   participant "Interfaz de Acceso" as InterfazDeAcceso
   participant "Servicio de Autenticacion" as SvcAutenticacion
   database "Almacen de Datos" as AlmacenDatos

3.3 Objetos (Comunicación / Colaboración)
------------------------------------------

.. code-block:: text

   ' CORRECTO
   object ":AuthEndpoint" as AuthEndpoint
   object ":SegmentResolver" as SegmentResolver
   object ":User (RBAC group)" as UserRBAC

3.4 Nodos de Despliegue
------------------------

.. code-block:: text

   ' CORRECTO
   node "Apache + mod_wsgi" as WebServer
   node "Cliente Web" as ClienteWeb
   database "MariaDB" as MariaDB

   ' PROHIBIDO
   node "Apache + mod_wsgi" as W
   node "Cliente Web" as C

3.5 Estados (Máquinas de Estado)
---------------------------------

Los aliases de estados pueden ser cortos si el estado es referenciado
muchas veces, pero deben ser multi-palabra reconocibles:

.. code-block:: text

   ' CORRECTO
   state "Autenticacion JWT" as AUTH
   state "Dashboard IACT" as DASH
   state "Cierre de Sesion" as FINAL

   ' El alias AUTH, DASH, FINAL son reconocibles por su contexto
   ' (nombres de módulo del sistema, no siglas aleatorias)

----

4. Excepciones Permitidas
==========================

4.1 Aliases de 2-3 letras universalmente reconocibles
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Los siguientes aliases cortos son permitidos porque su significado
es universalmente conocido en el dominio del proyecto:

- ``IVR`` — Interactive Voice Response (entidad externa)
- ``JWT`` — JSON Web Token
- ``ETL`` — Extract-Transform-Load (como nombre de entidad)
- ``GUI`` — Graphical User Interface
- ``CPU`` — Central Processing Unit

4.2 Diagramas de ejemplo en documentación de referencia
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Los archivos en ``source/base-cognitiva/_uml/`` son material de
referencia con ejemplos genéricos. Pueden usar aliases como
``as A``, ``as B``, ``as C`` solo en ejemplos genéricos
(``:ObjetoA``, ``:ObjetoB``) — nunca en diagramas de sistema real.

----

5. Referencia al Material de Base
===================================

La convención se deriva del patrón documentado en:

- ``uml-09-diagramas-secuencias.rst`` — participantes: ``as GUI``,
  ``as SO`` (SistemaOp), ``as CPU``, ``as TV`` (TarjetaVideo)
- ``uml-10-diagramas-colaboraciones.rst`` — objetos: ``as GUI``,
  ``as SO``, ``as CPU``

El patrón del material de referencia: el alias guarda correspondencia
directa con el nombre de la entidad. ``SO`` = SistemaOp (iniciales del
nombre), ``TV`` = TarjetaVideo. En IACT, ``AE`` ≠ AuthEndpoint porque
``A`` podría ser cualquier cosa y ``E`` no sugiere "Endpoint".

----

6. Aplicación Retroactiva
==========================

Los documentos existentes que violan este estándar se corrigen según
el WP ``2026-05-04-02-11-54-uml-alias-naming-fix``.

Prioridad de corrección:

1. ``diagramas-uml-sistema.rst`` — documento de arquitectura principal
2. ``diagramas-uc-por-modulo.rst`` — diagramas de módulos
3. ``requisitos/casos-uso/**/diagramas-uml.rst`` — UCs individuales
4. ``arquitectura-tecnica/modulos/**/diagramas.rst`` — módulos arch.

----

7. Validación
=============

.. code-block:: bash

 # Buscar aliases de 1-2 letras en diagramas PlantUML
 grep -rn " as [A-Z][A-Z]\?$\| as [a-z][a-z]\?$" \
   source/ \
   --include="*.rst" | grep -v "base-cognitiva"

Un resultado vacío indica conformidad con el estándar.

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
   - Versión inicial — formaliza D-ALIAS-001..003
