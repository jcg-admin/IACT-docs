.. meta::
 :artefacto: INDEX_AT_VISTAS_KRUCHTEN
 :tipo: Indice
 :dominio: arquitectura_tecnica
 :subdominio: vistas_kruchten
 :estado: Vigente
 :version: 1.1.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at-uc-index:

=============================================
Vista de Casos de Uso — Arquitectura Tecnica
=============================================

Diagramas arquitectonicos por UC siguiendo el modelo **4+1 de Kruchten**
(variante 5+1 con Domain Model). Cada subdirectorio contiene un archivo
por UC desde una perspectiva arquitectonica.

.. list-table::
 :widths: 25 20 55
 :header-rows: 1

 * - Vista
   - Tipo
   - Descripcion
 * - :doc:`domain-model/index`
   - Vista Logica
   - Entidades del dominio y relaciones para el UC.
     Diagrama de clases (conceptual) + estados.
 * - :doc:`design-view/index`
   - Vista de Diseno
   - Clases con detalle de diseno, secuencias, colaboracion.
     Como el sistema resuelve el UC tecnicamente.
 * - :doc:`implementation-view/index`
   - Vista de Implementacion
   - Componentes y paquetes. Organizacion del codigo.
 * - :doc:`use-case-view/index`
   - Vista de Casos de Uso
   - Diagrama UC con actores RBAC, includes y extends.
     Une todas las demas vistas.
 * - :doc:`process-view/index`
   - Vista de Procesos
   - Actividades y secuencias. Concurrencia, sincronizacion.
 * - :doc:`deploy-view/index`
   - Vista de Despliegue
   - Distribucion fisica. Nodos, artefactos, comunicacion.

----

.. toctree::
 :maxdepth: 2
 :caption: Vistas arquitectonicas

 domain-model/index
 design-view/index
 implementation-view/index
 use-case-view/index
 process-view/index
 deploy-view/index
