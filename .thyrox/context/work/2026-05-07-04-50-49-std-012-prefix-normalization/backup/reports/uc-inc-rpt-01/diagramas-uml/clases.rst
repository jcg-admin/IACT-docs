8.3 Clases
==========

.. uml::

 @startuml
 class SegmentResolver {
   + resolve(user_id) : list[str]
 }
 class RBACRepo {
   + get_did_assignments(user_id) : list[str]
   + is_global_admin(user_id) : bool
 }
 SegmentResolver --> RBACRepo
 @enduml
