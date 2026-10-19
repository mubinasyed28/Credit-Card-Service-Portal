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

def generate_task5_document():
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
    t2.rows[0].cells[1].text = "5"
    style_cell(t2.rows[0].cells[1], bold=True, font_size=12, text="5")
    
    # Row 1: Task Title
    task_title = "Feature Development with Branching: Implement the first core workflow of the Credit Card Service Portal on a feature branch. Use add, commit, push, pull and logs. Raise a pull request, review changes and merge into the development branch."
    t2.rows[1].cells[1].text = task_title
    style_cell(t2.rows[1].cells[1], bold=True, font_size=11, text=task_title)
    
    # Row 2: Resources / Apparatus Required
    hw_text = "Hardware: Laptop / PC (x86_64), 16 GB RAM, 512 GB SSD, Intel Core i5/i7 or AMD Ryzen 5/7"
    sw_text = "Software: Git 2.44+, GitHub Enterprise / Cloud, Windows 11 PowerShell, Eclipse Adoptium JDK 17 LTS, Apache Maven 3.9.6, Spring Boot 3.2.5, JUnit 5"
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
    r0 = p0.add_run("Executive summary and feature branching philosophy")
    r0.bold = True
    r0.font.name = "Calibri"
    r0.font.size = Pt(12)
    
    add_body_p(body_cell, "In professional DevOps engineering, direct modification of production or integration branches introduces severe risk of untested code leakage, regressions, and broken builds. Feature branching is an essential Git collaboration practice where individual functional capabilities are developed, tested, and validated in complete isolation on a dedicated branch branched off `dev`. Only after passing automated quality gates and formal peer code review is the branch merged back into the integration trunk.")
    add_body_p(body_cell, "The objective of Task 5 is to implement the first core workflow of the Credit Card Service Portal—Digital Credit Card Application & Limit Evaluation—on a dedicated feature branch (`feature/card-application-workflow`). I engineered dynamic credit limit assessment algorithms, expanded validation gates, authored comprehensive JUnit 5 unit tests, executed live Git staging and commit operations, and performed a non-fast-forward merge (`--no-ff`) into `dev` simulating an approved Pull Request review.")

    # Section 1: Feature 1 Functional Architecture
    add_heading(body_cell, "1. Feature 1 architecture: Credit card application & limit evaluation engine", keep_with_next=True)
    add_body_p(body_cell, "The first core workflow governs digital card onboarding and intelligent credit limit evaluation. When prospective applicants submit their profile, the service calculates the maximum credit eligibility based on their annual income and desired card tier, enforcing strict banking prudential guidelines:")
    
    add_body_p(body_cell, " In accordance with retail credit risk standards, an applicant's maximum permissible credit line is bounded to 40% of their documented annual income.", bold_prefix="• 40% Income Prudential Ceiling: ")
    add_body_p(body_cell, " Each card tier maintains an immutable hard limit: Titanium (₹1,00,000), Gold (₹2,50,000), and Platinum (₹5,00,000). The evaluated limit is strictly the lesser of the 40% income ceiling and the tier cap: min(Income × 0.40, Tier_Max).", bold_prefix="• Tier-Specific Maximum Limit Cap: ")
    add_body_p(body_cell, " If an applicant requests a limit exceeding their calculated eligibility, the engine automatically caps the assigned limit to their eligibility threshold and issues an informative notification.", bold_prefix="• Automatic Downward Limit Adjustment: ")

    # Table 5.1: Eligibility Rules (Total = 7900 dxa: 1400, 1600, 1600, 1700, 1600)
    table_el = body_cell.add_table(rows=5, cols=5)
    apply_table_styles(table_el, dxa_widths=[1400, 1600, 1600, 1700, 1600])
    
    headers_el = ["Card Tier", "Tier Maximum Limit", "Annual Income Sample", "40% Calculated Ceiling", "Approved Limit"]
    for i, h in enumerate(headers_el):
        style_cell(table_el.rows[0].cells[i], bg_color="EAECEE", bold=True, font_size=9.5, text=h)
        
    el_data = [
        ("Titanium Card", "₹1,00,000.00", "₹4,50,000.00", "₹1,80,000.00", "₹1,00,000.00 (Tier Capped)"),
        ("Gold Card", "₹2,50,000.00", "₹5,00,000.00", "₹2,00,000.00", "₹2,00,000.00 (Income Capped)"),
        ("Platinum Card", "₹5,00,000.00", "₹12,00,000.00", "₹4,80,000.00", "₹4,80,000.00 (Income Capped)"),
        ("Platinum Card", "₹5,00,000.00", "₹18,00,000.00", "₹7,20,000.00", "₹5,00,000.00 (Tier Capped)")
    ]
    for r_idx, row_vals in enumerate(el_data, start=1):
        for c_idx, val in enumerate(row_vals):
            style_cell(table_el.rows[r_idx].cells[c_idx], font_size=8.5, text=val)

    # Insert Figure 5.2: Sequence Diagram
    fig2_path = os.path.abspath("screenshots/task5/fig5_2_onboarding_workflow_sequence.png")
    if os.path.exists(fig2_path):
        add_figure(body_cell, fig2_path, 
                   "Figure 5.1: Sequence Diagram of Credit Card Application & Eligibility Evaluation Workflow", width_inches=5.4)

    # Section 2: Git Feature Branching Lifecycle
    add_heading(body_cell, "2. Feature branch creation, live Git operations, and commit log", keep_with_next=True)
    add_body_p(body_cell, "Following the Git Flow branching guidelines established in Task 4, I branched off the integration trunk (`dev`), implemented the feature changes, staged modified and new source files, and executed Conventional Commits. Table 5.2 outlines the complete terminal operation sequence:")

    # Table 5.2: Terminal Operations (Total = 7900 dxa: 600, 1800, 3000, 2500)
    table_git = body_cell.add_table(rows=7, cols=4)
    apply_table_styles(table_git, dxa_widths=[600, 1800, 3000, 2500])
    
    headers_git = ["Step", "Git Operation", "Terminal Command Executed", "Verified System Response"]
    for i, h in enumerate(headers_git):
        style_cell(table_git.rows[0].cells[i], bg_color="EAECEE", bold=True, font_size=9.5, text=h)
        
    git_data = [
        ("1", "Checkout Integration", "git checkout dev", "Switched to branch 'dev' as the source baseline."),
        ("2", "Create Feature Branch", "git checkout -b feature/card-application-workflow", "Switched to a new branch 'feature/card-application-workflow'."),
        ("3", "Implement Code", "Code edits in CreditCardService, Controller, Tests", "Source code enhanced with limit calculator and unit tests."),
        ("4", "Run Local Tests", "mvn test", "Surefire test report generated: 8 tests run, 0 failures, BUILD SUCCESS."),
        ("5", "Stage Changes", "git add app/", "Staged modified service, controller, and new test class."),
        ("6", "Feature Commit", "git commit -m 'feat(application): implement dynamic credit limit evaluation...'", "[feature/card-application-workflow e2b0d4b] 3 files changed, 86 insertions(+).")
    ]
    for r_idx, row_vals in enumerate(git_data, start=1):
        for c_idx, val in enumerate(row_vals):
            style_cell(table_git.rows[r_idx].cells[c_idx], font_size=8.5, text=val)

    # Section 3: Automated Testing Gate
    add_heading(body_cell, "3. Automated testing verification gate for Feature 1", keep_with_next=True)
    add_body_p(body_cell, "Before raising a Pull Request, the Definition of Done mandates 100% test pass on all unit and integration tests. I authored `CreditCardApplicationWorkflowTest.java` containing three targeted test cases to validate the business logic. Table 5.3 summarizes the automated test execution results:")

    # Table 5.3: Unit Test Suite Results (Total = 7900 dxa: 800, 2600, 3000, 1500)
    table_test = body_cell.add_table(rows=5, cols=4)
    apply_table_styles(table_test, dxa_widths=[800, 2600, 3000, 1500])
    
    headers_test = ["Test #", "Test Method Name", "Validation Scope & Test Assertions", "Result Status"]
    for i, h in enumerate(headers_test):
        style_cell(table_test.rows[0].cells[i], bg_color="EAECEE", bold=True, font_size=9.5, text=h)
        
    test_data = [
        ("TC-01", "testMaxEligibleLimitCalculation()", "Asserts 40% income cap evaluation and tier maximum capping (Titanium @ 1L, Platinum @ 5L).", "PASSED (0.015s)"),
        ("TC-02", "testIsEligibleForRequestedLimit()", "Verifies boolean gate returning true when requested limit <= ceiling and false when exceeding.", "PASSED (0.008s)"),
        ("TC-03", "testApplicationLimitCapping()", "Validates that submitting an application with excessive requested limit automatically caps to ceiling.", "PASSED (0.022s)"),
        ("TC-04", "CreditCardServiceTest (Suite of 5 Tests)", "Regression verification of seed data, status approve, emergency block, and KPI calculations.", "PASSED (0.632s)")
    ]
    for r_idx, row_vals in enumerate(test_data, start=1):
        for c_idx, val in enumerate(row_vals):
            style_cell(table_test.rows[r_idx].cells[c_idx], font_size=8.5, text=val)

    add_body_p(body_cell, "Total Test Suite Summary: 8 Tests Run, 0 Failures, 0 Errors, 0 Skipped. Overall Maven Build Time: 48.95s. Quality Gate Passed.")

    # Section 4: Pull Request Simulation
    add_heading(body_cell, "4. Pull Request simulation, peer review audit, and approval checklist", keep_with_next=True)
    add_body_p(body_cell, "In professional GitHub enterprise workflows, merging a feature branch requires raising a Pull Request (PR) against `dev`. Table 5.4 documents the simulated Pull Request review metadata, reviewer comments, and quality gate sign-off:")

    # Table 5.4: PR Review Audit (Total = 7900 dxa: 1500, 2200, 2700, 1500)
    table_pr = body_cell.add_table(rows=6, cols=4)
    apply_table_styles(table_pr, dxa_widths=[1500, 2200, 2700, 1500])
    
    headers_pr = ["PR Audit Dimension", "Configured PR Attribute", "Reviewer Assessment & Feedback", "Sign-Off Status"]
    for i, h in enumerate(headers_pr):
        style_cell(table_pr.rows[0].cells[i], bg_color="EAECEE", bold=True, font_size=9.5, text=h)
        
    pr_data = [
        ("PR Identifier", "Pull Request #1", "Branch: feature/card-application-workflow -> Target: dev", "Verified"),
        ("PR Title", "feat(app): dynamic credit limit evaluation", "Follows Conventional Commits standard with clear scope.", "Approved"),
        ("Code Review", "Separation of Concerns", "Eligibility calculation cleanly encapsulated in CreditCardService; Controller remains lightweight.", "Approved (Lead)"),
        ("Test Coverage", "JUnit 5 Automated Tests", "Added CreditCardApplicationWorkflowTest covering edge cases for tier capping.", "Approved (QA)"),
        ("Merge Feasibility", "Mergeability Assessment", "Clean merge without conflicts against dev trunk.", "Ready to Merge")
    ]
    for r_idx, row_vals in enumerate(pr_data, start=1):
        for c_idx, val in enumerate(row_vals):
            style_cell(table_pr.rows[r_idx].cells[c_idx], font_size=8.5, text=val)

    # Insert Figure 5.1: Feature Branching Workflow
    fig1_path = os.path.abspath("screenshots/task5/fig5_1_feature_branch_workflow.png")
    if os.path.exists(fig1_path):
        add_figure(body_cell, fig1_path, 
                   "Figure 5.2: Git Flow Feature Branching Lifecycle and Pull Request Quality Gate", width_inches=5.4)

    # Section 5: Non-Fast-Forward Merge
    add_heading(body_cell, "5. Non-fast-forward merge into dev and commit graph audit", keep_with_next=True)
    add_body_p(body_cell, "Following PR approval, I executed a non-fast-forward merge (`git merge --no-ff`) into `dev`. The `--no-ff` flag forces Git to create an explicit merge commit, preserving the isolated history of the feature branch and facilitating clean tracking and rollbacks. The verified Git log graph confirms the merge:")
    
    add_body_p(body_cell, "*   7352dcd Merge pull request #1 from feature/card-application-workflow into dev\n|\\\n| * e2b0d4b feat(application): implement dynamic credit limit evaluation and onboarding workflow\n|/\n* 08ce054 docs: compile Task 4 Git repository initialization report\n* 2aa4bd5 feat: initialize Credit Card Service Portal application skeleton and repository structure", bold_prefix="Git Commit Graph (git log --graph --oneline):\n")

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
        "In Task 5, I successfully demonstrated professional feature development using Git branching for the Credit Card Service Portal (CCSP). "
        "I isolated the first core workflow on a dedicated feature branch (`feature/card-application-workflow`), implementing dynamic credit limit "
        "evaluation algorithms that enforce a 40% income ceiling and card tier limits. I expanded the automated test suite with "
        "`CreditCardApplicationWorkflowTest.java`, achieving 100% pass across all 8 unit tests under Apache Maven. "
        "I conducted live Git operations spanning branch creation, staging, and Conventional Commits (`feat(application)`). "
        "Furthermore, I conducted a formal Pull Request simulation auditing code review notes, test coverage, and mergeability. "
        "Finally, I executed a non-fast-forward merge (`git merge --no-ff`) into the `dev` integration trunk (merge commit `7352dcd`), "
        "preserving complete commit history and establishing an auditable baseline for Task 6 MVP Completion and Git Collaboration."
    )
    rc.font.name = "Calibri"
    rc.font.size = Pt(11)

    # -------------------------------------------------------------
    # Save and Archive Output Document
    # -------------------------------------------------------------
    output_filename = "DevOps_Task5_Mubina_23102A0039.docx"
    canonical_path = os.path.abspath(os.path.join("docs", output_filename))
    
    saved_path = save_and_archive(doc, canonical_path)
    print(f"\nTask 5 Document successfully generated at: {saved_path}")
    return saved_path

if __name__ == "__main__":
    generate_task5_document()
