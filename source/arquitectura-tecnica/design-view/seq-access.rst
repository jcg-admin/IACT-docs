.. meta::
 :artefacto: AT_DESIGN_MOD_ACCESS
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_mod_access:

=================================================
Design View — MOD_Access: Control de Acceso RBAC
=================================================

Patron de interaccion del modulo de control de acceso. Muestra la
asignacion de ``FunctionGroup`` a un usuario con verificacion de
``SeparationRule`` (SoD) antes de crear el ``Assignment``.

.. uml::
 :caption: Design View MOD_Access — asignacion con verificacion SoD.

 @startuml

 actor AGR_ADMIN

 participant InterfazAdmin        <<frontend>>
 participant ServicioAcceso       <<api>>
 participant ServicioRBAC         <<domain>>
 participant RepositorioAssignment <<repository>>
 database    AlmacenDatos         <<postgresql>>

 AGR_ADMIN -> InterfazAdmin : POST /access/assignments\n{user_id, group_ref, expires_at}
 activate InterfazAdmin

 InterfazAdmin -> ServicioAcceso : asignarGrupo(user_id, group_ref, expires_at)
 activate ServicioAcceso

 ServicioAcceso -> ServicioRBAC : verificarSoD(user_id, group_ref)
 activate ServicioRBAC
 ServicioRBAC -> AlmacenDatos : SELECT separation_rules\nWHERE estado=ENABLED
 AlmacenDatos --> ServicioRBAC : List<SeparationRule>
 ServicioRBAC -> AlmacenDatos : SELECT assignments\nWHERE user_id=? AND state=ACTIVE
 AlmacenDatos --> ServicioRBAC : asignaciones actuales
 ServicioRBAC --> ServicioAcceso : resultado SoD check
 deactivate ServicioRBAC

 alt conflicto SoD detectado
   ServicioAcceso --> InterfazAdmin : 422 SoD Violation
 else sin conflicto
   ServicioAcceso -> RepositorioAssignment : crear(Assignment{\n  assignment_id:UUID,\n  user_id,\n  group_ref,\n  assigned_by,\n  expires_at,\n  state:AssignmentState.ACTIVE\n})
   activate RepositorioAssignment
   RepositorioAssignment -> AlmacenDatos : INSERT assignments
   AlmacenDatos --> RepositorioAssignment : OK
   RepositorioAssignment --> ServicioAcceso : Assignment
   deactivate RepositorioAssignment

   ServicioAcceso -> AlmacenDatos : INSERT audit_events\n{event_type:ACCESS_CHANGE}
   AlmacenDatos --> ServicioAcceso : AuditEvent registrado

   ServicioAcceso --> InterfazAdmin : 201 Created {assignment_id}
 end

 deactivate ServicioAcceso
 InterfazAdmin --> AGR_ADMIN : confirmacion
 deactivate InterfazAdmin

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/arquitectura-tecnica/domain-model/assignment`
 :doc:`/arquitectura-tecnica/domain-model/separation-rule`
 :doc:`/arquitectura-tecnica/domain-model/audit-event`
