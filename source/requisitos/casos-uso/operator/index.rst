.. meta::
 :artefacto: INDEX_UC_OPERATOR
 :tipo: Indice
 :dominio: requisitos
 :subdominio: casos_uso/operator
 :estado: Reservado
 :version: 1.1.0
 :fecha_creacion: 2026-05-01
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Importante

================================================
MOD_Operator — Operacion del Agente (User View)
================================================

.. warning:: Modulo reservado (out-of-scope para v5.6.0)

 MOD_Operator es un **extension point open-closed** del modelo
 RBAC v5.6.0: declarado en el catalogo (10 funciones,
 ``operator:agent_state``..``operator:mailbox``) pero
 **out-of-scope para esta release**. La documentacion de
 UC_OPR_01..10 se preserva como base para activacion futura,
 NO como especificacion implementable en v5.6.0.

 Modelo activo de v5.6.0: 9 modulos / 64 funciones (ver
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`).
 Catalogo total declarado: 77 funciones (64 activas + 13
 reservadas en MOD_Operator y MOD_Supervision).

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
