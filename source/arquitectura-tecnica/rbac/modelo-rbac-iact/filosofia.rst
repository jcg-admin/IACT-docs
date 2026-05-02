.. _modelo-rbac-iact-filosofia:

===============================
Modelo RBAC IACT — Filosofia
===============================

1. FILOSOFÍA DEL MODELO
=======================



1.1 Principio Central
---------------------


   **Los nombres de funciones describen QUÉ HACE la función, NO QUIÉN es la persona**


1.2 Enfoque Sin Pretensiones
----------------------------


**[NO] INCORRECTO - Con Pretensiones:**


.. code-block:: text

 Roles basados en títulos:
 - USERS_FULL_MANAGER → Define QUÉ ES la persona
 - SYSTEM_ADMIN → Cargo jerárquico


**[OK] CORRECTO - Sin Pretensiones:**


.. code-block:: text

 Funciones basadas en acciones (INGLÉS):
 - create_users → Describe QUÉ PUEDE HACER
 - view_reports → Acción concreta
 - export_csv → Capacidad específica


