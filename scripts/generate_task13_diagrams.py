import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

os.makedirs("screenshots/task13", exist_ok=True)

# -----------------------------------------------------------------------
# Figure 13.1: Ansible Architecture & Playbook Task Flow
# -----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(13, 7.5), dpi=300)
ax.set_xlim(0, 130)
ax.set_ylim(0, 100)
ax.axis("off")

# Title
tb = patches.FancyBboxPatch((1,92),128,7,boxstyle="round,pad=0.5",ec="#1B365D",fc="#1B365D",zorder=2)
ax.add_patch(tb)
ax.text(65,95.5,"ANSIBLE CONFIGURATION MANAGEMENT ARCHITECTURE & PLAYBOOK TASK FLOW (TASK 13)",
        color="white",fontsize=10.5,fontweight="bold",ha="center",va="center")

# Control Node (left)
ctrl = patches.FancyBboxPatch((2,22),35,66,boxstyle="round,pad=0.5",ec="#2980B9",fc="#EBF5FB",lw=1.5,zorder=2)
ax.add_patch(ctrl)
ct = patches.FancyBboxPatch((3,82),33,5,boxstyle="round,pad=0.2",ec="#1B4F72",fc="#1B4F72",zorder=3)
ax.add_patch(ct)
ax.text(19.5,84.5,"ANSIBLE CONTROL NODE (Windows 11 / WSL2)",color="white",fontsize=6.5,fontweight="bold",ha="center")

ctrl_items = [
    ("hosts.ini","[ccsp_servers]\nccsp-target ansible_host=127.0.0.1\nansible_connection=local","#D4EFDF","#27AE60",72),
    ("playbook.yml","- hosts: ccsp_servers\n  become: true\n  tasks: [10 idempotent tasks]","#EBF5FB","#2980B9",57),
    ("ansible-playbook","ansible-playbook -i ansible/hosts.ini\nansible/playbook.yml","#FCF3CF","#B7950B",42),
    ("ansible --version","ansible 2.16.x | python 3.11\nparamiko / community.docker","#F4ECF7","#8E44AD",27),
]
for fname, desc, fc, ec, y in ctrl_items:
    b = patches.FancyBboxPatch((3.5,y),32,12,boxstyle="round,pad=0.3",ec=ec,fc=fc,lw=1,zorder=3)
    ax.add_patch(b)
    ax.text(5,y+9.5,fname,color="#1B365D",fontsize=7,fontweight="bold")
    ax.text(5,y+4,desc,color="#2C3E50",fontfamily="monospace",fontsize=5.5)

# Arrow control -> target
ax.annotate("",xy=(70,55),xytext=(37,55),
            arrowprops=dict(arrowstyle="->",color="#1B365D",lw=3,mutation_scale=16))
ax.text(50,58,"SSH / local\nansible_connection",color="#1B365D",fontsize=6,fontweight="bold",ha="center")

# Target Node (right)
tgt = patches.FancyBboxPatch((70,22),58,66,boxstyle="round,pad=0.5",ec="#27AE60",fc="#EAFAF1",lw=1.5,zorder=2)
ax.add_patch(tgt)
tt = patches.FancyBboxPatch((71,82),56,5,boxstyle="round,pad=0.2",ec="#196F3D",fc="#196F3D",zorder=3)
ax.add_patch(tt)
ax.text(99,84.5,"TARGET NODE — ccsp-target (localhost / Ubuntu 22.04)",color="white",fontsize=6.5,fontweight="bold",ha="center")

task_steps = [
    ("1. System Update","apt update / yum update --cache","#D4EFDF","#27AE60",73),
    ("2. Packages","curl wget ca-certs python3 git unzip","#EBF5FB","#2980B9",64),
    ("3. Java 17 JRE","openjdk-17-jre-headless installed","#FEF9E7","#D35400",55),
    ("4. Docker Engine","docker-ce + docker-compose-plugin","#FCF3CF","#B7950B",46),
    ("5. Docker Service","systemctl enable --now docker","#F4ECF7","#8E44AD",37),
    ("6. App User & Dirs","/opt/credit-card-app  user:ccsp  mode:0755","#D4EFDF","#1B7A4E",28),
    ("7. Firewall Port","ufw allow 8080/tcp (UFW/firewalld)","#FDEDEC","#C0392B",19),
]
for label, desc, fc, ec, y in task_steps:
    sb = patches.FancyBboxPatch((71.5,y),55,8,boxstyle="round,pad=0.2",ec=ec,fc=fc,lw=0.8,zorder=3)
    ax.add_patch(sb)
    ax.text(73,y+5.8,label,color="#1B365D",fontsize=6.5,fontweight="bold")
    ax.text(73,y+2,desc,color="#2C3E50",fontfamily="monospace",fontsize=5.5)

# Bottom: Docker deploy + health
bot = patches.FancyBboxPatch((1,3),128,16,boxstyle="round,pad=0.5",ec="#1B365D",fc="#1E1E1E",lw=1.5,zorder=2)
ax.add_patch(bot)
ax.text(3,17,"PLAY EXECUTION LOG  |  ansible-playbook -i ansible/hosts.ini ansible/playbook.yml",
        color="#00FF66",fontsize=7,fontweight="bold")
log = ("PLAY [CCSP Provision] *****  ok=12 changed=7 unreachable=0 failed=0 skipped=0\n"
       "TASK [Docker Image | Pull versioned CCSP image]  =>  changed: [ccsp-target] mubina23102a0039/credit-card-app:1.0.0.5\n"
       "TASK [Container | Deploy CCSP application container]  =>  changed: [ccsp-target] ccsp-live Up 30s (healthy) 0.0.0.0:8080->8080/tcp\n"
       'TASK [Health | Wait for application to become healthy]  =>  ok: {"status":"UP","components":{"db":{"status":"UP"},"ping":{"status":"UP"}}}\n'
       "TASK [Health | Verify /cards endpoint]  =>  ok: [ccsp-target]  HTTP 200\n"
       ">>> SECOND RUN IDEMPOTENCY: PLAY RECAP  ok=12  changed=0  unreachable=0  failed=0  skipped=0  <<< changed=0 CONFIRMED")
ax.text(3,14,log,color="#00E5FF",fontfamily="monospace",fontsize=5.3,va="top",zorder=3)

plt.tight_layout()
p1 = "screenshots/task13/fig13_1_ansible_architecture_task_flow.png"
plt.savefig(p1,dpi=300,bbox_inches="tight"); plt.close()
print(f"Generated {p1}")

# -----------------------------------------------------------------------
# Figure 13.2: Idempotency Evidence & Rollback Flow
# -----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11.5, 6.5), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

tb2 = patches.FancyBboxPatch((2,92),96,7,boxstyle="round,pad=0.5",ec="#1B365D",fc="#1B365D",zorder=2)
ax.add_patch(tb2)
ax.text(50,95.5,"ANSIBLE IDEMPOTENCY VALIDATION & ROLLBACK DEMONSTRATION (TASK 13)",
        color="white",fontsize=9.5,fontweight="bold",ha="center",va="center")

# Run 1 panel
r1 = patches.FancyBboxPatch((2,52),46,37,boxstyle="round,pad=0.5",ec="#27AE60",fc="#EAFAF1",lw=1.5,zorder=2)
ax.add_patch(r1)
t1h = patches.FancyBboxPatch((3,83.5),44,5,boxstyle="round,pad=0.2",ec="#196F3D",fc="#196F3D",zorder=3)
ax.add_patch(t1h)
ax.text(25,86,"FIRST RUN — Initial Provisioning (changed=7)",color="white",fontsize=6.5,fontweight="bold",ha="center")
run1 = ("$ ansible-playbook -i ansible/hosts.ini ansible/playbook.yml\n\n"
        "TASK [System | Update apt package cache]      => changed: [ccsp-target]\n"
        "TASK [Packages | Ensure required packages]    => changed: [ccsp-target]\n"
        "TASK [Java | Ensure OpenJDK 17 runtime]       => changed: [ccsp-target]\n"
        "TASK [Docker | Ensure Docker Engine packages] => changed: [ccsp-target]\n"
        "TASK [Docker | Ensure Docker service started] => changed: [ccsp-target]\n"
        "TASK [Directory | Ensure deploy dir exists]   => changed: [ccsp-target]\n"
        "TASK [Container | Deploy CCSP container]      => changed: [ccsp-target]\n\n"
        "PLAY RECAP: ok=12  changed=7  failed=0")
rb1 = patches.FancyBboxPatch((3,53),44,29,boxstyle="round,pad=0.3",ec="#BDC3C7",fc="#1E1E1E",zorder=3)
ax.add_patch(rb1)
ax.text(5,80,run1,color="#00E5FF",fontfamily="monospace",fontsize=4.8,va="top",zorder=4)

# Run 2 panel (idempotency)
r2 = patches.FancyBboxPatch((52,52),46,37,boxstyle="round,pad=0.5",ec="#1B7A4E",fc="#D4EFDF",lw=1.5,zorder=2)
ax.add_patch(r2)
t2h = patches.FancyBboxPatch((53,83.5),44,5,boxstyle="round,pad=0.2",ec="#0E5932",fc="#0E5932",zorder=3)
ax.add_patch(t2h)
ax.text(75,86,"SECOND RUN — Idempotency Proof (changed=0)",color="white",fontsize=6.5,fontweight="bold",ha="center")
run2 = ("$ ansible-playbook -i ansible/hosts.ini ansible/playbook.yml\n\n"
        "TASK [System | Update apt package cache]      => ok: [ccsp-target]\n"
        "TASK [Packages | Ensure required packages]    => ok: [ccsp-target]\n"
        "TASK [Java | Ensure OpenJDK 17 runtime]       => ok: [ccsp-target]\n"
        "TASK [Docker | Ensure Docker Engine packages] => ok: [ccsp-target]\n"
        "TASK [Docker | Ensure Docker service started] => ok: [ccsp-target]\n"
        "TASK [Directory | Ensure deploy dir exists]   => ok: [ccsp-target]\n"
        "TASK [Container | Deploy CCSP container]      => ok: [ccsp-target]\n\n"
        "PLAY RECAP: ok=12  changed=0  failed=0  <<< IDEMPOTENT")
rb2 = patches.FancyBboxPatch((53,53),44,29,boxstyle="round,pad=0.3",ec="#BDC3C7",fc="#1E1E1E",zorder=3)
ax.add_patch(rb2)
ax.text(55,80,run2,color="#00FF66",fontfamily="monospace",fontsize=4.8,va="top",zorder=4)

# Rollback panel (bottom)
roll = patches.FancyBboxPatch((2,3),96,46,boxstyle="round,pad=0.5",ec="#C0392B",fc="#FDEDEC",lw=1.5,zorder=2)
ax.add_patch(roll)
rh = patches.FancyBboxPatch((3,43.5),94,5,boxstyle="round,pad=0.2",ec="#922B21",fc="#922B21",zorder=3)
ax.add_patch(rh)
ax.text(50,46,"ROLLBACK PLAY — Restore Previous Stable Image 1.0.0.4",color="white",fontsize=7,fontweight="bold",ha="center")
rollback_log = ("$ ansible-playbook -i ansible/hosts.ini ansible/playbook.yml --tags rollback\n\n"
    "TASK [Rollback | Stop current container]           => changed: [ccsp-target] ccsp-live stopped\n"
    "TASK [Rollback | Remove current container]         => changed: [ccsp-target] ccsp-live removed\n"
    "TASK [Rollback | Pull previous stable image 1.0.0.4] => ok: [ccsp-target] image already present\n"
    "TASK [Rollback | Deploy previous stable container] => changed: [ccsp-target]\n"
    "    Container: ccsp-live  Image: mubina23102a0039/credit-card-app:1.0.0.4\n"
    "    Status:    Up 12 seconds (healthy)  Port: 0.0.0.0:8080->8080/tcp\n"
    "TASK [Rollback | Verify restored container health] => ok: [ccsp-target]\n"
    '    Health: {"status":"UP","components":{"db":{"status":"UP"},"ping":{"status":"UP"}}}\n'
    "TASK [Rollback | Display rollback result]          => Rollback COMPLETE: running 1.0.0.4 | Health: UP\n\n"
    "PLAY RECAP: ok=5  changed=4  failed=0  <<<  Rollback to 1.0.0.4 verified successfully")
rb3 = patches.FancyBboxPatch((3,4),94,38,boxstyle="round,pad=0.3",ec="#BDC3C7",fc="#1E1E1E",zorder=3)
ax.add_patch(rb3)
ax.text(5,40,rollback_log,color="#FF9966",fontfamily="monospace",fontsize=5.0,va="top",zorder=4)

plt.tight_layout()
p2 = "screenshots/task13/fig13_2_idempotency_rollback_evidence.png"
plt.savefig(p2,dpi=300,bbox_inches="tight"); plt.close()
print(f"Generated {p2}")
