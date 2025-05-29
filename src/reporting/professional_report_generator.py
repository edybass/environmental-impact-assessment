"""
Professional EIA Report Generator
Generates comprehensive environmental impact assessment reports to international standards

Created by: Edy Bassil
Email: bassileddy@gmail.com
"""

import os
import json
from datetime import datetime
from io import BytesIO
import base64

# Try importing professional PDF libraries
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch, cm
    from reportlab.platypus import (
        SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
        PageBreak, Image, Frame, PageTemplate, KeepTogether,
        Flowable, ListFlowable, ListItem, Preformatted
    )
    from reportlab.graphics.shapes import Drawing, Line, Rect
    from reportlab.graphics.charts.barcharts import VerticalBarChart
    from reportlab.graphics.charts.piecharts import Pie
    from reportlab.graphics.charts.legends import Legend
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("Warning: ReportLab not installed. Using fallback PDF generation.")

# Fallback HTML to PDF if reportlab not available
try:
    import pdfkit
    PDFKIT_AVAILABLE = True
except ImportError:
    PDFKIT_AVAILABLE = False


class ProfessionalEIAReport:
    """Professional Environmental Impact Assessment Report Generator"""
    
    def __init__(self, project_data, assessment_results):
        self.project_data = project_data
        self.assessment_results = assessment_results
        self.creation_date = datetime.now()
        self.styles = getSampleStyleSheet() if REPORTLAB_AVAILABLE else None
        self._setup_custom_styles()
        
    def _setup_custom_styles(self):
        """Setup professional report styles"""
        if not REPORTLAB_AVAILABLE:
            return
            
        # Title styles
        self.styles.add(ParagraphStyle(
            name='MainTitle',
            parent=self.styles['Title'],
            fontSize=24,
            textColor=colors.HexColor('#059669'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        # Chapter heading
        self.styles.add(ParagraphStyle(
            name='ChapterHeading',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#047857'),
            spaceAfter=20,
            spaceBefore=30,
            borderWidth=2,
            borderColor=colors.HexColor('#059669'),
            borderPadding=10
        ))
        
        # Section heading
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#374151'),
            spaceAfter=12,
            spaceBefore=20
        ))
        
        # Professional body text
        self.styles.add(ParagraphStyle(
            name='ProfessionalBody',
            parent=self.styles['BodyText'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceBefore=6,
            spaceAfter=6,
            leading=16
        ))
        
        # Executive summary style
        self.styles.add(ParagraphStyle(
            name='ExecutiveSummary',
            parent=self.styles['BodyText'],
            fontSize=12,
            textColor=colors.HexColor('#1f2937'),
            backColor=colors.HexColor('#f3f4f6'),
            borderWidth=1,
            borderColor=colors.HexColor('#d1d5db'),
            borderPadding=15,
            alignment=TA_JUSTIFY
        ))
        
        # Compliance status styles
        self.styles.add(ParagraphStyle(
            name='CompliantStatus',
            parent=self.styles['BodyText'],
            fontSize=11,
            textColor=colors.HexColor('#059669'),
            backColor=colors.HexColor('#d1fae5')
        ))
        
        self.styles.add(ParagraphStyle(
            name='NonCompliantStatus',
            parent=self.styles['BodyText'],
            fontSize=11,
            textColor=colors.HexColor('#dc2626'),
            backColor=colors.HexColor('#fee2e2')
        ))
        
    def generate_report(self, output_path=None):
        """Generate the comprehensive EIA report"""
        if REPORTLAB_AVAILABLE:
            return self._generate_reportlab_pdf(output_path)
        elif PDFKIT_AVAILABLE:
            return self._generate_pdfkit_pdf(output_path)
        else:
            return self._generate_html_report()
            
    def _generate_reportlab_pdf(self, output_path=None):
        """Generate professional PDF using ReportLab"""
        # Create buffer or file
        if output_path:
            buffer = output_path
        else:
            buffer = BytesIO()
            
        # Create document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72,
            title=f"Environmental Impact Assessment - {self.project_data.get('name', 'Project')}",
            author="EIA Pro Platform",
            subject="Comprehensive Environmental Impact Assessment Report",
            creator="Professional EIA Report Generator"
        )
        
        # Build story (content)
        story = []
        
        # Cover page
        story.extend(self._create_cover_page())
        story.append(PageBreak())
        
        # Table of contents
        story.extend(self._create_table_of_contents())
        story.append(PageBreak())
        
        # Executive summary
        story.extend(self._create_executive_summary())
        story.append(PageBreak())
        
        # 1. Introduction
        story.extend(self._create_introduction())
        
        # 2. Project Description
        story.extend(self._create_project_description())
        
        # 3. Regulatory Framework
        story.extend(self._create_regulatory_framework())
        
        # 4. Environmental Baseline
        story.extend(self._create_environmental_baseline())
        
        # 5. Impact Assessment Results
        story.extend(self._create_impact_assessment())
        
        # 6. Mitigation Measures
        story.extend(self._create_mitigation_measures())
        
        # 7. Environmental Management Plan
        story.extend(self._create_emp_section())
        
        # 8. Monitoring Programs
        story.extend(self._create_monitoring_programs())
        
        # 9. Conclusions and Recommendations
        story.extend(self._create_conclusions())
        
        # Appendices
        story.extend(self._create_appendices())
        
        # Build PDF
        doc.build(story, onFirstPage=self._add_header_footer, onLaterPages=self._add_header_footer)
        
        if not output_path:
            buffer.seek(0)
            return buffer.getvalue()
        return True
        
    def _create_cover_page(self):
        """Create professional cover page"""
        elements = []
        
        # Main title
        elements.append(Spacer(1, 2*inch))
        elements.append(Paragraph(
            "ENVIRONMENTAL IMPACT ASSESSMENT",
            self.styles['MainTitle']
        ))
        
        elements.append(Spacer(1, 0.5*inch))
        
        # Project name
        elements.append(Paragraph(
            f"<b>{self.project_data.get('name', 'Project Name')}</b>",
            ParagraphStyle(
                'ProjectTitle',
                parent=self.styles['Title'],
                fontSize=20,
                alignment=TA_CENTER
            )
        ))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Location
        elements.append(Paragraph(
            f"{self.project_data.get('location', 'Location')}",
            ParagraphStyle(
                'Location',
                parent=self.styles['Normal'],
                fontSize=16,
                alignment=TA_CENTER
            )
        ))
        
        elements.append(Spacer(1, 2*inch))
        
        # Report details box
        report_info = [
            ['Report Reference:', f"EIA-{datetime.now().strftime('%Y%m%d')}-001"],
            ['Prepared for:', self.project_data.get('client', 'Client Name')],
            ['Prepared by:', 'EIA Pro Platform - Environmental Engineering Division'],
            ['Date:', self.creation_date.strftime('%B %Y')],
            ['Status:', 'FINAL']
        ]
        
        info_table = Table(report_info, colWidths=[2.5*inch, 3.5*inch])
        info_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f9fafb')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
            ('LINEBELOW', (0, 0), (-1, -2), 1, colors.HexColor('#e5e7eb'))
        ]))
        
        elements.append(info_table)
        
        elements.append(Spacer(1, 1*inch))
        
        # Compliance statement
        elements.append(Paragraph(
            "This Environmental Impact Assessment has been prepared in accordance with:",
            self.styles['Normal']
        ))
        elements.append(Spacer(1, 0.2*inch))
        
        compliance_list = ListFlowable([
            ListItem(Paragraph("UAE Federal Law No. 24 of 1999", self.styles['Normal'])),
            ListItem(Paragraph("Local Environmental Regulations", self.styles['Normal'])),
            ListItem(Paragraph("International Finance Corporation (IFC) Performance Standards", self.styles['Normal'])),
            ListItem(Paragraph("ISO 14001:2015 Environmental Management Systems", self.styles['Normal']))
        ], bulletType='bullet')
        
        elements.append(compliance_list)
        
        return elements
        
    def _create_table_of_contents(self):
        """Create table of contents"""
        elements = []
        
        elements.append(Paragraph("TABLE OF CONTENTS", self.styles['ChapterHeading']))
        elements.append(Spacer(1, 0.5*inch))
        
        toc_data = [
            ['', 'Page'],
            ['EXECUTIVE SUMMARY', 'i'],
            ['1. INTRODUCTION', '1'],
            ['   1.1 Purpose and Scope', '1'],
            ['   1.2 EIA Methodology', '2'],
            ['2. PROJECT DESCRIPTION', '5'],
            ['   2.1 Project Overview', '5'],
            ['   2.2 Project Components', '7'],
            ['   2.3 Construction Activities', '10'],
            ['3. REGULATORY FRAMEWORK', '15'],
            ['   3.1 National Regulations', '15'],
            ['   3.2 International Standards', '18'],
            ['4. ENVIRONMENTAL BASELINE', '20'],
            ['   4.1 Physical Environment', '20'],
            ['   4.2 Biological Environment', '25'],
            ['   4.3 Socio-Economic Environment', '30'],
            ['5. IMPACT ASSESSMENT', '35'],
            ['   5.1 Air Quality Impacts', '35'],
            ['   5.2 Noise Impacts', '40'],
            ['   5.3 Water Resources', '45'],
            ['   5.4 Waste Management', '50'],
            ['   5.5 Biodiversity', '55'],
            ['   5.6 Soil and Geology', '60'],
            ['6. MITIGATION MEASURES', '65'],
            ['7. ENVIRONMENTAL MANAGEMENT PLAN', '75'],
            ['8. MONITORING PROGRAMS', '85'],
            ['9. CONCLUSIONS', '95'],
            ['APPENDICES', '100']
        ]
        
        toc_table = Table(toc_data, colWidths=[5*inch, 1*inch])
        toc_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8)
        ]))
        
        elements.append(toc_table)
        
        return elements
        
    def _create_executive_summary(self):
        """Create executive summary"""
        elements = []
        
        elements.append(Paragraph("EXECUTIVE SUMMARY", self.styles['ChapterHeading']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Get summary data
        summary = self.assessment_results.get('summary', {})
        compliance_score = summary.get('compliance_score', 0)
        
        # Overview
        elements.append(Paragraph(
            f"""This Environmental Impact Assessment (EIA) has been prepared for the 
            {self.project_data.get('name')} project located in {self.project_data.get('location')}. 
            The assessment evaluates potential environmental impacts during construction and operation phases, 
            and proposes comprehensive mitigation measures to ensure regulatory compliance and environmental sustainability.""",
            self.styles['ExecutiveSummary']
        ))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Key findings
        elements.append(Paragraph("<b>Key Findings:</b>", self.styles['SectionHeading']))
        
        # Overall compliance
        compliance_status = "COMPLIANT" if compliance_score >= 80 else "REQUIRES MITIGATION"
        compliance_color = colors.HexColor('#059669') if compliance_score >= 80 else colors.HexColor('#f59e0b')
        
        findings_data = [
            ['Overall Compliance Score:', f'{compliance_score}%'],
            ['Compliance Status:', compliance_status],
            ['Critical Issues Identified:', str(len(summary.get('critical_issues', [])))],
            ['Mitigation Measures Required:', str(summary.get('mitigation_count', 45))]
        ]
        
        findings_table = Table(findings_data, colWidths=[3*inch, 2*inch])
        findings_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 1), (1, 1), compliance_color),
            ('TEXTCOLOR', (1, 1), (1, 1), colors.white),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
            ('LINEBELOW', (0, 0), (-1, -2), 1, colors.HexColor('#e5e7eb'))
        ]))
        
        elements.append(findings_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Impact summary by module
        elements.append(Paragraph("<b>Environmental Impact Summary:</b>", self.styles['SectionHeading']))
        
        # Create impact summary chart
        drawing = Drawing(400, 200)
        bc = VerticalBarChart()
        bc.x = 50
        bc.y = 50
        bc.height = 125
        bc.width = 300
        
        # Sample data for each module
        module_scores = [
            ('Air', 85),
            ('Noise', 78),
            ('Water', 92),
            ('Waste', 88),
            ('Bio', 75),
            ('Soil', 90),
            ('Social', 82),
            ('Risk', 79)
        ]
        
        bc.data = [[score for _, score in module_scores]]
        bc.categoryAxis.categoryNames = [name for name, _ in module_scores]
        bc.bars[0].fillColor = colors.HexColor('#059669')
        bc.valueAxis.valueMin = 0
        bc.valueAxis.valueMax = 100
        bc.valueAxis.valueStep = 20
        
        drawing.add(bc)
        elements.append(drawing)
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Critical recommendations
        elements.append(Paragraph("<b>Critical Recommendations:</b>", self.styles['SectionHeading']))
        
        recommendations = [
            "Implement comprehensive dust suppression system during construction phase",
            "Install acoustic barriers at project boundaries near sensitive receptors",
            "Establish water recycling system to achieve 40% reuse target",
            "Develop detailed waste segregation and management procedures",
            "Conduct pre-construction biodiversity survey and relocation program",
            "Implement real-time environmental monitoring system"
        ]
        
        for rec in recommendations[:3]:  # Top 3 recommendations
            elements.append(Paragraph(f"• {rec}", self.styles['ProfessionalBody']))
            
        return elements
        
    def _create_introduction(self):
        """Create introduction chapter"""
        elements = []
        
        elements.append(PageBreak())
        elements.append(Paragraph("1. INTRODUCTION", self.styles['ChapterHeading']))
        elements.append(Spacer(1, 0.3*inch))
        
        elements.append(Paragraph("1.1 Purpose and Scope", self.styles['SectionHeading']))
        elements.append(Paragraph(
            """This Environmental Impact Assessment (EIA) has been prepared to identify, predict, and evaluate 
            the potential environmental impacts associated with the proposed development. The assessment aims to:""",
            self.styles['ProfessionalBody']
        ))
        
        objectives = ListFlowable([
            ListItem(Paragraph("Identify potential environmental impacts during construction and operation", self.styles['Normal'])),
            ListItem(Paragraph("Assess the significance of identified impacts", self.styles['Normal'])),
            ListItem(Paragraph("Propose mitigation measures to minimize adverse impacts", self.styles['Normal'])),
            ListItem(Paragraph("Ensure compliance with applicable environmental regulations", self.styles['Normal'])),
            ListItem(Paragraph("Develop monitoring programs for environmental management", self.styles['Normal']))
        ], bulletType='bullet')
        
        elements.append(objectives)
        elements.append(Spacer(1, 0.3*inch))
        
        elements.append(Paragraph("1.2 EIA Methodology", self.styles['SectionHeading']))
        elements.append(Paragraph(
            """The environmental assessment follows internationally recognized methodologies including:""",
            self.styles['ProfessionalBody']
        ))
        
        methodology = ListFlowable([
            ListItem(Paragraph("Screening and scoping of environmental aspects", self.styles['Normal'])),
            ListItem(Paragraph("Baseline environmental surveys and data collection", self.styles['Normal'])),
            ListItem(Paragraph("Impact prediction using quantitative modeling", self.styles['Normal'])),
            ListItem(Paragraph("Evaluation of impact significance", self.styles['Normal'])),
            ListItem(Paragraph("Development of mitigation hierarchy", self.styles['Normal'])),
            ListItem(Paragraph("Stakeholder consultation and engagement", self.styles['Normal']))
        ], bulletType='bullet')
        
        elements.append(methodology)
        
        return elements
        
    def _create_project_description(self):
        """Create project description chapter"""
        elements = []
        
        elements.append(PageBreak())
        elements.append(Paragraph("2. PROJECT DESCRIPTION", self.styles['ChapterHeading']))
        elements.append(Spacer(1, 0.3*inch))
        
        elements.append(Paragraph("2.1 Project Overview", self.styles['SectionHeading']))
        
        # Project details table
        project_details = [
            ['Project Parameter', 'Details'],
            ['Project Name:', self.project_data.get('name', 'N/A')],
            ['Project Type:', self.project_data.get('type', 'N/A').replace('_', ' ').title()],
            ['Location:', self.project_data.get('location', 'N/A')],
            ['Total Area:', f"{self.project_data.get('size', 0):,} m²"],
            ['Construction Duration:', f"{self.project_data.get('duration', 24)} months"],
            ['Estimated Investment:', f"${self.project_data.get('budget', 0):,.0f} Million"],
            ['Workforce:', f"{self.project_data.get('workers', 100)} workers"]
        ]
        
        details_table = Table(project_details, colWidths=[2.5*inch, 3.5*inch])
        details_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
            ('LINEBELOW', (0, 0), (-1, -2), 1, colors.HexColor('#e5e7eb')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
        ]))
        
        elements.append(details_table)
        
        elements.append(Spacer(1, 0.3*inch))
        
        elements.append(Paragraph("2.2 Project Components", self.styles['SectionHeading']))
        elements.append(Paragraph(
            """The project comprises the following major components:""",
            self.styles['ProfessionalBody']
        ))
        
        # Add components based on project type
        components = self._get_project_components()
        comp_list = ListFlowable([
            ListItem(Paragraph(comp, self.styles['Normal'])) for comp in components
        ], bulletType='bullet')
        
        elements.append(comp_list)
        
        return elements
        
    def _create_impact_assessment(self):
        """Create detailed impact assessment results"""
        elements = []
        
        elements.append(PageBreak())
        elements.append(Paragraph("5. ENVIRONMENTAL IMPACT ASSESSMENT", self.styles['ChapterHeading']))
        elements.append(Spacer(1, 0.3*inch))
        
        # For each assessment module
        modules = [
            ('air_quality', '5.1 Air Quality Impact Assessment'),
            ('noise_assessment', '5.2 Noise Impact Assessment'),
            ('water_resources', '5.3 Water Resources Assessment'),
            ('waste_management', '5.4 Waste Management Assessment'),
            ('biological_environment', '5.5 Biodiversity Impact Assessment'),
            ('soil_geology', '5.6 Soil and Geological Assessment')
        ]
        
        for module_key, title in modules:
            elements.append(Paragraph(title, self.styles['SectionHeading']))
            
            module_data = self.assessment_results.get('assessment_results', {}).get(module_key, {})
            
            if module_data.get('status') == 'assessed':
                # Add specific module results
                elements.extend(self._create_module_results(module_key, module_data))
            else:
                elements.append(Paragraph(
                    "Assessment pending or data not available.",
                    self.styles['ProfessionalBody']
                ))
                
            elements.append(Spacer(1, 0.3*inch))
            
        return elements
        
    def _create_module_results(self, module_key, data):
        """Create results for specific module"""
        elements = []
        
        if module_key == 'air_quality':
            # Air quality specific results
            results_data = [
                ['Parameter', 'Value', 'Standard', 'Status'],
                ['PM10 Concentration', f"{data.get('pm10_concentration', 0):.1f} µg/m³", '150 µg/m³', 
                 'Compliant' if data.get('pm10_concentration', 0) < 150 else 'Non-compliant'],
                ['PM2.5 Concentration', f"{data.get('pm25_concentration', 0):.1f} µg/m³", '65 µg/m³',
                 'Compliant' if data.get('pm25_concentration', 0) < 65 else 'Non-compliant'],
                ['Annual Emissions', f"{data.get('annual_emissions_tons', 0):.1f} tons/year", 'N/A', 'Calculated'],
                ['Mitigation Effectiveness', f"{data.get('mitigation_effectiveness', 0)}%", '>60%',
                 'Adequate' if data.get('mitigation_effectiveness', 0) > 60 else 'Improve']
            ]
            
        elif module_key == 'noise_assessment':
            results_data = [
                ['Parameter', 'Value', 'Standard', 'Status'],
                ['Peak Noise Level', f"{data.get('peak_noise_level', 0):.1f} dB(A)", '75 dB(A)',
                 'Compliant' if data.get('peak_noise_level', 0) < 75 else 'Non-compliant'],
                ['Equipment Count', f"{data.get('equipment_count', 0)} units", 'N/A', 'Assessed'],
                ['Distance Attenuation', f"{data.get('distance_attenuation', 0):.1f} dB", 'N/A', 'Calculated'],
                ['Night Work', data.get('night_work', False), 'Restricted', 
                 'Review' if data.get('night_work') else 'Compliant']
            ]
            
        elif module_key == 'water_resources':
            results_data = [
                ['Parameter', 'Value', 'Target', 'Status'],
                ['Water Demand', f"{data.get('operational_water_demand_m3_year', 0):,.0f} m³/year", 'Minimize', 'Assessed'],
                ['Recycling Rate', f"{data.get('recycling_potential', 0)}%", '>30%',
                 'Good' if data.get('recycling_potential', 0) > 30 else 'Improve'],
                ['Sustainability Score', f"{data.get('water_sustainability_score', 0)}/100", '>70',
                 'Good' if data.get('water_sustainability_score', 0) > 70 else 'Review']
            ]
            
        else:
            # Generic results table
            results_data = [
                ['Assessment Status', data.get('status', 'pending').title()],
                ['Compliance', data.get('compliance', 'Under Review')],
                ['Key Findings', 'See detailed analysis below']
            ]
            
        results_table = Table(results_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        results_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e5e7eb')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
            ('LINEBELOW', (0, 0), (-1, -2), 1, colors.HexColor('#e5e7eb')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
        ]))
        
        elements.append(results_table)
        
        return elements
        
    def _create_mitigation_measures(self):
        """Create mitigation measures chapter"""
        elements = []
        
        elements.append(PageBreak())
        elements.append(Paragraph("6. MITIGATION MEASURES", self.styles['ChapterHeading']))
        elements.append(Spacer(1, 0.3*inch))
        
        elements.append(Paragraph(
            """The following mitigation measures shall be implemented to minimize environmental impacts:""",
            self.styles['ProfessionalBody']
        ))
        
        # Mitigation hierarchy
        elements.append(Paragraph("6.1 Mitigation Hierarchy", self.styles['SectionHeading']))
        
        hierarchy_data = [
            ['Priority', 'Approach', 'Description'],
            ['1', 'AVOID', 'Modify project design to prevent impacts'],
            ['2', 'MINIMIZE', 'Reduce duration, intensity or extent of impacts'],
            ['3', 'RESTORE', 'Rehabilitate affected environment'],
            ['4', 'OFFSET', 'Compensate for residual impacts']
        ]
        
        hierarchy_table = Table(hierarchy_data, colWidths=[1*inch, 1.5*inch, 3.5*inch])
        hierarchy_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (1, 1), (1, -1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (1, -1), 'CENTER'),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
            ('LINEBELOW', (0, 0), (-1, -2), 1, colors.HexColor('#e5e7eb'))
        ]))
        
        elements.append(hierarchy_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Specific mitigation measures by impact
        elements.append(Paragraph("6.2 Specific Mitigation Measures", self.styles['SectionHeading']))
        
        # Air quality mitigation
        elements.append(Paragraph("<b>Air Quality Management:</b>", self.styles['Normal']))
        air_measures = [
            "Water spraying on unpaved roads every 2 hours during working hours",
            "Cover all trucks transporting loose materials",
            "Install wheel washing facilities at site exits",
            "Use Tier 4 or electric equipment where feasible",
            "Implement no-idling policy for vehicles and equipment"
        ]
        
        for measure in air_measures:
            elements.append(Paragraph(f"• {measure}", self.styles['ProfessionalBody']))
            
        elements.append(Spacer(1, 0.2*inch))
        
        # Noise mitigation
        elements.append(Paragraph("<b>Noise Control Measures:</b>", self.styles['Normal']))
        noise_measures = [
            "Install 3m high acoustic barriers at site boundaries",
            "Restrict noisy activities to 07:00-18:00 hours",
            "Use quieter equipment models and maintain properly",
            "Implement real-time noise monitoring system",
            "Provide advance notice to nearby receptors"
        ]
        
        for measure in noise_measures:
            elements.append(Paragraph(f"• {measure}", self.styles['ProfessionalBody']))
            
        return elements
        
    def _create_emp_section(self):
        """Create Environmental Management Plan section"""
        elements = []
        
        elements.append(PageBreak())
        elements.append(Paragraph("7. ENVIRONMENTAL MANAGEMENT PLAN", self.styles['ChapterHeading']))
        elements.append(Spacer(1, 0.3*inch))
        
        elements.append(Paragraph(
            """The Environmental Management Plan (EMP) provides a framework for implementing 
            mitigation measures and monitoring programs throughout the project lifecycle.""",
            self.styles['ProfessionalBody']
        ))
        
        # EMP components
        elements.append(Paragraph("7.1 EMP Structure", self.styles['SectionHeading']))
        
        # Get EMP data if available
        emp_data = self.assessment_results.get('assessment_results', {}).get('environmental_management_plan', {})
        
        emp_components = [
            ['Component', 'Responsibility', 'Frequency', 'Budget (USD)'],
            ['Air Quality Management', 'Environmental Manager', 'Daily', '$25,000/year'],
            ['Noise Monitoring', 'Safety Officer', 'Weekly', '$15,000/year'],
            ['Water Management', 'Site Engineer', 'Daily', '$30,000/year'],
            ['Waste Management', 'Waste Coordinator', 'Daily', '$45,000/year'],
            ['Biodiversity Protection', 'Environmental Specialist', 'Monthly', '$20,000/year'],
            ['Training Programs', 'HSE Manager', 'Monthly', '$10,000/year'],
            ['Auditing & Reporting', 'QA/QC Manager', 'Quarterly', '$15,000/year']
        ]
        
        emp_table = Table(emp_components, colWidths=[2.2*inch, 1.8*inch, 1*inch, 1*inch])
        emp_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (2, 0), (-1, -1), 'CENTER'),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
            ('LINEBELOW', (0, 0), (-1, -2), 1, colors.HexColor('#e5e7eb')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
        ]))
        
        elements.append(emp_table)
        
        return elements
        
    def _create_monitoring_programs(self):
        """Create monitoring programs section"""
        elements = []
        
        elements.append(PageBreak())
        elements.append(Paragraph("8. ENVIRONMENTAL MONITORING PROGRAMS", self.styles['ChapterHeading']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Monitoring matrix
        monitoring_data = [
            ['Parameter', 'Location', 'Frequency', 'Method', 'Standard'],
            ['PM10/PM2.5', 'Site boundary', 'Continuous', 'Real-time monitor', 'UAE AQI'],
            ['Noise Levels', '4 receptors', 'Weekly', 'Sound level meter', '75 dB(A)'],
            ['Water Quality', 'Discharge points', 'Monthly', 'Laboratory analysis', 'Local standards'],
            ['Waste Generation', 'On-site', 'Daily', 'Weighbridge records', 'Track diversion'],
            ['Flora/Fauna', 'Project area', 'Quarterly', 'Ecological survey', 'Baseline comparison']
        ]
        
        monitoring_table = Table(monitoring_data, colWidths=[1.3*inch, 1.3*inch, 1*inch, 1.5*inch, 1.3*inch])
        monitoring_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
            ('LINEBELOW', (0, 0), (-1, -2), 1, colors.HexColor('#e5e7eb')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
        ]))
        
        elements.append(monitoring_table)
        
        return elements
        
    def _create_conclusions(self):
        """Create conclusions and recommendations"""
        elements = []
        
        elements.append(PageBreak())
        elements.append(Paragraph("9. CONCLUSIONS AND RECOMMENDATIONS", self.styles['ChapterHeading']))
        elements.append(Spacer(1, 0.3*inch))
        
        compliance_score = self.assessment_results.get('summary', {}).get('compliance_score', 0)
        
        elements.append(Paragraph(
            f"""Based on the comprehensive environmental assessment conducted for the {self.project_data.get('name')} project, 
            the following conclusions have been reached:""",
            self.styles['ProfessionalBody']
        ))
        
        elements.append(Spacer(1, 0.2*inch))
        
        # Key conclusions
        conclusions = [
            f"The project achieves an overall environmental compliance score of {compliance_score}%",
            "All identified impacts can be mitigated to acceptable levels through proposed measures",
            "No fatal flaws or insurmountable environmental constraints were identified",
            "The project aligns with national environmental objectives and international standards",
            "Implementation of the EMP will ensure sustainable development practices"
        ]
        
        for i, conclusion in enumerate(conclusions, 1):
            elements.append(Paragraph(f"{i}. {conclusion}", self.styles['ProfessionalBody']))
            
        elements.append(Spacer(1, 0.3*inch))
        
        elements.append(Paragraph("<b>Key Recommendations:</b>", self.styles['SectionHeading']))
        
        recommendations = [
            "Obtain all necessary environmental permits before commencing construction",
            "Appoint qualified Environmental Manager before project mobilization",
            "Implement Environmental Management System (EMS) certified to ISO 14001",
            "Conduct monthly environmental audits and quarterly management reviews",
            "Engage with stakeholders throughout project lifecycle",
            "Allocate sufficient budget for environmental management (min. 2% of project cost)"
        ]
        
        for rec in recommendations:
            elements.append(Paragraph(f"• {rec}", self.styles['ProfessionalBody']))
            
        return elements
        
    def _create_appendices(self):
        """Create appendices"""
        elements = []
        
        elements.append(PageBreak())
        elements.append(Paragraph("APPENDICES", self.styles['ChapterHeading']))
        elements.append(Spacer(1, 0.3*inch))
        
        appendices = [
            "Appendix A: Detailed Calculations and Modeling Results",
            "Appendix B: Regulatory Correspondence",
            "Appendix C: Baseline Survey Data",
            "Appendix D: Stakeholder Consultation Records",
            "Appendix E: Technical Specifications",
            "Appendix F: Environmental Standards and Guidelines",
            "Appendix G: Emergency Response Procedures",
            "Appendix H: Training Materials and Protocols"
        ]
        
        for appendix in appendices:
            elements.append(Paragraph(appendix, self.styles['SectionHeading']))
            elements.append(Paragraph(
                "Detailed information available in separate document.",
                self.styles['ProfessionalBody']
            ))
            elements.append(Spacer(1, 0.2*inch))
            
        return elements
        
    def _create_regulatory_framework(self):
        """Create regulatory framework section"""
        elements = []
        
        elements.append(PageBreak())
        elements.append(Paragraph("3. REGULATORY FRAMEWORK", self.styles['ChapterHeading']))
        elements.append(Spacer(1, 0.3*inch))
        
        elements.append(Paragraph("3.1 Applicable Environmental Regulations", self.styles['SectionHeading']))
        
        # Regulatory table
        regulations = [
            ['Regulation', 'Relevance', 'Compliance Requirement'],
            ['UAE Federal Law No. 24 (1999)', 'Environmental Protection', 'EIA approval required'],
            ['Cabinet Decision No. 37 (2001)', 'EIA Procedures', 'Follow prescribed methodology'],
            ['Local Municipality Regulations', 'Construction permits', 'Obtain NOC before construction'],
            ['Abu Dhabi EHS Manual', 'HSE Standards', 'Implement EHS requirements'],
            ['IFC Performance Standards', 'International best practice', 'Voluntary compliance']
        ]
        
        reg_table = Table(regulations, colWidths=[2.2*inch, 1.8*inch, 2*inch])
        reg_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
            ('LINEBELOW', (0, 0), (-1, -2), 1, colors.HexColor('#e5e7eb')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
        ]))
        
        elements.append(reg_table)
        
        return elements
        
    def _create_environmental_baseline(self):
        """Create environmental baseline section"""
        elements = []
        
        elements.append(PageBreak())
        elements.append(Paragraph("4. ENVIRONMENTAL BASELINE", self.styles['ChapterHeading']))
        elements.append(Spacer(1, 0.3*inch))
        
        elements.append(Paragraph("4.1 Physical Environment", self.styles['SectionHeading']))
        
        # Climate data
        elements.append(Paragraph("<b>Climate Conditions:</b>", self.styles['Normal']))
        climate_data = [
            ['Parameter', 'Value', 'Remarks'],
            ['Average Temperature', '28°C (Annual)', 'Peak: 45°C in summer'],
            ['Rainfall', '100mm/year', 'Primarily winter months'],
            ['Humidity', '60% average', 'Higher in coastal areas'],
            ['Wind Speed', '15 km/h average', 'NW prevailing direction'],
            ['Dust Storms', '8-10 events/year', 'Mainly spring season']
        ]
        
        climate_table = Table(climate_data, colWidths=[2*inch, 2*inch, 2*inch])
        climate_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e5e7eb')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
            ('LINEBELOW', (0, 0), (-1, -2), 1, colors.HexColor('#e5e7eb'))
        ]))
        
        elements.append(climate_table)
        
        return elements
        
    def _add_header_footer(self, canvas, doc):
        """Add header and footer to pages"""
        canvas.saveState()
        
        # Header
        canvas.setFont('Helvetica', 9)
        canvas.drawString(72, A4[1] - 40, f"EIA Report - {self.project_data.get('name', 'Project')}")
        canvas.drawRightString(A4[0] - 72, A4[1] - 40, 
                               f"Date: {self.creation_date.strftime('%B %Y')}")
        
        # Header line
        canvas.setStrokeColor(colors.HexColor('#d1d5db'))
        canvas.line(72, A4[1] - 50, A4[0] - 72, A4[1] - 50)
        
        # Footer
        canvas.drawString(72, 40, "EIA Pro Platform - Professional Environmental Assessment")
        canvas.drawRightString(A4[0] - 72, 40, f"Page {doc.page}")
        
        # Footer line
        canvas.line(72, 55, A4[0] - 72, 55)
        
        # Confidentiality notice
        canvas.setFont('Helvetica-Oblique', 8)
        canvas.drawCentredString(A4[0]/2, 25, 
                                 "This document contains confidential information and is for official use only")
        
        canvas.restoreState()
        
    def _get_project_components(self):
        """Get project components based on type"""
        project_type = self.project_data.get('type', 'mixed_use')
        
        components_map = {
            'residential': [
                "Residential towers (G+40 floors)",
                "Podium with retail facilities",
                "Basement parking (3 levels)",
                "Landscaped areas and gardens",
                "Community facilities and amenities",
                "Infrastructure and utilities"
            ],
            'commercial': [
                "Office towers",
                "Retail and F&B outlets",
                "Multi-level parking structure",
                "Service areas and loading bays",
                "Utility buildings",
                "External works and landscaping"
            ],
            'industrial': [
                "Production facilities",
                "Warehouse and storage areas",
                "Administrative buildings",
                "Utility and service buildings",
                "Truck parking and circulation",
                "Waste treatment facilities"
            ],
            'infrastructure': [
                "Main infrastructure components",
                "Support facilities",
                "Control buildings",
                "Access roads and parking",
                "Utility connections",
                "Security installations"
            ],
            'mixed_use': [
                "Residential component",
                "Commercial/retail component",
                "Office spaces",
                "Hotel facilities",
                "Parking structures",
                "Public realm and landscaping"
            ]
        }
        
        return components_map.get(project_type, components_map['mixed_use'])
        
    def _generate_html_report(self):
        """Generate HTML report as fallback"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>EIA Report - {self.project_data.get('name', 'Project')}</title>
            <style>
                body {{ 
                    font-family: Arial, sans-serif; 
                    line-height: 1.6; 
                    margin: 40px;
                    color: #333;
                }}
                h1 {{ 
                    color: #059669; 
                    border-bottom: 3px solid #059669;
                    padding-bottom: 10px;
                }}
                h2 {{ 
                    color: #047857; 
                    margin-top: 30px;
                }}
                .header {{
                    background: #f9fafb;
                    padding: 20px;
                    border-radius: 8px;
                    margin-bottom: 30px;
                }}
                .compliance-score {{
                    font-size: 48px;
                    font-weight: bold;
                    color: #059669;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin: 20px 0;
                }}
                th, td {{
                    border: 1px solid #e5e7eb;
                    padding: 12px;
                    text-align: left;
                }}
                th {{
                    background: #059669;
                    color: white;
                }}
                tr:nth-child(even) {{
                    background: #f9fafb;
                }}
                .footer {{
                    margin-top: 50px;
                    padding-top: 20px;
                    border-top: 2px solid #e5e7eb;
                    text-align: center;
                    color: #6b7280;
                }}
                @media print {{
                    body {{ margin: 20px; }}
                    .no-print {{ display: none; }}
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Environmental Impact Assessment Report</h1>
                <h2>{self.project_data.get('name', 'Project Name')}</h2>
                <p><strong>Location:</strong> {self.project_data.get('location', 'Location')}</p>
                <p><strong>Date:</strong> {self.creation_date.strftime('%B %Y')}</p>
                <p><strong>Overall Compliance Score:</strong> <span class="compliance-score">{self.assessment_results.get('summary', {}).get('compliance_score', 0)}%</span></p>
            </div>
            
            <h2>Executive Summary</h2>
            <p>This comprehensive Environmental Impact Assessment has been prepared for the {self.project_data.get('name')} project. 
            The assessment covers all environmental aspects including air quality, noise, water resources, waste management, 
            biodiversity, soil conditions, socio-economic impacts, and risk assessment.</p>
            
            <h2>Key Environmental Metrics</h2>
            <table>
                <tr>
                    <th>Assessment Module</th>
                    <th>Status</th>
                    <th>Key Finding</th>
                    <th>Compliance</th>
                </tr>
        """
        
        # Add results for each module
        modules = [
            ('Air Quality', 'air_quality'),
            ('Noise Impact', 'noise_assessment'),
            ('Water Resources', 'water_resources'),
            ('Waste Management', 'waste_management'),
            ('Biodiversity', 'biological_environment'),
            ('Soil & Geology', 'soil_geology'),
            ('Socio-Economic', 'socio_economic'),
            ('Risk Assessment', 'risk_assessment'),
            ('EMP', 'environmental_management_plan')
        ]
        
        for module_name, module_key in modules:
            module_data = self.assessment_results.get('assessment_results', {}).get(module_key, {})
            status = module_data.get('status', 'pending')
            compliance = module_data.get('compliance', 'Under Review')
            
            # Get key metric based on module
            key_finding = self._get_key_finding(module_key, module_data)
            
            html_content += f"""
                <tr>
                    <td>{module_name}</td>
                    <td>{status.title()}</td>
                    <td>{key_finding}</td>
                    <td>{compliance}</td>
                </tr>
            """
            
        html_content += """
            </table>
            
            <h2>Critical Recommendations</h2>
            <ol>
                <li>Implement comprehensive dust control measures during construction</li>
                <li>Install acoustic barriers at sensitive receptor locations</li>
                <li>Establish water recycling system to minimize consumption</li>
                <li>Develop detailed waste segregation procedures</li>
                <li>Conduct pre-construction biodiversity survey</li>
                <li>Implement real-time environmental monitoring</li>
            </ol>
            
            <div class="footer">
                <p>Generated by EIA Pro Platform - Professional Environmental Assessment System</p>
                <p>© 2024 EIA Pro | Created by Edy Bassil | bassileddy@gmail.com</p>
            </div>
            
            <div class="no-print" style="margin-top: 30px; text-align: center;">
                <button onclick="window.print()" style="padding: 10px 20px; background: #059669; color: white; border: none; border-radius: 5px; cursor: pointer;">
                    Print/Save as PDF
                </button>
            </div>
        </body>
        </html>
        """
        
        return html_content.encode('utf-8')
        
    def _generate_pdfkit_pdf(self, output_path=None):
        """Generate PDF using pdfkit (wkhtmltopdf)"""
        html_content = self._generate_html_report().decode('utf-8')
        
        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None
        }
        
        if output_path:
            pdfkit.from_string(html_content, output_path, options=options)
            return True
        else:
            return pdfkit.from_string(html_content, False, options=options)
            
    def _get_key_finding(self, module_key, data):
        """Get key finding for each module"""
        findings_map = {
            'air_quality': f"PM10: {data.get('pm10_concentration', 0):.1f} µg/m³",
            'noise_assessment': f"Peak: {data.get('peak_noise_level', 0):.1f} dB(A)",
            'water_resources': f"Demand: {data.get('operational_water_demand_m3_year', 0):,.0f} m³/yr",
            'waste_management': f"C&D: {data.get('construction_waste_tons', 0):.0f} tons",
            'biological_environment': f"Species: {data.get('species_affected', 0)} affected",
            'soil_geology': f"Risk: {data.get('erosion_risk', 'Moderate')}",
            'socio_economic': f"Jobs: {data.get('construction_workers', 0)}",
            'risk_assessment': f"High Risks: {data.get('high_priority_risks', 0)}",
            'environmental_management_plan': f"Measures: {data.get('mitigation_measures', 0)}"
        }
        
        return findings_map.get(module_key, "Assessment completed")


def generate_professional_eia_report(project_data, assessment_results, output_format='pdf'):
    """
    Generate professional EIA report
    
    Args:
        project_data: Project information dict
        assessment_results: Assessment results from all modules
        output_format: 'pdf', 'html', or 'buffer'
        
    Returns:
        Report content or file path
    """
    try:
        report_generator = ProfessionalEIAReport(project_data, assessment_results)
        
        if output_format == 'pdf':
            # Generate to file
            filename = f"EIA_Report_{project_data.get('name', 'Project').replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
            report_generator.generate_report(filename)
            return filename
        elif output_format == 'buffer':
            # Return buffer for API response
            return report_generator.generate_report()
        else:
            # Return HTML
            return report_generator._generate_html_report()
            
    except Exception as e:
        print(f"Error generating report: {str(e)}")
        # Return simple HTML report as fallback
        return report_generator._generate_html_report()


# Professional charts generator for reports
class EnvironmentalChartsGenerator:
    """Generate professional charts for EIA reports"""
    
    @staticmethod
    def create_compliance_chart(data):
        """Create compliance score chart"""
        if not REPORTLAB_AVAILABLE:
            return None
            
        drawing = Drawing(400, 200)
        bc = VerticalBarChart()
        bc.x = 50
        bc.y = 50
        bc.height = 125
        bc.width = 300
        
        # Data should be list of (module, score) tuples
        bc.data = [[score for _, score in data]]
        bc.categoryAxis.categoryNames = [name for name, _ in data]
        
        # Color bars based on score
        for i, (_, score) in enumerate(data):
            if score >= 80:
                bc.bars[0].fillColor = colors.HexColor('#059669')  # Green
            elif score >= 60:
                bc.bars[0].fillColor = colors.HexColor('#f59e0b')  # Yellow
            else:
                bc.bars[0].fillColor = colors.HexColor('#ef4444')  # Red
                
        bc.valueAxis.valueMin = 0
        bc.valueAxis.valueMax = 100
        bc.valueAxis.valueStep = 20
        
        drawing.add(bc)
        return drawing
        
    @staticmethod
    def create_impact_matrix(impacts):
        """Create impact assessment matrix visualization"""
        if not REPORTLAB_AVAILABLE:
            return None
            
        # Create visual matrix of impacts
        # This would create a color-coded matrix showing impact severity
        pass


if __name__ == "__main__":
    # Test report generation
    sample_project = {
        'name': 'Dubai Marina Tower Development',
        'type': 'mixed_use',
        'location': 'Dubai, UAE',
        'size': 50000,
        'duration': 24,
        'budget': 150,
        'workers': 500
    }
    
    sample_results = {
        'summary': {
            'compliance_score': 85,
            'critical_issues': ['Dust control required', 'Noise barriers needed'],
            'mitigation_count': 45
        },
        'assessment_results': {
            'air_quality': {
                'status': 'assessed',
                'pm10_concentration': 95.5,
                'pm25_concentration': 45.2,
                'compliance': 'Compliant with mitigation'
            },
            'noise_assessment': {
                'status': 'assessed',
                'peak_noise_level': 72.5,
                'compliance': 'Requires monitoring'
            }
        }
    }
    
    # Generate test report
    report = generate_professional_eia_report(
        sample_project,
        sample_results,
        output_format='html'
    )
    
    # Save test report
    with open('test_eia_report.html', 'wb') as f:
        f.write(report)
        
    print("Test report generated successfully!")