.. meta::
 :artefacto: AT_OPERATIONAL_VIEW_ADMIN
 :tipo: Diagrama Arquitectonico — Operational View
 :dominio: arquitectura_tecnica
 :subdominio: OperationalView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at-operational-admin:

==========================
Administracion del Sistema
==========================

Operaciones de administracion realizadas por AGR_ADMIN sobre el sistema IACT
en produccion: gestion de usuarios, asignacion de permisos RBAC, supervision
de sesiones activas y separacion de funciones.

Casos de uso operacionales — AGR_ADMIN
=======================================

.. uml::
 :caption: Figura — Casos de uso operacionales de administracion (AGR_ADMIN)

 @startuml

 left to right direction
 skinparam usecase {
   BackgroundColor White
   BorderColor #333333
 }
 skinparam actorBorderColor #555555
 skinparam shadowing false

 actor "system_admin\nAGR-010" as AGR_ADMIN

 rectangle "Administracion IACT" {
   usecase "Crear usuario" as CREAR_USUARIO
   usecase "Desactivar usuario\n(BR-009 v2.0.0)" as DESACTIVAR_USUARIO
   usecase "Asignar grupo RBAC\n(FunctionGroup/AccessGroup)" as ASIGNAR_GRUPO_RBAC
   usecase "Revocar grupo RBAC" as REVOCAR_GRUPO_RBAC
   usecase "Otorgar permiso temporal\n(CNST-031: max 6 meses)" as OTORGAR_PERMISO_TEMPORAL
   usecase "Revocar permiso temporal" as REVOCAR_PERMISO_TEMPORAL
   usecase "Ver sesiones activas" as VER_SESIONES_ACTIVAS
   usecase "Cerrar sesiones\n(view_all_active_sessions)" as CERRAR_SESIONES
   usecase "Ver reglas SoD\n(CNST-030)" as VER_REGLAS_SOD
   usecase "Ver audit log\n(CNST-025)" as VER_AUDIT_LOG
 }

 AGR_ADMIN --> CREAR_USUARIO
 AGR_ADMIN --> DESACTIVAR_USUARIO
 AGR_ADMIN --> ASIGNAR_GRUPO_RBAC
 AGR_ADMIN --> REVOCAR_GRUPO_RBAC
 AGR_ADMIN --> OTORGAR_PERMISO_TEMPORAL
 AGR_ADMIN --> REVOCAR_PERMISO_TEMPORAL
 AGR_ADMIN --> VER_SESIONES_ACTIVAS
 AGR_ADMIN --> CERRAR_SESIONES
 AGR_ADMIN --> VER_REGLAS_SOD
 AGR_ADMIN --> VER_AUDIT_LOG

 @enduml

Flujo de actividad — Alta de usuario
======================================

.. uml::
 :caption: Figura — Flujo de administracion: alta de usuario con asignacion RBAC

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
   if (¿Conflicto SoD detectado?) then (si)
     :Rechazar asignacion\n(CNST-030: enforcement SoD);
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
   - Separacion de funciones (SoD): el sistema impide asignar
     conjuntos de funciones en conflicto al mismo usuario.
     La separacion se evalua en tiempo de asignacion.
 * - **CNST-031**
   - Permisos temporales tienen rango obligatorio
     ``granted_at .. expires_at`` (maximo 6 meses). Requieren
     justificacion documentada.
 * - **CNST-003**
   - Un usuario solo puede tener una sesion activa simultanea.
     AGR_ADMIN puede cerrar sesiones activas de otros usuarios
     (``view_all_active_sessions``).
 * - **CNST-025**
   - Toda operacion de administracion genera un ``AuditEvent``
     inmutable (append-only). Sin excepciones.

.. seealso::

 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/normativa/restricciones/index`
 :doc:`system-configuration`
