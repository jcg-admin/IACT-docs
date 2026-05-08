.. meta::
 :artefacto: CLEAN_CODE_NAMING_PRINCIPLES_FRONTEND
 :tipo: Norma de Proyecto (Naming Frontend)
 :dominio: normativa
 :subdominio: estandares
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Critico

.. _clean-code-naming-principles-frontend:

============================================================
CLEAN_CODE_NAMING_PRINCIPLES — Frontend (Norma del Proyecto)
============================================================

.. note::

 Documento autoritativo de naming para identificadores
 frontend de IACT-ui. Complementa
 :doc:`clean-code-naming-principles` para componentes,
 hooks, props, rutas y stores. Los principios fundamentales
 (§1) son los mismos; este documento detalla aplicaciones
 especificas al stack frontend.

 La version markdown standalone en el repositorio raiz
 (``CLEAN_CODE_NAMING_PRINCIPLES_FRONTEND.md``) y este
 artefacto RST son **equivalentes en contenido**.

.. contents:: Contenido
 :depth: 2

----

1. Principios fundamentales (compartidos)
==========================================

Los principios §1.1 a §1.6 del documento general aplican
identicos:

- §1.1 El nombre describe el rol en el dominio.
- §1.2 Sufijos GoF como default prohibido.
- §1.3 Naming de tests (data: ``*TestData``, NO
  ``*Factory``).
- §1.4 Distincion produccion vs tests.
- §1.5 Identificadores en ingles.
- §1.6 Nombres canonicos prefijados sobre genericos.

Aplicacion frontend de §1.1: el nombre de un componente
debe permanecer valido si se migra de React a Vue o
viceversa. No debe contener marcas del framework.

Ver :doc:`clean-code-naming-principles` para definicion
completa.

----

2. Sufijos prohibidos por categoria (frontend)
================================================

2.1 Sufijos de framework
-------------------------

.. list-table::
 :widths: 35 25 40
 :header-rows: 1

 * - Sufijo
   - Origen
   - Reemplazo de dominio
 * - ``Component`` (sufijo redundante)
   - React class components legacy
   - omitir — el contexto ya lo indica
 * - ``HOC`` (Higher-Order Component)
   - React patron
   - omitir o nombrar el rol
 * - ``Container`` (Redux container)
   - Redux
   - omitir o ``Page`` / ``View`` semantico
 * - ``Provider`` (React Context Provider)
   - React Context
   - omitir o ``Context``
 * - ``Reducer``
   - Redux
   - aceptable solo si el archivo es reducer puro
 * - ``Action`` (suffix en action creators legacy)
   - Redux
   - usar verbo descriptivo

2.2 Sufijos GoF en frontend
----------------------------

Misma tabla que :doc:`clean-code-naming-principles` §2.2
(``Factory``, ``Builder``, ``Manager``, ``Helper``,
``Util``). Frontend tiende a abusar de ``Helper``/``Util``
— evitar siempre.

2.3 Componentes — verbos vs nombres
------------------------------------

.. list-table::
 :widths: 25 35 40
 :header-rows: 1

 * - Tipo
   - Patron
   - Ejemplo
 * - Pagina (route handler)
   - sustantivo + opcional ``Page``
   - ``UserProfile``, ``ReportsListPage``
 * - Componente de presentacion
   - sustantivo concreto
   - ``MenuItem``, ``AlertBanner``,
     ``ColumnPicker``
 * - Componente de logica
   - rol descriptivo
   - ``AuthGate``, ``RouteGuard``,
     ``FeatureFlag``
 * - Hook
   - ``use<Concepto>``
   - ``useUserSession``, ``useFeatureFlag``
 * - Store/slice
   - sustantivo + ``Store`` o ``Slice``
   - ``userSessionStore``, ``alertSlice``
 * - Selector
   - ``select<Concepto>``
   - ``selectActiveAlerts``,
     ``selectUserProfile``
 * - Action creator
   - verbo + ``<Concepto>``
   - ``loginUser``, ``acknowledgeAlert``

----

3. Convenciones especificas por capa
======================================

3.1 Componentes React/Vue
--------------------------

::

   ✓ MenuItem.tsx           ← sustantivo del dominio
   ✓ AlertBanner.tsx
   ✓ ColumnPicker.tsx
   ✓ UserProfilePage.tsx    ← Page sufijo solo en routes

   ✗ MenuItemComponent.tsx  ← sufijo redundante
   ✗ MenuItemHOC.tsx        ← marca framework
   ✗ MenuItemContainer.tsx  ← Redux marca; usar UserProfilePage
   ✗ MenuItemHelper.tsx     ← genericism

3.2 Hooks
----------

::

   ✓ useUserSession         ← convencion React `use*`
   ✓ useFeatureFlag
   ✓ useDebouncedSearch

   ✗ getUserSession         ← no es funcion regular
   ✗ userSessionHook        ← redundante

Hooks personalizados que envuelven otros hooks deben ser
explicitos sobre el rol:

::

   ✓ useFunctionGuard(fn: string)   ← AuthZ check
   ✓ useTransitionAwareNav()

3.3 State management (Redux/Pinia/Zustand)
-------------------------------------------

::

   ✓ userSessionStore
   ✓ alertSlice
   ✓ reportFiltersAtom (Jotai)

   Selectors: selectActiveUserSession, selectUnreadAlertCount
   Actions:   loginUser, acknowledgeAlert, dismissBanner

3.4 Rutas
----------

Rutas siguen :doc:`std-013-rest-api-conventions`
(kebab-case URLs, recursos no acciones):

::

   ✓ /access/separation-rules
   ✓ /reports/saved-views
   ✓ /audit/exports

   ✗ /access/separationRules
   ✗ /access/validate-pii

Componentes asociados a rutas usan PascalCase:

::

   /access/separation-rules → SeparationRulesPage
   /reports/saved-views     → SavedViewsPage

3.5 Props y eventos
--------------------

::

   ✓ onUserBlock(userId: string)        ← evento sin "Handler"
   ✓ onSubmit
   ✓ isLoading, isDisabled               ← booleans con `is*`
   ✓ canEdit, canDelete                  ← capability con `can*`
   ✓ hasUnreadAlerts                     ← presencia con `has*`

   ✗ onUserBlockHandler                  ← redundante
   ✗ loading                             ← ambiguo

3.6 Tipos y interfaces (TypeScript)
------------------------------------

::

   ✓ User                  ← entidad de dominio
   ✓ UserProfile           ← view-model
   ✓ LoginRequest          ← contrato de request
   ✓ LoginResponse         ← contrato de response
   ✓ UserState (enum)      ← estados de dominio

   ✗ IUser                 ← prefijo `I` (Hungarian) prohibido
   ✗ TUser                 ← prefijo `T` prohibido
   ✗ UserType              ← redundante con TS

----

4. Tests frontend
==================

4.1 Datos de prueba
--------------------

::

   tests/
     __mocks__/
       user-session.mock.ts
     test-data/
       user.test-data.ts
       alert.test-data.ts

NO usar ``userFactory.ts`` ni ``userBuilder.ts``.

4.2 Mocks
----------

::

   ✓ MockUserSession
   ✓ StubAuthProvider
   ✓ FakeAlertStream

   ✗ UserSessionMockFactory   ← Factory prohibido en tests

----

5. Naming de archivos frontend
================================

.. list-table::
 :widths: 25 35 40
 :header-rows: 1

 * - Tipo
   - Patron
   - Ejemplo
 * - Componente
   - ``PascalCase.tsx``
   - ``UserProfile.tsx``, ``MenuItem.tsx``
 * - Hook
   - ``kebab-case.ts`` o ``use-X.ts``
   - ``use-user-session.ts``
 * - Store/slice
   - ``kebab-case.ts``
   - ``user-session.slice.ts``
 * - Test
   - ``<file>.test.tsx``
   - ``UserProfile.test.tsx``
 * - Storybook
   - ``<file>.stories.tsx``
   - ``MenuItem.stories.tsx``
 * - Type definitions
   - ``<concepto>.types.ts``
   - ``user.types.ts``
 * - Test data
   - ``<concepto>.test-data.ts``
   - ``user.test-data.ts``

----

6. Anti-patterns frecuentes en frontend
==========================================

6.1 Componente "God" con sufijo Manager o Container
-----------------------------------------------------

::

   ✗ UserDataManager
   ✗ AlertContainerWrapper

Razon: contienen demasiada logica + presentacion. Dividir
en hook + componente puro:

::

   ✓ useUserData (hook)
   ✓ UserProfileView (componente puro)

6.2 Helper modules sin rol
---------------------------

::

   ✗ src/utils/helpers.ts
   ✗ src/lib/utils.ts
   ✗ src/common/index.ts (con 30 funciones sin relacion)

Razon: violan §1.2 (genericism). Reemplazar con modulos
con rol especifico:

::

   ✓ src/format/date-formatter.ts
   ✓ src/validation/email-validator.ts
   ✓ src/transform/menu-tree-builder.ts (con fluent real)
   ✓ src/transform/menu-tree-assembler.ts (sin fluent)

6.3 Props con nombres genericos
--------------------------------

::

   ✗ <UserCard data={...} />
   ✗ <MenuItem item={...} options={...} />

   ✓ <UserCard user={...} />
   ✓ <MenuItem menuItem={...} actionConfig={...} />

6.4 Prefijos Hungarian
-----------------------

::

   ✗ const sUserName = 'jdoe'    ← Hungarian (string)
   ✗ const bIsActive = true       ← Hungarian (bool)

   ✓ const username = 'jdoe'
   ✓ const isActive = true

----

7. Cross-references al corpus
==============================

- :doc:`clean-code-naming-principles` — principios
  fundamentales y aplicacion backend.
- :doc:`std-007-convencion-naming` — naming general
  (kebab-case en filenames).
- :doc:`std-008-naming-identificadores` — naming de
  identificadores; ingles tecnico.
- :doc:`std-013-rest-api-conventions` — REST API
  conventions (URLs frontend consumen).
- :doc:`std-010-vocabulario-abstracto` — vocabulario
  abstracto en narrativa (componentes UI heredan
  terminos).

----

8. Aplicacion del criterio en revisiones (frontend)
======================================================

#. ¿El componente nombra el rol del dominio o el patron
   de framework? Solo el rol.
#. ¿El sufijo es noun del dominio (``MenuItem``,
   ``AlertBanner``) o de framework (``Component``,
   ``Container``)? Si framework, omitir.
#. ¿Hay marca explicita de libreria
   (``HOC``, ``Provider``, ``Reducer``)? Justificar o
   omitir.
#. ¿El hook usa ``use*``? Si es hook real, si.
#. ¿Los tests usan ``*TestData``, ``Mock*``, ``Stub*``?
   No ``Factory``.
#. ¿Las props tienen ``is*``/``can*``/``has*`` para
   booleans? Si.

----

9. Historial
=============

.. list-table::
 :widths: 15 15 70
 :header-rows: 1

 * - Version
   - Fecha
   - Cambios
 * - 1.0.0
   - 2026-05-08
   - Documento canonico standalone para frontend —
     consolida la aplicacion del principio CLEAN_CODE al
     stack frontend (React/Vue/TS) en complemento a
     :doc:`clean-code-naming-principles`.
