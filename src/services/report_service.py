"""
Report Generation Service
Professional PDF report generation for environmental assessments

Author: Edy Bassil
Email: bassileddy@gmail.com
"""

from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta
import logging
import io
import os
from pathlib import Path
import json
import base64
from dataclasses import dataclass
from enum import Enum

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Image, KeepTogether,
    Frame, PageTemplate, BaseDocTemplate
)
from reportlab.graphics.shapes import Drawing, Line, Rect
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_JUSTIFY
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy.orm import Session

from src.models import (
    Project, Assessment, ImpactRecord, ComplianceRecord,
    MonitoringData, MitigationMeasure, get_session
)
from src.services import BaseService, ServiceException, ValidationError
from src.impact_calculator import ImpactCalculator
from src.risk_matrix import RiskMatrix
from src.compliance import RegulatoryCompliance

logger = logging.getLogger(__name__)


class ReportType(Enum):
    """Available report types."""
    SCREENING = "screening"
    IMPACT = "impact"
    COMPLIANCE = "compliance"
    MONITORING = "monitoring"
    COMPREHENSIVE = "comprehensive"
    EXECUTIVE_SUMMARY = "executive_summary"


class ReportLanguage(Enum):
    """Supported report languages."""
    ENGLISH = "en"
    ARABIC = "ar"


@dataclass
class ReportConfig:
    """Report generation configuration."""
    report_type: ReportType
    language: ReportLanguage = ReportLanguage.ENGLISH
    include_sections: List[str] = None
    date_range: Optional[Dict[str, datetime]] = None
    logo_path: Optional[str] = None
    watermark: bool = True
    page_numbers: bool = True
    table_of_contents: bool = True
    executive_summary: bool = True
    recommendations: bool = True
    appendices: bool = True
    charts: bool = True
    
    def __post_init__(self):
        if self.include_sections is None:
            self.include_sections = self._default_sections()
    
    def _default_sections(self) -> List[str]:
        """Get default sections based on report type."""
        sections_map = {
            ReportType.SCREENING: [
                "project_overview", "screening_results", 
                "regulatory_requirements", "recommendations"
            ],
            ReportType.IMPACT: [
                "project_overview", "methodology", "impact_assessment",
                "risk_assessment", "mitigation_measures", "conclusions"
            ],
            ReportType.COMPLIANCE: [
                "project_overview", "compliance_summary", 
                "detailed_checks", "non_compliance_items", "action_plan"
            ],
            ReportType.MONITORING: [
                "project_overview", "monitoring_summary", "parameter_analysis",
                "trends", "exceedances", "recommendations"
            ],
            ReportType.COMPREHENSIVE: [
                "executive_summary", "project_overview", "screening_results",
                "impact_assessment", "risk_assessment", "compliance_status",
                "monitoring_data", "mitigation_measures", "conclusions",
                "recommendations", "appendices"
            ],
            ReportType.EXECUTIVE_SUMMARY: [
                "key_findings", "compliance_status", "major_risks",
                "recommended_actions", "timeline"
            ]
        }
        return sections_map.get(self.report_type, [])


class ReportService(BaseService):
    """Service for generating professional EIA reports."""
    
    def __init__(self, db: Session):
        super().__init__(db, Project)
        self.styles = self._setup_styles()
        self.colors = self._setup_colors()
        
        # Services for data gathering
        self.impact_calculator = ImpactCalculator()
        self.risk_matrix = RiskMatrix()
        self.compliance_checker = RegulatoryCompliance()
    
    def _setup_styles(self) -> Dict[str, ParagraphStyle]:
        """Setup report styles."""
        styles = getSampleStyleSheet()
        
        # Custom styles
        styles.add(ParagraphStyle(
            name='CoverTitle',
            parent=styles['Title'],
            fontSize=28,
            textColor=colors.HexColor('#1e3a5f'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        styles.add(ParagraphStyle(
            name='CoverSubtitle',
            parent=styles['Normal'],
            fontSize=16,
            textColor=colors.HexColor('#2c5282'),
            spaceBefore=10,
            spaceAfter=10,
            alignment=TA_CENTER
        ))
        
        styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1e3a5f'),
            spaceBefore=20,
            spaceAfter=15
        ))
        
        styles.add(ParagraphStyle(
            name='SubsectionHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2c5282'),
            spaceBefore=15,
            spaceAfter=10
        ))
        
        styles.add(ParagraphStyle(
            name='BodyJustified',
            parent=styles['Normal'],
            alignment=TA_JUSTIFY,
            fontSize=11,
            leading=14
        ))
        
        styles.add(ParagraphStyle(
            name='TableHeader',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.white,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        styles.add(ParagraphStyle(
            name='Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_CENTER
        ))
        
        styles.add(ParagraphStyle(
            name='Watermark',
            parent=styles['Normal'],
            fontSize=48,
            textColor=colors.Color(0, 0, 0, alpha=0.1),
            alignment=TA_CENTER
        ))
        
        return styles
    
    def _setup_colors(self) -> Dict[str, Any]:
        """Setup color scheme."""
        return {
            'primary': colors.HexColor('#1e3a5f'),
            'secondary': colors.HexColor('#2c5282'),
            'accent': colors.HexColor('#38a169'),
            'warning': colors.HexColor('#d69e2e'),
            'danger': colors.HexColor('#e53e3e'),
            'success': colors.HexColor('#38a169'),
            'info': colors.HexColor('#3182ce'),
            'light_gray': colors.HexColor('#f7fafc'),
            'medium_gray': colors.HexColor('#e2e8f0'),
            'dark_gray': colors.HexColor('#2d3748')
        }
    
    def generate_report(
        self,
        project_id: int,
        config: ReportConfig,
        output_path: Optional[str] = None
    ) -> Union[str, bytes]:
        """
        Generate comprehensive EIA report.
        
        Args:
            project_id: Project ID
            config: Report configuration
            output_path: Optional output file path
            
        Returns:
            File path if output_path provided, else PDF bytes
        """
        try:
            # Validate project exists
            project = self.get_by_id(project_id)
            if not project:
                raise ValidationError(f"Project {project_id} not found")
            
            # Create report buffer
            if output_path:
                buffer = output_path
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
            else:
                buffer = io.BytesIO()
            
            # Create document
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72,
                title=f"Environmental Impact Assessment - {project.name}",
                author="EIA Tool Professional",
                subject=f"{config.report_type.value.replace('_', ' ').title()} Report",
                creator="EIA Tool by Edy Bassil"
            )
            
            # Build report content
            story = []
            
            # Add cover page
            story.extend(self._create_cover_page(project, config))
            story.append(PageBreak())
            
            # Add table of contents if requested
            if config.table_of_contents:
                story.extend(self._create_table_of_contents(config))
                story.append(PageBreak())
            
            # Add executive summary if requested
            if config.executive_summary and config.report_type != ReportType.EXECUTIVE_SUMMARY:
                story.extend(self._create_executive_summary(project))
                story.append(PageBreak())
            
            # Add main content based on report type
            content_method = getattr(
                self, 
                f"_create_{config.report_type.value}_content",
                self._create_comprehensive_content
            )
            story.extend(content_method(project, config))
            
            # Add recommendations if requested
            if config.recommendations:
                story.append(PageBreak())
                story.extend(self._create_recommendations(project, config))
            
            # Add appendices if requested
            if config.appendices and config.report_type == ReportType.COMPREHENSIVE:
                story.append(PageBreak())
                story.extend(self._create_appendices(project))
            
            # Build PDF
            doc.build(story, onFirstPage=self._add_page_elements, 
                     onLaterPages=self._add_page_elements)
            
            # Return result
            if output_path:
                logger.info(f"Report generated: {output_path}")
                return output_path
            else:
                buffer.seek(0)
                return buffer.getvalue()
                
        except Exception as e:
            logger.error(f"Report generation failed: {e}")
            raise ServiceException(f"Failed to generate report: {str(e)}")
    
    def _create_cover_page(self, project: Project, config: ReportConfig) -> List:
        """Create report cover page."""
        elements = []
        
        # Logo if provided
        if config.logo_path and os.path.exists(config.logo_path):
            logo = Image(config.logo_path, width=2*inch, height=1*inch)
            logo.hAlign = 'CENTER'
            elements.append(logo)
            elements.append(Spacer(1, 0.5*inch))
        
        # Report title
        title_text = f"Environmental Impact Assessment"
        elements.append(Paragraph(title_text, self.styles['CoverTitle']))
        
        # Report type
        report_type_text = config.report_type.value.replace('_', ' ').title() + " Report"
        elements.append(Paragraph(report_type_text, self.styles['CoverSubtitle']))
        
        elements.append(Spacer(1, 1*inch))
        
        # Project information
        project_info = f"""
        <para align="center">
        <b>Project:</b> {project.name}<br/>
        <b>Location:</b> {project.location}<br/>
        <b>Client:</b> {project.client_name or 'Not specified'}<br/>
        <b>Report Date:</b> {datetime.now().strftime('%B %d, %Y')}
        </para>
        """
        elements.append(Paragraph(project_info, self.styles['Normal']))
        
        elements.append(Spacer(1, 2*inch))
        
        # Prepared by section
        prepared_by = """
        <para align="center">
        <b>Prepared by:</b><br/>
        Environmental Impact Assessment Tool<br/>
        Professional Edition v2.0<br/>
        <br/>
        <i>Automated report generation powered by advanced environmental analysis</i>
        </para>
        """
        elements.append(Paragraph(prepared_by, self.styles['Normal']))
        
        # Jurisdiction badge
        elements.append(Spacer(1, 0.5*inch))
        jurisdiction = self._get_jurisdiction(project.location)
        jurisdiction_text = f"""
        <para align="center">
        <b>Regulatory Compliance:</b> {jurisdiction}
        </para>
        """
        elements.append(Paragraph(jurisdiction_text, self.styles['Normal']))
        
        return elements
    
    def _create_table_of_contents(self, config: ReportConfig) -> List:
        """Create table of contents."""
        elements = []
        
        elements.append(Paragraph("Table of Contents", self.styles['SectionHeading']))
        elements.append(Spacer(1, 0.2*inch))
        
        # TOC entries based on sections
        toc_data = []
        page_num = 3  # Start after cover and TOC
        
        for section in config.include_sections:
            section_title = section.replace('_', ' ').title()
            toc_data.append([section_title, str(page_num)])
            page_num += 1  # Simplified - in real implementation track actual pages
        
        toc_table = Table(toc_data, colWidths=[5*inch, 1*inch])
        toc_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        
        elements.append(toc_table)
        return elements
    
    def _create_executive_summary(self, project: Project) -> List:
        """Create executive summary section."""
        elements = []
        
        elements.append(Paragraph("Executive Summary", self.styles['SectionHeading']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Get latest assessment data
        assessment = self.db.query(Assessment).filter_by(
            project_id=project.id
        ).order_by(Assessment.assessment_date.desc()).first()
        
        impact = self.db.query(ImpactRecord).filter_by(
            project_id=project.id
        ).order_by(ImpactRecord.assessment_date.desc()).first()
        
        compliance = self.db.query(ComplianceRecord).filter_by(
            project_id=project.id
        ).all()
        
        # Project overview
        overview_text = f"""
        This Environmental Impact Assessment report presents a comprehensive analysis of 
        the {project.project_type.replace('_', ' ')} project "{project.name}" located in 
        {project.location}. The assessment was conducted in accordance with the applicable 
        environmental regulations and international best practices.
        """
        elements.append(Paragraph(overview_text, self.styles['BodyJustified']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Key findings
        elements.append(Paragraph("Key Findings:", self.styles['SubsectionHeading']))
        
        findings = []
        
        # EIA requirement
        if assessment:
            eia_status = "required" if assessment.eia_required else "not required"
            findings.append(f"Environmental Impact Assessment is <b>{eia_status}</b> for this project")
            if assessment.eia_level:
                findings.append(f"Recommended EIA level: <b>{assessment.eia_level}</b>")
        
        # Impact summary
        if impact:
            findings.append(f"Total carbon footprint: <b>{impact.carbon_footprint:.1f} tons CO₂e</b>")
            findings.append(f"Water consumption: <b>{impact.water_consumption:.0f} m³</b>")
            findings.append(f"Impact severity: <b>{impact.impact_severity}</b>")
        
        # Compliance summary
        if compliance:
            compliant = sum(1 for c in compliance if c.status == "Compliant")
            total = len(compliance)
            compliance_rate = (compliant / total * 100) if total > 0 else 100
            findings.append(f"Regulatory compliance rate: <b>{compliance_rate:.1f}%</b>")
        
        for finding in findings:
            elements.append(Paragraph(f"• {finding}", self.styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
        
        return elements
    
    def _create_screening_content(self, project: Project, config: ReportConfig) -> List:
        """Create screening report content."""
        elements = []
        
        # Get screening assessment
        assessment = self.db.query(Assessment).filter_by(
            project_id=project.id,
            assessment_type='screening'
        ).order_by(Assessment.assessment_date.desc()).first()
        
        if not assessment:
            elements.append(Paragraph(
                "No screening assessment found for this project.",
                self.styles['Normal']
            ))
            return elements
        
        # Project Overview Section
        if "project_overview" in config.include_sections:
            elements.extend(self._create_project_overview_section(project))
            elements.append(Spacer(1, 0.3*inch))
        
        # Screening Results Section
        if "screening_results" in config.include_sections:
            elements.append(Paragraph("Screening Results", self.styles['SectionHeading']))
            
            # EIA requirement
            eia_text = "Required" if assessment.eia_required else "Not Required"
            eia_color = self.colors['danger'] if assessment.eia_required else self.colors['success']
            
            result_data = [
                ["Parameter", "Value"],
                ["EIA Requirement", eia_text],
                ["EIA Level", assessment.eia_level or "N/A"],
                ["Assessment Date", assessment.assessment_date.strftime("%Y-%m-%d")],
                ["Estimated Duration", f"{assessment.estimated_duration} months" if assessment.estimated_duration else "N/A"]
            ]
            
            result_table = Table(result_data, colWidths=[3*inch, 3*inch])
            result_table.setStyle(self._get_table_style())
            elements.append(result_table)
            elements.append(Spacer(1, 0.3*inch))
            
            # Key concerns
            if assessment.key_concerns:
                elements.append(Paragraph("Key Environmental Concerns", self.styles['SubsectionHeading']))
                for concern in assessment.key_concerns:
                    elements.append(Paragraph(f"• {concern}", self.styles['Normal']))
                elements.append(Spacer(1, 0.2*inch))
        
        # Regulatory Requirements Section
        if "regulatory_requirements" in config.include_sections and assessment.regulatory_requirements:
            elements.append(Paragraph("Regulatory Requirements", self.styles['SectionHeading']))
            
            req_data = [["Requirement", "Authority", "Reference"]]
            for req in assessment.regulatory_requirements:
                # Parse requirement string (format: "Requirement - Authority (Reference)")
                parts = req.split(" - ")
                if len(parts) >= 2:
                    req_name = parts[0]
                    auth_ref = parts[1].split(" (")
                    authority = auth_ref[0] if auth_ref else "N/A"
                    reference = auth_ref[1].rstrip(")") if len(auth_ref) > 1 else "N/A"
                else:
                    req_name = req
                    authority = "N/A"
                    reference = "N/A"
                
                req_data.append([req_name, authority, reference])
            
            req_table = Table(req_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
            req_table.setStyle(self._get_table_style())
            elements.append(req_table)
            elements.append(Spacer(1, 0.3*inch))
        
        # Specialist Studies Section
        if assessment.specialist_studies:
            elements.append(Paragraph("Required Specialist Studies", self.styles['SubsectionHeading']))
            for study in assessment.specialist_studies:
                elements.append(Paragraph(f"• {study}", self.styles['Normal']))
            elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_impact_content(self, project: Project, config: ReportConfig) -> List:
        """Create impact assessment report content."""
        elements = []
        
        # Get latest impact assessment
        impact = self.db.query(ImpactRecord).filter_by(
            project_id=project.id
        ).order_by(ImpactRecord.assessment_date.desc()).first()
        
        if not impact:
            elements.append(Paragraph(
                "No impact assessment found for this project.",
                self.styles['Normal']
            ))
            return elements
        
        # Project Overview
        if "project_overview" in config.include_sections:
            elements.extend(self._create_project_overview_section(project))
            elements.append(PageBreak())
        
        # Methodology
        if "methodology" in config.include_sections:
            elements.append(Paragraph("Assessment Methodology", self.styles['SectionHeading']))
            methodology_text = """
            The environmental impact assessment was conducted using internationally 
            recognized methodologies including:
            
            • Carbon footprint calculation based on IPCC emission factors
            • Water consumption analysis using regional benchmarks
            • Waste generation estimates from construction industry standards
            • Biodiversity impact scoring using habitat sensitivity indices
            • Air quality modeling for construction emissions
            • Noise impact assessment per WHO guidelines
            """
            elements.append(Paragraph(methodology_text, self.styles['BodyJustified']))
            elements.append(Spacer(1, 0.3*inch))
        
        # Impact Assessment Results
        if "impact_assessment" in config.include_sections:
            elements.append(Paragraph("Environmental Impact Assessment", self.styles['SectionHeading']))
            
            # Summary table
            impact_data = [
                ["Impact Category", "Value", "Unit", "Severity"],
                ["Carbon Footprint", f"{impact.carbon_footprint:.1f}", "tons CO₂e", self._get_severity_badge(impact.carbon_footprint, 1000, 5000)],
                ["Water Consumption", f"{impact.water_consumption:.0f}", "m³", self._get_severity_badge(impact.water_consumption, 10000, 50000)],
                ["Waste Generation", f"{impact.waste_generation:.0f}", "tons", self._get_severity_badge(impact.waste_generation, 100, 500)],
                ["Energy Usage", f"{impact.energy_usage:.0f}", "MWh", self._get_severity_badge(impact.energy_usage, 500, 2000)],
                ["Biodiversity Score", f"{impact.biodiversity_score:.1f}", "index", self._get_severity_badge(100 - impact.biodiversity_score, 20, 50)],
            ]
            
            if impact.pm10_concentration:
                impact_data.append([
                    "PM10 Concentration", 
                    f"{impact.pm10_concentration:.1f}", 
                    "µg/m³", 
                    self._get_severity_badge(impact.pm10_concentration, 150, 250)
                ])
            
            if impact.pm25_concentration:
                impact_data.append([
                    "PM2.5 Concentration", 
                    f"{impact.pm25_concentration:.1f}", 
                    "µg/m³", 
                    self._get_severity_badge(impact.pm25_concentration, 65, 150)
                ])
            
            impact_table = Table(impact_data, colWidths=[2.5*inch, 1.5*inch, 1*inch, 1*inch])
            impact_table.setStyle(self._get_impact_table_style())
            elements.append(impact_table)
            elements.append(Spacer(1, 0.3*inch))
            
            # Impact charts if enabled
            if config.charts:
                elements.append(PageBreak())
                elements.append(Paragraph("Impact Analysis Charts", self.styles['SubsectionHeading']))
                
                # Create impact comparison chart
                chart_buffer = self._create_impact_chart(impact)
                if chart_buffer:
                    chart_img = Image(chart_buffer, width=6*inch, height=4*inch)
                    chart_img.hAlign = 'CENTER'
                    elements.append(chart_img)
                    elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_compliance_content(self, project: Project, config: ReportConfig) -> List:
        """Create compliance report content."""
        elements = []
        
        # Get compliance records
        compliance_records = self.db.query(ComplianceRecord).filter_by(
            project_id=project.id
        ).order_by(ComplianceRecord.check_date.desc()).all()
        
        if not compliance_records:
            elements.append(Paragraph(
                "No compliance checks found for this project.",
                self.styles['Normal']
            ))
            return elements
        
        # Group by latest check date
        latest_date = compliance_records[0].check_date
        latest_records = [r for r in compliance_records if r.check_date == latest_date]
        
        # Compliance Summary
        if "compliance_summary" in config.include_sections:
            elements.append(Paragraph("Compliance Summary", self.styles['SectionHeading']))
            
            total = len(latest_records)
            compliant = sum(1 for r in latest_records if r.status == "Compliant")
            non_compliant = total - compliant
            compliance_rate = (compliant / total * 100) if total > 0 else 100
            
            summary_text = f"""
            Overall regulatory compliance assessment shows that the project achieves a 
            <b>{compliance_rate:.1f}%</b> compliance rate with applicable environmental 
            regulations. Out of {total} regulatory requirements checked, {compliant} were 
            found to be compliant and {non_compliant} require attention.
            """
            elements.append(Paragraph(summary_text, self.styles['BodyJustified']))
            elements.append(Spacer(1, 0.3*inch))
            
            # Compliance pie chart
            if config.charts and non_compliant > 0:
                chart_buffer = self._create_compliance_pie_chart(compliant, non_compliant)
                if chart_buffer:
                    chart_img = Image(chart_buffer, width=4*inch, height=3*inch)
                    chart_img.hAlign = 'CENTER'
                    elements.append(chart_img)
                    elements.append(Spacer(1, 0.3*inch))
        
        # Detailed Compliance Checks
        if "detailed_checks" in config.include_sections:
            elements.append(Paragraph("Detailed Compliance Checks", self.styles['SectionHeading']))
            
            # Group by category
            categories = {}
            for record in latest_records:
                if record.category not in categories:
                    categories[record.category] = []
                categories[record.category].append(record)
            
            for category, records in categories.items():
                elements.append(Paragraph(f"{category} Requirements", self.styles['SubsectionHeading']))
                
                check_data = [["Regulation", "Status", "Value", "Limit", "Deviation"]]
                for record in records:
                    status_color = self.colors['success'] if record.status == "Compliant" else self.colors['danger']
                    deviation_text = f"{record.deviation:.1f}%" if record.deviation else "N/A"
                    
                    check_data.append([
                        record.regulation_name,
                        record.status,
                        f"{record.actual_value:.1f}" if record.actual_value else "N/A",
                        f"{record.required_value:.1f}" if record.required_value else "N/A",
                        deviation_text
                    ])
                
                check_table = Table(check_data, colWidths=[2.5*inch, 1*inch, 1*inch, 1*inch, 1*inch])
                check_table.setStyle(self._get_compliance_table_style(records))
                elements.append(check_table)
                elements.append(Spacer(1, 0.2*inch))
        
        # Non-compliance Items
        non_compliant_records = [r for r in latest_records if r.status != "Compliant"]
        if "non_compliance_items" in config.include_sections and non_compliant_records:
            elements.append(PageBreak())
            elements.append(Paragraph("Non-Compliance Items", self.styles['SectionHeading']))
            
            for record in non_compliant_records:
                elements.append(Paragraph(f"• <b>{record.regulation_name}</b>", self.styles['Normal']))
                
                details_text = f"""
                Category: {record.category}<br/>
                Current Value: {record.actual_value:.1f} | Required: {record.required_value:.1f}<br/>
                Deviation: {record.deviation:.1f}%<br/>
                Recommendation: {record.recommendation or 'Implement corrective measures'}
                """
                elements.append(Paragraph(details_text, self.styles['Normal']))
                elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_monitoring_content(self, project: Project, config: ReportConfig) -> List:
        """Create monitoring report content."""
        elements = []
        
        # Date range
        if config.date_range:
            start_date = config.date_range.get('start')
            end_date = config.date_range.get('end')
        else:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
        
        # Get monitoring data
        monitoring_data = self.db.query(MonitoringData).filter(
            MonitoringData.project_id == project.id,
            MonitoringData.measurement_date >= start_date,
            MonitoringData.measurement_date <= end_date
        ).order_by(MonitoringData.measurement_date.desc()).all()
        
        if not monitoring_data:
            elements.append(Paragraph(
                "No monitoring data found for the specified period.",
                self.styles['Normal']
            ))
            return elements
        
        # Monitoring Summary
        if "monitoring_summary" in config.include_sections:
            elements.append(Paragraph("Monitoring Summary", self.styles['SectionHeading']))
            
            period_text = f"Reporting Period: {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}"
            elements.append(Paragraph(period_text, self.styles['Normal']))
            elements.append(Spacer(1, 0.2*inch))
            
            # Group by parameter
            parameters = {}
            for data in monitoring_data:
                if data.parameter not in parameters:
                    parameters[data.parameter] = []
                parameters[data.parameter].append(data)
            
            summary_data = [["Parameter", "Measurements", "Average", "Max", "Exceedances"]]
            
            for param, measurements in parameters.items():
                values = [m.value for m in measurements]
                exceedances = sum(1 for m in measurements if m.exceeds_limit)
                
                summary_data.append([
                    param.upper(),
                    str(len(measurements)),
                    f"{np.mean(values):.1f}",
                    f"{max(values):.1f}",
                    str(exceedances)
                ])
            
            summary_table = Table(summary_data, colWidths=[1.5*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch])
            summary_table.setStyle(self._get_table_style())
            elements.append(summary_table)
            elements.append(Spacer(1, 0.3*inch))
        
        # Parameter Analysis
        if "parameter_analysis" in config.include_sections and config.charts:
            elements.append(PageBreak())
            elements.append(Paragraph("Parameter Analysis", self.styles['SectionHeading']))
            
            # Create time series charts for each parameter
            for param, measurements in parameters.items():
                elements.append(Paragraph(f"{param.upper()} Monitoring Data", self.styles['SubsectionHeading']))
                
                # Create time series chart
                chart_buffer = self._create_time_series_chart(measurements, param)
                if chart_buffer:
                    chart_img = Image(chart_buffer, width=6*inch, height=3*inch)
                    chart_img.hAlign = 'CENTER'
                    elements.append(chart_img)
                    elements.append(Spacer(1, 0.3*inch))
                
                # Statistics
                values = [m.value for m in measurements]
                stats_text = f"""
                Mean: {np.mean(values):.2f} | Std Dev: {np.std(values):.2f} | 
                Min: {min(values):.2f} | Max: {max(values):.2f}
                """
                elements.append(Paragraph(stats_text, self.styles['Normal']))
                elements.append(Spacer(1, 0.2*inch))
        
        # Exceedances
        exceedances = [m for m in monitoring_data if m.exceeds_limit]
        if "exceedances" in config.include_sections and exceedances:
            elements.append(Paragraph("Limit Exceedances", self.styles['SectionHeading']))
            
            exc_data = [["Date", "Time", "Parameter", "Value", "Limit", "Location"]]
            for exc in exceedances[:20]:  # Limit to 20 most recent
                exc_data.append([
                    exc.measurement_date.strftime("%Y-%m-%d"),
                    exc.measurement_time or "N/A",
                    exc.parameter.upper(),
                    f"{exc.value:.1f}",
                    f"{exc.limit_value:.1f}" if exc.limit_value else "N/A",
                    exc.monitoring_point or "N/A"
                ])
            
            exc_table = Table(exc_data, colWidths=[1.2*inch, 0.8*inch, 1*inch, 0.8*inch, 0.8*inch, 1.5*inch])
            exc_table.setStyle(self._get_exceedance_table_style())
            elements.append(exc_table)
        
        return elements
    
    def _create_comprehensive_content(self, project: Project, config: ReportConfig) -> List:
        """Create comprehensive report with all sections."""
        elements = []
        
        # Combine all report types
        report_types = [
            ("project_overview", self._create_project_overview_section),
            ("screening_results", lambda p: self._create_screening_content(p, config)),
            ("impact_assessment", lambda p: self._create_impact_content(p, config)),
            ("compliance_status", lambda p: self._create_compliance_content(p, config)),
            ("monitoring_data", lambda p: self._create_monitoring_content(p, config))
        ]
        
        for section_name, content_func in report_types:
            if section_name in config.include_sections:
                section_content = content_func(project)
                if section_content:
                    elements.extend(section_content)
                    elements.append(PageBreak())
        
        return elements
    
    def _create_recommendations(self, project: Project, config: ReportConfig) -> List:
        """Create recommendations section."""
        elements = []
        
        elements.append(Paragraph("Recommendations", self.styles['SectionHeading']))
        
        recommendations = []
        
        # Get latest assessments
        impact = self.db.query(ImpactRecord).filter_by(
            project_id=project.id
        ).order_by(ImpactRecord.assessment_date.desc()).first()
        
        compliance = self.db.query(ComplianceRecord).filter_by(
            project_id=project.id
        ).filter(ComplianceRecord.status != "Compliant").all()
        
        # Impact-based recommendations
        if impact:
            if impact.carbon_footprint > 1000:
                recommendations.append({
                    'priority': 'High',
                    'category': 'Climate Change',
                    'recommendation': 'Implement carbon reduction measures including renewable energy adoption, efficient equipment selection, and carbon offset programs.'
                })
            
            if impact.water_consumption > 10000:
                recommendations.append({
                    'priority': 'High',
                    'category': 'Water Resources',
                    'recommendation': 'Develop water conservation plan with recycling systems, rainwater harvesting, and efficient fixtures.'
                })
            
            if impact.biodiversity_score < 70:
                recommendations.append({
                    'priority': 'Medium',
                    'category': 'Biodiversity',
                    'recommendation': 'Enhance biodiversity protection through habitat restoration, green corridors, and native species planting.'
                })
        
        # Compliance-based recommendations
        for record in compliance[:5]:  # Top 5 non-compliant items
            recommendations.append({
                'priority': 'High',
                'category': 'Regulatory Compliance',
                'recommendation': f"{record.regulation_name}: {record.recommendation or 'Implement corrective measures'}"
            })
        
        # General recommendations
        recommendations.extend([
            {
                'priority': 'Medium',
                'category': 'Monitoring',
                'recommendation': 'Establish continuous environmental monitoring program with real-time data collection and alert systems.'
            },
            {
                'priority': 'Low',
                'category': 'Training',
                'recommendation': 'Conduct environmental awareness training for all construction personnel and contractors.'
            }
        ])
        
        # Create recommendations table
        rec_data = [["Priority", "Category", "Recommendation"]]
        
        # Sort by priority
        priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
        recommendations.sort(key=lambda x: priority_order.get(x['priority'], 3))
        
        for rec in recommendations:
            rec_data.append([rec['priority'], rec['category'], rec['recommendation']])
        
        rec_table = Table(rec_data, colWidths=[1*inch, 1.5*inch, 4*inch])
        rec_table.setStyle(self._get_recommendations_table_style(recommendations))
        elements.append(rec_table)
        
        return elements
    
    def _create_project_overview_section(self, project: Project) -> List:
        """Create project overview section."""
        elements = []
        
        elements.append(Paragraph("Project Overview", self.styles['SectionHeading']))
        
        # Project details table
        details_data = [
            ["Project Information", ""],
            ["Project Name", project.name],
            ["Project Type", project.project_type.replace('_', ' ').title()],
            ["Location", project.location],
            ["Coordinates", f"{project.latitude:.6f}, {project.longitude:.6f}" if project.latitude else "Not specified"],
            ["Project Size", f"{project.size:,.0f} m²" if project.size else "Not specified"],
            ["Duration", f"{project.duration} months" if project.duration else "Not specified"],
            ["Budget", f"${project.budget:,.1f}M" if project.budget else "Not specified"],
            ["", ""],
            ["Stakeholder Information", ""],
            ["Client", project.client_name or "Not specified"],
            ["Contractor", project.contractor or "Not specified"],
            ["Workers", f"{project.num_workers:,}" if project.num_workers else "Not specified"],
            ["", ""],
            ["Environmental Parameters", ""],
            ["Water Usage", f"{project.water_usage:,.0f} m³/day" if project.water_usage else "Not specified"],
            ["Construction Area", f"{project.construction_area:,.0f} m²" if project.construction_area else "Not specified"],
        ]
        
        details_table = Table(details_data, colWidths=[2.5*inch, 3.5*inch])
        details_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.colors['primary']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('BACKGROUND', (0, 9), (-1, 9), self.colors['primary']),
            ('TEXTCOLOR', (0, 9), (-1, 9), colors.white),
            ('BACKGROUND', (0, 14), (-1, 14), self.colors['primary']),
            ('TEXTCOLOR', (0, 14), (-1, 14), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.colors['light_gray']]),
        ]))
        
        elements.append(details_table)
        
        # Project description if available
        if project.description:
            elements.append(Spacer(1, 0.3*inch))
            elements.append(Paragraph("Project Description", self.styles['SubsectionHeading']))
            elements.append(Paragraph(project.description, self.styles['BodyJustified']))
        
        return elements
    
    def _create_appendices(self, project: Project) -> List:
        """Create appendices section."""
        elements = []
        
        elements.append(Paragraph("Appendices", self.styles['SectionHeading']))
        
        # Appendix A: Methodology Details
        elements.append(Paragraph("Appendix A: Assessment Methodology", self.styles['SubsectionHeading']))
        methodology_details = """
        The environmental impact assessment methodology employed in this study follows 
        international standards and best practices:
        
        1. Carbon Footprint Calculation:
           - Based on IPCC 2019 emission factors
           - Includes Scope 1, 2, and partial Scope 3 emissions
           - Material embodied carbon from ICE database
        
        2. Water Impact Assessment:
           - Direct consumption analysis
           - Indirect water use through materials
           - Regional water stress factors
        
        3. Biodiversity Impact:
           - Habitat sensitivity mapping
           - Species occurrence data
           - Ecosystem services valuation
        
        4. Air Quality Modeling:
           - Gaussian dispersion modeling for point sources
           - Construction dust emission factors
           - Cumulative impact assessment
        """
        elements.append(Paragraph(methodology_details, self.styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Appendix B: Regulatory Framework
        elements.append(Paragraph("Appendix B: Regulatory Framework", self.styles['SubsectionHeading']))
        
        # Get jurisdiction-specific regulations
        jurisdiction = self._get_jurisdiction(project.location)
        reg_framework = self.compliance_checker.get_regulations(jurisdiction)
        
        reg_data = [["Regulation", "Category", "Threshold", "Unit"]]
        for reg_id, reg_info in reg_framework.items():
            if 'threshold' in reg_info:
                reg_data.append([
                    reg_info['name'],
                    reg_info['category'],
                    str(reg_info['threshold']),
                    reg_info.get('unit', 'N/A')
                ])
        
        if len(reg_data) > 1:
            reg_table = Table(reg_data, colWidths=[2.5*inch, 1.5*inch, 1*inch, 1*inch])
            reg_table.setStyle(self._get_table_style())
            elements.append(reg_table)
        
        return elements
    
    # Helper methods for tables and charts
    
    def _get_table_style(self) -> TableStyle:
        """Get standard table style."""
        return TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.colors['primary']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.colors['light_gray']]),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ])
    
    def _get_impact_table_style(self) -> TableStyle:
        """Get impact assessment table style with severity coloring."""
        style = self._get_table_style()
        # Additional styling for severity column will be added dynamically
        return style
    
    def _get_compliance_table_style(self, records: List[ComplianceRecord]) -> TableStyle:
        """Get compliance table style with status coloring."""
        style = self._get_table_style()
        
        # Add status coloring
        for i, record in enumerate(records, 1):
            if record.status == "Compliant":
                style.add('TEXTCOLOR', (1, i), (1, i), self.colors['success'])
            else:
                style.add('TEXTCOLOR', (1, i), (1, i), self.colors['danger'])
        
        return style
    
    def _get_exceedance_table_style(self) -> TableStyle:
        """Get exceedance table style."""
        style = self._get_table_style()
        # Highlight all rows as they are exceedances
        style.add('BACKGROUND', (0, 1), (-1, -1), colors.Color(1, 0.9, 0.9))
        return style
    
    def _get_recommendations_table_style(self, recommendations: List[Dict]) -> TableStyle:
        """Get recommendations table style with priority coloring."""
        style = self._get_table_style()
        
        # Add priority coloring
        for i, rec in enumerate(recommendations, 1):
            if rec['priority'] == 'High':
                style.add('TEXTCOLOR', (0, i), (0, i), self.colors['danger'])
            elif rec['priority'] == 'Medium':
                style.add('TEXTCOLOR', (0, i), (0, i), self.colors['warning'])
            else:
                style.add('TEXTCOLOR', (0, i), (0, i), self.colors['info'])
        
        return style
    
    def _get_severity_badge(self, value: float, medium_threshold: float, high_threshold: float) -> str:
        """Get severity badge based on value."""
        if value >= high_threshold:
            return "High"
        elif value >= medium_threshold:
            return "Medium"
        else:
            return "Low"
    
    def _get_jurisdiction(self, location: str) -> str:
        """Get jurisdiction from location."""
        location_lower = location.lower()
        if any(loc in location_lower for loc in ['dubai', 'abu dhabi', 'sharjah', 'uae']):
            if 'dubai' in location_lower:
                return 'Dubai'
            elif 'abu dhabi' in location_lower:
                return 'Abu Dhabi'
            else:
                return 'UAE Federal'
        elif any(loc in location_lower for loc in ['riyadh', 'jeddah', 'neom', 'ksa', 'saudi']):
            if 'neom' in location_lower:
                return 'NEOM'
            else:
                return 'KSA National'
        else:
            return 'UAE Federal'  # Default
    
    def _create_impact_chart(self, impact: ImpactRecord) -> Optional[io.BytesIO]:
        """Create impact comparison bar chart."""
        try:
            fig, ax = plt.subplots(figsize=(8, 6))
            
            categories = ['Carbon\nFootprint', 'Water\nConsumption', 'Waste\nGeneration', 
                         'Energy\nUsage', 'Biodiversity\nImpact']
            values = [
                impact.carbon_footprint / 100,  # Scale for visualization
                impact.water_consumption / 1000,
                impact.waste_generation / 10,
                impact.energy_usage / 100,
                (100 - impact.biodiversity_score) / 10
            ]
            
            bars = ax.bar(categories, values, color=[
                self.colors['danger'].rgb(),
                self.colors['info'].rgb(),
                self.colors['warning'].rgb(),
                self.colors['secondary'].rgb(),
                self.colors['success'].rgb()
            ])
            
            ax.set_ylabel('Relative Impact Scale')
            ax.set_title('Environmental Impact Overview')
            ax.grid(True, alpha=0.3)
            
            # Add value labels
            for bar, val in zip(bars, values):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{val:.1f}', ha='center', va='bottom')
            
            plt.tight_layout()
            
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150)
            buffer.seek(0)
            plt.close()
            
            return buffer
            
        except Exception as e:
            logger.error(f"Failed to create impact chart: {e}")
            return None
    
    def _create_compliance_pie_chart(self, compliant: int, non_compliant: int) -> Optional[io.BytesIO]:
        """Create compliance status pie chart."""
        try:
            fig, ax = plt.subplots(figsize=(6, 6))
            
            sizes = [compliant, non_compliant]
            labels = ['Compliant', 'Non-Compliant']
            colors_list = [self.colors['success'].rgb(), self.colors['danger'].rgb()]
            
            wedges, texts, autotexts = ax.pie(
                sizes, 
                labels=labels, 
                colors=colors_list,
                autopct='%1.1f%%',
                startangle=90
            )
            
            ax.set_title('Regulatory Compliance Status')
            
            plt.tight_layout()
            
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150)
            buffer.seek(0)
            plt.close()
            
            return buffer
            
        except Exception as e:
            logger.error(f"Failed to create compliance chart: {e}")
            return None
    
    def _create_time_series_chart(
        self, 
        measurements: List[MonitoringData], 
        parameter: str
    ) -> Optional[io.BytesIO]:
        """Create time series chart for monitoring data."""
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Sort by date
            measurements.sort(key=lambda x: x.measurement_date)
            
            dates = [m.measurement_date for m in measurements]
            values = [m.value for m in measurements]
            
            # Plot main data
            ax.plot(dates, values, 'b-', linewidth=2, label='Measured Value')
            ax.scatter(dates, values, color='blue', s=50, zorder=5)
            
            # Add limit line if available
            if measurements and measurements[0].limit_value:
                limit = measurements[0].limit_value
                ax.axhline(y=limit, color='red', linestyle='--', 
                          linewidth=2, label=f'Limit ({limit})')
            
            # Highlight exceedances
            exceedances = [m for m in measurements if m.exceeds_limit]
            if exceedances:
                exc_dates = [m.measurement_date for m in exceedances]
                exc_values = [m.value for m in exceedances]
                ax.scatter(exc_dates, exc_values, color='red', s=100, 
                          marker='^', zorder=10, label='Exceedance')
            
            ax.set_xlabel('Date')
            ax.set_ylabel(f'{parameter.upper()} ({measurements[0].unit})')
            ax.set_title(f'{parameter.upper()} Monitoring Trend')
            ax.grid(True, alpha=0.3)
            ax.legend()
            
            # Format x-axis
            fig.autofmt_xdate()
            
            plt.tight_layout()
            
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150)
            buffer.seek(0)
            plt.close()
            
            return buffer
            
        except Exception as e:
            logger.error(f"Failed to create time series chart: {e}")
            return None
    
    def _add_page_elements(self, canvas, doc):
        """Add page header, footer, and other elements."""
        canvas.saveState()
        
        # Page dimensions
        width, height = A4
        
        # Header line
        canvas.setStrokeColor(self.colors['primary'])
        canvas.setLineWidth(2)
        canvas.line(72, height - 50, width - 72, height - 50)
        
        # Footer
        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(colors.grey)
        canvas.drawCentredString(
            width / 2.0, 
            40,
            f"Environmental Impact Assessment Report - Page {doc.page}"
        )
        
        # Watermark (if enabled)
        if hasattr(doc, 'watermark') and doc.watermark:
            canvas.setFont("Helvetica", 48)
            canvas.setFillColor(colors.Color(0, 0, 0, alpha=0.1))
            canvas.translate(width/2, height/2)
            canvas.rotate(45)
            canvas.drawCentredString(0, 0, "DRAFT")
            
        canvas.restoreState()
    
    def generate_batch_reports(
        self,
        project_ids: List[int],
        config: ReportConfig,
        output_dir: str
    ) -> List[str]:
        """
        Generate reports for multiple projects.
        
        Args:
            project_ids: List of project IDs
            config: Report configuration
            output_dir: Output directory for reports
            
        Returns:
            List of generated file paths
        """
        generated_files = []
        
        os.makedirs(output_dir, exist_ok=True)
        
        for project_id in project_ids:
            try:
                project = self.get_by_id(project_id)
                if not project:
                    logger.warning(f"Project {project_id} not found")
                    continue
                
                filename = f"{config.report_type.value}_{project.name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
                output_path = os.path.join(output_dir, filename)
                
                self.generate_report(project_id, config, output_path)
                generated_files.append(output_path)
                
            except Exception as e:
                logger.error(f"Failed to generate report for project {project_id}: {e}")
        
        return generated_files