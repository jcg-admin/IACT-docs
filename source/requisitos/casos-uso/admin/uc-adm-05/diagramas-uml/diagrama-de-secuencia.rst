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

   actor "Planificador de Tareas" as Sched
   participant "Servicio de Aplicacion" as Svc
   database   "Almacen de Datos" as DB
   participant "Servicio de Cache" as Cache
   database   "Audit Log" as Audit
   participant "Servicio de Notificacion" as Notif

   Sched -> Svc: ejecutar job auto_archive_menu_items()
   Svc -> DB: SELECT * WHERE status='DEPRECATED'\n  AND deprecated_at < now()-90d\n  AND block_auto_archive=False
   DB --> Svc: lista de N items

   loop por cada item
     group Transaccion atomica
       Svc -> DB: UPDATE menu_items\nSET status='ARCHIVED',\n    archived_at=now()
       Svc -> Audit: registrar LIFECYCLE_AUTO_ARCHIVED\n  (actor='system', days_in_deprecated)
     end
     Svc -> Cache: invalidar menu:user:{ids}
     alt cache OK
       Cache --> Svc: ok
     else cache fail
       Svc -> Audit: CACHE_INVALIDATION_FAILED
     end
   end

   Svc -> DB: SELECT items con\n  deprecated_at >= now()-90d\n  AND deprecated_at < now()-80d\n  AND block_auto_archive=False
   DB --> Svc: lista pre-archive (10d window)
   Svc -> Notif: warning "auto-archive en 10d"\n  a system_admin
   Svc -> Notif: resumen del job\n  (success_count, failure_count)

   Svc --> Sched: job ok\n  {archived: N, warned: M}

   @enduml
