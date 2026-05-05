PowerToys (TweakUI)
-------------------

Microsoft tiene un paquete llamado **PowerToys** que permite
hacer varias cosas con la GUI mediante una aplicación llamada
``TweakUI``.

Cuando lo descomprime, verá varios archivos con extensiones
``.dll``, un archivo de ayuda y un ``.CNT``. Hacer clic en el
archivo de ayuda generará un ``.GID``. Utilizar la característica
*Buscar* creará un ``.FTS``.

.. uml::

   @startuml
   allowmixing

   package "PowerToys" {
     component "TweakUI.exe"  as EXE
     component "TweakUI.dll"  as DLL
     component "TweakUI.hlp"  as HLP <<distribución>>
     component "TweakUI.cnt"  as CNT <<trabajo>>
     component "TweakUI.gid"  as GID <<ejecución>>
     component "TweakUI.fts"  as FTS <<ejecución>>
   }

   EXE ..> DLL : <<usa>>
   EXE ..> HLP : <<abre>>
   HLP ..> CNT : <<lee>>
   HLP ..> GID : <<genera>>
   HLP ..> FTS : <<genera>>
   @enduml
