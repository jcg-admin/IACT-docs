Importancia de los casos de uso
===============================

El diagrama de clases es un buen medio para estimular a un
**cliente** a que hable respecto a un sistema desde su propio
punto de vista. El caso de uso es una excelente herramienta para
estimular a que los **usuarios potenciales** hablen, de un
sistema, desde sus propios puntos de vista.

La idea es **involucrar a los usuarios en las etapas iniciales**
del análisis y diseño del sistema. Esto aumenta la probabilidad
de que el sistema sea de mayor provecho.

Un ejemplo: la **máquina de gaseosas**.

Suponga que empezará a diseñar una máquina despachadora de
gaseosas. Desde el punto de vista del interesado, entrevistará a
varios usuarios potenciales. Como resultado obtendrá la función
principal de una máquina de gaseosas: permitir a un cliente
adquirir una lata de gaseosa. Las personas le dirán que se
enfrentará a diversos escenarios — un caso de uso, en otras
palabras — que podría etiquetar como **"Comprar gaseosa"**.

.. uml::

   @startuml

   left to right direction
   actor Cliente
   rectangle "Máquina de Gaseosas" {
     usecase "Comprar gaseosa" as UC1
   }
   Cliente --> UC1
   @enduml

.. tip::

 Un caso de uso establece un conjunto de escenarios para
 realizar **algo útil (deseado) para un actor**. Un actor puede
 ser una persona, otro sistema, una parte del hardware o el
 paso del tiempo.

 Entre las preguntas que se tienen que responder con los casos
 de uso están:

 - ¿Qué condiciones llevaron al actor a iniciar el escenario?
 - ¿Qué se obtiene como resultado del escenario?
 - ¿Lo que he descrito es la única posibilidad del escenario?
 - ¿Qué pasa si el actor no cumple con los requisitos iniciales?
 - ¿Qué situaciones pueden impedir que el caso de uso alcance su
   propósito? ¿Cuáles son los puntos críticos donde podría
   fallar? ¿Qué pasa si el caso de uso falla? ¿Hay una ruta
   alternativa o acción correctiva?
 - ¿Qué pasa si el caso de uso tiene cambios?
 - ¿Qué sucede con los datos o el estado del sistema si el caso
   de uso se interrumpe?

En el caso de uso *"Comprar gaseosa"*, el actor es un**cliente
que desea** comprar una lata de gaseosa.

El escenario iniciará cuando el cliente inserte dinero,
posteriormente realizará una selección, y si todo funciona bien,
la máquina contará con al menos una lata de la gaseosa elegida,
misma que pondrá al alcance del cliente.

- **¿Qué condiciones llevaron al cliente a iniciar el escenario
  "Comprar gaseosa"?** La sed es la más obvia.
- **¿Qué se obtiene como resultado?** Lo obvio es que el cliente
  tenga una gaseosa en su poder.
- **¿Lo que he descrito es la única posibilidad?** No. Por
  ejemplo, es posible que la máquina no tenga la gaseosa que
  desee el cliente; también es posible que el cliente no tenga
  el importe exacto.

¿Cómo diseñaría a la máquina de gaseosas para controlar tales
**escenarios**?

Escenario: la máquina se ha quedado sin gaseosa
-----------------------------------------------

Imagínelo como una **ruta alternativa** dentro del caso de uso.
El cliente inicia el caso de uso al insertar dinero en la máquina
y posteriormente hace una selección. La máquina no cuenta con
ninguna lata de la gaseosa seleccionada, por lo que mostrará un
mensaje al cliente que indicará que no tiene de esa marca. Lo
ideal sería que el mensaje le pida al cliente que haga otra
selección; la máquina también debería dar la opción de devolver
el dinero al cliente. En este punto, el cliente selecciona otra
marca que la máquina entregará (siempre y cuando cuente con
provisiones de esta marca), o devolverá el dinero.

- **Condición previa:** un cliente sediento.
- **Resultado:** una lata de gaseosa**o** la (alternativa)
  devolución del dinero.

Claro que el escenario de quedarse sin gaseosa sería posible: el
mensaje *"No hay de esta marca"* podría aparecer en cuanto las
provisiones de la máquina se acabaran y permanecer a la vista
hasta que la máquina sea reabastecida. En tal caso, el usuario
podría no insertar el dinero en primera instancia. El cliente
para el que usted diseñará la máquina podría preferir el primer
escenario: si el cliente ya insertó dinero, la tendencia podría
ser **hacer otra selección** en lugar de pedir a la máquina que
lo devuelva.

Escenario: la cantidad de dinero es incorrecta
----------------------------------------------

El usuario inicia el caso de uso en la forma usual y
posteriormente hace una selección. Asumamos que la máquina tiene
provisión de la marca elegida. Si en la máquina hay una reserva
de moneda fraccionaria, devuelve la diferencia al despachar la
gaseosa; si la máquina **no cuenta con** una reserva de moneda
fraccionaria, devolverá el dinero **(alternativa)** y mostrará un
mensaje que pida al usuario el importe exacto.

- **Condición previa:** la ya indicada.
- **Resultado:** una lata de gaseosa junto con el cambio, o la
  devolución **(alternativa)** del dinero originalmente
  depositado.

Tan pronto como se agote la moneda fraccionaria, **aparezca un
mensaje** que informe a los clientes que se requiere el importe
exacto. El mensaje permanecería a la vista hasta que la máquina
sea reabastecida con moneda fraccionaria.
