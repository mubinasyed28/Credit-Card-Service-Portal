import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs("screenshots/whitepaper", exist_ok=True)

fig, ax = plt.subplots(figsize=(12, 6.6), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

# Main Title Banner
title_box = patches.FancyBboxPatch((2, 91.5), 96, 7.5, boxstyle="round,pad=0.7", ec="#0B2545", fc="#0B2545", zorder=3)
ax.add_patch(title_box)
ax.text(50, 95.2, "ENTERPRISE DEVOPS CI/CD & AUTOMATED QUALITY GATE ARCHITECTURE", 
        color="#FFFFFF", fontsize=11, fontweight="bold", fontname="Segoe UI", ha="center", va="center")

# Background swimlane container
bg_box = patches.FancyBboxPatch((2, 3), 96, 86.5, boxstyle="round,pad=0.5", ec="#D0D7DE", fc="#F8FAFC", zorder=1)
ax.add_patch(bg_box)

# 5 Core Architectural Pillars / Stages
stages = [
    {
        "id": "1",
        "title": "SOURCE & SCM",
        "subtitle": "Git & GitHub Workflow",
        "x": 4, "w": 16.5,
        "items": [
            "Branching: feature/*, dev, main",
            "Peer Review Pull Requests",
            "Webhook Trigger on Push",
            "Signed Commit Baseline"
        ],
        "color_edge": "#1F6FEB", "color_bg": "#F0F6FC", "header_bg": "#1F6FEB"
    },
    {
        "id": "2",
        "title": "CONTINUOUS INTEGRATION",
        "subtitle": "Jenkins & Maven Engine",
        "x": 23, "w": 17,
        "items": [
            "Declarative Jenkinsfile",
            "Clean Workspace Checkout",
            "mvn clean compile (Java 17)",
            "Surefire Unit & Service Tests"
        ],
        "color_edge": "#0969DA", "color_bg": "#EFF6FF", "header_bg": "#0969DA"
    },
    {
        "id": "3",
        "title": "SELENIUM QUALITY GATE",
        "subtitle": "Headless E2E Regression",
        "x": 42.5, "w": 18,
        "items": [
            "4 Critical User Journeys",
            "Page Object Model (POM)",
            "Strict Fail-Fast Gate",
            "TakesScreenshot on Defect"
        ],
        "color_edge": "#8250DF", "color_bg": "#FBEFFF", "header_bg": "#8250DF"
    },
    {
        "id": "4",
        "title": "CONTAINERIZATION",
        "subtitle": "Multi-Stage Docker",
        "x": 63, "w": 16,
        "items": [
            "Multi-Stage Build (Maven)",
            "Temurin-17 JRE Minimal Image",
            "Immutable Tag: ${BUILD_ID}",
            "Image Security & Layer Cache"
        ],
        "color_edge": "#1A7F37", "color_bg": "#F0FDF4", "header_bg": "#1A7F37"
    },
    {
        "id": "5",
        "title": "CD & PROVISIONING",
        "subtitle": "Ansible & Verification",
        "x": 81.5, "w": 15,
        "items": [
            "Idempotent YAML Playbook",
            "Target Host (Port 8080)",
            "Actuator Health Probe",
            "Automated Rollback Hook"
        ],
        "color_edge": "#BC4C00", "color_bg": "#FFF8F2", "header_bg": "#BC4C00"
    }
]

for s in stages:
    # Outer card
    card = patches.FancyBboxPatch((s["x"], 32), s["w"], 55, boxstyle="round,pad=0.5", 
                                  ec=s["color_edge"], fc=s["color_bg"], lw=1.5, zorder=2)
    ax.add_patch(card)
    
    # Header tag
    header = patches.FancyBboxPatch((s["x"] + 0.5, 78), s["w"] - 1, 8.2, boxstyle="round,pad=0.3",
                                    ec=s["header_bg"], fc=s["header_bg"], zorder=3)
    ax.add_patch(header)
    ax.text(s["x"] + s["w"]/2, 83.2, s["title"], color="white", fontsize=8, fontweight="bold", fontname="Segoe UI", ha="center")
    ax.text(s["x"] + s["w"]/2, 79.5, s["subtitle"], color="#E6EDF3", fontsize=6.5, fontname="Segoe UI", ha="center")
    
    # Content items
    y_text = 73
    for it in s["items"]:
        ax.text(s["x"] + 1.2, y_text, f"• {it}", color="#1F2328", fontsize=6.8, fontname="Segoe UI", va="top")
        y_text -= 9.5

# Connectors between stages (Top Flow)
for i in range(len(stages) - 1):
    curr = stages[i]
    nxt = stages[i+1]
    ax.annotate("", xy=(nxt["x"] - 0.2, 59), xytext=(curr["x"] + curr["w"] + 0.2, 59),
                arrowprops=dict(arrowstyle="->", color="#0B2545", lw=2.2, mutation_scale=13), zorder=4)

# Quality Gate Decision & Feedback Loops (Lower Section)
# Failure Interception Box under Selenium Gate
fail_box = patches.FancyBboxPatch((35, 6), 33, 21, boxstyle="round,pad=0.5", ec="#CF222E", fc="#FFEBE9", lw=1.5, zorder=2)
ax.add_patch(fail_box)
ax.text(51.5, 23.2, "FAIL-FAST QUALITY GATE POLICY", color="#A40E26", fontsize=7.8, fontweight="bold", fontname="Segoe UI", ha="center")
fail_details = [
    "Assertion Failure / Defect Interception",
    "Pipeline ABORT: Docker build & CD cancelled",
    "Failure artifacts saved (Surefire XML + Screenshot PNG)",
    "Instant feedback to Dev for defect turnaround"
]
y_f = 19.5
for fd in fail_details:
    ax.text(37, y_f, f"[!] {fd}", color="#82071E", fontsize=6.2, fontname="Segoe UI")
    y_f -= 4.2

# Red Arrow from Selenium Stage down to Fail-Fast Gate
ax.annotate("", xy=(51.5, 27.5), xytext=(51.5, 32),
            arrowprops=dict(arrowstyle="->", color="#CF222E", lw=2, mutation_scale=11), zorder=4)
ax.text(53, 29.5, "On Assertion Failure", color="#CF222E", fontsize=6.2, fontweight="bold", fontname="Segoe UI")

# Health Check & Rollback Loop from Stage 5 back
health_box = patches.FancyBboxPatch((72, 6), 24.5, 21, boxstyle="round,pad=0.5", ec="#0969DA", fc="#DDF4FF", lw=1.4, zorder=2)
ax.add_patch(health_box)
ax.text(84.2, 23.2, "RELIABILITY GATEWAY", color="#0550AE", fontsize=7.8, fontweight="bold", fontname="Segoe UI", ha="center")
health_details = [
    "GET /actuator/health == UP",
    "Idempotency: changed=0, failed=0",
    "Automatic Rollback on Error",
    "Zero Downtime Promotion"
]
y_h = 19.5
for hd in health_details:
    ax.text(74, y_h, f"[*] {hd}", color="#0969DA", fontsize=6.2, fontname="Segoe UI")
    y_h -= 4.2

# Arrow from Stage 5 down to Reliability Gateway
ax.annotate("", xy=(84.2, 27.5), xytext=(84.2, 32),
            arrowprops=dict(arrowstyle="->", color="#0969DA", lw=2, mutation_scale=11), zorder=4)

# Developer Feedback Arrow (from Fail box back to SCM)
ax.annotate("", xy=(12, 31.5), xytext=(35, 16.5),
            arrowprops=dict(arrowstyle="->", color="#CF222E", lw=1.6, linestyle="--",
                            connectionstyle="angle,angleA=-180,angleB=90,rad=8", mutation_scale=10), zorder=4)
ax.text(14, 18.5, "Instant Feedback\n& Defect Fix Loop", color="#CF222E", fontsize=6.2, fontweight="bold", fontname="Segoe UI", ha="center")

plt.tight_layout()
output_path = "screenshots/whitepaper/architecture_diagram.png"
plt.savefig(output_path, dpi=300, bbox_inches="tight")
plt.close()
print(f"Architecture diagram generated successfully at: {output_path}")
