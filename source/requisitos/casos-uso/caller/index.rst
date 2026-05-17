.. meta::
 :artefacto: INDEX_UC_CALLER
 :tipo: Indice
 :dominio: requisitos
 :subdominio: casos_uso/caller
 :estado: Fuera del scope
 :version: 1.1.0
 :fecha_creacion: 2026-05-01
 :ultimo_cambio: 2026-05-07
 :autor: NestorMonroy

==================================================
MOD_Caller — Cliente / Caller (External User View)
==================================================

.. warning:: **Cluster fuera del scope del proyecto IACT**

   Los 5 UCs de este cluster (uc-cli-01..05) estan declarados
   ``:estado: Fuera del scope`` desde 2026-05-07 (WP
   ``2026-05-07-04-50-49-std-012-prefix-normalization``).
   No se implementan en el proyecto v5.6.x. Su contenido
   documental se preserva pero no se actualiza
   activamente y sus diagramas no estan sujetos al ciclo
   de normalizacion STD-012 v1.1.0.

UCs desde la perspectiva del cliente que llama al
call center. El cliente NUNCA toca el sistema RBAC;
interactúa con IVR, agente, callback.

Casos de Uso
------------

.. toctree::
 :maxdepth: 1

 uc-cli-01/index
 uc-cli-02/index
 uc-cli-03/index
 uc-cli-04/index
 uc-cli-05/index
