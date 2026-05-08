.. meta::
 :artefacto: ADR_GOB_010
 :tipo: ADR
 :dominio: normativa
 :subdominio: gobernanza
 :estado: Propuesto
 :version: 2.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _adr-gob-010:

================================================================
ADR-GOB-010 — Mecanismo de Autorizacion DRF para RBAC IACT
================================================================

.. note::

 **Architecture Decision Record — Pendiente de aprobacion.**

 Registra la decision arquitectonica sobre el mecanismo de
 integracion entre el modelo RBAC IACT y el sistema de
 autorizacion de Django REST Framework. Debe ser aprobado
 por el equipo de arquitectura antes de iniciar la
 implementacion de DEC-003 del CIA-RBAC-002.

 Relacionados:

 - :doc:`adr-gob-008-rbac-coexistencia-acc-perm`
 - :doc:`/gestion/evidencia/rbac-arquitectura/cia-rbac-002-arquitectura-permisos-drf`
 - :doc:`/normativa/restricciones/cnst-033-vocabulario-unificado-rbac`

----

1. Estado
=========

**Propuesto.**

Pendiente de revision y aprobacion por el equipo de arquitectura.

----

2. Contexto
===========

2.1 El modelo RBAC IACT
------------------------

El modelo RBAC IACT v5.2.1 define un catalogo de funciones
atomicas (``Function``) que se asignan a usuarios directamente
o via grupos (``FunctionGroup``), con restricciones de
separacion de funciones (``SeparationRule``). La gestion de
estas entidades se realizara a traves de interfaces
administrativas propias del sistema IACT — construidas desde
cero — no a traves del Django Admin nativo.

El metodo central del modelo es ``calculate_effective_functions()``,
que retorna el conjunto de codenames activos para un usuario dado,
considerando asignaciones directas, grupos y reglas de separacion.

2.2 El contrato de autorizacion Django
---------------------------------------

Django REST Framework verifica permisos a traves de clases que
implementan ``has_permission`` y ``has_object_permission``. Estas
clases pueden delegar a ``user.has_perm()``, cuyo contrato exige
el formato ``app_label.codename``.

El backend estandar de Django (``ModelBackend``) resuelve ese
contrato contra la tabla ``auth_permission``. Esta tabla es
infraestructura Django: gestiona permisos sobre modelos Django
(``add_user``, ``change_post``, ``delete_logentry``) y su ciclo
de vida esta acoplado al de las migraciones Django.

2.3 La tension
--------------

El modelo IACT tiene su propia tabla ``functions`` como registro
de autoridad para permisos de negocio. La tabla ``auth_permission``
es un registro de infraestructura Django. Estos son dos dominios
con ciclos de vida distintos:

.. list-table::
 :header-rows: 1
 :widths: 25 37 38

 * - Tabla
   - Dominio
   - Ciclo de vida
 * - ``functions``
   - Negocio IACT
   - Evoluciona con el catalogo de funciones del negocio
 * - ``auth_permission``
   - Infraestructura Django
   - Evoluciona con las migraciones Django

La decision central de este ADR es como integrar el dominio IACT
con el contrato ``user.has_perm()`` sin acoplar indebidamente
el ciclo de vida del catalogo IACT al ciclo de vida de la
infraestructura Django.

2.4 Alcance
-----------

Esta decision afecta:

- El mecanismo por el cual ``user.has_perm()`` resuelve permisos
  del dominio ``permissions``.
- La relacion entre la tabla ``functions`` y la tabla
  ``auth_permission``.
- La clase de permiso DRF que verifica funciones en vistas.
- El formato del identificador retornado por
  ``calculate_effective_functions``.

Esta decision no afecta:

- El modelo de datos de ``Function``, ``FunctionGroup`` ni
  ``SeparationRule``.
- La logica de calculo de funciones efectivas.
- Los permisos Django estandar de otros modulos
  (``auth.add_user``, ``admin.view_logentry``, etc.).
- La gestion administrativa de funciones IACT, que se realiza
  mediante interfaces propias del sistema.

----

3. Drivers de la Decision
==========================

**D1 — Separacion de dominios.**
``auth_permission`` pertenece al dominio de infraestructura
Django. ``functions`` pertenece al dominio de negocio IACT.
Una decision de integracion correcta no debe mezclar la
responsabilidad de ambos dominios.

**D2 — Independencia de ciclos de vida.**
El catalogo de funciones IACT evoluciona con los requerimientos
del negocio. Las migraciones Django evolucionan con el modelo
de datos. Estos ciclos de vida son independientes y deben
mantenerse independientes.

**D3 — Compatibilidad con el contrato de** ``user.has_perm()``.
El resto del ecosistema Django usa ``has_perm()``. El mecanismo
elegido debe ser compatible con ese contrato sin modificarlo ni
romperlo para otros modulos del sistema.

**D4 — Ausencia de strings literales en el codigo.**
Strings de permisos dispersos en vistas y servicios son una
categoria de bug silencioso. Django no lanza error si el permiso
no existe — retorna ``False``. El mecanismo debe proveer un
punto unico de definicion de esos strings.

**D5 — Compatibilidad con renombre de app.**
Si el ``app_label`` del modulo ``permissions`` cambia, el impacto
debe estar localizado en un unico archivo.

**D6 — Clean Code.**
Los nombres de clases, archivos y modulos deben expresar
proposito de dominio, no mecanismo de implementacion ni contexto
que el path ya provee.

----

4. Opciones Consideradas
========================

4.1 Opcion A — ``auth_permission`` como puente
-----------------------------------------------

Crear objetos ``Permission`` de Django para cada funcion del
catalogo IACT, anclados a un ``ContentType`` del modulo
``permissions``. ``ModelBackend`` resuelve los permisos contra
``auth_permission`` de forma estandar.

**Ventajas:**

- No requiere codigo custom en ``AUTHENTICATION_BACKENDS``.
- Compatibilidad nativa con el sistema de asignacion de permisos
  del Django Admin.

**Desventajas:**

Acopla el ciclo de vida del catalogo IACT al ciclo de vida de
las migraciones Django. Cada nueva funcion en el catalogo
requiere una migracion adicional para crear el objeto
``Permission`` correspondiente en ``auth_permission``. Viola D2.

Asigna a ``auth_permission`` la responsabilidad de registrar
funciones de negocio IACT. ``auth_permission`` es infraestructura
Django — no es el registro correcto para ese dominio. Viola D1.

La compatibilidad con el Django Admin declarada como ventaja
no aplica en este sistema: la gestion de funciones IACT se
realizara a traves de interfaces propias. Las entidades
``FunctionGroup`` y ``SeparationRule`` requieren interfaces de
administracion custom independientemente de la opcion elegida.
La ventaja declarada no es una ventaja real en este contexto.

**Evaluacion contra drivers:**

.. list-table::
 :header-rows: 1
 :widths: 12 62 26

 * - Driver
   - Evaluacion
   - Resultado
 * - D1
   - Mezcla dominio IACT con infraestructura Django
   - No cumple
 * - D2
   - Cada cambio en el catalogo requiere migracion adicional
   - No cumple
 * - D3
   - Compatible via ``ModelBackend`` estandar
   - Cumple
 * - D4
   - No provee punto unico; strings siguen dispersos
   - No cumple sin implementacion adicional
 * - D5
   - ``app_label`` hardcodeado en los objetos ``Permission``
   - No cumple
 * - D6
   - Nombres no aplican directamente a esta opcion
   - Neutro

4.2 Opcion B — Custom backend ``FunctionAuthorization``
--------------------------------------------------------

Implementar un backend de autorizacion Django que intercepta
llamadas ``has_perm()`` del dominio ``permissions`` y las
resuelve directamente contra ``calculate_effective_functions()``,
sin consultar ``auth_permission``. Las llamadas de otros dominios
se dejan pasar al siguiente backend en ``AUTHENTICATION_BACKENDS``.

**Ventajas:**

El dominio IACT y el dominio de infraestructura Django mantienen
ciclos de vida independientes. Cumple D1 y D2.

Agregar una funcion al catalogo IACT no requiere migracion
adicional.

El contrato publico ``user.has_perm()`` se mantiene intacto para
todos los modulos del sistema. Cumple D3.

Compatible con D4, D5 y D6 mediante ``FunctionCatalog`` y la
resolucion dinamica de ``app_label``. Ver CIA-RBAC-002,
DEC-004 y DEC-006.

**Desventajas:**

Requiere implementacion de un backend custom.

El Django Admin no lista permisos IACT en su interfaz nativa
de asignacion de permisos. Este punto es aceptable porque la
gestion de permisos IACT se realiza a traves de interfaces
propias del sistema.

**Evaluacion contra drivers:**

.. list-table::
 :header-rows: 1
 :widths: 12 62 26

 * - Driver
   - Evaluacion
   - Resultado
 * - D1
   - Dominios separados; ``auth_permission`` no recibe entradas IACT
   - Cumple
 * - D2
   - Cambios en catalogo no requieren migraciones adicionales
   - Cumple
 * - D3
   - Contrato ``has_perm()`` intacto para todos los modulos
   - Cumple
 * - D4
   - ``FunctionCatalog`` centraliza todos los strings
   - Cumple
 * - D5
   - ``app_label`` resuelto via ``AppConfig`` en un unico punto
   - Cumple
 * - D6
   - Nomenclatura expresa proposito de dominio
   - Cumple

----

5. Decision
===========

**Se adopta la Opcion B.**

El argumento central es de separacion de dominios y de ciclos de
vida. ``auth_permission`` es infraestructura Django con un ciclo
de vida acoplado a migraciones. ``functions`` es dominio IACT con
un ciclo de vida acoplado al catalogo de funciones del negocio.
Introducir entradas IACT en ``auth_permission`` — via Opcion A —
asigna a infraestructura Django la responsabilidad de registrar
conceptos del dominio de negocio IACT. Esa asignacion de
responsabilidad es incorrecta.

La unica ventaja concreta de la Opcion A — compatibilidad nativa
con el Django Admin — no aplica en este sistema, porque la gestion
de funciones IACT se realizara mediante interfaces propias que
deben construirse independientemente de la opcion elegida.

El costo de implementar un backend custom es puntual y acotado.
El costo de mantener ``auth_permission`` como registro de
funciones IACT es recurrente: cada cambio en el catalogo requiere
una accion adicional en la capa de infraestructura Django.

La Opcion B cumple los seis drivers. La Opcion A cumple uno.

----

6. Implementacion
=================

La implementacion detallada de esta decision esta especificada
en :doc:`/gestion/evidencia/rbac-arquitectura/cia-rbac-002-arquitectura-permisos-drf`,
DEC-003. A continuacion se presenta el resumen ejecutivo.

6.1 Backend ``FunctionAuthorization``
--------------------------------------

.. code-block:: python

   # permissions/backends.py

   from django.apps import apps
   from permissions.services import calculate_effective_functions


   class FunctionAuthorization:
       """
       Autoriza usuarios verificando sus funciones efectivas.

       Intercepta has_perm() del dominio 'permissions' y lo resuelve
       contra calculate_effective_functions(). Llamadas de otros
       dominios se dejan pasar a ModelBackend.
       """

       APP_LABEL = apps.get_app_config('permissions').label

       def authenticate(self, request, **kwargs):
           return None

       def has_perm(self, user_obj, perm, obj=None) -> bool:
           if not user_obj.is_active:
               return False

           if '.' not in perm:
               return False

           app_label, codename = perm.split('.', 1)

           if app_label != self.APP_LABEL:
               return False

           effective = calculate_effective_functions(user_obj)
           return codename in effective

6.2 Registro en ``AUTHENTICATION_BACKENDS``
--------------------------------------------

.. code-block:: python

   # config/settings.py

   AUTHENTICATION_BACKENDS = [
       'permissions.backends.FunctionAuthorization',
       'django.contrib.auth.backends.ModelBackend',
   ]

El orden es significativo. Django itera los backends en orden y
retorna en el primer ``True``. ``FunctionAuthorization`` debe
preceder a ``ModelBackend`` para que los permisos del dominio
``permissions`` sean interceptados antes de llegar a
``auth_permission``.

6.3 Comportamiento resultante
------------------------------

.. list-table::
 :header-rows: 1
 :widths: 40 32 28

 * - Llamada
   - Backend que responde
   - Fuente de datos
 * - ``has_perm('permissions.view_reports')``
   - ``FunctionAuthorization``
   - Tabla ``functions`` (IACT)
 * - ``has_perm('permissions.export_csv')``
   - ``FunctionAuthorization``
   - Tabla ``functions`` (IACT)
 * - ``has_perm('auth.add_user')``
   - ``ModelBackend``
   - Tabla ``auth_permission``
 * - ``has_perm('admin.view_logentry')``
   - ``ModelBackend``
   - Tabla ``auth_permission``

6.4 Restriccion critica de implementacion
------------------------------------------

El filtro ``if app_label != self.APP_LABEL: return False`` es
obligatorio. Sin el, ``FunctionAuthorization`` intercepta la
totalidad de llamadas ``has_perm()`` del sistema, incluyendo
permisos de ``auth`` y ``admin``. El resultado es la ruptura
silenciosa del sistema de autorizacion completo cuando algun
codename IACT colisiona con uno nativo Django.

Esta restriccion debe verificarse mediante un test de integracion
que confirme que ``has_perm('auth.add_user')`` no es interceptado
por ``FunctionAuthorization``.

----

7. Consecuencias
================

7.1 Positivas
-------------

El ciclo de vida del catalogo IACT es independiente del ciclo
de vida de las migraciones Django. Agregar, modificar o eliminar
funciones del catalogo no requiere migraciones adicionales mas
alla de los cambios en el modelo ``Function``.

El contrato ``user.has_perm('permissions.view_reports')`` es
compatible con el ecosistema Django estandar — templates,
decorators y vistas genericas funcionan sin modificacion.

``auth_permission`` conserva su responsabilidad original:
registrar permisos sobre modelos Django. No recibe entradas de
dominio IACT.

7.2 Negativas y mitigaciones
-----------------------------

**El Django Admin no lista permisos IACT en su interfaz nativa.**
Aceptable en el estado actual del sistema porque la asignacion
de funciones IACT se gestiona a traves de la interfaz propia.
Si en el futuro se requiere integracion con el Admin nativo, se
debera implementar un ``ModelAdmin`` custom para ``Function`` y
``FunctionGroup``, o reevaluar esta decision bajo los criterios
de la seccion 9.

**Requiere un backend custom.**
El backend ``FunctionAuthorization`` es codigo adicional a
mantener. Su complejidad es baja y su comportamiento es
predecible: intercepta permisos del dominio ``permissions`` y
deja pasar el resto a ``ModelBackend``.

7.3 Neutrales
-------------

``ModelBackend`` continua activo como segundo backend para
permisos de otros modulos del sistema (``auth``, ``admin``,
etc.). No hay impacto en esos modulos.

``auth_permission`` sigue existiendo y siendo utilizada por
``ModelBackend`` para los permisos que le corresponden. No se
elimina ni se modifica.

----

8. Artefactos Resultantes
==========================

.. list-table::
 :header-rows: 1
 :widths: 42 58

 * - Archivo
   - Contenido
 * - ``permissions/backends.py``
   - ``class FunctionAuthorization``
 * - ``permissions/catalog.py``
   - ``class FunctionCatalog``
 * - ``permissions/enforcement.py``
   - ``class FunctionAccessPolicy``
 * - ``permissions/services.py``
   - ``def calculate_effective_functions()``
 * - ``permissions/apps.py``
   - ``class PermissionsConfig``
 * - ``config/settings.py``
   - ``AUTHENTICATION_BACKENDS`` actualizado

----

9. Criterios de Revision
=========================

Esta decision debe ser revisada si ocurre alguna de las
siguientes condiciones:

**C1 — Integracion con Django Admin nativo.**
Se requiere que los permisos IACT sean listados y asignables
desde el Django Admin nativo, y no es viable implementar un
``ModelAdmin`` custom para ``Function`` y ``FunctionGroup``.

**C2 — Degradacion de performance.**
El volumen de llamadas a ``calculate_effective_functions()`` por
request genera degradacion de performance medible. En este caso
se debe evaluar una estrategia de cache antes de revisar la
decision de backend. La estrategia de cache no invalida esta
decision por si sola.

**C3 — Segundo modulo con modelo de permisos propio.**
Se introduce un modulo adicional con modelo de permisos propio
que requiera el mismo patron. En ese caso se debe evaluar una
abstraccion generica en lugar de backends especificos por
modulo, para evitar multiplicar implementaciones similares.

----

10. Trazabilidad
================

.. list-table::
 :header-rows: 1
 :widths: 32 68

 * - Referencia
   - Path
 * - Change Impact Assessment
   - :doc:`/gestion/evidencia/rbac-arquitectura/cia-rbac-002-arquitectura-permisos-drf`
 * - Modelo de datos vigente
   - :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index` (v5.2.1)
 * - Restriccion normativa aplicable
   - :doc:`/normativa/restricciones/cnst-033-vocabulario-unificado-rbac`
 * - ADR relacionado — coexistencia ACC+PERM
   - :doc:`adr-gob-008-rbac-coexistencia-acc-perm`
 * - Analisis historico que origino v5.2.1
   - :doc:`/gestion/evidencia/rbac-historia/analisis-errores-modelo-rbac-v5-2-0`
