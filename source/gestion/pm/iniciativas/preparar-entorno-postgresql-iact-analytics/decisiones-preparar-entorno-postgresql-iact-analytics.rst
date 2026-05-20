.. meta::
   :artefacto: DECISIONES-PREPARAR-ENTORNO-POSTGRESQL-IACT-ANALYTICS
   :tipo: Decisiones
   :dominio: gestion
   :subdominio: pm/iniciativas/preparar-entorno-postgresql-iact-analytics
   :repo_objetivo: IACT-db
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T18:40:45
   :ultimo_cambio: 2026-05-19T18:40:45
   :autor: NestorMonroy
   :clasificacion: Interno

.. _decisiones-preparar-entorno-postgresql-iact-analytics:

==============================================================
Decisiones: Preparar Entorno PostgreSQL iact_analytics
==============================================================

Decisiones de diseno
=====================

D1 — Iniciativa compacta: tareas y progreso fusionados
--------------------------------------------------------

La iniciativa tiene 3 tareas atomicas, cadena lineal, sin
dependencias entre repos ni decisiones de diseno no obvias.
Considerado: el formato estandar de 5 artefactos (alcance,
analisis, tareas, progreso, decisiones).

Decision tomada: fusionar tareas + progreso en un solo
documento ``tareas-y-progreso-*.rst``. PROC-GOB-013 v2.0.0
Fase 2 permite "Documentos adicionales si el analisis lo
justifica" — el inverso aplica: omitir documentos cuando su
analisis no aporta. Aqui evitamos overhead documental sin
perder trazabilidad.

D2 — Omitir documento de Analisis separado
--------------------------------------------

Por el mismo motivo: el alcance describe el por que, el
estado inicial observado (cluster down) y el plan. No hay
gaps numerados ni priorizacion MoSCoW: todo es Must, lineal.

D3 — Reutilizar el patron Modelo C-runtime documentado en la iniciativa hermana
--------------------------------------------------------------------------------

``preparar-entorno-mariadb-ivr-legacy`` establecio el patron
``:repo_objetivo: IACT-db`` sin commit en el repo objetivo.
Esta iniciativa lo aplica de nuevo sin re-justificarlo. Las
decisiones D1 y D2 de aquella iniciativa quedan validas aqui
por referencia, no se duplican.

Hallazgos durante la ejecucion
================================

H-E1 — El cluster PostgreSQL 16 estaba instalado pero detenido
---------------------------------------------------------------

Esperado: el contenedor tenia ``postgresql-16`` instalado pero
sin servicio activo, lo que se traduce en
``pg_lsclusters: 16/main port 5432 down`` y
``connection failure`` al socket. ``pg_ctlcluster 16 main
start`` lo arranca limpiamente.

Esto es estado del contenedor (no del proyecto). Si el
contenedor se reciclara, el cluster necesita ser arrancado
nuevamente. Se registra para visibilidad pero no es accion
correctiva permanente.

H-E2 — setup.sh instala 4 extensiones por defecto
---------------------------------------------------

``provisioners/postgres/setup.sh`` instala ``uuid-ossp``,
``pg_trgm``, ``hstore`` y ``citext`` sin que sean explicitas
en el alcance. Son extensiones razonables para una app
Django moderna (UUID PKs, busqueda full-text, hstore, case
insensitive text). No bloquean nada y son idempotentes.

Verificacion post-ejecucion
=============================

.. list-table::
   :header-rows: 1
   :widths: 40 12 48

   * - Criterio del alcance
     - Resultado
     - Evidencia
   * - Cluster 16/main arriba
     - PASA
     - ``pg_isready -h 127.0.0.1 -p 5432`` retorna
       ``accepting connections``.
   * - BD iact_analytics existe
     - PASA
     - setup.sh paso 3: "Base de datos iact_analytics
       creada".
   * - django_user con CREATEDB
     - PASA
     - setup.sh paso 2: "Usuario django_user creado";
       paso 4: "Privilegios aplicados (incluye CREATEDB
       para tests)".
   * - 4 extensiones instaladas
     - PASA
     - setup.sh enumera "Extension uuid-ossp: OK",
       "pg_trgm: OK", "hstore: OK", "citext: OK".
   * - Conexion django_user
     - PASA
     - setup.sh paso 5: "Conexion OK:
       iact_analytics@django_user".

Conclusion
==========

El par de bases que IACT-api necesita esta completo.
``iact_analytics`` (PostgreSQL 16) e ``ivr_legacy``
(MariaDB 10.11) operativas con credenciales ``django_user`` /
``django_pass``. Habilita la siguiente iniciativa
``habilitar-pytest-iact-api`` (cadena ``db -> api``).
