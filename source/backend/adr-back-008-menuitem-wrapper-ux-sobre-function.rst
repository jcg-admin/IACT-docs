.. meta::
 :artefacto: ADR-BACK-008
 :tipo: ADR
 :dominio: backend
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-07
 :ultimo_cambio: 2026-05-07
 :autor: NestorMonroy
 :clasificacion: Interno

.. _adr-back-008:

============================================================================
ADR-BACK-008: MenuItem como wrapper UX sobre Function
============================================================================

Estado y metadata
=================

- **Estado:** Aprobada.
- **Fecha:** 2026-05-07.
- **Decisores:** NestorMonroy (ejecutor) + analisis documentado en WP
  ``2026-05-06-21-42-06-menu-rbac-user-scope-docs``.
- **Contexto tecnico:** Backend — modelo de datos RBAC v5.6.0 +
  capa UX persistida del menu IACT.
- **Relacionados:**

  - :doc:`/backend/adr-back-001-grupos-funcionales-sin-jerarquia`
    — modelo flat sin herencia (compatible).
  - :doc:`/backend/adr-back-007-rbac-custom-vs-auth-group`
    — RBAC custom (compatible).
  - :doc:`/backend/adr-back-009-cache-capabilities-degraded-mode`
    — politica de cache que consume MenuItem (caps:user e
    menu:user invalidados en transiciones de UC_ADM_05).
  - :doc:`/backend/adr-back-010-function-is-critical-governance`
    — ``manage_menu_catalog`` y ``manage_menu_lifecycle``
    (caps de UC_ADM_04/05) son ``is_critical=True``, bypass
    de cache (AP-2b).
  - :doc:`/normativa/restricciones/cnst-029-rbac-modelo-plano`.
  - :doc:`/normativa/restricciones/cnst-032-menu-dinamico-obligatorio`
    (a reescribir en CNST-032 v2.0.0 con prohibicion explicita
    de Diseno A standalone).
  - :doc:`/requisitos/casos-uso/permissions/uc-perm-08/index`
    (extension del endpoint ``GET /api/v1/menu/``).

- **Refs WP discover:**

  - ``discover/lifecycle-managed-menu-vs-static-analysis.md`` (Opcion 2 elegida).
  - ``discover/menuitem-standalone-vs-wrapper-clarification.md`` (I-1..I-4).
  - ``discover/menuitem-design-corrections-v2.md`` (G-1..G-4).
  - ``discover/cmenu2-legacy-archeology.md`` (anti-patron a evitar).
  - ``discover/final-decisions-p1-p4-and-pending-items.md`` (P1).

----

1. Contexto y Problema
======================

El proyecto IACT v5.6.0 deriva el menu UX a partir del catalogo
RBAC: la regla **"si el usuario tiene la capability X, ve el item
de menu de X"** es la traduccion canonica de capability a render.

El sistema legacy resolvia esto con dos tablas (``C_MENU2``,
``BD_MENU2``) donde el menu **era** la regla de acceso: si un
``BD_MENU2.ID_USR`` apuntaba al item, el usuario lo veia y podia
acceder al endpoint asociado. **Defense-in-depth roto** — el menu
era simultaneamente capa UX y capa de autorizacion.

v5.6.0 introduce ``Function`` (capability) y ``AccessGroup`` (AGR)
como fuentes unicas de la regla de acceso. Falta decidir como
modelar la **capa UX persistida** (display label, icono, route
path, orden, estado de catalogo) sin reintroducir el anti-patron.

**Pregunta arquitectonica:**

¿``MenuItem`` debe ser una entidad standalone con sus propios
campos de identidad y estado, o debe ser un wrapper UX
estrictamente derivado de ``Function``?

----

2. Factores de Decision
=======================

- **Defense-in-depth:** que el endpoint protegido siempre tenga
  una ``Function`` que lo respalde.
- **Modelo flat sin jerarquia** (CNST-029, ADR-BACK-001).
- **Lifecycle gestionado** del catalogo UX (DRAFT → ACTIVE →
  DEPRECATED → ARCHIVED) sin afectar la capability subyacente.
- **Independencia de fuente:** ``Function`` puede existir sin
  item de menu (e.g., ``manage_own_state`` no aparece en
  sidebar pero la capability es real).
- **No regresar al anti-patron** ``C_MENU2``.
- **Compatibilidad con ``ALL_NAV_LINKS`` frontend** (P2 del WP).

----

3. Decision
===========

``MenuItem`` se modela como **wrapper UX 1:1 sobre ``Function``**.
La relacion es ``OneToOneField(Function, on_delete=PROTECT)``,
obligatoria desde el lado ``MenuItem``, opcional desde el lado
``Function``.

3.1 Modelo canonico
-------------------

.. code-block:: python

   class MenuItem(models.Model):
       function = models.OneToOneField(
           Function,
           on_delete=models.PROTECT,
           related_name="menu_item",
       )
       display_label = models.CharField(max_length=100)
       icon = models.CharField(max_length=100, blank=True)
       display_order = models.IntegerField(default=0)
       route_path = models.URLField(max_length=200)
       parent = models.ForeignKey(
           "self", null=True, blank=True,
           on_delete=models.SET_NULL,
           related_name="children",
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
       deprecated_at = models.DateTimeField(null=True, blank=True)
       archived_at = models.DateTimeField(null=True, blank=True)
       block_auto_archive = models.BooleanField(default=False)
       block_reason = models.CharField(max_length=500, blank=True, default="")
       block_set_by = models.ForeignKey(
           User, null=True, blank=True,
           on_delete=models.PROTECT,
           related_name="menu_items_archive_blocked",
       )
       block_set_at = models.DateTimeField(null=True, blank=True)
       created_at = models.DateTimeField(auto_now_add=True)
       updated_at = models.DateTimeField(auto_now=True)
       created_by = models.ForeignKey(
           User, on_delete=models.PROTECT,
           related_name="menu_items_created",
       )

       class Meta:
           db_table = "menu_items"
           ordering = ("display_order",)
           indexes = [
               models.Index(fields=("status",)),
               models.Index(fields=("status", "display_order")),
               models.Index(fields=("deprecated_at",)),
           ]

3.2 Invariantes (I-1..I-4)
--------------------------

.. list-table::
 :widths: 8 35 57
 :header-rows: 1

 * - #
   - Invariante
   - Como se garantiza
 * - I-1
   - Todo MenuItem tiene exactamente una Function
   - ``OneToOneField(null=False, blank=False)`` + DB unique constraint
 * - I-2
   - Borrar Function bloquea borrado del MenuItem
   - ``on_delete=PROTECT`` (correctivo respecto a v1 que proponia CASCADE)
 * - I-3
   - Function puede existir sin MenuItem
   - OneToOne accesible via ``function.menu_item`` con ``DoesNotExist`` si no existe
 * - I-4
   - Desactivar Function (``is_active=False``) oculta MenuItem
   - filter del queryset manager (no signal) — ``MenuItem.objects.visible()``

3.3 Por que ``on_delete=PROTECT`` y no ``CASCADE``
--------------------------------------------------

La version inicial del diseno proponia ``CASCADE``. Tras revision
G-2 del WP, se cambio a ``PROTECT`` por dos razones:

(a) **Auditabilidad:** un Function que tuvo MenuItem no debe ser
    borrado silenciosamente — el admin debe explicitamente
    archivar el MenuItem antes de borrar la Function.

(b) **Defense-in-depth:** ``PROTECT`` previene un borrado
    accidental que dejaria endpoints sin capability. El admin
    debe hacer la transicion de estado (``status=ARCHIVED``)
    antes de remover la Function.

3.4 Render: filtro en queryset (no signal)
------------------------------------------

I-4 (visibilidad) se implementa con un manager / queryset, no con
``post_save`` signal:

.. code-block:: python

   class MenuItemQuerySet(models.QuerySet):
       def visible(self):
           return self.filter(
               status="ACTIVE",
               function__is_active=True,
           )

       def for_user(self, user):
           codenames = UserCapabilityResolver.resolve(user)
           return self.visible().filter(
               function__codename__in=codenames,
           )

Razones:

- Los signals son frágiles ante bulk operations
  (``Function.objects.update(...)`` no dispara ``post_save``).
- El queryset es la fuente de verdad transaccional —
  refleja el estado real al momento de la consulta.
- Composable con otros filtros (parent, scope, etc.).

----

4. Consecuencias
================

4.1 Positivas
-------------

- **Defense-in-depth** preservado: ``Function`` es siempre la
  fuente de verdad de la capability.
- **Lifecycle UX** independiente de la capability — admin puede
  preparar items (DRAFT) o deprecarlos (DEPRECATED) sin tocar
  el catalogo de Functions.
- **Compatible con ``ALL_NAV_LINKS`` frontend** — el endpoint
  ``GET /api/v1/menu/`` retorna flat ``{capabilities,
  menu_items}``.
- **CNST-029 preservado** — ``parent`` es solo override visual,
  no jerarquia de permisos.
- **No reintroduce ``C_MENU2``** — el menu nunca es la regla.

4.2 Negativas (aceptadas)
-------------------------

- **Mas tablas** — ``MenuItem`` se suma a ``Function``,
  ``AccessGroup``, ``FunctionGroupMembership``,
  ``UserAccessGroupAssignment``, ``FunctionSeparationRule``.
  Mitigacion: el dominio (catalogo lifecycle-gestionado) lo
  justifica.

- **Doble paso de creacion** — admin debe crear ``Function``
  primero y ``MenuItem`` despues.
  Mitigacion: UC_ADM_04 (``manage_menu_catalog``) documenta el
  flujo end-to-end en una transaccion.

- **No autoarchive transitivo** — borrar el MenuItem no borra
  la Function. Esto es deseado (la capability sobrevive).

----

5. Alternativas Consideradas
============================

5.1 Alternativa A — MenuItem standalone (sin FK a Function)
------------------------------------------------------------

``MenuItem`` con sus propios ``label``, ``route_path``,
``status``, sin relacion obligatoria a ``Function``.

- **Pros:** modelo mas simple. Permite items "informativos" sin
  capability subyacente.
- **Contras (criticos):** reproduce 1:1 el anti-patron legacy
  ``C_MENU2``. El menu seria fuente de capability si el frontend
  decide pintarlo. Defense-in-depth roto.
- **Veredicto:** rechazada explicitamente. CNST-032 v2.0.0
  prohibe este diseno.

5.2 Alternativa C — MenuItem como JSON en Function
--------------------------------------------------

``Function`` con campo ``ui_metadata: JSONField`` que contiene
``{label, icon, order, route_path, status}``.

- **Pros:** una sola tabla. Sin doble paso de creacion.
- **Contras:** sin tipos explicitos a nivel DB; queries por
  ``status="ACTIVE"`` ineficientes (sin indice); validacion de
  esquema queda en aplicacion; lifecycle independiente del
  catalogo RBAC se pierde.
- **Veredicto:** rechazada. La capa UX merece su propio modelo.

----

6. Implementacion
=================

6.1 Migration canonica
----------------------

Bootstrap del modelo via Django ``RunPython`` data migration
(coherente con ADR-BACK-007 §3.2):

.. code-block:: python

   # migrations/00XX_create_menuitem.py
   from django.db import migrations, models


   def create_menu_items(apps, schema_editor):
       Function = apps.get_model("access", "Function")
       MenuItem = apps.get_model("access", "MenuItem")
       User = apps.get_model("users", "User")
       system_user = User.objects.get(username="system")

       seed = [
           ("view_reports", "Mis Reportes", "BarChartIcon", "/reports", 10),
           # ...
       ]
       for codename, label, icon, route, order in seed:
           function = Function.objects.get(codename=codename)
           MenuItem.objects.create(
               function=function,
               display_label=label,
               icon=icon,
               route_path=route,
               display_order=order,
               status="ACTIVE",
               created_by=system_user,
           )


   class Migration(migrations.Migration):
       dependencies = [
           ("access", "0XXX_previous"),
       ]
       operations = [
           migrations.CreateModel(
               name="MenuItem",
               fields=[...],
           ),
           migrations.RunPython(
               create_menu_items, reverse_code=migrations.RunPython.noop,
           ),
       ]

6.2 Test guardrails I-1..I-4
----------------------------

.. code-block:: python

   @pytest.mark.django_db
   def test_cannot_create_menu_item_without_function():
       """I-1: Function requerida."""
       with pytest.raises(IntegrityError):
           MenuItem.objects.create(
               display_label="Test", route_path="/test",
               status="ACTIVE",
           )


   @pytest.mark.django_db
   def test_deleting_function_with_menu_item_protected():
       """I-2: PROTECT sobre delete."""
       fn = Function.objects.create(codename="test_fn", module="TST")
       MenuItem.objects.create(function=fn, display_label="X",
                                route_path="/x")
       with pytest.raises(ProtectedError):
           fn.delete()


   @pytest.mark.django_db
   def test_function_can_exist_without_menu_item():
       """I-3: capability sin item visual."""
       fn = Function.objects.create(codename="manage_own_state",
                                      module="OPR")
       assert not hasattr(fn, "menu_item") or fn.menu_item is None


   @pytest.mark.django_db
   def test_inactive_function_hides_menu_item():
       """I-4: visibility cascade via queryset."""
       fn = Function.objects.create(codename="x", module="TST",
                                      is_active=True)
       MenuItem.objects.create(function=fn, display_label="X",
                                route_path="/x", status="ACTIVE")
       assert MenuItem.objects.visible().filter(function=fn).exists()

       fn.is_active = False
       fn.save()
       assert not MenuItem.objects.visible().filter(function=fn).exists()

----

7. Trazabilidad
===============

- Decision documentada por primera vez:
  ``2026-05-06-21-42-06-menu-rbac-user-scope-docs/strategy/menu-rbac-user-scope-solution-strategy.md``
  §3 P1.
- Anti-patron evitado:
  ``2026-05-06-21-42-06-menu-rbac-user-scope-docs/discover/cmenu2-legacy-archeology.md``.
- Constraints satisfechas: CNST-029 (modelo plano), CNST-032
  v2.0.0 (a producir en L2 — prohibe Diseno A).
- ADR siguientes: ADR-BACK-009 (cache), ADR-BACK-010 (governance
  ``is_critical``).
