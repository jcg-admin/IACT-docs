.. meta::
   :artefacto: ARCHITECTURE-FRONTEND
   :tipo: Documentacion arquitectura
   :dominio: arquitectura_tecnica
   :subdominio: frontend
   :repo_origen: IACT-ui
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2026-05-19
   :ultimo_cambio: 2026-05-19
   :autor: NestorMonroy
   :clasificacion: Interno

.. admonition:: Documento portado desde repo IACT-ui
   :class: note

   Origen: ``/home/user/IACT-ui/docs/ARCHITECTURE.md``. Portado a IACT-docs en
   iniciativa ``integrar-docs-internos-multi-repo`` (2026-05-19).
   La fuente original permanece en el repo como historico.



Architecture Overview
=====================

Complete system architecture and design patterns.

Application Structure
---------------------

.. code-block:: text

   App (Entry Point)
   ├── Redux Provider (State Management)
   │   ├── UI Slice
   │   │   ├── isSidebarOpen
   │   │   ├── isDarkMode
   │   │   └── notifications
   │   └── User Slice
   │       ├── isAuthenticated
   │       ├── user
   │       ├── loading
   │       └── error
   └── React Router (Navigation)
       ├── DashboardLayout (Main Layout)
       │   ├── Header Component
       │   │   ├── LogoBrand
       │   │   ├── MenuButton
       │   │   ├── BreadcrumbNav
       │   │   ├── NotificationBell
       │   │   └── UserMenu
       │   ├── Sidebar Component
       │   │   ├── SidebarNav
       │   │   └── NavLink (Multiple)
       │   └── Main Content (Outlet)
       │       ├── Dashboard Page
       │       ├── Profile Page
       │       ├── Settings Page
       │       └── NotFound Page (404)

Feature Folders
---------------

Each feature is a self-contained folder with:
- Component(s) (.jsx files)
- Styles (.scss files)
- Tests (.test.js files)
- Barrel export (index.jsx or index.js)

.. code-block:: text

   Header/
   ├── index.jsx              ← Barrel export
   ├── Header.jsx             ← Main component
   ├── Header.scss            ← Component styles
   ├── Header.test.js         ← Tests
   ├── LogoBrand.jsx
   ├── LogoBrand.scss
   ├── LogoBrand.test.js
   └── ... (more sub-components)

State Management
----------------

Redux Store
~~~~~~~~~~~

.. code-block:: javascript

   store.js
   ├── Reducers (slices)
   │   ├── uiSlice (UI state)
   │   │   ├── isSidebarOpen
   │   │   ├── isDarkMode
   │   │   └── notifications
   │   └── userSlice (User state)
   │       ├── isAuthenticated
   │       ├── user
   │       ├── loading
   │       └── error
   └── Middleware (Redux Thunk for async)

Using Redux
~~~~~~~~~~~

.. code-block:: javascript

   // Components subscribe to state
   const sidebar = useSelector(state => state.ui.isSidebarOpen)

   // Components dispatch actions
   const dispatch = useDispatch()
   dispatch(toggleSidebar())

Routing
-------

Routes
~~~~~~

- ``/`` → Redirects to ``/dashboard``
- ``/dashboard`` → Dashboard page
- ``/profile`` → Profile page
- ``/settings`` → Settings page
- ``*`` → 404 Not Found

Nested Routes
~~~~~~~~~~~~~

All routes render inside DashboardLayout, so Header and Sidebar are always visible.

Component Patterns
------------------

Feature Component
~~~~~~~~~~~~~~~~~

.. code-block:: javascript

   // Feature/Feature.jsx
   import './Feature.scss'

   export default function Feature({ prop1, prop2 }) {
     return (
       <div className="container">
         <h2 className="title">Feature</h2>
       </div>
     )
   }

   // Feature/Feature.scss
   .container {
     padding: $spacing-md;
   }

   .title {
     color: $secondary-color;
   }

   // Feature/Feature.test.js
   describe('Feature Component', () => {
     it('should render', () => {
       // Test
     })
   })

   // Feature/index.jsx (Barrel Export)
   export { default as Feature } from './Feature'

Styling System
--------------

SCSS global
~~~~~~~~~~~

Each component has its own ``.scss`` file. Classes are global strings —
no CSS Modules scoping. The project uses plain SCSS following the
standard React + Sass pattern (``import './Component.scss'``).

Global Styles
~~~~~~~~~~~~~

Located in ``src/styles/abstracts/``:
- ``_variables.scss`` - Design tokens (colors, spacing, gray scale)
- ``_layout.scss`` - Layout variables
- ``_animations.scss`` - Animation keyframes

Variables — always available, no import needed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``webpack.config.js`` injects ``_variables.scss`` into every SCSS file
via ``sass-loader.additionalData`` using ``@use ... as *``. No manual
``@import`` or ``@use`` needed in component SCSS files.

.. code-block:: scss

   // Feature.scss — variables available without any import
   .container {
     background-color: white;
     padding: $spacing-md;
     border: 1px solid $border-color;
     color: $secondary-color;
   }

Testing Strategy
----------------

Test Types
~~~~~~~~~~

1. **Unit Tests** - Test components in isolation
2. **Integration Tests** - Test components working together
3. **Redux Tests** - Test reducers and actions

Test Structure
~~~~~~~~~~~~~~

.. code-block:: javascript

   describe('Component Name', () => {
     describe('Feature 1', () => {
       it('should do something', () => {
         // Test
       })
     })
   })

Performance Optimization
------------------------

Code Splitting
~~~~~~~~~~~~~~

Pages are lazy-loaded to reduce initial bundle:

.. code-block:: javascript

   const DashboardPage = React.lazy(() => import('@pages/Dashboard'))

Memoization
~~~~~~~~~~~

Expensive components are memoized:

.. code-block:: javascript

   export default React.memo(Component)

Accessibility
-------------

WCAG AAA Compliance
~~~~~~~~~~~~~~~~~~~

- Semantic HTML (header, nav, main)
- ARIA labels and roles
- Keyboard navigation (Tab, Enter, Escape)
- Focus management
- Color contrast

Memory Management
-----------------

Event Cleanup
~~~~~~~~~~~~~

All event listeners are cleaned up to prevent memory leaks:

.. code-block:: javascript

   useEffect(() => {
     window.addEventListener('keydown', handler)
     return () => window.removeEventListener('keydown', handler)
   }, [])

Design Tokens
-------------

Colors
~~~~~~

- ``$primary-color``: #3b82f6 (Blue)
- ``$secondary-color``: #1f2937 (Gray-800)
- ``$error-color``: #ef4444 (Red)
- ``$success-color``: #10b981 (Green)
- ``$warning-color``: #f59e0b (Amber)
- ``$info-color``: #0ea5e9 (Sky)
- ``$text-muted``: #94a3b8
- ``$border-color``: #374151
- ``$gray-50`` … ``$gray-900``: Tailwind gray scale

Spacing
~~~~~~~

- xs: 4px
- sm: 8px
- md: 16px
- lg: 24px
- xl: 32px

Breakpoints
~~~~~~~~~~~

- Mobile: 375px
- Tablet: 768px
- Desktop: 1024px
- Wide: 1440px

----

Next: `Component Development Guide <./guides/COMPONENT_GUIDE.md>`_

