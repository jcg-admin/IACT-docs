Condiciones de seguridad
========================

Si ha pasado cierto tiempo sin que haya interacción con el
usuario, la GUI hará una transición del estado *Operación* al
estado *Protector de pantallas*. El intervalo se especifica en
su sistema operativo (por lo general 15 minutos).

Cualquier opresión de una tecla o movimiento del ratón provocará
una transición del estado *Protector de pantallas* al estado
*Operación*.

**El intervalo es una condición de seguridad** (*guard
condition*): cuando se cumple, se realiza la transición. La
condición de seguridad se establece como **expresión booleana**
entre corchetes ``[ ]``.

.. uml::

   @startuml

   [*] --> Inicializacion : encender / arrancar
   Inicializacion --> Operacion
   Operacion --> ProtectorPantalla : [tiempoInactivo > 15min]
   ProtectorPantalla --> Operacion : tecla / movimientoRaton
   Operacion --> Apagado : apagar / cerrar_sesion
   Apagado --> [*]
   @enduml

----
