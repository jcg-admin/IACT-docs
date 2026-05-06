.. _uc-inc-rpt-01-parte-07:

================================
Parte 7 — Datos involucrados
================================

7.1 Entidades leidas
====================

- **SegmentoUsuario** — proyeccion de lectura derivada de
  la configuracion RBAC del usuario.

::

   SegmentoUsuario:
     usuario_id    : identificador del usuario
     segmentos     : lista de codigos de segmento
                     accesibles (nacional_A, nacional_B,
                     Puebla)
     es_global     : Boolean — True si el usuario tiene
                     acceso sin restriccion de segmento

7.2 Origen de los datos
=======================

Los segmentos se derivan de la tabla de asignaciones RBAC
(repositorio operacional IACT). No hay entidad
``SegmentoUsuario`` persistida; es una proyeccion calculada.

7.3 Indices
===========

- Lookup por ``usuario_id`` — O(1) si se cachea por sesion.
