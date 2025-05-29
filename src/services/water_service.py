"""
Water Resources Service
Business logic for water impact assessment and management

Author: Edy Bassil
Email: bassileddy@gmail.com
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.services import BaseService, ValidationError, NotFoundError
from src.models import Project, ImpactRecord, WaterAssessment, get_session
from src.analysis import (
    WaterResourcesAnalyzer,
    WaterConsumption,
    WaterQualityImpact,
    WaterBalance,
    WaterRiskAssessment
)

logger = logging.getLogger(__name__)


class WaterService(BaseService):
    """Service for water resources management."""
    
    def __init__(self, db: Session):
        super().__init__(db, Project)
        self.analyzer = WaterResourcesAnalyzer()
    
    def assess_water_impact(
        self,
        project_id: int,
        activities: Dict[str, float],
        water_sources: Optional[Dict[str, float]] = None,
        baseline_quality: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Perform comprehensive water impact assessment.
        
        Args:
            project_id: Project ID
            activities: Activity quantities
            water_sources: Water source breakdown
            baseline_quality: Baseline water quality data
            
        Returns:
            Water assessment results
        """
        try:
            # Get project
            project = self.get_by_id(project_id)
            if not project:
                raise NotFoundError(f"Project {project_id} not found")
            
            # Validate inputs
            if not activities:
                raise ValidationError("Activities data is required")
            
            # Calculate water consumption
            consumption = self.analyzer.calculate_water_consumption(
                project_type=project.project_type,
                project_size=project.size or 10000,
                duration_months=project.duration or 12,
                num_workers=project.num_workers or 100,
                activities=activities,
                water_sources=water_sources
            )
            
            # Calculate water balance
            # For UAE/KSA, assume limited water availability
            available_water = self._estimate_available_water(
                project.location,
                consumption.daily_average
            )
            
            balance = self.analyzer.calculate_water_balance(
                consumption=consumption,
                available_water=available_water,
                recycling_rate=0.3,
                evaporation_rate=0.08  # High evaporation in desert
            )
            
            # Assess water quality impacts if baseline provided
            quality_impacts = []
            if baseline_quality:
                quality_impacts = self.analyzer.assess_water_quality_impact(
                    baseline_quality=baseline_quality,
                    project_activities=list(activities.keys()),
                    discharge_volume=balance.discharge_volume,
                    receiving_water_volume=1000000  # Assume large water body
                )
            
            # Risk assessment
            risks = self.analyzer.assess_water_risks(
                location=project.location,
                water_balance=balance,
                quality_impacts=quality_impacts,
                project_duration_months=project.duration or 12
            )
            
            # Conservation recommendations
            conservation_measures = self.analyzer.recommend_conservation_measures(
                consumption=consumption,
                water_balance=balance,
                budget_constraint=project.budget * 0.02 if project.budget else None  # 2% of budget
            )
            
            # Save assessment to database
            assessment = self._save_water_assessment(
                project_id=project_id,
                consumption=consumption,
                balance=balance,
                risks=risks,
                quality_impacts=quality_impacts
            )
            
            # Generate management plan
            management_plan = self.analyzer.generate_water_management_plan(
                project_data={
                    'name': project.name,
                    'location': project.location,
                    'project_type': project.project_type,
                    'duration': project.duration
                },
                consumption=consumption,
                balance=balance,
                risks=risks,
                conservation_measures=conservation_measures
            )
            
            return {
                'assessment_id': assessment.id,
                'consumption': {
                    'daily_average': consumption.daily_average,
                    'peak_demand': consumption.peak_demand,
                    'total_project': consumption.total_project,
                    'per_worker': consumption.per_worker,
                    'per_area': consumption.per_area,
                    'by_activity': consumption.by_activity,
                    'by_source': consumption.by_source
                },
                'balance': {
                    'total_demand': balance.total_demand,
                    'available_supply': balance.available_supply,
                    'deficit_surplus': balance.deficit_surplus,
                    'recycled_water': balance.recycled_water,
                    'conservation_potential': balance.conservation_potential
                },
                'risks': {
                    'water_scarcity': risks.water_scarcity_risk,
                    'supply_reliability': risks.supply_reliability_risk,
                    'quality_degradation': risks.quality_degradation_risk,
                    'regulatory_compliance': risks.regulatory_compliance_risk,
                    'overall_risk': risks.overall_risk_level,
                    'priorities': risks.mitigation_priority
                },
                'quality_impacts': [
                    {
                        'parameter': impact.parameter,
                        'baseline': impact.baseline_value,
                        'predicted': impact.predicted_value,
                        'impact_level': impact.impact_level,
                        'exceeds_standard': impact.exceeds_standard
                    }
                    for impact in quality_impacts
                ],
                'conservation_measures': conservation_measures[:5],  # Top 5
                'management_plan': management_plan
            }
            
        except Exception as e:
            logger.error(f"Water impact assessment failed: {e}")
            raise
    
    def get_water_assessment_history(
        self,
        project_id: int,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get water assessment history for project.
        
        Args:
            project_id: Project ID
            limit: Maximum number of assessments
            
        Returns:
            List of water assessments
        """
        assessments = self.db.query(WaterAssessment).filter_by(
            project_id=project_id
        ).order_by(
            WaterAssessment.assessment_date.desc()
        ).limit(limit).all()
        
        return [
            {
                'id': a.id,
                'assessment_date': a.assessment_date.isoformat(),
                'daily_consumption': a.daily_consumption,
                'total_consumption': a.total_consumption,
                'water_balance': a.water_balance,
                'scarcity_risk': a.scarcity_risk,
                'quality_risk': a.quality_risk,
                'overall_risk': a.overall_risk
            }
            for a in assessments
        ]
    
    def update_water_monitoring(
        self,
        project_id: int,
        actual_consumption: float,
        date: datetime,
        quality_data: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Update water monitoring data.
        
        Args:
            project_id: Project ID
            actual_consumption: Actual daily consumption (m³)
            date: Monitoring date
            quality_data: Water quality measurements
            
        Returns:
            Monitoring update result
        """
        # Get latest assessment
        assessment = self.db.query(WaterAssessment).filter_by(
            project_id=project_id
        ).order_by(
            WaterAssessment.assessment_date.desc()
        ).first()
        
        if not assessment:
            raise NotFoundError("No water assessment found for project")
        
        # Compare with planned consumption
        variance = actual_consumption - assessment.daily_consumption
        variance_percentage = (variance / assessment.daily_consumption * 100) if assessment.daily_consumption > 0 else 0
        
        # Check if action needed
        alerts = []
        if variance_percentage > 20:
            alerts.append({
                'type': 'consumption_exceeded',
                'severity': 'high',
                'message': f'Water consumption {variance_percentage:.1f}% above planned'
            })
        
        # Check quality parameters if provided
        if quality_data:
            for param, value in quality_data.items():
                standard = self.analyzer._get_water_quality_standard(param, 'discharge')
                if standard and value > standard:
                    alerts.append({
                        'type': 'quality_exceedance',
                        'severity': 'medium',
                        'message': f'{param} exceeds standard: {value} > {standard}'
                    })
        
        # Update tracking in database (would need MonitoringData model)
        # For now, return the analysis
        
        return {
            'project_id': project_id,
            'date': date.isoformat(),
            'planned_consumption': assessment.daily_consumption,
            'actual_consumption': actual_consumption,
            'variance': variance,
            'variance_percentage': variance_percentage,
            'quality_data': quality_data,
            'alerts': alerts,
            'cumulative_consumption': self._calculate_cumulative_consumption(
                project_id, 
                date
            )
        }
    
    def generate_water_report(
        self,
        project_id: int,
        report_type: str = 'comprehensive',
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Generate water management report.
        
        Args:
            project_id: Project ID
            report_type: Type of report
            start_date: Report start date
            end_date: Report end date
            
        Returns:
            Water management report data
        """
        # Get project and latest assessment
        project = self.get_by_id(project_id)
        if not project:
            raise NotFoundError(f"Project {project_id} not found")
        
        assessment = self.db.query(WaterAssessment).filter_by(
            project_id=project_id
        ).order_by(
            WaterAssessment.assessment_date.desc()
        ).first()
        
        if not assessment:
            raise NotFoundError("No water assessment found")
        
        # Generate report based on type
        if report_type == 'summary':
            return self._generate_summary_report(project, assessment)
        elif report_type == 'compliance':
            return self._generate_compliance_report(project, assessment)
        elif report_type == 'conservation':
            return self._generate_conservation_report(project, assessment)
        else:
            return self._generate_comprehensive_report(
                project, 
                assessment,
                start_date,
                end_date
            )
    
    def _estimate_available_water(
        self,
        location: str,
        demand: float
    ) -> Dict[str, float]:
        """Estimate available water sources."""
        # Regional water availability patterns
        water_availability = {
            'Dubai': {
                'municipal': 0.4,
                'tanker': 0.4,
                'groundwater': 0.1,
                'recycled': 0.1
            },
            'Abu Dhabi': {
                'municipal': 0.5,
                'tanker': 0.3,
                'groundwater': 0.1,
                'recycled': 0.1
            },
            'Riyadh': {
                'municipal': 0.3,
                'tanker': 0.5,
                'groundwater': 0.2,
                'recycled': 0.0
            }
        }
        
        # Get location pattern or use default
        pattern = water_availability.get(location, {
            'municipal': 0.4,
            'tanker': 0.4,
            'groundwater': 0.1,
            'recycled': 0.1
        })
        
        # Calculate available water with 20% safety margin
        total_available = demand * 1.2
        
        return {
            source: total_available * fraction
            for source, fraction in pattern.items()
        }
    
    def _save_water_assessment(
        self,
        project_id: int,
        consumption: WaterConsumption,
        balance: WaterBalance,
        risks: WaterRiskAssessment,
        quality_impacts: List[WaterQualityImpact]
    ) -> WaterAssessment:
        """Save water assessment to database."""
        assessment = WaterAssessment(
            project_id=project_id,
            assessment_date=datetime.now(),
            daily_consumption=consumption.daily_average,
            peak_consumption=consumption.peak_demand,
            total_consumption=consumption.total_project,
            consumption_by_activity=consumption.by_activity,
            consumption_by_source=consumption.by_source,
            water_balance=balance.deficit_surplus,
            recycled_water=balance.recycled_water,
            conservation_potential=balance.conservation_potential,
            scarcity_risk=risks.water_scarcity_risk,
            quality_risk=risks.quality_degradation_risk,
            compliance_risk=risks.regulatory_compliance_risk,
            overall_risk=risks.overall_risk_level,
            mitigation_priorities=risks.mitigation_priority,
            quality_impacts=[
                {
                    'parameter': i.parameter,
                    'baseline': i.baseline_value,
                    'predicted': i.predicted_value,
                    'impact': i.impact_level
                }
                for i in quality_impacts
            ]
        )
        
        self.db.add(assessment)
        self.db.commit()
        self.db.refresh(assessment)
        
        # Update project impact record if exists
        impact_record = self.db.query(ImpactRecord).filter_by(
            project_id=project_id
        ).order_by(ImpactRecord.assessment_date.desc()).first()
        
        if impact_record:
            impact_record.water_consumption = consumption.total_project
            self.db.commit()
        
        return assessment
    
    def _calculate_cumulative_consumption(
        self,
        project_id: int,
        up_to_date: datetime
    ) -> float:
        """Calculate cumulative water consumption."""
        # This would query actual monitoring data
        # For now, estimate based on assessment
        assessment = self.db.query(WaterAssessment).filter_by(
            project_id=project_id
        ).order_by(
            WaterAssessment.assessment_date.desc()
        ).first()
        
        if not assessment:
            return 0
        
        # Calculate days elapsed
        project = self.get_by_id(project_id)
        start_date = project.created_at
        days_elapsed = (up_to_date - start_date).days
        
        return assessment.daily_consumption * days_elapsed
    
    def _generate_summary_report(
        self,
        project: Project,
        assessment: WaterAssessment
    ) -> Dict[str, Any]:
        """Generate summary water report."""
        return {
            'report_type': 'summary',
            'project': {
                'name': project.name,
                'location': project.location
            },
            'key_metrics': {
                'daily_consumption': assessment.daily_consumption,
                'total_consumption': assessment.total_consumption,
                'water_balance': assessment.water_balance,
                'recycling_rate': (assessment.recycled_water / assessment.daily_consumption * 100) if assessment.daily_consumption > 0 else 0
            },
            'risk_summary': {
                'scarcity': assessment.scarcity_risk,
                'quality': assessment.quality_risk,
                'compliance': assessment.compliance_risk,
                'overall': assessment.overall_risk
            },
            'top_priorities': assessment.mitigation_priorities[:3]
        }
    
    def _generate_compliance_report(
        self,
        project: Project,
        assessment: WaterAssessment
    ) -> Dict[str, Any]:
        """Generate water compliance report."""
        return {
            'report_type': 'compliance',
            'project': {
                'name': project.name,
                'location': project.location
            },
            'permits': {
                'water_abstraction': 'Required' if assessment.daily_consumption > 100 else 'Not Required',
                'discharge_permit': 'Required',
                'noc_status': 'Pending'
            },
            'consumption_limits': {
                'allocated': assessment.daily_consumption * 1.2,
                'actual': assessment.daily_consumption,
                'compliance': 'Within Limits'
            },
            'quality_compliance': {
                'parameters_monitored': len(assessment.quality_impacts) if assessment.quality_impacts else 0,
                'exceedances': sum(
                    1 for impact in (assessment.quality_impacts or [])
                    if impact.get('impact') == 'High'
                ),
                'compliance_status': assessment.compliance_risk
            },
            'reporting_requirements': [
                'Monthly consumption report',
                'Quarterly quality analysis',
                'Annual water audit'
            ]
        }
    
    def _generate_conservation_report(
        self,
        project: Project,
        assessment: WaterAssessment
    ) -> Dict[str, Any]:
        """Generate water conservation report."""
        return {
            'report_type': 'conservation',
            'project': {
                'name': project.name,
                'location': project.location
            },
            'current_performance': {
                'daily_consumption': assessment.daily_consumption,
                'recycling_rate': (assessment.recycled_water / assessment.daily_consumption * 100) if assessment.daily_consumption > 0 else 0,
                'conservation_achieved': 0  # Would track actual vs baseline
            },
            'conservation_potential': {
                'total_potential': assessment.conservation_potential,
                'percentage': (assessment.conservation_potential / assessment.daily_consumption * 100) if assessment.daily_consumption > 0 else 0
            },
            'implemented_measures': [],  # Would track from project data
            'recommended_actions': assessment.mitigation_priorities,
            'projected_savings': {
                'water_volume': assessment.conservation_potential * 365,
                'cost_savings': assessment.conservation_potential * 365 * 5  # $5/m³
            }
        }
    
    def _generate_comprehensive_report(
        self,
        project: Project,
        assessment: WaterAssessment,
        start_date: Optional[datetime],
        end_date: Optional[datetime]
    ) -> Dict[str, Any]:
        """Generate comprehensive water report."""
        # Combine all report types
        summary = self._generate_summary_report(project, assessment)
        compliance = self._generate_compliance_report(project, assessment)
        conservation = self._generate_conservation_report(project, assessment)
        
        return {
            'report_type': 'comprehensive',
            'report_period': {
                'start': start_date.isoformat() if start_date else assessment.assessment_date.isoformat(),
                'end': end_date.isoformat() if end_date else datetime.now().isoformat()
            },
            'executive_summary': summary['key_metrics'],
            'consumption_analysis': {
                'by_activity': assessment.consumption_by_activity,
                'by_source': assessment.consumption_by_source,
                'trends': []  # Would calculate from monitoring data
            },
            'water_balance': {
                'supply_demand': assessment.water_balance,
                'recycling': assessment.recycled_water,
                'losses': assessment.daily_consumption * 0.05  # Estimate
            },
            'risk_assessment': summary['risk_summary'],
            'compliance_status': compliance,
            'conservation_program': conservation,
            'recommendations': {
                'immediate': assessment.mitigation_priorities[:2],
                'short_term': assessment.mitigation_priorities[2:4],
                'long_term': assessment.mitigation_priorities[4:]
            }
        }