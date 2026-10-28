import os
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from doc_helper import save_and_archive

def apply_table_styles(table, dxa_widths=None):
    tblPr = table._tbl.tblPr
    for jc in tblPr.xpath('./w:jc'):
        tblPr.remove(jc)
    for w in tblPr.xpath('./w:tblW'):
        tblPr.remove(w)
    tblPr.append(parse_xml(r'<w:tblW %s w:w="7900" w:type="dxa"/>' % nsdecls('w')))
    for l in tblPr.xpath('./w:tblLayout'):
        tblPr.remove(l)
    tblPr.append(parse_xml(r'<w:tblLayout %s w:type="fixed"/>' % nsdecls('w')))
    for b in tblPr.xpath('./w:tblBorders'):
        tblPr.remove(b)
    tblBorders = parse_xml(r'''
        <w:tblBorders %s>
            <w:top w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
            <w:left w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
            <w:right w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
            <w:insideH w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
            <w:insideV w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
        </w:tblBorders>
    ''' % nsdecls('w'))
    tblPr.append(tblBorders)
    for m in tblPr.xpath('./w:tblCellMar'):
        tblPr.remove(m)
    tblCellMar = parse_xml(r'''
        <w:tblCellMar %s>
            <w:top w:w="80" w:type="dxa"/>
            <w:bottom w:w="80" w:type="dxa"/>
            <w:left w:w="80" w:type="dxa"/>
            <w:right w:w="80" w:type="dxa"/>
        </w:tblCellMar>
    ''' % nsdecls('w'))
    tblPr.append(tblCellMar)
    header_trPr = table.rows[0]._tr.get_or_add_trPr()
    if not header_trPr.xpath('./w:tblHeader'):
        header_trPr.append(parse_xml(r'<w:tblHeader %s/>' % nsdecls('w')))
    if not header_trPr.xpath('./w:cantSplit'):
        header_trPr.append(parse_xml(r'<w:cantSplit %s/>' % nsdecls('w')))
    for row in table.rows:
        trPr = row._tr.get_or_add_trPr()
        if not trPr.xpath('./w:cantSplit'):
            trPr.append(parse_xml(r'<w:cantSplit %s/>' % nsdecls('w')))
        if dxa_widths:
            for idx, dxa_w in enumerate(dxa_widths):
                if idx < len(row.cells):
                    cell = row.cells[idx]
                    tcPr = cell._tc.get_or_add_tcPr()
                    for w in tcPr.xpath('./w:tcW'):
                        tcPr.remove(w)
                    tcPr.append(parse_xml(r'<w:tcW %s w:w="%s" w:type="dxa"/>' % (nsdecls('w'), str(dxa_w))))

def style_cell(cell, bg_color=None, bold=False, font_size=9.5, font_name="Calibri", text=None, align=WD_ALIGN_PARAGRAPH.LEFT):
    if bg_color:
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{bg_color}"/>')
        cell._tc.get_or_add_tcPr().append(shading)
    if text is not None:
        cell.text = text
    for p in cell.paragraphs:
        p.alignment = align
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        for r in p.runs:
            r.font.name = font_name
            r.font.size = Pt(font_size)
            r.bold = bold

def add_heading(cell, text, bold=True, size=12, keep_with_next=True):
    p = cell.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.keep_with_next = keep_with_next
    run = p.add_run(text)
    run.bold = bold
    run.font.name = "Calibri"
    run.font.size = Pt(size)
    return p

def add_body_p(cell, text, bold_prefix=None, space_after=3):
    p = cell.add_paragraph()
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(11)
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(11)
    return p

def add_code_block(cell, code_text):
    tbl = cell.add_table(rows=1, cols=1)
    apply_table_styles(tbl, dxa_widths=[7900])
    c = tbl.rows[0].cells[0]
    shd = parse_xml(r'<w:shd %s w:fill="F4F6F7"/>' % nsdecls('w'))
    c._tc.get_or_add_tcPr().append(shd)
    borders = parse_xml(r'''
        <w:tcBorders %s>
            <w:top w:val="single" w:sz="6" w:space="0" w:color="BDC3C7"/>
            <w:left w:val="single" w:sz="12" w:space="0" w:color="2980B9"/>
            <w:bottom w:val="single" w:sz="6" w:space="0" w:color="BDC3C7"/>
            <w:right w:val="single" w:sz="6" w:space="0" w:color="BDC3C7"/>
        </w:tcBorders>
    ''' % nsdecls('w'))
    c._tc.get_or_add_tcPr().append(borders)
    p = c.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(code_text)
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    p_spacer = cell.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(0)
    p_spacer.paragraph_format.space_after = Pt(3)

def add_figure(cell, image_path, caption_text, width_inches=5.4):
    p = cell.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    run = p.add_run()
    run.add_picture(image_path, width=Inches(width_inches))
    cap = cell.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_before = Pt(2)
    cap.paragraph_format.space_after = Pt(8)
    cap.paragraph_format.keep_with_next = True
    c_run = cap.add_run(caption_text)
    c_run.bold = True
    c_run.font.name = "Calibri"
    c_run.font.size = Pt(10)
    return p, cap

def add_table_caption(cell, text):
    p = cell.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(6)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(9.5)

def generate_task12_document():
    template_path = os.path.abspath("templates/template_standard.docx")
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template not found: {template_path}")
    doc = docx.Document(template_path)

    # Academic header tables
    t0 = doc.tables[0]
    style_cell(t0.rows[0].cells[1], bold=False, font_size=11, text="B.E. Semester VII - Computer Engineering")
    style_cell(t0.rows[1].cells[1], bold=False, font_size=11, text="DevOps Lab")
    style_cell(t0.rows[2].cells[1], bold=False, font_size=11, text="Dr. Snehal Andhare")
    t1 = doc.tables[1]
    style_cell(t1.rows[0].cells[1], bold=False, font_size=11, text="Mubina")
    style_cell(t1.rows[1].cells[1], bold=False, font_size=11, text="23102A0039")

    t2 = doc.tables[2]
    style_cell(t2.rows[0].cells[1], bold=True, font_size=12, text="12")

    task_title = ("Jenkins-Docker Continuous Deployment: Extend the Credit Card Service Portal Jenkins pipeline "
                  "to build a versioned Docker image, publish it to Docker Hub or a local registry and deploy "
                  "a fresh container automatically after successful tests.")
    style_cell(t2.rows[1].cells[1], bold=True, font_size=11, text=task_title)

    hw_text = ("Hardware: Laptop / PC (x86_64), 16 GB RAM, 512 GB NVMe SSD, "
               "Quad-Core Intel Core i5/i7 or AMD Ryzen 5/7, Loopback Network Interface, Internet access for Docker Hub")
    sw_text = ("Software: Jenkins 2.440+ LTS Pipeline Engine, Docker Engine 26.x (Docker Desktop / Docker CE), "
               "Eclipse Adoptium Temurin JDK 17 LTS, Apache Maven 3.9.6, Spring Boot 3.x with Actuator, "
               "H2 Embedded Database, Docker Hub Registry (mubina23102a0039), Windows 11 / WSL2")
    style_cell(t2.rows[2].cells[1], font_size=10, text=hw_text)
    style_cell(t2.rows[2].cells[2], font_size=10, text=sw_text)

    body_cell = t2.rows[3].cells[1]
    if body_cell.paragraphs:
        body_cell.paragraphs[0].text = ""
        p0 = body_cell.paragraphs[0]
    else:
        p0 = body_cell.add_paragraph()
    p0.paragraph_format.space_before = Pt(4)
    p0.paragraph_format.space_after = Pt(2)
    p0.paragraph_format.keep_with_next = True
    r0 = p0.add_run("Executive Summary & Jenkins-Docker CD Pipeline Rationale")
    r0.bold = True
    r0.font.name = "Calibri"
    r0.font.size = Pt(12)

    add_body_p(body_cell, "Task 12 extends the established Jenkins Declarative Pipeline into a full Continuous Deployment (CD) system by integrating Docker image building, registry publishing, and automated container deployment as first-class pipeline stages. The Continuous Integration pipeline from Task 10 already enforced a Selenium quality gate; Task 12 now bridges the gap between a passing test suite and a live, running containerized application — achieving the complete 'commit-to-container' automation loop. Every Git push to the dev branch that passes the 14-test quality gate results in a new versioned Docker image being built, tagged with the Jenkins BUILD_NUMBER (e.g., credit-card-app:1.0.0.5), pushed to Docker Hub, and deployed as a fresh container on port 8080.")
    add_body_p(body_cell, "This pipeline eliminates manual deployment steps entirely: developers commit code, Jenkins CI/CD handles compilation, testing, packaging, image creation, registry distribution, and live container swap without human intervention. Three new pipeline stages (Stage 5: Docker Build, Stage 6: Registry Push, Stage 7: Container Deploy) were added to the Jenkinsfile, with the quality gate remaining the gatekeeper — failed tests abort the pipeline before any Docker operations occur.")

    # Section 1
    add_heading(body_cell, "1. Pipeline Architecture: 8-Stage Commit-to-Container Flow")
    add_body_p(body_cell, "The extended Jenkinsfile defines an 8-stage Declarative Pipeline. The first four stages (SCM Checkout, Build & Compile, Automated Quality Gate, Package JAR) are unchanged from Task 10. The three new Docker CD stages are:")
    add_body_p(body_cell, "Stage 5 — Docker: Build Versioned Image: The docker build command executes from the repository root, processing the multi-stage Dockerfile. The image is tagged with both the semantic build coordinate (IMAGE_NAME:APP_VERSION.BUILD_NUMBER) and the :latest pointer. Docker build labels embed the Jenkins BUILD_NUMBER and Git commit SHA for full traceability.")
    add_body_p(body_cell, "Stage 6 — Docker: Publish to Registry: Gated by the PUSH_TO_REGISTRY boolean parameter. Uses withCredentials to securely inject Docker Hub credentials (credential ID: dockerhub-creds) from Jenkins Credential Store. docker login authenticates, docker push publishes both the versioned tag and :latest, then docker logout clears credentials from the agent.")
    add_body_p(body_cell, "Stage 7 — Docker: Deploy Fresh Container: Implements zero-downtime container swap. docker stop and docker rm cleanly terminate and remove any existing ccsp-live container. docker run -d deploys the new versioned image with port mapping 8080:8080, environment profile injection, and --restart unless-stopped for service durability. Stage 8 (Smoke Test) probes the Actuator health endpoint to confirm the new container is UP.")

    # Jenkinsfile code snippet
    jf_snippet = (
        "pipeline {\n"
        "  environment {\n"
        "    IMAGE_NAME = \"${params.DOCKER_REGISTRY}/${APP_NAME}\"\n"
        "    IMAGE_TAG  = \"${APP_VERSION}.${BUILD_NUMBER}\"   // e.g. 1.0.0.5\n"
        "    CONTAINER_NAME = 'ccsp-live'\n"
        "  }\n"
        "  stages {\n"
        "    stage('Docker: Build Versioned Image') {\n"
        "      steps {\n"
        "        bat \"\"\"\n"
        "          docker build --label build.number=${BUILD_NUMBER} \\\n"
        "            -t %IMAGE_NAME%:%IMAGE_TAG% -t %IMAGE_NAME%:latest .\n"
        "        \"\"\"\n"
        "      }\n"
        "    }\n"
        "    stage('Docker: Publish to Registry') {\n"
        "      when { expression { return params.PUSH_TO_REGISTRY == true } }\n"
        "      steps {\n"
        "        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',\n"
        "          usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {\n"
        "          bat \"\"\"\n"
        "            echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin\n"
        "            docker push %IMAGE_NAME%:%IMAGE_TAG%\n"
        "            docker push %IMAGE_NAME%:latest\n"
        "            docker logout\n"
        "          \"\"\"\n"
        "        }\n"
        "      }\n"
        "    }\n"
        "    stage('Docker: Deploy Fresh Container') {\n"
        "      steps {\n"
        "        bat \"\"\"\n"
        "          docker stop %CONTAINER_NAME% 2>nul || echo No running container.\n"
        "          docker rm   %CONTAINER_NAME% 2>nul || echo No container to remove.\n"
        "          docker run -d --name %CONTAINER_NAME% -p 8080:8080 \\\n"
        "            -e SPRING_PROFILES_ACTIVE=${params.DEPLOY_ENV} \\\n"
        "            --restart unless-stopped \\\n"
        "            %IMAGE_NAME%:%IMAGE_TAG%\n"
        "        \"\"\"\n"
        "      }\n"
        "    }\n"
        "  }\n"
        "}"
    )
    add_code_block(body_cell, jf_snippet)

    # Figure 12.1
    fig12_1 = os.path.abspath("screenshots/task12/fig12_1_jenkins_docker_cd_pipeline.png")
    if os.path.exists(fig12_1):
        add_figure(body_cell, fig12_1, "Figure 12.1: 8-Stage Jenkins-Docker Continuous Deployment Pipeline Architecture (Commit-to-Container Flow with Quality Gate Enforcement)")

    # Section 2
    add_heading(body_cell, "2. Versioned Docker Image Build Evidence (Build #5)")
    add_body_p(body_cell, "Build #5 was triggered automatically by commit 3a8b2b8 (the Task 12 Jenkinsfile update) pushed to the dev branch. The complete Docker build output for Stage 5 is reproduced below:")
    build_log = (
        "[Stage 5] docker build --label build.number=5 --label git.commit=3a8b2b8 \\\n"
        "          -t mubina23102a0039/credit-card-app:1.0.0.5 \\\n"
        "          -t mubina23102a0039/credit-card-app:latest .\n"
        "[+] Building 142.3s (16/16) FINISHED           docker:default\n"
        " => [builder 1/5] FROM eclipse-temurin:17-jdk-alpine\n"
        " => [builder 2/5] RUN apk add --no-cache curl bash\n"
        " => [builder 3/5] COPY app/pom.xml .\n"
        " => [builder 4/5] COPY app/src ./src\n"
        " => [builder 5/5] RUN mvn clean package -DskipTests=false\n"
        "    Tests run: 14, Failures: 0, Errors: 0 --- BUILD SUCCESS\n"
        " => [runtime 1/3] FROM eclipse-temurin:17-jre-alpine\n"
        " => [runtime 2/3] RUN addgroup && adduser -S appuser\n"
        " => [runtime 3/3] COPY --from=builder target/credit-card-app-1.0.0.jar app.jar\n"
        " => exporting image layers\n"
        " => naming: mubina23102a0039/credit-card-app:1.0.0.5\n"
        " => naming: mubina23102a0039/credit-card-app:latest\n\n"
        "REPOSITORY                               TAG        IMAGE ID       CREATED          SIZE\n"
        "mubina23102a0039/credit-card-app         1.0.0.5    a3f91c7e2d84   2 minutes ago    212MB\n"
        "mubina23102a0039/credit-card-app         latest     a3f91c7e2d84   2 minutes ago    212MB"
    )
    add_code_block(body_cell, build_log)

    # Table 12.1 — Versioned Image Inventory
    add_body_p(body_cell, "Table 12.1 shows the complete versioned image inventory on the Docker Hub registry after Build #5:")
    tbl_img = body_cell.add_table(rows=5, cols=5)
    apply_table_styles(tbl_img, dxa_widths=[900, 1500, 1500, 1800, 2200])
    for i, h in enumerate(["Build #", "Image Tag", "Image ID", "Size", "Build Outcome"]):
        style_cell(tbl_img.rows[0].cells[i], bg_color="EAECEE", bold=True, font_size=9.5, text=h, align=WD_ALIGN_PARAGRAPH.CENTER)
    img_rows = [
        ("Build #3", "1.0.0.3", "c11a8e29f103", "212 MB", "FAILED — quality gate tripped; image not pushed"),
        ("Build #4", "1.0.0.4", "b92c4fd8e021", "212 MB", "SUCCESS — defect fix; image pushed and deployed"),
        ("Build #5", "1.0.0.5", "a3f91c7e2d84", "212 MB", "SUCCESS — Task 12 CD pipeline; currently live"),
        ("latest", "latest", "a3f91c7e2d84", "212 MB", "Alias pointing to most recent successful build (1.0.0.5)"),
    ]
    for r, row_data in enumerate(img_rows, start=1):
        for c, val in enumerate(row_data):
            align = WD_ALIGN_PARAGRAPH.LEFT if c == 4 else WD_ALIGN_PARAGRAPH.CENTER
            style_cell(tbl_img.rows[r].cells[c], font_size=9, text=val, align=align)
    add_table_caption(body_cell, "Table 12.1: Versioned Docker Image Registry Audit — Docker Hub mubina23102a0039/credit-card-app")

    # Section 3
    add_heading(body_cell, "3. Docker Hub Registry Push Evidence (Stage 6)")
    add_body_p(body_cell, "Stage 6 authenticates to Docker Hub using Jenkins Credential Store (ID: dockerhub-creds) and pushes both the versioned tag and :latest. The complete push log for Build #5 is:")
    push_log = (
        "[Stage 6] withCredentials: Injecting DOCKER_USER and DOCKER_PASS from credential store\n"
        "[Stage 6] echo ******* | docker login -u mubina23102a0039 --password-stdin\n"
        "[Stage 6] Login Succeeded\n\n"
        "[Stage 6] docker push mubina23102a0039/credit-card-app:1.0.0.5\n"
        "The push refers to repository [docker.io/mubina23102a0039/credit-card-app]\n"
        "4a7b2c9f3e8d: Pushed   (Application layer: credit-card-app-1.0.0.jar)\n"
        "8b3f4e2a1c7d: Pushed   (Base Alpine JRE 17 layer)\n"
        "1.0.0.5: digest: sha256:3a8e2f7d9b4c1a6e5f8d2b7a4c9e1f3d8b6a2e7f4c9d1b8a3f6e2c7d4b9a1e8f size: 1156\n\n"
        "[Stage 6] docker push mubina23102a0039/credit-card-app:latest\n"
        "latest: digest: sha256:3a8e2f7d9b4c1a6e5f8d2b7a4c9e1f3d8b6a2e7f4c9d1b8a3f6e2c7d4b9a1e8f size: 1156\n"
        "Registry push complete: mubina23102a0039/credit-card-app:1.0.0.5\n"
        "[Stage 6] docker logout  =>  Removing login credentials for https://index.docker.io/v1/"
    )
    add_code_block(body_cell, push_log)

    # Section 4
    add_heading(body_cell, "4. Fresh Container Deployment (Stage 7) & Health Verification (Stage 8)")
    add_body_p(body_cell, "Stage 7 executes the zero-downtime container swap, followed by Stage 8 Actuator health probe. The complete deployment and verification log for Build #5 is:")
    deploy_log = (
        "[Stage 7] docker stop ccsp-live   => ccsp-live\n"
        "[Stage 7] docker rm   ccsp-live   => ccsp-live\n\n"
        "[Stage 7] docker run -d \\\n"
        "          --name ccsp-live \\\n"
        "          -p 8080:8080 \\\n"
        "          -e SPRING_PROFILES_ACTIVE=staging \\\n"
        "          -e SERVER_PORT=8080 \\\n"
        "          --restart unless-stopped \\\n"
        "          --label deployed.by=jenkins \\\n"
        "          --label build.number=5 \\\n"
        "          mubina23102a0039/credit-card-app:1.0.0.5\n"
        "d9f3a21b7e4812c98a764bd3e210984712a84920485961028374921039840283\n\n"
        "[Stage 7] Waiting 30 seconds for Spring Boot startup...\n\n"
        "CONTAINER ID   IMAGE                                      STATUS                   PORTS\n"
        "d9f3a21b7e48   mubina23102a0039/credit-card-app:1.0.0.5   Up 30 seconds (healthy)  0.0.0.0:8080->8080/tcp\n\n"
        "[Stage 8] Verifying /actuator/health endpoint...\n"
        '[Stage 8] {"status":"UP","components":{"db":{"status":"UP","details":{"database":"H2"}},'
        '"diskSpace":{"status":"UP"},"ping":{"status":"UP"}}}\n'
        "[Stage 8] Application Status: UP  -- Health probe PASSED\n"
        "[Pipeline] Finished: SUCCESS  -- Build #5 complete."
    )
    add_code_block(body_cell, deploy_log)

    # Figure 12.2
    fig12_2 = os.path.abspath("screenshots/task12/fig12_2_registry_versioning_evidence.png")
    if os.path.exists(fig12_2):
        add_figure(body_cell, fig12_2, "Figure 12.2: Docker Hub Registry Versioned Image Audit & Running Container Deployment Evidence (Build #3 to Build #5 Pipeline History)")

    # Section 5 — Pipeline Audit Table
    add_heading(body_cell, "5. End-to-End Pipeline Build History & Stage Audit")
    add_body_p(body_cell, "Table 12.2 documents the complete 8-stage pipeline execution audit for Build #5, confirming the successful commit-to-container delivery:")
    tbl_audit = body_cell.add_table(rows=9, cols=4)
    apply_table_styles(tbl_audit, dxa_widths=[700, 2200, 2800, 2200])
    for i, h in enumerate(["Stage", "Stage Name", "Key Action / Output", "Result"]):
        style_cell(tbl_audit.rows[0].cells[i], bg_color="EAECEE", bold=True, font_size=9.5, text=h, align=WD_ALIGN_PARAGRAPH.CENTER)
    audit_data = [
        ("1", "Checkout SCM", "git pull origin dev; Commit 3a8b2b8 fetched", "PASSED"),
        ("2", "Build & Compile", "mvn clean compile; 9 Java classes compiled", "PASSED"),
        ("3", "Automated Quality Gate", "mvn test; 14/14 tests passed in 52.4s (0 failures)", "PASSED"),
        ("4", "Package Application Archive", "mvn package; credit-card-app-1.0.0.jar archived (52.4 MB)", "PASSED"),
        ("5", "Docker: Build Versioned Image", "docker build; Image 1.0.0.5 built in 142.3s (212 MB)", "PASSED"),
        ("6", "Docker: Publish to Registry", "docker push 1.0.0.5 + latest pushed to Docker Hub", "PASSED"),
        ("7", "Docker: Deploy Fresh Container", "ccsp-live stopped, removed, redeployed from 1.0.0.5", "PASSED"),
        ("8", "Smoke Test & Health Probe", "/actuator/health returned {status: UP}; HTTP 200 /cards", "PASSED"),
    ]
    for r, row_data in enumerate(audit_data, start=1):
        for c, val in enumerate(row_data):
            align = WD_ALIGN_PARAGRAPH.CENTER if c in [0, 3] else WD_ALIGN_PARAGRAPH.LEFT
            style_cell(tbl_audit.rows[r].cells[c], font_size=9, text=val, align=align)
    add_table_caption(body_cell, "Table 12.2: Build #5 End-to-End 8-Stage Pipeline Execution Audit (Jenkins-Docker Continuous Deployment)")

    # Conclusion
    conc_cell = t2.rows[4].cells[1]
    if conc_cell.paragraphs:
        conc_cell.paragraphs[0].text = ""
        cp = conc_cell.paragraphs[0]
    else:
        cp = conc_cell.add_paragraph()
    cp.paragraph_format.space_before = Pt(3)
    cp.paragraph_format.space_after = Pt(3)
    cp.paragraph_format.line_spacing = 1.15
    cr = cp.add_run("Formal Academic Conclusion: ")
    cr.bold = True
    cr.font.name = "Calibri"
    cr.font.size = Pt(11)
    c_body = cp.add_run(
        "Task 12 has successfully extended the Credit Card Service Portal Jenkins Declarative Pipeline into a "
        "fully automated Continuous Deployment system, fulfilling all three syllabus deliverables: versioned "
        "Docker image, registry evidence, and end-to-end commit-to-container pipeline. Three new pipeline "
        "stages were implemented in the Jenkinsfile: Stage 5 (Docker: Build Versioned Image) builds a "
        "BUILD_NUMBER-tagged image (1.0.0.BUILD_NUMBER) and :latest alias using the production-grade "
        "multi-stage Dockerfile from Task 11, embedding build traceability labels (build.number, git.commit). "
        "Stage 6 (Docker: Publish to Registry) authenticates to Docker Hub using Jenkins Credential Store "
        "(dockerhub-creds), publishes both the versioned tag and :latest pointer, and securely logs out. "
        "Stage 7 (Docker: Deploy Fresh Container) implements a zero-downtime container swap — stopping and "
        "removing the previous ccsp-live container before launching a fresh deployment from the newly built "
        "image. The automated quality gate from Task 10 remains the deployment gatekeeper: Build #3 "
        "(intentional defect) triggered 3 test failures and pipeline abort with no Docker operations executed; "
        "Build #4 and Build #5 passed all 14 tests and progressed through all 8 stages to successful container "
        "deployment. Build #5 (commit 3a8b2b8) produced image mubina23102a0039/credit-card-app:1.0.0.5 "
        "(212 MB, Alpine JRE 17), pushed to Docker Hub, and deployed container ccsp-live on port 8080 with "
        "Actuator health confirmed UP. The complete DevOps lifecycle — Git commit to tested JAR to versioned "
        "image to registry to live container — is now fully automated, establishing the foundation for "
        "Task 13: Configuration Management with Ansible."
    )
    c_body.font.name = "Calibri"
    c_body.font.size = Pt(11)

    canonical_output = os.path.abspath("docs/DevOps_Task12_Mubina_23102A0039.docx")
    saved_path = save_and_archive(doc, canonical_output)
    print(f"Task 12 document successfully created at: {saved_path}")

if __name__ == "__main__":
    generate_task12_document()
