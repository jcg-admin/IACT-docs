# Test: Component Diagram with Centralized Styling

```yml
created_at: 2026-04-25 11:26:00
project: IACT-docs
phase: Phase 10 — EXECUTE
feature: plantuml-java-integration-impl
status: Test
```

## Validations

- ✓ !include path resolution (second diagram type)
- ✓ Style inheritance across diagram types
- ✓ Component and interface coloring
- ✓ Sphinx sphinxcontrib-plantuml integration

## Diagram

```puml
@startuml test-component-diagram
!include ../../../_static/plantuml-styles.puml

package "API Layer" {
  component [UserService]
  component [AuthService]
  component [NotificationService]
  interface "REST API" as rest
}

package "Database Layer" {
  component [MongoDB]
  component [Redis]
}

package "External Services" {
  component [EmailProvider]
  component [PaymentGateway]
}

UserService --> rest
AuthService --> rest
NotificationService --> rest
UserService --> MongoDB
AuthService --> Redis
NotificationService --> EmailProvider
PaymentGateway ..> MongoDB

@enduml
```

## Success Criteria

- [x] File created in discover/test-component-diagram.md
- [x] !include path correct: `!include ../../../_static/plantuml-styles.puml`
- [x] Diagram contains 3 packages and 8 components with relationships
- [x] Markdown is well-formed
- [x] Diagram syntax is valid PlantUML
