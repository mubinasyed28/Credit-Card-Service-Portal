import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

os.makedirs("screenshots/task2", exist_ok=True)

# ----------------------------------------------------------------------
# Figure 2.1: Agile Kanban Sprint Board & Task Progression State
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 6.2), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

# Title Banner
rect_title = patches.FancyBboxPatch((2, 90), 96, 8, boxstyle="round,pad=1", ec="#1B365D", fc="#1B365D", zorder=2)
ax.add_patch(rect_title)
ax.text(50, 94, "CREDIT CARD SERVICE PORTAL — 15-TASK AGILE KANBAN SPRINT BOARD", 
        color="white", fontsize=11, fontweight="bold", ha="center", va="center")

# Define Kanban Columns
columns = [
    ("BACKLOG\n(WIP: ∞)", "#EAEDED", "#5D6D7E", 3, 17),
    ("TO DO / SPRINT READY\n(WIP: 4)", "#EBF5FB", "#2980B9", 22.5, 17),
    ("IN PROGRESS\n(WIP: 3)", "#FEF9E7", "#D4AC0D", 42, 17),
    ("SELENIUM QA GATE\n(WIP: 2)", "#F4ECF7", "#8E44AD", 61.5, 17),
    ("DONE / DEPLOYED\n(WIP: 15)", "#EAFAF1", "#27AE60", 81, 17)
]

for col_title, bg_col, border_col, x, w in columns:
    # Column background card
    card = patches.FancyBboxPatch((x, 6), w, 81, boxstyle="round,pad=0.8", ec=border_col, fc=bg_col, lw=1.5, zorder=1)
    ax.add_patch(card)
    
    # Column header
    header = patches.FancyBboxPatch((x, 79), w, 7.5, boxstyle="round,pad=0.5", ec=border_col, fc=border_col, zorder=2)
    ax.add_patch(header)
    ax.text(x + w/2, 82.7, col_title, color="white", fontsize=8.5, fontweight="bold", ha="center", va="center")

# Populate Cards into Columns
# Column 1: Backlog Items
backlog_cards = [
    ("Task 13: Ansible Config", "PBI-13 | 5 pts\nHosts & Playbook", 70),
    ("Task 14: Idempotency", "PBI-14 | 5 pts\nAnsible Reliability", 55),
    ("Task 15: Final Viva", "PBI-15 | 8 pts\nEnd-to-End Demo", 40)
]
for title, desc, y in backlog_cards:
    c_box = patches.FancyBboxPatch((4, y), 15, 12, boxstyle="round,pad=0.4", ec="#BDC3C7", fc="white", lw=1, zorder=3)
    ax.add_patch(c_box)
    ax.text(11.5, y + 8.5, title, fontsize=7.5, fontweight="bold", color="#2C3E50", ha="center")
    ax.text(11.5, y + 3.8, desc, fontsize=7.0, color="#7F8C8D", ha="center")

# Column 2: To Do / Sprint Ready
todo_cards = [
    ("Task 9: Selenium Suite", "PBI-09 | 8 pts\n4 Critical Journeys", 70),
    ("Task 10: Jenkins Gate", "PBI-10 | 5 pts\nFailure Abort Check", 55),
    ("Task 11: Docker Build", "PBI-11 | 5 pts\nMulti-Stage Image", 40),
    ("Task 12: Docker CD", "PBI-12 | 5 pts\nContainer Deploy", 25)
]
for title, desc, y in todo_cards:
    c_box = patches.FancyBboxPatch((23.5, y), 15, 12, boxstyle="round,pad=0.4", ec="#85C1E9", fc="white", lw=1, zorder=3)
    ax.add_patch(c_box)
    ax.text(31, y + 8.5, title, fontsize=7.5, fontweight="bold", color="#1B4F72", ha="center")
    ax.text(31, y + 3.8, desc, fontsize=7.0, color="#5499C7", ha="center")

# Column 3: In Progress
in_prog_cards = [
    ("Task 6: MVP Release", "PBI-06 | 8 pts\nMerge Conflict & Tag", 70),
    ("Task 7: Jenkins CI", "PBI-07 | 5 pts\nMaven Build Trigger", 55),
    ("Task 8: Jenkinsfile", "PBI-08 | 5 pts\nPipeline as Code", 40)
]
for title, desc, y in in_prog_cards:
    c_box = patches.FancyBboxPatch((43, y), 15, 12, boxstyle="round,pad=0.4", ec="#F9E79F", fc="white", lw=1, zorder=3)
    ax.add_patch(c_box)
    ax.text(50.5, y + 8.5, title, fontsize=7.5, fontweight="bold", color="#7D6608", ha="center")
    ax.text(50.5, y + 3.8, desc, fontsize=7.0, color="#B7950B", ha="center")

# Column 4: QA Gate
qa_cards = [
    ("Task 5: Card Apply", "PBI-05 | 5 pts\nPR & Code Review", 70),
    ("Task 4: Git Init", "PBI-04 | 3 pts\nRepo & Branch Rule", 55)
]
for title, desc, y in qa_cards:
    c_box = patches.FancyBboxPatch((62.5, y), 15, 12, boxstyle="round,pad=0.4", ec="#D7BDE2", fc="white", lw=1, zorder=3)
    ax.add_patch(c_box)
    ax.text(70, y + 8.5, title, fontsize=7.5, fontweight="bold", color="#512E5F", ha="center")
    ax.text(70, y + 3.8, desc, fontsize=7.0, color="#8E44AD", ha="center")

# Column 5: Done / Deployed
done_cards = [
    ("Task 1: Scope Freeze", "PBI-01 | 3 pts\nProblem & Scope", 70),
    ("Task 2: Agile Workflow", "PBI-02 | 5 pts\nBacklog & DoD", 55),
    ("Task 3: Architecture", "PBI-03 | 5 pts\nSpring Boot Setup", 40)
]
for title, desc, y in done_cards:
    c_box = patches.FancyBboxPatch((82, y), 15, 12, boxstyle="round,pad=0.4", ec="#A9DFBF", fc="white", lw=1, zorder=3)
    ax.add_patch(c_box)
    ax.text(89.5, y + 8.5, title, fontsize=7.5, fontweight="bold", color="#145A32", ha="center")
    ax.text(89.5, y + 3.8, desc, fontsize=7.0, color="#27AE60", ha="center")

plt.tight_layout()
fig1_path = os.path.abspath("screenshots/task2/fig2_1_kanban_board.png")
plt.savefig(fig1_path, bbox_inches="tight", dpi=300)
plt.close()
print(f"Figure 2.1 saved to: {fig1_path}")

# ----------------------------------------------------------------------
# Figure 2.2: End-to-End DevOps Lifecycle Workflow Loop
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 6.2), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

# Title Banner
rect_title2 = patches.FancyBboxPatch((2, 90), 96, 8, boxstyle="round,pad=1", ec="#1B365D", fc="#1B365D", zorder=2)
ax.add_patch(rect_title2)
ax.text(50, 94, "CREDIT CARD SERVICE PORTAL — END-TO-END DEVOPS CONTINUOUS LIFECYCLE", 
        color="white", fontsize=11, fontweight="bold", ha="center", va="center")

# Define 8 DevOps Lifecycle Stages in an Infinity / Flow Layout
stages = [
    ("1. PLAN", "Agile User Stories\nProduct Backlog\nTasks 1 & 2", 12, 66, "#2980B9", "#EBF5FB"),
    ("2. CODE", "Spring Boot 3.x\nGit & Feature Branch\nTasks 3, 4, 5, 6", 36, 66, "#16A085", "#E8F8F5"),
    ("3. BUILD", "Maven Wrapper\nCompile & Package\nTasks 7 & 8", 60, 66, "#D35400", "#FBEEE6"),
    ("4. TEST GATE", "Selenium WebDriver\nHeadless Regression\nTasks 9 & 10", 84, 66, "#C0392B", "#FDEDEC"),
    ("5. RELEASE", "Docker Multi-stage\nVersioned Image Tag\nTask 11 & 12", 84, 24, "#8E44AD", "#F4ECF7"),
    ("6. DEPLOY", "Jenkins Pipeline\nContainer Port 8080\nTask 12", 60, 24, "#27AE60", "#EAFAF1"),
    ("7. CONFIGURE", "Ansible Playbook\nIdempotent Nodes\nTasks 13 & 14", 36, 24, "#D4AC0D", "#FEF9E7"),
    ("8. MONITOR", "Actuator /health\nPrometheus & Logs\nTask 15", 12, 24, "#2C3E50", "#EAECEE")
]

for stage_name, stage_desc, x, y, border_col, bg_col in stages:
    box = patches.FancyBboxPatch((x - 10, y - 10), 20, 20, boxstyle="round,pad=0.8", ec=border_col, fc=bg_col, lw=2, zorder=2)
    ax.add_patch(box)
    
    header = patches.FancyBboxPatch((x - 10, y + 3.5), 20, 6.5, boxstyle="round,pad=0.3", ec=border_col, fc=border_col, zorder=3)
    ax.add_patch(header)
    ax.text(x, y + 6.7, stage_name, color="white", fontsize=9, fontweight="bold", ha="center", va="center")
    ax.text(x, y - 4, stage_desc, color="#2C3E50", fontsize=7.8, ha="center", va="center")

# Arrows Connecting the Loop
# Top row (Left to Right: 1 -> 2 -> 3 -> 4)
ax.annotate("", xy=(25, 66), xytext=(23, 66), arrowprops=dict(arrowstyle="->", color="#2C3E50", lw=2.5, mutation_scale=15))
ax.annotate("", xy=(49, 66), xytext=(47, 66), arrowprops=dict(arrowstyle="->", color="#2C3E50", lw=2.5, mutation_scale=15))
ax.annotate("", xy=(73, 66), xytext=(71, 66), arrowprops=dict(arrowstyle="->", color="#2C3E50", lw=2.5, mutation_scale=15))

# Right Column (Top to Bottom: 4 -> 5)
ax.annotate("", xy=(84, 35), xytext=(84, 55), arrowprops=dict(arrowstyle="->", color="#C0392B", lw=2.5, mutation_scale=15))
ax.text(88, 45, "Quality Gate\nPass", color="#C0392B", fontsize=7.5, fontweight="bold", ha="left", va="center")

# Bottom row (Right to Left: 5 -> 6 -> 7 -> 8)
ax.annotate("", xy=(73, 24), xytext=(75, 24), arrowprops=dict(arrowstyle="->", color="#2C3E50", lw=2.5, mutation_scale=15))
ax.annotate("", xy=(49, 24), xytext=(51, 24), arrowprops=dict(arrowstyle="->", color="#2C3E50", lw=2.5, mutation_scale=15))
ax.annotate("", xy=(25, 24), xytext=(27, 24), arrowprops=dict(arrowstyle="->", color="#2C3E50", lw=2.5, mutation_scale=15))

# Left Column (Bottom to Top: 8 -> 1)
ax.annotate("", xy=(12, 55), xytext=(12, 35), arrowprops=dict(arrowstyle="->", color="#2C3E50", lw=2.5, mutation_scale=15))
ax.text(6, 45, "Continuous\nFeedback", color="#1B4F72", fontsize=7.5, fontweight="bold", ha="right", va="center")

# Central Badge: Core Quality Standard
center_badge = patches.FancyBboxPatch((28, 43), 44, 9, boxstyle="round,pad=0.8", ec="#C0392B", fc="#FDEDEC", lw=1.5, zorder=2)
ax.add_patch(center_badge)
ax.text(50, 47.5, "CORE QUALITY GATE: SELENIUM TEST AUTOMATION IN JENKINS", 
        color="#922B21", fontsize=8.2, fontweight="bold", ha="center", va="center")
ax.text(50, 44.5, "Any Selenium assertion failure immediately aborts Docker & Deployment stages", 
        color="#78281F", fontsize=7.2, style="italic", ha="center", va="center")

plt.tight_layout()
fig2_path = os.path.abspath("screenshots/task2/fig2_2_devops_lifecycle.png")
plt.savefig(fig2_path, bbox_inches="tight", dpi=300)
plt.close()
print(f"Figure 2.2 saved to: {fig2_path}")
