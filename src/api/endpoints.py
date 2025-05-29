"""
API Endpoints
Comprehensive REST API endpoints for EIA system

Author: Edy Bassil
Email: bassileddy@gmail.com
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Body, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
import logging

from src.services import (
    ProjectService, MonitoringService, AuthService, ReportService, WaterService,
    ValidationError, NotFoundError, UnauthorizedError,
    UserRole, Permission, ReportType, ReportLanguage
)
from src.models import (
    get_session, ProjectStatus, Assessment, ImpactRecord, 
    ComplianceRecord, MonitoringData
)
from src.api.schemas import *  # Will create this next

logger = logging.getLogger(__name__)

# Security
security = HTTPBearer()

# Routers
auth_router = APIRouter(prefix="/api/auth", tags=["Authentication"])
projects_router = APIRouter(prefix="/api/projects", tags=["Projects"])
monitoring_router = APIRouter(prefix="/api/monitoring", tags=["Monitoring"])
assessment_router = APIRouter(prefix="/api/assessments", tags=["Assessments"])
water_router = APIRouter(prefix="/api/water", tags=["Water Resources"])
compliance_router = APIRouter(prefix="/api/compliance", tags=["Compliance"])
reports_router = APIRouter(prefix="/api/reports", tags=["Reports"])


# Dependencies
def get_db():
    """Database session dependency."""
    db = get_session()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get current authenticated user."""
    token = credentials.credentials
    auth_service = AuthService(db)
    
    user = auth_service.get_current_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    return user


def require_permission(permission: Permission):
    """Decorator to require specific permission."""
    def permission_checker(
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        auth_service = AuthService(db)
        if not auth_service.check_permission(current_user, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied: {permission.value}"
            )
        return current_user
    return permission_checker


# Error handler
def handle_service_error(e: Exception):
    """Convert service exceptions to HTTP exceptions."""
    if isinstance(e, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
            headers={"X-Error-Field": e.field} if e.field else None
        )
    elif isinstance(e, NotFoundError):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    elif isinstance(e, UnauthorizedError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    else:
        logger.error(f"Unhandled service error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# ============= Authentication Endpoints =============

@auth_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    registration: UserRegistration,
    db: Session = Depends(get_db)
):
    """Register new user."""
    try:
        auth_service = AuthService(db)
        user = auth_service.register_user(
            username=registration.username,
            email=registration.email,
            password=registration.password,
            full_name=registration.full_name,
            organization=registration.organization,
            role=registration.role or UserRole.CLIENT.value
        )
        
        return UserResponse.from_orm(user)
    except Exception as e:
        handle_service_error(e)


@auth_router.post("/login", response_model=TokenResponse)
async def login(
    credentials: LoginCredentials,
    db: Session = Depends(get_db)
):
    """Login and get access token."""
    auth_service = AuthService(db)
    
    user = auth_service.authenticate(credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    token = auth_service.generate_token(user)
    
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        expires_in=auth_service.token_expiry.total_seconds(),
        user=UserResponse.from_orm(user)
    )


@auth_router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user=Depends(get_current_user)
):
    """Get current user information."""
    return UserResponse.from_orm(current_user)


@auth_router.post("/change-password")
async def change_password(
    password_change: PasswordChange,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change user password."""
    try:
        auth_service = AuthService(db)
        auth_service.change_password(
            current_user.id,
            password_change.old_password,
            password_change.new_password
        )
        return {"message": "Password changed successfully"}
    except Exception as e:
        handle_service_error(e)


# ============= Project Endpoints =============

@projects_router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project: ProjectCreate,
    current_user=Depends(require_permission(Permission.PROJECT_CREATE)),
    db: Session = Depends(get_db)
):
    """Create new project with initial screening."""
    try:
        project_service = ProjectService(db)
        
        project_data = project.dict()
        project_data['assessor_name'] = current_user.full_name or current_user.username
        project_data['assessor_organization'] = current_user.organization
        
        created_project, assessment = project_service.create_project_with_screening(project_data)
        
        return ProjectResponse.from_orm(created_project)
    except Exception as e:
        handle_service_error(e)


@projects_router.get("/", response_model=List[ProjectResponse])
async def list_projects(
    search: Optional[str] = Query(None, description="Search in name, description, client"),
    status: Optional[ProjectStatus] = Query(None),
    location: Optional[str] = Query(None),
    project_type: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user=Depends(require_permission(Permission.PROJECT_READ)),
    db: Session = Depends(get_db)
):
    """List projects with filtering and pagination."""
    project_service = ProjectService(db)
    auth_service = AuthService(db)
    
    # Apply access control for clients
    if current_user.role == UserRole.CLIENT.value:
        # Clients only see their own projects
        projects = project_service.search_projects(
            query=search,
            status=status,
            location=location,
            project_type=project_type,
            limit=limit,
            offset=offset
        )
        # Filter by client access
        projects = [p for p in projects if auth_service.check_project_access(current_user, p.id)]
    else:
        projects = project_service.search_projects(
            query=search,
            status=status,
            location=location,
            project_type=project_type,
            limit=limit,
            offset=offset
        )
    
    return [ProjectResponse.from_orm(p) for p in projects]


@projects_router.get("/{project_id}", response_model=ProjectDetailResponse)
async def get_project(
    project_id: int,
    current_user=Depends(require_permission(Permission.PROJECT_READ)),
    db: Session = Depends(get_db)
):
    """Get project details with dashboard data."""
    try:
        auth_service = AuthService(db)
        
        # Check project access
        if not auth_service.check_project_access(current_user, project_id):
            raise UnauthorizedError("Access denied to this project")
        
        project_service = ProjectService(db)
        dashboard = project_service.get_project_dashboard(project_id)
        
        return ProjectDetailResponse(**dashboard)
    except Exception as e:
        handle_service_error(e)


@projects_router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    update_data: ProjectUpdate,
    current_user=Depends(require_permission(Permission.PROJECT_UPDATE)),
    db: Session = Depends(get_db)
):
    """Update project information."""
    try:
        auth_service = AuthService(db)
        
        # Check project access
        if not auth_service.check_project_access(current_user, project_id):
            raise UnauthorizedError("Access denied to this project")
        
        project_service = ProjectService(db)
        updated_project = project_service.update(
            project_id, 
            update_data.dict(exclude_unset=True)
        )
        
        return ProjectResponse.from_orm(updated_project)
    except Exception as e:
        handle_service_error(e)


@projects_router.post("/{project_id}/impact-assessment", response_model=ImpactResponse)
async def perform_impact_assessment(
    project_id: int,
    impact_data: ImpactAssessmentRequest,
    current_user=Depends(require_permission(Permission.ASSESSMENT_CREATE)),
    db: Session = Depends(get_db)
):
    """Perform comprehensive impact assessment."""
    try:
        auth_service = AuthService(db)
        
        # Check project access
        if not auth_service.check_project_access(current_user, project_id):
            raise UnauthorizedError("Access denied to this project")
        
        project_service = ProjectService(db)
        impact_record = project_service.perform_impact_assessment(
            project_id,
            impact_data.dict()
        )
        
        return ImpactResponse.from_orm(impact_record)
    except Exception as e:
        handle_service_error(e)


@projects_router.post("/{project_id}/check-compliance", response_model=ComplianceReportResponse)
async def check_project_compliance(
    project_id: int,
    compliance_data: Optional[ComplianceCheckRequest] = None,
    current_user=Depends(require_permission(Permission.COMPLIANCE_CREATE)),
    db: Session = Depends(get_db)
):
    """Check regulatory compliance for project."""
    try:
        auth_service = AuthService(db)
        
        # Check project access
        if not auth_service.check_project_access(current_user, project_id):
            raise UnauthorizedError("Access denied to this project")
        
        project_service = ProjectService(db)
        compliance_records = project_service.check_compliance(
            project_id,
            compliance_data.dict() if compliance_data else None
        )
        
        # Calculate summary
        total = len(compliance_records)
        compliant = sum(1 for r in compliance_records if r.status == "Compliant")
        
        return ComplianceReportResponse(
            project_id=project_id,
            total_checks=total,
            compliant_checks=compliant,
            compliance_percentage=(compliant / total * 100) if total > 0 else 100,
            checks=[ComplianceCheckResponse.from_orm(r) for r in compliance_records]
        )
    except Exception as e:
        handle_service_error(e)


# ============= Monitoring Endpoints =============

@monitoring_router.post("/record", response_model=MonitoringDataResponse, status_code=status.HTTP_201_CREATED)
async def record_monitoring_data(
    data: MonitoringDataCreate,
    current_user=Depends(require_permission(Permission.MONITORING_CREATE)),
    db: Session = Depends(get_db)
):
    """Record environmental monitoring data."""
    try:
        auth_service = AuthService(db)
        
        # Check project access
        if not auth_service.check_project_access(current_user, data.project_id):
            raise UnauthorizedError("Access denied to this project")
        
        monitoring_service = MonitoringService(db)
        record = monitoring_service.record_measurement(
            project_id=data.project_id,
            parameter=data.parameter,
            value=data.value,
            monitoring_point=data.monitoring_point,
            coordinates=(data.latitude, data.longitude) if data.latitude and data.longitude else None,
            weather_conditions=data.weather_conditions,
            equipment_used=data.equipment_used
        )
        
        return MonitoringDataResponse.from_orm(record)
    except Exception as e:
        handle_service_error(e)


@monitoring_router.post("/bulk-record", response_model=List[MonitoringDataResponse])
async def bulk_record_monitoring_data(
    data_list: List[MonitoringDataCreate],
    current_user=Depends(require_permission(Permission.MONITORING_CREATE)),
    db: Session = Depends(get_db)
):
    """Record multiple monitoring measurements."""
    try:
        auth_service = AuthService(db)
        
        # Check project access for all projects
        project_ids = set(d.project_id for d in data_list)
        for project_id in project_ids:
            if not auth_service.check_project_access(current_user, project_id):
                raise UnauthorizedError(f"Access denied to project {project_id}")
        
        monitoring_service = MonitoringService(db)
        records = monitoring_service.bulk_record_measurements(
            [d.dict() for d in data_list]
        )
        
        return [MonitoringDataResponse.from_orm(r) for r in records]
    except Exception as e:
        handle_service_error(e)


@monitoring_router.get("/projects/{project_id}/latest", response_model=Dict[str, Any])
async def get_latest_readings(
    project_id: int,
    parameters: Optional[List[str]] = Query(None),
    current_user=Depends(require_permission(Permission.MONITORING_READ)),
    db: Session = Depends(get_db)
):
    """Get latest monitoring readings for project."""
    try:
        auth_service = AuthService(db)
        
        # Check project access
        if not auth_service.check_project_access(current_user, project_id):
            raise UnauthorizedError("Access denied to this project")
        
        monitoring_service = MonitoringService(db)
        readings = monitoring_service.get_latest_readings(project_id, parameters)
        
        return readings
    except Exception as e:
        handle_service_error(e)


@monitoring_router.get("/projects/{project_id}/trends/{parameter}", response_model=TrendAnalysisResponse)
async def analyze_parameter_trend(
    project_id: int,
    parameter: str,
    days: int = Query(30, ge=1, le=365),
    current_user=Depends(require_permission(Permission.MONITORING_READ)),
    db: Session = Depends(get_db)
):
    """Analyze trends for specific parameter."""
    try:
        auth_service = AuthService(db)
        
        # Check project access
        if not auth_service.check_project_access(current_user, project_id):
            raise UnauthorizedError("Access denied to this project")
        
        monitoring_service = MonitoringService(db)
        trend = monitoring_service.analyze_trends(project_id, parameter, days)
        
        return TrendAnalysisResponse(
            parameter=trend.parameter,
            trend=trend.trend,
            change_percentage=trend.change_percentage,
            forecast_value=trend.forecast_value,
            confidence=trend.confidence
        )
    except Exception as e:
        handle_service_error(e)


@monitoring_router.get("/alerts", response_model=List[AlertResponse])
async def get_monitoring_alerts(
    project_id: Optional[int] = Query(None),
    severity: Optional[str] = Query(None),
    hours: int = Query(24, ge=1, le=168),
    current_user=Depends(require_permission(Permission.MONITORING_READ)),
    db: Session = Depends(get_db)
):
    """Get recent monitoring alerts."""
    try:
        auth_service = AuthService(db)
        
        # Check project access if specified
        if project_id and not auth_service.check_project_access(current_user, project_id):
            raise UnauthorizedError("Access denied to this project")
        
        monitoring_service = MonitoringService(db)
        alerts = monitoring_service.get_monitoring_alerts(project_id, severity, hours)
        
        # Filter alerts by user access
        if current_user.role == UserRole.CLIENT.value:
            alerts = [a for a in alerts if auth_service.check_project_access(current_user, a.project_id)]
        
        return [
            AlertResponse(
                project_id=a.project_id,
                parameter=a.parameter,
                value=a.value,
                threshold=a.threshold,
                severity=a.severity,
                message=a.message,
                timestamp=a.timestamp.isoformat(),
                location=a.location
            )
            for a in alerts
        ]
    except Exception as e:
        handle_service_error(e)


# ============= Water Resources Endpoints =============

@water_router.post("/projects/{project_id}/assess")
async def assess_water_impact(
    project_id: int,
    activities: Dict[str, float] = Body(..., description="Activity quantities"),
    water_sources: Optional[Dict[str, float]] = Body(None, description="Water source breakdown"),
    baseline_quality: Optional[Dict[str, float]] = Body(None, description="Baseline water quality"),
    current_user=Depends(require_permission(Permission.ASSESSMENT_CREATE)),
    db: Session = Depends(get_db)
):
    """Perform comprehensive water impact assessment."""
    try:
        auth_service = AuthService(db)
        
        # Check project access
        if not auth_service.check_project_access(current_user, project_id):
            raise UnauthorizedError("Access denied to this project")
        
        water_service = WaterService(db)
        assessment = water_service.assess_water_impact(
            project_id=project_id,
            activities=activities,
            water_sources=water_sources,
            baseline_quality=baseline_quality
        )
        
        return assessment
    except Exception as e:
        handle_service_error(e)


@water_router.get("/projects/{project_id}/assessments")
async def get_water_assessment_history(
    project_id: int,
    limit: int = Query(10, ge=1, le=50),
    current_user=Depends(require_permission(Permission.ASSESSMENT_READ)),
    db: Session = Depends(get_db)
):
    """Get water assessment history for project."""
    try:
        auth_service = AuthService(db)
        
        # Check project access
        if not auth_service.check_project_access(current_user, project_id):
            raise UnauthorizedError("Access denied to this project")
        
        water_service = WaterService(db)
        assessments = water_service.get_water_assessment_history(project_id, limit)
        
        return {"project_id": project_id, "assessments": assessments}
    except Exception as e:
        handle_service_error(e)


@water_router.post("/projects/{project_id}/monitor")
async def update_water_monitoring(
    project_id: int,
    actual_consumption: float = Body(..., description="Actual daily consumption in m³"),
    date: datetime = Body(...),
    quality_data: Optional[Dict[str, float]] = Body(None, description="Water quality measurements"),
    current_user=Depends(require_permission(Permission.MONITORING_CREATE)),
    db: Session = Depends(get_db)
):
    """Update water consumption monitoring data."""
    try:
        auth_service = AuthService(db)
        
        # Check project access
        if not auth_service.check_project_access(current_user, project_id):
            raise UnauthorizedError("Access denied to this project")
        
        water_service = WaterService(db)
        result = water_service.update_water_monitoring(
            project_id=project_id,
            actual_consumption=actual_consumption,
            date=date,
            quality_data=quality_data
        )
        
        return result
    except Exception as e:
        handle_service_error(e)


@water_router.get("/projects/{project_id}/report")
async def generate_water_report(
    project_id: int,
    report_type: str = Query("comprehensive", regex="^(summary|compliance|conservation|comprehensive)$"),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    current_user=Depends(require_permission(Permission.REPORT_GENERATE)),
    db: Session = Depends(get_db)
):
    """Generate water management report."""
    try:
        auth_service = AuthService(db)
        
        # Check project access
        if not auth_service.check_project_access(current_user, project_id):
            raise UnauthorizedError("Access denied to this project")
        
        water_service = WaterService(db)
        report = water_service.generate_water_report(
            project_id=project_id,
            report_type=report_type,
            start_date=start_date,
            end_date=end_date
        )
        
        return report
    except Exception as e:
        handle_service_error(e)


# ============= Report Endpoints =============

@reports_router.get("/projects/{project_id}/monitoring-report", response_model=MonitoringReportResponse)
async def generate_monitoring_report(
    project_id: int,
    start_date: datetime = Query(...),
    end_date: datetime = Query(...),
    current_user=Depends(require_permission(Permission.REPORT_GENERATE)),
    db: Session = Depends(get_db)
):
    """Generate monitoring report for date range."""
    try:
        auth_service = AuthService(db)
        
        # Check project access
        if not auth_service.check_project_access(current_user, project_id):
            raise UnauthorizedError("Access denied to this project")
        
        monitoring_service = MonitoringService(db)
        report = monitoring_service.generate_monitoring_report(
            project_id, start_date, end_date
        )
        
        return MonitoringReportResponse(**report)
    except Exception as e:
        handle_service_error(e)


@reports_router.post("/generate", response_model=ReportResponse)
async def generate_report(
    request: ReportGenerationRequest,
    current_user=Depends(require_permission(Permission.REPORT_GENERATE)),
    db: Session = Depends(get_db)
):
    """Generate comprehensive report in various formats."""
    try:
        auth_service = AuthService(db)
        
        # Check project access
        if not auth_service.check_project_access(current_user, request.project_id):
            raise UnauthorizedError("Access denied to this project")
        
        report_service = ReportService(db)
        
        # Create report config
        from src.services.report_service import ReportConfig
        config = ReportConfig(
            report_type=ReportType(request.report_type),
            language=ReportLanguage(request.language),
            include_sections=request.include_sections,
            date_range=request.date_range
        )
        
        # Generate report
        if request.format == "pdf":
            report_bytes = report_service.generate_report(
                request.project_id,
                config
            )
            
            # In a real implementation, you would upload to a storage service
            # and return a download URL. For now, we'll return a placeholder
            report_id = f"rpt_{request.project_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            return ReportResponse(
                report_id=report_id,
                project_id=request.project_id,
                report_type=request.report_type,
                format=request.format,
                status="completed",
                download_url=f"/api/reports/download/{report_id}",
                generated_at=datetime.now()
            )
        
        elif request.format == "excel":
            from src.reporting import ExcelExporter
            exporter = ExcelExporter(db)
            
            excel_bytes = exporter.export_project_data(
                request.project_id,
                include_charts=True
            )
            
            report_id = f"xls_{request.project_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            return ReportResponse(
                report_id=report_id,
                project_id=request.project_id,
                report_type="comprehensive",
                format="excel",
                status="completed",
                download_url=f"/api/reports/download/{report_id}",
                generated_at=datetime.now()
            )
        
        else:
            # JSON format - return data directly
            from src.reporting import ReportGenerator
            generator = ReportGenerator(db)
            
            report_data = generator.get_report_data(request.project_id)
            
            return ReportResponse(
                report_id="json_export",
                project_id=request.project_id,
                report_type="data_export",
                format="json",
                status="completed",
                download_url=None,
                generated_at=datetime.now()
            )
            
    except Exception as e:
        handle_service_error(e)


@reports_router.get("/projects/{project_id}/available-reports")
async def get_available_reports(
    project_id: int,
    current_user=Depends(require_permission(Permission.REPORT_READ)),
    db: Session = Depends(get_db)
):
    """Get list of available report types for a project."""
    try:
        auth_service = AuthService(db)
        
        # Check project access
        if not auth_service.check_project_access(current_user, project_id):
            raise UnauthorizedError("Access denied to this project")
        
        # Check what data is available
        project_service = ProjectService(db)
        project = project_service.get_by_id(project_id)
        
        if not project:
            raise NotFoundError("Project not found")
        
        # Check available data
        has_screening = db.query(Assessment).filter_by(project_id=project_id).first() is not None
        has_impact = db.query(ImpactRecord).filter_by(project_id=project_id).first() is not None
        has_compliance = db.query(ComplianceRecord).filter_by(project_id=project_id).first() is not None
        has_monitoring = db.query(MonitoringData).filter_by(project_id=project_id).first() is not None
        
        available_reports = []
        
        if has_screening:
            available_reports.append({
                "type": "screening",
                "name": "Screening Report",
                "description": "Environmental screening assessment results",
                "formats": ["pdf", "excel"]
            })
        
        if has_impact:
            available_reports.append({
                "type": "impact",
                "name": "Impact Assessment Report",
                "description": "Comprehensive environmental impact analysis",
                "formats": ["pdf", "excel"]
            })
        
        if has_compliance:
            available_reports.append({
                "type": "compliance",
                "name": "Compliance Report",
                "description": "Regulatory compliance status and gaps",
                "formats": ["pdf", "excel"]
            })
        
        if has_monitoring:
            available_reports.append({
                "type": "monitoring",
                "name": "Monitoring Report",
                "description": "Environmental monitoring data and trends",
                "formats": ["pdf", "excel", "json"]
            })
        
        # Always available
        available_reports.extend([
            {
                "type": "comprehensive",
                "name": "Comprehensive Report",
                "description": "Complete environmental assessment report",
                "formats": ["pdf"]
            },
            {
                "type": "executive_summary",
                "name": "Executive Summary",
                "description": "High-level summary for decision makers",
                "formats": ["pdf"]
            }
        ])
        
        return {"project_id": project_id, "available_reports": available_reports}
        
    except Exception as e:
        handle_service_error(e)


@reports_router.post("/batch-generate")
async def generate_batch_reports(
    project_ids: List[int] = Body(...),
    report_type: str = Body(...),
    format: str = Body("pdf"),
    current_user=Depends(require_permission(Permission.REPORT_GENERATE)),
    db: Session = Depends(get_db)
):
    """Generate reports for multiple projects."""
    try:
        auth_service = AuthService(db)
        
        # Check access for all projects
        authorized_projects = []
        for project_id in project_ids:
            if auth_service.check_project_access(current_user, project_id):
                authorized_projects.append(project_id)
        
        if not authorized_projects:
            raise UnauthorizedError("No access to any of the specified projects")
        
        # Generate reports
        results = []
        
        if format == "pdf":
            report_service = ReportService(db)
            from src.services.report_service import ReportConfig
            
            config = ReportConfig(
                report_type=ReportType(report_type),
                language=ReportLanguage.ENGLISH
            )
            
            for project_id in authorized_projects:
                try:
                    report_bytes = report_service.generate_report(
                        project_id,
                        config
                    )
                    
                    report_id = f"batch_{project_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    
                    results.append({
                        "project_id": project_id,
                        "status": "success",
                        "report_id": report_id,
                        "download_url": f"/api/reports/download/{report_id}"
                    })
                except Exception as e:
                    results.append({
                        "project_id": project_id,
                        "status": "failed",
                        "error": str(e)
                    })
        
        return {
            "total_requested": len(project_ids),
            "total_authorized": len(authorized_projects),
            "total_generated": sum(1 for r in results if r["status"] == "success"),
            "results": results
        }
        
    except Exception as e:
        handle_service_error(e)


# Export all routers
all_routers = [
    auth_router,
    projects_router,
    monitoring_router,
    assessment_router,
    water_router,
    compliance_router,
    reports_router
]