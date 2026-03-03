from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import TableStyle
from reportlab.lib.units import inch


def generate_pdf(query, summary_text, dataframe=None, forecast_value=None):

    file_path = "AI_Executive_Report.pdf"
    doc = SimpleDocTemplate(file_path)
    elements = []

    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    normal_style = styles["Normal"]

    # Title
    elements.append(Paragraph("AI Business Intelligence Report", title_style))
    elements.append(Spacer(1, 0.3 * inch))

    # Query
    elements.append(Paragraph(f"<b>Query:</b> {query}", normal_style))
    elements.append(Spacer(1, 0.2 * inch))

    # Summary
    elements.append(Paragraph(f"<b>Summary:</b> {summary_text}", normal_style))
    elements.append(Spacer(1, 0.3 * inch))

    # Forecast value (if exists)
    if forecast_value is not None:
        elements.append(
            Paragraph(
                f"<b>Forecasted Revenue:</b> {round(float(forecast_value),2)}",
                normal_style
            )
        )
        elements.append(Spacer(1, 0.3 * inch))

    # Data table (if exists)
    if dataframe is not None:
        data = [dataframe.columns.tolist()] + dataframe.values.tolist()

        table = Table(data)
        table.setStyle(
            TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ])
        )

        elements.append(table)

    doc.build(elements)

    return file_path