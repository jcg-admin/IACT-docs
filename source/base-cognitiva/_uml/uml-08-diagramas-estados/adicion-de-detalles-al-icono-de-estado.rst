Adición de detalles al ícono de estado
--------------------------------------

UML le da la opción de agregar detalles a la simbología: es
posible dividir un símbolo de estado en tres áreas (similar al
símbolo de clase: nombre, atributos y operaciones).

- El **área superior** contendrá el nombre del estado (que tiene
  que establecerse exista o no la subdivisión).
- El **área central** contendrá las**variables de estado**
  (cronómetros, contadores).
- El **área inferior** las**actividades**.

Las actividades constan de **sucesos y acciones**. Tres de las
más utilizadas son:

- **entrada** (``entry``) — qué sucede cuando el sistema entra
  al estado.
- **salida** (``exit``) — qué sucede cuando el sistema sale del
  estado.
- **hacer** (``do``) — qué sucede cuando el sistema está en el
  estado.

Puede agregar otras si es necesario.

Cuando se envía un fax — esto es, cuando se encuentra en estado
de *Envío de fax* — la máquina anota la fecha y hora en que
inició el envío (los valores de las variables de estado
``fecha`` y ``hora``), y también anota su número telefónico así
como el nombre del propietario (``telefono`` y ``propietario``).
Al encontrarse en este estado, la máquina se encarga de agregar
un registro de fecha y hora al fax. En otras actividades, la
máquina jala las hojas, pagina el fax y finaliza la transmisión.
Mientras se encuentre en el estado de *Inactividad*, la máquina
muestra la fecha y la hora en una pantalla.

.. uml::

   @startuml

   state "Inactividad" as INA {
     INA : do / mostrarFechaYHora
   }

   state "Envío de fax" as ENV {
     ENV : fecha
     ENV : hora
     ENV : telefono
     ENV : propietario
     ENV : ---
     ENV : entry / registrarFechaYHora
     ENV : do / jalarHojas, paginar, transmitir
     ENV : exit / mostrarConfirmacion
   }

   [*]  --> INA
   INA  --> ENV : iniciarEnvio
   ENV  --> INA : finTransmision
   @enduml
