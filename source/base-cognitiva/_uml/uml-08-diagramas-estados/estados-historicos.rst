Estados históricos
==================

Cuando se activa su protector de pantallas y mueve su ratón
para regresar al estado *Operación*, ¿qué ocurre? ¿Acaso su
pantalla retoma el estado inicial, como si apenas se hubiera
encendido? ¿O lucirá tal como la dejó antes de que se activara
el protector? El **estado histórico** captura esta idea.

Un estado compuesto **recuerda su subestado activo** cuando el
objeto trasciende fuera del estado compuesto.

El símbolo es la **letra "H" encerrada en un círculo** que se
conecta por una línea continua al subestado por recordar, con
una punta de flecha que apunta a tal subestado.

.. uml::

   @startuml

   state Operacion {
     [*] --> Espera
     state Espera
     state Registro
     state Representacion
     Espera --> Registro
     Registro --> Representacion
     Representacion --> Espera
     state H <<history>>
   }
   ProtectorPantalla --> H : tecla / mov.Raton
   Operacion --> ProtectorPantalla : [tiempoInactivo > 15min]
   @enduml

- Cuando un estado histórico **recuerda los subestados en todos
  los niveles de anidación**, el estado histórico es
  **profundo**. Se representa agregando un asterisco (``*``) a
  la "H" en el círculo: ``H*``.
- Si sólo recuerda el subestado principal, el estado histórico
  será **superficial**.

El estado histórico y el estado inicial (representado por el
círculo relleno) son conocidos como **pseudoestados**. *No
tienen variables de estado ni actividades*, por lo que no son
estados "completos".

----
