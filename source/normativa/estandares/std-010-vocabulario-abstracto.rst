.. meta::
 :artefacto: STD_010
 :tipo: Estándar
 :dominio: normativa
 :subdominio: estandares
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
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
**rol** y **responsabilidad**, no en términos de tecnología de
implementación.

**Regla central:**

  Los documentos de requisitos describen **LO QUE HACE** el sistema,
  no **CÓMO LO IMPLEMENTA**. Los nombres de bibliotecas, frameworks,
  algoritmos concretos y excepciones de lenguaje pertenecen a
  ``implementacion-tecnica.rst`` y a ``source/arquitectura-tecnica/``.

----

2. Ámbito de Aplicación
=======================

+------------------------------------------+------------+
| Archivos                                 | Aplica     |
+==========================================+============+
| flujo-principal.rst                      | Sí         |
+------------------------------------------+------------+
| actores-precondiciones.rst               | Sí         |
+------------------------------------------+------------+
| criterios-aceptacion.rst                 | Sí         |
+------------------------------------------+------------+
| datos-involucrados.rst                   | Sí         |
+------------------------------------------+------------+
| informacion-general.rst                  | Sí         |
+------------------------------------------+------------+
| patrones-diseno.rst                      | Sí         |
+------------------------------------------+------------+
| requisitos-no-funcionales.rst            | Sí         |
+------------------------------------------+------------+
| excepciones.rst                          | Sí         |
+------------------------------------------+------------+
| diagramas-uml.rst (participantes)        | Sí         |
+------------------------------------------+------------+
| implementacion-tecnica.rst               | No — libre |
+------------------------------------------+------------+
| source/arquitectura-tecnica/**           | No — libre |
+------------------------------------------+------------+

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
en documentos de requisitos:

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
