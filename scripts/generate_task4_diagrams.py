import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

os.makedirs("screenshots/task4", exist_ok=True)

fig, ax = plt.subplots(figsize=(11, 6.2), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

# Title Banner
rect_title = patches.FancyBboxPatch((2, 90), 96, 8, boxstyle="round,pad=1", ec="#1B365D", fc="#1B365D", zorder=2)
ax.add_patch(rect_title)
ax.text(50, 94, "CREDIT CARD SERVICE PORTAL — GIT FLOW BRANCHING & COLLABORATION ARCHITECTURE", 
        color="white", fontsize=10.5, fontweight="bold", ha="center", va="center")

# Horizontal Branch Track Lines
# 1. main branch (Top)
ax.plot([5, 95], [74, 74], color="#1B365D", lw=3.5, zorder=1)
# 2. dev branch (Middle)
ax.plot([5, 95], [48, 48], color="#27AE60", lw=3.5, zorder=1)
# 3. feature 1 branch (Bottom Left)
ax.plot([25, 55], [22, 22], color="#2980B9", lw=3, zorder=1)
# 4. feature 2 branch (Bottom Right)
ax.plot([55, 85], [22, 22], color="#8E44AD", lw=3, zorder=1)

# Branch Labels on Left
b_main = patches.FancyBboxPatch((2, 70), 14, 8, boxstyle="round,pad=0.4", ec="#1B365D", fc="#1B365D", zorder=3)
ax.add_patch(b_main)
ax.text(9, 74, "main\n(Production)", color="white", fontsize=8, fontweight="bold", ha="center", va="center")

b_dev = patches.FancyBboxPatch((2, 44), 14, 8, boxstyle="round,pad=0.4", ec="#27AE60", fc="#27AE60", zorder=3)
ax.add_patch(b_dev)
ax.text(9, 48, "dev\n(Integration)", color="white", fontsize=8, fontweight="bold", ha="center", va="center")

# Commits on main
# Initial commit
c_init = plt.Circle((20, 74), 2.2, color="#1B365D", ec="white", lw=2, zorder=4)
ax.add_patch(c_init)
ax.text(20, 79, "Init Commit\n(Skeleton)", fontsize=7.5, fontweight="bold", color="#1B365D", ha="center")

# Release Tag v1.0.0
c_rel = plt.Circle((90, 74), 2.8, color="#C0392B", ec="white", lw=2, zorder=4)
ax.add_patch(c_rel)
ax.text(90, 81, "TAG: v1.0.0\n(Release MVP)", fontsize=8, fontweight="bold", color="#C0392B", ha="center")

# Commits on dev
c_dev1 = plt.Circle((20, 48), 2.0, color="#27AE60", ec="white", lw=1.5, zorder=4)
ax.add_patch(c_dev1)

c_dev2 = plt.Circle((55, 48), 2.2, color="#27AE60", ec="white", lw=1.5, zorder=4)
ax.add_patch(c_dev2)
ax.text(55, 53, "Merge PR #1\n(Feature 1)", fontsize=7.5, fontweight="bold", color="#196F3D", ha="center")

c_dev3 = plt.Circle((85, 48), 2.2, color="#27AE60", ec="white", lw=1.5, zorder=4)
ax.add_patch(c_dev3)
ax.text(85, 53, "Merge PR #2\n(Conflict Res)", fontsize=7.5, fontweight="bold", color="#196F3D", ha="center")

# Branching from main to dev
ax.annotate("", xy=(20, 50), xytext=(20, 72), arrowprops=dict(arrowstyle="->", color="#27AE60", lw=2, mutation_scale=12))

# Feature 1 Branch
ax.annotate("", xy=(25, 22), xytext=(22, 46), arrowprops=dict(arrowstyle="->", color="#2980B9", lw=2, mutation_scale=12))
c_f1_1 = plt.Circle((35, 22), 1.8, color="#2980B9", ec="white", lw=1.5, zorder=4)
ax.add_patch(c_f1_1)
c_f1_2 = plt.Circle((45, 22), 1.8, color="#2980B9", ec="white", lw=1.5, zorder=4)
ax.add_patch(c_f1_2)
ax.text(40, 14, "feature/card-application\n(Task 5: Onboarding Flow)", fontsize=7.5, fontweight="bold", color="#1B4F72", ha="center")

# Merge Feature 1 back to dev
ax.annotate("", xy=(55, 46), xytext=(52, 22), arrowprops=dict(arrowstyle="->", color="#2980B9", lw=2, mutation_scale=12))

# Feature 2 Branch
ax.annotate("", xy=(58, 22), xytext=(55, 46), arrowprops=dict(arrowstyle="->", color="#8E44AD", lw=2, mutation_scale=12))
c_f2_1 = plt.Circle((68, 22), 1.8, color="#8E44AD", ec="white", lw=1.5, zorder=4)
ax.add_patch(c_f2_1)
c_f2_2 = plt.Circle((78, 22), 1.8, color="#8E44AD", ec="white", lw=1.5, zorder=4)
ax.add_patch(c_f2_2)
ax.text(73, 14, "feature/card-search-lifecycle\n(Task 6: Directory & State Engine)", fontsize=7.5, fontweight="bold", color="#6C3483", ha="center")

# Merge Feature 2 back to dev
ax.annotate("", xy=(85, 46), xytext=(82, 22), arrowprops=dict(arrowstyle="->", color="#8E44AD", lw=2, mutation_scale=12))

# Merge dev to main (Release)
ax.annotate("", xy=(90, 71), xytext=(87, 50), arrowprops=dict(arrowstyle="->", color="#C0392B", lw=2.5, mutation_scale=15))
ax.text(93, 60, "Production\nRelease PR", fontsize=7.5, fontweight="bold", color="#C0392B", ha="left")

# Bottom Banner: Quality Standards & Conventional Commits
q_box = patches.FancyBboxPatch((10, 2), 80, 7.5, boxstyle="round,pad=0.5", ec="#BDC3C7", fc="#F8F9F9", lw=1, zorder=2)
ax.add_patch(q_box)
ax.text(50, 5.7, "Branching Rules: Conventional Commits (feat, fix, docs, test, ci) • 100% Jenkins CI Pass • Peer Review Approval", 
        color="#2C3E50", fontsize=8, ha="center", va="center", fontweight="bold")

plt.tight_layout()
fig_path = os.path.abspath("screenshots/task4/fig4_1_git_branching_workflow.png")
plt.savefig(fig_path, bbox_inches="tight", dpi=300)
plt.close()
print(f"Figure 4.1 saved to: {fig_path}")
