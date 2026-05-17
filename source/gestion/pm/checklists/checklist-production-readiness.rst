.. meta::
   :artefacto: CHECKLIST-production-readiness
   :tipo: Checklist
   :dominio: gestion
   :subdominio: pm/checklists
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2025-11-07
   :ultimo_cambio: 2026-05-16T23:01:11
   :autor: NestorMonroy
   :clasificacion: Interno

.. _checklist-production-readiness:

==========================================
Checklist: Production Readiness
==========================================

.. note::

   Checklist de 70+ items para validar que el sistema IACT esta
   listo para produccion. Cubre infraestructura, seguridad,
   performance, observabilidad, compliance, documentacion,
   testing y DORA metrics.

   Usar antes de cada go-live o despliegue mayor.

Criterio Go / No-Go
====================

**GO** (todos deben cumplirse):

- Todos los items del checklist completados
- Build Sphinx 0 warnings, 0 errors
- Sin bugs P0/P1 abiertos
- Test de DR exitoso en los ultimos 30 dias
- Auditoria de seguridad aprobada
- Performance dentro de targets

**NO-GO** (cualquiera detiene el go-live):

- Cualquier bug P0 abierto
- Health check fallando
- Falta sign-off de rol critico
- Test de DR fallido
- Vulnerabilidad de seguridad sin resolver

1. Infraestructura (15 items)
==============================

- [ ] Cassandra cluster 3 nodos configurado y funcionando
- [ ] MySQL replication master-slave configurado
- [ ] Load balancer configurado con health checks
- [ ] Firewall rules production configuradas
- [ ] SSL/TLS certificates validos (no expiran en 90 dias)
- [ ] DNS configurado y propagado
- [ ] Monitoring activo en todos los componentes
- [ ] Alerting configurado con escalation policies
- [ ] Backup automatico funcionando y tested
- [ ] DR plan tested y documentado (ver :doc:`/devops/runbooks/runbook-disaster-recovery`)
- [ ] Log aggregation funcionando (Cassandra)
- [ ] Disk space mayor a 50% libre en todos los nodos
- [ ] Network bandwidth adecuado (mayor a 1 Gbps)
- [ ] Cron jobs de mantenimiento activos (ver :doc:`/devops/runbooks/runbook-cron-jobs-mantenimiento`)
- [ ] Infrastructure as Code actualizado

2. Seguridad (18 items)
========================

- [ ] Security audit completado y vulnerabilidades remediadas
- [ ] Secrets management configurado (sin credenciales hardcoded)
- [ ] HTTPS enforced en todos los endpoints
- [ ] HTTP Strict Transport Security (HSTS) headers
- [ ] Rate limiting activo y tested
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (template escaping)
- [ ] CSRF protection enabled
- [ ] Autenticacion robusta (Django auth)
- [ ] Autorizacion granular (permissions/groups)
- [ ] Session security (secure cookies, httponly)
- [ ] Password policies enforced
- [ ] API authentication (tokens/JWT)
- [ ] Input validation en todos los endpoints
- [ ] Output encoding para prevenir injection
- [ ] Security headers configurados (CSP, X-Frame-Options)
- [ ] Dependency scanning para vulnerabilidades
- [ ] Penetration testing completado

3. Performance (12 items)
==========================

- [ ] Load testing completado (escenarios 1x, 2x, 5x normal load)
- [ ] Performance tuning aplicado (MySQL, Cassandra, Django)
- [ ] Database indexes optimizados
- [ ] Query performance validado (p95 menor a 1 segundo)
- [ ] API response times dentro de target (p95 menor a 500 ms)
- [ ] Cassandra throughput mayor a 100K writes/s
- [ ] Connection pooling optimizado
- [ ] Static files con compression habilitado
- [ ] Resource limits configurados (CPU, memory)
- [ ] Sin memory leaks detectados (24h soak test)
- [ ] Caching configurado donde aplica
- [ ] Performance regression tests pasando

4. Observabilidad (10 items)
==============================

- [ ] Logging estructurado activo (JSON format)
- [ ] Log levels configurados apropiadamente
- [ ] Monitoring dashboards operativos
- [ ] Alerting rules configuradas para metricas criticas
- [ ] On-call schedule definido y publicado
- [ ] Runbooks documentados para incidents comunes
- [ ] Incident response plan documentado
- [ ] Health check endpoints funcionando
- [ ] Metricas expuestas para key indicators
- [ ] Log retention policies activas (ver :doc:`/devops/runbooks/runbook-log-retention-policies`)

5. Compliance (8 items)
========================

- [ ] RNF-002 compliance: sin Redis, Prometheus ni Grafana

  .. code-block:: bash

     pip list | grep -E "(redis|prometheus|grafana)"
     # Debe retornar vacio

- [ ] SESSION_ENGINE = ``django.contrib.sessions.backends.db``

  .. code-block:: bash

     grep SESSION_ENGINE api/callcentersite/callcentersite/settings.py

- [ ] Data retention policies activas y documentadas
- [ ] Audit logging completo para acciones sensibles
- [ ] GDPR compliance: proceso de borrado de datos documentado
- [ ] Privacy policy actualizada
- [ ] Terms of service actualizados
- [ ] Requisitos regulatorios cumplidos

6. Documentacion (9 items)
============================

- [ ] Arquitectura documentada y actualizada
- [ ] API documentation actualizada (endpoints, schemas)
- [ ] Runbooks completos para operaciones
- [ ] Onboarding docs para nuevos integrantes
- [ ] Troubleshooting guides para issues comunes
- [ ] DR procedures documentadas y tested
- [ ] Deployment procedures documentadas
- [ ] Configuration management documentado
- [ ] Changelog mantenido

7. Testing (11 items)
======================

- [ ] Unit tests con coverage mayor a 80%
- [ ] Integration tests pasando 100%
- [ ] E2E tests pasando para user journeys criticos
- [ ] Load tests pasando con target performance
- [ ] Stress tests pasando sin crashes
- [ ] Security tests pasando (OWASP top 10)
- [ ] DR drill completado exitosamente
- [ ] Smoke tests suite creada y passing
- [ ] Regression tests pasando
- [ ] Performance regression tests pasando
- [ ] Automated testing en CI/CD pipeline

8. DORA Metrics (9 items)
==========================

- [ ] 7/7 DORA 2025 AI Capabilities implementadas
- [ ] Deployment Frequency mayor a 1 deploy por semana
- [ ] Lead Time menor a 2 dias
- [ ] Change Failure Rate menor a 15%
- [ ] MTTR menor a 4 horas
- [ ] DORA metrics dashboard operativo
- [ ] DORA metrics tracking automatizado
- [ ] DORA historical data disponible (30+ dias)
- [ ] DORA improvement trends positivos

Proceso de Sign-off
====================

Requiere aprobacion de los siguientes roles antes del go-live:

.. list-table::
   :widths: 30 40 30
   :header-rows: 1

   * - Rol
     - Area de responsabilidad
     - Estado
   * - Tech Lead
     - Implementacion tecnica general
     - Pendiente
   * - Arquitecto Senior
     - Arquitectura y diseno
     - Pendiente
   * - DevOps Lead
     - Infraestructura y operaciones
     - Pendiente
   * - Security Lead
     - Auditoria de seguridad y compliance
     - Pendiente
   * - QA Lead
     - Testing y calidad
     - Pendiente
   * - Product Owner
     - Requisitos de negocio
     - Pendiente

Trazabilidad
============

- Fuente: ``temp-holding/FASE 01/docs/operaciones/TASK-038-production_readiness.md``
- DR relacionado: :doc:`/devops/runbooks/runbook-disaster-recovery`
- Cron jobs: :doc:`/devops/runbooks/runbook-cron-jobs-mantenimiento`
- Log retention: :doc:`/devops/runbooks/runbook-log-retention-policies`
