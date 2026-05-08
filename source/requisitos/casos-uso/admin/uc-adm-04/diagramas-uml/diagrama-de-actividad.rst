.. meta::
 :artefacto: UC_ADM_04_ACT
 :tipo: Diagrama UML
 :dominio: requisitos
 :subdominio: casos_uso/admin
 :estado: Borrador
 :version: 1.0.0

8.2 Diagrama de Actividad — CREATE MenuItem
============================================

.. uml::

   @startuml

   start
   :Invoker abre catalogo de MenuItems;
   :Selecciona "Crear MenuItem";
   :Selecciona Function (codename, name);
   :Define metadata UX
   (label, icon, route, order, parent);
   :POST /api/v1/admin/menu-items/;

   :Verificar capability
   manage_menu_catalog (bypass cache);
   if (Capability presente?) then (no)
     :403 Forbidden;
     stop
   else (si)
   endif

   :Validar Function existe + activa;
   if (Function valida?) then (no)
     :422 Unprocessable Entity;
     stop
   else (si)
   endif

   :Validar Function sin MenuItem previo (I-1);
   if (Sin previo?) then (no)
     :409 Conflict (sugerir UPDATE);
     stop
   else (si)
   endif

   :Validar parent (si aplica);
   if (Parent valido y NOT ARCHIVED?) then (no)
     :422 (parent_archived);
     stop
   else (si)
   endif

   :BEGIN TRANSACTION;
   :INSERT menu_items (status=DRAFT);
   :Registrar AuditEvent;
   :COMMIT;

   :Invalidar cache (post-COMMIT);
   if (Cache OK?) then (si)
   else (no)
     :Log + telemetria
     (degraded mode);
   endif

   :201 Created;
   stop

   @enduml
