.. meta::
   :artefacto: STATE-DESIGN-FRONTEND
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

   Origen: ``/home/user/IACT-ui/docs/STATE_DESIGN.md``. Portado a IACT-docs en
   iniciativa ``integrar-docs-internos-multi-repo`` (2026-05-19).
   La fuente original permanece en el repo como historico.



Redux State Design Guide - IACT Dashboard
=========================================

Overview
--------

Este documento describe cómo está estructurado el estado en IACT Dashboard
y las decisiones de diseño detrás de él.

Principios
----------

1. **Single Source of Truth**: Cada dato existe en un único lugar del Redux store
2. **Normalization**: Datos complejos se normalizan para evitar duplicación
3. **Immutability**: El estado nunca se modifica directamente (Redux Toolkit + Immer)
4. **Derived State**: Estados computados se derivan con selectores memoizados
5. **Async Pattern**: Estados de loading/error consistentes en todos los slices

State Shape
-----------

.. code-block:: javascript

   {
     auth: {
       isAuthenticated: boolean,
       user: User | null,
       token: string | null,
       loading: boolean,
       error: string | null,
     },
     dashboard: {
       metrics: Metric[],
       loading: boolean,
       error: string | null,
       filters: {
         startDate: Date,
         endDate: Date,
       },
       lastUpdate: string (ISO 8601),
     },
   }

Detalle por Slice
-----------------

1. Auth State
~~~~~~~~~~~~~

**Propósito**: Gestionar autenticación y datos del usuario

**Shape**:

.. code-block:: javascript

   {
     isAuthenticated: boolean,     // Usuario logueado?
     user: {                       // Datos del usuario
       id: number,
       email: string,
       name: string,
       role: 'admin' | 'user',
     } | null,
     token: string | null,         // JWT token
     loading: boolean,             // Fetch en progreso?
     error: string | null,         // Mensaje de error
   }

**Acciones**:
- ``loginUser`` (async thunk)
- ``logout`` (sincrónico)
- ``clearError`` (sincrónico)

**Selectores**:
- ``selectIsAuthenticated``: ¿Está el usuario logueado?
- ``selectUser``: Datos del usuario
- ``selectIsLoading``: ¿Se está haciendo login?
- ``selectError``: Mensaje de error actual

**Decisiones de Diseño**:

1. **Separar user de token**:
   - ``user``: Datos para mostrar en UI
   - ``token``: Solo para autenticación
   - Razón: Permite actualizar uno sin el otro

2. **Error no se limpia automáticamente**:
   - Permanece hasta ``clearError()`` o nuevo ``loginUser()``
   - Razón: UI puede mostrar mensaje más tiempo si lo necesita

3. **Loading global**:
   - Un solo ``loading`` para toda la auth
   - Razón: IACT es simple, un login a la vez

**Uso en Componentes**:

.. code-block:: javascript

   const { isAuthenticated, user, loading, error } = useAuth();

   // O con selectores:
   const isAuth = useSelector(selectIsAuthenticated);
   const user = useSelector(selectUser);

----

2. Dashboard State
~~~~~~~~~~~~~~~~~~

**Propósito**: Gestionar datos de métricas del dashboard

**Shape**:

.. code-block:: javascript

   {
     metrics: [
       {
         id: number,
         name: string,
         value: number | string,
         change: number,  // % cambio desde último periodo
         timestamp: string (ISO 8601),
       },
       ...
     ],
     loading: boolean,        // Fetch inicial en progreso?
     error: string | null,    // Error en fetch?
     filters: {
       startDate: Date,       // Filtro por fecha
       endDate: Date,
     },
     lastUpdate: string,      // Cuándo se actualizó por última vez
   }

**Acciones**:
- ``fetchMetrics`` (async thunk) - Cargar métricas iniciales
- ``updateMetrics`` (sincrónico) - Actualizar métricas (de WebSocket)
- ``setFilters`` (sincrónico) - Cambiar filtros
- ``clearError`` (sincrónico) - Limpiar error

**Selectores**:
- ``selectMetrics``: Array de métricas
- ``selectMetricsLoading``: ¿Está cargando?
- ``selectMetricsError``: Error actual
- ``selectMetricById``: Una métrica específica por ID
- ``selectFilteredMetrics``: Métricas filtradas (computado)
- ``selectMetricsTotal``: Suma total (computado)

**Decisiones de Diseño**:

1. **Metrics como array, no como objeto**:

   .. code-block:: javascript

      // Actual (array):
      metrics: [{ id: 1, name: 'Users', value: 100 }, ...]

      // Alternativa (objeto - NO usado):
      metrics: { byId: { 1: {...}, 2: {...} }, allIds: [1, 2] }

   - Razón: Dashboard muestra lista, no necesita búsqueda frecuente
   - Si escalas a 10,000+ métricas, considera normalization

2. **Timestamp en cada métrica**:
   - Permite saber cuándo se actualizó esa métrica
   - Razón: Dashboard tiempo real, timestamp es crítico

3. **Filters separados del estado de datos**:
   - Filters en su propio objeto
   - Razón: Se pueden cambiar sin afectar datos
   - Selectores computados aplican filtros

4. **lastUpdate a nivel de slice**:
   - Cuándo se actualizó el todo el dashboard por última vez
   - Razón: UI puede mostrar "actualizado hace X segundos"

**Patrón de Async**:

.. code-block:: javascript

   // fetchMetrics es async thunk con:
   // - pending: loading = true
   // - fulfilled: metrics = payload, loading = false, error = null
   // - rejected: error = message, loading = false

   dispatch(fetchMetrics());
   // → State: { loading: true, metrics: [], error: null }
   // (Request en progreso)

   // Cuando termina:
   // → State: { loading: false, metrics: [...], error: null }
   // o
   // → State: { loading: false, metrics: [], error: "Network error" }

----

Decisiones Arquitectónicas
--------------------------

1. Normalization
~~~~~~~~~~~~~~~~

**Decisión**: NO normalizar metrics (array plano)

**Razón**: 
- IACT tiene pocas métricas (5-10)
- Array es más simple que estructura normalizada
- Selectores suficientes para casos comunes

**Cuándo normalizar**:
- Si > 100 métricas
- Si necesitas actualizar individual frecuentemente
- Si relaciones complejas entre datos

**Estructura normalizada sería**:

.. code-block:: javascript

   metrics: {
     byId: {
       1: { name: 'Users', value: 100, change: 5 },
       2: { name: 'Revenue', value: 5000, change: -2 },
     },
     allIds: [1, 2],
   }

2. Loading States
~~~~~~~~~~~~~~~~~

**Decisión**: Usar patrón ``loading`` + ``error`` en todos los slices

.. code-block:: javascript

   // Patrón consistente en auth y dashboard:
   {
     data: any,
     loading: boolean,
     error: string | null,
   }

**Ventaja**: 
- Consistencia
- Fácil de testear
- UX predecible

**Uso en componentes**:

.. code-block:: javascript

   if (loading) return <Spinner />;
   if (error) return <ErrorMessage error={error} />;
   return <DataView data={data} />;

3. Selectores Memoizados
~~~~~~~~~~~~~~~~~~~~~~~~

**Decisión**: Usar reselect para selectores computados

.. code-block:: javascript

   // Sin memoización (re-computa cada render):
   const selectFilteredMetrics = (state) => {
     return state.dashboard.metrics.filter(...);
   };

   // Con memoización (computa solo si dependencies cambian):
   export const selectFilteredMetrics = createSelector(
     selectMetrics,
     selectFilters,
     (metrics, filters) => metrics.filter(...)
   );

**Beneficio**: Previene re-renders innecesarios

4. Async Thunks vs API calls
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Decisión**: Usar createAsyncThunk de Redux Toolkit

.. code-block:: javascript

   // Thunk:
   export const fetchMetrics = createAsyncThunk(
     'dashboard/fetchMetrics',
     async (_, { rejectWithValue }) => {
       try {
         const response = await fetch('/api/metrics');
         return await response.json();
       } catch (error) {
         return rejectWithValue(error.message);
       }
     }
   );

   // Uso en componente:
   useEffect(() => {
     dispatch(fetchMetrics());
   }, [dispatch]);

**Ventaja**:
- Manejo automático de loading/error
- Integrado con Redux
- Fácil de testear

5. WebSockets vs HTTP
~~~~~~~~~~~~~~~~~~~~~

**Decisión**: Usar WebSockets para actualizaciones en tiempo real

**Flujo**:
1. HTTP: Cargar datos iniciales con ``fetchMetrics`` (thunk)
2. WebSocket: Recibir updates con ``updateMetrics`` (action síncrona)

.. code-block:: javascript

   // En DashboardPage:
   useEffect(() => {
     // Cargar inicial
     dispatch(fetchMetrics());

     // Subscribirse a updates
     const unsubscribe = subscribe('metricsUpdate', (data) => {
       dispatch(updateMetrics(data));
     });

     return unsubscribe;
   }, [dispatch]);

**Razón**: 
- HTTP es más robusto para datos iniciales
- WebSocket es eficiente para updates frecuentes

----

Mejores Prácticas Implementadas
-------------------------------

✓ **Immutability**: Redux Toolkit con Immer
✓ **Separation of Concerns**: Auth y Dashboard en slices separados
✓ **Type Safety**: PropTypes en componentes
✓ **Performance**: Selectores memoizados, React.memo, useMemo
✓ **Error Handling**: Patrón consistente de loading/error
✓ **Testing**: Reducers y thunks con tests unitarios
✓ **Code Splitting**: React.lazy para rutas
✓ **Performance Monitoring**: Lighthouse + webpack-bundle-analyzer

----

Anti-patterns a Evitar
----------------------

❌ **Guardar en state si puede derivarse**:

.. code-block:: javascript

   // MAL:
   { firstName, lastName, fullName: 'John Doe' }

   // BIEN:
   { firstName, lastName }
   // Derivar en selector:
   const selectFullName = createSelector(
     selectFirstName,
     selectLastName,
     (first, last) => `${first} ${last}`
   );

❌ **Múltiples fuentes de verdad**:

.. code-block:: javascript

   // MAL:
   // Redux: { user: { email: 'test@test.com' } }
   // LocalStorage: { userEmail: 'test@test.com' }
   // State local: { userEmail: 'test@test.com' }

   // BIEN: Un único lugar
   // Redux: { user: { email: 'test@test.com' } }

❌ **Ignorar efectos secundarios**:

.. code-block:: javascript

   // MAL:
   dispatch(loginUser(credentials)); // No esperar resultado

   // BIEN:
   const result = await dispatch(loginUser(credentials));
   if (result.meta.requestStatus === 'fulfilled') {
     navigate('/dashboard');
   }

----

Escalabilidad
-------------

Si IACT crece y necesita:

Más Slices
~~~~~~~~~~

.. code-block:: javascript

   const store = configureStore({
     reducer: {
       auth: authReducer,
       dashboard: dashboardReducer,
       notifications: notificationsReducer,  // Agregar
       theme: themeReducer,                  // Agregar
       settings: settingsReducer,            // Agregar
     },
   });

Más Métricas (100+)
~~~~~~~~~~~~~~~~~~~

Refactorizar a estado normalizado:

.. code-block:: javascript

   metrics: {
     byId: { ... },
     allIds: [ ... ],
   }

Más Selectores
~~~~~~~~~~~~~~

Crear archivo ``dashboardSelectors.js`` con todos los selectores

Cache/Persistence
~~~~~~~~~~~~~~~~~

Agregar persistencia con redux-persist:

.. code-block:: javascript

   npm install redux-persist

   import persistStore from 'redux-persist/lib/persistStore';
   const persistor = persistStore(store);

----

Checklist para Code Review
--------------------------

Cuando revises código de React/Redux, verifica:

- [ ] ¿El estado es flat y normalizado cuando es necesario?
- [ ] ¿Hay single source of truth para cada dato?
- [ ] ¿Los loading/error states siguen el patrón?
- [ ] ¿Se usan selectores memoizados cuando es apropiadado?
- [ ] ¿Los async thunks tienen manejo de error?
- [ ] ¿Los componentes usan Redux o state local correctamente?
- [ ] ¿Se evitan los 7 anti-patterns?

----

Conclusión
----------

El estado de IACT está diseñado para ser:
- **Simple**: Fácil de entender
- **Escalable**: Puede crecer sin problemas
- **Performante**: Selectores memoizados
- **Testeable**: Reducers puros y determinísticos
- **Mantenible**: Patrón consistente

Para nuevas features, sigue estos principios y el código
se mantendrá limpio y eficiente.

Contacto
--------

Para preguntas sobre el state design, consulta:
- ``src/redux/store.js`` - Configuración del store
- ``src/redux/slices/`` - Definición de slices
- ``src/redux/selectors/`` - Selectores memoizados
- ``tests/unit/reducers/`` - Tests de reducers

