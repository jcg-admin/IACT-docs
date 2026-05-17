.. meta::
 :artefacto: ADR-BACK-010
 :tipo: ADR
 :dominio: backend
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-07
 :ultimo_cambio: 2026-05-07
 :autor: NestorMonroy
 :clasificacion: Interno

.. _adr-back-010:

============================================================================
ADR-BACK-010: Function.is_critical y governance del flag
============================================================================

Estado y metadata
=================

- **Estado:** Aprobada.
- **Fecha:** 2026-05-07.
- **Decisores:** NestorMonroy (ejecutor) + analisis documentado en WP
  ``2026-05-06-21-42-06-menu-rbac-user-scope-docs``.
- **Contexto tecnico:** Backend — flag de capability critica que
  bypassa el cache y mecanismo de governance del flag mismo.
- **Relacionados:**

  - :doc:`/backend/adr-back-007-rbac-custom-vs-auth-group`
    (modelo RBAC custom).
  - :doc:`/backend/adr-back-008-menuitem-wrapper-ux-sobre-function`
    (consumidor del bypass).
  - :doc:`/backend/adr-back-009-cache-capabilities-degraded-mode`
    (cache que se bypassa).

- **Refs WP discover:**

  - ``strategy/strategy-addendum-gaps-and-module.md`` §5
    (gap #4 resuelto).
  - ``strategy/gap-3-4-decision-rationale.md`` §3 (razonamiento).

----

1. Contexto y Problema
======================

ADR-BACK-009 documenta cache de capabilities con TTL 300s y
degraded mode ante falla. Esa politica es aceptable para la
mayoria de capabilities, pero **falla** ante un escenario:

  *"Un actor con capability sensible es comprometido o
  detectado. El admin revoca su acceso. Durante hasta 300s,
  el cache permite usar la capability revocada para causar
  dano."*

Capabilities con riesgo real bajo este escenario en el catalogo
v5.6.0:

- ``assign_functions``, ``revoke_function_group`` (modificar
  permisos de otros).
- ``manage_menu_catalog``, ``manage_menu_lifecycle`` (modificar
  catalogo UX que afecta a todos).
- ``manage_function_catalog`` (modificar el catalogo RBAC mismo).
- ``manage_access_groups`` (modificar composicion AGR).
- Cualquier ``delete_*`` sobre entidades RBAC.

**Pregunta arquitectonica:**

¿Como diferenciar capabilities donde 300s de stale es
inaceptable, sin degradar latencia de las demas, y como evitar
que un atacante con acceso al catalogo de Functions desactive
esta proteccion?

----

2. Factores de Decision
=======================

- **Risk by capability, not by HTTP verb** — no todas las writes
  son iguales; modelar el riesgo en el catalogo.
- **Data-driven security** — la decision de seguridad debe ser
  versionable, auditable, migrable.
- **Default cache, explicit bypass** — el comportamiento
  eficiente es default; el bypass requiere accion explicita.
- **Defense-in-depth aplicada al mecanismo de seguridad mismo** —
  el flag que protege debe ser inmutable desde la superficie que
  protege.

----

3. Decision
===========

3.1 El flag ``Function.is_critical``
------------------------------------

Se agrega al modelo ``Function``:

.. code-block:: python

   class Function(models.Model):
       codename = models.CharField(max_length=100, unique=True)
       module = models.CharField(max_length=20)
       name = models.CharField(max_length=200)
       is_active = models.BooleanField(default=True)
       is_critical = models.BooleanField(
           default=False,
           help_text=(
               "Si True, la verificacion de capability bypassa el "
               "servicio de cache y consulta DB en cada request. "
               "Reservado para capabilities de modificacion de "
               "permisos o cambios estructurales irreversibles."
           ),
       )
       # ... otros campos ...

       class Meta:
           db_table = "functions"
           indexes = [
               models.Index(fields=("codename",)),
               models.Index(fields=("is_active",)),
               models.Index(fields=("module",)),
               models.Index(fields=("codename", "is_active")),
           ]

3.2 AP-2b: bypass de cache para is_critical
-------------------------------------------

El ``UserCapabilityResolver`` decide cache vs DB segun el flag:

.. code-block:: python

   class UserCapabilityResolver:
       @staticmethod
       def has_capability(user, codename: str) -> bool:
           """Decide cache vs DB segun is_critical del catalogo."""
           is_critical = Function.objects.filter(
               codename=codename, is_critical=True,
           ).exists()
           if is_critical:
               return codename in UserCapabilityResolver.resolve_uncached(user)
           return codename in UserCapabilityResolver.resolve(user)

       @staticmethod
       def resolve_uncached(user) -> set[str]:
           """DB-first. Bypass de cache para capabilities criticas."""
           return UserCapabilityResolver._query_db(user)

3.3 Catalogo inicial de is_critical=True
----------------------------------------

Capabilities marcadas como criticas desde el dia 1, alineadas
al catalogo canonico
:doc:`/requisitos/reglas-negocio/rbac/catalogo-funciones`:

.. list-table::
 :widths: 30 12 22 36
 :header-rows: 1

 * - Codename
   - Modulo
   - UC titular
   - Razon
 * - ``assign_functions``
   - ACC
   - UC-010, UC-042
   - Asigna Function a usuarios — modifica permisos de otros
 * - ``revoke_functions``
   - ACC
   - UC-010
   - Revoca Function de usuarios (simetria con asignar)
 * - ``assign_function_groups``
   - ACC
   - UC-010
   - Asigna grupos de funciones — modifica permisos
 * - ``revoke_function_group``
   - PERM
   - UC_PERM_02
   - Revoca grupo asignado a usuario
 * - ``assign_functions_to_group``
   - PERM/ADM
   - UC_PERM_06, UC_ADM_03
   - Modifica composicion de AGRs (catalogo de los 12 grupos
     predefinidos del sistema y AGRs custom)
 * - ``manage_function_catalog``
   - ADM
   - UC_ADM_02
   - CRUD del catalogo RBAC mismo (Function entries)
 * - ``manage_menu_catalog``
   - ADM (v5.6.x)
   - UC_ADM_04
   - CRUD del catalogo UX persistido (MenuItem)
 * - ``manage_menu_lifecycle``
   - ADM (v5.6.x)
   - UC_ADM_05
   - Transiciones de estado afectan render para todos
 * - ``deactivate_users``
   - USR
   - UC_USR_xx
   - Soft delete de usuarios (semantica BR-009 — no
     eliminacion fisica)

**Total inicial: 9 capabilities.**

**Nota sobre semantica de borrado en IACT:**

El catalogo IACT NO incluye capabilities de tipo
``delete_*`` con borrado fisico — el proyecto aplica
**BR-009 baja logica** documentada en catalogo §3.x:
``deactivate_users`` (RENAME v5.4.0 desde
``delete_users``), ``disable_alerts`` (RENAME v5.4.0
desde ``delete_alerts``), etc. La proteccion
``is_critical=True`` cubre las capabilities de
desactivacion donde aplica el riesgo de revocacion
diferida.

**Capabilities consideradas y NO incluidas:**

- ``manage_access_groups``, ``delete_function``,
  ``delete_access_group`` — no existen en el catalogo
  IACT. La gestion de AGRs y Function se realiza via
  ``assign_functions_to_group`` (composicion) y
  ``manage_function_catalog`` (catalogo Function);
  ambas ya en la lista. La desactivacion sigue el
  patron ``is_active=False`` (soft) cubierto por
  ``manage_function_catalog``.

3.4 Governance del flag — separacion de capabilities
----------------------------------------------------

**Problema mitigado:** un atacante con ``manage_function_catalog``
comprometido podria marcar su propia capability como
``is_critical=False`` antes de ser revocado, anulando la
proteccion.

**Decision crítica:** ``manage_critical_function_flag`` es una
capability **separada** de ``manage_function_catalog``, con
governance estricta y sin auto-asignacion.

.. list-table::
 :widths: 35 32 33
 :header-rows: 1

 * - Capability
   - ``manage_function_catalog``
   - ``manage_critical_function_flag``
 * - Que permite
   - CRUD del catalogo de Function: crear, renombrar, activar,
     desactivar, asignar modulo
   - **Solo** modificar el campo ``is_critical`` de Function
 * - Quien la tiene en v5.6.0
   - ``system_admin`` (AGR-010)
   - **Ningun rol del catalogo v5.6.0** — sin titular
 * - Como se modifica el campo ``is_critical``
   - **No** puede via esta capability
   - Solo via Django RunPython data migration
 * - Auto-asignacion permitida
   - N/A (capability comun de admin)
   - **Prohibida explicitamente**: la migration RBAC no puede
     asignar esta capability a ningun AGR existente sin un
     ADR explicito que lo autorice
 * - Visibilidad en UI admin
   - Editable
   - Read-only en admin Django; UI no expone acciones de
     escritura sobre ``is_critical``

**Por que separadas y no la misma capability:**

(a) **Principio de minimo privilegio:** un admin que gestiona
    el catalogo (renombra Functions, las activa/desactiva) no
    necesita autoridad sobre la politica de seguridad
    (``is_critical``). Mezclar las dos rompe least privilege.

(b) **Vector de ataque eliminado:** si fueran la misma
    capability, comprometer ``manage_function_catalog`` daria
    al atacante poder de auto-desproteger sus propias
    capabilities. Separadas, el atacante necesita comprometer
    *dos* capabilities ortogonales.

(c) **Auditabilidad:** los cambios al catalogo (alta de
    Functions) son frecuentes y rutinarios; los cambios al flag
    ``is_critical`` son raros y deben requerir review fuera de
    banda. Capabilities separadas permiten audit logs separados
    con politicas distintas.

3.5 Mecanismo operacional para cambiar is_critical
--------------------------------------------------

Un cambio a ``Function.is_critical`` requiere:

1. **Pull request** al repositorio de migrations RBAC con el
   cambio del campo.
2. **Review obligatoria ≥ 2 aprobaciones** de
   maintainers RBAC declarados (CODEOWNERS sobre la carpeta
   de migrations).
3. **Aplicacion via Django RunPython data migration** — nunca
   via endpoint admin, nunca via shell de produccion sin
   migration.
4. **Audit log de la migration** — el commit del PR queda como
   evidencia trazable; la migration en produccion deja registro
   en ``django_migrations``.

UI de Django admin:

.. code-block:: python

   class FunctionAdmin(admin.ModelAdmin):
       list_display = ("codename", "module", "is_active",
                       "is_critical")
       readonly_fields = ("is_critical",)  # NO editable en admin
       # ... resto ...

3.6 Capability futura ``manage_critical_function_flag``
-------------------------------------------------------

La capability ``manage_critical_function_flag`` se declara en
el catalogo v5.6.x **sin titular** desde el dia 1. Si en el
futuro se requiere una via runtime para modificar el flag, la
asignacion a un AGR (o creacion de un AGR-013 dedicado)
requeriria un ADR explicito.

Documentado como **TD-RBAC-03** en deuda tecnica:
*"manage_critical_function_flag sin titular — disponibilidad
runtime de cambios al flag is_critical pendiente de decidir."*

----

4. Consecuencias
================

4.1 Positivas
-------------

- **Strong consistency** para capabilities sensibles.
- **Sin window de stale** tras revocacion en capabilities
  criticas.
- **Catalogo versionable** — el flag vive en data migrations,
  trazable en git.
- **Defense-in-depth aplicada al mecanismo:** el flag que
  protege es inmutable desde la superficie protegida.
- **Separacion de capabilities** elimina el vector de
  auto-desproteccion.

4.2 Negativas (aceptadas)
-------------------------

- **Latencia mayor** en endpoints con capability critica —
  cache MISS forzado en cada request. Mitigado: capabilities
  criticas son administrativas, baja frecuencia.

- **Cambios al flag requieren deploy** — no hay UI admin para
  toggle en runtime. Mitigado: cambios al flag son raros por
  diseno; si se vuelven frecuentes, replantear con ADR.

- **TD-RBAC-03 abierto** — ``manage_critical_function_flag``
  sin titular. Mitigado: explicito en deuda tecnica con trigger
  de revision.

----

5. Alternativas Consideradas
============================

5.1 Alternativa A — Misma capability ``manage_function_catalog``
----------------------------------------------------------------

Permitir que el rol que gestiona el catalogo tambien edite
``is_critical``.

- **Pros:** menos capabilities en el catalogo.
- **Contras:** rompe least privilege; introduce vector de
  auto-desproteccion descrito en §3.4.
- **Veredicto:** rechazada explicitamente. La separacion es la
  decision crítica de este ADR.

5.2 Alternativa B — Hardcoded list en codigo
--------------------------------------------

Lista hardcoded en el modulo de auth:
``CRITICAL_CAPABILITIES = {"assign_functions", ...}``.

- **Pros:** sin field en DB; sin migrations.
- **Contras:** cambios requieren modificar codigo y desplegar;
  no auditable como cambio de catalogo; no migrable entre
  entornos como dato.
- **Veredicto:** rechazada. ``is_critical`` debe ser**dato del
  catalogo**, no codigo.

5.3 Alternativa C — TTL distinto por capability
-----------------------------------------------

``Function.cache_ttl_seconds`` con default 300 y override a 0
para criticas.

- **Pros:** unifica la politica.
- **Contras:** complejidad innecesaria — boolean es suficiente.
  TTL=0 efectivamente equivale a bypass.
- **Veredicto:** rechazada. Boolean es mas simple y expresivo.

----

6. Implementacion
=================

6.1 Migration de Function.is_critical
-------------------------------------

.. code-block:: python

   # migrations/00XX_function_is_critical.py
   from django.db import migrations, models


   # Alineado al catalogo canonico v5.6.x (catalogo-funciones.rst).
   # 9 capabilities marcadas is_critical=True (D-DR-001).
   CRITICAL_INITIAL = {
       # ACC — modifican permisos de usuarios
       "assign_functions",
       "revoke_functions",
       "assign_function_groups",
       # PERM — modifican grupos / asignaciones
       "revoke_function_group",
       "assign_functions_to_group",
       # ADM — catalogos y lifecycle
       "manage_function_catalog",
       "manage_menu_catalog",          # v5.6.x extension
       "manage_menu_lifecycle",        # v5.6.x extension
       # USR — soft delete (BR-009)
       "deactivate_users",
   }


   def mark_critical_functions(apps, schema_editor):
       Function = apps.get_model("access", "Function")
       missing = set(CRITICAL_INITIAL) - set(
           Function.objects.filter(codename__in=CRITICAL_INITIAL)
                           .values_list("codename", flat=True)
       )
       assert not missing, (
           f"CRITICAL_INITIAL contains codenames not in catalog: {missing}. "
           f"Update catalogo-funciones.rst or remove from CRITICAL_INITIAL."
       )
       Function.objects.filter(codename__in=CRITICAL_INITIAL).update(
           is_critical=True,
       )


   class Migration(migrations.Migration):
       dependencies = [
           ("access", "0XXX_previous"),
       ]
       operations = [
           migrations.AddField(
               model_name="Function",
               name="is_critical",
               field=models.BooleanField(default=False),
           ),
           migrations.RunPython(
               mark_critical_functions,
               reverse_code=migrations.RunPython.noop,
           ),
       ]

6.2 Migration de la capability separada
---------------------------------------

.. code-block:: python

   # migrations/00YY_critical_function_flag_capability.py
   from django.db import migrations


   def create_capability_without_titular(apps, schema_editor):
       Function = apps.get_model("access", "Function")
       Function.objects.create(
           codename="manage_critical_function_flag",
           module="ADM",
           name="Modificar flag is_critical de Function",
           is_active=True,
           is_critical=True,  # ironicamente, ella misma es critica
       )
       # NO se asigna a ningun AGR — sin titular por diseno


   class Migration(migrations.Migration):
       dependencies = [
           ("access", "00XX_function_is_critical"),
       ]
       operations = [
           migrations.RunPython(
               create_capability_without_titular,
               reverse_code=migrations.RunPython.noop,
           ),
       ]

6.3 Tests guardrail
-------------------

.. code-block:: python

   @pytest.mark.django_db
   def test_critical_function_bypasses_cache():
       """is_critical=True dispara DB-direct en has_capability."""
       fn = Function.objects.create(
           codename="assign_functions", module="ADM",
           is_critical=True, is_active=True,
       )
       user = make_user_with_capability("assign_functions")
       cache.set(f"caps:user:{user.id}", set())  # cache vacio
       assert UserCapabilityResolver.has_capability(
           user, "assign_functions",
       ) is True
       # cache decia vacio, pero DB dijo True → bypass funciono


   @pytest.mark.django_db
   def test_non_critical_function_uses_cache():
       """is_critical=False usa cache."""
       fn = Function.objects.create(
           codename="view_reports", module="RPT",
           is_critical=False, is_active=True,
       )
       user = make_user_without_capability("view_reports")
       cache.set(f"caps:user:{user.id}", {"view_reports"})  # stale
       assert UserCapabilityResolver.has_capability(
           user, "view_reports",
       ) is True  # cache stale gana


   @pytest.mark.django_db
   def test_manage_critical_function_flag_has_no_titular():
       """La capability separada no tiene AGR titular en v5.6.0."""
       fn = Function.objects.get(
           codename="manage_critical_function_flag",
       )
       assert fn.is_critical is True
       agrs = AccessGroup.objects.filter(
           functiongroupmembership__function=fn,
       )
       assert not agrs.exists()


   @pytest.mark.django_db
   def test_is_critical_readonly_in_admin():
       """admin no permite editar is_critical via formulario."""
       admin_obj = FunctionAdmin(Function, admin.site)
       assert "is_critical" in admin_obj.readonly_fields

----

7. Trazabilidad
===============

- Decision en strategy:
  ``2026-05-06-21-42-06-menu-rbac-user-scope-docs/strategy/strategy-addendum-gaps-and-module.md``
  §5 (gap #4 resuelto).
- Razonamiento del ejecutor:
  ``2026-05-06-21-42-06-menu-rbac-user-scope-docs/strategy/gap-3-4-decision-rationale.md``
  §3.
- Gate review explicito:
  *"Al escribir ADR-BACK-010 confirma que incluye la separacion
  explicita entre manage_critical_function_flag y
  manage_function_catalog como capabilities distintas con
  governance diferenciada."* — implementado en §3.4.
- Constraints satisfechas: ADR-BACK-007 (custom RBAC sin
  ``auth.Permission``), CNST-029 (modelo plano).
- Deuda tecnica creada: TD-RBAC-03
  (``manage_critical_function_flag`` sin titular).
