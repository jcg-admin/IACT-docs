.. meta::
 :artefacto: AT_DM_CLASS_PASSWORD_GENERATOR
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Auth
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Importante

.. _dm_class_password_generator:

=================
PasswordGenerator
=================

Generador de passwords criptograficamente seguros para casos donde el
sistema crea credenciales: passwords iniciales al crear User
(UC_USR_01), passwords temporales en flujos de recovery (UC_AUTH_03),
y reset administrativo. Cumple con politicas de complejidad
configurables y entrega el password en plain text **una sola vez**
(via mailbox interno) para que el usuario lo cambie en su primer uso.

NO almacena el plain text — el ``password_hash`` se persiste en
``User`` mediante hashing seguro (bcrypt/argon2) y el plain text se
descarta tras la entrega.

.. uml::
 :caption: Clase PasswordGenerator — passwords seguros para User init.

 @startuml

 class PasswordGenerator {
   - policy : PasswordPolicy
   --
   + generate(policy : PasswordPolicy) : String
   + generate_initial(user_id : UUID) : String
   + generate_temporary(user_id : UUID, ttl : Duration) : String
   + meets_policy(plain : String, policy : PasswordPolicy) : Boolean
 }

 class PasswordPolicy {
   + min_length : Integer
   + require_uppercase : Boolean
   + require_lowercase : Boolean
   + require_digits : Boolean
   + require_symbols : Boolean
   + forbidden_patterns : List<String>
 }

 PasswordGenerator --> PasswordPolicy : usa

 note bottom of PasswordGenerator
   Default policy: 12 chars min,
   upper+lower+digit+symbol.
   Plain text entregado UNA vez via
   InternalMailbox y descartado.
   No persiste plain en logs (CNST-026).
 end note

 @enduml

Trazabilidad a UCs
==================

UCs que invocan PasswordGenerator:

- :doc:`/requisitos/casos-uso/users/uc-usr-01/index` —
  crear usuario: generate_initial entrega password al User
  destino via InternalMessage.
- :doc:`/requisitos/casos-uso/auth/uc-auth-03/index` —
  recuperar contraseña: generate_temporary con TTL corto.

Relaciones
==========

- :doc:`user` — recipient del password generado (almacena hash).
- :doc:`internal-message` — vehiculo de entrega del plain text una vez.
- :doc:`sanitizer` — asegura que el plain no entre a logs.
- :doc:`audit-service` — emite ``PASSWORD_GENERATED`` (sin el plain).
