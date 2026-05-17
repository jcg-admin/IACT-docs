.. meta::
   :artefacto: RUNBOOK-disaster-recovery
   :tipo: Runbook
   :dominio: devops
   :subdominio: runbooks
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2025-11-07
   :ultimo_cambio: 2026-05-16T23:01:11
   :autor: NestorMonroy
   :clasificacion: Operacional

.. _runbook-disaster-recovery:

==========================================
Runbook: Disaster Recovery
==========================================

.. note::

   Plan de Disaster Recovery (DR) del sistema IACT con procedimientos
   de backup y restore para MySQL y Cassandra.

   **RTO objetivo:** < 4 horas para fallo completo.
   **RPO objetivo:** < 1 hora.

1. Cuando ejecutar
==================

- Fallo de base de datos con corrupcion detectada
- Fallo completo del servidor
- Ataque de ransomware o borrado accidental de datos
- Test mensual de DR (obligatorio)

2. Precondiciones
=================

- Acceso SSH al servidor o acceso al entorno DR
- Credenciales de base de datos disponibles
- Backups recientes verificados en ``/var/backups/``

3. Targets RTO/RPO por componente
==================================

.. list-table::
   :widths: 35 15 15 15 20
   :header-rows: 1

   * - Componente
     - Criticidad
     - RTO
     - RPO
     - Prioridad restore
   * - Django Application
     - Alta
     - 30 min
     - 0
     - 1
   * - MySQL (dora_metrics)
     - Alta
     - 2 horas
     - 1 hora
     - 2
   * - Cassandra (logs)
     - Media
     - 4 horas
     - 6 horas
     - 3
   * - Static files
     - Baja
     - 24 horas
     - 24 horas
     - 4

4. Procedimiento: Restore MySQL
================================

.. code-block:: bash

   # 1. Detener MySQL
   systemctl stop mysql

   # 2. Restaurar desde backup
   ./scripts/disaster_recovery/restore_mysql.sh \
     /var/backups/mysql_backup_<FECHA>.sql.gz.enc

   # 3. Iniciar MySQL
   systemctl start mysql

   # 4. Verificar integridad
   mysql -e "SELECT table_name, table_rows
             FROM information_schema.tables
             WHERE table_schema = 'iact';"
   mysql -e "SELECT MAX(created_at) FROM dora_metrics;"
   mysql -e "CHECK TABLE dora_metrics;"

**Tiempo estimado:** 1 hora para 10 GB de base de datos.

5. Procedimiento: Restore Cassandra
=====================================

.. code-block:: bash

   # 1. Detener Cassandra
   systemctl stop cassandra

   # 2. Limpiar datos existentes
   rm -rf /var/lib/cassandra/data/iact_logs/*

   # 3. Restaurar snapshot
   tar -xzf /var/backups/cassandra_<FECHA>.tar.gz \
       -C /var/lib/cassandra/data/

   # 4. Iniciar y reparar
   systemctl start cassandra
   nodetool repair

   # 5. Verificar consistencia
   nodetool status

**Tiempo estimado:** 2 horas para 100 GB.

6. Estrategia de backup
========================

.. list-table::
   :widths: 20 25 25 30
   :header-rows: 1

   * - Componente
     - Full backup
     - Incremental
     - Retention
   * - MySQL
     - Diario 2:00 AM
     - Cada 6 horas (binary logs)
     - 30 dias
   * - Cassandra
     - Cada 6 horas (snapshot)
     - Cada hora (commit logs)
     - 30 dias

Los cron jobs de backup estan en
:doc:`runbook-cron-jobs-mantenimiento`.

7. Verificacion del restore
============================

.. code-block:: bash

   # Test de aplicacion
   curl http://localhost:8000/api/dora/metrics/

   # Verificar conectividad
   cd api/callcentersite
   python manage.py check --database default
   python manage.py check --database mysql

8. Test mensual de DR
======================

**Script:** ``scripts/disaster_recovery/test_dr.sh``

Ejecutar el primer dia de cada mes. El script:

1. Crea backups de prueba
2. Simula fallo (detiene servicios)
3. Ejecuta restore
4. Valida integridad de datos
5. Mide el tiempo de recovery
6. Genera reporte

Resultado del ultimo test (2025-11-07):

.. list-table::
   :widths: 40 30 30
   :header-rows: 1

   * - Metrica
     - Resultado
     - Target
   * - Recovery Time (RTO)
     - 2 horas 22 min
     - < 4 horas
   * - Data Loss (RPO)
     - 30 minutos
     - < 1 hora
   * - Estado
     - PASS
     -

9. Escalacion
=============

.. list-table::
   :widths: 20 30 15 35
   :header-rows: 1

   * - Severidad
     - Primer contacto
     - Escalar en
     - Segundo contacto
   * - P0 (critico)
     - On-call engineer
     - 15 min
     - Senior DBA
   * - P1 (alto)
     - On-call engineer
     - 30 min
     - Team Lead
   * - P2 (medio)
     - Support team
     - 1 hora
     - On-call engineer

10. Trazabilidad
================

- Fuente: ``temp-holding/FASE 01/docs/operaciones/TASK-036-disaster_recovery.md``
- Scripts: ``scripts/disaster_recovery/``
- Politicas de retention: :doc:`runbook-log-retention-policies`
- Backup automatico: :doc:`runbook-cron-jobs-mantenimiento`
