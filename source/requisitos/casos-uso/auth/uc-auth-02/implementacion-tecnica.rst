.. _uc-auth-02-parte-11:

=================================
Parte 11 — Implementacion tecnica
=================================

11.1 Stack
==========

.. list-table::
 :widths: 30 70
 :header-rows: 0

 * - **Backend**
   - Django 4.2+, DRF 3.14+, djangorestframework-simplejwt
 * - **BD**
   - MySQL 8.0 (analitica)
 * - **Cache (opcional)**
   - Redis 7 para BlacklistedToken hot path
 * - **Frontend**
   - React 18, Redux Toolkit, React Router v6
 * - **Servidor**
   - Apache + mod_wsgi (ADR-DEVOPS-001)

11.2 Backend — estructura
=========================

::

   apps/auth_app/
   ├── views/
   │   └── logout_view.py            # LogoutView (DRF APIView)
   ├── services/
   │   ├── auth_service.py           # logout()
   │   └── token_invalidator.py      # Strategy pattern
   ├── models/
   │   ├── session.py                # Session
   │   └── blacklisted_token.py      # BlacklistedToken
   ├── serializers/
   │   └── logout_serializer.py
   └── urls.py                       # path('logout/', ...)

11.3 LogoutView (esqueleto)
===========================

.. note::

 Los detalles de implementacion de este requisito estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.
11.4 AuthService.logout (esqueleto)
===================================

.. note::

 Los detalles de implementacion de este requisito estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.
11.5 TokenInvalidator (Strategy)
================================

.. note::

 Los detalles de implementacion de este requisito estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.
11.6 Modelo Session
===================

.. note::

 Los detalles de implementacion de este requisito estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.
11.7 URL routing
================

.. note::

 Los detalles de implementacion de este requisito estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.
11.8 Frontend — estructura
==========================

::

   src/features/auth/
   ├── components/
   │   ├── LogoutButton.jsx
   │   └── LogoutConfirmModal.jsx
   ├── hooks/
   │   └── useLogout.js
   ├── slices/
   │   └── authSlice.js              # Redux Toolkit
   └── api/
       └── authApi.js                # logout() call

11.9 useLogout hook
===================

.. code-block:: javascript

   // src/features/auth/hooks/useLogout.js
   import { useDispatch } from 'react-redux';
   import { useNavigate } from 'react-router-dom';
   import { authApi } from '../api/authApi';
   import { clearAuth } from '../slices/authSlice';

   export function useLogout() {
     const dispatch = useDispatch();
     const navigate = useNavigate();

     return async () => {
       const refreshToken = localStorage.getItem('refresh_token');
       try {
         await authApi.logout({ refresh_token: refreshToken });
       } catch (err) {
         // logout local incluso si el backend falla
       } finally {
         localStorage.removeItem('access_token');
         localStorage.removeItem('refresh_token');
         dispatch(clearAuth());
         navigate('/login', {
           state: { message: 'Tu sesion fue cerrada correctamente' }
         });
       }
     };
   }

11.10 Configuracion DRF
=======================

.. note::

 Los detalles de implementacion de este requisito estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.
11.11 Cron de purga de blacklist
================================

.. note::

 Los detalles de implementacion de este requisito estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.
Cronjob: cada hora.
