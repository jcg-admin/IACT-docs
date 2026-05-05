2. Componentes básicos
======================

Cuatro elementos canónicos: **objetos** (rectángulos con
nombre), **enlaces** (líneas que conectan objetos),
**mensajes numerados** sobre los enlaces, y **flechas** que
indican dirección.

.. uml::

   @startuml
   allowmixing

   object Objeto1
   object Objeto2
   object Objeto3

   Objeto1 -> Objeto2 : "1: mensaje()"
   Objeto2 -> Objeto3 : "2: mensaje()"
   Objeto3 -> Objeto1 : "3: respuesta()"
   @enduml

2.1 Sintaxis del mensaje
------------------------

::

 [condición] número [anidación] : operación(parámetros)

Ejemplos IACT:

::

 1: verificar_permiso(usuario, funcion)
 [usuario_activo] 2: aplicar_filtro_segmento(BR_012)
 2.1: validar_segmento_no_nulo()
 2.2: aplicar_SQL_WHERE(segmento)
 [* funcion_implicada en macro_funcion]
   3: verificar_permiso(usuario, sub_funcion)
 resultado := evaluar_umbral(metrica, umbral)
