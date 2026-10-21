# Git Branching Strategy & Contribution Policy
### Credit Card Service Portal (CCSP) — DevOps Engineering Guidelines

---

## 1. Branch Topology & Hierarchy
The repository follows the Git Flow branching model tailored for automated CI/CD continuous delivery:

```text
  main (Protected: Tagged Production Releases v1.0.0, v1.1.0)
   ▲
   │ [Pull Request: Peer Review + 100% CI Pipeline Pass]
   │
  dev (Integration & Continuous Delivery Baseline)
   ▲
   ├── feature/card-application-flow   (Feature 1: Onboarding Form)
   ├── feature/card-search-lifecycle   (Feature 2: Directory & State Engine)
   └── bugfix/validation-error-display (Defect Resolution)
```

### Branch Responsibilities
1. **`main` Branch:**
   * Contains strictly production-ready, stable releases.
   * Direct commits to `main` are strictly prohibited.
   * Every release to `main` must be tagged with semantic versioning (e.g. `v1.0.0`).
2. **`dev` Branch:**
   * Serves as the integration branch for ongoing sprint development.
   * Jenkins CI jobs trigger automatically on every push or merge into `dev`.
   * All feature branches branch off `dev` and merge back into `dev` via Pull Requests.
3. **`feature/*` Branches:**
   * Dedicated to individual backlog user stories or tasks.
   * Naming convention: `feature/<descriptive-kebab-case-name>`
   * Examples: `feature/card-application`, `feature/directory-search`, `feature/metrics-dashboard`.
4. **`bugfix/*` Branches:**
   * Created to remediate defects identified during Selenium regression testing or staging.
   * Naming convention: `bugfix/<issue-id>-<defect-summary>`
   * Example: `bugfix/issue-12-income-validation`.

---

## 2. Commit Message Standards (Conventional Commits)
All commit messages must follow the **Conventional Commits v1.0.0** specification:

```text
<type>(<scope>): <short imperative description>

[optional body explaining rationale]

[optional footer referencing issue ID: Closes #12]
```

### Approved Commit Types:
* `feat`: A new user-facing functional feature (e.g., `feat(apply): add client-side limit validation`)
* `fix`: A defect resolution or bug fix (e.g., `fix(service): prevent negative annual income submission`)
* `docs`: Documentation updates only (e.g., `docs(readme): add quickstart and architecture details`)
* `test`: Adding or refactoring test suites (e.g., `test(selenium): implement journey 1 application flow`)
* `ci`: Continuous Integration pipeline changes (e.g., `ci(jenkins): configure Maven test quality gate`)
* `chore`: Build tooling, dependency, or configuration updates (e.g., `chore(pom): upgrade Spring Boot to 3.2.5`)
* `refactor`: Code changes that neither fix a bug nor add a feature

---

## 3. Pull Request (PR) & Quality Gate Checklist
Before merging any feature branch into `dev`, the following automated and peer review checks must pass:
- [ ] Code compiles without warnings (`mvn clean compile`).
- [ ] 100% pass on all JUnit 5 unit tests (`mvn test`).
- [ ] 100% pass on all headless Selenium WebDriver user journeys.
- [ ] Zero merge conflicts with the target integration branch.
- [ ] Code adheres to 4-tier architectural separation of concerns.
- [ ] Peer review approved by at least one reviewer.
