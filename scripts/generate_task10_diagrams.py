import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

os.makedirs("screenshots/task10", exist_ok=True)

# ----------------------------------------------------------------------
# Figure 10.1: Continuous Testing & Automated Quality Gate Architecture
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11.5, 6.8), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

# Title Banner
rect_title = patches.FancyBboxPatch((2, 91), 96, 7.5, boxstyle="round,pad=0.8", ec="#1B365D", fc="#1B365D", zorder=2)
ax.add_patch(rect_title)
ax.text(50, 94.7, "JENKINS CONTINUOUS TESTING ARCHITECTURE & AUTOMATED QUALITY GATE (TASK 10)", 
        color="white", fontsize=10, fontweight="bold", ha="center", va="center")

# Pipeline Flow: Stage 1 (Checkout) -> Stage 2 (Compile) -> Stage 3 (Quality Gate Decision)
stages_top = [
    ("Stage 1: Checkout SCM", "Git origin/dev\nCleanBeforeCheckout\nFetch commit SHA", 3, 21),
    ("Stage 2: Compile & Build", "mvn -B clean compile\nJava 17 Temurin LTS\nBytecode in target/", 27, 21),
    ("Stage 3: Automated Quality Gate", "mvn -B test (Surefire Plugin)\n• 10 Unit/Service Tests\n• 4 Selenium Headless Journeys", 51, 25)
]

for title, desc, x_pos, w in stages_top:
    sb = patches.FancyBboxPatch((x_pos, 60), w, 24, boxstyle="round,pad=0.5", ec="#2980B9", fc="#EBF5FB", lw=1.3, zorder=2)
    ax.add_patch(sb)
    ax.text(x_pos + (w/2), 79.5, title, color="#1B4F72", fontsize=7.5, fontweight="bold", ha="center")
    ax.text(x_pos + (w/2), 69, desc, color="#2C3E50", fontsize=6.3, ha="center")
    if x_pos < 50:
        ax.annotate("", xy=(x_pos + w + 3, 72), xytext=(x_pos + w, 72),
                    arrowprops=dict(arrowstyle="->", color="#1B365D", lw=2, mutation_scale=12))

# Arrow from Stage 3 to Decision Diamond
ax.annotate("", xy=(82, 72), xytext=(76, 72),
            arrowprops=dict(arrowstyle="->", color="#1B365D", lw=2, mutation_scale=12))

# Decision Diamond: All Tests Pass?
diamond = patches.Polygon([[86, 79], [94, 72], [86, 65], [78, 72]], ec="#8E44AD", fc="#F4ECF7", lw=1.5, zorder=3)
ax.add_patch(diamond)
ax.text(86, 73.5, "ALL TESTS\nPASS?", color="#512E5F", fontsize=6.8, fontweight="bold", ha="center", va="center")

# Decision Branch 1: FAILURE PATH (Down -> Left)
ax.annotate("", xy=(86, 48), xytext=(86, 65),
            arrowprops=dict(arrowstyle="->", color="#C0392B", lw=2.5, mutation_scale=12))
ax.text(89, 56.5, "NO (Fail)", color="#C0392B", fontsize=7.5, fontweight="bold")

box_fail = patches.FancyBboxPatch((55, 14), 42, 33, boxstyle="round,pad=0.6", ec="#C0392B", fc="#FDEDEC", lw=1.5, zorder=2)
ax.add_patch(box_fail)
ax.text(76, 42.5, "FAIL-FAST QUALITY GATE INTERCEPTION", color="#922B21", fontsize=8, fontweight="bold", ha="center")
ax.text(76, 38.5, "Pipeline Halted Immediately (Build Marked FAILED)", color="#78281F", fontsize=7, fontweight="bold", ha="center")
fail_desc = (
    "• ABORT: Package and Server Deploy stages strictly SKIPPED\n"
    "• SCREENSHOT: TakesScreenshot archives failure PNG to screenshots/failures/\n"
    "• AUDIT: Surefire reports published to Jenkins test trend dashboard\n"
    "• ALERT: Notification sent to engineering team with defect stack trace"
)
ax.text(76, 26, fail_desc, color="#641E16", fontsize=6.2, ha="center")

# Decision Branch 2: SUCCESS PATH (Down to Success Pipeline Stages)
ax.annotate("", xy=(30, 48), xytext=(86, 72),
            arrowprops=dict(arrowstyle="->", color="#27AE60", lw=2.5, mutation_scale=12,
                            connectionstyle="arc3,rad=-0.2"))
ax.text(50, 52, "YES (100% Pass)", color="#196F3D", fontsize=7.5, fontweight="bold")

box_succ = patches.FancyBboxPatch((3, 14), 48, 33, boxstyle="round,pad=0.6", ec="#27AE60", fc="#EAFAF1", lw=1.5, zorder=2)
ax.add_patch(box_succ)
ax.text(27, 42.5, "DOWNSTREAM STAGES UNLOCKED (PROCEED)", color="#196F3D", fontsize=8, fontweight="bold", ha="center")
ax.text(27, 38.5, "Artifact Packaging, Server Deployment & Verification", color="#145A32", fontsize=7, fontweight="bold", ha="center")
succ_desc = (
    "• Stage 4: Package binary JAR (credit-card-app-1.0.0.jar, 52.4 MB)\n"
    "• Stage 5: Deploy to target Tomcat web container (port 8080)\n"
    "• Stage 6: Issue Actuator health probe (/actuator/health -> status UP)\n"
    "• Complete Continuous Delivery workflow certified as release-ready"
)
ax.text(27, 26, succ_desc, color="#1E8449", fontsize=6.2, ha="center")

# Bottom Banner: Academic Assurance
box_foot = patches.FancyBboxPatch((3, 2), 94, 9.5, boxstyle="round,pad=0.4", ec="#D35400", fc="#FEF9E7", lw=1.2, zorder=2)
ax.add_patch(box_foot)
ax.text(50, 7.5, "ACADEMIC & INDUSTRY ENFORCEMENT: QUALITY GATES ELIMINATE INTEGRATION DEBT", color="#B9770E", fontsize=7.8, fontweight="bold", ha="center")
ax.text(50, 4, "No defect can breach production: Automated Selenium tests physically prevent deployment of regressions.", 
        color="#1B365D", fontsize=6.5, ha="center")

plt.tight_layout()
fig10_1_path = "screenshots/task10/fig10_1_jenkins_continuous_testing_quality_gate.png"
plt.savefig(fig10_1_path, dpi=300, bbox_inches="tight")
plt.close()
print(f"Generated {fig10_1_path}")

# ----------------------------------------------------------------------
# Figure 10.2: Defect Experiment Comparison: Failed Build vs. Corrected Rerun
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11.5, 7.0), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

# Title Banner
rect_title2 = patches.FancyBboxPatch((2, 91), 96, 7.5, boxstyle="round,pad=0.8", ec="#1B365D", fc="#1B365D", zorder=2)
ax.add_patch(rect_title2)
ax.text(50, 94.7, "INTENTIONAL DEFECT EXPERIMENT: JENKINS STAGE VIEW & PIPELINE AUDIT", 
        color="white", fontsize=10, fontweight="bold", ha="center", va="center")

# Top Section: Build #3 - FAILED BUILD (Intentional Defect Commit: 9112dde)
box_b3 = patches.FancyBboxPatch((3, 48), 94, 40, boxstyle="round,pad=0.6", ec="#C0392B", fc="#FDEDEC", lw=1.5, zorder=2)
ax.add_patch(box_b3)

# Header Tag for Build #3
tag_b3 = patches.FancyBboxPatch((4.5, 82), 91, 5, boxstyle="round,pad=0.2", ec="#922B21", fc="#922B21", zorder=3)
ax.add_patch(tag_b3)
ax.text(6, 84.5, "BUILD #3 [FAILED] - Intentional Defect Commit: 9112dde (Credit Limit Multiplier 0.80 instead of 0.40)", 
        color="#FFFFFF", fontsize=7.2, fontweight="bold", va="center")
ax.text(93, 84.5, "STATUS: FAILURE (Pipeline Stopped)", color="#FFC0CB", fontsize=7.2, fontweight="bold", ha="right", va="center")

# Stage blocks for Build #3
stages_b3 = [
    ("Checkout SCM\n2.1s (Passed)", 12, "#D4EFDF", "#27AE60"),
    ("Build & Compile\n4.8s (Passed)", 28, "#D4EFDF", "#27AE60"),
    ("Quality Gate\nFAILED (3 errs)", 44, "#FADBD8", "#C0392B"),
    ("Package Binary\nSKIPPED", 60, "#EAEDED", "#95A5A6"),
    ("Deploy Server\nSKIPPED", 76, "#EAEDED", "#95A5A6"),
    ("Smoke & Probe\nSKIPPED", 90, "#EAEDED", "#95A5A6")
]
for text, x_pos, fc, ec in stages_b3:
    s_blk = patches.FancyBboxPatch((x_pos - 6, 68), 12, 12, boxstyle="round,pad=0.3", ec=ec, fc=fc, lw=1.2, zorder=3)
    ax.add_patch(s_blk)
    ax.text(x_pos, 74, text, color="#922B21" if ec=="#C0392B" else ("#7F8C8D" if ec=="#95A5A6" else "#196F3D"), 
            fontsize=6.5, fontweight="bold", ha="center")

# Console snippet for Build #3
cons_b3 = patches.FancyBboxPatch((4.5, 50), 91, 16, boxstyle="round,pad=0.3", ec="#333333", fc="#1E1E1E", zorder=3)
ax.add_patch(cons_b3)
b3_text = """[ERROR] Failures: CreditCardApplicationWorkflowTest.testMaxEligibleLimitCalculation:27 ==> expected: <400000.0> but was: <800000.0>
[ERROR] Failures: CreditCardApplicationWorkflowTest.testIsEligibleForRequestedLimit:42 ==> expected: <false> but was: <true>
[INFO] BUILD FAILURE -> Surefire quality gate tripped: 3 failures, 0 errors. Execution stopped.
[Jenkins] Quality Gate failed! Stages [Package Application Archive, Deploy to Server, Smoke Test] aborted."""
ax.text(6, 64, b3_text, color="#FF6666", fontfamily="monospace", fontsize=5.8, va="top", zorder=4)

# Bottom Section: Build #4 - SUCCESSFUL RERUN (Defect Correction Commit: 6ffd8d6)
box_b4 = patches.FancyBboxPatch((3, 5), 94, 40, boxstyle="round,pad=0.6", ec="#27AE60", fc="#EAFAF1", lw=1.5, zorder=2)
ax.add_patch(box_b4)

# Header Tag for Build #4
tag_b4 = patches.FancyBboxPatch((4.5, 39), 91, 5, boxstyle="round,pad=0.2", ec="#196F3D", fc="#196F3D", zorder=3)
ax.add_patch(tag_b4)
ax.text(6, 41.5, "BUILD #4 [SUCCESSFUL RERUN] - Defect Correction Commit: 6ffd8d6 (Restored 40% Debt Multiplier)", 
        color="#FFFFFF", fontsize=7.2, fontweight="bold", va="center")
ax.text(93, 41.5, "STATUS: SUCCESS (Weather: Sunny 100%)", color="#00FF66", fontsize=7.2, fontweight="bold", ha="right", va="center")

# Stage blocks for Build #4
stages_b4 = [
    ("Checkout SCM\n2.0s (Passed)", 12, "#D4EFDF", "#27AE60"),
    ("Build & Compile\n4.7s (Passed)", 28, "#D4EFDF", "#27AE60"),
    ("Quality Gate\n14/14 Passed", 44, "#D4EFDF", "#27AE60"),
    ("Package Binary\n14.1s (Passed)", 60, "#D4EFDF", "#27AE60"),
    ("Deploy Server\n2.4s (Passed)", 76, "#D4EFDF", "#27AE60"),
    ("Smoke & Probe\n1.8s (Passed)", 90, "#D4EFDF", "#27AE60")
]
for text, x_pos, fc, ec in stages_b4:
    s_blk = patches.FancyBboxPatch((x_pos - 6, 25), 12, 12, boxstyle="round,pad=0.3", ec=ec, fc=fc, lw=1.2, zorder=3)
    ax.add_patch(s_blk)
    ax.text(x_pos, 31, text, color="#196F3D", fontsize=6.5, fontweight="bold", ha="center")

# Console snippet for Build #4
cons_b4 = patches.FancyBboxPatch((4.5, 7), 91, 16, boxstyle="round,pad=0.3", ec="#333333", fc="#1E1E1E", zorder=3)
ax.add_patch(cons_b4)
b4_text = """[INFO] Running com.creditcard.app.CreditCardPortalSeleniumTest (4/4 passed)
[INFO] Running com.creditcard.app.CreditCardServiceTest (7/7 passed)
[INFO] Running com.creditcard.app.CreditCardApplicationWorkflowTest (3/3 passed)
[INFO] Results: Tests run: 14, Failures: 0, Errors: 0, Skipped: 0 -> BUILD SUCCESS (Total time: 52.45 s)
[Jenkins] Archiving artifacts: app/target/*.jar (credit-card-app-1.0.0.jar, 52.4 MB, SHA-256 registered)
[Jenkins] Deploying to Tomcat server on port 8080 -> GET /actuator/health: HTTP 200 OK (status: UP) -> Finished: SUCCESS"""
ax.text(6, 21, b4_text, color="#00FF66", fontfamily="monospace", fontsize=5.8, va="top", zorder=4)

plt.tight_layout()
fig10_2_path = "screenshots/task10/fig10_2_defect_experiment_stage_view.png"
plt.savefig(fig10_2_path, dpi=300, bbox_inches="tight")
plt.close()
print(f"Generated {fig10_2_path}")
