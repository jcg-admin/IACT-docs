.. _uc-inc-rpt-01-parte-11:

=================================
Parte 11 — Implementacion tecnica
=================================

Componente: ``SegmentResolver``.

Contrato:

::

   contract SegmentResolver:
     resolve(user_id) -> list[str]
       # retorna lista de segmentos: ['nacional_A', 'nacional_B', 'Puebla']
       # o subconjunto segun RBAC del usuario

Pseudocodigo:

::

   procedure resolve(user_id):
       asignaciones = RBACRepo.get_did_assignments(user_id)
       if asignaciones is empty and not RBACRepo.is_global_admin(user_id):
           raise SinSegmentoError(user_id)
       if RBACRepo.is_global_admin(user_id):
           return ['nacional_A', 'nacional_B', 'Puebla']
       segmentos = []
       DID_MAP = {
           '19028031': 'nacional_A',
           '19020001': 'nacional_B',
           '19020084': 'Puebla'
       }
       for did in asignaciones:
           if did in DID_MAP:
               segmentos.append(DID_MAP[did])
       return list(set(segmentos))

El resultado puede cachearse por sesion (TTL = duracion del
JWT) para evitar queries repetidas a PostgreSQL dentro de la
misma sesion de usuario.
