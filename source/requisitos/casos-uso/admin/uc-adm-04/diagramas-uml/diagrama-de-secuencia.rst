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

   actor "manage_menu_catalog" as Actor
   participant "Interfaz de Usuario" as UI
   participant "Servicio de Aplicacion" as Svc
   database   "Almacen de Datos" as DB
   participant "Servicio de Cache" as Cache
   database   "Audit Log" as Audit

   Actor -> UI: Crea MenuItem
   UI -> Svc: POST /api/v1/admin/menu-items/
   Svc -> Svc: Verificar capability (bypass cache)
   Svc -> DB: Validar Function existe + activa
   DB --> Svc: ok
   Svc -> DB: Validar Function sin MenuItem previo
   DB --> Svc: ok (I-1)
   Svc -> DB: Validar parent (si aplica)
   DB --> Svc: ok

   group Transaccion atomica
     Svc -> DB: INSERT menu_items (status=DRAFT)
     Svc -> Audit: registrar MENU_ITEM_CREATED
   end

   Svc -> Cache: invalidar menu:user:{ids} (post-COMMIT)
   alt cache OK
     Cache --> Svc: ok
   else cache fail
     Cache --> Svc: error
     Svc -> Audit: CACHE_INVALIDATION_FAILED
     Svc -> Svc: metric +1 (degraded mode)
   end

   Svc --> UI: 201 Created + MenuItem
   UI --> Actor: confirmacion + preview admin

   @enduml
