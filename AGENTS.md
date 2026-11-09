# Project instructions

[AWS-KI-Workshop.md](AWS-KI-Workshop.md) is the authoritative project plan for
scope, decisions, learning goals and operating limits. Read the relevant sections
before starting work; the plan alone is not authorization to execute its steps.

- AI-generated code and independently executed local routine checks are welcome.
  Work in small functional increments and explain relevant changes and results.
  Coaching focuses on new connections, especially AI concepts; manual coding and
  repetition of familiar programming or DevOps basics are not required.
- Manage AWS infrastructure exclusively through IaC: the global budget via
  Terraform in `infra/budget/`, all other infrastructure via CDK in Stockholm.
  Never manage the same resource with both tools. Before any cloud change,
  including bootstrap or teardown, explain the concrete resources, permissions
  and expected costs and obtain approval for that scope. Do not ask again for
  already approved substeps; obtain further approval if the scope changes.
- Later, automatic demo deployments may run within explicitly approved limits.
  This does not authorize automatic infrastructure changes or publication now.
- Do not commit, push or publish without an explicit assignment.
- Distinguish local checks from checks that access cloud services. Run applicable
  local routine checks independently within the current assignment. Identify
  cloud access and possible side effects or costs before running cloud checks;
  a check that changes cloud resources follows the approval rule above.
- Follow the additional CDK instructions in `infra/AGENTS.md` for work there.
