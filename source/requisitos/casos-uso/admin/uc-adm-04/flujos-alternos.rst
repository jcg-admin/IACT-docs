.. meta::
 :artefacto: UC_ADM_04_ALT
 :tipo: Caso de Uso (seccion)
 :dominio: requisitos
 :subdominio: casos_uso/admin
 :estado: Borrador
 :version: 1.0.0

=========================
4. Flujos Alternos
=========================

4.1 FA-01: Function ya tiene MenuItem (CREATE)
==============================================

**Cuando:** PASO 9 detecta que la ``Function`` seleccionada
ya tiene un ``MenuItem`` asociado.

**Justificacion:** I-1 prohibe dos ``MenuItem`` para la misma
``Function`` (OneToOneField).

**Pasos:**

::

   PASO 9A    Detectar MenuItem existente para
              la Function seleccionada                (Servicio de Aplicacion)
   PASO 9B    Responder 409 Conflict con
              {existing_menu_item_id}                 (Servicio de Aplicacion → Interfaz de Usuario)
   PASO 9C    Sugerir UPDATE en lugar de CREATE       (Interfaz de Usuario)

**Postcondiciones:**

- Sin cambios en DB.
- Sin audit event.

4.2 FA-02: Update parcial de metadata UX
========================================

**Cuando:** invoker quiere cambiar solo el ``display_label``
de un ``MenuItem`` existente sin tocar otros campos.

**Pasos:**

::

   PASO 1    PATCH /api/v1/admin/menu-items/{id}/
             {"display_label": "Nuevo Label"}        (Interfaz de Usuario → Servicio de Aplicacion)
   PASO 2    Verificar capability (bypass cache)     (Servicio de Aplicacion)
   PASO 3    Validar MenuItem existe                  (Servicio de Aplicacion → Almacen de Datos)
   PASO 4    Validar status NOT ARCHIVED              (Servicio de Aplicacion)
   PASO 5    UPDATE menu_items SET display_label=?
             WHERE id=?                                (Servicio de Aplicacion → Almacen de Datos)
   PASO 6    Audit event MENU_ITEM_UPDATED con
             diff de campos                           (Servicio de Aplicacion → Almacen de Datos)
   PASO 7    COMMIT                                   (Servicio de Aplicacion)
   PASO 8    Invalidar cache de menu post-COMMIT      (Servicio de Aplicacion → Servicio de Cache)
   PASO 9    Responder 200 OK                         (Servicio de Aplicacion → Interfaz de Usuario)

4.3 FA-03: Reorganizar jerarquia visual (parent)
================================================

**Cuando:** invoker mueve un ``MenuItem`` bajo otro parent
o lo lleva a top-level.

**Validaciones especificas:**

- ``parent`` no es el mismo item (no auto-referencia).
- ``parent`` no genera ciclo (validar via traversal).
- ``parent`` no esta ARCHIVED.

**Pasos:**

::

   PASO 1    PATCH .../menu-items/{id}/
             {"parent_id": <new_parent_id>}          (Interfaz de Usuario)
   PASO 2-4  Identicos a FA-02
   PASO 5    Validar nueva jerarquia es DAG           (Servicio de Aplicacion)
             (no ciclos)
   PASO 6    UPDATE + audit + invalidacion            (mismo patron)

4.4 FA-04: Listar MenuItems con filtros
=======================================

**Cuando:** invoker explora el catalogo.

**Pasos:**

::

   PASO 1    GET /api/v1/admin/menu-items/
             ?status=DRAFT&module=ADM
             &include_archived=false                 (Interfaz de Usuario)
   PASO 2    Verificar capability (bypass cache)     (Servicio de Aplicacion)
   PASO 3    Query con filtros + select_related
             ('function')                            (Servicio de Aplicacion → Almacen de Datos)
   PASO 4    Responder lista paginada                 (Servicio de Aplicacion → Interfaz de Usuario)

**Notas:**

- Sin invalidacion de cache (operacion read-only).
- Default page_size=50, max=200.
- Sin audit event (solo READ).

4.5 FA-05: Bulk reorder por display_order
=========================================

**Cuando:** invoker arrastra y suelta multiples items para
reordenarlos en una sola operacion.

**Pasos:**

::

   PASO 1    PATCH /api/v1/admin/menu-items/bulk-reorder/
             [{"id": 12, "display_order": 10},
              {"id": 14, "display_order": 20}, ...]  (Interfaz de Usuario)
   PASO 2    Verificar capability (bypass cache)     (Servicio de Aplicacion)
   PASO 3    Validar todos los IDs existen           (Servicio de Aplicacion → Almacen de Datos)
   PASO 4    BEGIN TRANSACTION                        (Servicio de Aplicacion)
   PASO 5    UPDATE multi-row con CASE WHEN
             id=? THEN ?                              (Servicio de Aplicacion → Almacen de Datos)
   PASO 6    Audit event MENU_ITEM_BULK_REORDERED
             con lista de cambios                    (Servicio de Aplicacion → Almacen de Datos)
   PASO 7    COMMIT                                   (Servicio de Aplicacion)
   PASO 8    Invalidacion de cache (todos los users
             con cualquiera de las capabilities)     (Servicio de Aplicacion → Servicio de Cache)
   PASO 9    Responder 200 OK                         (Servicio de Aplicacion → Interfaz de Usuario)
