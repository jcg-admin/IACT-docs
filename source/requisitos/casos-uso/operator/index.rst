.. meta::
 :artefacto: INDEX_UC_OPERATOR
 :tipo: Indice
 :dominio: requisitos
 :subdominio: casos_uso/operator
 :estado: Fuera del scope
 :version: 1.2.0
 :fecha_creacion: 2026-05-01
 :ultimo_cambio: 2026-05-07
 :autor: NestorMonroy
 :clasificacion: Importante

================================================
MOD_Operator — Operacion del Agente (User View)
================================================

.. warning:: **Cluster fuera del scope del proyecto IACT**

 MOD_Operator es un **extension point open-closed** del modelo
 RBAC v5.6.0: declarado en el catalogo (10 funciones,
 ``operator:agent_state``..``operator:mailbox``) pero
 **fuera del scope del proyecto**. La documentacion de
 UC_OPR_01..10 se preserva como base para activacion futura,
 NO como especificacion implementable. Sus diagramas NO estan
 sujetos al ciclo de normalizacion STD-012 v1.1.0 (WP
 ``2026-05-07-04-50-49-std-012-prefix-normalization``).

 Modelo activo de v5.6.x: 67 funciones in-scope (catalogo
 declara 80 con 13 reservadas en MOD_Operator y
 MOD_Supervision). Ver
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`.

UCs derivados del principio UML-06: la perspectiva
del USUARIO de la máquina (agente operador), no la
implementación interna.

Casos de Uso
------------

.. toctree::
 :maxdepth: 1

 uc-opr-01/index
 uc-opr-02/index
 uc-opr-03/index
 uc-opr-04/index
 uc-opr-05/index
 uc-opr-06/index
 uc-opr-07/index
 uc-opr-08/index
 uc-opr-09/index
 uc-opr-10/index
