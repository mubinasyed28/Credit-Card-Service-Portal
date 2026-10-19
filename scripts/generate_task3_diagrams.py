import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

os.makedirs("screenshots/task3", exist_ok=True)

# ----------------------------------------------------------------------
# Figure 3.1: Use-Case Diagram for Credit Card Service Portal
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 7.0), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

# Title Banner
rect_title = patches.FancyBboxPatch((2, 92), 96, 7, boxstyle="round,pad=1", ec="#1B365D", fc="#1B365D", zorder=2)
ax.add_patch(rect_title)
ax.text(50, 95.5, "CREDIT CARD SERVICE PORTAL (CCSP) — SYSTEM USE-CASE MODEL", 
        color="white", fontsize=11, fontweight="bold", ha="center", va="center")

# System Boundary Rectangle
rect_sys = patches.FancyBboxPatch((28, 4), 44, 85, boxstyle="round,pad=1.5", ec="#2C3E50", fc="#F8FBFD", lw=2, ls="--", zorder=1)
ax.add_patch(rect_sys)
ax.text(50, 86, "SYSTEM BOUNDARY: CREDIT CARD SERVICE PORTAL", color="#1B365D", fontsize=10, fontweight="bold", ha="center")

# Left Column Actors (Human Users)
# Actor 1: Retail Card Applicant
ax.plot([8, 8], [76, 80], color="#27AE60", lw=2) # body
ax.plot([6, 10], [78, 78], color="#27AE60", lw=2) # arms
ax.plot([6, 8, 10], [73, 76, 73], color="#27AE60", lw=2) # legs
circle1 = plt.Circle((8, 81), 1.8, color="#27AE60", ec="#196F3D", lw=1.5, zorder=3)
ax.add_patch(circle1)
ax.text(8, 70, "Retail Card\nApplicant", color="#196F3D", fontsize=8.5, fontweight="bold", ha="center")

# Actor 2: Active Cardholder
ax.plot([8, 8], [51, 55], color="#2980B9", lw=2)
ax.plot([6, 10], [53, 53], color="#2980B9", lw=2)
ax.plot([6, 8, 10], [48, 51, 48], color="#2980B9", lw=2)
circle2 = plt.Circle((8, 56), 1.8, color="#2980B9", ec="#1B4F72", lw=1.5, zorder=3)
ax.add_patch(circle2)
ax.text(8, 45, "Active\nCardholder", color="#1B4F72", fontsize=8.5, fontweight="bold", ha="center")

# Actor 3: Credit Risk Officer
ax.plot([8, 8], [26, 30], color="#D35400", lw=2)
ax.plot([6, 10], [28, 28], color="#D35400", lw=2)
ax.plot([6, 8, 10], [23, 26, 23], color="#D35400", lw=2)
circle3 = plt.Circle((8, 31), 1.8, color="#D35400", ec="#A04000", lw=1.5, zorder=3)
ax.add_patch(circle3)
ax.text(8, 20, "Credit Risk\nOfficer", color="#A04000", fontsize=8.5, fontweight="bold", ha="center")

# Right Column Actors (Technical & Operations)
# Actor 4: Branch Relationship Mgr
ax.plot([92, 92], [66, 70], color="#8E44AD", lw=2)
ax.plot([90, 94], [68, 68], color="#8E44AD", lw=2)
ax.plot([90, 92, 94], [63, 66, 63], color="#8E44AD", lw=2)
circle4 = plt.Circle((92, 71), 1.8, color="#8E44AD", ec="#6C3483", lw=1.5, zorder=3)
ax.add_patch(circle4)
ax.text(92, 60, "Branch\nManager", color="#6C3483", fontsize=8.5, fontweight="bold", ha="center")

# Actor 5: DevOps / QA Engineer
ax.plot([92, 92], [36, 40], color="#C0392B", lw=2)
ax.plot([90, 94], [38, 38], color="#C0392B", lw=2)
ax.plot([90, 92, 94], [33, 36, 33], color="#C0392B", lw=2)
circle5 = plt.Circle((92, 41), 1.8, color="#C0392B", ec="#922B21", lw=1.5, zorder=3)
ax.add_patch(circle5)
ax.text(92, 30, "DevOps / QA\nEngineer", color="#922B21", fontsize=8.5, fontweight="bold", ha="center")

# Use Cases (Ellipses in central boundary)
use_cases = [
    ("UC-01: Apply for Credit Card & Limit", 50, 78, "#D4E6F1", "#2980B9"),
    ("UC-02: Query & Search Directory (/cards)", 50, 66, "#D5F5E3", "#27AE60"),
    ("UC-03: Evaluate & Approve/Reject Cards", 50, 54, "#FCF3CF", "#D4AC0D"),
    ("UC-04: Emergency Security Freeze / Unfreeze", 50, 42, "#FADBD8", "#E74C3C"),
    ("UC-05: View Summary KPI Dashboard (/)", 50, 30, "#E8DAEF", "#8E44AD"),
    ("UC-06: Probe Health Telemetry (/actuator)", 50, 18, "#D0ECE7", "#16A085"),
    ("UC-07: Execute Headless Selenium Quality Gate", 50, 7.5, "#EDBB99", "#DC7633")
]

for title, cx, cy, fc, ec in use_cases:
    ellipse = patches.Ellipse((cx, cy), 36, 7.5, ec=ec, fc=fc, lw=1.5, zorder=2)
    ax.add_patch(ellipse)
    ax.text(cx, cy, title, color="#2C3E50", fontsize=7.8, fontweight="bold", ha="center", va="center")

# Association Lines (Solid)
# Applicant -> UC-01
ax.annotate("", xy=(32, 78), xytext=(12, 76), arrowprops=dict(arrowstyle="-", color="#27AE60", lw=1.5))
# Applicant -> UC-02
ax.annotate("", xy=(32, 67), xytext=(12, 75), arrowprops=dict(arrowstyle="-", color="#27AE60", lw=1.2, ls=":"))
# Cardholder -> UC-02
ax.annotate("", xy=(32, 65), xytext=(12, 53), arrowprops=dict(arrowstyle="-", color="#2980B9", lw=1.5))
# Cardholder -> UC-04
ax.annotate("", xy=(32, 44), xytext=(12, 51), arrowprops=dict(arrowstyle="-", color="#2980B9", lw=1.5))
# Officer -> UC-02
ax.annotate("", xy=(32, 63), xytext=(12, 29), arrowprops=dict(arrowstyle="-", color="#D35400", lw=1.2))
# Officer -> UC-03
ax.annotate("", xy=(32, 54), xytext=(12, 28), arrowprops=dict(arrowstyle="-", color="#D35400", lw=1.5))
# Officer -> UC-04
ax.annotate("", xy=(32, 42), xytext=(12, 27), arrowprops=dict(arrowstyle="-", color="#D35400", lw=1.2))

# Branch Manager -> UC-02
ax.annotate("", xy=(68, 66), xytext=(88, 66), arrowprops=dict(arrowstyle="-", color="#8E44AD", lw=1.5))
# Branch Manager -> UC-05
ax.annotate("", xy=(68, 31), xytext=(88, 64), arrowprops=dict(arrowstyle="-", color="#8E44AD", lw=1.5))

# DevOps Engineer -> UC-06
ax.annotate("", xy=(68, 19), xytext=(88, 38), arrowprops=dict(arrowstyle="-", color="#922B21", lw=1.5))
# DevOps Engineer -> UC-07
ax.annotate("", xy=(68, 9), xytext=(88, 36), arrowprops=dict(arrowstyle="-", color="#922B21", lw=1.5))

plt.tight_layout()
fig1_path = os.path.abspath("screenshots/task3/fig3_1_usecase_diagram.png")
plt.savefig(fig1_path, bbox_inches="tight", dpi=300)
plt.close()
print(f"Figure 3.1 saved to: {fig1_path}")

# ----------------------------------------------------------------------
# Figure 3.2: 4-Tier Monolithic Web Architecture Diagram
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 7.2), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

# Title Banner
rect_title2 = patches.FancyBboxPatch((2, 92), 96, 7, boxstyle="round,pad=1", ec="#1B365D", fc="#1B365D", zorder=2)
ax.add_patch(rect_title2)
ax.text(50, 95.5, "CREDIT CARD SERVICE PORTAL — 4-TIER MONOLITHIC WEB ARCHITECTURE", 
        color="white", fontsize=11, fontweight="bold", ha="center", va="center")

# 4 Horizontal Tiers
tiers = [
    ("TIER 1: PRESENTATION & CLIENT BROWSER LAYER", 
     [("Thymeleaf Server Templates\n(cards.html, apply.html)", 16, 73),
      ("Bootstrap 5 Responsive UI\n(Cards, Badges, Modals)", 50, 73),
      ("Selenium Locator Contract\n(Unique id & class DOM)", 84, 73)],
     "#EBF5FB", "#2980B9", 70),
    
    ("TIER 2: CONTROLLER & WEB ROUTING LAYER", 
     [("CreditCardController\n(@Controller Spring MVC)", 16, 52),
      ("Input Validation Gates\n(@Valid, BindingResult)", 50, 52),
      ("Actuator Health Endpoint\n(GET /actuator/health)", 84, 52)],
     "#E8F8F5", "#16A085", 49),
    
    ("TIER 3: BUSINESS SERVICE & WORKFLOW ENGINE", 
     [("CreditCardService\n(@Service Business Logic)", 20, 31),
      ("Lifecycle State Machine\n(PENDING -> ACTIVE -> BLOCKED)", 54, 31),
      ("KPI Analytics Calculator\n(Dynamic Counter Aggregation)", 82, 31)],
     "#FEF9E7", "#D4AC0D", 28),
    
    ("TIER 4: DATA ACCESS & IN-MEMORY PERSISTENCE", 
     [("Spring Data JPA Repository\n(CreditCardRepository)", 25, 10),
      ("Hibernate ORM 6.x\n(Auto Schema DDL)", 54, 10),
      ("Embedded In-Memory H2 DB\n(jdbc:h2:mem:ccsp_db)", 82, 10)],
     "#F4ECF7", "#8E44AD", 7)
]

for tier_title, comps, bg_col, border_col, y in tiers:
    # Outer tier box
    tier_box = patches.FancyBboxPatch((3, y), 94, 18, boxstyle="round,pad=0.8", ec=border_col, fc=bg_col, lw=1.5, zorder=1)
    ax.add_patch(tier_box)
    
    # Tier Title Label
    t_label = patches.FancyBboxPatch((4, y + 14), 48, 3.8, boxstyle="round,pad=0.2", ec=border_col, fc=border_col, zorder=2)
    ax.add_patch(t_label)
    ax.text(28, y + 15.9, tier_title, color="white", fontsize=7.8, fontweight="bold", ha="center", va="center")
    
    # Component badges inside tier
    for c_name, cx, cy in comps:
        c_box = patches.FancyBboxPatch((cx - 13, cy - 3.8), 26, 7.6, boxstyle="round,pad=0.4", ec=border_col, fc="white", lw=1.2, zorder=3)
        ax.add_patch(c_box)
        ax.text(cx, cy, c_name, color="#2C3E50", fontsize=7.2, fontweight="bold", ha="center", va="center")

# Inter-tier communication vertical arrows
ax.annotate("", xy=(30, 68), xytext=(30, 69), arrowprops=dict(arrowstyle="<->", color="#1B365D", lw=2))
ax.annotate("", xy=(50, 47), xytext=(50, 48), arrowprops=dict(arrowstyle="<->", color="#1B365D", lw=2))
ax.annotate("", xy=(50, 26), xytext=(50, 27), arrowprops=dict(arrowstyle="<->", color="#1B365D", lw=2))

# Supporting Cross-Cutting Envelope on right
rect_env = patches.FancyBboxPatch((86, 2), 12, 65, boxstyle="round,pad=0.5", ec="#C0392B", fc="#FDEDEC", lw=1.2, ls=":", zorder=1)
ax.add_patch(rect_env)
ax.text(92, 34.5, "RUNTIME ENVELOPE\n\nEmbedded Tomcat 10\nPort 8080\n\nJVM Temurin 17\nHeap < 512MB\n\nActuator Telemetry\nJSON Liveness", 
        color="#922B21", fontsize=6.8, fontweight="bold", ha="center", va="center")

plt.tight_layout()
fig2_path = os.path.abspath("screenshots/task3/fig3_2_architecture_diagram.png")
plt.savefig(fig2_path, bbox_inches="tight", dpi=300)
plt.close()
print(f"Figure 3.2 saved to: {fig2_path}")
