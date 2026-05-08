.. meta::
 :artefacto: CNST_032
 :tipo: Restriccion
 :dominio: normativa
 :subdominio: restricciones
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-04-29
 :ultimo_cambio: 2026-05-07
 :autor: NestorMonroy
 :clasificacion: Critico

.. _cnst-032:

==========================================================
CNST-032: Menu como wrapper UX sobre Function (no fuente)
==========================================================

Resumen Ejecutivo
-----------------

.. list-table::
 :widths: 30 70
 :header-rows: 0

 * - **ID**
   - CNST_032
 * - **Categoria**
   - RBAC + UX
 * - **Tipo (TXM_01)**
   - Tecnica
 * - **Criticidad**
   - Critico
 * - **Negociable**
   - No
 * - **Estado**
   - Vigente
 * - **Version**
   - 2.0.0 (reescritura — ver §10 historial)

----

1. Definicion
=============

1.1 Enunciado
-------------

El menu UX del sistema IACT DEBE derivarse del catalogo
``Function`` (RBAC v5.6.0) via una capa wrapper persistida
``MenuItem`` con relacion 1:1 obligatoria a ``Function``. Esta
**prohibido** que el menu sea fuente de capability — la regla
de acceso vive **siempre** en ``Function`` (vinculada a
``AccessGroup`` via ``FunctionGroupMembership``).

1.2 Justificacion
-----------------

Sin esta restriccion, el sistema regresa al anti-patron legacy
``C_MENU2`` documentado en
``2026-05-06-21-42-06-menu-rbac-user-scope-docs/discover/cmenu2-legacy-archeology.md``,
donde el menu **era** la regla de acceso (un user veia el item
si y solo si tenia entrada en ``BD_MENU2``, sin verificacion
backend). Defense-in-depth roto: comprometer la tabla del menu
era equivalente a obtener acceso al endpoint.

CNST-032 v2.0.0 separa explicitamente:

- **Capa de autorizacion:** ``Function`` + ``AccessGroup`` +
  ``FunctionGroupMembership`` — **fuente** de la regla.
- **Capa UX persistida:** ``MenuItem`` 1:1 con ``Function`` —
  solo controla *"¿lo muestro en el sidebar?"*.

1.3 Origen
----------

- **Fuente:** ADR-BACK-008 (MenuItem como wrapper UX sobre
  Function).
- **Documento:** :doc:`/backend/adr-back-008-menuitem-wrapper-ux-sobre-function`.
- **WP:** ``2026-05-06-21-42-06-menu-rbac-user-scope-docs``.
- **Fecha v2.0.0:** 2026-05-07.

----

2. Especificacion Tecnica
=========================

2.1 Modelo obligatorio
----------------------

``MenuItem`` DEBE implementarse con los siguientes campos
minimos:

.. code-block:: python

   class MenuItem(models.Model):
       function = models.OneToOneField(
           Function,
           on_delete=models.PROTECT,    # NO CASCADE — auditable
           related_name="menu_item",
           # null=False, blank=False (default) — OBLIGATORIO
       )
       display_label = models.CharField(max_length=100)
       icon = models.CharField(max_length=100, blank=True)
       display_order = models.IntegerField(default=0)
       route_path = models.URLField(max_length=200)
       parent = models.ForeignKey(
           "self", null=True, blank=True,
           on_delete=models.SET_NULL,
       )
       status = models.CharField(
           max_length=20,
           choices=[
               ("DRAFT", "Borrador"),
               ("ACTIVE", "Activo"),
               ("DEPRECATED", "Deprecado"),
               ("ARCHIVED", "Archivado"),
           ],
           default="DRAFT",
       )

2.2 Endpoint canonico
---------------------

El frontend obtiene el menu via:

.. code-block:: text

   GET /api/v1/menu/
   Authorization: Bearer <jwt>

   200 OK
   {
     "capabilities": ["view_reports", "manage_menu_catalog", ...],
     "menu_items": [
       {
         "id": 12,
         "codename": "view_reports",
         "display_label": "Mis Reportes",
         "icon": "BarChartIcon",
         "route_path": "/reports",
         "display_order": 10,
         "parent_id": null,
         "status": "ACTIVE"
       }
     ]
   }

Estructura **flat**. Frontend reconstruye arbol via
``parent_id`` si necesita render anidado.

2.3 Invariantes obligatorias (I-1..I-4)
---------------------------------------

.. list-table::
 :widths: 8 35 57
 :header-rows: 1

 * - #
   - Invariante
   - Garantia
 * - I-1
   - Todo MenuItem tiene exactamente una Function asociada
   - ``OneToOneField(null=False)`` + DB unique constraint
 * - I-2
   - Borrar Function bloquea borrado del MenuItem
   - ``on_delete=PROTECT``
 * - I-3
   - Function puede existir sin MenuItem
   - OneToOne opcional desde el lado Function
 * - I-4
   - Desactivar Function (``is_active=False``) oculta MenuItem
   - filter en queryset manager (no signal)

----

3. Prohibiciones explicitas
===========================

3.1 PROHIBIDO — MenuItem standalone
-----------------------------------

``MenuItem`` con sus propios campos de capability (label como
permission name, codename propio que no exista en ``Function``,
status que controle acceso). Equivalente al Diseno A descrito
en ``discover/menuitem-standalone-vs-wrapper-clarification.md``
§1 — **regresion 1:1 a C_MENU2**.

.. code-block:: python

   # PROHIBIDO
   class MenuItem(models.Model):
       label = models.CharField(...)
       codename = models.CharField(...)  # no FK a Function
       route_path = models.URLField(...)
       status = models.CharField(...)
       # NO hay OneToOneField a Function

3.2 PROHIBIDO — Frontend que pinta sin verificar capability
-----------------------------------------------------------

El frontend NO puede pintar un item del menu sin verificar
que el usuario tenga la ``Function.codename`` correspondiente.
Pintar primero y verificar despues equivale a no verificar:
expone la existencia de items que el usuario no debe ver.

.. code-block:: typescript

   // PROHIBIDO
   const menuItems = ALL_NAV_LINKS.map(link => ({
     ...link, visible: true  // sin filtrar por capabilities
   }));

   // CORRECTO
   const menuItems = ALL_NAV_LINKS
     .filter(link => userCapabilities.has(link.codename));

3.3 PROHIBIDO — Endpoint protegido sin Function
-----------------------------------------------

Cada endpoint del backend protegido por ``MenuItem`` DEBE
estar respaldado por una ``Function`` activa. Endpoints que
existen solo porque un ``MenuItem`` los apunta (sin
``Function`` que los autorice) violan defense-in-depth.

3.4 PROHIBIDO — Jerarquia de permisos via parent
------------------------------------------------

``MenuItem.parent`` es **exclusivamente** override visual de
ordenamiento en el sidebar. NO implica herencia de permisos:
tener acceso al item padre NO da acceso a los items hijos
(cada uno requiere su propia ``Function``).

CNST-029 (modelo plano) preservado.

----

4. Impacto en Sistema
=====================

4.1 Modulos Afectados
---------------------

- **MOD_PERM:** UC_PERM_08 extension del endpoint
  ``GET /api/v1/menu/``.
- **MOD_Admin:** UC_ADM_04 (manage_menu_catalog), UC_ADM_05
  (manage_menu_lifecycle).
- **Frontend:** consumidor del endpoint + filtro
  ``ALL_NAV_LINKS`` por capabilities.

4.2 Casos de Uso Afectados
--------------------------

- UC_PERM_08 (Generar Menu Dinamico) — extendido con shape
  flat ``{capabilities, menu_items}``.
- UC_ADM_04 (Gestionar catalogo de MenuItems) — nuevo.
- UC_ADM_05 (Gestionar lifecycle de MenuItem) — nuevo.

4.3 Lo que NO se puede hacer
----------------------------

- Crear ``MenuItem`` sin ``Function`` asociada (rechazo a
  nivel DB por ``NOT NULL``).
- Borrar ``Function`` que tenga ``MenuItem`` (rechazo por
  ``PROTECT``).
- Renderizar item de menu sin verificar capability del user
  en frontend.
- Usar ``MenuItem`` como fuente de codename — la fuente es
  ``Function.codename``.

----

5. Business Rules Derivadas
===========================

- **BR-MENU-01:** todo MenuItem en estado ACTIVE con
  ``Function.is_active=True`` ES visible en
  ``GET /api/v1/menu/`` para users con la capability.
- **BR-MENU-02:** un MenuItem en DRAFT NO es visible en el
  endpoint para users finales (solo en preview admin).
- **BR-MENU-03:** un MenuItem en DEPRECATED es visible con
  flag ``status=DEPRECATED`` en la respuesta — frontend lo
  pinta con tag "(legacy)".
- **BR-MENU-04:** un MenuItem en ARCHIVED NO es visible en el
  endpoint; capability sigue accesible via URL directa.

----

6. Implementacion
=================

6.1 Codigo de referencia
------------------------

Ver:

- :doc:`/backend/adr-back-008-menuitem-wrapper-ux-sobre-function`
  (modelo + invariantes + tests).
- :doc:`/backend/adr-back-009-cache-capabilities-degraded-mode`
  (cache de capabilities consumidas por el endpoint).
- :doc:`/backend/adr-back-010-function-is-critical-governance`
  (bypass de cache para capabilities criticas).
- :doc:`/backend/rbac-implementation-guide` §Q9 (extension
  con MenuItem y UserCapabilityResolver).

6.2 Validacion de cumplimiento
------------------------------

.. code-block:: bash

   # Test guardrail I-1..I-4
   pytest apps/access/tests/test_menu_item.py -v

   # Verificar que todos los MenuItem tienen Function activa
   python manage.py shell -c "
   from apps.access.models import MenuItem
   orphans = MenuItem.objects.filter(function__isnull=True)
   assert not orphans.exists(), f'I-1 violated: {orphans}'
   "

----

7. Excepciones
==============

7.1 Excepciones permitidas
--------------------------

- **Items en DRAFT** son invisibles al user final pero
  persisten en DB. No es excepcion — es parte del lifecycle.
- **MenuItems con `block_auto_archive=True`** sobreviven al
  job de auto-archive a 90d en DEPRECATED. Requiere
  `block_reason` y entrada en audit log (ver
  :doc:`/backend/adr-back-009-cache-capabilities-degraded-mode`
  y UC_ADM_05).

7.2 No se permiten excepciones a 3.1, 3.2, 3.3, 3.4
---------------------------------------------------

Las prohibiciones son absolutas. Cualquier propuesta de
excepcion requiere RFC y ADR explicito que justifique por
que el caso no es regresion al anti-patron legacy.

----

8. Trazabilidad
===============

- ADR-BACK-008 — modelo MenuItem wrapper UX (decision
  arquitectonica).
- ADR-BACK-009 — cache de capabilities (consumidor del
  endpoint).
- ADR-BACK-010 — governance ``is_critical`` (capabilities
  criticas bypassean cache).
- CNST-029 — RBAC modelo plano (compatible).
- ADR-BACK-001 — grupos sin jerarquia (compatible — parent
  es UI).
- ADR-BACK-007 — RBAC custom (compatible).
- STD-010 — vocabulario abstracto (cumplido en narrativa
  UC).

----

9. WP de origen
===============

- ``2026-05-06-21-42-06-menu-rbac-user-scope-docs`` —
  analisis y decisiones P1-P4.
- ``2026-05-06-23-25-08-std-010-corpus-compliance`` —
  alineacion narrativa con STD-010.

----

10. Historial de versiones
==========================

.. list-table::
 :widths: 12 12 20 56
 :header-rows: 1

 * - Version
   - Fecha
   - Autor
   - Cambios
 * - 1.0.0
   - 2026-04-29
   - NestorMonroy
   - Version inicial — menu dinamico via ``obtener_menu_usuario(user_id)``
 * - 2.0.0
   - 2026-05-07
   - NestorMonroy
   - Reescritura completa. Cambia el modelo conceptual: el
     menu ya no es resultado de una funcion SQL ad-hoc sino
     un wrapper UX persistido (``MenuItem``) 1:1 sobre
     ``Function``. Endpoint canonico:
     ``GET /api/v1/menu/`` con shape flat
     ``{capabilities, menu_items}``. Prohibiciones explicitas
     (3.1-3.4) que clausuran el anti-patron Diseno A standalone
     y la regresion a ``C_MENU2``.
