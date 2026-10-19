import os
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from doc_helper import save_and_archive

def apply_table_styles(table, dxa_widths=None):
    """
    Applies exact department styling:
    - Fixed table width: 7900 dxa (5.486 inches) fitting inside the cell
    - No center misalignment (w:jc is NOT center, stays flush with text)
    - Fixed table layout (w:tblLayout type='fixed')
    - Clean single borders on all edges and inside cells (#CCCCCC)
    - Cell margins (padding): top=80, bottom=80, left=80, right=80 dxa
    - tblHeader on row 0 so headers repeat across page breaks
    - cantSplit on every row so rows don't get sliced across page breaks
    - Exact dxa column widths applied to every cell
    """
    tblPr = table._tbl.tblPr
    
    # Remove any existing jc to prevent centering overflow
    for jc in tblPr.xpath('./w:jc'):
        tblPr.remove(jc)
        
    # Set fixed table width to 7900 dxa
    for w in tblPr.xpath('./w:tblW'):
        tblPr.remove(w)
    tblPr.append(parse_xml(r'<w:tblW %s w:w="7900" w:type="dxa"/>' % nsdecls('w')))
    
    # Set fixed table layout
    for l in tblPr.xpath('./w:tblLayout'):
        tblPr.remove(l)
    tblPr.append(parse_xml(r'<w:tblLayout %s w:type="fixed"/>' % nsdecls('w')))
    
    # Clean borders
    for b in tblPr.xpath('./w:tblBorders'):
        tblPr.remove(b)
    tblBorders = parse_xml(r'''
        <w:tblBorders %s>
            <w:top w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
            <w:left w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
            <w:right w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
            <w:insideH w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
            <w:insideV w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
        </w:tblBorders>
    ''' % nsdecls('w'))
    tblPr.append(tblBorders)
    
    # Cell margins
    for m in tblPr.xpath('./w:tblCellMar'):
        tblPr.remove(m)
    tblCellMar = parse_xml(r'''
        <w:tblCellMar %s>
            <w:top w:w="80" w:type="dxa"/>
            <w:bottom w:w="80" w:type="dxa"/>
            <w:left w:w="80" w:type="dxa"/>
            <w:right w:w="80" w:type="dxa"/>
        </w:tblCellMar>
    ''' % nsdecls('w'))
    tblPr.append(tblCellMar)

    # Row 0: tblHeader + cantSplit
    header_trPr = table.rows[0]._tr.get_or_add_trPr()
    if not header_trPr.xpath('./w:tblHeader'):
        header_trPr.append(parse_xml(r'<w:tblHeader %s/>' % nsdecls('w')))
    if not header_trPr.xpath('./w:cantSplit'):
        header_trPr.append(parse_xml(r'<w:cantSplit %s/>' % nsdecls('w')))
    
    # All rows: cantSplit + exact cell width in dxa
    for row in table.rows:
        trPr = row._tr.get_or_add_trPr()
        if not trPr.xpath('./w:cantSplit'):
            trPr.append(parse_xml(r'<w:cantSplit %s/>' % nsdecls('w')))
        if dxa_widths:
            for idx, dxa_w in enumerate(dxa_widths):
                if idx < len(row.cells):
                    cell = row.cells[idx]
                    tcPr = cell._tc.get_or_add_tcPr()
                    for w in tcPr.xpath('./w:tcW'):
                        tcPr.remove(w)
                    tcPr.append(parse_xml(r'<w:tcW %s w:w="%s" w:type="dxa"/>' % (nsdecls('w'), str(dxa_w))))

def style_cell(cell, bg_color=None, bold=False, font_size=9.5, font_name="Calibri", text=None, align=WD_ALIGN_PARAGRAPH.LEFT):
    if bg_color:
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{bg_color}"/>')
        cell._tc.get_or_add_tcPr().append(shading)
    if text is not None:
        cell.text = text
    for p in cell.paragraphs:
        p.alignment = align
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        for r in p.runs:
            r.font.name = font_name
            r.font.size = Pt(font_size)
            r.bold = bold

def add_heading(cell, text, bold=True, size=12, keep_with_next=True):
    p = cell.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.keep_with_next = keep_with_next
    run = p.add_run(text)
    run.bold = bold
    run.font.name = "Calibri"
    run.font.size = Pt(size)
    return p

def add_subheading(cell, text, bold=True, size=11, keep_with_next=True):
    p = cell.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.keep_with_next = keep_with_next
    run = p.add_run(text)
    run.bold = bold
    run.font.name = "Calibri"
    run.font.size = Pt(size)
    return p

def add_body_p(cell, text, bold_prefix=None, space_after=3):
    p = cell.add_paragraph()
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(11)
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(11)
    return p

def add_figure(cell, image_path, caption_text, width_inches=5.4):
    p = cell.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    run = p.add_run()
    run.add_picture(image_path, width=Inches(width_inches))
    
    cap = cell.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_before = Pt(2)
    cap.paragraph_format.space_after = Pt(8)
    cap.paragraph_format.keep_with_next = True
    c_run = cap.add_run(caption_text)
    c_run.bold = True
    c_run.font.name = "Calibri"
    c_run.font.size = Pt(10)
    return p, cap

def generate_task2_document():
    # Base template for Task 2 to 15
    template_path = os.path.abspath("templates/template_standard.docx")
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template not found at: {template_path}")
        
    doc = docx.Document(template_path)
    
    # -------------------------------------------------------------
    # 1. Academic Header Envelopes (Table 0 and Table 1)
    # -------------------------------------------------------------
    t0 = doc.tables[0]
    t0.rows[0].cells[1].text = "B.E. Semester VII – Computer Engineering"
    style_cell(t0.rows[0].cells[1], bold=False, font_size=11, text="B.E. Semester VII – Computer Engineering")
    t0.rows[1].cells[1].text = "DevOps Lab"
    style_cell(t0.rows[1].cells[1], bold=False, font_size=11, text="DevOps Lab")
    t0.rows[2].cells[1].text = "Dr. Snehal Andhare"
    style_cell(t0.rows[2].cells[1], bold=False, font_size=11, text="Dr. Snehal Andhare")
    
    t1 = doc.tables[1]
    t1.rows[0].cells[1].text = "Mubina"
    style_cell(t1.rows[0].cells[1], bold=False, font_size=11, text="Mubina")
    t1.rows[1].cells[1].text = "23102A0039"
    style_cell(t1.rows[1].cells[1], bold=False, font_size=11, text="23102A0039")
    
    # Table 2: 5-row standard format
    t2 = doc.tables[2]
    
    # Row 0: Task Number
    t2.rows[0].cells[1].text = "2"
    style_cell(t2.rows[0].cells[1], bold=True, font_size=12, text="2")
    
    # Row 1: Task Title
    task_title = "Agile Planning and DevOps Workflow: Create user stories and acceptance criteria for the Credit Card Service Portal. Prepare a product backlog, 15-Task Kanban/Scrum plan, Definition of Done and a DevOps lifecycle diagram from development to operations."
    t2.rows[1].cells[1].text = task_title
    style_cell(t2.rows[1].cells[1], bold=True, font_size=11, text=task_title)
    
    # Row 2: Resources / Apparatus Required
    hw_text = "Hardware: Laptop / PC (x86_64), 16 GB RAM, 512 GB SSD, Intel Core i5/i7 or AMD Ryzen 5/7"
    sw_text = "Software: Windows 11, Eclipse Adoptium JDK 17/21 LTS, Apache Maven Wrapper (3.9.x), Spring Boot 3.x, Selenium WebDriver 4.x, Docker Engine, Jenkins CI/CD, Ansible Core, Git & GitHub, Google Chrome / Edge"
    t2.rows[2].cells[1].text = hw_text
    style_cell(t2.rows[2].cells[1], font_size=10, text=hw_text)
    t2.rows[2].cells[2].text = sw_text
    style_cell(t2.rows[2].cells[2], font_size=10, text=sw_text)
    
    # Row 3: Program & Output (Core Deliverable Content)
    body_cell = t2.rows[3].cells[1]
    if body_cell.paragraphs:
        body_cell.paragraphs[0].text = ""
        p0 = body_cell.paragraphs[0]
    else:
        p0 = body_cell.add_paragraph()
        
    p0.paragraph_format.space_before = Pt(4)
    p0.paragraph_format.space_after = Pt(2)
    p0.paragraph_format.keep_with_next = True
    r0 = p0.add_run("Agile planning philosophy and DevOps integration strategy")
    r0.bold = True
    r0.font.name = "Calibri"
    r0.font.size = Pt(12)
    
    add_body_p(body_cell, "In contemporary software engineering and digital banking operations, high-performing organizations replace monolithic, waterfall delivery cycles with an integrated Agile-DevOps paradigm. For the Credit Card Service Portal (CCSP), we implement a hybrid Scrumban methodology that fuses the iterative discipline of Scrum (sprint goal-setting, story point estimations, and strict Definitions of Done) with the continuous flow visibility of Kanban (visual WIP limits, bottleneck identification, and cycle-time optimization).")
    add_body_p(body_cell, "The strategic imperative of this agile planning phase is to decompose the broad system vision established in Task 1 into fine-grained, testable user stories with unequivocal acceptance criteria written in Gherkin format (Given/When/Then). By combining functional user stories with technical DevOps enablers—such as Selenium automated browser test suites, multi-stage Docker builds, and idempotent Ansible automation—every backlog item is engineered with automated verification at its core.")

    # Section 1: User Stories and Acceptance Criteria
    add_heading(body_cell, "1. Core user stories and Gherkin acceptance criteria", keep_with_next=True)
    add_body_p(body_cell, "To ensure that software behavior is precisely defined and directly translatable into automated Selenium WebDriver assertions in Task 9 and Task 10, I formulated six primary user stories covering customer operations, administrative workflows, and DevOps reliability gates:")

    # User Story 1
    add_subheading(body_cell, "User Story US-01: Digital Credit Card Application & Limit Request Management", keep_with_next=True)
    add_body_p(body_cell, "As a prospective retail customer, I want to submit my personal and employment details online and request a credit limit so that I can apply for a credit card without physical paperwork.", bold_prefix="• Story Formulation: ")
    add_body_p(body_cell, "Given the applicant navigates to the `/apply` endpoint, When valid details (Full Name, Email, Card Type [Platinum/Gold/Titanium], Annual Income > INR 3,00,000, Requested Limit) are submitted, Then the application is stored with status `PENDING`, a unique Card Application ID is generated, and a success confirmation displays with a link to `/cards`.", bold_prefix="  - Acceptance Scenario 1.1 (Valid Submission): ")
    add_body_p(body_cell, "Given the applicant is on the `/apply` form, When negative income, zero requested limit, or malformed email is entered, Then client-side and server-side validation gates prevent submission and render inline error messages adjacent to invalid fields.", bold_prefix="  - Acceptance Scenario 1.2 (Validation Failure): ")

    # User Story 2
    add_subheading(body_cell, "User Story US-02: Centralized Card Directory & Real-time Live Search", keep_with_next=True)
    add_body_p(body_cell, "As a branch relationship manager or operations analyst, I want to query the cardholder directory and perform real-time search by applicant name, card number, or lifecycle status so that I can instantly locate customer records.", bold_prefix="• Story Formulation: ")
    add_body_p(body_cell, "Given an officer views the `/cards` directory, When a search term (e.g., customer name or masked card number) is entered into the live search field, Then the application table dynamically filters to display only matching rows without triggering full-page reloads.", bold_prefix="  - Acceptance Scenario 2.1 (Live Search): ")
    add_body_p(body_cell, "Given an officer selects a status filter (`PENDING`, `ACTIVE`, `BLOCKED`, `REJECTED`) from the dropdown, When applied, Then only applications matching that exact lifecycle state are rendered.", bold_prefix="  - Acceptance Scenario 2.2 (Status Filtering): ")

    # User Story 3
    add_subheading(body_cell, "User Story US-03: Role-Based Card Approval & Lifecycle Governance", keep_with_next=True)
    add_body_p(body_cell, "As a credit risk officer, I want to evaluate submitted applications and execute status transitions between `PENDING` -> `ACTIVE` or `REJECTED` so that only creditworthy customers receive active credit cards.", bold_prefix="• Story Formulation: ")
    add_body_p(body_cell, "Given a card record exists in `PENDING` status, When an authorized officer clicks 'Approve', Then the status mutates to `ACTIVE`, an embossed masked card number is generated, and the status badge turns green.", bold_prefix="  - Acceptance Scenario 3.1 (Application Approval): ")
    add_body_p(body_cell, "Given a `PENDING` application that fails credit verification, When the officer clicks 'Reject', Then the status mutates to `REJECTED` and subsequent activation actions are permanently disabled.", bold_prefix="  - Acceptance Scenario 3.2 (Application Rejection): ")

    # User Story 4
    add_subheading(body_cell, "User Story US-04: Emergency Card Blocking / Security Freeze", keep_with_next=True)
    add_body_p(body_cell, "As a cardholder or risk officer, I want to immediately freeze a compromised or misplaced card so that unauthorized financial transactions are halted.", bold_prefix="• Story Formulation: ")
    add_body_p(body_cell, "Given an `ACTIVE` credit card, When the user or officer clicks 'Block Card', Then the card lifecycle status transitions immediately to `BLOCKED`, the status badge updates to danger red, and all payment gateway simulation authorizations return HTTP 403 Forbidden.", bold_prefix="  - Acceptance Scenario 4.1 (Immediate Security Freeze): ")
    add_body_p(body_cell, "Given a `BLOCKED` card, When KYC re-verification is completed and the officer clicks 'Unblock', Then the card status is restored to `ACTIVE` with an auditable security timestamp.", bold_prefix="  - Acceptance Scenario 4.2 (Card Unblocking & Restoration): ")

    # User Story 5
    add_subheading(body_cell, "User Story US-05: Executive Summary KPI Metrics Dashboard", keep_with_next=True)
    add_body_p(body_cell, "As a branch operations executive, I want to view aggregated real-time metrics cards so that I can monitor portfolio volume, approval ratios, and blocked card counts at a single glance.", bold_prefix="• Story Formulation: ")
    add_body_p(body_cell, "Given the user navigates to the portal dashboard `/`, When the page loads, Then four summary KPI cards render with dynamic real-time counts: Total Cards, Active Cards, Pending Applications, and Blocked Cards.", bold_prefix="  - Acceptance Scenario 5.1 (Real-Time Counter Aggregation): ")
    add_body_p(body_cell, "Given any lifecycle transition is executed (e.g., approval or freeze), When the dashboard is accessed, Then the KPI counts recalculate instantly to reflect the mutated state.", bold_prefix="  - Acceptance Scenario 5.2 (State Reflection Accuracy): ")

    # User Story 6
    add_subheading(body_cell, "User Story US-06: Production Liveness Probe & Actuator Telemetry", keep_with_next=True)
    add_body_p(body_cell, "As a DevOps / Platform SRE Engineer, I want an automated HTTP GET `/actuator/health` endpoint returning real-time JSON status `{\"status\": \"UP\"}` so that CI/CD pipelines, Docker probes, and Ansible provisioning scripts can deterministically verify container readiness.", bold_prefix="• Story Formulation: ")
    add_body_p(body_cell, "Given the Credit Card Service Portal application is running on port 8080, When an HTTP GET request is sent to `/actuator/health`, Then the server responds with HTTP 200 OK and payload `{\"status\":\"UP\"}`.", bold_prefix="  - Acceptance Scenario 6.1 (Healthy State Telemetry): ")
    add_body_p(body_cell, "Given a database initialization failure or server thread starvation, When probed, Then Actuator returns HTTP 503 Service Unavailable, signaling the Jenkins quality gate to abort deployment.", bold_prefix="  - Acceptance Scenario 6.2 (Unhealthy State Detection): ")

    # Section 2: Product Backlog and Estimation
    add_heading(body_cell, "2. Prioritized product backlog and Fibonacci estimation", keep_with_next=True)
    add_body_p(body_cell, "I structured the Product Backlog using the MoSCoW prioritization scheme (Must Have, Should Have, Could Have) and estimated relative complexity using the Fibonacci story point scale (1, 2, 3, 5, 8). Table 2.1 documents the complete prioritized backlog.")

    # Table 2.1: Product Backlog (Total = 7900 dxa: 800, 1500, 2600, 800, 1100, 1100)
    table_pb = body_cell.add_table(rows=9, cols=6)
    apply_table_styles(table_pb, dxa_widths=[800, 1500, 2600, 800, 1100, 1100])
    
    headers_pb = ["Item ID", "Epic / Module", "User Story / Backlog Description", "Points", "MoSCoW", "Sprint"]
    for i, h in enumerate(headers_pb):
        style_cell(table_pb.rows[0].cells[i], bg_color="EAECEE", bold=True, font_size=9.5, text=h)
        
    pb_data = [
        ("PBI-01", "Core Architecture", "Architect Spring Boot 3.x app, H2 database, Thymeleaf UI, Actuator health, and Maven setup.", "5", "Must Have", "Sprint 1"),
        ("PBI-02", "Version Control", "Initialize Git repository, configure .gitignore, branch policy, and initial application skeleton.", "3", "Must Have", "Sprint 1"),
        ("PBI-03", "Card Application", "Develop `/apply` form with client/server validation, credit limit checks, and H2 JPA persistence.", "5", "Must Have", "Sprint 2"),
        ("PBI-04", "Search & Directory", "Implement `/cards` searchable directory with live keyword filter and status dropdown selectors.", "5", "Must Have", "Sprint 2"),
        ("PBI-05", "Lifecycle & KPI", "Implement status finite state engine (Approve, Reject, Block) and summary dashboard KPI counters.", "8", "Must Have", "Sprint 2"),
        ("PBI-06", "CI Automation", "Configure Jenkins CI server, Maven automated build job triggered on Git commit, and artifact archiving.", "5", "Must Have", "Sprint 3"),
        ("PBI-07", "Selenium Quality Gate", "Author 4 Selenium WebDriver user journeys, JUnit 5 assertions, and failure screenshot capture hook.", "8", "Must Have", "Sprint 3"),
        ("PBI-08", "Docker & Ansible CD", "Engineer multi-stage Dockerfile, Jenkins Docker CD pipeline, and idempotent Ansible configuration.", "8", "Must Have", "Sprint 4")
    ]
    for r_idx, row_vals in enumerate(pb_data, start=1):
        for c_idx, val in enumerate(row_vals):
            style_cell(table_pb.rows[r_idx].cells[c_idx], font_size=8.5, text=val)

    # Section 3: 15-Task Kanban / Scrum Sprint Plan & Task Board
    add_heading(body_cell, "3. 15-task Kanban/Scrum sprint plan and task board matrix", keep_with_next=True)
    add_body_p(body_cell, "To align agile execution with our 15 university laboratory tasks, I organized the engineering lifecycle into four iterative sprints. Table 2.2 defines the Sprint Allocation Plan, and Table 2.3 defines the Kanban Task Board State Matrix with explicit Work-In-Progress (WIP) constraints.")

    # Table 2.2: Sprint Allocation Plan (Total = 7900 dxa: 1100, 1600, 2400, 1600, 1200)
    table_sp = body_cell.add_table(rows=5, cols=5)
    apply_table_styles(table_sp, dxa_widths=[1100, 1600, 2400, 1600, 1200])
    
    headers_sp = ["Sprint #", "Sprint Focus Theme", "Tasks Covered (University Syllabus)", "Key Deliverable Artifacts", "Velocity"]
    for i, h in enumerate(headers_sp):
        style_cell(table_sp.rows[0].cells[i], bg_color="EAECEE", bold=True, font_size=9.5, text=h)
        
    sp_data = [
        ("Sprint 1", "Inception & Architecture", "Task 1 (Scope), Task 2 (Agile), Task 3 (Architecture), Task 4 (Git Repo)", "SRS, Backlog, Working Spring Boot App, Git Repo", "16 Pts"),
        ("Sprint 2", "Feature Dev & Collaboration", "Task 5 (Feature Branching), Task 6 (MVP Release & Merge Conflict)", "Card Application, Directory Search, Tagged v1.0.0", "13 Pts"),
        ("Sprint 3", "CI & Automated Quality Gate", "Task 7 (Jenkins CI), Task 8 (Pipeline as Code), Task 9 (Selenium), Task 10 (Gate)", "Jenkinsfile, Selenium Suite, Defect Abort Proof", "23 Pts"),
        ("Sprint 4", "Containerization & IaC Delivery", "Task 11 (Docker), Task 12 (Docker CD), Task 13 (Ansible), Task 14 (Idempotency), Task 15 (Viva)", "Multi-Stage Dockerfile, Ansible Playbook, End-to-End Demo", "26 Pts")
    ]
    for r_idx, row_vals in enumerate(sp_data, start=1):
        for c_idx, val in enumerate(row_vals):
            style_cell(table_sp.rows[r_idx].cells[c_idx], font_size=8.5, text=val)

    # Insert Figure 2.1
    fig1_path = os.path.abspath("screenshots/task2/fig2_1_kanban_board.png")
    if os.path.exists(fig1_path):
        add_figure(body_cell, fig1_path, 
                   "Figure 2.1: Credit Card Service Portal — 15-Task Agile Kanban Sprint Board & Task Progression State", width_inches=5.4)

    # Table 2.3: Kanban State Progression Matrix (Total = 7900 dxa: 1400, 1500, 1600, 1700, 1700)
    add_subheading(body_cell, "Kanban Task Board State Matrix Across 15 Laboratory Tasks", keep_with_next=True)
    table_kb = body_cell.add_table(rows=6, cols=5)
    apply_table_styles(table_kb, dxa_widths=[1400, 1500, 1600, 1700, 1700])
    
    headers_kb = ["Sprint Iteration", "Backlog (WIP: Unlimited)", "To Do / Ready (WIP: 4)", "In Progress (WIP: 3)", "Done / Deployed (WIP: 15)"]
    for i, h in enumerate(headers_kb):
        style_cell(table_kb.rows[0].cells[i], bg_color="EAECEE", bold=True, font_size=9.5, text=h)
        
    kb_data = [
        ("Sprint 1 (Current)", "Tasks 5 to 15", "Task 3 (Architecture), Task 4 (Git Init)", "Task 2 (Agile Planning)", "Task 1 (Problem Scope)"),
        ("Sprint 2 (Upcoming)", "Tasks 7 to 15", "Task 5 (Card Apply Feature)", "Task 6 (MVP & Git Conflict)", "Tasks 1, 2, 3, 4"),
        ("Sprint 3 (Testing Gate)", "Tasks 11 to 15", "Task 7 (CI), Task 8 (Jenkinsfile)", "Task 9 (Selenium), Task 10 (Gate)", "Tasks 1 to 6"),
        ("Sprint 4 (Deployment)", "None", "Task 11 (Docker), Task 12 (CD)", "Task 13 & 14 (Ansible IaC)", "Tasks 1 to 10"),
        ("Post-Sprint 4 (Viva)", "None", "None", "Task 15 (Final Viva & Demo)", "Tasks 1 to 14 (Production Ready)")
    ]
    for r_idx, row_vals in enumerate(kb_data, start=1):
        for c_idx, val in enumerate(row_vals):
            style_cell(table_kb.rows[r_idx].cells[c_idx], font_size=8.5, text=val)

    # Section 4: Comprehensive Multi-Tier Definition of Done (DoD)
    add_heading(body_cell, "4. Multi-tier DevOps Definition of Done (DoD)", keep_with_next=True)
    add_body_p(body_cell, "To eliminate technical debt, ensure zero regression, and guarantee that code meets production-grade standards before advancing across pipeline stages, I formulated a strict, multi-tier Definition of Done. Table 2.4 details the seven verification tiers.")

    # Table 2.4: Definition of Done (Total = 7900 dxa: 1300, 2400, 2700, 1500)
    table_dod = body_cell.add_table(rows=8, cols=4)
    apply_table_styles(table_dod, dxa_widths=[1300, 2400, 2700, 1500])
    
    headers_dod = ["Quality Tier", "Quality Criterion", "Verification Standard & Threshold", "Enforcement Tool"]
    for i, h in enumerate(headers_dod):
        style_cell(table_dod.rows[0].cells[i], bg_color="EAECEE", bold=True, font_size=9.5, text=h)
        
    dod_data = [
        ("Tier 1: Code Quality", "Clean Code & Static Analysis", "Java 17/21 standards, zero SonarLint blocker/critical issues, modular packages.", "Maven Compiler & Checkstyle"),
        ("Tier 2: Unit Testing", "Component Level Validation", "100% pass on JUnit 5 service/controller tests; zero build warnings.", "Maven Surefire Plugin"),
        ("Tier 3: Selenium Gate", "Browser User Journey Testing", "100% pass on 4 critical user journeys; automatic timestamped screenshot on failure.", "Selenium WebDriver + JUnit 5"),
        ("Tier 4: Git Standards", "Branching & Peer Review", "Conventional Commits (feat, fix, docs), clean PR review, resolved merge conflict.", "Git CLI & GitHub PR Rules"),
        ("Tier 5: CI/CD Pipeline", "Pipeline as Code Automation", "Green Jenkins pipeline; intentional defect halts build; fix reruns to green.", "Declarative Jenkinsfile"),
        ("Tier 6: Containerization", "Multi-Stage Docker Image", "Minimal Temurin JRE runtime image < 350 MB; port 8080 exposed and verified.", "Docker CLI & Daemon Engine"),
        ("Tier 7: Infrastructure", "Idempotent Node Provisioning", "Ansible playbook execution yielding changed=0, failed=0 on 2nd run; /actuator/health UP.", "Ansible Core & cURL Probe")
    ]
    for r_idx, row_vals in enumerate(dod_data, start=1):
        for c_idx, val in enumerate(row_vals):
            style_cell(table_dod.rows[r_idx].cells[c_idx], font_size=8.5, text=val)

    # Section 5: End-to-End DevOps Lifecycle Architecture
    add_heading(body_cell, "5. End-to-end DevOps continuous delivery lifecycle architecture", keep_with_next=True)
    add_body_p(body_cell, "The Credit Card Service Portal implements a closed-loop, eight-stage DevOps continuous delivery lifecycle. The pipeline operates as an automated feedback loop connecting software development with IT operations:")
    
    add_body_p(body_cell, " Requirements captured as user stories in Product Backlog; sprint tasks managed on Kanban board (Tasks 1 & 2).", bold_prefix="1. Plan: ")
    add_body_p(body_cell, " Java 17/21 Spring Boot MVC controllers, Thymeleaf UI components, JPA entities; managed via Git feature branches (Tasks 3, 4, 5, 6).", bold_prefix="2. Code: ")
    add_body_p(body_cell, " Apache Maven wrapper compiles source, resolves dependencies, and packages executable JAR artifact (Tasks 7 & 8).", bold_prefix="3. Build: ")
    add_body_p(body_cell, " Headless Selenium WebDriver executes end-to-end browser journeys in Jenkins. If any assertion fails, the pipeline immediately halts deployment (Tasks 9 & 10).", bold_prefix="4. Test (Core Quality Gate): ")
    add_body_p(body_cell, " Multi-stage Docker build packages the validated JAR into a minimal Eclipse Temurin JRE image, tagged with build number (credit-card-app:${BUILD_NUMBER}) (Tasks 11 & 12).", bold_prefix="5. Release: ")
    add_body_p(body_cell, " Jenkins CD pipeline replaces old container with new versioned container on host port 8080 with zero manual intervention (Task 12).", bold_prefix="6. Deploy: ")
    add_body_p(body_cell, " Ansible inventory and YAML playbook provision target environment prerequisites, enforcing 100% idempotency (changed=0, failed=0) (Tasks 13 & 14).", bold_prefix="7. Configure: ")
    add_body_p(body_cell, " Spring Boot Actuator exposes real-time `/actuator/health` endpoint, continuously probed to ensure system liveness and trigger rollback if required (Tasks 14 & 15).", bold_prefix="8. Monitor & Feedback: ")

    # Insert Figure 2.2
    fig2_path = os.path.abspath("screenshots/task2/fig2_2_devops_lifecycle.png")
    if os.path.exists(fig2_path):
        add_figure(body_cell, fig2_path, 
                   "Figure 2.2: Credit Card Service Portal — End-to-End DevOps Continuous Delivery Lifecycle Architecture", width_inches=5.4)

    # Row 4: Conclusion Cell (Formal Academic Conclusion)
    t2.rows[4].cells[0].text = "Conclusion:"
    style_cell(t2.rows[4].cells[0], bold=True, font_size=11, text="Conclusion:")
    
    concl_cell = t2.rows[4].cells[1]
    if concl_cell.paragraphs:
        concl_cell.paragraphs[0].text = ""
        pc = concl_cell.paragraphs[0]
    else:
        pc = concl_cell.add_paragraph()
        
    pc.paragraph_format.space_before = Pt(3)
    pc.paragraph_format.space_after = Pt(3)
    pc.paragraph_format.line_spacing = 1.15
    rc = pc.add_run(
        "In Task 2, I successfully established the complete agile planning architecture and DevOps continuous delivery lifecycle "
        "for the Credit Card Service Portal (CCSP). I formulated six comprehensive user stories spanning digital card onboarding, "
        "real-time directory search, role-based status lifecycle transitions, emergency card freezing, summary KPI dashboards, and Actuator health probes. "
        "Each user story was formalized with rigorous Gherkin acceptance criteria (Given/When/Then), directly defining the automated assertion gates "
        "required for subsequent Selenium WebDriver test suites. I engineered a prioritized Product Backlog estimated via the Fibonacci scale, "
        "a 4-sprint execution plan mapping all 15 syllabus tasks, and an Agile Kanban Task Board governed by explicit Work-In-Progress (WIP) limits. "
        "Furthermore, I established a 7-tier Definition of Done (DoD) enforcing strict standards across code quality, automated testing, Git branching, "
        "Jenkins CI/CD, Docker containerization, and Ansible configuration idempotency. Finally, I modeled the end-to-end 8-stage DevOps continuous "
        "lifecycle architecture, validating the feedback mechanism that connects software planning to production monitoring. "
        "All deliverable requirements for Task 2 have been verified and documented, providing an unambiguous engineering blueprint for Task 3 Application Architecture and Technology Setup."
    )
    rc.font.name = "Calibri"
    rc.font.size = Pt(11)

    # -------------------------------------------------------------
    # Save and Archive Output Document
    # -------------------------------------------------------------
    output_filename = "DevOps_Task2_Mubina_23102A0039.docx"
    canonical_path = os.path.abspath(os.path.join("docs", output_filename))
    
    saved_path = save_and_archive(doc, canonical_path)
    print(f"\nTask 2 Document successfully generated at: {saved_path}")
    return saved_path

if __name__ == "__main__":
    generate_task2_document()
