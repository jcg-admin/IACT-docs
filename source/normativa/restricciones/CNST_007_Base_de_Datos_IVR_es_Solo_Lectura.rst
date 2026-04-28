.. meta::
   :artefacto: CNST_007
   :tipo: Restriccion
   :dominio: normativa
   :subdominio: restricciones
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2025-12-17
   :ultimo_cambio: 2026-04-28
   :autor: NestorMonroy
   :clasificacion: Critico

.. _cnst-007:

===========================================
CNST-007: Base de Datos IVR es Solo Lectura
===========================================

Enunciado
---------

El sistema IACT NO PUEDE ejecutar ninguna operacion de escritura
(INSERT, UPDATE, DELETE, DDL) contra la BD IVR. La inmutabilidad
desde IACT es absoluta y sin excepciones tecnicas.

Justificacion
-------------

La BD IVR es propiedad del cliente; cualquier escritura desde IACT
violaria el contrato de no-intervencion y crearia riesgo legal y
operacional. La inmutabilidad se enforza en tres niveles: permisos
de BD, configuracion Django y middleware de aplicacion.

Especificacion
--------------

- Usuario MySQL de IACT en BD IVR: solo permisos ``SELECT``.
- Modelos Django de IVR: ``managed = False`` y ``Meta.permissions``
  vacio.
- Router Django bloquea ``allow_migrate`` y enruta escrituras de
  modelos IVR a un error explicito.
- Middleware intercepta queries de modificacion sobre alias ``ivr``
  y las rechaza con respuesta 500.

Verificacion
------------

.. code-block:: bash

   mysql -u iact_user -e "SHOW GRANTS FOR CURRENT_USER" | grep -v SELECT && exit 1 || exit 0

Referencias cruzadas
--------------------

- :doc:`CNST_006_Arquitectura_de_Base_de_Datos_Dual`
- :doc:`CNST_008_Sincronizacion_ETL_en_Ventana_de_6_a_12_Horas`
