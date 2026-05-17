5. Adapter — LDAPUserAdapter
============================

**Problema.** ``auth_app`` consulta ``ldap-corporativo`` que
expone atributos LDAP estándar (``cn``, ``mail``,
``memberOf``); el dominio interno usa ``User`` con
``username``, ``email``, ``grupos[]``.

.. uml::

   @startuml
   class LDAPEntry {
     + cn : str
     + mail : str
     + memberOf : list
   }
   class User {
     + username : str
     + email : str
     + grupos : list
   }
   class LDAPUserAdapter {
     - entry : LDAPEntry
     + a_user() : User
   }
   LDAPUserAdapter --> LDAPEntry
   LDAPUserAdapter ..> User : produce
   @enduml

.. note::

 La implementacion del patron sigue la estructura mostrada en el
 diagrama UML. Los detalles de codigo van en el repositorio fuente,
 no en la especificacion.

Solo cambia el adapter si LDAP cambia de schema; el resto de
``auth_app`` permanece estable.
