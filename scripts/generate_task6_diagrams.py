import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

os.makedirs("screenshots/task6", exist_ok=True)

# ----------------------------------------------------------------------
# Figure 6.1: Git Merge Conflict Creation, Manual Resolution & Tagging
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11.5, 6.5), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

# Title Banner
rect_title = patches.FancyBboxPatch((2, 91), 96, 7.5, boxstyle="round,pad=0.8", ec="#1B365D", fc="#1B365D", zorder=2)
ax.add_patch(rect_title)
ax.text(50, 94.7, "GIT COLLABORATION WORKFLOW: CONFLICT RESOLUTION & RELEASE BASELINE TAGGING (TASK 6)", 
        color="white", fontsize=10, fontweight="bold", ha="center", va="center")

# Track lines
# main branch (Top)
ax.plot([5, 95], [78, 78], color="#8E44AD", lw=3.5, zorder=1)
# dev branch (Middle)
ax.plot([5, 95], [52, 52], color="#27AE60", lw=3.5, zorder=1)
# feature branch (Bottom)
ax.plot([18, 58], [24, 24], color="#2980B9", lw=3.5, zorder=1)

# Branch Labels
b_main = patches.FancyBboxPatch((2, 74.5), 13, 7, boxstyle="round,pad=0.4", ec="#8E44AD", fc="#8E44AD", zorder=3)
ax.add_patch(b_main)
ax.text(8.5, 78, "main branch\n(Production)", color="white", fontsize=7.5, fontweight="bold", ha="center", va="center")

b_dev = patches.FancyBboxPatch((2, 48.5), 13, 7, boxstyle="round,pad=0.4", ec="#27AE60", fc="#27AE60", zorder=3)
ax.add_patch(b_dev)
ax.text(8.5, 52, "dev branch\n(Integration)", color="white", fontsize=7.5, fontweight="bold", ha="center", va="center")

b_feat = patches.FancyBboxPatch((2, 20.5), 15, 7, boxstyle="round,pad=0.4", ec="#2980B9", fc="#2980B9", zorder=3)
ax.add_patch(b_feat)
ax.text(9.5, 24, "feature/card-update...\n(Limit & CRUD)", color="white", fontsize=7, fontweight="bold", ha="center", va="center")

# Initial commit base
c_base = plt.Circle((18, 52), 2.2, color="#27AE60", ec="white", lw=2, zorder=4)
ax.add_patch(c_base)
ax.text(18, 57, "Base Commit\ne5943a9", fontsize=7, fontweight="bold", color="#196F3D", ha="center")

# Branch off dev -> feature
ax.annotate("", xy=(22, 25), xytext=(19, 50), arrowprops=dict(arrowstyle="->", color="#2980B9", lw=2, mutation_scale=12))

# Commit on dev (Concurrent enhancement)
c_dev_edit = plt.Circle((36, 52), 2.2, color="#27AE60", ec="white", lw=2, zorder=4)
ax.add_patch(c_dev_edit)
ax.text(36, 57, "dev: f264557\n+approvalRate Metric", fontsize=6.8, fontweight="bold", color="#196F3D", ha="center")

# Commit on feature branch
c_feat_edit = plt.Circle((36, 24), 2.2, color="#2980B9", ec="white", lw=2, zorder=4)
ax.add_patch(c_feat_edit)
ax.text(36, 17, "feat: e01a848\n+Limit Update & REST", fontsize=6.8, fontweight="bold", color="#1B4F72", ha="center")

# Merge Attempt Arrow -> Conflict
ax.annotate("", xy=(49, 49), xytext=(38, 26), arrowprops=dict(arrowstyle="->", color="#C0392B", lw=2, ls="--", mutation_scale=14))

# Conflict Box
box_conflict = patches.FancyBboxPatch((44, 31), 22, 17, boxstyle="round,pad=0.6", ec="#C0392B", fc="#FDEDEC", lw=1.5, zorder=3)
ax.add_patch(box_conflict)
ax.text(55, 45, "GIT MERGE CONFLICT", color="#922B21", fontsize=8, fontweight="bold", ha="center")
ax.text(55, 41, "Conflict on CreditCardService.java\nLines 134-140 (getMetrics)", color="#78281F", fontsize=6.8, fontweight="bold", ha="center")
ax.text(55, 34, "<<<<<<< HEAD: approvalRate\n=======\n>>>>>>> feat: totalCreditLimit", color="#900C3F", fontfamily="monospace", fontsize=6.2, ha="center")

# Resolution Arrow
ax.annotate("", xy=(68, 51), xytext=(63, 40), arrowprops=dict(arrowstyle="->", color="#27AE60", lw=2.2, mutation_scale=14))

# Resolution Commit on dev
c_resolve = plt.Circle((70, 52), 2.4, color="#E67E22", ec="white", lw=2, zorder=4)
ax.add_patch(c_resolve)
ax.text(70, 57, "Merge Resolution\nfe824a5 (Combined)", fontsize=7, fontweight="bold", color="#B9770E", ha="center")

# Hardening commit
c_guard = plt.Circle((80, 52), 2.2, color="#27AE60", ec="white", lw=2, zorder=4)
ax.add_patch(c_guard)
ax.text(80, 44, "Guard: 2a275f1\nUniqueness Check", fontsize=6.8, fontweight="bold", color="#196F3D", ha="center")

# Merge to main Arrow
ax.annotate("", xy=(87, 76), xytext=(81, 54), arrowprops=dict(arrowstyle="->", color="#8E44AD", lw=2.5, mutation_scale=15))
ax.text(82, 66, "git merge dev\n(--no-ff)", fontsize=7, color="#5B2C6F", fontweight="bold", ha="right")

# Release Tag on main
c_main_rel = plt.Circle((90, 78), 2.8, color="#8E44AD", ec="#F4D03F", lw=2.5, zorder=4)
ax.add_patch(c_main_rel)
ax.text(90, 70.5, "Release Baseline\nv1.0.0 (9ea5e65)", fontsize=7.2, fontweight="bold", color="#5B2C6F", ha="center")

# Tag Callout Banner
tag_box = patches.FancyBboxPatch((78, 83), 20, 7, boxstyle="round,pad=0.5", ec="#F39C12", fc="#FEF9E7", lw=1.5, zorder=5)
ax.add_patch(tag_box)
ax.text(88, 86.5, "TAG: v1.0.0 [STABLE MVP]", color="#7D6608", fontsize=7.5, fontweight="bold", ha="center", va="center")

# Test suite verification badge
test_badge = patches.FancyBboxPatch((30, 2), 40, 7, boxstyle="round,pad=0.5", ec="#27AE60", fc="#EAFAF1", lw=1.2, zorder=2)
ax.add_patch(test_badge)
ax.text(50, 5.5, "AUTOMATED QUALITY GATE: 10 / 10 UNIT & INTEGRATION TESTS PASSING (100% GREEN)", 
        color="#1E8449", fontsize=7.2, fontweight="bold", ha="center", va="center")

plt.tight_layout()
fig.savefig("screenshots/task6/fig6_1_git_conflict_resolution.png", dpi=300)
plt.close(fig)
print("[+] Generated fig6_1_git_conflict_resolution.png")


# ----------------------------------------------------------------------
# Figure 6.2: Completed MVP Functional Architecture & State Lifecycle
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11.5, 6.5), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

# Title Banner
rect_title2 = patches.FancyBboxPatch((2, 91), 96, 7.5, boxstyle="round,pad=0.8", ec="#1B365D", fc="#1B365D", zorder=2)
ax.add_patch(rect_title2)
ax.text(50, 94.7, "CREDIT CARD SERVICE PORTAL: COMPLETE 5-FUNCTION MVP TOPOLOGY (TASK 6)", 
        color="white", fontsize=10, fontweight="bold", ha="center", va="center")

# Left Column: The 5 Core Functional Modules (MVP Scope)
cols_mvp = [
    ("1. Card Application & Limit Engine", "Income-based limit evaluation (40% ceiling),\ntier cap enforcement, automatic masking", "#1B4F72", 76),
    ("2. Card Directory & Live Search", "Multi-field search (Customer name, masked\ncard number), real-time status filtering", "#117864", 61),
    ("3. Role-Based Status Lifecycle", "State machine: PENDING -> ACTIVE, BLOCKED,\nREJECTED, UNBLOCK with audit timestamps", "#B9770E", 46),
    ("4. Record Update & Limit Adjustment", "Safe limit adjustment validated against eligibility;\ncontact info update via Web UI and REST API", "#2E86C1", 31),
    ("5. Summary Metrics & Health Monitoring", "Executive KPI cards, portfolio credit limit sum,\napproval rate, Actuator /actuator/health", "#7D3C98", 16)
]

for title, desc, color, y in cols_mvp:
    box = patches.FancyBboxPatch((4, y), 42, 12, boxstyle="round,pad=0.6", ec=color, fc="#F8F9F9", lw=1.5, zorder=2)
    ax.add_patch(box)
    header = patches.FancyBboxPatch((4, y+8.5), 42, 3.5, boxstyle="round,pad=0.2", ec=color, fc=color, zorder=3)
    ax.add_patch(header)
    ax.text(25, y+10.2, title, color="white", fontsize=7.5, fontweight="bold", ha="center", va="center")
    ax.text(25, y+4.2, desc, color="#2C3E50", fontsize=6.8, ha="center", va="center")

# Connecting Arrow from Modules to Core Platform
ax.annotate("", xy=(51, 50), xytext=(47, 50), arrowprops=dict(arrowstyle="->", color="#1B365D", lw=3, mutation_scale=15))

# Right Column: Enterprise Architecture Stack & State Transitions
# Top Right: dual interface layer
dual_box = patches.FancyBboxPatch((52, 62), 44, 25, boxstyle="round,pad=0.7", ec="#2874A6", fc="#EBF5FB", lw=1.5, zorder=2)
ax.add_patch(dual_box)
ax.text(74, 83.5, "DUAL INTERACTION INTERFACE", color="#1B4F72", fontsize=8.2, fontweight="bold", ha="center")

ui_sub = patches.FancyBboxPatch((54, 65), 19, 15, boxstyle="round,pad=0.4", ec="#2874A6", fc="white", lw=1.2, zorder=3)
ax.add_patch(ui_sub)
ax.text(63.5, 77, "Web Presentation Layer", color="#154360", fontsize=7.2, fontweight="bold", ha="center")
ax.text(63.5, 71, "• Bootstrap 5 UI\n• Thymeleaf Views\n• Responsive Modals\n• Selenium Selectors", color="#2C3E50", fontsize=6.5, ha="center")

api_sub = patches.FancyBboxPatch((75, 65), 19, 15, boxstyle="round,pad=0.4", ec="#117864", fc="white", lw=1.2, zorder=3)
ax.add_patch(api_sub)
ax.text(84.5, 77, "RESTful API Layer", color="#0E6251", fontsize=7.2, fontweight="bold", ha="center")
ax.text(84.5, 71, "• /api/cards (CRUD)\n• /api/cards/{id}/limit\n• /api/metrics\n• /actuator/health", color="#2C3E50", fontsize=6.5, ha="center")

# Bottom Right: State Transition Lifecycle Engine
fsm_box = patches.FancyBboxPatch((52, 14), 44, 43, boxstyle="round,pad=0.7", ec="#D4AC0D", fc="#FEFDE8", lw=1.5, zorder=2)
ax.add_patch(fsm_box)
ax.text(74, 53.5, "ROLE-BASED STATUS WORKFLOW ENGINE", color="#7D6608", fontsize=8.2, fontweight="bold", ha="center")

# State Nodes
# PENDING
p_node = patches.FancyBboxPatch((55, 37), 16, 8, boxstyle="round,pad=0.4", ec="#F39C12", fc="#FDEBD0", lw=1.5, zorder=3)
ax.add_patch(p_node)
ax.text(63, 41, "PENDING\n(New Application)", color="#7E5109", fontsize=6.8, fontweight="bold", ha="center", va="center")

# ACTIVE
a_node = patches.FancyBboxPatch((77, 37), 16, 8, boxstyle="round,pad=0.4", ec="#27AE60", fc="#D5F5E3", lw=1.5, zorder=3)
ax.add_patch(a_node)
ax.text(85, 41, "ACTIVE\n(Card Activated)", color="#196F3D", fontsize=6.8, fontweight="bold", ha="center", va="center")

# BLOCKED
b_node = patches.FancyBboxPatch((77, 18), 16, 8, boxstyle="round,pad=0.4", ec="#E74C3C", fc="#FADBD8", lw=1.5, zorder=3)
ax.add_patch(b_node)
ax.text(85, 22, "BLOCKED\n(Security Freeze)", color="#922B21", fontsize=6.8, fontweight="bold", ha="center", va="center")

# REJECTED
r_node = patches.FancyBboxPatch((55, 18), 16, 8, boxstyle="round,pad=0.4", ec="#7F8C8D", fc="#EAEDED", lw=1.5, zorder=3)
ax.add_patch(r_node)
ax.text(63, 22, "REJECTED\n(Failed Evaluation)", color="#515A5A", fontsize=6.8, fontweight="bold", ha="center", va="center")

# Transition arrows
# PENDING -> ACTIVE (Approve)
ax.annotate("", xy=(76, 42.5), xytext=(72, 42.5), arrowprops=dict(arrowstyle="->", color="#27AE60", lw=2, mutation_scale=10))
ax.text(74, 45, "Approve", color="#196F3D", fontsize=6.2, fontweight="bold", ha="center")

# PENDING -> REJECTED (Reject)
ax.annotate("", xy=(63, 27), xytext=(63, 36), arrowprops=dict(arrowstyle="->", color="#7F8C8D", lw=2, mutation_scale=10))
ax.text(66, 31.5, "Reject", color="#515A5A", fontsize=6.2, fontweight="bold", ha="left")

# ACTIVE -> BLOCKED (Freeze)
ax.annotate("", xy=(83, 27), xytext=(83, 36), arrowprops=dict(arrowstyle="->", color="#E74C3C", lw=2, mutation_scale=10))
ax.text(80, 31.5, "Freeze", color="#922B21", fontsize=6.2, fontweight="bold", ha="right")

# BLOCKED -> ACTIVE (Unblock)
ax.annotate("", xy=(87, 36), xytext=(87, 27), arrowprops=dict(arrowstyle="->", color="#2980B9", lw=2, mutation_scale=10))
ax.text(90, 31.5, "Unblock", color="#1B4F72", fontsize=6.2, fontweight="bold", ha="left")

plt.tight_layout()
fig.savefig("screenshots/task6/fig6_2_mvp_architecture_lifecycle.png", dpi=300)
plt.close(fig)
print("[+] Generated fig6_2_mvp_architecture_lifecycle.png")
