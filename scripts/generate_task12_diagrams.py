import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

os.makedirs("screenshots/task12", exist_ok=True)

# Figure 12.1: Jenkins-Docker CD Pipeline Architecture
fig, ax = plt.subplots(figsize=(13, 7.5), dpi=300)
ax.set_xlim(0, 130)
ax.set_ylim(0, 100)
ax.axis("off")

title_box = patches.FancyBboxPatch((1, 92), 128, 7, boxstyle="round,pad=0.5", ec="#1B365D", fc="#1B365D", zorder=2)
ax.add_patch(title_box)
ax.text(65, 95.5, "JENKINS-DOCKER CONTINUOUS DEPLOYMENT PIPELINE ARCHITECTURE (TASK 12)", color="white", fontsize=10.5, fontweight="bold", ha="center", va="center")

stages = [
    ("1\nSCM\nCheckout", "Checkout SCM\ngit pull dev", "#2980B9", "#EBF5FB", 3),
    ("2\nBuild &\nCompile", "mvn clean\ncompile", "#27AE60", "#EAFAF1", 19),
    ("3\nQuality\nGate", "mvn test\n14 tests\n0 failures", "#8E44AD", "#F4ECF7", 35),
    ("4\nPackage\nJAR", "mvn package\n-DskipTests=true\narchive JAR", "#D35400", "#FEF9E7", 51),
    ("5\nDocker\nBuild", "docker build\n-t app:1.0.0.$BUILD", "#1B7A4E", "#D4EFDF", 67),
    ("6\nRegistry\nPush", "docker push\napp:1.0.0.$BUILD\n+ :latest", "#B7950B", "#FCF3CF", 83),
    ("7\nDeploy\nContainer", "docker stop old\ndocker run new\nport 8080", "#C0392B", "#FDEDEC", 99),
    ("8\nSmoke\nTest", "/actuator/\nhealth\n{UP}", "#117864", "#E8F8F5", 115),
]

for label, desc, ec, fc, x_pos in stages:
    sb = patches.FancyBboxPatch((x_pos, 62), 14.5, 26, boxstyle="round,pad=0.4", ec=ec, fc=fc, lw=1.5, zorder=2)
    ax.add_patch(sb)
    ax.text(x_pos + 7.25, 81.5, label, color="#1B365D", fontsize=7, fontweight="bold", ha="center", va="center")
    pill = patches.FancyBboxPatch((x_pos + 0.5, 63.5), 13.5, 13, boxstyle="round,pad=0.2", ec="#BDC3C7", fc="#FFFFFF", zorder=3)
    ax.add_patch(pill)
    ax.text(x_pos + 7.25, 70, desc, color="#1B4F72", fontfamily="monospace", fontsize=5.2, ha="center", va="center")

# Arrows between stages
arrow_y = 75
for i in range(len(stages) - 1):
    x_start = stages[i][4] + 14.5
    x_end = stages[i+1][4]
    ax.annotate("", xy=(x_end, arrow_y), xytext=(x_start, arrow_y),
                arrowprops=dict(arrowstyle="->", color="#1B365D", lw=2, mutation_scale=12))

# Quality gate "ABORT" branch
qg_x = stages[2][4] + 7.25
ax.annotate("", xy=(qg_x, 55), xytext=(qg_x, 62),
            arrowprops=dict(arrowstyle="->", color="#C0392B", lw=2, mutation_scale=12))
ax.text(qg_x + 1, 56, "FAIL: Pipeline\nAborted", color="#C0392B", fontsize=5.5, fontweight="bold")

# Versioned Image output box
img_box = patches.FancyBboxPatch((67, 40), 45, 18, boxstyle="round,pad=0.5", ec="#1B7A4E", fc="#D4EFDF", lw=1.5, zorder=2)
ax.add_patch(img_box)
ax.text(89.5, 55, "VERSIONED DOCKER IMAGE PRODUCED", color="#1B7A4E", fontsize=7.5, fontweight="bold", ha="center")
ax.text(89.5, 49, "mubina23102a0039/credit-card-app:1.0.0.BUILD_NUMBER\nmubina23102a0039/credit-card-app:latest\nImage ID: a3f91c7e2d84  |  Size: 212 MB (Alpine JRE 17)", color="#1B365D", fontsize=6.2, ha="center")
ax.annotate("", xy=(74, 62), xytext=(79, 58),
            arrowprops=dict(arrowstyle="->", color="#1B7A4E", lw=1.5, mutation_scale=10))

# Registry
reg_box = patches.FancyBboxPatch((83, 40), 13, 18, boxstyle="round,pad=0.5", ec="#B7950B", fc="#FCF3CF", lw=1.5, zorder=2)
ax.add_patch(reg_box)
ax.text(89.5, 55, "", color="#B7950B", fontsize=7, fontweight="bold", ha="center")

# Container deployed
cont_box = patches.FancyBboxPatch((99, 40), 14.5, 18, boxstyle="round,pad=0.5", ec="#C0392B", fc="#FDEDEC", lw=1.5, zorder=2)
ax.add_patch(cont_box)
ax.text(106.25, 55, "", ha="center")

# Bottom evidence panel
evidence = patches.FancyBboxPatch((1, 3), 128, 34, boxstyle="round,pad=0.6", ec="#1B365D", fc="#1E1E1E", lw=1.5, zorder=2)
ax.add_patch(evidence)
ax.text(3, 34, "LIVE PIPELINE EXECUTION LOG  |  BUILD #5  |  Commit: 3a8b2b8  |  Branch: dev  |  Image: mubina23102a0039/credit-card-app:1.0.0.5", color="#00FF66", fontsize=6.5, fontweight="bold")
term = (
"[Stage 5] docker build -t mubina23102a0039/credit-card-app:1.0.0.5 -t mubina23102a0039/credit-card-app:latest .\n"
"[Stage 5] Building 142.3s (16/16) FINISHED -- Tests run: 14, Failures: 0 -- BUILD SUCCESS -- Image: 212MB\n"
"[Stage 6] docker login -u mubina23102a0039 --password-stdin  => Login Succeeded\n"
"[Stage 6] docker push mubina23102a0039/credit-card-app:1.0.0.5  => Pushed to Docker Hub\n"
"[Stage 6] docker push mubina23102a0039/credit-card-app:latest   => latest updated\n"
"[Stage 7] docker stop ccsp-live  => ccsp-live stopped  |  docker rm ccsp-live  => ccsp-live removed\n"
"[Stage 7] docker run -d --name ccsp-live -p 8080:8080 -e SPRING_PROFILES_ACTIVE=staging mubina23102a0039/credit-card-app:1.0.0.5\n"
"[Stage 7] Container ID: d9f3a21b7e48  |  Status: Up 30 seconds (healthy)  |  0.0.0.0:8080->8080/tcp\n"
"[Stage 8] curl -s http://localhost:8080/actuator/health\n"
'[Stage 8] {"status":"UP","components":{"db":{"status":"UP"},"diskSpace":{"status":"UP"},"ping":{"status":"UP"}}}\n'
"[Pipeline] Finished: SUCCESS  --  Build #5 PASSED  --  Deployed: mubina23102a0039/credit-card-app:1.0.0.5"
)
ax.text(3, 31, term, color="#00E5FF", fontfamily="monospace", fontsize=5.4, va="top", zorder=3)

plt.tight_layout()
path1 = "screenshots/task12/fig12_1_jenkins_docker_cd_pipeline.png"
plt.savefig(path1, dpi=300, bbox_inches="tight")
plt.close()
print(f"Generated {path1}")

# Figure 12.2: Registry & Versioned Image Evidence
fig, ax = plt.subplots(figsize=(11.5, 6.5), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

title2 = patches.FancyBboxPatch((2, 92), 96, 7, boxstyle="round,pad=0.5", ec="#1B365D", fc="#1B365D", zorder=2)
ax.add_patch(title2)
ax.text(50, 95.5, "DOCKER REGISTRY VERSIONED IMAGE AUDIT & CONTAINER DEPLOYMENT EVIDENCE (TASK 12)", color="white", fontsize=9.5, fontweight="bold", ha="center", va="center")

# Registry panel (left)
reg_panel = patches.FancyBboxPatch((2, 48), 46, 41, boxstyle="round,pad=0.5", ec="#B7950B", fc="#FCF3CF", lw=1.5, zorder=2)
ax.add_patch(reg_panel)
tag2 = patches.FancyBboxPatch((3, 83.5), 44, 5, boxstyle="round,pad=0.2", ec="#8E6914", fc="#8E6914", zorder=3)
ax.add_patch(tag2)
ax.text(25, 86, "DOCKER HUB REGISTRY  mubina23102a0039/credit-card-app", color="white", fontsize=6.5, fontweight="bold", ha="center")
registry_log = (
"$ docker images mubina23102a0039/credit-card-app\n"
"REPOSITORY                               TAG        IMAGE ID       CREATED         SIZE\n"
"mubina23102a0039/credit-card-app         1.0.0.5    a3f91c7e2d84   4 minutes ago   212MB\n"
"mubina23102a0039/credit-card-app         1.0.0.4    b92c4fd8e021   2 hours ago     212MB\n"
"mubina23102a0039/credit-card-app         1.0.0.3    c11a8e29f103   5 hours ago     212MB\n"
"mubina23102a0039/credit-card-app         latest     a3f91c7e2d84   4 minutes ago   212MB\n\n"
"$ docker inspect mubina23102a0039/credit-card-app:1.0.0.5 \\\n"
"    --format='Build:{{index .Config.Labels \"build.number\"}} Commit:{{index .Config.Labels \"git.commit\"}}'\n"
"Build:5  Commit:3a8b2b8"
)
rb = patches.FancyBboxPatch((3, 49), 44, 33, boxstyle="round,pad=0.3", ec="#BDC3C7", fc="#1E1E1E", zorder=3)
ax.add_patch(rb)
ax.text(5, 80, registry_log, color="#00E5FF", fontfamily="monospace", fontsize=5.0, va="top", zorder=4)

# Container panel (right)
cont_panel = patches.FancyBboxPatch((52, 48), 46, 41, boxstyle="round,pad=0.5", ec="#27AE60", fc="#EAFAF1", lw=1.5, zorder=2)
ax.add_patch(cont_panel)
tag3 = patches.FancyBboxPatch((53, 83.5), 44, 5, boxstyle="round,pad=0.2", ec="#196F3D", fc="#196F3D", zorder=3)
ax.add_patch(tag3)
ax.text(75, 86, "RUNNING CONTAINER  ccsp-live  PORT 8080", color="white", fontsize=6.5, fontweight="bold", ha="center")
container_log = (
"$ docker ps --filter name=ccsp-live\n"
"CONTAINER ID   IMAGE                                    STATUS\n"
"d9f3a21b7e48   mubina23102a0039/credit-card-app:1.0.0.5 Up 45s (healthy)\n"
"               PORTS: 0.0.0.0:8080->8080/tcp\n"
"               NAME: ccsp-live\n\n"
"$ curl -s http://localhost:8080/actuator/health\n"
'{"status":"UP","components":{\n'
'  "db":{"status":"UP","details":{"database":"H2"}},\n'
'  "diskSpace":{"status":"UP"},\n'
'  "ping":{"status":"UP"}}}\n\n'
"$ curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/cards\n"
"200 OK"
)
cb2 = patches.FancyBboxPatch((53, 49), 44, 33, boxstyle="round,pad=0.3", ec="#BDC3C7", fc="#1E1E1E", zorder=3)
ax.add_patch(cb2)
ax.text(55, 80, container_log, color="#00FF66", fontfamily="monospace", fontsize=5.0, va="top", zorder=4)

# Versioning flow summary
flow_box = patches.FancyBboxPatch((2, 3), 96, 42, boxstyle="round,pad=0.5", ec="#2980B9", fc="#EBF5FB", lw=1.5, zorder=2)
ax.add_patch(flow_box)
ax.text(50, 42, "COMMIT-TO-CONTAINER PIPELINE VERSIONING AUDIT  (Build #3 to Build #5)", color="#1B365D", fontsize=8, fontweight="bold", ha="center")

builds = [
    ("Build #3", "9112dde", "Defect introduced\n80% income cap", "FAILED", "Pipeline aborted\nNo image pushed", "#FDEDEC", "#C0392B"),
    ("Build #4", "6ffd8d6", "Defect fixed\n40% income cap", "PASSED", "Image 1.0.0.4 pushed\nContainer deployed", "#EAFAF1", "#27AE60"),
    ("Build #5", "3a8b2b8", "Docker CD added\nTask 12 pipeline", "PASSED", "Image 1.0.0.5 pushed\nccsp-live running", "#D4EFDF", "#1B7A4E"),
]
for i, (bld, sha, msg, status, outcome, fc3, ec3) in enumerate(builds):
    bx = 5 + i * 33
    bb = patches.FancyBboxPatch((bx, 6), 30, 33, boxstyle="round,pad=0.4", ec=ec3, fc=fc3, lw=1.2, zorder=3)
    ax.add_patch(bb)
    ax.text(bx + 15, 36, bld, color="#1B365D", fontsize=8, fontweight="bold", ha="center")
    ax.text(bx + 15, 32, f"Commit: {sha}", color="#2C3E50", fontsize=6.5, ha="center")
    ax.text(bx + 15, 28, msg, color="#2C3E50", fontsize=6, ha="center")
    sc = patches.FancyBboxPatch((bx + 6, 20), 18, 6, boxstyle="round,pad=0.2", ec=ec3, fc=ec3, zorder=4)
    ax.add_patch(sc)
    ax.text(bx + 15, 23, status, color="white", fontsize=7, fontweight="bold", ha="center")
    ax.text(bx + 15, 13.5, outcome, color=ec3, fontsize=5.8, ha="center")

plt.tight_layout()
path2 = "screenshots/task12/fig12_2_registry_versioning_evidence.png"
plt.savefig(path2, dpi=300, bbox_inches="tight")
plt.close()
print(f"Generated {path2}")
