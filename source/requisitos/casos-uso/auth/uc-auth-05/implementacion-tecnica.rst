.. _uc-auth-05-parte-11:

=================================
Parte 11 — Implementacion tecnica
=================================

11.1 Estructura backend
=======================

::

   apps/auth_app/
   ├── views/
   │   ├── session_list_view.py        # GET listado
   │   ├── session_detail_view.py      # GET detalle
   │   ├── session_close_view.py       # POST close
   │   └── close_all_sessions_view.py  # POST close-all
   ├── permissions.py                  # HasViewAllSessions, etc.
   ├── filters.py                      # SessionFilter (django-filter)
   ├── serializers/
   │   └── session_serializer.py
   ├── services/
   │   └── session_service.py          # close, close_all
   └── repositories/
       └── session_repository.py

11.2 Permission classes
=======================

.. note::

 Los detalles de implementacion de este requisito estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.

11.3 SessionListView
====================

.. note::

 Los detalles de implementacion de este requisito estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.

11.4 SessionFilter
==================

.. note::

 Los detalles de implementacion de este requisito estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.

11.5 SessionSerializer (sin PII)
================================

.. note::

 Los detalles de implementacion de este requisito estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.

11.6 SessionCloseView
=====================

.. note::

 Los detalles de implementacion de este requisito estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.

11.7 CloseAllSessionsView
=========================

.. note::

 Los detalles de implementacion de este requisito estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.

11.8 SessionService
===================

.. note::

 Los detalles de implementacion de este requisito estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.

11.9 URLs
=========

.. note::

 Los detalles de implementacion de este requisito estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.

11.10 Settings
==============

.. note::

 Los detalles de implementacion de este requisito estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.

11.11 Frontend
==============

.. code-block:: javascript

   // src/features/admin/sessions/SessionsTable.jsx
   import { useSessions } from './useSessions';

   export function SessionsTable({ filters }) {
     const { data, isLoading } = useSessions(filters);
     // tabla con paginacion, filtros, badge "TU SESION"
     // boton "Cerrar" con modal individual
   }

   // src/features/admin/sessions/useCloseAllSessions.js
   export function useCloseAllSessions() {
     return async (userId, userName) => {
       const ok = await openConfirmModal({
         title: 'Cerrar TODAS las sesiones',
         message: `Esto cerrara TODAS las sesiones de ${userName} `
                  + `inmediatamente. ¿Continuar?`,
         destructive: true, requireDoubleConfirm: true });
       if (!ok) return;
       await api.post(`/users/${userId}/close-all-sessions/`);
       toast.success(`Sesiones cerradas`);
     };
   }
