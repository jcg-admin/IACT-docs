.. meta::
   :artefacto: DEBT_004
   :tipo: Deuda Tecnica
   :dominio: risks-technical-debt
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2026-05-18T23:37:34
   :ultimo_cambio: 2026-05-18T23:37:34
   :autor: NestorMonroy
   :clasificacion: Interno

.. _deuda-integracion-r3-residual:

==================================================
Deuda Tecnica: Residuales de integracion R3
==================================================

Origen
======

Iniciativa ``integrar-contenido-rescatado``. Durante la
auditoria estatica de referencias previa a integrar (hallazgo
H-EJ1 de sus decisiones) se detectaron archivos que NO pueden
integrarse sin reintroducir deuda. Se registran aqui para no
dejarlos como cabo suelto.

Catalogo
========

.. list-table::
   :widths: 12 60 28
   :header-rows: 1

   * - ID
     - Descripcion
     - Estado
   * - DEBT-014
     - Los 8 archivos "nuevos" de R3 resultaron NO
       integrables tras auditoria: ``cnst-030-sod.rst``
       referencia cnst-029/031 inexistentes (2 ``:doc:``
       rotos); ``modelo-rbac-iact.rst`` (plano 2897 lin) y
       los 6 ``diagramas-uml.rst`` (planos) chocan con
       estructuras de SUBDIRECTORIO que develop ya tiene
       mas completas (``modelo-rbac-iact/`` 13 archivos,
       ``diagramas-uml/`` 5-6 archivos c/u). Integrar los
       planos seria huerfano + retroceso estructural.
       R3 estaba mas atrasado de lo que la fecha sugeria:
       develop evoluciono esos contenidos a subdirectorios
       despues del backup 17-mayo.
     - Activa
   * - DEBT-015
     - ``diagramas-uml.rst`` (R2) es archivo plano, pero
       develop ya tiene ``uc-sup-01/diagramas-uml/`` como
       subdirectorio con 6 archivos mas estructurados. No se
       integro (seria huerfano + retroceso). Si se quiere el
       contenido del plano, requiere fusionarlo en la
       estructura de subdirectorio existente, no reemplazar.
     - Activa
   * - DEBT-016
     - El ``index.rst`` de
       ``source/requisitos/casos-uso/supervision/uc-sup-01/``
       en develop usa nomenclatura antigua en su meta
       (``:subdominio: casos_uso/...`` con guion bajo,
       ``:artefacto: UC_SUP_01``). Deuda PREEXISTENTE en
       develop, no introducida por esta iniciativa, pero
       detectada durante ella. Migrar a nomenclatura kebab
       vigente.
     - Activa

Naturaleza
==========

DEBT-014 y DEBT-015 son contenido de R2/R3 que no se integro
por reintroducir deuda (referencias rotas / huerfano +
retroceso). DEBT-016 es deuda preexistente de develop
descubierta durante la auditoria. Ninguna se silencia: la
iniciativa integra solo lo verificado limpio (11 de R2) y
deja estas tres como deuda viva con accion concreta.


Insumo
======

El analisis y la auditoria estatica de referencias estan en
:doc:`/gestion/pm/iniciativas/integrar-contenido-rescatado/decisiones-integrar-contenido-rescatado`
(H-EJ1). No requieren re-analisis: requieren la accion
descrita por item.
