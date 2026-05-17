.. _uc-inc-rpt-01-parte-08-diagrama-clases:

8.3 Diagrama de clases
=======================

.. uml::
 :caption: UC_INC_RPT_01 — clases involucradas.

 @startuml

 class SegmentResolver {
   + resolve(user) : set of String
   + is_global(user) : Boolean
   + invalidate_cache(user_id) : void
 }

 class RBACRepo {
   + get_user_segments(user) : set of String
   + has_global_capability(user) : Boolean
 }

 class SegmentScope {
   + segments : set
   + es_global : Boolean
 }

 SegmentResolver --> RBACRepo : reads
 SegmentResolver --> SegmentScope : returns

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/segment-resolver`.
 - :doc:`/arquitectura-tecnica/domain-model/rbac-repo`.
