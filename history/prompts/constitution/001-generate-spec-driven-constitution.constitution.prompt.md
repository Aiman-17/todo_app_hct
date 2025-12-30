---
id: 001
title: Generate Spec-Driven Constitution
stage: constitution
date: 2025-12-29
surface: agent
model: claude-sonnet-4-5
feature: none
branch: 001-docusaurus-docs
user: ACS
command: /sp.constitution
labels: ["constitution", "governance", "agents", "principles"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A (constitution document)
---

## Prompt

Generate a **Spec-Driven Constitution** for my Hackathon II Todo project as a Markdown file (CLAUDE.md).

Requirements:

1. Purpose: Define the high-level mission and goals of the project.
2. Principles:
   - Spec-first development: every feature must have a corresponding spec.
   - Agent-centric workflow: all tasks executed through agents.
   - Skill reusability: repeated operations implemented as modular, versioned skills.
   - Phase-based evolution: console → web → AI chatbot → local K8s → cloud deployment.
   - Quality & compliance: TestAgent and SpecAgent enforce correctness.
   - Event-driven architecture: all async operations via Kafka and Dapr.
   - Security: JWT authentication and user isolation enforced by AuthenticationAgent.

3. Agent Governance:
   - Define each agent's role and scope: TodoMasterAgent, TaskCRUDAgent, AuthenticationAgent, ChatbotAgent, DockerAgent, KubernetesAgent, DeploymentAgent, CI_CDAgent, KafkaAgent, DaprAgent, SpecAgent, TestAgent.
   - Specify rules: agents act only within their scope unless delegated by TodoMasterAgent.
   - Orchestration rules: TodoMasterAgent coordinates multi-agent workflows.

4. Workflow Governance:
   - Standard pipeline: Spec → Skill → Agent Execution → Test → Deployment.
   - Versioning and logging requirements.
   - Reporting rules: all agents report status to TodoMasterAgent.

5. Deployment Governance:
   - Minikube must be validated before cloud rollout.
   - CI/CD pipelines managed by CI_CDAgent.
   - Dapr and Kafka configuration must follow specs.
   - DeploymentAgent cannot override configs without TodoMasterAgent approval.

6. Compliance & Escalation:
   - Spec violations or test failures trigger automatic escalation.
   - TodoMasterAgent coordinates corrections.

Additional instructions:
- Write in second person ("You are…", "You will…"), as instructions for agents.
- Make it concise, structured, and actionable.
- Do **not** include feature implementation details — focus on governance and rules.
- Use clear Markdown headings for all sections.
- Output as plain Markdown, ready to save as `CLAUDE.md`.

## Response snapshot

Created comprehensive Spec-Driven Constitution v1.0.0 for Hackathon II Todo project at `.specify/memory/constitution.md`.

**Structure**:
- Mission statement defining the 5-phase evolution
- 7 Core Principles (all non-negotiable):
  1. Spec-First Development
  2. Agent-Centric Workflow
  3. Skill Reusability
  4. Phase-Based Evolution
  5. Quality & Compliance
  6. Event-Driven Architecture
  7. Security

- Agent Governance section defining 12 specialized agents with clear scopes, authority, and restrictions
- Workflow Governance defining standard pipeline and versioning requirements
- Deployment Governance with validation gates and rollback procedures
- Compliance & Escalation framework with automatic triggers and resolution process

**Key Features**:
- All principles written in imperative "You MUST/MUST NOT" format for clarity
- Each agent has defined scope, authority, and restrictions
- Clear escalation triggers and resolution processes
- Versioning requirements for specs, skills, APIs, events, and deployments
- Phase-based delivery with mandatory gates between phases

## Outcome

- ✅ Impact: Established governance framework for entire Hackathon II Todo project; provides operational boundaries for all 12 agents
- 🧪 Tests: N/A (governance document)
- 📁 Files: Created .specify/memory/constitution.md (308 lines)
- 🔁 Next prompts:
  - Create feature spec for Phase 1 (Console App) using `/sp.specify`
  - Define first skill for task CRUD operations
  - Configure agent-specific behavior based on constitution roles
- 🧠 Reflection: Constitution successfully bridges high-level governance with actionable agent rules. Second-person imperative format ensures agents understand boundaries. Phase-based evolution provides clear roadmap.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Constitution template validation PASS, All placeholders resolved PASS
- Prompt variant (if applicable): N/A (initial version)
- Next experiment (smallest change to try): Monitor agent adherence to scope restrictions during first feature implementation
