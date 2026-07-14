"""
pdf_utils — lightweight PDF report renderer built on ReportLab.
Used by the Drug Report and Disease Diagnosis Report modules so both can be
viewed, downloaded, and printed as PDF, per the project requirements.
"""
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, ListFlowable, ListItem, HRFlowable)

_styles = getSampleStyleSheet()
_title_style = ParagraphStyle("MRTitle", parent=_styles["Title"], fontSize=18, spaceAfter=4)
_subtitle_style = ParagraphStyle("MRSubtitle", parent=_styles["Normal"], fontSize=10, textColor=colors.grey)
_h2_style = ParagraphStyle("MRH2", parent=_styles["Heading2"], fontSize=13, spaceBefore=14, spaceAfter=6,
                            textColor=colors.HexColor("#1d4ed8"))
_body_style = ParagraphStyle("MRBody", parent=_styles["Normal"], fontSize=10, leading=14)
_disclaimer_style = ParagraphStyle("MRDisclaimer", parent=_styles["Normal"], fontSize=8.5,
                                    textColor=colors.HexColor("#b91c1c"), leading=12)


def _para(text):
    return Paragraph(str(text).replace("\n", "<br/>"), _body_style)


def build_pdf(title, subtitle, meta_rows, sections, disclaimer=None):
    """
    title: str
    subtitle: str
    meta_rows: list[(label, value)] rendered as a small key/value table
    sections: list[(heading, content)] where content is a str, a list[str],
              or a dict (rendered as a key/value table)
    disclaimer: optional str shown at the bottom in red
    Returns: bytes (PDF file content)
    """
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                             topMargin=18 * mm, bottomMargin=16 * mm,
                             leftMargin=18 * mm, rightMargin=18 * mm)
    flow = [Paragraph(title, _title_style)]
    if subtitle:
        flow.append(Paragraph(subtitle, _subtitle_style))
    flow.append(Spacer(1, 8))
    flow.append(HRFlowable(width="100%", color=colors.HexColor("#e5e7eb")))
    flow.append(Spacer(1, 8))

    if meta_rows:
        data = [[Paragraph(f"<b>{k}</b>", _body_style), _para(v)] for k, v in meta_rows]
        t = Table(data, colWidths=[45 * mm, None])
        t.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
        ]))
        flow.append(t)
        flow.append(Spacer(1, 6))

    for heading, content in sections:
        flow.append(Paragraph(heading, _h2_style))
        if not content:
            flow.append(_para("Not specified."))
        elif isinstance(content, dict):
            data = [[Paragraph(f"<b>{k}</b>", _body_style), _para(v)] for k, v in content.items()]
            t = Table(data, colWidths=[45 * mm, None])
            t.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]))
            flow.append(t)
        elif isinstance(content, (list, tuple)):
            items = [ListItem(_para(x), leftIndent=6) for x in content]
            flow.append(ListFlowable(items, bulletType="bullet", start="•"))
        else:
            flow.append(_para(content))

    if disclaimer:
        flow.append(Spacer(1, 14))
        flow.append(HRFlowable(width="100%", color=colors.HexColor("#e5e7eb")))
        flow.append(Spacer(1, 6))
        flow.append(Paragraph(disclaimer, _disclaimer_style))

    doc.build(flow)
    return buf.getvalue()
