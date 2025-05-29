"""
Database Models
SQLAlchemy models for environmental impact assessment data

Author: Edy Bassil
Email: bassileddy@gmail.com
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import enum
import os

Base = declarative_base()


class ProjectStatus(enum.Enum):
    """Project status options."""
    PLANNING = "Planning"
    SCREENING = "Screening"
    ASSESSMENT = "Assessment"
    CONSTRUCTION = "Construction"
    OPERATION = "Operation"
    COMPLETED = "Completed"


class AssessmentType(enum.Enum):
    """Types of environmental assessments."""
    SCREENING = "Screening"
    LIMITED_EIA = "Limited EIA"
    FULL_EIA = "Full EIA"
    STRATEGIC = "Strategic"


class Project(Base):
    """Project information model."""
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    project_type = Column(String(50), nullable=False)
    location = Column(String(100), nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    size = Column(Float)  # in m²
    duration = Column(Integer)  # in months
    budget = Column(Float)  # in millions
    status = Column(SQLEnum(ProjectStatus), default=ProjectStatus.PLANNING)
    
    # Client information
    client_name = Column(String(200))
    client_contact = Column(String(100))
    contractor = Column(String(200))
    
    # Key parameters
    num_workers = Column(Integer)
    water_usage = Column(Float)  # m³/day
    construction_area = Column(Float)  # m²
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    assessments = relationship("Assessment", back_populates="project", cascade="all, delete-orphan")
    impacts = relationship("ImpactRecord", back_populates="project", cascade="all, delete-orphan")
    compliance_checks = relationship("ComplianceRecord", back_populates="project", cascade="all, delete-orphan")
    mitigation_measures = relationship("MitigationMeasure", back_populates="project", cascade="all, delete-orphan")
    water_assessments = relationship("WaterAssessment", back_populates="project", cascade="all, delete-orphan")
    monitoring_data = relationship("MonitoringData", back_populates="project", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="project", cascade="all, delete-orphan")


class Assessment(Base):
    """Environmental assessment records."""
    __tablename__ = 'assessments'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    assessment_type = Column(SQLEnum(AssessmentType), nullable=False)
    assessment_date = Column(DateTime, default=datetime.utcnow)
    
    # Screening results
    eia_required = Column(Boolean, default=False)
    eia_level = Column(String(50))
    key_concerns = Column(JSON)  # List of concerns
    regulatory_requirements = Column(JSON)  # List of requirements
    specialist_studies = Column(JSON)  # List of required studies
    estimated_duration = Column(Integer)  # days
    
    # Assessment details
    assessor_name = Column(String(100))
    assessor_organization = Column(String(200))
    methodology = Column(Text)
    
    # Status
    status = Column(String(50), default="In Progress")
    approval_date = Column(DateTime)
    approval_authority = Column(String(200))
    approval_reference = Column(String(100))
    
    # Relationships
    project = relationship("Project", back_populates="assessments")


class ImpactRecord(Base):
    """Environmental impact measurements and calculations."""
    __tablename__ = 'impact_records'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    assessment_date = Column(DateTime, default=datetime.utcnow)
    
    # Air quality impacts
    pm10_concentration = Column(Float)  # μg/m³
    pm25_concentration = Column(Float)  # μg/m³
    nox_emissions = Column(Float)  # kg
    so2_emissions = Column(Float)  # kg
    co_emissions = Column(Float)  # kg
    
    # Noise impacts
    peak_noise_level = Column(Float)  # dB(A)
    average_noise_level = Column(Float)  # dB(A)
    nearest_receptor_distance = Column(Float)  # meters
    
    # Carbon footprint
    carbon_footprint = Column(Float)  # tonnes CO2e
    material_emissions = Column(Float)  # tonnes CO2e
    equipment_emissions = Column(Float)  # tonnes CO2e
    transport_emissions = Column(Float)  # tonnes CO2e
    
    # Water impacts
    water_consumption = Column(Float)  # m³
    wastewater_generation = Column(Float)  # m³
    
    # Waste impacts
    waste_generation = Column(Float)  # tonnes
    hazardous_waste = Column(Float)  # tonnes
    recycled_waste = Column(Float)  # tonnes
    
    # Energy usage
    energy_usage = Column(Float)  # MWh
    renewable_energy = Column(Float)  # MWh
    
    # Biodiversity
    biodiversity_score = Column(Float)  # 0-100
    area_cleared = Column(Float)  # m²
    habitat_type = Column(String(100))
    
    # Overall assessment
    impact_severity = Column(String(50))  # Low, Medium, High
    mitigation_effectiveness = Column(Float)  # percentage
    
    # Relationships
    project = relationship("Project", back_populates="impacts")


class ComplianceRecord(Base):
    """Regulatory compliance check records."""
    __tablename__ = 'compliance_records'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    check_date = Column(DateTime, default=datetime.utcnow)
    
    # Compliance details
    jurisdiction = Column(String(50), nullable=False)
    regulation_id = Column(String(50))
    regulation_name = Column(String(200))
    category = Column(String(100))
    
    # Compliance status
    status = Column(String(50))  # Compliant, Non-Compliant, Conditional
    actual_value = Column(Float)
    required_value = Column(Float)
    deviation = Column(Float)  # percentage
    
    # Actions
    recommendation = Column(Text)
    evidence_required = Column(JSON)  # List of required documents
    deadline = Column(DateTime)
    
    # Resolution
    resolved = Column(Boolean, default=False)
    resolution_date = Column(DateTime)
    resolution_notes = Column(Text)
    
    # Relationships
    project = relationship("Project", back_populates="compliance_checks")


class MitigationMeasure(Base):
    """Mitigation measures for environmental impacts."""
    __tablename__ = 'mitigation_measures'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    
    # Measure details
    impact_category = Column(String(100), nullable=False)
    measure_type = Column(String(100))
    description = Column(Text, nullable=False)
    
    # Implementation
    implementation_date = Column(DateTime)
    responsible_party = Column(String(200))
    cost_estimate = Column(Float)  # in currency units
    
    # Effectiveness
    expected_reduction = Column(Float)  # percentage
    actual_reduction = Column(Float)  # percentage
    
    # Status
    status = Column(String(50), default="Planned")  # Planned, In Progress, Implemented
    verification_date = Column(DateTime)
    verified_by = Column(String(100))
    
    # Relationships
    project = relationship("Project", back_populates="mitigation_measures")


class WaterAssessment(Base):
    """Water assessment records for environmental impacts."""
    __tablename__ = 'water_assessments'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    
    # Assessment details
    assessment_date = Column(DateTime, default=datetime.utcnow)
    
    # Consumption metrics
    daily_consumption = Column(Float)  # m³/day
    peak_consumption = Column(Float)  # m³/day
    total_consumption = Column(Float)  # m³
    
    # Detailed breakdowns (JSON)
    consumption_by_activity = Column(JSON)  # {"concrete_mixing": 100, "dust_control": 50, etc.}
    consumption_by_source = Column(JSON)  # {"municipal": 80%, "tanker": 20%, etc.}
    
    # Water balance
    water_balance = Column(Float)  # m³ (supply - demand)
    recycled_water = Column(Float)  # m³
    conservation_potential = Column(Float)  # m³
    
    # Risk assessment
    scarcity_risk = Column(String(50))  # Low, Medium, High
    quality_risk = Column(String(50))  # Low, Medium, High
    compliance_risk = Column(String(50))  # Low, Medium, High
    overall_risk = Column(String(50))  # Low, Medium, High
    
    # Mitigation and impacts (JSON)
    mitigation_priorities = Column(JSON)  # List of priority mitigation measures
    quality_impacts = Column(JSON)  # {"TSS": 100, "pH": 7.5, "BOD": 20, etc.}
    
    # Relationships
    project = relationship("Project", back_populates="water_assessments")


class MonitoringData(Base):
    """Environmental monitoring data records."""
    __tablename__ = 'monitoring_data'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    
    # Monitoring details
    parameter = Column(String(100), nullable=False)  # PM10, Noise, etc.
    measurement_date = Column(DateTime, default=datetime.utcnow)
    measurement_time = Column(String(10))  # HH:MM
    
    # Location
    monitoring_point = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Measurement
    value = Column(Float, nullable=False)
    unit = Column(String(20), nullable=False)
    
    # Quality
    equipment_used = Column(String(100))
    calibration_date = Column(DateTime)
    weather_conditions = Column(String(200))
    
    # Compliance
    limit_value = Column(Float)
    exceeds_limit = Column(Boolean, default=False)
    
    # Relationships
    project = relationship("Project", back_populates="monitoring_data")


class Document(Base):
    """Document management for projects."""
    __tablename__ = 'documents'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    
    # Document details
    document_type = Column(String(100), nullable=False)  # EIA Report, Permit, etc.
    title = Column(String(200), nullable=False)
    filename = Column(String(255))
    file_path = Column(String(500))
    file_size = Column(Integer)  # in bytes
    
    # Metadata
    version = Column(String(20))
    author = Column(String(100))
    upload_date = Column(DateTime, default=datetime.utcnow)
    
    # Approval
    approval_status = Column(String(50))  # Draft, Under Review, Approved
    approved_by = Column(String(100))
    approval_date = Column(DateTime)
    
    # Expiry
    valid_until = Column(DateTime)
    renewal_required = Column(Boolean, default=False)
    
    # Relationships
    project = relationship("Project", back_populates="documents")


class User(Base):
    """User accounts for the system."""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    full_name = Column(String(100))
    organization = Column(String(200))
    role = Column(String(50))  # Admin, Assessor, Client, Regulator
    
    # Credentials (in production, use proper hashing)
    password_hash = Column(String(255))
    
    # Status
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    
    # Preferences
    preferred_language = Column(String(10), default="en")
    notification_email = Column(Boolean, default=True)


# Database setup functions
def get_database_url():
    """Get database URL from environment or use default SQLite."""
    return os.getenv('DATABASE_URL', 'sqlite:///eia_database.db')


def init_database():
    """Initialize the database with tables."""
    engine = create_engine(get_database_url())
    Base.metadata.create_all(engine)
    return engine


def get_session():
    """Get database session."""
    engine = create_engine(get_database_url())
    Session = sessionmaker(bind=engine)
    return Session()


# Example usage functions
def create_sample_project(session):
    """Create a sample project in the database."""
    project = Project(
        name="Dubai Marina Tower",
        description="50-story mixed-use development in Dubai Marina",
        project_type="commercial",
        location="Dubai",
        latitude=25.0807,
        longitude=55.1408,
        size=25000,
        duration=24,
        budget=500,
        client_name="Marina Development LLC",
        contractor="ABC Construction",
        num_workers=500,
        water_usage=1200,
        construction_area=5000
    )
    
    session.add(project)
    session.commit()
    
    return project


def record_impact_assessment(session, project_id, impact_data):
    """Record impact assessment results."""
    impact = ImpactRecord(
        project_id=project_id,
        **impact_data
    )
    
    session.add(impact)
    session.commit()
    
    return impact


def main():
    """Example database operations."""
    # Initialize database
    engine = init_database()
    session = get_session()
    
    # Create sample project
    project = create_sample_project(session)
    print(f"Created project: {project.name} (ID: {project.id})")
    
    # Record impact assessment
    impact_data = {
        'pm10_concentration': 120,
        'pm25_concentration': 55,
        'peak_noise_level': 75,
        'average_noise_level': 68,
        'carbon_footprint': 1500,
        'water_consumption': 45000,
        'waste_generation': 250,
        'biodiversity_score': 65
    }
    
    impact = record_impact_assessment(session, project.id, impact_data)
    print(f"Recorded impact assessment (ID: {impact.id})")
    
    # Query projects
    projects = session.query(Project).all()
    print(f"\nTotal projects in database: {len(projects)}")
    
    session.close()


if __name__ == "__main__":
    main()