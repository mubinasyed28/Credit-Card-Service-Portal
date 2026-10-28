import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

os.makedirs("screenshots/task15", exist_ok=True)

# -----------------------------------------------------------------------
# Figure 15.1: End-to-End DevOps Pipeline Architecture (Commit-to-Production)
# -----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(13.0, 7.2), dpi=200)
ax.set_facecolor('#F8F9FA')
fig.patch.set_facecolor('#FFFFFF')
ax.set_xlim(0, 130)
ax.set_ylim(0, 72)
ax.axis('off')

# Title block
ax.text(65, 68.5, "Credit Card Service Portal (CCSP) — Complete End-to-End DevOps Pipeline",
        ha='center', va='center', fontsize=14, fontweight='bold', color='#1B365D')
ax.text(65, 65.5, "Developer: Mubina (23102A0039) | Course: DevOps Lab (Sem VII) | Evaluator: Dr. Snehal Andhare",
        ha='center', va='center', fontsize=10.5, color='#4A5568')

# Stage Definitions
stages = [
    {
        "id": "1",
        "title": "STAGE 1: CODE & COLLABORATION",
        "subtitle": "Git & GitHub Branching Strategy",
        "color": "#1B365D",
        "bg": "#EBF3FB",
        "x": 3, "y": 36, "w": 22, "h": 26,
        "items": [
            "• Feature Branch: feature/*",
            "• Integration Branch: dev",
            "• Protected Release: main",
            "• Release Tag: v1.0.0",
            "• Peer PR Review & Merge",
            "• Conflict Resolution Validated",
            "• Webhook Trigger to Jenkins"
        ]
    },
    {
        "id": "2",
        "title": "STAGE 2: CONTINUOUS INTEGRATION",
        "subtitle": "Jenkins & Maven Automated Build",
        "color": "#0B5394",
        "bg": "#E1EBF5",
        "x": 28, "y": 36, "w": 22, "h": 26,
        "items": [
            "• SCM Polling / GitHub Hook",
            "• Clean Workspace Checkout",
            "• JDK 17 Environment Inject",
            "• mvn clean compile",
            "• Unit Testing (JUnit 5)",
            "• Surefire Report Publishing",
            "• Fast Feedback Loop (< 90s)"
        ]
    },
    {
        "id": "3",
        "title": "STAGE 3: AUTOMATED QUALITY GATE",
        "subtitle": "Selenium Headless Verification",
        "color": "#78281F",
        "bg": "#FADBD8",
        "x": 53, "y": 36, "w": 24, "h": 26,
        "items": [
            "• Headless Chrome & Driver",
            "• 4 User Journey Validations:",
            "  1. Application & Limit Submit",
            "  2. Validation & Negative Gates",
            "  3. Search & Real-time Filter",
            "  4. Status Lifecycle Transition",
            "• Screenshot Failure Trap",
            "• Hard Pipeline Halt on Defect"
        ]
    },
    {
        "id": "4",
        "title": "STAGE 4: CONTAINERIZATION & CD",
        "subtitle": "Docker Multi-Stage & Registry",
        "color": "#196F3D",
        "bg": "#D5F5E3",
        "x": 80, "y": 36, "w": 22, "h": 26,
        "items": [
            "• Multi-Stage Dockerfile",
            "• Stage 1: Maven Package",
            "• Stage 2: Eclipse Temurin JRE",
            "• Image Tag: ccsp:${BUILD_NO}",
            "• Static Tag: ccsp:v1.0.0",
            "• Push to Registry / Local Cache",
            "• Minimal Footprint (~180 MB)"
        ]
    },
    {
        "id": "5",
        "title": "STAGE 5: PROVISION & HEALTH CHECK",
        "subtitle": "Ansible IaC & Production Actuator",
        "color": "#B9770E",
        "bg": "#FCF3CF",
        "x": 105, "y": 36, "w": 22, "h": 26,
        "items": [
            "• Target Host hosts.ini",
            "• Play 1: Clean Host Provision",
            "• Dirs, Users, Firewall (8080)",
            "• Container Run (8080:8080)",
            "• Actuator Check (/actuator/health)",
            "• Idempotency (changed=0)",
            "• Rollback Ready (--tags rollback)"
        ]
    }
]

for s in stages:
    # Outer box
    rect = patches.FancyBboxPatch((s["x"], s["y"]), s["w"], s["h"],
                                  boxstyle="round,pad=0.6,rounding_size=1.2",
                                  facecolor=s["bg"], edgecolor=s["color"], linewidth=2.0)
    ax.add_patch(rect)
    
    # Header bar
    hbar = patches.FancyBboxPatch((s["x"], s["y"] + s["h"] - 5.5), s["w"], 5.5,
                                  boxstyle="round,pad=0.2,rounding_size=0.6",
                                  facecolor=s["color"], edgecolor=s["color"])
    ax.add_patch(hbar)
    
    # Header text
    ax.text(s["x"] + s["w"]/2, s["y"] + s["h"] - 2.5, s["title"],
            ha='center', va='center', fontsize=8.2, fontweight='bold', color='#FFFFFF')
    ax.text(s["x"] + s["w"]/2, s["y"] + s["h"] - 4.4, s["subtitle"],
            ha='center', va='center', fontsize=7.2, color='#EAECEE', style='italic')
    
    # Items
    y_pos = s["y"] + s["h"] - 7.5
    for item in s["items"]:
        ax.text(s["x"] + 1.0, y_pos, item, ha='left', va='center',
                fontsize=7.8, color='#1A252C', fontweight='bold' if item.startswith("• STAGE") else 'normal')
        y_pos -= 2.5

# Connectors between stages (arrows)
arrow_pairs = [(25.5, 49, 27.5, 49), (50.5, 49, 52.5, 49), (77.5, 49, 79.5, 49), (102.5, 49, 104.5, 49)]
for x1, y1, x2, y2 in arrow_pairs:
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(facecolor='#2980B9', edgecolor='#1B365D', width=2.5, headwidth=7, headlength=6))

# Lower Banner: Governance, Quality Gate & Observability Pillars
gp_box = patches.FancyBboxPatch((3, 4), 124, 28,
                                boxstyle="round,pad=0.6,rounding_size=1.2",
                                facecolor='#F4F6F7', edgecolor='#7F8C8D', linewidth=1.5)
ax.add_patch(gp_box)

ax.text(65, 29.5, "END-TO-END DEVOPS GOVERNANCE, QUALITY GATE & OPERATIONAL READINESS MATRIX",
        ha='center', va='center', fontsize=11, fontweight='bold', color='#1B365D')

pillars = [
    {
        "x": 5, "w": 28, "title": "1. Traceability & Versioning",
        "items": [
            "• Git SHA pinned to Docker tag",
            "• Build # propagated via Jenkins",
            "• Release v1.0.0 tagged on main",
            "• Conventional commit history",
            "• Zero unaccounted artifacts"
        ]
    },
    {
        "x": 36, "w": 28, "title": "2. Fail-Fast Quality Gate",
        "items": [
            "• Headless Selenium test suite",
            "• Automated screenshot on failure",
            "• Aborts Docker build on defect",
            "• Intentional defect proven (Task 10)",
            "• Verified test pass before deploy"
        ]
    },
    {
        "x": 67, "w": 28, "title": "3. Infrastructure as Code",
        "items": [
            "• Ansible declarative playbooks",
            "• Idempotency verified: changed=0",
            "• Non-root container execution (ccsp)",
            "• UFW firewall port isolation (8080)",
            "• Host directory hierarchy enforcement"
        ]
    },
    {
        "x": 98, "w": 28, "title": "4. Observability & Recovery",
        "items": [
            "• Spring Boot Actuator /health",
            "• Sub-30s automated rollback",
            "• Structured application logging",
            "• Health status validated before green",
            "• Disaster recovery playbook tag"
        ]
    }
]

for p in pillars:
    pb = patches.FancyBboxPatch((p["x"], 6), p["w"], 21,
                                boxstyle="round,pad=0.4,rounding_size=0.8",
                                facecolor='#FFFFFF', edgecolor='#BDC3C7', linewidth=1.0)
    ax.add_patch(pb)
    
    # Pillar title
    ax.text(p["x"] + p["w"]/2, 24.5, p["title"],
            ha='center', va='center', fontsize=8.8, fontweight='bold', color='#2C3E50')
    
    # Line separator
    ax.plot([p["x"] + 1, p["x"] + p["w"] - 1], [23, 23], color='#3498DB', linewidth=1.5)
    
    py_pos = 20.8
    for item in p["items"]:
        ax.text(p["x"] + 1.2, py_pos, item, ha='left', va='center',
                fontsize=7.8, color='#34495E')
        py_pos -= 3.2

plt.tight_layout()
plt.savefig("screenshots/task15/fig15_1_end_to_end_devops_pipeline.png", dpi=200, bbox_inches='tight')
plt.close()
print("Figure 15.1 generated successfully.")

# -----------------------------------------------------------------------
# Figure 15.2: Technical Architecture Stack & Viva Defense Matrix
# -----------------------------------------------------------------------
fig2, ax2 = plt.subplots(figsize=(13.0, 7.2), dpi=200)
ax2.set_facecolor('#F8F9FA')
fig2.patch.set_facecolor('#FFFFFF')
ax2.set_xlim(0, 130)
ax2.set_ylim(0, 72)
ax2.axis('off')

# Title block
ax2.text(65, 68.5, "Credit Card Service Portal (CCSP) — Technical Stack & Viva Voce Defense Framework",
         ha='center', va='center', fontsize=14, fontweight='bold', color='#1B365D')
ax2.text(65, 65.5, "Academic Defense Reference | Student: Mubina (23102A0039) | Supervisor: Dr. Snehal Andhare",
         ha='center', va='center', fontsize=10.5, color='#4A5568')

# Left Side: 5-Layer System Architecture Stack
layers = [
    {
        "y": 50, "h": 12, "color": "#1B365D", "bg": "#EBF3FB",
        "layer_name": "LAYER 5: PRESENTATION & SERVICE PORTAL (UI)",
        "tech": "Spring Boot Thymeleaf 3.x + Bootstrap 5 + Vanilla CSS",
        "details": "Responsive UI with deterministic element IDs (nameInput, incomeInput, applyBtn) designed specifically for automated Selenium DOM traversal and visual status validation."
    },
    {
        "y": 37, "h": 12, "color": "#0E6251", "bg": "#E8F8F5",
        "layer_name": "LAYER 4: APPLICATION CORE & DOMAIN LOGIC",
        "tech": "Java 17 LTS + Spring Boot 3.2 + Spring Actuator",
        "details": "REST API endpoints, business validation gates (credit limit calculation, income thresholds), state machine (PENDING->ACTIVE->BLOCKED), and health monitoring (/actuator/health)."
    },
    {
        "y": 24, "h": 12, "color": "#512E5F", "bg": "#F5EEF8",
        "layer_name": "LAYER 3: PERSISTENCE & DATA MANAGEMENT",
        "tech": "Embedded H2 Database + Spring Data JPA / Hibernate",
        "details": "Zero external dependency in-memory relational store. Provides instant cold boot (<2.5s) for fast CI test execution, reproducible test fixture isolation, and live inspection console."
    },
    {
        "y": 11, "h": 12, "color": "#7D6608", "bg": "#FEF9E7",
        "layer_name": "LAYER 2: CONTAINERIZATION & PACKAGING",
        "tech": "Multi-Stage Dockerfile + Eclipse Temurin 17 JRE",
        "details": "Stage 1 Maven build creates jar; Stage 2 minimal JRE packages final artifact. Non-root user execution, strict layer caching, lightweight ~180MB footprint with port 8080 exposed."
    },
    {
        "y": -2, "h": 12, "color": "#6E2C00", "bg": "#FBEEE6",
        "layer_name": "LAYER 1: INFRASTRUCTURE AS CODE & ORCHESTRATION",
        "tech": "Ansible 8.x + Declarative Jenkinsfile + Git/GitHub",
        "details": "Automated provisioning of clean target nodes, UFW firewall rules, service directories, idempotent configuration enforcement, and automated rollback orchestration."
    }
]

for l in layers:
    box = patches.FancyBboxPatch((4, l["y"]), 68, l["h"],
                                boxstyle="round,pad=0.3,rounding_size=0.6",
                                facecolor=l["bg"], edgecolor=l["color"], linewidth=1.5)
    ax2.add_patch(box)
    
    ax2.text(6, l["y"] + l["h"] - 2.6, l["layer_name"],
             ha='left', va='center', fontsize=8.8, fontweight='bold', color=l["color"])
    ax2.text(70, l["y"] + l["h"] - 2.6, l["tech"],
             ha='right', va='center', fontsize=8.0, fontweight='bold', color='#2C3E50')
    
    # Divider
    ax2.plot([6, 70], [l["y"] + l["h"] - 4.2, l["y"] + l["h"] - 4.2], color=l["color"], linewidth=0.8, alpha=0.5)
    
    ax2.text(6, l["y"] + 3.2, l["details"],
             ha='left', va='center', fontsize=7.5, color='#34495E', wrap=True)

# Right Side: Viva Voce Key Defense Concepts Box
viva_box = patches.FancyBboxPatch((76, -2), 50, 64,
                                  boxstyle="round,pad=0.6,rounding_size=1.0",
                                  facecolor='#F4F6F7', edgecolor='#1B365D', linewidth=2.0)
ax2.add_patch(viva_box)

# Viva Header
vh_bar = patches.FancyBboxPatch((76, 56), 50, 6,
                                boxstyle="round,pad=0.2,rounding_size=0.6",
                                facecolor='#1B365D', edgecolor='#1B365D')
ax2.add_patch(vh_bar)
ax2.text(101, 59, "TOP VIVA VOCE DEFENSE TOPICS (10 CORE CONCEPTS)",
         ha='center', va='center', fontsize=9.2, fontweight='bold', color='#FFFFFF')

viva_topics = [
    ("Q1: CI/CD Pipeline Flow", "Commit -> Jenkins -> Maven -> Selenium Gate -> Docker -> Ansible"),
    ("Q2: Automated Quality Gate", "Selenium failures halt pipeline; zero broken code reaches Docker"),
    ("Q3: Selenium Headless Mode", "Enables test execution in headless CI environments without X11"),
    ("Q4: Multi-Stage Dockerfile", "Separates build tools from runtime; cuts image size by >70%"),
    ("Q5: Ansible Idempotency", "Running playbook twice results in changed=0, guaranteeing consistency"),
    ("Q6: Rollback Strategy", "Automated tagging of prior stable image tag restores service in <30s"),
    ("Q7: Git Branching Model", "Feature branches merge to dev; only vetted releases merge to main"),
    ("Q8: Actuator Health Endpoint", "Provides real-time JSON readiness check for continuous deployment"),
    ("Q9: Defect Experiment", "Deliberately injected calculation bug to prove pipeline halt (Task 10)"),
    ("Q10: Cloud Migration Plan", "Roadmap from Docker single-node to Kubernetes Kubelet/Pod orchestration")
]

vy = 52.5
for q, a in viva_topics:
    ax2.text(78, vy, q, ha='left', va='center', fontsize=8.0, fontweight='bold', color='#1B365D')
    ax2.text(78, vy - 2.2, a, ha='left', va='center', fontsize=7.2, color='#2C3E50')
    vy -= 5.5

plt.tight_layout()
plt.savefig("screenshots/task15/fig15_2_technical_architecture_viva_matrix.png", dpi=200, bbox_inches='tight')
plt.close()
print("Figure 15.2 generated successfully.")
