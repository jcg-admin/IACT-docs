Sucesos y acciones
==================

Puede agregar ciertos detalles a las líneas de transición. Puede
indicar **un suceso** que provoque una transición (desencadenar
un suceso), y la *actividad de cómputo* (la**acción**) que se
ejecute y haga que suceda la modificación del estado. Los
sucesos y acciones se escriben cerca de la línea de transición,
con una **diagonal** (``/``) para separar un suceso desencadenado
de una acción.

En ocasiones un evento causa una transición *sin una acción
asociada*, y algunas veces una transición sucede dado que*un
estado finaliza una actividad* (en lugar de hacerlo por un
suceso). Este tipo de transición se le conoce como **transición
no desencadenada**.

.. note:: Conceptos clave

 - **Transición:** cambio o paso de un estado a otro.
 - **Suceso (Evento):** algo que**OCURRE** y puede hacer que el
   sistema cambie de estado. *Dispara una transición*.

   - Un cliente presiona un botón
   - Llega un mensaje
   - Se alcanza cierta temperatura
   - El tiempo de espera expira

 - **Acción:** una**OPERACIÓN** o comportamiento que se
   ejecuta. Algo que el sistema **HACE como respuesta a un
   suceso**. Es la*parte ejecutable de la transición*.

   - Guardar datos en base de datos
   - Incrementar un contador
   - Enviar una notificación
   - Actualizar la interfaz

 - **Transición Desencadenada:** **siempre requiere un suceso
   específico** para ocurrir. La acción es**opcional**.

   - ``evento / acción`` — ej: ``boton_presionado / guardar_datos``
   - Sólo evento: ``tiempo_agotado`` (sin acción)

 - **Transición No Desencadenada:** **no requiere ningún suceso
   externo**. Se activa cuando un estado finaliza su actividad,
   ocurre **automáticamente**. La acción es opcional.

   - Cuando termina de procesar un pago, automáticamente pasa al
     siguiente estado.
   - Cuando termina de cargar datos, pasa al estado "listo".
   - No necesita esperar ningún evento externo.

La GUI con que interactúe le dará ejemplos de detalles de la
transición. Asumamos que la GUI puede establecerse en uno de
tres estados: **Inicialización**,**Operación**,**Apagado**.

- Cuando enciende su equipo, se ejecutará un proceso de arranque:
  *al encender se desencadena un suceso* que provoca que la GUI
  aparezca luego de una *transición desde el estado de
  Inicialización*, y*el arranque es una acción* que se realiza
  *durante tal transición*.
- Como resultado de las actividades en el estado de
  Inicialización, la GUI entra al modo de Operación.
- Cuando *desea apagar su PC*,*desencadena un suceso* que
  provoca la *transición hacia el estado de Apagado*, y con ello
  la PC se apaga (transición no desencadenada del Apagado al fin).

.. uml::

   @startuml

   [*] --> Inicializacion : encender / arrancar
   Inicializacion --> Operacion
   Operacion --> Apagado : apagar / cerrar_sesion
   Apagado --> [*]
   @enduml
