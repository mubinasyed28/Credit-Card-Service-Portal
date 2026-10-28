import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

os.makedirs("screenshots/task1", exist_ok=True)

# -------------------------------------------------------------
# Figure 1.1: Stakeholder Ecosystem & User Interaction Flow
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5.8), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

# Title Banner
rect_title = patches.FancyBboxPatch((2, 88), 96, 10, boxstyle="round,pad=1", ec="#1B365D", fc="#1B365D", zorder=2)
ax.add_patch(rect_title)
ax.text(50, 93, "CREDIT CARD SERVICE PORTAL (CCSP) — STAKEHOLDER & ACTOR ECOSYSTEM", 
        color="white", fontsize=11, fontweight="bold", ha="center", va="center")

# Central System Box
rect_core = patches.FancyBboxPatch((35, 30), 30, 42, boxstyle="round,pad=1.5", ec="#2C3E50", fc="#EBF5FB", lw=2, zorder=2)
ax.add_patch(rect_core)
ax.text(50, 67, "CREDIT CARD SERVICE PORTAL", color="#1B365D", fontsize=11, fontweight="bold", ha="center")
ax.text(50, 62, "(Spring Boot 3.x + H2 In-Memory)", color="#5D6D7E", fontsize=9, ha="center")

# Internal modules in central box
modules = [
    (38, 48, 24, 8, "Card Application & KYC Engine", "#D4E6F1"),
    (38, 37, 24, 8, "Lifecycle & Status Workflow", "#D4E6F1"),
    (38, 26, 24, 8, "KPI Metrics & Actuator Health", "#D4E6F1"),
]
for (x, y, w, h, label, col) in modules:
    r = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.5", ec="#2980B9", fc=col, lw=1, zorder=3)
    ax.add_patch(r)
    ax.text(x + w/2, y + h/2, label, color="#1B4F72", fontsize=8.5, fontweight="bold", ha="center", va="center")

# Left Column: Business & Customer Stakeholders
# 1. Retail Cardholder / Applicant
r_user1 = patches.FancyBboxPatch((3, 58), 24, 18, boxstyle="round,pad=1", ec="#27AE60", fc="#EAFAF1", lw=1.5, zorder=2)
ax.add_patch(r_user1)
ax.text(15, 72, "Retail Card Applicant", color="#196F3D", fontsize=9.5, fontweight="bold", ha="center")
ax.text(15, 66, "• Apply for Credit Card\n• Track Status & Limit\n• Self-Service Inquiries", 
        color="#2C3E50", fontsize=8, ha="center", va="center")

# 2. Branch Officer / Credit Analyst
r_user2 = patches.FancyBboxPatch((3, 20), 24, 18, boxstyle="round,pad=1", ec="#2980B9", fc="#EAF2F8", lw=1.5, zorder=2)
ax.add_patch(r_user2)
ax.text(15, 34, "Credit Operations Analyst", color="#1B4F72", fontsize=9.5, fontweight="bold", ha="center")
ax.text(15, 28, "• Review Application Docs\n• Approve / Reject Cards\n• Set Credit Limits", 
        color="#2C3E50", fontsize=8, ha="center", va="center")

# Right Column: Technical & Engineering Stakeholders
# 3. QA Automation Engineer
r_user3 = patches.FancyBboxPatch((73, 58), 24, 18, boxstyle="round,pad=1", ec="#E67E22", fc="#FEF5E7", lw=1.5, zorder=2)
ax.add_patch(r_user3)
ax.text(85, 72, "QA Automation Engineer", color="#B9770E", fontsize=9.5, fontweight="bold", ha="center")
ax.text(85, 66, "• Selenium Test Suites\n• Regression User Journeys\n• Quality Gate Enforcement", 
        color="#2C3E50", fontsize=8, ha="center", va="center")

# 4. DevOps & Platform Engineer
r_user4 = patches.FancyBboxPatch((73, 20), 24, 18, boxstyle="round,pad=1", ec="#8E44AD", fc="#F4ECF7", lw=1.5, zorder=2)
ax.add_patch(r_user4)
ax.text(85, 34, "DevOps / SRE Engineer", color="#6C3483", fontsize=9.5, fontweight="bold", ha="center")
ax.text(85, 28, "• CI/CD Pipeline (Jenkins)\n• Docker Containers\n• Ansible Idempotency", 
        color="#2C3E50", fontsize=8, ha="center", va="center")

# Arrows Left to Center
ax.annotate("", xy=(34, 66), xytext=(28, 66),
            arrowprops=dict(arrowstyle="->", color="#27AE60", lw=2, mutation_scale=15))
ax.text(31, 68, "Apply", fontsize=7.5, color="#196F3D", fontweight="bold", ha="center")

ax.annotate("", xy=(34, 30), xytext=(28, 30),
            arrowprops=dict(arrowstyle="->", color="#2980B9", lw=2, mutation_scale=15))
ax.text(31, 32, "Review", fontsize=7.5, color="#1B4F72", fontweight="bold", ha="center")

# Arrows Right to Center
ax.annotate("", xy=(66, 66), xytext=(72, 66),
            arrowprops=dict(arrowstyle="->", color="#E67E22", lw=2, mutation_scale=15))
ax.text(69, 68, "Validate", fontsize=7.5, color="#B9770E", fontweight="bold", ha="center")

ax.annotate("", xy=(66, 30), xytext=(72, 30),
            arrowprops=dict(arrowstyle="->", color="#8E44AD", lw=2, mutation_scale=15))
ax.text(69, 32, "Deploy", fontsize=7.5, color="#6C3483", fontweight="bold", ha="center")

# Bottom Banner: Core Quality & Regulatory Pillars
rect_bottom = patches.FancyBboxPatch((10, 3), 80, 8, boxstyle="round,pad=0.8", ec="#BDC3C7", fc="#F8F9F9", lw=1, zorder=2)
ax.add_patch(rect_bottom)
ax.text(50, 7, "Regulatory & Quality Standards: RBI Data Localization • PCI-DSS Security Guidelines • ISO 27001 • OWASP Top 10", 
        color="#566573", fontsize=8, ha="center", va="center", style="italic")

plt.tight_layout()
fig1_path = os.path.abspath("screenshots/task1/fig1_1_stakeholder_ecosystem.png")
plt.savefig(fig1_path, bbox_inches="tight", dpi=300)
plt.close()
print(f"Figure 1.1 saved to: {fig1_path}")

# -------------------------------------------------------------
# Figure 1.2: 15-Task DevOps Implementation Roadmap
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10.5, 6.2), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

# Title
rect_title2 = patches.FancyBboxPatch((2, 90), 96, 8, boxstyle="round,pad=1", ec="#1B365D", fc="#1B365D", zorder=2)
ax.add_patch(rect_title2)
ax.text(50, 94, "15-TASK DEVOPS MVP ROADMAP & CONTINUOUS TESTING DELIVERY PIPELINE", 
        color="white", fontsize=10.5, fontweight="bold", ha="center", va="center")

# Define 7 Phases
phases = [
    ("Phase 1: Inception & Planning", 
     [("Task 1: Problem Definition & Scope", "#2980B9"),
      ("Task 2: Agile Planning & Workflow", "#2980B9")], 
     "#EAF2F8", "#1B4F72", 72),
    
    ("Phase 2: Architecture & Version Control", 
     [("Task 3: Architecture & Tech Setup", "#16A085"),
      ("Task 4: Git & Repo Initialization", "#16A085"),
      ("Task 5: Feature Branching Workflow", "#16A085"),
      ("Task 6: MVP Release & Merge Conflict", "#16A085")], 
     "#E8F8F5", "#0E6655", 54),
    
    ("Phase 3: CI/CD & Pipeline as Code", 
     [("Task 7: Jenkins CI Build Job", "#D35400"),
      ("Task 8: Jenkinsfile Pipeline as Code", "#D35400")], 
     "#FBEEE6", "#935116", 36),
    
    ("Phase 4: Selenium Automated Testing Gates", 
     [("Task 9: Selenium Test Suite (4 Journeys)", "#8E44AD"),
      ("Task 10: Jenkins Test Quality Gate", "#8E44AD")], 
     "#F4ECF7", "#5B2C6F", 18),
    
    ("Phase 5: Docker Containerization", 
     [("Task 11: Multi-Stage Docker Build", "#27AE60"),
      ("Task 12: Continuous Docker CD Pipeline", "#27AE60")], 
     "#EAFAF1", "#1E8449", 0)
]

# We will display them as 5 horizontal stage blocks with tasks inside
y_positions = [74, 57, 40, 23, 6]
stage_height = 14

for idx, (title, task_list, bg_color, border_color, _) in enumerate(phases):
    y = y_positions[idx]
    # Background card
    card = patches.FancyBboxPatch((2, y), 96, stage_height, boxstyle="round,pad=0.8", ec=border_color, fc=bg_color, lw=1.2, zorder=1)
    ax.add_patch(card)
    
    # Phase Title Banner on left
    title_box = patches.FancyBboxPatch((3, y + 1), 26, stage_height - 2, boxstyle="round,pad=0.5", ec=border_color, fc=border_color, zorder=2)
    ax.add_patch(title_box)
    ax.text(16, y + stage_height/2, title, color="white", fontsize=8.5, fontweight="bold", ha="center", va="center", wrap=True)
    
    # Task badges
    n_tasks = len(task_list)
    available_width = 66
    spacing = 1.0
    task_width = (available_width - (n_tasks - 1) * spacing) / n_tasks
    
    for t_idx, (t_name, t_col) in enumerate(task_list):
        t_x = 31 + t_idx * (task_width + spacing)
        t_box = patches.FancyBboxPatch((t_x, y + 2), task_width, stage_height - 4, boxstyle="round,pad=0.4", ec=border_color, fc="white", lw=1, zorder=2)
        ax.add_patch(t_box)
        ax.text(t_x + task_width/2, y + stage_height/2, t_name, color="#2C3E50", fontsize=7.5, fontweight="bold", ha="center", va="center")

plt.tight_layout()
fig2_path = os.path.abspath("screenshots/task1/fig1_2_devops_roadmap.png")
plt.savefig(fig2_path, bbox_inches="tight", dpi=300)
plt.close()
print(f"Figure 1.2 saved to: {fig2_path}")
