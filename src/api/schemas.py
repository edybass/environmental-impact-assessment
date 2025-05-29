"""
API Schemas
Pydantic models for API requests and responses

Author: Edy Bassil
Email: bassileddy@gmail.com
"""

from pydantic import BaseModel, Field, EmailStr, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

from src.models import ProjectStatus, AssessmentType


# ============= Authentication Schemas =============

class UserRegistration(BaseModel):
    """User registration request."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = Field(None, max_length=100)
    organization: Optional[str] = Field(None, max_length=200)
    role: Optional[str] = Field("client")
    
    @validator('username')
    def validate_username(cls, v):
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Username can only contain letters, numbers, underscores, and hyphens')
        return v


class LoginCredentials(BaseModel):
    """Login credentials."""
    username: str = Field(..., description="Username or email")
    password: str


class PasswordChange(BaseModel):
    """Password change request."""
    old_password: str
    new_password: str = Field(..., min_length=8)


class UserResponse(BaseModel):
    """User response model."""
    id: int
    username: str
    email: str
    full_name: Optional[str]
    organization: Optional[str]
    role: str
    active: bool
    created_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        orm_mode = True


class TokenResponse(BaseModel):
    """Authentication token response."""
    access_token: str
    token_type: str = "bearer"
    expires_in: float
    user: UserResponse


# ============= Project Schemas =============

class ProjectCreate(BaseModel):
    """Project creation request."""
    name: str = Field(..., min_length=3, max_length=200)
    description: Optional[str] = None
    project_type: str = Field(..., regex="^(residential|commercial|industrial|infrastructure|mixed_use)$")
    location: str = Field(..., regex="^(Dubai|Abu Dhabi|Sharjah|Riyadh|Jeddah|NEOM)$")
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    size: Optional[float] = Field(None, ge=0, description="Project size in m²")
    duration: Optional[int] = Field(None, ge=1, description="Duration in months")
    budget: Optional[float] = Field(None, ge=0, description="Budget in millions")
    client_name: Optional[str] = Field(None, max_length=200)
    client_contact: Optional[str] = Field(None, max_length=100)
    contractor: Optional[str] = Field(None, max_length=200)
    num_workers: Optional[int] = Field(None, ge=0)
    water_usage: Optional[float] = Field(None, ge=0, description="Water usage in m³/day")
    construction_area: Optional[float] = Field(None, ge=0, description="Construction area in m²")
    
    # Screening parameters
    sensitive_receptors: Optional[List[str]] = []
    near_protected_area: Optional[bool] = False


class ProjectUpdate(BaseModel):
    """Project update request."""
    name: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = None
    location: Optional[str] = Field(None, regex="^(Dubai|Abu Dhabi|Sharjah|Riyadh|Jeddah|NEOM)$")
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    size: Optional[float] = Field(None, ge=0)
    duration: Optional[int] = Field(None, ge=1)
    budget: Optional[float] = Field(None, ge=0)
    status: Optional[ProjectStatus] = None
    client_name: Optional[str] = Field(None, max_length=200)
    client_contact: Optional[str] = Field(None, max_length=100)
    contractor: Optional[str] = Field(None, max_length=200)
    num_workers: Optional[int] = Field(None, ge=0)
    water_usage: Optional[float] = Field(None, ge=0)
    construction_area: Optional[float] = Field(None, ge=0)


class ProjectResponse(BaseModel):
    """Project response model."""
    id: int
    name: str
    project_type: str
    location: str
    status: str
    size: Optional[float]
    duration: Optional[int]
    client_name: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class ProjectDetailResponse(BaseModel):
    """Detailed project response with dashboard data."""
    project: Dict[str, Any]
    assessment: Dict[str, Any]
    impacts: Dict[str, Any]
    compliance: Dict[str, Any]
    mitigation: Dict[str, Any]
    monitoring: Dict[str, Any]


# ============= Assessment Schemas =============

class AssessmentResponse(BaseModel):
    """Assessment response model."""
    id: int
    project_id: int
    assessment_type: str
    assessment_date: datetime
    eia_required: bool
    eia_level: Optional[str]
    key_concerns: List[str]
    regulatory_requirements: List[str]
    specialist_studies: List[str]
    estimated_duration: Optional[int]
    status: str
    
    class Config:
        orm_mode = True


# ============= Impact Assessment Schemas =============

class ImpactAssessmentRequest(BaseModel):
    """Impact assessment request."""
    materials: Dict[str, float] = Field(default_factory=dict, description="Materials quantities")
    equipment_hours: Dict[str, float] = Field(default_factory=dict, description="Equipment usage hours")
    transport_km: Optional[float] = Field(0, ge=0)
    concrete_volume: Optional[float] = Field(0, ge=0)
    facility_area: Optional[float] = Field(0, ge=0)
    area_cleared: Optional[float] = Field(0, ge=0)
    habitat_type: Optional[str] = Field("urban")
    mitigation_measures: Optional[List[str]] = []
    
    # Optional specific assessments
    noise_assessment: Optional[Dict[str, float]] = None
    dust_assessment: Optional[Dict[str, float]] = None


class ImpactResponse(BaseModel):
    """Impact assessment response."""
    id: int
    project_id: int
    assessment_date: datetime
    carbon_footprint: Optional[float]
    water_consumption: Optional[float]
    waste_generation: Optional[float]
    energy_usage: Optional[float]
    biodiversity_score: Optional[float]
    pm10_concentration: Optional[float]
    pm25_concentration: Optional[float]
    peak_noise_level: Optional[float]
    average_noise_level: Optional[float]
    impact_severity: Optional[str]
    
    class Config:
        orm_mode = True


# ============= Compliance Schemas =============

class ComplianceCheckRequest(BaseModel):
    """Compliance check request."""
    pm10: Optional[float] = Field(None, ge=0)
    pm25: Optional[float] = Field(None, ge=0)
    noise: Optional[float] = Field(None, ge=0)
    water: Optional[float] = Field(None, ge=0)
    waste_plan: Optional[bool] = False
    waste_segregation: Optional[bool] = False
    water_plan: Optional[bool] = False


class ComplianceCheckResponse(BaseModel):
    """Individual compliance check response."""
    id: int
    regulation_id: str
    regulation_name: str
    category: str
    status: str
    actual_value: Optional[float]
    required_value: Optional[float]
    deviation: Optional[float]
    recommendation: Optional[str]
    
    class Config:
        orm_mode = True


class ComplianceReportResponse(BaseModel):
    """Compliance report response."""
    project_id: int
    total_checks: int
    compliant_checks: int
    compliance_percentage: float
    checks: List[ComplianceCheckResponse]


# ============= Monitoring Schemas =============

class MonitoringDataCreate(BaseModel):
    """Monitoring data creation request."""
    project_id: int
    parameter: str = Field(..., regex="^(pm10|pm25|noise|temperature|humidity|wind_speed|voc|co|no2|so2|vibration)$")
    value: float = Field(..., ge=0)
    monitoring_point: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    weather_conditions: Optional[str] = None
    equipment_used: Optional[str] = None


class MonitoringDataResponse(BaseModel):
    """Monitoring data response."""
    id: int
    project_id: int
    parameter: str
    value: float
    unit: str
    measurement_date: datetime
    measurement_time: Optional[str]
    monitoring_point: Optional[str]
    exceeds_limit: bool
    limit_value: Optional[float]
    
    class Config:
        orm_mode = True


class TrendAnalysisResponse(BaseModel):
    """Trend analysis response."""
    parameter: str
    trend: str
    change_percentage: float
    forecast_value: float
    confidence: float


class AlertResponse(BaseModel):
    """Monitoring alert response."""
    project_id: int
    parameter: str
    value: float
    threshold: float
    severity: str
    message: str
    timestamp: str
    location: Optional[str]


class MonitoringReportResponse(BaseModel):
    """Monitoring report response."""
    project_id: int
    period: Dict[str, Any]
    parameters: Dict[str, Dict[str, Any]]
    overall: Dict[str, Any]


# ============= Risk Schemas =============

class RiskResponse(BaseModel):
    """Risk assessment response."""
    id: str
    category: str
    description: str
    likelihood: str
    consequence: str
    risk_level: str
    mitigation_measures: Optional[List[str]]
    residual_risk_level: Optional[str]


# ============= Mitigation Schemas =============

class MitigationMeasureCreate(BaseModel):
    """Mitigation measure creation request."""
    project_id: int
    impact_category: str
    measure_type: Optional[str]
    description: str
    responsible_party: Optional[str]
    cost_estimate: Optional[float] = Field(None, ge=0)
    expected_reduction: Optional[float] = Field(None, ge=0, le=100)


class MitigationMeasureResponse(BaseModel):
    """Mitigation measure response."""
    id: int
    project_id: int
    impact_category: str
    measure_type: Optional[str]
    description: str
    implementation_date: Optional[datetime]
    responsible_party: Optional[str]
    cost_estimate: Optional[float]
    expected_reduction: Optional[float]
    actual_reduction: Optional[float]
    status: str
    
    class Config:
        orm_mode = True


# ============= Report Schemas =============

class ReportGenerationRequest(BaseModel):
    """Report generation request."""
    project_id: int
    report_type: str = Field(..., regex="^(screening|impact|compliance|monitoring|comprehensive)$")
    format: str = Field("pdf", regex="^(pdf|excel|json)$")
    language: str = Field("en", regex="^(en|ar)$")
    include_sections: Optional[List[str]] = None
    date_range: Optional[Dict[str, datetime]] = None


class ReportResponse(BaseModel):
    """Report generation response."""
    report_id: str
    project_id: int
    report_type: str
    format: str
    status: str
    download_url: Optional[str]
    generated_at: datetime