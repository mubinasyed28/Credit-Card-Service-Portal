# Credit Card Service Portal (CCSP)
### Enterprise Selenium Test Automation & Continuous Delivery Pipeline

---

## Academic & Institutional Identification
* **Student Name:** Mubina
* **Roll Number:** 23102A0039
* **Program & Branch:** B.E. Semester VII – Computer Engineering
* **Subject:** DevOps Lab
* **Subject In-charge / Evaluator:** Dr. Snehal Andhare
* **Assigned Project Title:** Selenium Testing Framework for a Credit Card Service Portal
* **Academic Year:** 2026–2027

---

## 1. Project Overview & Architecture
The **Credit Card Service Portal (CCSP)** is an enterprise-grade, lightweight web application designed for retail banking credit card lifecycle management. It provides prospective customers with digital onboarding capabilities, offers operations teams a searchable master directory, and provides credit risk analysts with role-based lifecycle governance tools.

### Core Technology Stack:
* **Backend:** Java 17 LTS (Eclipse Adoptium) with Spring Boot 3.2.5
* **Build Tool:** Apache Maven 3.9.6
* **Database:** Embedded In-Memory H2 Database (`jdbc:h2:mem:ccsp_db`)
* **Presentation Tier:** Spring Boot Thymeleaf + Bootstrap 5 (Responsive UI)
* **Test Automation Quality Gate:** Selenium WebDriver 4.x + JUnit 5 + WebDriverManager
* **System Telemetry:** Spring Boot Actuator (`/actuator/health`)
* **Containerization:** Multi-Stage Dockerfile (Eclipse Temurin JRE minimal runtime)
* **Configuration Management:** Ansible Core (Idempotent playbooks)

---

## 2. Core Functional MVP Modules (5 Key Functions)
1. **Digital Credit Card Onboarding (`/apply`):** Customer details (Name, Email, Card Tier [Platinum, Gold, Titanium], Annual Income, Requested Credit Limit) with strict validation gates.
2. **Searchable Master Directory (`/cards`):** Real-time search by customer name or card number and status dropdown filtering.
3. **Role-Based Status Lifecycle Engine:** Finite state machine governing legal transitions: `PENDING` $\rightarrow$ `ACTIVE` $\rightarrow$ `BLOCKED` / `REJECTED`.
4. **Summary Metrics Dashboard (`/`):** Real-time KPI counter cards for Total Cards, Active Cards, Pending Review, and Frozen Cards.
5. **Actuator Health Telemetry (`/actuator/health`):** Real-time JSON health status (`UP`) for automated CI/CD quality gate verification.

---

## 3. Directory Structure
```text
DevOps_AI_Starter_Kit/
├── .github/
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md          # Bug report template
│       └── feature_request.md     # Feature request template
├── app/                           # Spring Boot Application Root
│   ├── pom.xml                    # Maven build configuration
│   └── src/
│       ├── main/java/com/creditcard/app/
│       │   ├── controller/        # Spring MVC Web Controllers
│       │   ├── dto/               # Form Validation DTOs
│       │   ├── model/             # JPA Entities & Enums
│       │   ├── repository/        # Spring Data JPA Repositories
│       │   ├── service/           # Business Logic & State Engine
│       │   └── CreditCardAppApplication.java
│       ├── main/resources/
│       │   ├── application.properties
│       │   └── templates/         # Thymeleaf HTML5 Views
│       └── test/java/com/creditcard/app/
├── docs/                          # Canonical Lab Task Reports
│   └── prev/                      # Archived Previous Report Versions
├── scripts/                       # Document & Diagram Automation Scripts
├── screenshots/                   # Verification Evidence & Visual Schematics
├── templates/                     # Official Department Word Templates
├── .gitignore                     # Git ignore rules
├── BRANCHING_POLICY.md            # Git Flow branching rules & conventions
└── README.md                      # Project master documentation
```

---

## 4. Local Development & Quick Start Guide

### Prerequisites
* Java 17 LTS (`java -version`)
* Apache Maven 3.9+ (`mvn -v`)
* Modern Web Browser (Google Chrome / Microsoft Edge)

### Execution Commands
```powershell
# 1. Navigate to application folder
cd app

# 2. Compile source code
mvn clean compile

# 3. Execute automated unit test suite
mvn test

# 4. Run application locally on port 8080
mvn spring-boot:run

# 5. Access application endpoints in browser:
#    - Dashboard:      http://localhost:8080/
#    - Card Directory: http://localhost:8080/cards
#    - Onboarding:     http://localhost:8080/apply
#    - Health Probe:   http://localhost:8080/actuator/health
```

---

## 5. Git Branching & Contribution Workflow
* **Protected Production Branch:** `main` (only tagged release versions e.g., `v1.0.0`)
* **Integration Branch:** `dev` (day-to-day feature integration)
* **Feature Branches:** `feature/<feature-name>` (e.g., `feature/card-onboarding`)
* **Bugfix Branches:** `bugfix/<ticket-id>-<description>`
* **Commit Standard:** Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `ci:`, `chore:`)
