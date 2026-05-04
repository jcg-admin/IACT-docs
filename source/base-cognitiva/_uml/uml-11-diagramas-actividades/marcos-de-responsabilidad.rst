Marcos de responsabilidad
=========================

El diagrama de actividades puede expandirse y mostrar **quién
tiene la responsabilidad** en un proceso.

Caso: firma de consultoría y proceso de negociación con un
cliente.

1. Un vendedor llama al cliente y concierta una cita.
2. Si la cita es en la oficina del consultor, los técnicos
   corporativos preparan una sala de conferencias para la
   presentación.
3. Si es en la oficina del cliente, un consultor prepara una
   presentación en una laptop.
4. El consultor y el vendedor se reúnen con el cliente.
5. El vendedor crea una minuta.
6. Si la reunión planteó la solución de un problema, el
   consultor crea una propuesta y la envía al cliente.

Para visualizar responsabilidades se separa el diagrama en
segmentos paralelos conocidos como **marcos de responsabilidad**
(*swimlanes*). Cada marco muestra el nombre de un responsable en
la parte superior y presenta sus actividades.

.. uml::

   @startuml

   |Vendedor|
   start
   :Llamar al cliente;
   :Concertar cita;
   if ([cita]) then (oficina consultor)
     |Técnicos corporativos|
     :Preparar sala\nde conferencias;
   else (oficina cliente)
     |Consultor|
     :Preparar presentación\nen laptop;
   endif
   |Vendedor|
   :Reunirse con cliente;
   |Consultor|
   :Reunirse con cliente;
   |Vendedor|
   :Crear minuta;
   |Consultor|
   if ([solución requerida]) then (sí)
     :Crear propuesta;
     :Enviar al cliente;
   endif
   stop
   @enduml

----
