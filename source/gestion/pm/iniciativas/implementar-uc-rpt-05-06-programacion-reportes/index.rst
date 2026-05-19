.. meta::
   :artefacto: INICIATIVA-IMPLEMENTAR-UC-RPT-05-06-PROGRAMACION-REPORTES
   :tipo: Iniciativa
   :dominio: gestion
   :subdominio: pm/iniciativas
   :repo_objetivo: IACT-api
   :estado: COMPLETADA
   :version: 1.1.0
   :fecha_creacion: 2026-05-19T20:13:49
   :ultimo_cambio: 2026-05-19T20:25:00
   :autor: NestorMonroy
   :clasificacion: Interno

.. _iniciativa-implementar-uc-rpt-05-06-programacion-reportes:

==============================================================
Iniciativa: Implementar UC_RPT_05/06 Programacion de Reportes
==============================================================

.. admonition:: Resultado: NO REQUIERE IMPLEMENTACION
   :class: important

   El deep-analysis revelo que ``UC_RPT_05`` y ``UC_RPT_06``
   **no son gaps de implementacion** — son **gaps en la
   numeracion del codigo**. Los UCs documentados que la
   iniciativa anterior asumio que correspondian a esos
   markers (``uc-036-programar-reporte`` y
   ``uc-037-ver-reportes-programados``) **ya estan
   implementados bajo ``UC_RPT_07`` y ``UC_RPT_08``** en el
   codigo de IACT-api.

   La iniciativa hermana
   ``auditar-cobertura-uc-implementacion`` asumio un mapeo
   lineal docs <-> codigo (uc-032 = UC_RPT_01,
   uc-033 = UC_RPT_02, ...) que no es correcto: el codigo
   salta del ``UC_RPT_04`` al ``UC_RPT_07``, dejando 05 y
   06 sin asignar (probable reserva o features retiradas).

   La iniciativa NO produce codigo nuevo. Su entrega es:
   (a) la correccion del mapping erroneo en la auditoria
   previa y (b) la identificacion del unico gap real en
   el dominio reports: ``UC_RPT_02`` (Real-time metrics)
   declarado explicitamente como STUB por restriccion
   arquitectonica CNST-004 (NO Channels, NO Celery).

.. toctree::
   :maxdepth: 1

   alcance-implementar-uc-rpt-05-06-programacion-reportes
   deep-analisis-implementar-uc-rpt-05-06-programacion-reportes
   tareas-y-progreso-implementar-uc-rpt-05-06-programacion-reportes
   decisiones-implementar-uc-rpt-05-06-programacion-reportes
