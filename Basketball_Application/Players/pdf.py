
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib import colors
from io import BytesIO
import datetime

def generate_player_report(report):

    buffer = BytesIO()
    

    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    

    styles = getSampleStyleSheet()
    
   
    title_style = ParagraphStyle(
        'title_style',
        parent=styles['Heading1'],
        fontSize=20,
        alignment=1,  # Center aligned
        spaceAfter=0.5*inch
    )
    
    section_style = ParagraphStyle(
        'section_style',
        parent=styles['Heading2'],
        fontSize=14,
        spaceBefore=0.3*inch,
        spaceAfter=0.1*inch
    )
    
   
    current_time = datetime.datetime.now().strftime("%H:%M")
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, height - 50, "Report")
    pdf.drawString(width - 100, height - 50, current_time)
    
    title = Paragraph(f"Report for {report.player.name}", title_style)
    title.wrapOn(pdf, width - 100, height)
    title.drawOn(pdf, 50, height - 100)
    
    overview_title = Paragraph("Overview", section_style)
    overview_title.wrapOn(pdf, width - 100, height)
    overview_title.drawOn(pdf, 50, height - 150)
    
    overview_content = Paragraph(report.overview, styles['BodyText'])
    overview_content.wrapOn(pdf, width - 100, height)
    overview_content.drawOn(pdf, 50, height - 180)

    strength_title = Paragraph("Strength", section_style)
    strength_title.wrapOn(pdf, width - 100, height)
    strength_title.drawOn(pdf, 50, height - 230)
    
    strength_content = Paragraph(report.strength, styles['BodyText'])
    strength_content.wrapOn(pdf, width - 100, height)
    strength_content.drawOn(pdf, 50, height - 260)
    

    weaknesses_title = Paragraph("Weaknesses", section_style)
    weaknesses_title.wrapOn(pdf, width - 100, height)
    weaknesses_title.drawOn(pdf, 50, height - 310)
    
    weaknesses_content = Paragraph(report.weaknesses, styles['BodyText'])
    weaknesses_content.wrapOn(pdf, width - 100, height)
    weaknesses_content.drawOn(pdf, 50, height - 340)

    projection_title = Paragraph("Projection", section_style)
    projection_title.wrapOn(pdf, width - 100, height)
    projection_title.drawOn(pdf, 50, height - 390)
    
    projection_content = Paragraph(report.projection, styles['BodyText'])
    projection_content.wrapOn(pdf, width - 100, height)
    projection_content.drawOn(pdf, 50, height - 420)
    
  
    stats_title = Paragraph("Performance Stats", section_style)
    stats_title.wrapOn(pdf, width - 100, height)
    stats_title.drawOn(pdf, 50, height - 480)
    
    stats_data = [
        ["Points Per Game (PPG)", report.points_per_game],
        ["Field Goal % (FG%)", f"{report.field_goal_percentage}%"],
        ["Rebounds (RPG)", report.rebounds],
        ["Assists (APG)", report.assists],
        ["Steals & Blocks", report.steals_and_blocks]
    ]
    
    stats_table = Table(stats_data, colWidths=[3*inch, 1.5*inch])
    stats_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
    ]))
    
    stats_table.wrapOn(pdf, width - 100, height)
    stats_table.drawOn(pdf, 50, height - 550)
    

    pdf.showPage()
    pdf.save()
    
   
    buffer.seek(0)
    return buffer