.. _arq-mod-008-restricciones:

================================================
ARQ_MOD_008 — Restricciones Aplicables
================================================

.. list-table::
 :widths: 15 85
 :header-rows: 1

 * - CNST
   - Descripcion y Aplicacion
 * - CNST_009
   - **Logging Auditoria Inmutable**: PII enmascarado en logs.
     No incluir passwords, tokens, datos sensibles.
 * - CNST_008
   - **Infraestructura Deployment**: Logs en /var/log/iact/.
     Rotacion automatica. Permisos restrictivos.
