.. meta::
 :artefacto: AT_CONTEXT_VIEW_STAKEHOLDERS
 :tipo: Diagrama Arquitectonico — Context View
 :dominio: arquitectura_tecnica
 :subdominio: ContextView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at-context-stakeholders:

=============
Stakeholders
=============

Mapa de stakeholders del sistema IACT con sus grupos RBAC, concerns
arquitectonicos y relacion con las vistas arquitectonicas.

Grupos de usuario IACT
=======================

.. list-table::
 :header-rows: 1
 :widths: 18 20 62

 * - Grupo RBAC
   - Perfil
   - Concerns arquitectonicos
 * - **AGR_ADMIN**
   - Administrador IACT
   - Control de acceso RBAC granular (64 funciones atomicas activas);
     gestion de usuarios (crear, desactivar — BR-009);
     asignacion de permisos temporales (CNST-031);
     visualizacion de separacion de funciones (separation of duties) (CNST-030).
 * - **AGR_OPERADOR**
   - Operador / Supervisor de Operaciones
   - Disponibilidad del pipeline ETL (P-04);
     acceso a dashboards IVR en tiempo real;
     gestion de alertas y umbrales;
     acceso a logs de ejecucion ETL.
 * - **AGR_AUDITOR**
   - Auditor de Acceso
   - Trazabilidad regulatoria completa (CNST-025);
     exportacion del audit log (append-only, inmutable);
     generacion de reportes de cumplimiento;
     cobertura normativa institucional.
 * - **AGR_CALLER** *(datos)*
   - Ciudadano / llamante
   - No es usuario IACT. Es la fuente de datos de las
     llamadas registradas en el Sistema IVR. Sus datos
     se procesan via ETL (P-01: solo lectura).

Stakeholders organizacionales
===============================

.. list-table::
 :header-rows: 1
 :widths: 25 75

 * - Stakeholder
   - Rol y concern
 * - **Instituciones adquirentes**
   - Organizaciones que despliegan IACT para el analisis
     de sus operaciones de call center. Concern principal:
     seguridad de datos (RBAC restrictivo), disponibilidad
     del sistema y cumplimiento normativo.
 * - **Equipo de desarrollo**
   - Concern: modularidad arquitectonica (13 modulos UC: 10 RBAC activos in-scope v5.6.0 + 2 reservados open-closed + Caller sin RBAC),
     evolucionabilidad incremental, stack Django/Python,
     separacion de capas (5-layer stack en implementation-view).
 * - **Operaciones / DevOps**
   - Concern: despliegue multi-variante (deploy-estandar,
     deploy-auth-cache, deploy-etl), monitoreo del pipeline
     ETL, gestion de ventanas de mantenimiento (CNST-008).

Conflictos de concerns
=======================

Los siguientes conflictos de concerns se resuelven mediante restricciones
formales (CNST-*) y decisiones arquitectonicas (ADR-GOB-*):

.. list-table::
 :header-rows: 1
 :widths: 25 35 40

 * - Conflicto
   - Stakeholders en tension
   - Resolucion
 * - Seguridad vs. operabilidad
   - AGR_ADMIN (acceso restrictivo) vs. AGR_OPERADOR (acceso amplio)
   - RBAC granular: 64 funciones atomicas activas; separacion de deberes (CNST-030);
     permisos temporales (CNST-031) para casos excepcionales.
 * - Disponibilidad vs. consistencia ETL
   - AGR_OPERADOR (sistema disponible 24/7) vs. restriccion ETL
   - Ventana ETL de 6-12 horas (CNST-008); aislamiento de
     fallos ETL (P-04: fallo no bloquea operaciones).
 * - Trazabilidad vs. rendimiento
   - AGR_AUDITOR (audit log completo) vs. rendimiento de escrituras
   - AuditEvent append-only (CNST-025); indices en event_type
     y actor_user_id para busqueda eficiente.

.. seealso::

 :doc:`context-diagram`
 :doc:`external-interfaces`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/normativa/restricciones/index`
