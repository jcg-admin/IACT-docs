.. meta::
   :artefacto: CNST_028
   :tipo: Restriccion
   :dominio: normativa
   :subdominio: restricciones
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2025-12-17
   :ultimo_cambio: 2026-04-28
   :autor: NestorMonroy
   :clasificacion: Critico

.. _cnst-028:

=====================================================
CNST-028: Cifrado Obligatorio de Datos Confidenciales
=====================================================

Enunciado
---------

Los datos clasificados como ``Confidential`` y ``Restricted`` DEBEN
cifrarse en reposo y en transito en todas las exportaciones que los
incluyan.

Justificacion
-------------

Reduce el impacto de un acceso no autorizado a almacenamiento o
backup. Es requisito tipico de regulaciones aplicables al sector del
cliente.

Especificacion
--------------

- En reposo: cifrado a nivel columna con ``pgcrypto`` o equivalente
  para campos ``Restricted``; cifrado a nivel volumen para BD.
- En transito interno: TLS 1.2+ entre componentes.
- En exportaciones: ZIP con AES-256 + password fuera de banda.
- Las llaves se rotan minimo cada 12 meses.

Verificacion
------------

.. code-block:: bash

   psql -c "SELECT * FROM pg_extension WHERE extname='pgcrypto';"

Referencias cruzadas
--------------------

- :doc:`CNST_027_Clasificacion_Obligatoria_de_Datos_en_4_Niveles`
- :doc:`CNST_020_Throttling_de_Exportaciones_por_Formato`
