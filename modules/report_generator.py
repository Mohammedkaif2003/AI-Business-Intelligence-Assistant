from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import TableStyle
from reportlab.lib.units import inch
from datetime import datetime


def generate_pdf(query, summary_text, dataframe=None, forecast_value=None):

    file_path = "AI_Executive_Report.pdf"

    doc = SimpleDocTemplate(file_path)
    elements = []

    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    heading_style = styles["Heading3"]
    normal_style = styles["Normal"]

    # Title
    elements.append(Paragraph("AI Business Intelligence Report", title_style))
    elements.append(Spacer(1, 0.2 * inch))

    # Timestamp
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    elements.append(Paragraph(f"Generated on: {now}", normal_style))
    elements.append(Spacer(1, 0.3 * inch))

    # Query Section
    elements.append(Paragraph("User Query", heading_style))
    elements.append(Paragraph(query, normal_style))
    elements.append(Spacer(1, 0.3 * inch))

    # Summary Section
    elements.append(Paragraph("AI Summary", heading_style))
    elements.append(Paragraph(summary_text, normal_style))
    elements.append(Spacer(1, 0.3 * inch))

    # Forecast
    if forecast_value is not None:

        elements.append(Paragraph("Forecast", heading_style))
        elements.append(
            Paragraph(
                f"Forecasted value: {round(float(forecast_value),2)}",
                normal_style
            )
        )
        elements.append(Spacer(1, 0.3 * inch))

    # Table Section
    if dataframe is not None and not dataframe.empty:

        elements.append(Paragraph("Data Analysis", heading_style))
        elements.append(Spacer(1, 0.2 * inch))

        # limit rows
        dataframe = dataframe.head(20)

        data = [dataframe.columns.tolist()] + dataframe.values.tolist()

        table = Table(data)

        table.setStyle(
            TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ALIGN', (1, 1), (-1, -1), 'CENTER')
            ])
        )

        elements.append(table)

    doc.build(elements)

    return file_path