========================================================================
 DEVOPS LAB - AUTONOMOUS AI STARTER KIT (FOR ANTIGRAVITY)
========================================================================

FILES YOUR FRIEND NEEDS TO TOUCH (ONLY 2 FILES!):
------------------------------------------------------------------------
1. 'GEMINI.md':
   - Open it and change the 3 lines in Section 1 (Name, Roll No, Project Title).
2. 'ASSIGNMENT.md':
   - Paste your full raw row or 15 task descriptions from the professor's Excel sheet.

THAT'S IT! DO NOT TOUCH ANY OTHER CODE OR SCRIPTS.

------------------------------------------------------------------------
PREREQUISITES:
------------------------------------------------------------------------
Run this once in your terminal:
pip install python-docx matplotlib

------------------------------------------------------------------------
MASTER KICKOFF PROMPT (COPY-PASTE INTO ANTIGRAVITY):
------------------------------------------------------------------------
I need you to work as an autonomous Senior DevOps Engineer and Academic Researcher to complete our university DevOps Lab tasks for my assigned project.

Here is how our workspace is set up:
1. Read 'GEMINI.md' in the workspace root. It contains the absolute rules, my identity, document formatting standards, and quality criteria you MUST follow.
2. Read 'ASSIGNMENT.md'. It contains my official assigned project title and all 15 task descriptions from the university syllabus.
3. We have the approved department document templates at:
   - 'templates/template_task1.docx' (for Task 1)
   - 'templates/template_standard.docx' (for Tasks 2 to 15)
4. Never edit Word documents manually. All documentation must be generated programmatically using Python ('python-docx') following the architecture in 'scripts/doc_helper.py' and 'scripts/generate_task3.py'.
5. All code must be real, functional, and runnable (no mock placeholders, no fake screenshots). Always run tests, build Docker containers, and execute configuration management scripts live using terminal commands.
6. Store canonical reports in 'docs/' and archive older versions into 'docs/prev/'.

Please inspect the workspace, read Task 1 from 'ASSIGNMENT.md', initialize the project structure, implement the task, execute the code, and compile the official Word document using 'scripts/generate_task1.py'.
------------------------------------------------------------------------

FOR EACH SUBSEQUENT TASK (TASKS 2 TO 15):
------------------------------------------------------------------------
Just tell Antigravity:
"Proceed to Task {N}. Read Task {N} requirements from 'ASSIGNMENT.md', implement the necessary code and configs, run live terminal verification to capture output/screenshots, and generate the final Word document using a new 'scripts/generate_task{N}.py' script following GEMINI.md rules."
========================================================================
