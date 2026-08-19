# AGENTS.md

## Kadam

Kadam is a citizen-facing workflow assistant for **certificate chaining after major life events** such as death, birth, and marriage.

The core problem is cross-department fragmentation: a citizen may discover only after starting an application that it requires certificates or documents from other departments.

Example:

```text
Death Certificate → Legal Heir Certificate → Property Mutation → Succession Certificate
```

Each step may have a different department, office, form, document set, and validation process.

The key failure Kadam must prevent is:

```text
Citizen applies → application rejected → missing prerequisite discovered too late
```

Kadam should instead help citizens discover the complete chain **before they get stuck**.

The product should:

* Identify the citizen's goal/life event.
* Determine the required certificate chain.
* Show prerequisites and required documents.
* Explain why each step is needed.
* Identify the responsible department/office.
* Track progress across the chain.
* Detect missing prerequisites before submission.
* Explain rejection reasons in plain language.
* Clearly show the next actionable step.

The problem is high-severity and affects inheritance, pensions, school admission, property transfer, and other essential services. It is inherently cross-department, so no single government department owns the complete workflow.

---

## Stack

* **Backend:** FastAPI
* **Frontend:** React + Vite + Tailwind CSS
* **Database:** SQLite
* **Backend tests:** under `backend/tests/`

Do not introduce alternative frameworks or databases without an explicit requirement.

---

## Repository Structure

```text
.
├── AGENTS.md
├── README.md
├── backend
│   ├── ai
│   ├── app
│   ├── database
│   ├── mock_services
│   ├── tests
│   └── workflow
├── data
├── docs
│   ├── architecture.md
│   ├── repo-structure.md
│   ├── submission-writeup.md
│   └── tasks.md
├── frontend
│   └── src
│       ├── components
│       ├── lib
│       └── pages
└── scripts
```

### Directory Responsibilities

* `backend/app/` — FastAPI routes, API schemas, application services.
* `backend/ai/` — AI integrations and AI-specific logic.
* `backend/database/` — SQLite models, repositories, queries, persistence.
* `backend/workflow/` — certificate chains, prerequisites, workflow state, orchestration, validation.
* `backend/mock_services/` — synthetic government-service implementations only.
* `backend/tests/` — backend tests.
* `frontend/src/components/` — reusable React components.
* `frontend/src/lib/` — API clients and shared frontend utilities.
* `frontend/src/pages/` — page-level views.
* `data/` — project data only; never build output.
* `docs/` — architecture, repository, tasks, and submission documentation.
* `scripts/` — repeatable development/maintenance scripts.

Keep related code in its intended area. Do not create new top-level directories without a reason.

---

## Non-Negotiable Rules

### 1. Inspect Before Changing

**Always inspect existing code before modifying anything.**

Before implementing a change:

* Read the relevant files.
* Check existing abstractions/utilities.
* Check related tests.
* Check imports/usages.
* Check relevant documentation.

Prefer modifying existing functionality over duplicating it.

Keep changes focused. Do not perform unrelated refactors.

### 2. No Unnecessary Dependencies

**Do not add dependencies unless explicitly asked or genuinely required.**

Before adding one, check whether the existing stack or standard library can solve the problem.

Never introduce a new framework for convenience.

### 3. Test New Logic

**Write tests for new non-trivial logic.**

At minimum cover:

* Normal behavior
* Validation failures
* Important edge cases
* Regression scenarios

For Kadam, prioritize tests for certificate dependencies, cross-department workflows, missing prerequisites, rejection handling, and next-step resolution.

### 4. Never Call Real Government APIs

**Never call real government APIs.**

Everything under:

```text
backend/mock_services/
```

must remain **synthetic**.

Use mock/fake services for all government integrations.

Never commit:

* Government API credentials
* API keys/tokens
* Production government endpoints
* Real citizen records
* Real certificates or identifiers

Mock services should simulate realistic validation, document requirements, application states, dependencies, and rejection scenarios.

### 5. Keep Citizen Data Synthetic

Use fictional data in code, tests, fixtures, demos, and mock services.

Never commit real Aadhaar, PAN, phone numbers, addresses, certificates, property records, or other personally identifiable citizen information.

---

## Architecture Rules

Keep API, workflow, persistence, and external-service simulation concerns separated.

### Backend

FastAPI routes should remain thin.

Business rules belong in services/workflow modules, not directly inside route handlers.

Certificate-chain logic should be independently testable without HTTP.

### Workflow

`backend/workflow/` is the source of truth for certificate-chain orchestration.

Represent dependencies explicitly.

For example:

```text
Life Event
    ↓
Death Certificate
    ↓
Legal Heir Certificate
    ↓
Property Mutation
    ↓
Succession Certificate
```

A workflow should be able to represent:

* Required steps
* Prerequisite certificates
* Required documents
* Responsible department/office
* Application status
* Rejection reasons
* Next available action

Never hide a prerequisite that the citizen needs to know about.

### Mock Services

Mock departments should behave like independent external systems.

They may have their own:

* Request/response schemas
* Validation rules
* Required documents
* Application statuses
* Rejection conditions
* Synthetic data

Cross-department coordination belongs in the workflow/application layer.

---

## Frontend Rules

Use React + Vite + Tailwind.

Prefer reusable components and a clear API layer.

Do not scatter raw HTTP calls throughout components.

Citizen-facing UI should use clear, plain language.

Do not expose internal implementation details, database IDs, or mock-service terminology unless necessary.

The UI should make these immediately understandable:

1. Where the citizen is in the chain.
2. What is required now.
3. What prerequisites are missing.
4. Why the prerequisite is needed.
5. What happens next.

---

## Coding Style

Follow the formatter/linter configured for the component.

If none exists:

* JavaScript/TypeScript: **2 spaces**
* Python: **4 spaces**

Naming:

* Python files/functions/variables: `snake_case`
* JS/TS functions/variables: `camelCase`
* React components: `PascalCase`
* Web assets/directories: prefer `kebab-case`

Prefer descriptive names and small, focused modules.

Avoid premature abstraction.

---

## Testing

Backend tests belong in:

```text
backend/tests/
```

Use descriptive names such as:

```text
test_certificate_chain.py
test_workflow.py
test_legal_heir_certificate.py
```

Always test workflow changes involving:

* Missing prerequisites
* Invalid documents
* Rejected applications
* Cross-department dependencies
* Invalid workflow transitions
* Correct next-step resolution

Run the relevant component tests after changes.

Do not invent project-wide commands before the required tooling/configuration exists.

Once tooling exists, document canonical commands in `README.md`.

---

## Documentation

Update documentation when implementation changes its subject.

* `README.md` — setup, commands, developer workflow.
* `docs/architecture.md` — architecture and major boundaries.
* `docs/repo-structure.md` — repository organization.
* `docs/tasks.md` — implementation tasks/milestones.
* `docs/submission-writeup.md` — demo/submission story.

Document the **current implementation**, not an imagined future architecture.

---

## Git

Use short, imperative, lowercase commit messages.

Examples:

```text
add certificate chain workflow
fix prerequisite validation
add mock legal heir service
update workflow docs
```

Do not commit:

* `.env` files
* Secrets
* Virtual environments
* Dependency directories
* Build artifacts
* Unintended local databases
* Real citizen data

Keep commits focused and avoid mixing unrelated changes.

---

## Pull Requests

Include:

1. What changed
2. Why it changed
3. User-visible/architectural impact
4. Tests run
5. Relevant task/issue
6. Configuration or migration steps, if any
7. Screenshots for frontend changes

For certificate-workflow changes, mention affected chains, prerequisites, mock services, and rejection scenarios.

---

## Priority

When making trade-offs, prioritize:

1. **Correct citizen workflow**
2. **Explicit certificate dependencies**
3. **Preventing unknown prerequisites**
4. **Testability**
5. **Simple architecture**
6. **Clear citizen UX**
7. **Extensibility**

Do not add complexity just to demonstrate technology.

**Kadam's core job is to prevent the citizen from reaching "I didn't know I needed this certificate."**
