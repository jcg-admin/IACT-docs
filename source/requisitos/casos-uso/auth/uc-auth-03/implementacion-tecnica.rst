.. _uc-auth-03-parte-11:

=================================
Parte 11 — Implementacion tecnica
=================================

11.1 Stack
==========

.. list-table::
 :widths: 30 70
 :header-rows: 0

 * - **Backend**
   - Django 4.2+, DRF 3.14+, algoritmo-de-hash
 * - **BD**
   - MySQL 8.0
 * - **Generacion entropica**
   - ``secrets.SystemRandom``
 * - **Frontend**
   - React 18, Redux Toolkit

11.2 Backend — estructura
=========================

::

   apps/users/
   ├── views/
   │   └── reset_password_view.py    # ResetPasswordView
   ├── permissions.py                # HasResetPasswordFunction
   apps/auth_app/
   ├── services/
   │   ├── password_generator.py     # Strategy
   │   └── auth_service.py           # reset_password()
   ├── models/
   │   ├── user.py                   # User (touched fields)
   │   └── internal_message.py       # InternalMessage

11.3 Permission class
=====================

.. note::

 Los detalles de implementacion de este requisito estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.
11.4 ResetPasswordView
======================

.. note::

 Los detalles de implementacion de este requisito estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.
11.5 PasswordGenerator (Strategy)
=================================

.. note::

 Los detalles de implementacion de este requisito estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.
11.6 AuthService.reset_password
===============================

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
11.8 Throttling
===============

.. note::

 Los detalles de implementacion de este requisito estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.
11.9 Frontend
=============

.. code-block:: javascript

   // src/features/users/hooks/useResetPassword.js
   import { useState } from 'react';
   import { usersApi } from '../api/usersApi';
   import { toast } from '../../../ui/toast';

   export function useResetPassword() {
     const [loading, setLoading] = useState(false);

     const reset = async (userId, userName) => {
       const ok = await openConfirmModal({
         title: 'Resetear contrasena',
         message: `Esto cerrara las sesiones de ${userName} `
                  + `y le enviara una contrasena temporal a `
                  + `su buzon interno. ¿Continuar?`,
         destructive: true,
       });
       if (!ok) return;

       setLoading(true);
       try {
         const resp = await usersApi.resetPassword(userId);
         toast.success(
           'Contrasena reseteada. El usuario recibira '
           + 'la nueva contrasena en su buzon interno.');
       } catch (err) {
         toast.error(err.response?.data?.message
                     || 'Error al resetear');
       } finally {
         setLoading(false);
       }
     };

     return { reset, loading };
   }

11.10 Restriccion de logging
============================

.. note::

 Los detalles de implementacion de este requisito estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.
