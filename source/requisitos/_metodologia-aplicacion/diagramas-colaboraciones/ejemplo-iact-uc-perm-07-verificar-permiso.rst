4.1 Ejemplo IACT — UC_PERM_07 (Verificar permiso)
-------------------------------------------------

.. uml::

   @startuml
   allowmixing

   actor Backend
   object ":SecRules"           as SecRules
   object ":CatalogoFunciones"  as Cat
   object ":Usuario_grupos"     as UsuarioGrupos
   object ":PermisosTemporales" as PermisosTemporales
   object ":AuditoriaPermiso"   as AuditoriaPermiso

   Backend -> SecRules : "1: verificar_permiso(\n   user, fn)"
   SecRules -> Cat     : "1.1: existe_funcion(fn)?"
   SecRules -> UsuarioGrupos      : "1.2: [funcion_existe]\n   buscar_via_grupo(\n   user, fn)"
   SecRules -> PermisosTemporales      : "1.3: [no_via_grupo]\n   buscar_excepcional(\n   user, fn,\n   vigente_hoy)"
   SecRules -> AuditoriaPermiso      : "1.4: [permiso_resuelto]\n   registrar(\n   PERMISO_OK)"
   SecRules -> AuditoriaPermiso      : "1.5: [no_resuelto]\n   registrar(\n   PERMISO_DENEGADO)"
   SecRules -> Backend : "2: bool resultado"
   @enduml
