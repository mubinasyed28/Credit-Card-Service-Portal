import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
import fitz  # PyMuPDF to check exact page count

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, total_pages):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        
        # Draw header on pages 2+
        if self._pageNumber > 1:
            self.drawString(36, 756, "Credit Card Service Portal (CCSP) — Comprehensive DevOps & Viva Guide")
            self.drawRightString(576, 756, "Mubina | 23102A0039")
            self.setStrokeColor(colors.HexColor("#D0D7DE"))
            self.setLineWidth(0.5)
            self.line(36, 750, 576, 750)
            
        # Draw footer on all pages
        self.setStrokeColor(colors.HexColor("#D0D7DE"))
        self.setLineWidth(0.5)
        self.line(36, 38, 576, 38)
        self.drawString(36, 26, "Department of Computer Engineering | DevOps Lab (Sem VII) | Evaluator: Dr. Snehal Andhare")
        page_text = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(576, 26, page_text)
        self.restoreState()

print("Canvas class defined successfully.")
