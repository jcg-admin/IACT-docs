.. _br_001:

##############################################
BR-001: Inmutabilidad de la Base de Datos Fuente
##############################################

.. card:: Resumen de Atributos
   :shadow: md

   * **Identificador:** BR-001
   * **Prioridad:** Crítica
   * **Estado:** Validado
   * **Responsable:** Arquitectura de Datos

Descripción
-----------
El sistema IACT, incluyendo sus procesos de extracción (ETL) y la interfaz de visualización, tiene estrictamente prohibido realizar cualquier operación de escritura, actualización, borrado o modificación de esquema en la base de datos de origen (MySQL).

Racional de Negocio
-------------------
La base de datos MySQL sustenta las operaciones transaccionales diarias. Cualquier intervención de escritura por parte del sistema analítico podría comprometer la integridad de la fuente de verdad o degradar el rendimiento operativo, afectando la continuidad del negocio.

Criterios de Aceptación
-----------------------
1. El perfil de conexión a MySQL debe poseer exclusivamente privilegios de ``SELECT``.
2. El motor de extracción debe validar la inmutabilidad de los registros durante la fase de captura.
3. Las transformaciones y limpieza de datos deben persistirse exclusivamente en el entorno de destino (PostgreSQL).

Trazabilidad Technical
----------------------
* **Componente relacionado:** Proceso ETL (Backend Python).
* **Base de datos afectada:** MySQL Operativa.