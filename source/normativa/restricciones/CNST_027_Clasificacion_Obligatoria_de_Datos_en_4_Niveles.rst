.. meta::
   :artefacto: CNST_027
   :tipo: Restriccion
   :dominio: normativa
   :subdominio: restricciones
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2025-12-17
   :ultimo_cambio: 2026-04-28
   :autor: NestorMonroy
   :clasificacion: Critico

.. _cnst-027:

=========================================================
CNST-027: Clasificacion Obligatoria de Datos en 4 Niveles
=========================================================

Enunciado
---------

Todo dato persistido en BD Analytics DEBE clasificarse en uno de
cuatro niveles: ``Public``, ``Internal``, ``Confidential``,
``Restricted``. Modelos sin clasificacion no se aceptan en code
review.

Justificacion
-------------

Sin clasificacion explicita, las decisiones de proteccion (cifrado, exportacion, RBAC) quedan a criterio caso a caso y son inconsistentes. La clasificacion explicita en el modelo permite enforce-ar las politicas en el codigo y en code review.

Niveles
-------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Nivel
     - Definicion
   * - Public
     - Datos publicables sin restriccion.
   * - Internal
     - Datos para uso interno; sin PII.
   * - Confidential
     - PII basica, datos de operacion sensibles. Requiere RBAC.
   * - Restricted
     - PII regulada, datos financieros. Requiere RBAC + cifrado.

Especificacion
--------------

- Cada modelo declara ``Meta.classification`` con uno de los 4
  valores.
- Datos ``Confidential`` y ``Restricted`` requieren cifrado en reposo
  (CNST_028).

Verificacion
------------

.. code-block:: python

   for model in apps.get_models():
       if hasattr(model.Meta, "classification"):
           assert model.Meta.classification in ["Public", "Internal", "Confidential", "Restricted"]

Referencias cruzadas
--------------------

- :doc:`CNST_028_Cifrado_Obligatorio_de_Datos_Confidenciales`
- :doc:`CNST_026_PII_Prohibida_en_Logs_y_Auditoria`
