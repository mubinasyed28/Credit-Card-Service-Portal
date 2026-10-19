# DevOps Project Master Rules & Operational Blueprint

This document defines the absolute, uncompromised standards, constraints, academic identity, document layouts, and DevOps technical requirements for all 15 tasks of this laboratory project. Every operation, code modification, document generation, and test execution must strictly adhere to these rules.

---

## 1. Academic & Student Identity
All generated documents, git commits, configuration files, reports, and code comments must consistently reflect the following exact identity:

* **Student Name:** Mubina
* **Roll Number:** 23102A0039
* **Program & Branch:** B.E. Semester VII – Computer Engineering
* **Subject:** DevOps Lab
* **Subject In-charge / Evaluator:** Dr. Snehal Andhare
* **Assigned Project Title:** Selenium Testing Framework for a Credit Card Service Portal
* **Document Filename Pattern:** `DevOps_Task{N}_Mubina_23102A0039.docx` (where `{N}` is 1 to 15)

---

## 2. Document Template & Formatting Enforcement
Every task document must be generated programmatically from the approved department template to ensure 100% structural fidelity and visual consistency:

1. **Base Templates:**
   * **Task 1:** `templates/template_task1.docx` (4-row Table 2 format).
   * **Tasks 2 to 15:** `templates/template_standard.docx` (5-row Table 2 format with Apparatus row).
2. **Table Envelope Integrity:**
   * **Table 0:** Semester, Subject, Subject In-charge (`Dr. Snehal Andhare`).
   * **Table 1:** Student Name (`Mubina`), Roll Number (`23102A0039`), Teacher's Signature.
   * **Table 2:**
     * `Row 0`: Task Number.
     * `Row 1`: Task Title (Exact title from the official 15-task allocation sheet).
     * `Row 2` (Tasks 2-15): Resources / Apparatus Required (Hardware & Software).
     * `Row 3` (Task 1: Row 2): Program & Output (Core content, bold section titles, tables, code snippets, centered figures).
     * `Row 4` (Task 1: Row 3): Conclusion (Formal academic summary of objectives achieved and verified).
3. **Typography & Styling:**
   * Default Font Family: **Calibri**.
   * Body Paragraphs: 11pt–12pt regular, 1.15 line spacing, 3pt space-after.
   * Section Headings: 12pt Bold Calibri.
   * Tables in Content: Headers shaded `#EAECEE`, cell borders `#CCCCCC`, font size 9.5pt–10pt.
   * Margins: Top: `0.53"`, Bottom: `0.50"`, Left: `0.75"`, Right: `0.75"`.
4. **Reproducibility & Document Archival Policy:**
   * Every document must be generated via a Python script in `scripts/generate_task{N}.py` so it can be re-run and updated deterministically.
   * **Archival of Previous Versions:** The root `docs/` folder must ONLY ever contain the single, latest, canonical task file (`DevOps_Task{N}_Mubina_23102A0039.docx`). Whenever an updated version of a task document is generated, any previous version must automatically be archived into `docs/prev/` (e.g., `docs/prev/DevOps_Task{N}_Mubina_23102A0039_prev_<timestamp>.docx`) so there is zero confusion. Never leave temporary `_v2`, `_v3` files loose in `docs/`.

---

## 3. Application Domain: Credit Card Service Portal (CCSP)
The application is a lightweight, responsive web application designed for enterprise credit card lifecycle management, customer service requests, and automated validation:

* **Tech Stack:**
  * **Backend:** Java 17/21+ with Spring Boot 3.x.
  * **Build & Dependency Tool:** Apache Maven (`pom.xml`) with Maven Wrapper (`mvnw`).
  * **Database:** Embedded H2 Database (zero external database setup required, fast in-memory execution, reliable CI test runs).
  * **Frontend / UI:** Spring Boot Thymeleaf + Bootstrap 5 (clean responsive web layout with distinct IDs/classes for reliable Selenium locator targeting).
  * **Health Check & Monitoring:** Spring Boot Actuator (`/actuator/health`) for automated CI/CD and Ansible reliability checks.
* **Core MVP Scope (Strictly 5 Functions):**
  1. *Credit Card Application & Limit Request Management:* Customer Name, Email, Card Type (Platinum, Gold, Titanium), Requested Credit Limit, Annual Income, Employment Status with validation gates.
  2. *Card Directory & Live Search:* Responsive table with search by customer name / card number and status filter (`PENDING`, `ACTIVE`, `BLOCKED`, `REJECTED`).
  3. *Role-Based Status Lifecycle:* Transitions enforcing: `PENDING` $\rightarrow$ `ACTIVE` $\rightarrow$ `BLOCKED` / `CLOSED` (Administrative approvals, card activations, and security freeze).
  4. *Summary Metrics Dashboard:* Summary KPI cards (Total Cards, Active Cards, Pending Applications, Blocked Cards).
  5. *Actuator Health Endpoint:* Real-time JSON health status (`UP`).

---

## 4. Git & GitHub Branching Policy
* **Branch Structure:**
  * `main`: Protected production-ready branch. Only tagged releases (`v1.0.0`).
  * `dev`: Integration branch for day-to-day development.
  * `feature/*`: Specific feature branches (e.g., `feature/coupon-create`, `feature/coupon-search-dashboard`).
* **Commit Conventions:** Follow Conventional Commits format (`feat: ...`, `fix: ...`, `docs: ...`, `test: ...`, `ci: ...`).
* **Collaboration Demo (Tasks 5 & 6):**
  * Raise clean Pull Requests from feature branches into `dev`.
  * Create an intentional Git merge conflict on a shared file, inspect conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`), resolve manually, commit resolution, and tag `v1.0.0`.

---

## 5. Automated Testing & Quality Gate (Selenium WebDriver)
* **Framework:** Java + Selenium WebDriver 4.x + JUnit 5 / TestNG + WebDriverManager.
* **Execution Mode:** Headless Chrome / Edge execution for automated CI runs, with local headful support for demonstration.
* **4 Critical User Journeys to Cover:**
  1. Customer / Admin navigates to `/apply`, fills application form, asserts card record is created and appears in `/cards`.
  2. Validation gate: Submitting negative income or invalid credit limit triggers inline error message.
  3. Search & filter: User enters search term into search box and asserts table filters correctly.
  4. Status action: Officer clicks "Approve" or "Block" and verifies status tag changes to `ACTIVE` or `BLOCKED`.
* **Screenshot Failure Mechanism:** Implement an `@AfterEach` or `TestWatcher` hook that automatically saves a timestamped PNG into `screenshots/failures/` on any assertion failure.
* **Jenkins Quality Gate (Task 10):**
  * The pipeline must execute `mvn test`.
  * If tests fail, Jenkins **must immediately stop execution** and abort all subsequent Docker and deployment stages.
  * An intentional defect experiment must be recorded: introduce a bug $\rightarrow$ show pipeline failure $\rightarrow$ fix bug $\rightarrow$ show pipeline success.

---

## 6. Docker Containerization & Deployment
* **Dockerfile Standard:** Multi-stage build (Stage 1: Maven build, Stage 2: Minimal Eclipse Temurin JRE runtime) to ensure lightweight, secure images.
* **Container Lifecycle Commands:** Must document `build`, `tag`, `run`, `ps`, `logs`, `stop`, `restart`, and `rm`.
* **Port Mapping:** Host port `8080` $\rightarrow$ Container port `8080`.
* **CD Pipeline:** Jenkinsfile automatically tags Docker image with build number (`credit-card-app:${BUILD_NUMBER}`) and updates the running container.

---

## 7. Configuration Management with Ansible
* **Files:** Clean inventory file (`hosts.ini`) and structured playbook (`playbook.yml`).
* **Prerequisites Managed:** System updates, Java runtime, Docker engine, required directories (`/opt/credit-card-app`), firewall ports (8080).
* **Idempotency Rule:** Running `ansible-playbook -i hosts.ini playbook.yml` a second time **must yield 0 changes** (`changed=0, failed=0`).
* **Rollback & Verification:** Must demonstrate automated curl health-check against `/actuator/health` and a rollback task restoring the prior stable container tag.

---

## 8. Evidence & Screenshot Quality Standards
* **No Clutter:** Screenshots must be strictly cropped to exclude Windows taskbars, unrelated desktop windows, or browser chrome unless illustrating full-screen flow.
* **Standard Resolution:** Centered in Word documents, scaled to a maximum width of `6.0` to `6.2` inches so it never causes page overflow.
* **Captions:** Every inserted figure must have a centered, bold caption: `Figure {TaskNo}.{FigNo}: {Description}`.
* **Raw & Processed Separation:**
  * Raw screenshots: `screenshots/task{N}/raw/`
  * Cleaned/cropped: `screenshots/task{N}/`

---

## 9. Quality & Zero-Regression Checklist (Before Finalizing Any Task)
- [ ] Student name and roll number verified (`Mubina` / `23102A0039`).
- [ ] Task title matches the official syllabus allocation exactly.
- [ ] Document generated and opens without XML corruption.
- [ ] Code snippets and configuration syntax validated.
- [ ] All tables contain complete, realistic domain data (no dummy placeholders like `TODO` or `Lorem Ipsum`).
- [ ] Conclusion reflects genuine academic analysis.
