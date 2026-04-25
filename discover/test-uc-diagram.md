# Test: Use Case Diagram with Centralized Styling

```yml
created_at: 2026-04-25 11:25:00
project: IACT-docs
phase: Phase 10 — EXECUTE
feature: plantuml-java-integration-impl
status: Test
```

## Validations

- ✓ !include path resolution from discover/ to _static/
- ✓ Actor and UseCase color application
- ✓ Sphinx sphinxcontrib-plantuml integration
- ✓ Diagram compiles without PlantUML errors

## Diagram

```puml
@startuml test-uc-diagram
!include ../../../_static/plantuml-styles.puml

actor "Student" as student
actor "Instructor" as instructor
actor "Administrator" as admin

usecase "Submit Assignment" as submit
usecase "Grade Assignment" as grade
usecase "View Results" as results
usecase "Manage Courses" as manage

student --> submit
student --> results
instructor --> grade
instructor --> manage
admin --> manage

@enduml
```

## Success Criteria

- [x] File created in discover/test-uc-diagram.md
- [x] PlantUML block contains !include with correct path: `!include ../../../_static/plantuml-styles.puml`
- [x] Diagram contains 3-5 actors (4 total: student, instructor, admin) and 4 use cases
- [x] Markdown is well-formed (Sphinx parseable)
- [x] Diagram syntax is valid PlantUML
