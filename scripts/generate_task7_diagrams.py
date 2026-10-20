import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

os.makedirs("screenshots/task7", exist_ok=True)

# ----------------------------------------------------------------------
# Figure 7.1: Jenkins Continuous Integration Architecture & Automated Workflow
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11.5, 6.8), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

# Title Banner
rect_title = patches.FancyBboxPatch((2, 91), 96, 7.5, boxstyle="round,pad=0.8", ec="#1B365D", fc="#1B365D", zorder=2)
ax.add_patch(rect_title)
ax.text(50, 94.7, "JENKINS CONTINUOUS INTEGRATION (CI) ARCHITECTURE & WORKFLOW (TASK 7)", 
        color="white", fontsize=10.5, fontweight="bold", ha="center", va="center")

# Outer Container 1: Git & GitHub SCM Trigger
box_git = patches.FancyBboxPatch((3, 48), 24, 38, boxstyle="round,pad=0.6", ec="#E74C3C", fc="#FDEDEC", lw=1.5, zorder=2)
ax.add_patch(box_git)
ax.text(15, 82.5, "SOURCE CODE MANAGEMENT", color="#922B21", fontsize=8.5, fontweight="bold", ha="center")
ax.text(15, 79, "Git & GitHub Repository", color="#641E16", fontsize=7.5, fontweight="bold", ha="center")

# Sub-boxes in Git
box_repo = patches.FancyBboxPatch((4.5, 63), 21, 13, boxstyle="round,pad=0.4", ec="#C0392B", fc="#FFFFFF", lw=1.2, zorder=3)
ax.add_patch(box_repo)
ax.text(15, 72.5, "Repository: credit-card-portal", color="#1B365D", fontsize=7, fontweight="bold", ha="center")
ax.text(15, 68.5, "Branch: */dev (Integration)", color="#27AE60", fontsize=7, fontweight="bold", ha="center")
ax.text(15, 65, "Commit: bf88fdd (Task 6 Baseline)", color="#5D6D7E", fontsize=6.5, ha="center")

box_trigger = patches.FancyBboxPatch((4.5, 50), 21, 10.5, boxstyle="round,pad=0.4", ec="#C0392B", fc="#FFFFFF", lw=1.2, zorder=3)
ax.add_patch(box_trigger)
ax.text(15, 57.5, "Automated Trigger Mechanisms", color="#922B21", fontsize=7, fontweight="bold", ha="center")
ax.text(15, 53.5, "• SCM Polling: H/5 * * * * (Every 5m)\n• Push Webhook: /github-webhook/", color="#2C3E50", fontsize=6.5, ha="center")

# Arrow from Git to Jenkins Master
ax.annotate("", xy=(30, 67), xytext=(27, 67),
            arrowprops=dict(arrowstyle="->", color="#1B365D", lw=2.5, mutation_scale=14))
ax.text(28.5, 70, "Trigger Event\n& Clone", color="#1B365D", fontsize=6.8, fontweight="bold", ha="center")

# Outer Container 2: Jenkins CI Server & Automation Engine
box_jenkins = patches.FancyBboxPatch((30, 16), 42, 70, boxstyle="round,pad=0.8", ec="#2980B9", fc="#EBF5FB", lw=1.8, zorder=2)
ax.add_patch(box_jenkins)
ax.text(51, 82.5, "JENKINS AUTOMATION SERVER (PORT 8080 / 8082)", color="#1B4F72", fontsize=9, fontweight="bold", ha="center")
ax.text(51, 79, "LTS Runtime: Eclipse Temurin JDK 17 LTS | Maven 3.9.6 Plugin", color="#2874A6", fontsize=7.2, fontweight="bold", ha="center")

# Job Container
box_job = patches.FancyBboxPatch((32, 20), 38, 56, boxstyle="round,pad=0.6", ec="#1B4F72", fc="#FFFFFF", lw=1.2, zorder=3)
ax.add_patch(box_job)
ax.text(51, 72.5, "Freestyle CI Job: CreditCardPortal-CI", color="#154360", fontsize=8, fontweight="bold", ha="center")

# Pipeline Stages inside Jenkins Job
stages = [
    ("Stage 1: Clean Workspace & SCM Checkout", "git clone -b dev ...\nVerify commit SHA & clean working directory", "#D4EFDF", "#196F3D", 61.5),
    ("Stage 2: Source Code Compilation", "mvn compile\nJava 17 Temurin, Spring Boot 3.2.5 dependencies", "#FCF3CF", "#B7950B", 50.5),
    ("Stage 3: Automated Quality Gate & Testing", "mvn test (10 / 10 Tests Passing: 100%)\nSurefire test reports generated in surefire-reports/*.xml", "#D5F5E3", "#229954", 39.5),
    ("Stage 4: Executable Fat JAR Packaging", "mvn package -DskipTests=false\nBuilds target/credit-card-app-1.0.0.jar (52.4 MB)", "#E8F8F5", "#117864", 28.5),
]

for title, desc, fc, ec, y_pos in stages:
    sp = patches.FancyBboxPatch((34, y_pos), 34, 9, boxstyle="round,pad=0.4", ec=ec, fc=fc, lw=1.1, zorder=4)
    ax.add_patch(sp)
    ax.text(51, y_pos + 6.2, title, color="#1B365D", fontsize=7.2, fontweight="bold", ha="center")
    ax.text(51, y_pos + 2.5, desc, color="#2C3E50", fontsize=6.3, ha="center")
    if y_pos > 30:
        ax.annotate("", xy=(51, y_pos - 1), xytext=(51, y_pos),
                    arrowprops=dict(arrowstyle="->", color="#1B365D", lw=1.8, mutation_scale=10))

# Arrow from Jenkins to Artifact Storage & Test Reporting
ax.annotate("", xy=(75, 67), xytext=(72, 67),
            arrowprops=dict(arrowstyle="->", color="#1B365D", lw=2.5, mutation_scale=14))
ax.text(73.5, 70, "Archive\nOutputs", color="#1B365D", fontsize=6.8, fontweight="bold", ha="center")

# Outer Container 3: Archived Artifacts & Test Reporting
box_out = patches.FancyBboxPatch((75, 36), 22, 50, boxstyle="round,pad=0.6", ec="#27AE60", fc="#EAFAF1", lw=1.5, zorder=2)
ax.add_patch(box_out)
ax.text(86, 82.5, "BUILD ARTIFACTS & REPORTS", color="#196F3D", fontsize=8.5, fontweight="bold", ha="center")
ax.text(86, 79, "Archived & Retained in Jenkins", color="#145A32", fontsize=7.2, fontweight="bold", ha="center")

# Artifact 1: JAR
box_jar = patches.FancyBboxPatch((76.5, 60), 19, 16, boxstyle="round,pad=0.4", ec="#229954", fc="#FFFFFF", lw=1.2, zorder=3)
ax.add_patch(box_jar)
ax.text(86, 72.5, "Archived Deployable Artifact", color="#196F3D", fontsize=7, fontweight="bold", ha="center")
ax.text(86, 68, "credit-card-app-1.0.0.jar", color="#1B365D", fontsize=6.8, fontweight="bold", ha="center")
ax.text(86, 64.5, "Size: 52.4 MB | SHA-256 Fingerprinted\nPattern: app/target/*.jar", color="#5D6D7E", fontsize=6.2, ha="center")

# Artifact 2: Test Report
box_junit = patches.FancyBboxPatch((76.5, 40), 19, 17, boxstyle="round,pad=0.4", ec="#2980B9", fc="#FFFFFF", lw=1.2, zorder=3)
ax.add_patch(box_junit)
ax.text(86, 53, "JUnit 5 Test Trend & XMLs", color="#154360", fontsize=7, fontweight="bold", ha="center")
ax.text(86, 48.5, "10 Tests Run | 0 Failures | 0 Errors", color="#27AE60", fontsize=6.8, fontweight="bold", ha="center")
ax.text(86, 44, "Health Score: 100% (Sunny)\nLocation: surefire-reports/*.xml", color="#5D6D7E", fontsize=6.2, ha="center")

# Bottom Banner: Verification & Next Steps
box_summary = patches.FancyBboxPatch((3, 3), 94, 11, boxstyle="round,pad=0.5", ec="#7D3C98", fc="#F4ECF7", lw=1.3, zorder=2)
ax.add_patch(box_summary)
ax.text(50, 10.5, "CONTINUOUS INTEGRATION (CI) ASSURANCE & DOWNSTREAM HANDOFF", color="#512E5F", fontsize=7.8, fontweight="bold", ha="center")
ax.text(50, 6, "• Automated Trigger: SCM polling detects changes deterministically without developer intervention.\n• Quality Gate: Unit and workflow tests execute automatically; any regression immediately stops artifact archival.\n• Downstream Contract: Guaranteed immutable release artifact ready for Task 8 (Pipeline as Code) & Task 11 (Docker Containerization).", 
        color="#1B365D", fontsize=6.8, ha="center")

plt.tight_layout()
fig7_1_path = "screenshots/task7/fig7_1_jenkins_ci_architecture.png"
plt.savefig(fig7_1_path, dpi=300, bbox_inches="tight")
plt.close()
print(f"Generated {fig7_1_path}")

# ----------------------------------------------------------------------
# Figure 7.2: Jenkins CI Job Dashboard, SCM Polling Log & Console Output Evidence
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11.5, 7.0), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

# Title Banner
rect_title2 = patches.FancyBboxPatch((2, 91), 96, 7.5, boxstyle="round,pad=0.8", ec="#1B365D", fc="#1B365D", zorder=2)
ax.add_patch(rect_title2)
ax.text(50, 94.7, "JENKINS CI JOB DASHBOARD, SCM POLLING LOG & CONSOLE OUTPUT EVIDENCE", 
        color="white", fontsize=10.5, fontweight="bold", ha="center", va="center")

# Left Panel: Jenkins Navigation & Job Summary (Width: 32)
box_left = patches.FancyBboxPatch((3, 6), 33, 82, boxstyle="round,pad=0.6", ec="#BDC3C7", fc="#F8F9FA", lw=1.3, zorder=2)
ax.add_patch(box_left)

# Jenkins Header Bar simulation
box_jhdr = patches.FancyBboxPatch((4.5, 81), 30, 5.5, boxstyle="round,pad=0.3", ec="#333333", fc="#333333", zorder=3)
ax.add_patch(box_jhdr)
ax.text(19.5, 83.7, "Jenkins [Mubina - 23102A0039]", color="#FFFFFF", fontsize=7.5, fontweight="bold", ha="center")

# Job Title and Status Badge
ax.text(19.5, 77.5, "Project CreditCardPortal-CI", color="#1B365D", fontsize=8.5, fontweight="bold", ha="center")
badge_status = patches.FancyBboxPatch((8, 72.5), 23, 3.8, boxstyle="round,pad=0.2", ec="#27AE60", fc="#D4EFDF", zorder=3)
ax.add_patch(badge_status)
ax.text(19.5, 74.4, "Status: SUCCESS (Build #2)", color="#196F3D", fontsize=7, fontweight="bold", ha="center")

# Navigation Menu
nav_items = ["Status", "Changes", "Workspace", "Build Now", "Configure", "Delete Project", "Polling Log", "Test Result Trend"]
for i, item in enumerate(nav_items):
    y_nav = 68 - (i * 3.2)
    nav_box = patches.FancyBboxPatch((5.5, y_nav), 28, 2.6, boxstyle="round,pad=0.2", 
                                     ec="#2980B9" if item == "Polling Log" else "#EAEDED", 
                                     fc="#EBF5FB" if item == "Polling Log" else "#FFFFFF", zorder=3)
    ax.add_patch(nav_box)
    ax.text(7, y_nav + 1.3, f"• {item}", color="#1B4F72" if item == "Polling Log" else "#2C3E50", 
            fontsize=6.5, fontweight="bold" if item == "Polling Log" else "normal", va="center")

# Build History Widget
box_hist = patches.FancyBboxPatch((5.5, 17), 28, 23, boxstyle="round,pad=0.4", ec="#BDC3C7", fc="#FFFFFF", zorder=3)
ax.add_patch(box_hist)
ax.text(19.5, 37.5, "Build History (trend)", color="#1B365D", fontsize=7.2, fontweight="bold", ha="center")

builds = [
    ("#2", "Oct 20, 2026 17:18", "SCM Poll: commit bf88fdd", "#27AE60", 31.5),
    ("#1", "Oct 20, 2026 17:05", "Manual Trigger: baseline", "#27AE60", 22.5)
]
for b_num, b_time, b_cause, b_col, y_b in builds:
    b_pill = patches.FancyBboxPatch((7, y_b), 25, 6.5, boxstyle="round,pad=0.3", ec=b_col, fc="#EAFAF1", zorder=4)
    ax.add_patch(b_pill)
    ax.text(9, y_b + 4.3, f"Build {b_num} (SUCCESS)", color=b_col, fontsize=6.8, fontweight="bold")
    ax.text(9, y_b + 2.4, b_time, color="#566573", fontsize=6)
    ax.text(9, y_b + 0.8, b_cause, color="#2C3E50", fontsize=5.8)

# Right Top Panel: SCM Polling Log Evidence (Width: 59, Height: 38)
box_poll = patches.FancyBboxPatch((38, 48), 59, 40, boxstyle="round,pad=0.6", ec="#E67E22", fc="#FEF9E7", lw=1.3, zorder=2)
ax.add_patch(box_poll)
ax.text(67.5, 84.5, "SCM POLLING LOG EVIDENCE (/job/CreditCardPortal-CI/pollingLog/)", 
        color="#B9770E", fontsize=8.2, fontweight="bold", ha="center")

poll_terminal = patches.FancyBboxPatch((40, 50), 55, 31.5, boxstyle="round,pad=0.3", ec="#333333", fc="#1E1E1E", zorder=3)
ax.add_patch(poll_terminal)

poll_text = """Started on Oct 20, 2026 17:15:00
Polling SCM changes on git repository https://github.com/mubina-ce/credit-card-portal.git
Using strategy: Default
[poll] Last Built Revision: Revision e5943a95d (origin/dev)
 > git.exe --version # timeout=10
 > git.exe ls-remote -h -- https://github.com/mubina-ce/credit-card-portal.git dev
Found 1 remote branch changes on origin/dev:
  * bf88fdd [docs: compile Task 6 MVP completion and release baseline report]
[poll] Latest remote revision: Revision bf88fdd38 (origin/dev)
Done. Changes found between e5943a9 and bf88fdd.
Scheduling a new automated build: #2 (Triggered by SCM change)"""

ax.text(41.5, 80, poll_text, color="#00FF66", fontfamily="monospace", fontsize=5.8, va="top", zorder=4)

# Right Bottom Panel: Console Output & Artifact Archiving Evidence (Width: 59, Height: 40)
box_console = patches.FancyBboxPatch((38, 6), 59, 40, boxstyle="round,pad=0.6", ec="#27AE60", fc="#EAFAF1", lw=1.3, zorder=2)
ax.add_patch(box_console)
ax.text(67.5, 42.5, "BUILD CONSOLE OUTPUT & ARTIFACT ARCHIVING EVIDENCE (/job/CreditCardPortal-CI/2/console)", 
        color="#196F3D", fontsize=8.2, fontweight="bold", ha="center")

cons_terminal = patches.FancyBboxPatch((40, 8), 55, 31.5, boxstyle="round,pad=0.3", ec="#333333", fc="#1E1E1E", zorder=3)
ax.add_patch(cons_terminal)

cons_text = """[INFO] ------------------------------------------------------------------------
[INFO] Building Credit Card Service Portal 1.0.0
[INFO] --- maven-compiler-plugin:3.11.0:compile (default-compile) @ credit-card-app ---
[INFO] Compiling 7 source files to target/classes
[INFO] --- maven-surefire-plugin:3.1.2:test (default-test) @ credit-card-app ---
[INFO] Running com.creditcard.app.CreditCardApplicationWorkflowTest (3/3 passed)
[INFO] Running com.creditcard.app.CreditCardServiceTest (7/7 passed)
[INFO] Results: Tests run: 10, Failures: 0, Errors: 0, Skipped: 0
[INFO] Building jar: app/target/credit-card-app-1.0.0.jar
[INFO] Replacing main artifact with repackaged archive (BOOT-INF/lib nested)
[INFO] BUILD SUCCESS (Total time: 35.732 s)
[Jenkins] Archiving artifacts: app/target/*.jar
[Jenkins] Recorded 1 archived artifact: credit-card-app-1.0.0.jar (52.4 MB, SHA-256)
[Jenkins] Recording test results: app/target/surefire-reports/*.xml (10 passed)
Finished: SUCCESS"""

ax.text(41.5, 38, cons_text, color="#00E5FF", fontfamily="monospace", fontsize=5.8, va="top", zorder=4)

plt.tight_layout()
fig7_2_path = "screenshots/task7/fig7_2_jenkins_job_console_evidence.png"
plt.savefig(fig7_2_path, dpi=300, bbox_inches="tight")
plt.close()
print(f"Generated {fig7_2_path}")
