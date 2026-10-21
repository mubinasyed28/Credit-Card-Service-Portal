import docx

doc = docx.Document("docs/DevOps_WhitePaper_Mubina_23102A0039.docx")
xml = doc._body._element.xml
page_breaks = xml.count('w:type="page"')
print("Total explicit page breaks found:", page_breaks)
print("Which corresponds to exactly", page_breaks + 1, "distinct pages!")

# Print headings across the document
for p in doc.paragraphs:
    if p.text.startswith(("ABSTRACT", "1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "DEPARTMENT", "ENTERPRISE DEVOPS")):
        print(f"Heading: {p.text[:70]}")
