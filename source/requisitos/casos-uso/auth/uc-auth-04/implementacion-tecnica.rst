.. _uc-auth-04-parte-11:

=================================
Parte 11 — Implementacion tecnica
=================================

11.1 Stack
==========

Mismo que UC_AUTH_01..03 (Django/DRF, MySQL,
algoritmo-de-hash, React).

11.2 Estructura backend
=======================

::

   apps/auth_app/
   ├── views/
   │   └── change_password_view.py
   ├── serializers/
   │   └── change_password_serializer.py
   ├── services/
   │   ├── auth_service.py            # change_password()
   │   ├── password_policy.py         # PolicyValidator
   │   └── password_history.py        # HistoryChecker
   ├── models/
   │   ├── user.py
   │   └── password_history.py        # PasswordHistory
   └── urls.py

11.3 Serializer
===============

.. note::

 Los detalles de implementacion de este requisito estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.
11.4 ChangePasswordView
=======================

.. note::

 Los detalles de implementacion de este requisito estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.
11.5 PasswordPolicyValidator
============================

.. note::

 Los detalles de implementacion de este requisito estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.
11.6 AuthService.change_password
================================

.. note::

 Los detalles de implementacion de este requisito estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.
11.7 PasswordHistory model
==========================

.. note::

 Los detalles de implementacion de este requisito estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.
11.8 URL + throttling
=====================

.. note::

 Los detalles de implementacion de este requisito estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.
11.9 Frontend hook
==================

.. code-block:: javascript

   // src/features/auth/hooks/useChangePassword.js
   import { useState } from 'react';
   import { authApi } from '../api/authApi';
   import { toast } from '../../../ui/toast';
   import { useNavigate } from 'react-router-dom';

   export function useChangePassword() {
     const navigate = useNavigate();
     const [errors, setErrors] = useState({});

     async function submit({ current, next, confirm }) {
       setErrors({});
       try {
         const r = await authApi.changePassword({
           current_password: current,
           new_password: next,
           new_password_confirmation: confirm,
         });
         toast.success('Contrasena actualizada correctamente');
         if (r.scope_upgraded) navigate('/');
       } catch (err) {
         const e = err.response?.data;
         setErrors({
           code: e?.error,
           message: e?.message,
           violations: e?.violations,
         });
       }
     }

     return { submit, errors };
   }

11.10 Logging filter
====================

.. note::

 Los detalles de implementacion de este requisito estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.
