4.1 Búsqueda de Llamada por id
------------------------------

.. uml::

   @startuml

   class Report
   class Call
   Report "1" -[#black]- "(id)" Call : searches
   note right of Call
     Calificador `id` reduce
     1:* a 1:1 en runtime.
     Se usa en UC_RPT_03 al
     consultar el detalle de
     una llamada específica.
   end note
   @enduml
