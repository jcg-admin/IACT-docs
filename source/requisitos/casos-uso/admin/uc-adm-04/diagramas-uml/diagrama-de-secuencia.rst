.. meta::
 :artefacto: UC_ADM_04_SEQ
 :tipo: Diagrama UML
 :dominio: requisitos
 :subdominio: casos_uso/admin
 :estado: Borrador
 :version: 1.0.0

8.1 Diagrama de Secuencia — CREATE MenuItem
============================================

.. uml::

   @startuml

   actor "manage_menu_catalog" as manage_menu_catalog
   participant "Interfaz de Usuario" as InterfazDeUsuario
   participant "Servicio de Aplicacion" as SvcAplicacion
   database   "Almacen de Datos" as AlmacenDatos
   participant "Servicio de Cache" as SvcCache
   database   "Audit Log" as AuditLog

   manage_menu_catalog -> InterfazDeUsuario: Crea MenuItem
   InterfazDeUsuario -> SvcAplicacion: POST /api/v1/admin/menu-items/
   SvcAplicacion -> SvcAplicacion: Verificar capability (bypass cache)
   SvcAplicacion -> AlmacenDatos: Validar Function existe + activa
   AlmacenDatos --> SvcAplicacion: ok
   SvcAplicacion -> AlmacenDatos: Validar Function sin MenuItem previo
   AlmacenDatos --> SvcAplicacion: ok (I-1)
   SvcAplicacion -> AlmacenDatos: Validar parent (si aplica)
   AlmacenDatos --> SvcAplicacion: ok

   group Transaccion atomica
     SvcAplicacion -> AlmacenDatos: INSERT menu_items (status=DRAFT)
     SvcAplicacion -> AuditLog: registrar MENU_ITEM_CREATED
   end

   SvcAplicacion -> SvcCache: invalidar menu:user:{ids} (post-COMMIT)
   alt cache OK
     SvcCache --> SvcAplicacion: ok
   else cache fail
     SvcCache --> SvcAplicacion: error
     SvcAplicacion -> AuditLog: CACHE_INVALIDATION_FAILED
     SvcAplicacion -> SvcAplicacion: metric +1 (degraded mode)
   end

   SvcAplicacion --> InterfazDeUsuario: 201 Created + MenuItem
   InterfazDeUsuario --> manage_menu_catalog: confirmacion + preview admin

   @enduml
