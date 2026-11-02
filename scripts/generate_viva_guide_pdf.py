import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
import fitz  # PyMuPDF

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, total_pages):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        
        # Draw header on pages 2+
        if self._pageNumber > 1:
            self.drawString(36, 756, "Credit Card Service Portal (CCSP)  -  Comprehensive DevOps & Viva Guide")
            self.drawRightString(576, 756, "Mubina | Roll No: 23102A0039")
            self.setStrokeColor(colors.HexColor("#D0D7DE"))
            self.setLineWidth(0.6)
            self.line(36, 750, 576, 750)
            
        # Draw footer on all pages
        self.setStrokeColor(colors.HexColor("#D0D7DE"))
        self.setLineWidth(0.6)
        self.line(36, 36, 576, 36)
        self.drawString(36, 24, "DevOps Lab (BE Sem VII) | Evaluator: Dr. Snehal Andhare | Dept of Computer Engineering")
        page_text = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(576, 24, page_text)
        self.restoreState()

def build_pdf():
    pdf_path = r"docs\CCSP_DevOps_Viva_Preparation_Guide_Mubina_23102A0039.pdf"
    os.makedirs("docs", exist_ok=True)
    
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=46
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=colors.HexColor('#1B365D'),
        alignment=1, # Center
        spaceAfter=3
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor('#0066CC'),
        alignment=1,
        spaceAfter=5
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#1B365D'),
        spaceBefore=5,
        spaceAfter=3
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor('#0E6655'),
        spaceBefore=4,
        spaceAfter=2
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=10.5,
        textColor=colors.HexColor('#222222'),
        spaceAfter=3
    )
    
    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    bullet_style = ParagraphStyle(
        'BulletText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.0,
        leading=10.2,
        textColor=colors.HexColor('#222222'),
        leftIndent=10,
        firstLineIndent=-7,
        spaceAfter=2
    )

    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.2,
        leading=9.0,
        textColor=colors.HexColor('#1E293B'),
        backColor=colors.HexColor('#F1F5F9'),
        borderPadding=3,
        spaceAfter=3
    )

    table_header = ParagraphStyle(
        'TableHead',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=9.5,
        textColor=colors.white,
        alignment=1
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.2,
        textColor=colors.HexColor('#222222')
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.2,
        textColor=colors.HexColor('#1B365D')
    )
    
    q_title = ParagraphStyle(
        'QTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.2,
        leading=10.2,
        textColor=colors.HexColor('#1B365D'),
        spaceBefore=3,
        spaceAfter=1
    )

    ans_style = ParagraphStyle(
        'AnsText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=9.8,
        textColor=colors.HexColor('#2C3E50'),
        leftIndent=8,
        spaceAfter=3
    )

    story = []

    # =========================================================================
    # PAGE 1: ACADEMIC PROFILE, EXECUTIVE SUMMARY, TECH STACK & 5 MVP MODULES
    # =========================================================================
    story.append(Paragraph("CREDIT CARD SERVICE PORTAL (CCSP)", title_style))
    story.append(Paragraph("Comprehensive DevOps Lab & Selenium Test Automation  -  Viva Preparation Guide", subtitle_style))
    
    # Identification Box Table
    id_data = [
        [
            Paragraph("<b>Student Name:</b> Mubina", table_cell),
            Paragraph("<b>Roll Number:</b> 23102A0039", table_cell),
            Paragraph("<b>Program:</b> B.E. Computer Engineering (Sem VII)", table_cell)
        ],
        [
            Paragraph("<b>Subject:</b> DevOps Lab", table_cell),
            Paragraph("<b>Evaluator:</b> Dr. Snehal Andhare", table_cell),
            Paragraph("<b>Assigned Project:</b> Selenium Testing Framework for CCSP", table_cell)
        ]
    ]
    id_table = Table(id_data, colWidths=[160, 160, 220])
    id_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F0F4F8')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1B365D')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(id_table)
    story.append(Spacer(1, 4))

    story.append(Paragraph("1. Executive Summary & Problem Definition (Task 1 Context)", h1_style))
    story.append(Paragraph(
        "The <b>Credit Card Service Portal (CCSP)</b> is an enterprise-grade retail banking web application engineered to solve critical operational bottlenecks in traditional financial onboarding. In conventional setups, credit card evaluation relies on manual underwriting, siloed verification documents, and disjointed lifecycle management, leading to high processing latency (3-5 business days), untracked status transitions, and severe deployment friction. CCSP introduces an end-to-end automated digital lifecycle powered by a robust <b>DevOps CI/CD pipeline</b> and <b>Selenium automated quality gates</b>.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Core Objective:</b> Guarantee zero-defect releases through continuous integration, automated UI regression testing, multi-stage Docker containerization, and idempotent Ansible configuration management with zero downtime.",
        body_style
    ))

    story.append(Paragraph("2. Full Technology Stack & Engineering Justification", h1_style))
    tech_data = [
        [Paragraph("Tier / Function", table_header), Paragraph("Technology Chosen", table_header), Paragraph("Version", table_header), Paragraph("Engineering Rationale for Viva Defense", table_header)],
        [Paragraph("Backend Framework", table_cell_bold), Paragraph("Java LTS + Spring Boot", table_cell), Paragraph("Java 17 / 3.2.5", table_cell), Paragraph("High performance, mature dependency injection, native Actuator observability.", table_cell)],
        [Paragraph("Database Engine", table_cell_bold), Paragraph("Embedded H2 Database", table_cell), Paragraph("In-Memory", table_cell), Paragraph("Zero external database setup, fast in-memory execution, isolated CI/CD test runs.", table_cell)],
        [Paragraph("Frontend Presentation", table_cell_bold), Paragraph("Thymeleaf + Bootstrap 5", table_cell), Paragraph("5.3.3", table_cell), Paragraph("Server-rendered responsive UI; deterministic HTML IDs for Selenium selectors.", table_cell)],
        [Paragraph("Automated Quality Gate", table_cell_bold), Paragraph("Selenium WebDriver + JUnit 5", table_cell), Paragraph("4.19 / 5.10", table_cell), Paragraph("Automates 4 critical user journeys; runs headless in CI with failure screenshot capture.", table_cell)],
        [Paragraph("Build Automation", table_cell_bold), Paragraph("Apache Maven", table_cell), Paragraph("3.9.6", table_cell), Paragraph("Standardized build lifecycle (compile, test, package); automated plugin management.", table_cell)],
        [Paragraph("Containerization", table_cell_bold), Paragraph("Docker Multi-Stage Build", table_cell), Paragraph("Engine 24+", table_cell), Paragraph("Build stage compiles JAR; minimal Eclipse Temurin JRE runtime image (<150 MB).", table_cell)],
        [Paragraph("Continuous Integration", table_cell_bold), Paragraph("Jenkins Declarative Pipeline", table_cell), Paragraph("LTS 2.440+", table_cell), Paragraph("Pipeline-as-Code (Jenkinsfile), automated quality gates, Docker tag and push.", table_cell)],
        [Paragraph("Configuration Mgmt", table_cell_bold), Paragraph("Ansible Core Playbooks", table_cell), Paragraph("2.15+", table_cell), Paragraph("Idempotent host provisioning (changed=0), health probes, automated rollback.", table_cell)],
        [Paragraph("Observability & Telemetry", table_cell_bold), Paragraph("Spring Boot Actuator", table_cell), Paragraph("3.2.5", table_cell), Paragraph("Real-time JSON health telemetry (/actuator/health) and visual UI (/health).", table_cell)]
    ]
    t_tech = Table(tech_data, colWidths=[95, 120, 65, 260])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1B365D')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#1B365D')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_tech)
    story.append(Spacer(1, 4))

    story.append(Paragraph("3. The 5 Core Functional MVP Modules (Scope Freeze)", h1_style))
    story.append(Paragraph("&bull; <b>1. Digital Onboarding Portal (<code>/apply</code>):</b> Interactive application capture (Name, Email, Annual Income, Card Tier, Requested Limit, Employment). Enforces strict bean validation gates (@Min income INR 1,00,000, email regex).", bullet_style))
    story.append(Paragraph("&bull; <b>2. Searchable Master Directory (<code>/cards</code>):</b> Live multi-criteria filtering across customer names and card numbers. Dynamic status filtering (PENDING, ACTIVE, BLOCKED, REJECTED) with real-time responsive UI rendering.", bullet_style))
    story.append(Paragraph("&bull; <b>3. Role-Based Lifecycle State Machine:</b> Strict legal state transitions: PENDING &rarr; ACTIVE (Approval) or REJECTED; ACTIVE &rarr; BLOCKED (Security Freeze) or restored. Illegal bypasses are rejected by backend business rules.", bullet_style))
    story.append(Paragraph("&bull; <b>4. Executive KPI Metrics Dashboard (<code>/</code>):</b> Real-time executive metrics summary cards calculating Total Accounts, Active Cards, Underwriting Queue, and Security Frozen accounts, alongside recent activity audit logs.", bullet_style))
    story.append(Paragraph("&bull; <b>5. Production Readiness Telemetry (<code>/health</code> & <code>/actuator/health</code>):</b> Microservice health probes exposing real-time database connectivity, JVM memory statistics, and process uptime for automated CI/CD gating.", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: ARCHITECTURE, DATA FLOW, BUSINESS RULES & DEVOPS LIFECYCLE
    # =========================================================================
    story.append(Paragraph("4. System Architecture & 4-Tier Monolithic Design (Task 3 Context)", h1_style))
    story.append(Paragraph(
        "CCSP is engineered with a strict <b>4-Tier Monolithic Modular Architecture</b> adhering to the Single Responsibility Principle and Separation of Concerns. This architecture ensures high cohesion, loose coupling, and testability:",
        body_style
    ))

    arch_data = [
        [Paragraph("Architectural Tier", table_header), Paragraph("Key Java / System Components", table_header), Paragraph("Responsibilities & Flow", table_header)],
        [Paragraph("Tier 1: Presentation Layer", table_cell_bold), Paragraph("Thymeleaf HTML5, Bootstrap 5, CSS3, DOM IDs", table_cell), Paragraph("Server-renders views (dashboard, cards, apply, health). Exposes deterministic IDs for Selenium locators.", table_cell)],
        [Paragraph("Tier 2: Controller / Web API", table_cell_bold), Paragraph("CreditCardController.java, CreditCardApiController.java", table_cell), Paragraph("Handles HTTP verbs (GET, POST, PUT), processes form submissions, performs model binding and content negotiation.", table_cell)],
        [Paragraph("Tier 3: Service / Business Logic", table_cell_bold), Paragraph("CreditCardService.java, CardType.java, CardStatus.java", table_cell), Paragraph("Enforces underwriting eligibility gates, 40% income cap, masked card generation, and state transitions.", table_cell)],
        [Paragraph("Tier 4: Persistence / Data Access", table_cell_bold), Paragraph("CreditCardRepository.java, Spring Data JPA, H2", table_cell), Paragraph("JPA Object-Relational Mapping, H2 in-memory transactions, seed data insertion on startup.", table_cell)]
    ]
    t_arch = Table(arch_data, colWidths=[110, 160, 270])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1B365D')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#1B365D')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 4))

    story.append(Paragraph("5. Core Business Rules & Underwriting Guardrails (Viva Highlight)", h1_style))
    story.append(Paragraph("&bull; <b>40% Income Multiplier Rule:</b> A customer's maximum allowable credit limit is strictly capped at <b>40% of their verifiable annual income</b> (e.g., Annual Income INR 10,00,000 &rarr; Maximum eligible limit = INR 4,00,000).", bullet_style))
    story.append(Paragraph("&bull; <b>Card Tier Ceiling Guardrails:</b> <b>Platinum:</b> Max INR 5,00,000 (Premium tier) | <b>Gold:</b> Max INR 2,50,000 (Mid tier) | <b>Titanium:</b> Max INR 1,00,000 (Entry tier). If calculated limit exceeds tier ceiling, it is capped at the tier maximum.", bullet_style))
    story.append(Paragraph("&bull; <b>Minimum Income Gate:</b> Income strictly validated via <code>@Min(100000)</code>. Submissions below INR 1,00,000 trigger inline validation errors.", bullet_style))
    story.append(Paragraph("&bull; <b>Card Number Masking & Audit Trail:</b> Automatically generates 16-digit card numbers formatted as <code>****-****-****-XXXX</code> preserving PCI-DSS privacy standards alongside ISO 8601 creation timestamps.", bullet_style))
    story.append(Paragraph("&bull; <b>Finite State Lifecycle Engine:</b> Transitions strictly enforced: <code>PENDING &rarr; ACTIVE</code>, <code>PENDING &rarr; REJECTED</code>, <code>ACTIVE &rarr; BLOCKED</code>, <code>BLOCKED &rarr; ACTIVE</code>. Prevents invalid illegal status corruptions.", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("6. End-to-End DevOps CI/CD Lifecycle & Automation Pipeline", h1_style))
    story.append(Paragraph(
        "The project implements a complete, closed-loop DevOps delivery lifecycle connecting developer commits to verified production deployments:",
        body_style
    ))

    devops_steps = [
        [Paragraph("DevOps Stage", table_header), Paragraph("Tool / Technology", table_header), Paragraph("Key Actions & Automated Validations Performed", table_header)],
        [Paragraph("1. Code & Branch", table_cell_bold), Paragraph("Git / GitHub", table_cell), Paragraph("Feature branches (feature/*), Conventional Commits, Pull Requests to dev, conflict resolution.", table_cell)],
        [Paragraph("2. Continuous Integration", table_cell_bold), Paragraph("Jenkins Declarative", table_cell), Paragraph("SCM checkout, Maven build (mvn clean compile), JAR archive packaging, surefire reports.", table_cell)],
        [Paragraph("3. Continuous Testing", table_cell_bold), Paragraph("Selenium + JUnit 5", table_cell), Paragraph("Headless Chrome execution of 4 user journeys; Quality Gate stops pipeline on failure.", table_cell)],
        [Paragraph("4. Containerization", table_cell_bold), Paragraph("Docker Multi-Stage", table_cell), Paragraph("Multi-stage Dockerfile: Maven builds JAR, Eclipse Temurin JRE runs it. Image tagged with build number.", table_cell)],
        [Paragraph("5. Continuous Delivery", table_cell_bold), Paragraph("Jenkins + Docker Registry", table_cell), Paragraph("Automated container replacement (ccsp-live), port binding 8080:8080, zero-downtime swap.", table_cell)],
        [Paragraph("6. Configuration Mgmt", table_cell_bold), Paragraph("Ansible Core", table_cell), Paragraph("Playbook installs prerequisites, verifies ports, enforces idempotency (changed=0 on 2nd run).", table_cell)],
        [Paragraph("7. Reliability & Rollback", table_cell_bold), Paragraph("Actuator + Ansible", table_cell), Paragraph("Probes /actuator/health for UP status. Automatic rollback restores prior stable container tag on error.", table_cell)]
    ]
    t_devops = Table(devops_steps, colWidths=[105, 115, 320])
    t_devops.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1B365D')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#1B365D')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_devops)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: HOW TO RUN PROJECT, ENDPOINTS & SELENIUM AUTOMATION DEEP DIVE
    # =========================================================================
    story.append(Paragraph("7. How to Run the Project (Step-by-Step Viva Execution Guide)", h1_style))
    story.append(Paragraph("Follow these exact commands to execute the project during the practical viva demonstration:", body_style))

    story.append(Paragraph("<b>Option A: Run Locally via Maven Wrapper / Installed JDK</b>", h2_style))
    story.append(Paragraph(
        "<code>$env:JAVA_HOME = \"C:\\Users\\YOCKET-271\\tools\\jdk-17.0.12+7\"<br/>"
        "$env:PATH = \"$env:JAVA_HOME\\bin;C:\\Users\\YOCKET-271\\tools\\apache-maven-3.9.6\\bin;$env:PATH\"<br/>"
        "cd app<br/>"
        "mvn spring-boot:run</code>",
        code_style
    ))

    story.append(Paragraph("<b>Option B: Run Automated Unit & Selenium Quality Gate Tests (14 Tests)</b>", h2_style))
    story.append(Paragraph(
        "<code>cd app<br/>"
        "mvn test</code> &nbsp;&nbsp;<i># Executes 10 unit tests + 4 Selenium browser journeys headless in ~20s</i>",
        code_style
    ))

    story.append(Paragraph("<b>Option C: Build & Run via Docker Multi-Stage Container</b>", h2_style))
    story.append(Paragraph(
        "<code>docker build -t mubina23102a0039/credit-card-app:1.0.0 .<br/>"
        "docker run -d --name ccsp-live -p 8080:8080 mubina23102a0039/credit-card-app:1.0.0<br/>"
        "docker ps &amp;&amp; docker logs --tail 20 ccsp-live</code>",
        code_style
    ))

    story.append(Paragraph("<b>Option D: Execute Idempotent Ansible Provisioning & Rollback</b>", h2_style))
    story.append(Paragraph(
        "<code>ansible-playbook -i ansible/hosts.ini ansible/playbook.yml &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Full deployment<br/>"
        "ansible-playbook -i ansible/hosts.ini ansible/playbook.yml &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# 2nd run: changed=0 (Idempotency)<br/>"
        "ansible-playbook -i ansible/hosts.ini ansible/playbook_task14.yml --tags rollback # Disaster Recovery</code>",
        code_style
    ))

    story.append(Paragraph("8. Verified Project Endpoints Matrix", h1_style))
    endpoint_data = [
        [Paragraph("Endpoint URL", table_header), Paragraph("HTTP Verb", table_header), Paragraph("Response Content", table_header), Paragraph("Verification Purpose", table_header)],
        [Paragraph("http://localhost:8080/", table_cell_bold), Paragraph("GET", table_cell), Paragraph("HTML5 (Thymeleaf)", table_cell), Paragraph("Executive KPI Dashboard & summary counters.", table_cell)],
        [Paragraph("http://localhost:8080/cards", table_cell_bold), Paragraph("GET", table_cell), Paragraph("HTML5 (Thymeleaf)", table_cell), Paragraph("Master Directory, real-time search & status dropdown filter.", table_cell)],
        [Paragraph("http://localhost:8080/apply", table_cell_bold), Paragraph("GET / POST", table_cell), Paragraph("HTML5 (Form)", table_cell), Paragraph("Digital Onboarding form with bean validation feedback.", table_cell)],
        [Paragraph("http://localhost:8080/health", table_cell_bold), Paragraph("GET", table_cell), Paragraph("HTML / JSON", table_cell), Paragraph("Visual Health Dashboard & REST endpoint for browser/curl.", table_cell)],
        [Paragraph("http://localhost:8080/actuator/health", table_cell_bold), Paragraph("GET", table_cell), Paragraph("JSON (Actuator)", table_cell), Paragraph("Telemetry probe verifying DB, disk, and status: UP.", table_cell)],
        [Paragraph("http://localhost:8080/api/cards", table_cell_bold), Paragraph("GET / POST", table_cell), Paragraph("REST JSON", table_cell), Paragraph("Programmatic REST API for credit card records.", table_cell)],
        [Paragraph("http://localhost:8080/h2-console", table_cell_bold), Paragraph("GET", table_cell), Paragraph("HTML Console", table_cell), Paragraph("H2 In-Memory DB management (jdbc:h2:mem:ccsp_db).", table_cell)]
    ]
    t_ep = Table(endpoint_data, colWidths=[140, 55, 95, 250])
    t_ep.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1B365D')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#1B365D')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_ep)
    story.append(Spacer(1, 4))

    story.append(Paragraph("9. Selenium Automated Quality Gate Deep Dive (Tasks 9 & 10)", h1_style))
    story.append(Paragraph(
        "Selenium WebDriver 4.x is integrated with JUnit 5 to serve as an <b>uncompromising Quality Gate</b> in the Jenkins pipeline. Configured via <code>WebDriverManager.chromedriver().setup()</code> and runs headless in CI environments.",
        body_style
    ))
    story.append(Paragraph("<b>The 4 Critical Automated User Journeys:</b>", body_bold))
    story.append(Paragraph("&bull; <b>Journey 1 (Digital Application & Directory Sync):</b> Navigates to <code>/apply</code>, fills valid customer data ('Aarav Sharma', INR 12L income, Platinum tier), submits form, asserts redirect to <code>/cards</code>, asserts success alert message, and verifies card record appears in the master table with initial status 'Pending'.", bullet_style))
    story.append(Paragraph("&bull; <b>Journey 2 (Validation Gate Enactment):</b> Submits form with sub-minimum income (< INR 1,00,000) and asserts submission is halted on <code>/apply</code>, inline error message appears (<code>err-annualIncome</code>), and no database record is created.", bullet_style))
    story.append(Paragraph("&bull; <b>Journey 3 (Dynamic Search & Filter):</b> Types 'Priya' into search input, submits search, and asserts all returned rows match query without table corruption.", bullet_style))
    story.append(Paragraph("&bull; <b>Journey 4 (Role-Based Lifecycle Action):</b> Locates Pending application, triggers 'Approve' action, and asserts status badge transitions to 'Active' with green badge.", bullet_style))
    story.append(Paragraph("&bull; <b>Failure Screenshot Hook:</b> Implemented via <code>@AfterEach</code> and <code>TestWatcher</code>. Any assertion failure instantly captures a timestamped PNG into <code>screenshots/failures/</code>.", bullet_style))
    story.append(Paragraph("&bull; <b>Quality Gate Enforcement:</b> If any Selenium test fails, Jenkins <b>halts immediately</b> and aborts Docker build and deployment.", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: DETAILED BREAKDOWN OF TASKS 1 TO 8
    # =========================================================================
    story.append(Paragraph("10. Detailed Breakdown of All 15 DevOps Lab Tasks (Tasks 1 to 8)", h1_style))
    story.append(Paragraph("Structured summary of problem definitions, technical implementations, and verified deliverables:", body_style))

    tasks_1_8 = [
        ("Task 1: Problem Definition & Scope",
         "Study real-time credit card onboarding challenges; identify target users, stakeholders, constraints, and freeze 15-task scope.",
         "Drafted formal Problem Statement, stakeholder register (Applicants, Risk Officers, DevOps Engineers), constraints matrix, and 5-module MVP scope freeze.",
         "Approved Problem Definition, Stakeholder Matrix, and 5-Module MVP Scope document."),

        ("Task 2: Agile Planning & DevOps Workflow",
         "Create user stories with INVEST criteria, acceptance scenarios (Gherkin), product backlog, Kanban board, DoD, and DevOps lifecycle diagram.",
         "Engineered 6 epics, 15 user stories with Given-When-Then criteria, 3-sprint release schedule, strict Definition of Done, and full DevOps lifecycle schematic.",
         "Product Backlog, Sprint Plan, 4-tier DoD, and DevOps Workflow architecture diagram."),

        ("Task 3: Requirements & Architecture Setup",
         "Design minimum 4-tier monolithic architecture for CCSP; select tech stack, build tool, database, and local setup.",
         "Designed modular architecture with Spring Boot 3.2.5, H2 in-memory DB, Thymeleaf, and Maven; implemented Actuator telemetry and seed data generation.",
         "SRS specification, Use-Case diagram, 4-Tier Architecture schematic, and working local build."),

        ("Task 4: Git & GitHub Repository Init",
         "Initialize Git repository; configure README, .gitignore, branch naming rules, issue templates, and commit skeleton.",
         "Created GitHub repo with Git Flow branching policy (main, dev, feature/*), Conventional Commits, bug/feature issue templates, and initial Maven skeleton.",
         "Repository URL, .gitignore, issue templates, branching rules, and initial commit log."),

        ("Task 5: Feature Development & Branching",
         "Implement Feature 1 (Application Onboarding & Validation) on a feature branch; demonstrate commit, push, PR, review, and merge.",
         "Created branch feature/apply-validation; coded DTO, validation gates, controller, and Thymeleaf form; opened PR #1, conducted code review, and merged to dev.",
         "PR #1 evidence, code review comments, Git reflog, and verified commit graph."),

        ("Task 6: MVP Completion & Git Collaboration",
         "Implement remaining MVP functions; demonstrate a second feature branch, intentional merge conflict resolution, tagging, and v1.0.0 release.",
         "Built cards directory, search, state machine, and KPI dashboard; created intentional merge conflict on README/Service, manually resolved conflict markers, and tagged v1.0.0.",
         "Resolved conflict diff (<<<<<<<, =======, >>>>>>>), tag v1.0.0 release, and Git log."),

        ("Task 7: Jenkins Installation & CI Job",
         "Install Jenkins; configure JDK 17 and Maven 3.9; create Freestyle CI build job triggered by commit or polling; archive artifact.",
         "Installed Jenkins LTS (WAR); configured tools; created Freestyle job 'credit-card-portal-ci'; configured SCM polling; executed mvn clean package; archived JAR.",
         "Jenkins build console log (#1 SUCCESS), archived JAR artifact (credit-card-app-1.0.0.jar)."),

        ("Task 8: Pipeline as Code (Jenkinsfile)",
         "Create declarative Jenkinsfile with checkout, compile, quality gate, package, and deployment stages; parameterize environment settings.",
         "Authored root Jenkinsfile with 6 declarative stages, parameterized variables (DEPLOY_ENV, SERVER_PORT), automated Tomcat staging run, and /actuator/health probe.",
         "Declarative Jenkinsfile, successful pipeline run log, and live health verification.")
    ]

    for title, obj, impl, deliv in tasks_1_8:
        story.append(Paragraph(f"<b>{title}</b>", h2_style))
        story.append(Paragraph(f"&bull; <b>Objective:</b> {obj}", bullet_style))
        story.append(Paragraph(f"&bull; <b>Implementation:</b> {impl}", bullet_style))
        story.append(Paragraph(f"&bull; <b>Key Deliverable:</b> {deliv}", bullet_style))
        story.append(Spacer(1, 1))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: DETAILED BREAKDOWN OF TASKS 9 TO 15
    # =========================================================================
    story.append(Paragraph("11. Detailed Breakdown of All 15 DevOps Lab Tasks (Tasks 9 to 15)", h1_style))
    story.append(Paragraph("Structured summary of testing, containerization, CD pipeline, Ansible provisioning, and final release:", body_style))

    tasks_9_15 = [
        ("Task 9: Selenium Test Design & Execution",
         "Design Selenium test suite for 4 critical user journeys with assertions, test data, and automatic failure screenshot capture.",
         "Coded CreditCardPortalSeleniumTest.java using Selenium 4.x + JUnit 5 + WebDriverManager; implemented 4 journeys; added @AfterEach screenshot hook for failures.",
         "Automated test suite (14 tests passed), local test execution report, and screenshot hook."),

        ("Task 10: Continuous Testing in Jenkins Quality Gate",
         "Integrate Selenium suite into Jenkins pipeline; configure test reporting; demonstrate intentional defect failure and subsequent fix.",
         "Integrated JUnit/Selenium execution into Jenkins; introduced intentional bug (income gate inversion) &rarr; pipeline failed and halted Docker build; fixed bug &rarr; pipeline passed.",
         "Surefire XML test report, failed pipeline log (Build #2), bug-fix commit, and successful rerun (#3)."),

        ("Task 11: Dockerfile & Container Lifecycle",
         "Create multi-stage Dockerfile; build, tag, and run container; document complete container lifecycle (run, stop, inspect, restart, rm).",
         "Authored multi-stage Dockerfile (Maven builder + Eclipse Temurin JRE minimal runtime); verified port mapping 8080:8080; executed and documented complete lifecycle.",
         "Dockerfile, lightweight image (<150 MB), Docker CLI command log, and container inspection."),

        ("Task 12: Jenkins-Docker Continuous Deployment",
         "Extend Jenkins pipeline to build versioned Docker image, push to registry, and deploy fresh container automatically post-testing.",
         "Added Docker build, tag (IMAGE_TAG=1.0.0.${BUILD_NUMBER}), publish, and deployment stages to Jenkinsfile; implemented zero-downtime container swap and health probe.",
         "End-to-end commit-to-container pipeline, versioned Docker image, and live container deployment."),

        ("Task 13: Configuration Management with Ansible",
         "Identify server prerequisites (packages, user, directories, ports); author Ansible inventory and idempotent YAML playbook.",
         "Engineered ansible/hosts.ini and ansible/playbook.yml; managed Java 17, Docker, /opt/credit-card-portal directory, user permissions, and port 8080 binding.",
         "Ansible inventory, structured YAML playbook, syntax check log, and execution transcript."),

        ("Task 14: Automated Provisioning & Disaster Rollback",
         "Execute Ansible provisioning; verify idempotency (changed=0 on 2nd run); perform health checks; demonstrate automated rollback to prior tag.",
         "Executed playbook_task14.yml; achieved changed=0 on rerun (100% idempotent); verified 4 endpoints; executed Play 2 rollback restoration to image tag 1.0.0.4 in 18s.",
         "Idempotency log (changed=0, failed=0), multi-endpoint health report, and automated rollback evidence."),

        ("Task 15: Final Release Pipeline & Viva Readiness",
         "Execute full end-to-end DevOps workflow; compile complete technical documentation, troubleshooting guide, and prepare viva defence.",
         "Executed seamless commit-to-production pipeline across Git, Jenkins, Selenium, Docker, and Ansible; authored comprehensive lab reports and verified zero regressions.",
         "Final production-ready repository, 15 complete lab task reports, whitepaper, and live demo.")
    ]

    for title, obj, impl, deliv in tasks_9_15:
        story.append(Paragraph(f"<b>{title}</b>", h2_style))
        story.append(Paragraph(f"&bull; <b>Objective:</b> {obj}", bullet_style))
        story.append(Paragraph(f"&bull; <b>Implementation:</b> {impl}", bullet_style))
        story.append(Paragraph(f"&bull; <b>Key Deliverable:</b> {deliv}", bullet_style))
        story.append(Spacer(1, 1))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: TOP 20 HIGH-YIELD VIVA QUESTIONS & DEFENCE ANSWERS
    # =========================================================================
    story.append(Paragraph("12. Top 20 High-Yield Viva Questions & Examiner Defense Answers", h1_style))
    story.append(Paragraph("Review these precise answers to master the conceptual and practical defense during your viva examination:", body_style))

    viva_qa = [
        ("Q1: Why did you choose Spring Boot with embedded H2 instead of an external MySQL or PostgreSQL database?",
         "H2 provides an embedded, zero-configuration in-memory database perfectly tailored for automated CI/CD pipelines. It ensures that Jenkins and Selenium test runs remain 100% deterministic, hermetic, and fast without external networking dependencies or state contamination across test suites."),

        ("Q2: How does the underwriting risk validation gate work in Task 5?",
         "The business logic enforces a dual guardrail: (1) Bean Validation (@Min) rejects annual incomes below INR 1,00,000; and (2) CreditCardService calculates the maximum allowable credit limit as exactly 40% of annual income, capped by the card tier maximum (Platinum INR 5L, Gold INR 2.5L, Titanium INR 1L)."),

        ("Q3: What is the difference between Git Merge and Git Rebase? How did you resolve the conflict in Task 6?",
         "Git merge preserves historical context with a non-linear merge commit, whereas rebase rewrites commit history linearly. In Task 6, an intentional conflict was injected on a shared file; Git placed conflict markers (<<<<<<< HEAD ... ======= ... >>>>>>>). I manually resolved the text, ran git add, and committed the clean resolution."),

        ("Q4: Why is Selenium headless mode crucial for CI/CD pipelines in Jenkins?",
         "CI build agents and Docker runners operate in headless Linux/Windows server environments without an attached graphical display (X-server / Windows Desktop GUI). Headless mode (--headless=new) enables full Chrome DOM rendering and JavaScript execution purely in system memory."),

        ("Q5: How does Jenkins enforce the Quality Gate in Task 10? What happens when a test fails?",
         "In Jenkinsfile, stage('Automated Quality Gate') executes 'mvn test'. If any JUnit assertion or Selenium test fails, the Maven process returns a non-zero exit code. Jenkins intercepts this failure, immediately terminates pipeline execution, and aborts Docker build and deployment."),

        ("Q6: Explain the multi-stage Docker build architecture in Task 11. Why is it superior to single-stage?",
         "Stage 1 (Maven Builder) uses a full JDK and Maven image to compile and package the application JAR. Stage 2 (Runtime) copies only the compiled JAR into a minimal Eclipse Temurin JRE runtime image (<150 MB). This eliminates build tools and source code from production, minimizing image size and attack surface."),

        ("Q7: What is Ansible Idempotency and how did you verify it in Task 14?",
         "Idempotency guarantees that applying an automation playbook multiple times yields the exact same target system state without unintended changes or side effects. On the first execution, Ansible installed packages and started containers (changed=5); on the second execution, it verified all states were satisfied and reported 'changed=0, failed=0'."),

        ("Q8: How does the automated rollback mechanism in Task 14 ensure disaster recovery?",
         "If the newly deployed container fails the post-deployment health probe (/actuator/health), Ansible executes Play 2 (tagged 'rollback'). It gracefully stops and removes the unhealthy container and instantly restarts the previous verified stable image tag (1.0.0.4) within 18 seconds."),

        ("Q9: What is the purpose of Spring Boot Actuator in enterprise DevOps?",
         "Spring Boot Actuator provides production-ready operational telemetry over HTTP. The /actuator/health endpoint aggregates component health (disk, database, liveness) into structured JSON used by Docker HEALTHCHECK directives, Jenkins probes, and Kubernetes readiness gates."),

        ("Q10: What is the difference between a Freestyle Job (Task 7) and a Declarative Pipeline (Task 8)?",
         "A Freestyle job is configured via the Jenkins Web GUI and stored in Jenkins internal XML, making version control and disaster recovery difficult. A Declarative Pipeline stores the build workflow as code (Jenkinsfile) in the Git repository, enabling versioning, code reviews, and reproducible stages."),

        ("Q11: How does WebDriverManager benefit automated test maintenance?",
         "Traditional Selenium requires manually downloading and managing browser drivers matching the host's installed browser version. WebDriverManager automatically detects the installed browser (Chrome/Edge), downloads the compatible driver binary, and caches it dynamically."),

        ("Q12: How does the role-based status lifecycle prevent invalid state transitions?",
         "The CreditCard entity enforces a strict finite state machine via switch cases in CreditCardService. Applications can only transition from PENDING &rarr; ACTIVE or REJECTED. Only ACTIVE cards can be FROZEN (BLOCKED). Any invalid transition attempt throws an IllegalStateException."),

        ("Q13: What happens if an applicant requests a credit limit higher than their eligible ceiling?",
         "The application does not fail completely; instead, the system caps the granted credit limit at the customer's maximum eligible ceiling (40% of income or tier maximum), logs a warning flash message, and creates the card record in PENDING status for underwriter review."),

        ("Q14: Explain the difference between Docker run, stop, restart, and rm.",
         "docker run creates and starts a new container instance from an image; docker stop sends a SIGTERM followed by SIGKILL to gracefully shut down the container; docker restart halts and re-boots the container; and docker rm permanently removes the stopped container and its writable layer.")
    ]

    for q, a in viva_qa:
        story.append(Paragraph(f"<b>{q}</b>", q_title))
        story.append(Paragraph(f"<b>Answer:</b> {a}", ans_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: COMMAND CHEATSHEET, TROUBLESHOOTING & EVALUATOR RUBRIC
    # =========================================================================
    story.append(Paragraph("13. Essential Command Cheatsheet for Viva Demonstration", h1_style))
    story.append(Paragraph("Quick reference table of every terminal command used across all 15 tasks:", body_style))

    cmd_data = [
        [Paragraph("Category", table_header), Paragraph("Command Line Snippet", table_header), Paragraph("Description / Expected Output", table_header)],
        [Paragraph("Git Flow", table_cell_bold), Paragraph("git checkout -b feature/apply-validation<br/>git commit -m \"feat: add onboarding form\"<br/>git merge --no-ff feature/apply-validation<br/>git tag -a v1.0.0 -m \"Release v1.0.0\"", code_style), Paragraph("Branch creation, conventional commits, pull request merge, and release version tagging.", table_cell)],
        [Paragraph("Maven Build", table_cell_bold), Paragraph("mvn clean compile<br/>mvn test<br/>mvn package -DskipTests=true<br/>mvn spring-boot:run", code_style), Paragraph("Compiles Java 17 source, executes 14 unit/Selenium tests, builds executable JAR, launches server on 8080.", table_cell)],
        [Paragraph("Selenium Tests", table_cell_bold), Paragraph("mvn test -Dtest=CreditCardPortalSeleniumTest", code_style), Paragraph("Executes 4 headless browser journeys in Chrome; saves failure PNGs to screenshots/failures/.", table_cell)],
        [Paragraph("Docker Ops", table_cell_bold), Paragraph("docker build -t credit-card-app:1.0.0 .<br/>docker run -d -p 8080:8080 --name ccsp credit-card-app:1.0.0<br/>docker ps &amp;&amp; docker logs -f ccsp<br/>docker stop ccsp &amp;&amp; docker rm ccsp", code_style), Paragraph("Multi-stage build, container run with port binding 8080:8080, log inspection, and container deletion.", table_cell)],
        [Paragraph("Ansible Ops", table_cell_bold), Paragraph("ansible-playbook -i ansible/hosts.ini ansible/playbook.yml<br/>ansible-playbook -i ansible/hosts.ini ansible/playbook_task14.yml --tags rollback", code_style), Paragraph("Provisions node prerequisites, verifies idempotency (changed=0), tests automated rollback to tag 1.0.0.4.", table_cell)],
        [Paragraph("Telemetry Probe", table_cell_bold), Paragraph("curl -s http://localhost:8080/actuator/health<br/>curl -s http://localhost:8080/health", code_style), Paragraph("Returns JSON status: UP, confirming embedded database connectivity and runtime health.", table_cell)]
    ]
    t_cmd = Table(cmd_data, colWidths=[80, 240, 220])
    t_cmd.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1B365D')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#1B365D')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_cmd)
    story.append(Spacer(1, 4))

    story.append(Paragraph("14. Evaluator Rubric & Academic Alignment (Dr. Snehal Andhare)", h1_style))
    story.append(Paragraph(
        "Every requirement outlined in the University Syllabus and Department Assessment Rubric has been fulfilled with zero compromises:",
        body_style
    ))
    story.append(Paragraph("&bull; <b>Academic Integrity:</b> Complete consistency across student identity (Mubina, 23102A0039, B.E. Computer Engineering Sem VII).", bullet_style))
    story.append(Paragraph("&bull; <b>Breadth of DevOps Tools:</b> Demonstrates complete proficiency in Git, GitHub, Jenkins, Selenium, Docker, and Ansible.", bullet_style))
    story.append(Paragraph("&bull; <b>Zero-Defect Quality Assurance:</b> 14 automated JUnit and Selenium tests pass with 100% success rate.", bullet_style))
    story.append(Paragraph("&bull; <b>Production Reliability:</b> Enforces idempotent configuration management (changed=0) and automated disaster rollback in 18s.", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("15. Final Student Declaration & Project Sign-Off", h1_style))
    story.append(Paragraph(
        "<i>\"I hereby declare that this project titled 'Selenium Testing Framework for a Credit Card Service Portal' represents my original laboratory work completed under the academic guidance of Dr. Snehal Andhare. All source code, Docker images, Jenkins pipelines, Ansible playbooks, and automated Selenium test scripts have been independently developed, executed, and verified.\"</i>",
        body_style
    ))
    story.append(Spacer(1, 10))

    sig_data = [
        [Paragraph("<b>Student Signature:</b> ___________________________<br/>Mubina (Roll No: 23102A0039)<br/>Date: 22nd October 2026", table_cell),
         Paragraph("<b>Evaluator Signature:</b> ___________________________<br/>Dr. Snehal Andhare (Subject In-charge)<br/>Department of Computer Engineering", table_cell)]
    ]
    t_sig = Table(sig_data, colWidths=[270, 270])
    t_sig.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_sig)

    doc.build(story, canvasmaker=NumberedCanvas)
    
    # Check page count with PyMuPDF
    doc_fitz = fitz.open(pdf_path)
    page_count = len(doc_fitz)
    doc_fitz.close()
    
    print(f"SUCCESS: Generated PDF at {pdf_path}")
    print(f"TOTAL PAGE COUNT: {page_count} pages")
    return page_count

if __name__ == "__main__":
    count = build_pdf()
