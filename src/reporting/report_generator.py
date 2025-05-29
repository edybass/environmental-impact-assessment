"""
Report Generator
High-level interface for report generation

Author: Edy Bassil
Email: bassileddy@gmail.com
"""

from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import logging
from sqlalchemy.orm import Session

from src.services.report_service import ReportService, ReportConfig, ReportType, ReportLanguage
from src.models import get_session, Project, Assessment, ImpactRecord, ComplianceRecord
from .report_templates import (
    ScreeningTemplate, ImpactTemplate, ComplianceTemplate,
    MonitoringTemplate, ComprehensiveTemplate
)

logger = logging.getLogger(__name__)


class ReportGenerator:
    """
    High-level report generator with template support.
    Simplifies report generation for common use cases.
    """
    
    def __init__(self, db: Session = None):
        """Initialize report generator."""
        self.db = db or get_session()
        self.report_service = ReportService(self.db)
        
        # Template mapping
        self.templates = {
            ReportType.SCREENING: ScreeningTemplate,
            ReportType.IMPACT: ImpactTemplate,
            ReportType.COMPLIANCE: ComplianceTemplate,
            ReportType.MONITORING: MonitoringTemplate,
            ReportType.COMPREHENSIVE: ComprehensiveTemplate
        }
    
    def generate_screening_report(
        self,
        project_id: int,
        output_path: Optional[str] = None,
        language: ReportLanguage = ReportLanguage.ENGLISH
    ) -> Union[str, bytes]:
        """Generate screening report for a project."""
        logger.info(f"Generating screening report for project {project_id}")
        
        config = ReportConfig(
            report_type=ReportType.SCREENING,
            language=language,
            include_sections=[
                "project_overview",
                "screening_results",
                "regulatory_requirements",
                "recommendations"
            ]
        )
        
        return self.report_service.generate_report(project_id, config, output_path)
    
    def generate_impact_report(
        self,
        project_id: int,
        output_path: Optional[str] = None,
        include_charts: bool = True,
        language: ReportLanguage = ReportLanguage.ENGLISH
    ) -> Union[str, bytes]:
        """Generate impact assessment report."""
        logger.info(f"Generating impact report for project {project_id}")
        
        config = ReportConfig(
            report_type=ReportType.IMPACT,
            language=language,
            charts=include_charts,
            include_sections=[
                "project_overview",
                "methodology",
                "impact_assessment",
                "risk_assessment",
                "mitigation_measures",
                "conclusions"
            ]
        )
        
        return self.report_service.generate_report(project_id, config, output_path)
    
    def generate_compliance_report(
        self,
        project_id: int,
        output_path: Optional[str] = None,
        language: ReportLanguage = ReportLanguage.ENGLISH
    ) -> Union[str, bytes]:
        """Generate compliance report."""
        logger.info(f"Generating compliance report for project {project_id}")
        
        config = ReportConfig(
            report_type=ReportType.COMPLIANCE,
            language=language,
            include_sections=[
                "project_overview",
                "compliance_summary",
                "detailed_checks",
                "non_compliance_items",
                "action_plan"
            ]
        )
        
        return self.report_service.generate_report(project_id, config, output_path)
    
    def generate_monitoring_report(
        self,
        project_id: int,
        start_date: datetime,
        end_date: datetime,
        output_path: Optional[str] = None,
        include_charts: bool = True,
        language: ReportLanguage = ReportLanguage.ENGLISH
    ) -> Union[str, bytes]:
        """Generate monitoring report for date range."""
        logger.info(f"Generating monitoring report for project {project_id}")
        
        config = ReportConfig(
            report_type=ReportType.MONITORING,
            language=language,
            charts=include_charts,
            date_range={'start': start_date, 'end': end_date},
            include_sections=[
                "project_overview",
                "monitoring_summary",
                "parameter_analysis",
                "trends",
                "exceedances",
                "recommendations"
            ]
        )
        
        return self.report_service.generate_report(project_id, config, output_path)
    
    def generate_comprehensive_report(
        self,
        project_id: int,
        output_path: Optional[str] = None,
        include_all_data: bool = True,
        language: ReportLanguage = ReportLanguage.ENGLISH
    ) -> Union[str, bytes]:
        """Generate comprehensive report with all assessments."""
        logger.info(f"Generating comprehensive report for project {project_id}")
        
        sections = [
            "executive_summary",
            "project_overview",
            "screening_results",
            "impact_assessment",
            "risk_assessment",
            "compliance_status",
            "monitoring_data",
            "mitigation_measures",
            "conclusions",
            "recommendations"
        ]
        
        if include_all_data:
            sections.append("appendices")
        
        config = ReportConfig(
            report_type=ReportType.COMPREHENSIVE,
            language=language,
            charts=True,
            include_sections=sections
        )
        
        return self.report_service.generate_report(project_id, config, output_path)
    
    def generate_executive_summary(
        self,
        project_id: int,
        output_path: Optional[str] = None,
        language: ReportLanguage = ReportLanguage.ENGLISH
    ) -> Union[str, bytes]:
        """Generate executive summary report (1-2 pages)."""
        logger.info(f"Generating executive summary for project {project_id}")
        
        config = ReportConfig(
            report_type=ReportType.EXECUTIVE_SUMMARY,
            language=language,
            charts=False,
            table_of_contents=False,
            appendices=False,
            include_sections=[
                "key_findings",
                "compliance_status",
                "major_risks",
                "recommended_actions",
                "timeline"
            ]
        )
        
        return self.report_service.generate_report(project_id, config, output_path)
    
    def generate_custom_report(
        self,
        project_id: int,
        report_type: ReportType,
        sections: List[str],
        output_path: Optional[str] = None,
        **kwargs
    ) -> Union[str, bytes]:
        """Generate custom report with specified sections."""
        logger.info(f"Generating custom {report_type.value} report for project {project_id}")
        
        config = ReportConfig(
            report_type=report_type,
            include_sections=sections,
            **kwargs
        )
        
        return self.report_service.generate_report(project_id, config, output_path)
    
    def generate_batch_reports(
        self,
        project_ids: List[int],
        report_type: ReportType,
        output_dir: str,
        language: ReportLanguage = ReportLanguage.ENGLISH
    ) -> List[str]:
        """Generate reports for multiple projects."""
        logger.info(f"Generating {report_type.value} reports for {len(project_ids)} projects")
        
        config = ReportConfig(
            report_type=report_type,
            language=language
        )
        
        return self.report_service.generate_batch_reports(
            project_ids,
            config,
            output_dir
        )
    
    def get_report_data(self, project_id: int) -> Dict[str, Any]:
        """
        Get all report data for a project.
        Useful for custom report generation or data export.
        """
        project = self.db.query(Project).filter_by(id=project_id).first()
        if not project:
            raise ValueError(f"Project {project_id} not found")
        
        # Get latest assessment
        assessment = self.db.query(Assessment).filter_by(
            project_id=project_id
        ).order_by(Assessment.assessment_date.desc()).first()
        
        # Get latest impact
        impact = self.db.query(ImpactRecord).filter_by(
            project_id=project_id
        ).order_by(ImpactRecord.assessment_date.desc()).first()
        
        # Get compliance data
        compliance_records = self.db.query(ComplianceRecord).filter_by(
            project_id=project_id
        ).all()
        
        # Calculate compliance summary
        compliance_summary = self._calculate_compliance_summary(compliance_records)
        
        # Get monitoring summary (last 30 days)
        monitoring_summary = self._get_monitoring_summary(project_id)
        
        return {
            'project': {
                'id': project.id,
                'name': project.name,
                'project_type': project.project_type,
                'location': project.location,
                'status': project.status,
                'client_name': project.client_name,
                'size': project.size,
                'duration': project.duration,
                'budget': project.budget
            },
            'assessment': {
                'eia_required': assessment.eia_required,
                'eia_level': assessment.eia_level,
                'key_concerns': assessment.key_concerns,
                'regulatory_requirements': assessment.regulatory_requirements,
                'specialist_studies': assessment.specialist_studies,
                'assessment_type': assessment.assessment_type,
                'estimated_duration': assessment.estimated_duration
            } if assessment else None,
            'impact': {
                'carbon_footprint': impact.carbon_footprint,
                'water_consumption': impact.water_consumption,
                'waste_generation': impact.waste_generation,
                'energy_usage': impact.energy_usage,
                'biodiversity_score': impact.biodiversity_score,
                'pm10_concentration': impact.pm10_concentration,
                'pm25_concentration': impact.pm25_concentration,
                'impact_severity': impact.impact_severity
            } if impact else None,
            'compliance_summary': compliance_summary,
            'monitoring_summary': monitoring_summary
        }
    
    def _calculate_compliance_summary(
        self, 
        records: List[ComplianceRecord]
    ) -> Dict[str, Any]:
        """Calculate compliance summary statistics."""
        if not records:
            return {
                'total_checks': 0,
                'compliant_checks': 0,
                'compliance_rate': 100.0,
                'critical_violations': 0
            }
        
        total = len(records)
        compliant = sum(1 for r in records if r.status == "Compliant")
        critical = sum(1 for r in records 
                      if r.status != "Compliant" and r.deviation and r.deviation > 50)
        
        return {
            'total_checks': total,
            'compliant_checks': compliant,
            'compliance_rate': (compliant / total * 100) if total > 0 else 100,
            'critical_violations': critical,
            'non_compliant_items': [
                {
                    'regulation_id': r.regulation_id,
                    'regulation_name': r.regulation_name,
                    'category': r.category,
                    'actual_value': r.actual_value,
                    'required_value': r.required_value,
                    'deviation': r.deviation,
                    'recommendation': r.recommendation
                }
                for r in records if r.status != "Compliant"
            ][:10]  # Top 10 non-compliant items
        }
    
    def _get_monitoring_summary(self, project_id: int) -> Dict[str, Any]:
        """Get monitoring summary for last 30 days."""
        from src.services import MonitoringService
        
        monitoring_service = MonitoringService(self.db)
        end_date = datetime.now()
        start_date = end_date.replace(day=1)  # Current month
        
        try:
            report = monitoring_service.generate_monitoring_report(
                project_id, start_date, end_date
            )
            
            # Extract summary
            total_exceedances = sum(
                param_data.get('exceedances', 0)
                for param_data in report.get('parameters', {}).values()
            )
            
            return {
                'period': report.get('period', {}),
                'parameters': report.get('parameters', {}),
                'total_exceedances': total_exceedances,
                'monitoring_points': report.get('overall', {}).get('monitoring_points', 0)
            }
        except Exception as e:
            logger.error(f"Failed to get monitoring summary: {e}")
            return {
                'period': {'start': start_date, 'end': end_date},
                'parameters': {},
                'total_exceedances': 0,
                'monitoring_points': 0
            }
    
    def preview_report(
        self,
        project_id: int,
        report_type: ReportType,
        max_pages: int = 3
    ) -> str:
        """
        Generate a preview of the report (first few pages).
        Returns base64 encoded PDF.
        """
        import base64
        
        config = ReportConfig(
            report_type=report_type,
            table_of_contents=False,
            appendices=False,
            recommendations=False
        )
        
        # Generate full report in memory
        pdf_bytes = self.report_service.generate_report(project_id, config)
        
        # For preview, we'll return the full report but could implement
        # page limiting in the future
        return base64.b64encode(pdf_bytes).decode('utf-8')
    
    def get_available_sections(self, report_type: ReportType) -> List[str]:
        """Get available sections for a report type."""
        all_sections = {
            ReportType.SCREENING: [
                "project_overview", "screening_results", "regulatory_requirements",
                "specialist_studies", "recommendations"
            ],
            ReportType.IMPACT: [
                "project_overview", "methodology", "impact_assessment",
                "risk_assessment", "mitigation_measures", "biodiversity_impact",
                "air_quality", "noise_assessment", "water_resources",
                "waste_management", "conclusions"
            ],
            ReportType.COMPLIANCE: [
                "project_overview", "compliance_summary", "detailed_checks",
                "non_compliance_items", "compliance_by_category",
                "regulatory_framework", "action_plan", "compliance_history"
            ],
            ReportType.MONITORING: [
                "project_overview", "monitoring_summary", "parameter_analysis",
                "trends", "exceedances", "alerts", "monitoring_locations",
                "equipment_calibration", "qaqc_results", "recommendations"
            ],
            ReportType.COMPREHENSIVE: [
                "executive_summary", "project_overview", "screening_results",
                "impact_assessment", "risk_assessment", "compliance_status",
                "monitoring_data", "mitigation_measures", "biodiversity_analysis",
                "social_impact", "economic_analysis", "cumulative_impacts",
                "alternatives_analysis", "stakeholder_feedback", "conclusions",
                "recommendations", "appendices"
            ],
            ReportType.EXECUTIVE_SUMMARY: [
                "key_findings", "compliance_status", "major_risks",
                "critical_issues", "recommended_actions", "timeline",
                "budget_implications", "stakeholder_summary"
            ]
        }
        
        return all_sections.get(report_type, [])