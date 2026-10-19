import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

os.makedirs("screenshots/task5", exist_ok=True)

# ----------------------------------------------------------------------
# Figure 5.1: Feature Branching & Pull Request Lifecycle
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 6.2), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

# Title Banner
rect_title = patches.FancyBboxPatch((2, 90), 96, 8, boxstyle="round,pad=1", ec="#1B365D", fc="#1B365D", zorder=2)
ax.add_patch(rect_title)
ax.text(50, 94, "FEATURE BRANCHING WORKFLOW & PULL REQUEST MERGE GATEWAY (TASK 5)", 
        color="white", fontsize=10.5, fontweight="bold", ha="center", va="center")

# Track Lines
# dev branch (Top)
ax.plot([5, 95], [68, 68], color="#27AE60", lw=3.5, zorder=1)
# feature branch (Bottom)
ax.plot([25, 75], [32, 32], color="#2980B9", lw=3.5, zorder=1)

# Branch Labels
b_dev = patches.FancyBboxPatch((2, 64), 14, 8, boxstyle="round,pad=0.4", ec="#27AE60", fc="#27AE60", zorder=3)
ax.add_patch(b_dev)
ax.text(9, 68, "dev branch\n(Integration)", color="white", fontsize=8, fontweight="bold", ha="center", va="center")

b_feat = patches.FancyBboxPatch((5, 28), 18, 8, boxstyle="round,pad=0.4", ec="#2980B9", fc="#2980B9", zorder=3)
ax.add_patch(b_feat)
ax.text(14, 32, "feature/card-app...\n(Feature 1)", color="white", fontsize=7.5, fontweight="bold", ha="center", va="center")

# Commits on dev before branching
c_base = plt.Circle((20, 68), 2.2, color="#27AE60", ec="white", lw=2, zorder=4)
ax.add_patch(c_base)
ax.text(20, 73, "Base Baseline\n(Task 4 Init)", fontsize=7.5, fontweight="bold", color="#196F3D", ha="center")

# Branching arrow: dev -> feature
ax.annotate("", xy=(28, 33), xytext=(21, 66), arrowprops=dict(arrowstyle="->", color="#2980B9", lw=2.5, mutation_scale=15))
ax.text(21, 48, "git checkout -b\nfeature/...", fontsize=7.2, color="#1B4F72", fontweight="bold", ha="right")

# Commits on feature branch
c_f1 = plt.Circle((40, 32), 2.2, color="#2980B9", ec="white", lw=2, zorder=4)
ax.add_patch(c_f1)
ax.text(40, 24, "feat(application)\nLimit Evaluator", fontsize=7.2, fontweight="bold", color="#1B4F72", ha="center")

c_f2 = plt.Circle((58, 32), 2.2, color="#2980B9", ec="white", lw=2, zorder=4)
ax.add_patch(c_f2)
ax.text(58, 24, "test(application)\nUnit Tests Pass", fontsize=7.2, fontweight="bold", color="#1B4F72", ha="center")

# Quality Gate Box
q_box = patches.FancyBboxPatch((42, 44), 30, 16, boxstyle="round,pad=0.8", ec="#D4AC0D", fc="#FEF9E7", lw=1.5, zorder=2)
ax.add_patch(q_box)
ax.text(57, 56, "PULL REQUEST REVIEW GATE #1", color="#7D6608", fontsize=8, fontweight="bold", ha="center")
ax.text(57, 51, "• 8 Unit Tests Pass (mvn test)\n• Code Review Approved\n• Zero Merge Conflicts", 
        color="#2C3E50", fontsize=7.2, ha="center")

# Merge arrow: feature -> dev
ax.annotate("", xy=(80, 66), xytext=(60, 34), arrowprops=dict(arrowstyle="->", color="#C0392B", lw=2.5, mutation_scale=15))
ax.text(74, 46, "PR Merge\n(--no-ff)", fontsize=7.5, color="#C0392B", fontweight="bold", ha="left")

# Merge commit on dev
c_merge = plt.Circle((82, 68), 2.8, color="#C0392B", ec="white", lw=2, zorder=4)
ax.add_patch(c_merge)
ax.text(82, 75, "Merge PR #1\n(Commit 7352dcd)", fontsize=8, fontweight="bold", color="#C0392B", ha="center")

# Bottom Banner: Verification Summary
b_box = patches.FancyBboxPatch((10, 4), 80, 7.5, boxstyle="round,pad=0.5", ec="#BDC3C7", fc="#F8F9F9", lw=1, zorder=2)
ax.add_patch(b_box)
ax.text(50, 7.7, "Branching Verification: Non-fast-forward merge preserves complete feature commit history", 
        color="#2C3E50", fontsize=8, ha="center", va="center", fontweight="bold")

plt.tight_layout()
fig1_path = os.path.abspath("screenshots/task5/fig5_1_feature_branch_workflow.png")
plt.savefig(fig1_path, bbox_inches="tight", dpi=300)
plt.close()
print(f"Figure 5.1 saved to: {fig1_path}")

# ----------------------------------------------------------------------
# Figure 5.2: Credit Card Application Workflow Sequence Diagram
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 6.8), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

# Title Banner
rect_title2 = patches.FancyBboxPatch((2, 92), 96, 7, boxstyle="round,pad=1", ec="#1B365D", fc="#1B365D", zorder=2)
ax.add_patch(rect_title2)
ax.text(50, 95.5, "FEATURE 1: CREDIT CARD APPLICATION & ELIGIBILITY EVALUATION SEQUENCE", 
        color="white", fontsize=10.5, fontweight="bold", ha="center", va="center")

# Sequence Actors / Lifelines
lifelines = [
    ("Retail Applicant\n(Web Browser)", 12, "#27AE60"),
    ("CreditCardController\n(Spring MVC)", 38, "#2980B9"),
    ("CreditCardService\n(Limit Evaluator)", 64, "#8E44AD"),
    ("H2 Database\n(JPA Repository)", 88, "#D35400")
]

for name, x, col in lifelines:
    # Lifeline header box
    h_box = patches.FancyBboxPatch((x - 10, 78), 20, 9, boxstyle="round,pad=0.4", ec=col, fc=col, zorder=3)
    ax.add_patch(h_box)
    ax.text(x, 82.5, name, color="white", fontsize=7.8, fontweight="bold", ha="center", va="center")
    # Vertical dashed line
    ax.plot([x, x], [12, 78], color=col, lw=1.5, ls="--", zorder=1)

# Sequence Messages
messages = [
    (12, 38, 70, "1. POST /apply (Name, Email, Income, Limit)", "#2C3E50", "->"),
    (38, 64, 60, "2. calculateMaxEligibleLimit(Income, Tier)", "#2C3E50", "->"),
    (64, 64, 52, "3. Apply 40% income cap & Tier max ceiling", "#8E44AD", "loop"),
    (64, 88, 44, "4. save(CreditCard: PENDING, Capped Limit)", "#2C3E50", "->"),
    (88, 64, 36, "5. Return Persisted Entity with Generated ID", "#27AE60", "-->"),
    (64, 38, 28, "6. Return Saved CreditCard Object", "#27AE60", "-->"),
    (38, 12, 20, "7. 302 Redirect /cards with Confirmation Flash Msg", "#27AE60", "-->")
]

for x1, x2, y, text, col, arrow in messages:
    if arrow == "loop":
        # Self call arc
        arc = patches.Arc((x1 + 4, y + 2), 8, 6, angle=0, theta1=270, theta2=90, color=col, lw=1.5)
        ax.add_patch(arc)
        ax.annotate("", xy=(x1, y - 1), xytext=(x1 + 4, y - 1), arrowprops=dict(arrowstyle="->", color=col, lw=1.5))
        ax.text(x1 + 9, y + 2, text, color=col, fontsize=7.2, fontweight="bold", va="center")
    elif arrow == "-->":
        ax.annotate("", xy=(x2, y), xytext=(x1, y), arrowprops=dict(arrowstyle="->", color=col, lw=1.5, ls="--"))
        ax.text((x1 + x2)/2, y + 2, text, color=col, fontsize=7.2, fontweight="bold", ha="center")
    else:
        ax.annotate("", xy=(x2, y), xytext=(x1, y), arrowprops=dict(arrowstyle="->", color=col, lw=1.5))
        ax.text((x1 + x2)/2, y + 2, text, color=col, fontsize=7.2, fontweight="bold", ha="center")

plt.tight_layout()
fig2_path = os.path.abspath("screenshots/task5/fig5_2_onboarding_workflow_sequence.png")
plt.savefig(fig2_path, bbox_inches="tight", dpi=300)
plt.close()
print(f"Figure 5.2 saved to: {fig2_path}")
