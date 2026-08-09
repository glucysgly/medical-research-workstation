# Shared routing contract

Route a request in this order:

1. Resolve the project and read `project.yaml`/`status.yaml`.
2. Classify the task code and domain.
3. Select one most-specific primary Skill and only necessary supporting tools.
4. Check privacy, input, runtime and human-gate preconditions.
5. Execute a deterministic runner or produce a plan when inputs are absent.
6. Record outputs, warnings, evidence and provenance.
7. Verify the artifact before claiming completion.

Routing success means that a workflow was selected. It does not mean that a
scientific analysis ran or that its conclusion is valid.
