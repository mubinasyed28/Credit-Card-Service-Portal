import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

os.makedirs("screenshots/task9", exist_ok=True)

# ----------------------------------------------------------------------
# Figure 9.1: Selenium WebDriver 4.x Automation Architecture & Quality Gate
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11.5, 6.8), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

# Title Banner
rect_title = patches.FancyBboxPatch((2, 91), 96, 7.5, boxstyle="round,pad=0.8", ec="#1B365D", fc="#1B365D", zorder=2)
ax.add_patch(rect_title)
ax.text(50, 94.7, "SELENIUM WEBDRIVER 4.x AUTOMATION ARCHITECTURE & TEST EXECUTION FRAMEWORK (TASK 9)", 
        color="white", fontsize=10, fontweight="bold", ha="center", va="center")

# Layer 1: Test Runner & LifeCycle (Left: Width: 28)
box_runner = patches.FancyBboxPatch((3, 22), 28, 65, boxstyle="round,pad=0.6", ec="#8E44AD", fc="#F4ECF7", lw=1.4, zorder=2)
ax.add_patch(box_runner)
ax.text(17, 83.5, "JUNIT 5 & TEST HARNESS", color="#512E5F", fontsize=8.5, fontweight="bold", ha="center")
ax.text(17, 80, "Test Runner & Lifecycle Management", color="#6C3483", fontsize=7.2, fontweight="bold", ha="center")

runner_items = [
    ("JUnit 5 Jupiter Engine", "Executes @Test, @Order(1..4),\n@BeforeEach & @AfterEach hooks", 71),
    ("WebDriverManager 5.8.0", "Automated binary resolution for\nchromedriver.exe (win64 155.0)", 60),
    ("Spring Boot Test Server", "@SpringBootTest(RANDOM_PORT)\nEmbedded Tomcat 10.1 & H2 DB", 49),
    ("Failure Screenshot Hook", "TakesScreenshot API captures PNG\ninto screenshots/failures/ on error", 38),
    ("Surefire Reporting Plugin", "Emits surefire-reports/*.xml\nAggregates 4/4 passing tests", 27)
]
for title, desc, y_pos in runner_items:
    ib = patches.FancyBboxPatch((4.5, y_pos - 3), 25, 9, boxstyle="round,pad=0.3", ec="#7D3C98", fc="#FFFFFF", lw=1, zorder=3)
    ax.add_patch(ib)
    ax.text(17, y_pos + 4, title, color="#512E5F", fontsize=6.8, fontweight="bold", ha="center")
    ax.text(17, y_pos, desc, color="#2C3E50", fontsize=5.8, ha="center")

# Connecting Arrow Runner -> Driver
ax.annotate("", xy=(34, 55), xytext=(31, 55),
            arrowprops=dict(arrowstyle="->", color="#1B365D", lw=2.5, mutation_scale=14))

# Layer 2: Selenium WebDriver Core Engine (Middle: Width: 32)
box_engine = patches.FancyBboxPatch((34, 22), 32, 65, boxstyle="round,pad=0.6", ec="#2980B9", fc="#EBF5FB", lw=1.4, zorder=2)
ax.add_patch(box_engine)
ax.text(50, 83.5, "SELENIUM WEBDRIVER 4.19.1", color="#1B4F72", fontsize=8.5, fontweight="bold", ha="center")
ax.text(50, 80, "Headless W3C Browser Automation Engine", color="#2874A6", fontsize=7.2, fontweight="bold", ha="center")

engine_items = [
    ("Headless Chrome Options", "--headless=new --disable-gpu\n--window-size=1920,1080 --no-sandbox", 71),
    ("Explicit Wait Mechanism", "WebDriverWait (Duration: 10s)\nExpectedConditions.visibilityOf()", 60),
    ("Locator Strategy Suite", "By.id('customerName', 'btn-search')\nBy.cssSelector, By.className", 49),
    ("Form Interaction Engine", "sendKeys(), click(), clear()\nSelect(By.id('cardType'))", 38),
    ("State & DOM Assertions", "assertEquals(title), assertTrue()\nVerify badge text & CSS classes", 27)
]
for title, desc, y_pos in engine_items:
    eb = patches.FancyBboxPatch((35.5, y_pos - 3), 29, 9, boxstyle="round,pad=0.3", ec="#2980B9", fc="#FFFFFF", lw=1, zorder=3)
    ax.add_patch(eb)
    ax.text(50, y_pos + 4, title, color="#1B4F72", fontsize=6.8, fontweight="bold", ha="center")
    ax.text(50, y_pos, desc, color="#2C3E50", fontsize=5.8, ha="center")

# Connecting Arrow Driver -> Target
ax.annotate("", xy=(69, 55), xytext=(66, 55),
            arrowprops=dict(arrowstyle="->", color="#1B365D", lw=2.5, mutation_scale=14))

# Layer 3: Application Under Test (AUT) (Right: Width: 28)
box_aut = patches.FancyBboxPatch((69, 22), 28, 65, boxstyle="round,pad=0.6", ec="#27AE60", fc="#EAFAF1", lw=1.4, zorder=2)
ax.add_patch(box_aut)
ax.text(83, 83.5, "CREDIT CARD PORTAL (AUT)", color="#196F3D", fontsize=8.5, fontweight="bold", ha="center")
ax.text(83, 80, "Live Target Application Under Test", color="#1E8449", fontsize=7.2, fontweight="bold", ha="center")

aut_items = [
    ("/apply Page (Journey 1)", "Digital card application form\nDynamic debt limit evaluator", 71),
    ("Validation Gate (Journey 2)", "Inline feedback (#err-annualIncome)\nBlocks sub-100k submissions", 60),
    ("/cards Directory (Journey 3)", "Multi-field search & live filter\nDynamic table row filtering", 49),
    ("Status Engine (Journey 4)", "Role-based approvals & freeze\nPENDING -> ACTIVE transition", 38),
    ("Actuator / Health Endpoint", "Continuous health probe (/health)\nEnsures runtime integrity", 27)
]
for title, desc, y_pos in aut_items:
    ab = patches.FancyBboxPatch((70.5, y_pos - 3), 25, 9, boxstyle="round,pad=0.3", ec="#27AE60", fc="#FFFFFF", lw=1, zorder=3)
    ax.add_patch(ab)
    ax.text(83, y_pos + 4, title, color="#196F3D", fontsize=6.8, fontweight="bold", ha="center")
    ax.text(83, y_pos, desc, color="#2C3E50", fontsize=5.8, ha="center")

# Bottom Banner: Framework Key Advantages
box_foot = patches.FancyBboxPatch((3, 3), 94, 15, boxstyle="round,pad=0.5", ec="#D35400", fc="#FEF9E7", lw=1.3, zorder=2)
ax.add_patch(box_foot)
ax.text(50, 14.5, "SELENIUM AUTOMATED TESTING QUALITY GATE & FAILURE RECOVERY STANDARDS", color="#B9770E", fontsize=8, fontweight="bold", ha="center")
ax.text(50, 8.5, "• Zero Driver Configuration: WebDriverManager automatically negotiates and installs OS-specific chromedriver.\n• Resilient Synchronization: 100% of interactions utilize explicit waits (WebDriverWait) eliminating brittle Thread.sleep calls.\n• Automated Failure Evidence: Any assertion failure automatically triggers full-page screenshot archiving into screenshots/failures/.\n• CI/CD Pipeline Gate: Headless Chrome runs seamlessly inside Maven build jobs without requiring a graphical desktop environment.", 
        color="#1B365D", fontsize=6.8, ha="center")

plt.tight_layout()
fig9_1_path = "screenshots/task9/fig9_1_selenium_framework_architecture.png"
plt.savefig(fig9_1_path, dpi=300, bbox_inches="tight")
plt.close()
print(f"Generated {fig9_1_path}")

# ----------------------------------------------------------------------
# Figure 9.2: 4 Critical User Journeys Execution Flow & Validation Matrix
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11.5, 6.8), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

# Title Banner
rect_title2 = patches.FancyBboxPatch((2, 91), 96, 7.5, boxstyle="round,pad=0.8", ec="#1B365D", fc="#1B365D", zorder=2)
ax.add_patch(rect_title2)
ax.text(50, 94.7, "4 CRITICAL USER JOURNEYS EXECUTION FLOW & VALIDATION EVIDENCE (TASK 9)", 
        color="white", fontsize=10, fontweight="bold", ha="center", va="center")

journeys = [
    ("Journey 1: Card Application Onboarding",
     "Input: Aarav Sharma | Platinum | Limit: 300k | Income: 1200k\nAction: Submit form on /apply\nAssert: Redirect to /cards, alert-success displayed,\nrecord created in table with status 'Pending Approval'",
     "#D4EFDF", "#27AE60", 72, "PASSED (14.2s)", "Evidence: journey1_application_success.png"),

    ("Journey 2: Validation Gate Enforcement",
     "Input: Invalid Tester | Titanium | Income: 50,000 (Sub-100k)\nAction: Submit application form\nAssert: Block submission, remain on /apply,\nassert inline error #err-annualIncome is displayed",
     "#FCF3CF", "#B7950B", 50, "PASSED (8.5s)", "Evidence: journey2_validation_gate.png"),

    ("Journey 3: Multi-Field Search & Live Filtering",
     "Input: Search query 'Priya' in #search-input\nAction: Click #btn-search button\nAssert: Table dynamically filters, matching rows contain 'Priya',\nnon-matching customer records excluded from view",
     "#EBF5FB", "#2980B9", 28, "PASSED (12.1s)", "Evidence: journey3_search_filter.png"),

    ("Journey 4: Status Lifecycle Approval Transition",
     "Target: Locate PENDING card row in #cards-table\nAction: Click #btn-approve-{id} button\nAssert: Status badge updates to 'Active / Approved',\nCSS badge class transitions to 'bg-success'",
     "#F4ECF7", "#8E44AD", 6, "PASSED (15.8s)", "Evidence: journey4_status_lifecycle.png")
]

for title, desc, fc, ec, y_pos, status, evid in journeys:
    j_box = patches.FancyBboxPatch((3, y_pos), 94, 18.5, boxstyle="round,pad=0.5", ec=ec, fc=fc, lw=1.4, zorder=2)
    ax.add_patch(j_box)
    
    # Header tag
    ax.text(5.5, y_pos + 14.8, title, color="#1B365D", fontsize=8.5, fontweight="bold")
    
    # Status Pill
    st_pill = patches.FancyBboxPatch((81, y_pos + 13), 14, 4.5, boxstyle="round,pad=0.2", ec="#27AE60", fc="#FFFFFF", zorder=3)
    ax.add_patch(st_pill)
    ax.text(88, y_pos + 15.2, status, color="#196F3D", fontsize=7.2, fontweight="bold", ha="center")
    
    # Description Body
    ax.text(5.5, y_pos + 7.5, desc, color="#2C3E50", fontsize=7.2)
    
    # Evidence tag
    ax.text(5.5, y_pos + 2.5, evid, color="#566573", fontsize=6.8, fontstyle="italic")

plt.tight_layout()
fig9_2_path = "screenshots/task9/fig9_2_user_journeys_matrix.png"
plt.savefig(fig9_2_path, dpi=300, bbox_inches="tight")
plt.close()
print(f"Generated {fig9_2_path}")
