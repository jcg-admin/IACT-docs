.. meta::
 :artefacto: MODELO_DOMINIO_IACT
 :tipo: Modelo Arquitectonico
 :dominio: arquitectura_tecnica
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-01
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _modelo-dominio-iact:

===================
MODELO DOMINIO IACT
===================

.. note::

 **Modelo conceptual canonico del dominio IACT**, complementario a
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`. Producido por
 el WP ``2026-05-01-02-01-06-domain-model-canonization`` aplicando el
 filtro de Abbott + IEEE 830 sobre el corpus vigente (64 funciones activas
 RBAC v5.6.0, BR/CNST en sus versiones vigentes). El numero de UCs
 es dinamico y evoluciona con el scope; la trazabilidad UC-clase se
 mantiene en la seccion de cobertura.

 **Convencion de nombres**: identificadores (clases, atributos,
 operaciones, valores de enum) en **ingles** por consistencia con el
 modelo RBAC v5.6.0 y NOM_001 § 2.3. La prosa, los comentarios y las
 notas de los diagramas estan en **espanol**.

----

1. Proposito y alcance
======================

Este documento materializa las **26 clases canonicas** del dominio
IACT distribuidas en **ocho bounded contexts** (Auth, RBAC, Calls,
Reports & Metrics, Pipeline, Alerts, Audit, Logs). Cada clase
incluye atributos relevantes, operaciones de negocio, restricciones
canonicas (BR/CNST en versiones vigentes) y trazabilidad a los UCs
del catalogo.

El alcance del modelo cubre los conceptos persistentes con identidad
propia y operaciones de negocio. Roles operativos
(Operator/Supervisor/Administrator/Auditor) NO son clases — se
modelan como pertenencia del usuario a un AccessGroup. El concepto
``DataSegment`` que aparecio en versiones historicas fue descartado
por Z.1.C (Camino C) y no aparece en este modelo.

----

2. Convenciones aplicadas
=========================

2.1 Identificadores en ingles
-----------------------------

- **Clases** en PascalCase (``User``, ``Session``, ``PipelineExecution``).
- **Atributos** en snake_case (``user_id``, ``started_at``,
  ``last_login_at``).
- **Operaciones** en snake_case (``deactivate``, ``acknowledge``,
  ``schedule_report``).
- **Valores de enum** en UPPER_SNAKE (``ACTIVE``, ``ACKNOWLEDGED``).

Justificacion: el modelo RBAC v5.6.0 ya usa ingles para nombres de
funciones tras la correccion aplicada por Z.1.C. Mantener una
unica convencion idiomatica para todos los identificadores formales
del dominio reduce el costo cognitivo y el riesgo de mismatches que
documentaron las iteraciones previas v5.0..v5.2.x.

2.2 Versiones canonicas de constraints
--------------------------------------

Todas las restricciones citadas en este documento son las versiones
vigentes tras el programa Z (modelo-rbac-improvement):

.. list-table::
 :widths: 30 15 55
 :header-rows: 1

 * - Constraint
   - Version
   - Alcance
 * - BR-009 — Bajas logicas
   - v2.0.0
   - Global; toda entidad con ciclo de vida desactiva, no elimina
 * - BR-011 — Limites de exportacion
   - v2.0.0
   - Delega a CNST-019 / CNST-020; sin cifras embebidas
 * - CNST-001 — Buzon interno
   - vigente
   - Entrega de notificaciones via ``InternalMailbox``, no email
 * - CNST-002 — Caducidad de sesion
   - vigente
   - Timeout de sesion configurable
 * - CNST-003 — Sesion unica
   - vigente
   - Una sesion activa por usuario
 * - CNST-006 / 007 / 008 — Ventana ETL
   - vigente
   - Ventana de carga, BD operativa de solo lectura, BD analitica
 * - CNST-019 — Exportaciones asincronas
   - v3.0.0
   - Cola asincrona abstracta; sin acoplamiento a tecnologia
 * - CNST-020 — Throttling de exportaciones
   - v3.0.0
   - Throttling abstracto por recursos; cifras en ADR de
     implementacion
 * - CNST-024 — Retencion de logs
   - vigente
   - Periodo de retencion para los logs y snapshots de salud
 * - CNST-025 — Auditoria inmutable
   - vigente
   - Append-only en ``AuditEvent``; sin actualizar ni DELETE
 * - CNST-030 — Separacion de funciones (SoD)
   - vigente
   - Reglas de exclusion mutua entre funciones
 * - CNST-031 — Rango temporal de permisos
   - vigente
   - Permisos excepcionales con ventana ``granted_at..expires_at``

----

3. Diagramas por clase
======================

Un archivo por clase de dominio (26 clases en 8 bounded contexts).
Cada archivo incluye atributos canonicos, metodos, enums propios y
relaciones directas con otras clases del mismo bounded context.

Ver indice completo en :doc:`domain-model/index`.

.. toctree::
 :maxdepth: 1
 :caption: Domain Model — Overview

 domain-model/overview

----

4. Cobertura UC × clase
=======================

El WP que produjo este modelo verifico cobertura **bidireccional al
100 %**:

- **UC -> clase**: todos los UCs vigentes en
  ``source/requisitos/casos-uso/`` operan sobre al menos una clase
  del modelo.
- **Clase -> UC**: las 25 clases del modelo aparecen como sujeto u
  objeto en al menos un UC.

La matriz detallada vive en el WP
``2026-05-01-02-01-06-domain-model-canonization/pilot/uc-vs-domain-validation.md``
con mapeo completo (cluster por cluster, categoria Z.2.A por UC,
funcion RBAC v5.6.0 por UC).

Resumen de actividad por clase:

.. list-table::
 :widths: 30 15 55
 :header-rows: 1

 * - Clase
   - UCs que la tocan
   - Comentario
 * - User
   - 17
   - Entidad central; aparece en Auth, USR, ACC, PERM, ALR
 * - Report
   - 14
   - Concentra los 15 UCs del cluster RPT
 * - AuditEvent
   - 10
   - Producida por toda escritura en el sistema
 * - Function
   - 9
   - Catalogo RBAC consumido transversalmente
 * - Assignment
   - 9
   - Vinculo User-Group / User-AccessGroup
 * - Call
   - 6 explicito
   - Fuente de datos para los 17 UCs RPT (lectura indirecta)
 * - Session
   - 5
   - Operada por AUTH y USR
 * - PipelineExecution
   - 5
   - Cluster PIP completo + LOG-02 cross-context
 * - ExceptionalPermission, FunctionGroup, Alert
   - 4 c/u
   - Operaciones especificas con SoD via RBAC

----

5. Decisiones canonicas heredadas (D-01..D-11)
==============================================

Once decisiones del WP cerrado
``rbac-modelo-conceptual-cleanup`` (programa Z.2) son vinculantes
para este modelo. Resumen de su impacto sobre las clases:

.. list-table::
 :widths: 8 35 57
 :header-rows: 1

 * - ID
   - Decision Z.2
   - Impacto en este modelo
 * - D-01
   - Renames ``delete_*`` a ``deactivate_*`` / ``disable_*``;
     BR-009 alcance global
   - Toda clase con ciclo de vida tiene atributo ``state`` y
     operacion soft-delete; cero clases con ``delete``
 * - D-02
   - Agregar ``acknowledge_alert``
   - ``Alert`` tiene maquina de estados con transicion ACKNOWLEDGED
 * - D-03
   - Split de suscripcion en subscribe / unsubscribe /
     configure_severity
   - ``Subscription`` es entidad de primera clase con tres
     operaciones distintas
 * - D-04
   - Un solo UC con flujos alternativos para las tres operaciones
   - Capa de UC y capa RBAC son ortogonales
 * - D-05
   - Logs en application / etl / infrastructure + system_health +
     technical_metrics
   - 5 clases distintas en bounded context Logs; Health y
     TechnicalMetric NO son logs
 * - D-06
   - Auditoria SRP preventiva
   - Una sola responsabilidad por clase; particionado SRP aplicado
 * - D-07
   - Larman para UCs, SRP para funciones RBAC (capas ortogonales)
   - Las clases modelan conceptos de negocio; las funciones RBAC
     no son clases
 * - D-08
   - CNST-020 abstracto sin cuotas por formato
   - ``ExportJob`` cita CNST como nota; numeros viven en ADR
 * - D-09
   - Quota anti-abuse generica
   - ``ExportJob`` tiene atributos de recursos, no de formato
 * - D-10
   - Tres tipos de reporte como instancias de ``view_reports``
   - ``Report`` tiene atributo ``scope`` con siete valores; sin
     subclases
 * - D-11
   - BR-011 reescrita como regla de negocio
   - ``ExportJob`` referencia BR/CNST; sin numeros embebidos

----

6. Trazabilidad y referencias
=============================

6.1 WPs que produjeron este modelo
----------------------------------

- WP actual:
  ``.thyrox/context/work/2026-05-01-02-01-06-domain-model-canonization/``
  con seis analisis registrados (inventario de temp-holding,
  historia de elicitacion, riesgos historicos, criterios de
  calidad, fixes ya aplicados en WPs previos, estado canonico del
  programa Z) y los entregables de Stage 1 / 3 / 7 / 9.

6.2 WPs cerrados que aportaron decisiones canonicas
---------------------------------------------------

- ``2026-04-29-17-52-15-modelo-rbac-improvement`` (programa Z
  padre).
- ``2026-04-30-00-07-08-rbac-functions-count-audit`` (Z.1.C):
  conteo de funciones reconciliado, concepto Segmento descartado.
- ``2026-04-30-00-37-45-rbac-modelo-conceptual-cleanup`` (Z.2):
  bump del modelo RBAC a v5.5.0 con 64 funciones activas, decisiones
  D-01..D-11.
- ``2026-04-30-00-44-07-rbac-missing-ucs-discovery`` (Z.2.A):
  clasificacion de los 61 UCs base en cinco categorias (+ 19 OPR/SUP/CLI en v5.5.0).
- ``2026-04-29-14-56-40-std007-rename-cleanup``: migracion de
  nomenclatura kebab-case en 315 archivos del corpus.

6.3 Documentos relacionados
---------------------------

- :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index` — modelo RBAC
  v5.6.0 con las 64 funciones activas (77 declaradas, 13 reservadas open-closed) que operan sobre las clases
  declaradas aqui.
- ``source/requisitos/_metodologia-aplicacion/analisis-dominio.rst``
  — guia metodologica del modelado del dominio. La cifra "97 UCs"
  citada en su § 11 debe corregirse a 61 (cifra vigente al cierre
  del WP que produjo este modelo, susceptible de evolucion en WPs
  posteriores).

----

7. Evolucion del modelo
=======================

Este es el **primer modelo de dominio canonico** del proyecto. Se
versionara con SemVer 2.0.0 a partir de v1.0.0:

- Bump **MAJOR** cuando se elimine o renombre una clase, o cambie
  un atributo identificador.
- Bump **MINOR** cuando se agregue una clase nueva, una operacion o
  un atributo.
- Bump **PATCH** para correcciones documentales sin cambios
  estructurales.

Cualquier cambio futuro al modelo debe verificar:

- Cobertura UC × clase 100 % (ningun UC sin clase, ninguna clase
  sin UC).
- Cumplimiento de las decisiones D-01..D-11 vigentes (o registro
  formal de su superseding).
- Build de Sphinx con 0 warnings y 0 errors antes de publicar.
