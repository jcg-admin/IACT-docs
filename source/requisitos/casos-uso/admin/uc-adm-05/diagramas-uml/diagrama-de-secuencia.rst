.. meta::
 :artefacto: UC_ADM_05_SEQ
 :tipo: Diagrama UML
 :dominio: requisitos
 :subdominio: casos_uso/admin
 :estado: Borrador
 :version: 1.0.0

8.2 Diagrama de Secuencia — Auto-archive (FA-04)
=================================================

.. uml::

   @startuml

   actor "Planificador de Tareas" as PlanificadorTareas
   participant "Servicio de Aplicacion" as SvcAplicacion
   database   "Almacen de Datos" as AlmacenDatos
   participant "Servicio de Cache" as SvcCache
   database   "Audit Log" as AuditLog
   participant "Internal Mailbox" as InternalMailbox

   PlanificadorTareas -> SvcAplicacion: ejecutar job auto_archive_menu_items()
   SvcAplicacion -> AlmacenDatos: SELECT * WHERE status='DEPRECATED'\n  AND deprecated_at < now()-90d\n  AND block_auto_archive=False
   AlmacenDatos --> SvcAplicacion: lista de N items

   loop por cada item
     group Transaccion atomica
       SvcAplicacion -> AlmacenDatos: UPDATE menu_items\nSET status='ARCHIVED',\n    archived_at=now()
       SvcAplicacion -> AuditLog: registrar LIFECYCLE_AUTO_ARCHIVED\n  (actor='system', days_in_deprecated)
     end
     SvcAplicacion -> SvcCache: invalidar menu:user:{ids}
     alt cache OK
       SvcCache --> SvcAplicacion: ok
     else cache fail
       SvcAplicacion -> AuditLog: CACHE_INVALIDATION_FAILED
     end
   end

   SvcAplicacion -> AlmacenDatos: SELECT items con\n  deprecated_at >= now()-90d\n  AND deprecated_at < now()-80d\n  AND block_auto_archive=False
   AlmacenDatos --> SvcAplicacion: lista pre-archive (10d window)
   SvcAplicacion -> InternalMailbox: warning "auto-archive en 10d"\n  a system_admin
   SvcAplicacion -> InternalMailbox: resumen del job\n  (success_count, failure_count)

   SvcAplicacion --> PlanificadorTareas: job ok\n  {archived: N, warned: M}

   @enduml
