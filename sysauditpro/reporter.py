from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from xml.sax.saxutils import escape

def generate_report(audit_results):
    """Erstellt einen PDF-Bericht aus den Audit-Ergebnissen."""
    filename = "audit_report.pdf"
    document = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    normal_style = styles['BodyText']
    wrapped_style = ParagraphStyle('Wrapped', parent=normal_style, wordWrap='CJK')

    elements = []

    # Titel des Dokuments
    title = Paragraph("Cybersecurity Audit Report", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))

    for section, details in audit_results.items():
        section_title = Paragraph(section, styles['Heading2'])
        elements.append(section_title)
        elements.append(Spacer(1, 12))

        if isinstance(details, dict):
            for key, value in details.items():
                key_paragraph = Paragraph(f"<b>{escape(key)}:</b>", styles['BodyText'])
                value_paragraph = Paragraph(escape(str(value)), wrapped_style)
                elements.append(key_paragraph)
                elements.append(value_paragraph)
                elements.append(Spacer(1, 12))
        else:
            text = Paragraph(escape(details), wrapped_style)
            elements.append(text)
            elements.append(Spacer(1, 12))

    document.build(elements)
    return filename

def save_report(path):
    """Platzhalterfunktion, um den Bericht in einem bestimmten Pfad zu speichern oder zu senden."""
    # Implementieren Sie je nach Bedarf Logik zum Speichern oder Senden des Berichts.
    print(f"Report saved to {path}")
