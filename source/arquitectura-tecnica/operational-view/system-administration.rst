.. meta::
 :artefacto: AT_OPERATIONAL_VIEW_ADMIN
 :tipo: Diagrama Arquitectonico — Operational View
 :dominio: arquitectura_tecnica
 :subdominio: OperationalView
 :estado: Vigente
 :version: 1.1.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-09
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at-operational-admin:

==========================
Administracion del Sistema
==========================

Procedimientos operacionales realizados por AGR_ADMIN sobre
el sistema IACT en produccion: gestion de usuarios,
asignacion de permisos RBAC, supervision de sesiones activas
y otorgamiento de permisos temporales.

.. note::

 OperationalView documenta **como se opera** el sistema —
 procedimientos paso a paso. NO documenta **que** hace el
 sistema (eso es UseCaseView). Por esa razon esta vista
 usa **diagramas de actividad** (no diagramas de casos de
 uso). Ver
 :doc:`/base-cognitiva/_uml/uml-14-uml-vistas-arquitectonicas/relaciones-dependencia-iact`
 para la asignacion de tipos de diagrama por vista.

Inventario de procedimientos administrativos
=============================================

.. list-table::
 :widths: 35 65
 :header-rows: 1

 * - Procedimiento
   - Restriccion / regla aplicable
 * - Alta de usuario con asignacion RBAC
   - CNST-030 (separacion de funciones)
 * - Desactivacion de usuario (no eliminacion)
   - BR-009 v2.0.0 (no eliminar, desactivar)
 * - Asignacion / revocacion de FunctionGroup o
     AccessGroup
   - CNST-030
 * - Otorgamiento de permiso temporal (max 6 meses)
   - CNST-031 (rango ``granted_at..expires_at``)
 * - Revocacion de permiso temporal
   - CNST-025 (auditoria)
 * - Cierre administrativo de sesion ajena
   - CNST-003 (una sesion activa por usuario)
 * - Consulta de reglas de separacion
   - CNST-030
 * - Consulta del audit log
   - CNST-025 (append-only inmutable)

----

Flujo 1 — Alta de usuario con asignacion RBAC
==============================================

.. uml::
 :caption: Procedimiento — alta de usuario con verificacion CNST-030.

 @startuml

 skinparam ArrowColor #444444
 skinparam ActivityBorderColor #333333
 skinparam ActivityBackgroundColor #F5F5F5
 skinparam shadowing false

 start

 :system_admin (AGR-010): autenticar en sistema;
 :Crear cuenta de usuario\n(username, email, full_name);
 :Asignar AccessGroup primario\n(AGR-001..012);

 if (¿Requiere funciones adicionales?) then (si)
   :Asignar FunctionGroup(s)\ncomplementarios;
   if (¿Conflicto de separacion detectado?) then (si)
     :Rechazar asignacion\n(CNST-030: enforcement de separacion);
     stop
   else (no)
     :Confirmar asignacion;
   endif
 else (no)
 endif

 :AuditEvent generado automaticamente\n(CNST-025: append-only);
 :Notificar a InternalMailbox del usuario\n(CNST-001);

 stop

 @enduml

----

Flujo 2 — Otorgamiento de permiso temporal
===========================================

.. uml::
 :caption: Procedimiento — otorgar permiso temporal con CNST-031.

 @startuml

 skinparam ArrowColor #444444
 skinparam ActivityBorderColor #333333
 skinparam ActivityBackgroundColor #F5F5F5
 skinparam shadowing false

 start

 :system_admin selecciona usuario destino;
 :Especificar Function a otorgar
 + justificacion documentada;

 if (¿granted_at .. expires_at\ndentro de 6 meses?\n(CNST-031)) then (no)
   :Rechazar — duracion maxima 6 meses;
   stop
 else (si)
 endif

 if (¿Function en conflicto con
 grupos existentes?\n(CNST-030)) then (si)
   :Rechazar (separacion de funciones);
   stop
 else (no)
 endif

 :INSERT TemporalPermission
 (granted_at, expires_at,
 justification);

 :AuditEvent (TEMPORAL_GRANT);

 :Notificar a usuario y supervisor;

 :Job de housekeeping detecta
 expires_at < NOW() y revoca
 automaticamente;

 stop

 @enduml

----

Flujo 3 — Cierre administrativo de sesion ajena
================================================

.. uml::
 :caption: Procedimiento — cerrar sesion de otro usuario (CNST-003 + view_all_active_sessions).

 @startuml

 skinparam ArrowColor #444444
 skinparam ActivityBorderColor #333333
 skinparam ActivityBackgroundColor #F5F5F5
 skinparam shadowing false

 start

 :system_admin: ver sesiones activas
 (view_all_active_sessions permission);

 :SELECT Session
 WHERE status = 'active'
 ORDER BY last_activity DESC;

 :system_admin selecciona sesion a cerrar;

 if (¿es la propia sesion?) then (si)
   :Logout normal — flujo aparte;
   stop
 else (no)
 endif

 if (¿usuario destino tiene permission
 admin de igual o mayor rango?) then (si)
   :Rechazar — separacion administrativa
   (no se puede cerrar admin con admin);
   stop
 else (no)
 endif

 :UPDATE Session
 SET status = 'closed_by_admin',
 closed_by = admin.id,
 closed_at = NOW();

 :Revocar JWT activos del usuario
 (jti blacklist + invalidate cache);

 :AuditEvent (SESSION_FORCE_CLOSE);

 :Notificar al usuario afectado
 via email (sesion cerrada por
 administrador, motivo);

 stop

 @enduml

----

Restricciones operacionales
=============================

.. list-table::
 :header-rows: 1
 :widths: 15 85

 * - Restriccion
   - Descripcion
 * - **BR-009 v2.0.0**
   - Los usuarios no se eliminan — se desactivan. Estado
     ``INACTIVE`` o ``BLOCKED`` pero el registro permanece.
 * - **CNST-030**
   - Separacion de funciones (separation of duties): el
     sistema impide asignar conjuntos de funciones en
     conflicto al mismo usuario. La separacion se evalua
     en tiempo de asignacion.
 * - **CNST-031**
   - Permisos temporales tienen rango obligatorio
     ``granted_at .. expires_at`` (maximo 6 meses).
     Requieren justificacion documentada.
 * - **CNST-003**
   - Un usuario solo puede tener una sesion activa
     simultanea. AGR_ADMIN puede cerrar sesiones activas
     de otros usuarios (``view_all_active_sessions``).
 * - **CNST-025**
   - Toda operacion de administracion genera un
     ``AuditEvent`` inmutable (append-only). Sin
     excepciones.

----

.. seealso::

 - :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index` —
   modelo RBAC autoritativo.
 - :doc:`/arquitectura-tecnica/use-case-view/admin/index` —
   casos de uso administrativos (UseCaseView, distinto de
   esta vista operacional).
 - :doc:`system-configuration` — configuracion del sistema.
 - :doc:`system-support` — procedimientos de soporte.
