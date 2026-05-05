.. meta::
 :artefacto: AT_DESIGN_MOD_PERMISSIONS
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_mod_permissions:

===================================================
Design View — MOD_Permissions: Permisos RBAC
===================================================

Patron de interaccion del modulo de gestion RBAC. Muestra el flujo
de otorgamiento de ``ExceptionalPermission`` con validacion del rango
temporal (CNST-031) y registro de ``AuditEvent(PERMISSION_GRANT)``.

.. uml::
 :caption: Design View MOD_Permissions — otorgamiento de permiso excepcional temporal.

 @startuml

 actor AGR_ADMIN

 participant InterfazAdmin                <<frontend>>
 participant ServicioPermisos             <<api>>
 participant RepositorioExceptionalPerm   <<repository>>
 database    AlmacenDatos                 <<postgresql>>

 AGR_ADMIN -> InterfazAdmin : POST /permissions/exceptional\n{user_id, function_id,\n expires_at, justification}
 activate InterfazAdmin

 InterfazAdmin -> ServicioPermisos : otorgarPermisoExcepcional(datos)
 activate ServicioPermisos

 ServicioPermisos -> ServicioPermisos : validarRangoTemporal(\n  granted_at, expires_at)\n<<CNST-031>>

 alt expires_at <= granted_at
   ServicioPermisos --> InterfazAdmin : 400 rango temporal invalido
 else rango valido
   ServicioPermisos -> RepositorioExceptionalPerm : crear(ExceptionalPermission{\n  permission_id:UUID,\n  user_id,\n  function_id,\n  granted_by,\n  granted_at,\n  expires_at,\n  justification,\n  state:PermissionState.ACTIVE\n})
   activate RepositorioExceptionalPerm
   RepositorioExceptionalPerm -> AlmacenDatos : INSERT exceptional_permissions
   AlmacenDatos --> RepositorioExceptionalPerm : OK
   RepositorioExceptionalPerm --> ServicioPermisos : ExceptionalPermission
   deactivate RepositorioExceptionalPerm

   ServicioPermisos -> AlmacenDatos : INSERT audit_events\n{event_type:PERMISSION_GRANT,\n details:{function_id, expires_at}}
   AlmacenDatos --> ServicioPermisos : AuditEvent registrado

   ServicioPermisos --> InterfazAdmin : 201 Created {permission_id}
 end

 deactivate ServicioPermisos
 InterfazAdmin --> AGR_ADMIN : confirmacion
 deactivate InterfazAdmin

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/arquitectura-tecnica/domain-model/exceptional-permission`
 :doc:`/arquitectura-tecnica/domain-model/function`
 :doc:`/arquitectura-tecnica/domain-model/audit-event`
