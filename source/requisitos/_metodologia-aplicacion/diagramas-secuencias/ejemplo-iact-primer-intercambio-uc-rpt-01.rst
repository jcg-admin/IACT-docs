Ejemplo IACT — primer intercambio UC_RPT_01
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Aplicado al UC_RPT_01 (consultar dashboard) con SLA
CNST_017:

.. uml::

   @startuml
   title UC_RPT_01 — primer intercambio dashboard

   actor Supervisor
   participant "Browser" as Browser
   participant "rpt_app" as Rpt

   Supervisor -> Browser : selecciona dashboard
   Browser -> Rpt : GET /dashboard?segmento=N
   Rpt --> Browser : 200 OK (HTML + datos)
   Browser --> Supervisor : renderiza dashboard
   note right of Rpt
     SLA CNST_017: respuesta <= 10s
   end note
   @enduml

La nota referencia explícitamente la restricción
temporal sin saturar la etiqueta del mensaje. Este
patrón (mensaje + nota explicativa) se repite a lo
largo de la documentación IACT.
