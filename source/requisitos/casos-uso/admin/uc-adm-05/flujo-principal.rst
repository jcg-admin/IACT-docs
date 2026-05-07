.. meta::
 :artefacto: UC_ADM_05_FLUJO
 :tipo: Caso de Uso (seccion)
 :dominio: requisitos
 :subdominio: casos_uso/admin
 :estado: Borrador
 :version: 1.0.0

==========================
3. Flujo Principal
==========================

Caso: invoker con ``manage_menu_lifecycle`` ejecuta la
transicion **DRAFT → ACTIVE** (publicar) — la mas comun.

::

   PASO 1   Invoker abre detalle del MenuItem en DRAFT  (Interfaz de Usuario)
   PASO 2   Selecciona "Publicar"                       (Interfaz de Usuario)
   PASO 3   Confirma con dialog (revision de
            metadata: label, route, icon)               (Interfaz de Usuario)
   PASO 4   POST /api/v1/admin/menu-items/{id}/publish/  (Interfaz de Usuario → Servicio de Aplicacion)
   PASO 5   Verificar capability con bypass de cache    (Servicio de Aplicacion)
   PASO 6   Validar MenuItem existe                      (Servicio de Aplicacion → Almacen de Datos)
   PASO 7   Validar status_actual = DRAFT                (Servicio de Aplicacion)
   PASO 8   Validar Function asociada is_active=True     (Servicio de Aplicacion → Almacen de Datos)
   PASO 9   BEGIN TRANSACTION                            (Servicio de Aplicacion)
   PASO 10  UPDATE menu_items
            SET status='ACTIVE', deprecated_at=NULL,
                archived_at=NULL, block_auto_archive=False,
                block_reason='', updated_at=now()        (Servicio de Aplicacion → Almacen de Datos)
   PASO 11  Registrar AuditEvent
            (LIFECYCLE_TRANSITION DRAFT->ACTIVE)         (Servicio de Aplicacion → Almacen de Datos)
   PASO 12  COMMIT                                       (Servicio de Aplicacion)
   PASO 13  Invalidar cache de menu post-COMMIT          (Servicio de Aplicacion → Servicio de Cache)
   PASO 14  Responder 200 OK con MenuItem actualizado    (Servicio de Aplicacion → Interfaz de Usuario)
   PASO 15  Mostrar confirmacion + actualizar UI         (Interfaz de Usuario)

3.1 Detalles por paso
=====================

PASO 5 — Verificacion bypass de cache
-------------------------------------

``manage_menu_lifecycle.is_critical=True``. La verificacion
consulta DB sin cache (AP-2b — strong consistency).

PASO 7 — Validar transicion valida
----------------------------------

Tabla de transiciones validas:

.. list-table::
 :widths: 25 25 50
 :header-rows: 1

 * - From
   - To
   - Endpoint
 * - DRAFT
   - ACTIVE
   - ``POST .../publish/``
 * - ACTIVE
   - DEPRECATED
   - ``POST .../deprecate/``
 * - DEPRECATED
   - ACTIVE
   - ``POST .../reactivate/``
 * - DEPRECATED
   - ARCHIVED
   - ``POST .../archive/``
 * - ARCHIVED
   - ACTIVE
   - ``POST .../reactivate/``

Transiciones no listadas son **invalidas** y rechazadas
con 409 Conflict (EX-02).

PASO 10 — UPDATE con campos derivados
-------------------------------------

Cada transicion modifica campos especificos:

.. list-table::
 :widths: 25 25 50
 :header-rows: 1

 * - Transicion
   - deprecated_at
   - archived_at
 * - DRAFT → ACTIVE
   - NULL
   - NULL
 * - ACTIVE → DEPRECATED
   - now()
   - sin cambio
 * - DEPRECATED → ACTIVE
   - NULL (limpia)
   - sin cambio
 * - DEPRECATED → ARCHIVED
   - sin cambio
   - now()
 * - ARCHIVED → ACTIVE
   - NULL (limpia)
   - NULL (limpia)

Adicionalmente, cualquier transicion a ACTIVE limpia
``block_auto_archive=False``, ``block_reason=""``,
``block_set_by=NULL``, ``block_set_at=NULL`` (porque el
flag solo aplica en DEPRECATED).

PASO 13 — Invalidacion de cache
-------------------------------

Si la transicion afecta visibilidad (DRAFT→ACTIVE,
ACTIVE→DEPRECATED, etc.), invalidar
``menu:user:{id}`` para todos los users con la capability
subyacente. La transicion ``ACTIVE → DEPRECATED`` cambia
el ``status`` en la respuesta del endpoint —
imprescindible invalidar.

3.2 Variantes documentadas en flujos alternos
=============================================

Las otras 5 transiciones siguen el mismo patron con
endpoints diferenciados. Ver
:doc:`flujos-alternos`.
