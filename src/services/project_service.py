"""
Project Service
Business logic for project management

Author: Edy Bassil
Email: bassileddy@gmail.com
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
import logging

from src.services.base_service import BaseService, ValidationError, ServiceException
from src.models import (
    Project, ProjectStatus, Assessment, ImpactRecord, 
    ComplianceRecord, MitigationMeasure, MonitoringData
)
from src.assessment import EIAScreening
from src.analysis import ConstructionImpact
from src.compliance import RegulatoryCompliance, Jurisdiction
from src.impact_calculator import ImpactCalculator
from src.risk_matrix import RiskMatrix
from src.config import get_config

logger = logging.getLogger(__name__)
config = get_config()


class ProjectService(BaseService[Project]):
    """
    Service for project management with business logic.
    Handles project lifecycle, assessments, and reporting.
    """
    
    def __init__(self, session: Session):
        super().__init__(Project, session)
        self.eia_screening = None
        self.impact_calculator = ImpactCalculator()
        self.risk_matrix = RiskMatrix()
        self.compliance_checker = RegulatoryCompliance()
    
    def _validate_create_data(self, data: Dict[str, Any]) -> None:
        """Validate project creation data."""
        required_fields = ['name', 'project_type', 'location']
        
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValidationError(f"{field} is required", field)
        
        # Validate project type
        valid_types = ['residential', 'commercial', 'industrial', 'infrastructure', 'mixed_use']
        if data['project_type'] not in valid_types:
            raise ValidationError(f"Invalid project type. Must be one of: {valid_types}", 'project_type')
        
        # Validate location
        valid_locations = ['Dubai', 'Abu Dhabi', 'Sharjah', 'Riyadh', 'Jeddah', 'NEOM']
        if data['location'] not in valid_locations:
            raise ValidationError(f"Invalid location. Must be one of: {valid_locations}", 'location')
        
        # Validate numeric fields
        numeric_fields = ['size', 'duration', 'budget', 'num_workers', 'water_usage']
        for field in numeric_fields:
            if field in data and data[field] is not None:
                if not isinstance(data[field], (int, float)) or data[field] < 0:
                    raise ValidationError(f"{field} must be a positive number", field)
        
        # Validate coordinates if provided
        if 'latitude' in data and 'longitude' in data:
            lat, lon = data.get('latitude'), data.get('longitude')
            if lat is not None and lon is not None:
                if not (-90 <= lat <= 90):
                    raise ValidationError("Latitude must be between -90 and 90", 'latitude')
                if not (-180 <= lon <= 180):
                    raise ValidationError("Longitude must be between -180 and 180", 'longitude')
    
    def _validate_update_data(self, data: Dict[str, Any], entity: Project) -> None:
        """Validate project update data."""
        # Can't change project type after creation
        if 'project_type' in data and data['project_type'] != entity.project_type:
            raise ValidationError("Project type cannot be changed after creation", 'project_type')
        
        # Validate status transitions
        if 'status' in data:
            current_status = entity.status
            new_status = data['status']
            
            # Define valid transitions
            valid_transitions = {
                ProjectStatus.PLANNING: [ProjectStatus.SCREENING],
                ProjectStatus.SCREENING: [ProjectStatus.ASSESSMENT, ProjectStatus.PLANNING],
                ProjectStatus.ASSESSMENT: [ProjectStatus.CONSTRUCTION, ProjectStatus.SCREENING],
                ProjectStatus.CONSTRUCTION: [ProjectStatus.OPERATION],
                ProjectStatus.OPERATION: [ProjectStatus.COMPLETED],
                ProjectStatus.COMPLETED: []
            }
            
            if new_status not in valid_transitions.get(current_status, []):
                raise ValidationError(
                    f"Invalid status transition from {current_status.value} to {new_status.value}",
                    'status'
                )
        
        # Run same validations as create for other fields
        if data:
            self._validate_create_data({**entity.__dict__, **data})
    
    def create_project_with_screening(self, project_data: Dict[str, Any]) -> Tuple[Project, Assessment]:
        """
        Create project and perform initial screening.
        
        Args:
            project_data: Project data including screening parameters
            
        Returns:
            Tuple of (Project, Assessment)
        """
        try:
            # Create project
            project = self.create(project_data)
            
            # Perform screening
            screening = EIAScreening(project.project_type, project.location)
            
            screening_data = {
                "project_size": project.size or 0,
                "duration": project.duration or 0,
                "sensitive_receptors": project_data.get("sensitive_receptors", []),
                "water_usage": project.water_usage or 0,
                "near_protected_area": project_data.get("near_protected_area", False)
            }
            
            result = screening.assess(screening_data)
            
            # Create assessment record
            assessment = Assessment(
                project_id=project.id,
                assessment_type="SCREENING",
                eia_required=result.eia_required,
                eia_level=result.eia_level,
                key_concerns=result.key_concerns,
                regulatory_requirements=result.regulatory_requirements,
                specialist_studies=result.specialist_studies,
                estimated_duration=result.estimated_duration,
                assessor_name=project_data.get("assessor_name", "System"),
                assessor_organization=project_data.get("assessor_organization", "EIA Tool"),
                status="Completed"
            )
            
            self.session.add(assessment)
            
            # Update project status
            project.status = ProjectStatus.SCREENING
            
            self.session.commit()
            
            logger.info(f"Created project {project.id} with screening assessment")
            return project, assessment
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to create project with screening: {e}")
            raise ServiceException(f"Failed to create project: {str(e)}")
    
    def perform_impact_assessment(self, project_id: int, impact_data: Dict[str, Any]) -> ImpactRecord:
        """
        Perform comprehensive impact assessment for project.
        
        Args:
            project_id: Project ID
            impact_data: Impact calculation data
            
        Returns:
            ImpactRecord with calculated impacts
        """
        project = self.get_by_id(project_id)
        
        # Prepare data for impact calculator
        calc_data = {
            'materials': impact_data.get('materials', {}),
            'equipment_hours': impact_data.get('equipment_hours', {}),
            'transport_km': impact_data.get('transport_km', 0),
            'concrete_volume': impact_data.get('concrete_volume', 0),
            'construction_area': project.construction_area or impact_data.get('construction_area', 0),
            'duration_days': (project.duration or 12) * 30,  # Convert months to days
            'num_workers': project.num_workers or impact_data.get('num_workers', 50),
            'facility_area': impact_data.get('facility_area', 500),
            'area_cleared': impact_data.get('area_cleared', project.size or 0),
            'habitat_type': impact_data.get('habitat_type', 'urban'),
            'mitigation_measures': impact_data.get('mitigation_measures', [])
        }
        
        # Calculate impacts
        metrics = self.impact_calculator.calculate_comprehensive_impact(calc_data)
        
        # Create impact record
        impact_record = ImpactRecord(
            project_id=project_id,
            carbon_footprint=metrics.carbon_footprint,
            water_consumption=metrics.water_consumption,
            waste_generation=metrics.waste_generation,
            energy_usage=metrics.energy_usage,
            biodiversity_score=metrics.biodiversity_score,
            area_cleared=metrics.land_disturbance,
            habitat_type=calc_data['habitat_type']
        )
        
        # Add construction-specific impacts if provided
        if 'noise_assessment' in impact_data:
            noise_data = impact_data['noise_assessment']
            impact_record.peak_noise_level = noise_data.get('peak_level')
            impact_record.average_noise_level = noise_data.get('average_level')
            impact_record.nearest_receptor_distance = noise_data.get('receptor_distance')
        
        if 'dust_assessment' in impact_data:
            dust_data = impact_data['dust_assessment']
            impact_record.pm10_concentration = dust_data.get('pm10')
            impact_record.pm25_concentration = dust_data.get('pm25')
        
        # Determine overall severity
        severity_counts = {'low': 0, 'medium': 0, 'high': 0}
        
        for impact_type, value in [
            ('carbon', metrics.carbon_footprint),
            ('water', metrics.water_consumption),
            ('waste', metrics.waste_generation),
            ('energy', metrics.energy_usage)
        ]:
            severity = self.impact_calculator._assess_severity(value, impact_type)
            severity_counts[severity] += 1
        
        if severity_counts['high'] >= 2:
            impact_record.impact_severity = 'High'
        elif severity_counts['medium'] >= 2:
            impact_record.impact_severity = 'Medium'
        else:
            impact_record.impact_severity = 'Low'
        
        self.session.add(impact_record)
        
        # Update project status if needed
        if project.status == ProjectStatus.SCREENING:
            project.status = ProjectStatus.ASSESSMENT
        
        self.session.commit()
        
        logger.info(f"Completed impact assessment for project {project_id}")
        return impact_record
    
    def check_compliance(self, project_id: int, compliance_data: Dict[str, Any] = None) -> List[ComplianceRecord]:
        """
        Check regulatory compliance for project.
        
        Args:
            project_id: Project ID
            compliance_data: Additional compliance data
            
        Returns:
            List of compliance records
        """
        project = self.get_by_id(project_id)
        
        # Get latest impact data
        latest_impact = self.session.query(ImpactRecord).filter_by(
            project_id=project_id
        ).order_by(ImpactRecord.assessment_date.desc()).first()
        
        if not latest_impact and not compliance_data:
            raise ServiceException("No impact data available for compliance check")
        
        # Determine jurisdiction
        jurisdiction_map = {
            'Dubai': Jurisdiction.DUBAI,
            'Abu Dhabi': Jurisdiction.ABU_DHABI,
            'Sharjah': Jurisdiction.SHARJAH,
            'Riyadh': Jurisdiction.KSA_NATIONAL,
            'Jeddah': Jurisdiction.KSA_NATIONAL,
            'NEOM': Jurisdiction.NEOM
        }
        
        jurisdiction = jurisdiction_map.get(project.location, Jurisdiction.UAE_FEDERAL)
        
        # Prepare compliance data
        check_data = {
            'project_name': project.name,
            'pm10_concentration': latest_impact.pm10_concentration if latest_impact else compliance_data.get('pm10', 0),
            'pm25_concentration': latest_impact.pm25_concentration if latest_impact else compliance_data.get('pm25', 0),
            'noise_level': latest_impact.average_noise_level if latest_impact else compliance_data.get('noise', 0),
            'water_consumption': latest_impact.water_consumption if latest_impact else compliance_data.get('water', 0),
            'eia_completed': bool(project.assessments),
            'waste_management_plan': compliance_data.get('waste_plan', False),
            'waste_segregation': compliance_data.get('waste_segregation', False),
            'water_conservation_plan': compliance_data.get('water_plan', False)
        }
        
        # Perform compliance check
        report = self.compliance_checker.check_compliance(check_data, jurisdiction)
        
        # Create compliance records
        compliance_records = []
        for check in report.checks:
            record = ComplianceRecord(
                project_id=project_id,
                jurisdiction=jurisdiction.value,
                regulation_id=check.regulation_id,
                regulation_name=check.regulation_name,
                category=check.regulation_name.split(' - ')[0] if ' - ' in check.regulation_name else 'General',
                status=check.status.value,
                actual_value=check.actual_value,
                required_value=check.required_value,
                deviation=check.deviation,
                recommendation=check.recommendation,
                evidence_required=check.evidence_required
            )
            
            compliance_records.append(record)
            self.session.add(record)
        
        self.session.commit()
        
        logger.info(f"Completed compliance check for project {project_id}: {report.compliance_percentage:.1f}% compliant")
        return compliance_records
    
    def get_project_dashboard(self, project_id: int) -> Dict[str, Any]:
        """
        Get comprehensive project dashboard data.
        
        Args:
            project_id: Project ID
            
        Returns:
            Dictionary with project metrics and status
        """
        project = self.get_by_id(project_id)
        
        # Get latest assessment
        latest_assessment = self.session.query(Assessment).filter_by(
            project_id=project_id
        ).order_by(Assessment.assessment_date.desc()).first()
        
        # Get latest impact
        latest_impact = self.session.query(ImpactRecord).filter_by(
            project_id=project_id
        ).order_by(ImpactRecord.assessment_date.desc()).first()
        
        # Get compliance summary
        compliance_records = self.session.query(ComplianceRecord).filter_by(
            project_id=project_id
        ).order_by(ComplianceRecord.check_date.desc()).limit(20).all()
        
        compliant_count = sum(1 for r in compliance_records if r.status == "Compliant")
        compliance_percentage = (compliant_count / len(compliance_records) * 100) if compliance_records else 0
        
        # Get active mitigation measures
        active_mitigations = self.session.query(MitigationMeasure).filter(
            and_(
                MitigationMeasure.project_id == project_id,
                MitigationMeasure.status.in_(["Planned", "In Progress"])
            )
        ).count()
        
        # Get recent monitoring data
        recent_monitoring = self.session.query(
            MonitoringData.parameter,
            func.avg(MonitoringData.value).label('avg_value'),
            func.max(MonitoringData.value).label('max_value'),
            func.count(MonitoringData.id).label('count')
        ).filter(
            and_(
                MonitoringData.project_id == project_id,
                MonitoringData.measurement_date >= datetime.utcnow() - timedelta(days=30)
            )
        ).group_by(MonitoringData.parameter).all()
        
        dashboard = {
            'project': {
                'id': project.id,
                'name': project.name,
                'type': project.project_type,
                'location': project.location,
                'status': project.status.value,
                'size': project.size,
                'duration': project.duration,
                'progress': self._calculate_progress(project)
            },
            'assessment': {
                'eia_required': latest_assessment.eia_required if latest_assessment else None,
                'eia_level': latest_assessment.eia_level if latest_assessment else None,
                'key_concerns': latest_assessment.key_concerns if latest_assessment else []
            },
            'impacts': {
                'carbon_footprint': latest_impact.carbon_footprint if latest_impact else None,
                'water_consumption': latest_impact.water_consumption if latest_impact else None,
                'biodiversity_score': latest_impact.biodiversity_score if latest_impact else None,
                'overall_severity': latest_impact.impact_severity if latest_impact else None
            },
            'compliance': {
                'percentage': compliance_percentage,
                'total_checks': len(compliance_records),
                'non_compliant': len(compliance_records) - compliant_count,
                'last_check': compliance_records[0].check_date.isoformat() if compliance_records else None
            },
            'mitigation': {
                'active_measures': active_mitigations,
                'categories': self._get_mitigation_categories(project_id)
            },
            'monitoring': {
                'parameters': [
                    {
                        'name': m.parameter,
                        'average': float(m.avg_value),
                        'maximum': float(m.max_value),
                        'readings': m.count
                    }
                    for m in recent_monitoring
                ]
            }
        }
        
        return dashboard
    
    def _calculate_progress(self, project: Project) -> float:
        """Calculate project progress percentage."""
        if project.status == ProjectStatus.COMPLETED:
            return 100.0
        elif project.status == ProjectStatus.OPERATION:
            return 90.0
        elif project.status == ProjectStatus.CONSTRUCTION:
            if project.created_at and project.duration:
                elapsed = (datetime.utcnow() - project.created_at).days / 30  # months
                return min(80.0, 50.0 + (elapsed / project.duration) * 30)
            return 60.0
        elif project.status == ProjectStatus.ASSESSMENT:
            return 30.0
        elif project.status == ProjectStatus.SCREENING:
            return 15.0
        else:  # PLANNING
            return 5.0
    
    def _get_mitigation_categories(self, project_id: int) -> List[Dict[str, Any]]:
        """Get mitigation measures by category."""
        measures = self.session.query(
            MitigationMeasure.impact_category,
            func.count(MitigationMeasure.id).label('count'),
            func.sum(func.cast(MitigationMeasure.status == 'Implemented', Integer)).label('implemented')
        ).filter_by(
            project_id=project_id
        ).group_by(MitigationMeasure.impact_category).all()
        
        return [
            {
                'category': m.impact_category,
                'total': m.count,
                'implemented': m.implemented or 0
            }
            for m in measures
        ]
    
    def search_projects(self, 
                       query: str = None,
                       status: ProjectStatus = None,
                       location: str = None,
                       project_type: str = None,
                       date_from: datetime = None,
                       date_to: datetime = None,
                       limit: int = 50,
                       offset: int = 0) -> List[Project]:
        """
        Search projects with various filters.
        
        Args:
            query: Text search in name and description
            status: Project status filter
            location: Location filter
            project_type: Project type filter
            date_from: Created after date
            date_to: Created before date
            limit: Maximum results
            offset: Results offset
            
        Returns:
            List of matching projects
        """
        search_query = self.session.query(Project)
        
        if query:
            search_query = search_query.filter(
                or_(
                    Project.name.ilike(f'%{query}%'),
                    Project.description.ilike(f'%{query}%'),
                    Project.client_name.ilike(f'%{query}%')
                )
            )
        
        if status:
            search_query = search_query.filter(Project.status == status)
        
        if location:
            search_query = search_query.filter(Project.location == location)
        
        if project_type:
            search_query = search_query.filter(Project.project_type == project_type)
        
        if date_from:
            search_query = search_query.filter(Project.created_at >= date_from)
        
        if date_to:
            search_query = search_query.filter(Project.created_at <= date_to)
        
        # Order by creation date descending
        search_query = search_query.order_by(Project.created_at.desc())
        
        # Apply pagination
        if offset:
            search_query = search_query.offset(offset)
        if limit:
            search_query = search_query.limit(limit)
        
        return search_query.all()