
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

def generate_pdf_report(contract_type, risk_results):
    file_path = "contract_risk_report.pdf"
    doc = SimpleDocTemplate(file_path)
    elements = []

    styles = getSampleStyleSheet()

    elements.append(Paragraph(f"<b>Contract Type:</b> {contract_type}", styles["Normal"]))
    elements.append(Spacer(1, 0.3 * inch))
    elements.append(Paragraph(f"<b>Composite Risk Score:</b> {risk_results['composite_score']}", styles["Normal"]))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph("<b>Summary:</b>", styles["Normal"]))
    elements.append(Paragraph(risk_results["summary"], styles["Normal"]))
    elements.append(Spacer(1, 0.5 * inch))

    elements.append(Paragraph("<b>High Risk Clauses:</b>", styles["Normal"]))
    for clause in risk_results["high_risk_clauses"]:
        elements.append(Paragraph(clause[:300], styles["Normal"]))
        elements.append(Spacer(1, 0.2 * inch))

    doc.build(elements)
    return file_path
