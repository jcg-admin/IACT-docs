.. _requisitos-funcionales-operator:

=====================================
Requisitos Funcionales — Operator
=====================================

.. warning:: Modulo reservado (out-of-scope para v5.6.0)

 MOD_Operator es un **extension point open-closed** del modelo
 RBAC v5.6.0. Los FR derivados de UC_OPR_01..10 se preservan como
 base de diseño para activacion futura, NO como especificacion
 implementable en esta release. Ver
 :doc:`/requisitos/casos-uso/operator/index` y
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`.

Requisitos Funcionales derivados de los 10 casos de uso del módulo
Operator (UC_OPR_01 .. UC_OPR_10). Cubre gestión de estados del agente,
atención de llamadas entrantes/salientes, hold, transferencia, disposición,
descansos, métricas propias, historial de llamadas y buzón interno.

.. toctree::
   :maxdepth: 2

   uc-022-cambiar-estado-agente/index
   uc-023-atender-llamada-entrante/index
   uc-024-iniciar-llamada-saliente/index
   uc-025-pausar-llamada/index
   uc-026-transferir-llamada/index
   uc-027-registrar-disposicion-llamada/index
   uc-028-solicitar-descanso/index
   uc-029-ver-metricas-propias/index
   uc-030-ver-historial-llamadas/index
   uc-031-leer-buzon-interno/index
