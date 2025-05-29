"""
Report Templates
Customizable templates for different report types

Author: Edy Bassil
Email: bassileddy@gmail.com
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Table, TableStyle, Spacer, PageBreak


class ReportTemplate(ABC):
    """Base class for report templates."""
    
    def __init__(self, styles: Dict[str, ParagraphStyle], color_scheme: Dict[str, Any]):
        self.styles = styles
        self.colors = color_scheme
    
    @abstractmethod
    def get_cover_page(self, project_data: Dict[str, Any]) -> List:
        """Generate cover page elements."""
        pass
    
    @abstractmethod
    def get_main_content(self, data: Dict[str, Any]) -> List:
        """Generate main report content."""
        pass
    
    def get_header(self, title: str) -> List:
        """Generate section header."""
        return [
            Paragraph(title, self.styles['SectionHeading']),
            Spacer(1, 0.2 * 72)  # 0.2 inch
        ]
    
    def get_subheader(self, title: str) -> List:
        """Generate subsection header."""
        return [
            Paragraph(title, self.styles['SubsectionHeading']),
            Spacer(1, 0.1 * 72)
        ]
    
    def create_data_table(
        self, 
        data: List[List[str]], 
        col_widths: List[float],
        highlight_header: bool = True
    ) -> Table:
        """Create formatted data table."""
        table = Table(data, colWidths=col_widths)
        
        style_commands = [
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]
        
        if highlight_header:
            style_commands.extend([
                ('BACKGROUND', (0, 0), (-1, 0), self.colors['primary']),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.colors['light_gray']]),
            ])
        
        table.setStyle(TableStyle(style_commands))
        return table
    
    def format_jurisdiction_badge(self, location: str) -> str:
        """Format jurisdiction badge for display."""
        jurisdiction_map = {
            'dubai': 'Dubai Municipality',
            'abu dhabi': 'Environment Agency Abu Dhabi',
            'sharjah': 'EPAA Sharjah',
            'riyadh': 'Saudi Environmental Authority',
            'jeddah': 'Saudi Environmental Authority',
            'neom': 'NEOM Environmental Department'
        }
        
        location_lower = location.lower()
        for key, value in jurisdiction_map.items():
            if key in location_lower:
                return value
        
        return 'UAE Federal Environmental Authority'


class ScreeningTemplate(ReportTemplate):
    """Template for screening reports."""
    
    def get_cover_page(self, project_data: Dict[str, Any]) -> List:
        """Generate screening report cover page."""
        elements = []
        
        # Title
        elements.append(Paragraph(
            "Environmental Impact Assessment",
            self.styles['CoverTitle']
        ))
        elements.append(Paragraph(
            "Screening Report",
            self.styles['CoverSubtitle']
        ))
        elements.append(Spacer(1, 72))  # 1 inch
        
        # Project info
        project_info = f"""
        <para align="center">
        <b>Project:</b> {project_data['name']}<br/>
        <b>Type:</b> {project_data['project_type'].replace('_', ' ').title()}<br/>
        <b>Location:</b> {project_data['location']}<br/>
        <b>Date:</b> {datetime.now().strftime('%B %d, %Y')}
        </para>
        """
        elements.append(Paragraph(project_info, self.styles['Normal']))
        
        return elements
    
    def get_main_content(self, data: Dict[str, Any]) -> List:
        """Generate screening report main content."""
        elements = []
        
        # Screening results
        elements.extend(self.get_header("Screening Results"))
        
        assessment = data.get('assessment', {})
        if assessment:
            # EIA requirement summary
            eia_required = assessment.get('eia_required', False)
            eia_text = "Required" if eia_required else "Not Required"
            eia_color = self.colors['danger'] if eia_required else self.colors['success']
            
            summary_text = f"""
            Based on the screening assessment, an Environmental Impact Assessment is 
            <font color="{eia_color}"><b>{eia_text}</b></font> for this project.
            """
            elements.append(Paragraph(summary_text, self.styles['BodyJustified']))
            elements.append(Spacer(1, 0.2 * 72))
            
            # Results table
            result_data = [
                ["Parameter", "Value"],
                ["EIA Requirement", eia_text],
                ["EIA Level", assessment.get('eia_level', 'N/A')],
                ["Assessment Method", assessment.get('assessment_type', 'Screening').title()],
                ["Estimated Duration", f"{assessment.get('estimated_duration', 'N/A')} months"]
            ]
            
            table = self.create_data_table(result_data, [3 * 72, 3 * 72])
            elements.append(table)
            elements.append(Spacer(1, 0.3 * 72))
            
            # Key concerns
            concerns = assessment.get('key_concerns', [])
            if concerns:
                elements.extend(self.get_subheader("Key Environmental Concerns"))
                for concern in concerns:
                    elements.append(Paragraph(f"• {concern}", self.styles['Normal']))
                elements.append(Spacer(1, 0.2 * 72))
            
            # Regulatory requirements
            requirements = assessment.get('regulatory_requirements', [])
            if requirements:
                elements.extend(self.get_subheader("Applicable Regulations"))
                for req in requirements[:10]:  # Limit to top 10
                    elements.append(Paragraph(f"• {req}", self.styles['Normal']))
                elements.append(Spacer(1, 0.2 * 72))
            
            # Specialist studies
            studies = assessment.get('specialist_studies', [])
            if studies:
                elements.extend(self.get_subheader("Required Specialist Studies"))
                for study in studies:
                    elements.append(Paragraph(f"• {study}", self.styles['Normal']))
        
        return elements


class ImpactTemplate(ReportTemplate):
    """Template for impact assessment reports."""
    
    def get_cover_page(self, project_data: Dict[str, Any]) -> List:
        """Generate impact assessment cover page."""
        elements = []
        
        elements.append(Paragraph(
            "Environmental Impact Assessment",
            self.styles['CoverTitle']
        ))
        elements.append(Paragraph(
            "Impact Analysis Report",
            self.styles['CoverSubtitle']
        ))
        elements.append(Spacer(1, 72))
        
        # Project and impact summary
        impact_data = project_data.get('latest_impact', {})
        severity = impact_data.get('impact_severity', 'Not Assessed')
        severity_color = {
            'Low': self.colors['success'],
            'Medium': self.colors['warning'],
            'High': self.colors['danger']
        }.get(severity, self.colors['info'])
        
        project_info = f"""
        <para align="center">
        <b>Project:</b> {project_data['name']}<br/>
        <b>Location:</b> {project_data['location']}<br/>
        <b>Impact Severity:</b> <font color="{severity_color}"><b>{severity}</b></font><br/>
        <b>Assessment Date:</b> {datetime.now().strftime('%B %d, %Y')}
        </para>
        """
        elements.append(Paragraph(project_info, self.styles['Normal']))
        
        return elements
    
    def get_main_content(self, data: Dict[str, Any]) -> List:
        """Generate impact assessment main content."""
        elements = []
        
        impact = data.get('impact', {})
        if not impact:
            elements.append(Paragraph(
                "No impact assessment data available.",
                self.styles['Normal']
            ))
            return elements
        
        # Executive Summary
        elements.extend(self.get_header("Impact Assessment Summary"))
        
        summary_text = f"""
        The environmental impact assessment reveals that this project will generate 
        approximately <b>{impact.get('carbon_footprint', 0):.1f} tons of CO₂ equivalent</b> 
        emissions, consume <b>{impact.get('water_consumption', 0):.0f} cubic meters</b> of 
        water, and produce <b>{impact.get('waste_generation', 0):.0f} tons</b> of waste 
        during the construction phase. The overall environmental impact is classified as 
        <b>{impact.get('impact_severity', 'Medium')}</b>.
        """
        elements.append(Paragraph(summary_text, self.styles['BodyJustified']))
        elements.append(Spacer(1, 0.3 * 72))
        
        # Detailed Impact Table
        elements.extend(self.get_header("Environmental Impacts"))
        
        impact_data = [
            ["Impact Category", "Value", "Unit", "Benchmark", "Status"],
            [
                "Carbon Footprint",
                f"{impact.get('carbon_footprint', 0):.1f}",
                "tons CO₂e",
                "1,000",
                self._get_status_text(impact.get('carbon_footprint', 0), 1000)
            ],
            [
                "Water Consumption",
                f"{impact.get('water_consumption', 0):.0f}",
                "m³",
                "10,000",
                self._get_status_text(impact.get('water_consumption', 0), 10000)
            ],
            [
                "Waste Generation",
                f"{impact.get('waste_generation', 0):.0f}",
                "tons",
                "100",
                self._get_status_text(impact.get('waste_generation', 0), 100)
            ],
            [
                "Energy Usage",
                f"{impact.get('energy_usage', 0):.0f}",
                "MWh",
                "500",
                self._get_status_text(impact.get('energy_usage', 0), 500)
            ],
            [
                "Biodiversity Score",
                f"{impact.get('biodiversity_score', 0):.1f}",
                "index",
                "70",
                self._get_status_text(impact.get('biodiversity_score', 0), 70, reverse=True)
            ]
        ]
        
        # Add air quality data if available
        if impact.get('pm10_concentration'):
            impact_data.append([
                "PM10 Concentration",
                f"{impact['pm10_concentration']:.1f}",
                "µg/m³",
                "150",
                self._get_status_text(impact['pm10_concentration'], 150)
            ])
        
        if impact.get('pm25_concentration'):
            impact_data.append([
                "PM2.5 Concentration",
                f"{impact['pm25_concentration']:.1f}",
                "µg/m³",
                "65",
                self._get_status_text(impact['pm25_concentration'], 65)
            ])
        
        table = self.create_data_table(
            impact_data,
            [2 * 72, 1.2 * 72, 0.8 * 72, 0.8 * 72, 1.2 * 72]
        )
        elements.append(table)
        
        # Risk Assessment
        risks = data.get('risks', [])
        if risks:
            elements.append(PageBreak())
            elements.extend(self.get_header("Environmental Risk Assessment"))
            
            risk_data = [["Risk Category", "Likelihood", "Consequence", "Risk Level"]]
            for risk in risks[:10]:  # Top 10 risks
                risk_data.append([
                    risk.get('category', 'Unknown'),
                    risk.get('likelihood', 'Medium'),
                    risk.get('consequence', 'Medium'),
                    risk.get('risk_level', 'Medium')
                ])
            
            risk_table = self.create_data_table(
                risk_data,
                [2.5 * 72, 1.5 * 72, 1.5 * 72, 1.5 * 72]
            )
            elements.append(risk_table)
        
        return elements
    
    def _get_status_text(self, value: float, benchmark: float, reverse: bool = False) -> str:
        """Get status text based on benchmark comparison."""
        if reverse:
            if value >= benchmark:
                return "Good"
            else:
                return "Poor"
        else:
            if value <= benchmark:
                return "Good"
            else:
                return "Exceeds"


class ComplianceTemplate(ReportTemplate):
    """Template for compliance reports."""
    
    def get_cover_page(self, project_data: Dict[str, Any]) -> List:
        """Generate compliance report cover page."""
        elements = []
        
        elements.append(Paragraph(
            "Environmental Compliance Report",
            self.styles['CoverTitle']
        ))
        
        # Calculate compliance rate
        compliance_data = project_data.get('compliance_summary', {})
        compliance_rate = compliance_data.get('compliance_rate', 100)
        
        rate_color = self.colors['success'] if compliance_rate >= 90 else \
                    self.colors['warning'] if compliance_rate >= 70 else \
                    self.colors['danger']
        
        elements.append(Paragraph(
            f'<font color="{rate_color}"><b>{compliance_rate:.1f}% Compliant</b></font>',
            self.styles['CoverSubtitle']
        ))
        elements.append(Spacer(1, 72))
        
        project_info = f"""
        <para align="center">
        <b>Project:</b> {project_data['name']}<br/>
        <b>Location:</b> {project_data['location']}<br/>
        <b>Regulatory Framework:</b> {self.format_jurisdiction_badge(project_data['location'])}<br/>
        <b>Assessment Date:</b> {datetime.now().strftime('%B %d, %Y')}
        </para>
        """
        elements.append(Paragraph(project_info, self.styles['Normal']))
        
        return elements
    
    def get_main_content(self, data: Dict[str, Any]) -> List:
        """Generate compliance report main content."""
        elements = []
        
        # Compliance Overview
        elements.extend(self.get_header("Compliance Overview"))
        
        summary = data.get('compliance_summary', {})
        total_checks = summary.get('total_checks', 0)
        compliant_checks = summary.get('compliant_checks', 0)
        non_compliant = total_checks - compliant_checks
        
        overview_text = f"""
        The regulatory compliance assessment evaluated <b>{total_checks}</b> environmental 
        requirements applicable to this project. The assessment found <b>{compliant_checks}</b> 
        requirements in compliance and <b>{non_compliant}</b> requiring corrective action.
        """
        elements.append(Paragraph(overview_text, self.styles['BodyJustified']))
        elements.append(Spacer(1, 0.3 * 72))
        
        # Summary Statistics
        summary_data = [
            ["Compliance Metric", "Value"],
            ["Total Requirements Checked", str(total_checks)],
            ["Compliant Items", str(compliant_checks)],
            ["Non-Compliant Items", str(non_compliant)],
            ["Compliance Rate", f"{summary.get('compliance_rate', 0):.1f}%"],
            ["Critical Violations", str(summary.get('critical_violations', 0))],
            ["Action Items Generated", str(summary.get('action_items', non_compliant))]
        ]
        
        table = self.create_data_table(summary_data, [3 * 72, 2 * 72])
        elements.append(table)
        elements.append(Spacer(1, 0.3 * 72))
        
        # Non-Compliant Items
        non_compliant_items = data.get('non_compliant_items', [])
        if non_compliant_items:
            elements.extend(self.get_header("Non-Compliant Items Requiring Action"))
            
            for item in non_compliant_items[:15]:  # Limit to top 15
                category = item.get('category', 'General')
                regulation = item.get('regulation_name', 'Unknown')
                actual = item.get('actual_value', 'N/A')
                required = item.get('required_value', 'N/A')
                
                item_text = f"""
                <b>{category} - {regulation}</b><br/>
                Current: {actual} | Required: {required}<br/>
                <i>Action: {item.get('recommendation', 'Implement corrective measures')}</i>
                """
                elements.append(Paragraph(item_text, self.styles['Normal']))
                elements.append(Spacer(1, 0.2 * 72))
        
        # Compliance by Category
        categories = data.get('compliance_by_category', {})
        if categories:
            elements.append(PageBreak())
            elements.extend(self.get_header("Compliance by Category"))
            
            cat_data = [["Category", "Checked", "Compliant", "Rate"]]
            for category, stats in categories.items():
                total = stats.get('total', 0)
                compliant = stats.get('compliant', 0)
                rate = (compliant / total * 100) if total > 0 else 100
                cat_data.append([
                    category,
                    str(total),
                    str(compliant),
                    f"{rate:.1f}%"
                ])
            
            cat_table = self.create_data_table(
                cat_data,
                [2.5 * 72, 1 * 72, 1 * 72, 1 * 72]
            )
            elements.append(cat_table)
        
        return elements


class MonitoringTemplate(ReportTemplate):
    """Template for monitoring reports."""
    
    def get_cover_page(self, project_data: Dict[str, Any]) -> List:
        """Generate monitoring report cover page."""
        elements = []
        
        elements.append(Paragraph(
            "Environmental Monitoring Report",
            self.styles['CoverTitle']
        ))
        
        # Date range
        date_range = project_data.get('date_range', {})
        start_date = date_range.get('start', datetime.now().replace(day=1))
        end_date = date_range.get('end', datetime.now())
        
        elements.append(Paragraph(
            f"{start_date.strftime('%B %d')} - {end_date.strftime('%B %d, %Y')}",
            self.styles['CoverSubtitle']
        ))
        elements.append(Spacer(1, 72))
        
        # Project info with monitoring summary
        monitoring_summary = project_data.get('monitoring_summary', {})
        exceedances = monitoring_summary.get('total_exceedances', 0)
        
        project_info = f"""
        <para align="center">
        <b>Project:</b> {project_data['name']}<br/>
        <b>Location:</b> {project_data['location']}<br/>
        <b>Monitoring Points:</b> {monitoring_summary.get('monitoring_points', 'Multiple')}<br/>
        <b>Exceedances Recorded:</b> <font color="{self.colors['danger'] if exceedances > 0 else self.colors['success']}">
        <b>{exceedances}</b></font>
        </para>
        """
        elements.append(Paragraph(project_info, self.styles['Normal']))
        
        return elements
    
    def get_main_content(self, data: Dict[str, Any]) -> List:
        """Generate monitoring report main content."""
        elements = []
        
        # Monitoring Summary
        elements.extend(self.get_header("Monitoring Summary"))
        
        summary = data.get('monitoring_summary', {})
        parameters = summary.get('parameters', {})
        
        if parameters:
            summary_data = [["Parameter", "Measurements", "Average", "Max", "Exceedances"]]
            
            for param, stats in parameters.items():
                summary_data.append([
                    param.upper(),
                    str(stats.get('count', 0)),
                    f"{stats.get('average', 0):.1f}",
                    f"{stats.get('max', 0):.1f}",
                    str(stats.get('exceedances', 0))
                ])
            
            table = self.create_data_table(
                summary_data,
                [1.5 * 72, 1.2 * 72, 1.2 * 72, 1.2 * 72, 1.2 * 72]
            )
            elements.append(table)
            elements.append(Spacer(1, 0.3 * 72))
        
        # Trends Analysis
        trends = data.get('trends', [])
        if trends:
            elements.extend(self.get_header("Parameter Trends"))
            
            for trend in trends:
                param = trend.get('parameter', 'Unknown')
                direction = trend.get('trend', 'stable')
                change = trend.get('change_percentage', 0)
                
                trend_color = self.colors['success'] if direction == 'decreasing' else \
                             self.colors['danger'] if direction == 'increasing' else \
                             self.colors['info']
                
                trend_text = f"""
                <b>{param.upper()}</b>: <font color="{trend_color}">
                {direction.title()} ({change:+.1f}%)</font>
                """
                elements.append(Paragraph(trend_text, self.styles['Normal']))
            elements.append(Spacer(1, 0.2 * 72))
        
        # Recent Exceedances
        exceedances = data.get('exceedances', [])
        if exceedances:
            elements.extend(self.get_header("Recent Limit Exceedances"))
            
            exc_data = [["Date", "Parameter", "Value", "Limit", "Location"]]
            for exc in exceedances[:20]:  # Top 20
                exc_data.append([
                    exc.get('date', 'N/A'),
                    exc.get('parameter', 'N/A').upper(),
                    f"{exc.get('value', 0):.1f}",
                    f"{exc.get('limit', 0):.1f}",
                    exc.get('location', 'N/A')
                ])
            
            exc_table = self.create_data_table(
                exc_data,
                [1.2 * 72, 1 * 72, 0.8 * 72, 0.8 * 72, 2 * 72]
            )
            elements.append(exc_table)
        
        # Alerts
        alerts = data.get('alerts', [])
        if alerts:
            elements.append(PageBreak())
            elements.extend(self.get_header("Environmental Alerts"))
            
            for alert in alerts[:10]:  # Top 10
                severity = alert.get('severity', 'medium')
                severity_color = {
                    'high': self.colors['danger'],
                    'medium': self.colors['warning'],
                    'low': self.colors['info']
                }.get(severity, self.colors['info'])
                
                alert_text = f"""
                <font color="{severity_color}"><b>{severity.upper()} - {alert.get('parameter', 'Unknown').upper()}</b></font><br/>
                {alert.get('message', 'Alert triggered')}<br/>
                <i>Location: {alert.get('location', 'N/A')} | Time: {alert.get('timestamp', 'N/A')}</i>
                """
                elements.append(Paragraph(alert_text, self.styles['Normal']))
                elements.append(Spacer(1, 0.2 * 72))
        
        return elements


class ComprehensiveTemplate(ReportTemplate):
    """Template for comprehensive reports combining all sections."""
    
    def __init__(self, styles: Dict[str, ParagraphStyle], color_scheme: Dict[str, Any]):
        super().__init__(styles, color_scheme)
        # Initialize sub-templates
        self.screening_template = ScreeningTemplate(styles, color_scheme)
        self.impact_template = ImpactTemplate(styles, color_scheme)
        self.compliance_template = ComplianceTemplate(styles, color_scheme)
        self.monitoring_template = MonitoringTemplate(styles, color_scheme)
    
    def get_cover_page(self, project_data: Dict[str, Any]) -> List:
        """Generate comprehensive report cover page."""
        elements = []
        
        elements.append(Paragraph(
            "Environmental Impact Assessment",
            self.styles['CoverTitle']
        ))
        elements.append(Paragraph(
            "Comprehensive Report",
            self.styles['CoverSubtitle']
        ))
        elements.append(Spacer(1, 0.5 * 72))
        
        # Quick stats
        compliance_rate = project_data.get('compliance_summary', {}).get('compliance_rate', 100)
        impact_severity = project_data.get('latest_impact', {}).get('impact_severity', 'Medium')
        
        quick_stats = f"""
        <para align="center">
        <b>Compliance:</b> {compliance_rate:.1f}% | 
        <b>Impact Level:</b> {impact_severity} | 
        <b>Status:</b> {project_data.get('status', 'Active')}
        </para>
        """
        elements.append(Paragraph(quick_stats, self.styles['Normal']))
        elements.append(Spacer(1, 0.5 * 72))
        
        project_info = f"""
        <para align="center">
        <b>Project:</b> {project_data['name']}<br/>
        <b>Type:</b> {project_data['project_type'].replace('_', ' ').title()}<br/>
        <b>Location:</b> {project_data['location']}<br/>
        <b>Client:</b> {project_data.get('client_name', 'Not specified')}<br/>
        <b>Report Date:</b> {datetime.now().strftime('%B %d, %Y')}
        </para>
        """
        elements.append(Paragraph(project_info, self.styles['Normal']))
        
        elements.append(Spacer(1, 2 * 72))
        
        # Report sections
        sections_text = """
        <para align="center">
        <b>This comprehensive report includes:</b><br/>
        • Executive Summary<br/>
        • Environmental Screening Results<br/>
        • Impact Assessment Analysis<br/>
        • Regulatory Compliance Status<br/>
        • Environmental Monitoring Data<br/>
        • Risk Assessment & Mitigation<br/>
        • Recommendations & Action Plan
        </para>
        """
        elements.append(Paragraph(sections_text, self.styles['Normal']))
        
        return elements
    
    def get_main_content(self, data: Dict[str, Any]) -> List:
        """Generate comprehensive report main content."""
        elements = []
        
        # Executive Summary
        elements.extend(self._create_executive_summary(data))
        elements.append(PageBreak())
        
        # Screening Results
        if data.get('assessment'):
            elements.extend(self.screening_template.get_main_content(data))
            elements.append(PageBreak())
        
        # Impact Assessment
        if data.get('impact'):
            elements.extend(self.impact_template.get_main_content(data))
            elements.append(PageBreak())
        
        # Compliance Status
        if data.get('compliance_summary'):
            elements.extend(self.compliance_template.get_main_content(data))
            elements.append(PageBreak())
        
        # Monitoring Data
        if data.get('monitoring_summary'):
            elements.extend(self.monitoring_template.get_main_content(data))
            elements.append(PageBreak())
        
        # Integrated Analysis
        elements.extend(self._create_integrated_analysis(data))
        
        return elements
    
    def _create_executive_summary(self, data: Dict[str, Any]) -> List:
        """Create executive summary for comprehensive report."""
        elements = []
        
        elements.extend(self.get_header("Executive Summary"))
        
        # Project overview
        project = data.get('project', {})
        summary_text = f"""
        This comprehensive Environmental Impact Assessment report presents the complete 
        environmental analysis for the {project.get('project_type', 'construction').replace('_', ' ')} 
        project "{project.get('name', 'Unknown')}" located in {project.get('location', 'Unknown')}. 
        The assessment encompasses screening results, detailed impact analysis, regulatory 
        compliance evaluation, and ongoing environmental monitoring data.
        """
        elements.append(Paragraph(summary_text, self.styles['BodyJustified']))
        elements.append(Spacer(1, 0.2 * 72))
        
        # Key findings
        elements.extend(self.get_subheader("Key Findings"))
        
        # Create findings based on available data
        findings = []
        
        # Screening findings
        assessment = data.get('assessment', {})
        if assessment:
            eia_status = "required" if assessment.get('eia_required') else "not required"
            findings.append(f"Environmental Impact Assessment is <b>{eia_status}</b>")
        
        # Impact findings
        impact = data.get('impact', {})
        if impact:
            findings.append(f"Carbon footprint: <b>{impact.get('carbon_footprint', 0):.1f} tons CO₂e</b>")
            findings.append(f"Environmental impact severity: <b>{impact.get('impact_severity', 'Medium')}</b>")
        
        # Compliance findings
        compliance = data.get('compliance_summary', {})
        if compliance:
            findings.append(f"Regulatory compliance: <b>{compliance.get('compliance_rate', 100):.1f}%</b>")
            non_compliant = compliance.get('total_checks', 0) - compliance.get('compliant_checks', 0)
            if non_compliant > 0:
                findings.append(f"Action items: <b>{non_compliant} non-compliant items</b>")
        
        # Monitoring findings
        monitoring = data.get('monitoring_summary', {})
        if monitoring:
            exceedances = monitoring.get('total_exceedances', 0)
            if exceedances > 0:
                findings.append(f"Monitoring alerts: <b>{exceedances} limit exceedances</b>")
        
        for finding in findings:
            elements.append(Paragraph(f"• {finding}", self.styles['Normal']))
        
        elements.append(Spacer(1, 0.2 * 72))
        
        # Overall assessment
        elements.extend(self.get_subheader("Overall Assessment"))
        
        # Determine overall status
        compliance_rate = compliance.get('compliance_rate', 100) if compliance else 100
        severity = impact.get('impact_severity', 'Medium') if impact else 'Medium'
        exceedances = monitoring.get('total_exceedances', 0) if monitoring else 0
        
        if compliance_rate >= 90 and severity in ['Low', 'Medium'] and exceedances == 0:
            overall_status = "Good"
            status_color = self.colors['success']
        elif compliance_rate >= 70 and severity != 'High' and exceedances < 5:
            overall_status = "Satisfactory with Minor Issues"
            status_color = self.colors['warning']
        else:
            overall_status = "Requires Immediate Attention"
            status_color = self.colors['danger']
        
        overall_text = f"""
        The project's overall environmental performance is assessed as 
        <font color="{status_color}"><b>{overall_status}</b></font>. 
        Continued monitoring and implementation of recommended mitigation measures 
        are essential for maintaining environmental compliance.
        """
        elements.append(Paragraph(overall_text, self.styles['BodyJustified']))
        
        return elements
    
    def _create_integrated_analysis(self, data: Dict[str, Any]) -> List:
        """Create integrated analysis section."""
        elements = []
        
        elements.extend(self.get_header("Integrated Environmental Analysis"))
        
        # Cross-reference different assessments
        assessment = data.get('assessment', {})
        impact = data.get('impact', {})
        compliance = data.get('compliance_summary', {})
        monitoring = data.get('monitoring_summary', {})
        
        # Risk-Impact-Compliance Matrix
        elements.extend(self.get_subheader("Risk-Impact-Compliance Correlation"))
        
        correlation_text = """
        Analysis of the relationship between identified environmental risks, measured 
        impacts, and regulatory compliance reveals the following correlations:
        """
        elements.append(Paragraph(correlation_text, self.styles['BodyJustified']))
        elements.append(Spacer(1, 0.2 * 72))
        
        # Create correlation insights
        insights = []
        
        if impact and compliance:
            if impact.get('carbon_footprint', 0) > 1000 and compliance.get('compliance_rate', 100) < 90:
                insights.append(
                    "High carbon emissions correlate with climate-related compliance gaps"
                )
            
            if impact.get('water_consumption', 0) > 10000:
                insights.append(
                    "Significant water consumption requires enhanced conservation measures"
                )
        
        if monitoring and compliance:
            exceedances = monitoring.get('total_exceedances', 0)
            if exceedances > 0 and compliance.get('compliance_rate', 100) < 100:
                insights.append(
                    "Monitoring exceedances align with identified compliance deficiencies"
                )
        
        if not insights:
            insights.append("Environmental parameters are within acceptable ranges")
            insights.append("No significant correlations identified requiring immediate action")
        
        for insight in insights:
            elements.append(Paragraph(f"• {insight}", self.styles['Normal']))
        
        elements.append(Spacer(1, 0.3 * 72))
        
        # Recommendations Priority Matrix
        elements.extend(self.get_subheader("Prioritized Action Plan"))
        
        action_data = [["Priority", "Action Item", "Timeline", "Responsible Party"]]
        
        # Generate prioritized actions based on findings
        actions = []
        
        # High priority actions
        if compliance and compliance.get('compliance_rate', 100) < 90:
            actions.append([
                "High",
                "Address regulatory non-compliance items",
                "Immediate",
                "Environmental Manager"
            ])
        
        if monitoring and monitoring.get('total_exceedances', 0) > 5:
            actions.append([
                "High",
                "Investigate and mitigate monitoring exceedances",
                "Within 7 days",
                "Site Supervisor"
            ])
        
        # Medium priority actions
        if impact and impact.get('carbon_footprint', 0) > 1000:
            actions.append([
                "Medium",
                "Implement carbon reduction measures",
                "Within 30 days",
                "Project Manager"
            ])
        
        # Low priority actions
        actions.append([
            "Low",
            "Enhance environmental training program",
            "Within 60 days",
            "HSE Department"
        ])
        
        action_data.extend(actions)
        
        action_table = self.create_data_table(
            action_data,
            [0.8 * 72, 3 * 72, 1.2 * 72, 1.5 * 72]
        )
        elements.append(action_table)
        
        return elements