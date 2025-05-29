"""
Comprehensive tests for new EIA features
Tests for impact calculator, risk matrix, compliance, and database models

Author: Edy Bassil
Email: bassileddy@gmail.com
"""

import pytest
import tempfile
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import modules to test
from src.impact_calculator import ImpactCalculator, ImpactMetrics
from src.risk_matrix import RiskMatrix, Risk, Likelihood, Consequence, RiskLevel
from src.compliance.regulatory_compliance import (
    RegulatoryCompliance, ComplianceStatus, Jurisdiction, ComplianceReport
)
from src.models import Base, Project, ImpactRecord, init_database, get_session
from src.config import Config, get_config


class TestImpactCalculator:
    """Test suite for ImpactCalculator."""
    
    def setup_method(self):
        """Set up test instance."""
        self.calculator = ImpactCalculator()
    
    def test_carbon_footprint_calculation(self):
        """Test carbon footprint calculation."""
        materials = {
            'concrete': 1000,  # m³
            'steel': 150,      # tonnes
            'cement': 200,     # tonnes
        }
        equipment_hours = {
            'excavator': 200,
            'crane': 150,
            'concrete_mixer': 100,
        }
        
        carbon = self.calculator.calculate_carbon_footprint(
            materials, equipment_hours, transport_km=500
        )
        
        assert carbon > 0
        assert isinstance(carbon, float)
        # Check reasonable range (tonnes CO2e)
        assert 500 < carbon < 2000
    
    def test_water_consumption_calculation(self):
        """Test water consumption calculation."""
        water = self.calculator.calculate_water_consumption(
            concrete_volume=1000,
            construction_area=5000,
            duration_days=180,
            num_workers=50
        )
        
        assert water > 0
        assert isinstance(water, float)
        # Check reasonable range (m³)
        assert 1000 < water < 10000
    
    def test_biodiversity_impact_score(self):
        """Test biodiversity impact scoring."""
        # Test desert habitat with mitigation
        score = self.calculator.calculate_biodiversity_impact(
            area_cleared=5000,
            habitat_type='desert',
            mitigation_measures=['habitat_restoration', 'timing_restrictions']
        )
        
        assert 0 <= score <= 100
        assert score > 50  # Desert with mitigation should have lower impact
        
        # Test wetland without mitigation
        score_wetland = self.calculator.calculate_biodiversity_impact(
            area_cleared=5000,
            habitat_type='wetland',
            mitigation_measures=[]
        )
        
        assert score_wetland < score  # Wetland should have higher impact
    
    def test_comprehensive_impact_calculation(self):
        """Test comprehensive impact calculation."""
        project_data = {
            'materials': {'concrete': 500, 'steel': 75},
            'equipment_hours': {'excavator': 100, 'crane': 75},
            'transport_km': 200,
            'concrete_volume': 500,
            'construction_area': 2500,
            'duration_days': 90,
            'num_workers': 25,
            'facility_area': 250,
            'area_cleared': 4000,
            'habitat_type': 'urban',
            'mitigation_measures': ['noise_barriers']
        }
        
        metrics = self.calculator.calculate_comprehensive_impact(project_data)
        
        assert isinstance(metrics, ImpactMetrics)
        assert metrics.carbon_footprint > 0
        assert metrics.water_consumption > 0
        assert metrics.waste_generation > 0
        assert metrics.energy_usage > 0
        assert metrics.biodiversity_score > 0
    
    def test_impact_severity_assessment(self):
        """Test impact severity assessment."""
        # Test low severity
        assert self.calculator._assess_severity(50, 'carbon') == 'low'
        assert self.calculator._assess_severity(500, 'water') == 'low'
        
        # Test medium severity
        assert self.calculator._assess_severity(300, 'carbon') == 'medium'
        assert self.calculator._assess_severity(3000, 'water') == 'medium'
        
        # Test high severity
        assert self.calculator._assess_severity(1000, 'carbon') == 'high'
        assert self.calculator._assess_severity(10000, 'water') == 'high'


class TestRiskMatrix:
    """Test suite for RiskMatrix."""
    
    def setup_method(self):
        """Set up test instance."""
        self.risk_matrix = RiskMatrix()
    
    def test_risk_assessment(self):
        """Test risk level assessment."""
        # Test extreme risk
        assert self.risk_matrix.assess_risk(
            Likelihood.ALMOST_CERTAIN, Consequence.CATASTROPHIC
        ) == RiskLevel.EXTREME
        
        # Test low risk
        assert self.risk_matrix.assess_risk(
            Likelihood.RARE, Consequence.INSIGNIFICANT
        ) == RiskLevel.LOW
        
        # Test medium risk
        assert self.risk_matrix.assess_risk(
            Likelihood.POSSIBLE, Consequence.MINOR
        ) == RiskLevel.MEDIUM
    
    def test_add_risk(self):
        """Test adding risks to register."""
        risk = Risk(
            id="TEST001",
            category="Air Quality",
            description="Test risk",
            likelihood=Likelihood.LIKELY,
            consequence=Consequence.MODERATE,
            existing_controls=["Test control"],
            mitigation_measures=["Test mitigation"]
        )
        
        self.risk_matrix.add_risk(risk)
        
        assert len(self.risk_matrix.risks) == 1
        assert self.risk_matrix.risks[0].risk_level == RiskLevel.HIGH
        assert self.risk_matrix.risks[0].residual_risk_level is not None
    
    def test_construction_risks_generation(self):
        """Test construction risk generation."""
        risks = self.risk_matrix.get_construction_risks("commercial", "Dubai")
        
        assert len(risks) > 0
        assert any(r.category == "Air Quality" for r in risks)
        assert any(r.category == "Noise & Vibration" for r in risks)
        assert any(r.category == "Water Resources" for r in risks)
    
    def test_risk_prioritization(self):
        """Test risk prioritization."""
        risks = [
            Risk("R1", "Cat1", "Low risk", Likelihood.RARE, Consequence.MINOR, []),
            Risk("R2", "Cat2", "High risk", Likelihood.LIKELY, Consequence.MAJOR, []),
            Risk("R3", "Cat3", "Extreme risk", Likelihood.ALMOST_CERTAIN, Consequence.CATASTROPHIC, []),
        ]
        
        for risk in risks:
            self.risk_matrix.add_risk(risk)
        
        prioritized = self.risk_matrix.prioritize_risks()
        
        assert prioritized[0].id == "R3"  # Extreme risk first
        assert prioritized[1].id == "R2"  # High risk second
        assert prioritized[2].id == "R1"  # Low risk last
    
    def test_risk_summary_export(self):
        """Test risk summary export."""
        risks = self.risk_matrix.get_construction_risks("industrial", "NEOM")
        for risk in risks:
            self.risk_matrix.add_risk(risk)
        
        summary = self.risk_matrix.export_risk_summary()
        
        assert summary['total_risks'] == len(risks)
        assert 'by_level' in summary
        assert 'by_category' in summary
        assert 'high_priority_risks' in summary
        assert len(summary['high_priority_risks']) > 0


class TestRegulatoryCompliance:
    """Test suite for RegulatoryCompliance."""
    
    def setup_method(self):
        """Set up test instance."""
        self.compliance = RegulatoryCompliance()
    
    def test_compliance_check_compliant(self):
        """Test compliance check for compliant project."""
        project_data = {
            'project_name': 'Test Project',
            'pm10_concentration': 100,  # Below UAE limit (150)
            'pm25_concentration': 50,   # Below limit
            'noise_level': 60,          # Below limit
            'eia_completed': True,
            'waste_management_plan': True,
            'waste_segregation': True,
            'water_conservation_plan': True
        }
        
        report = self.compliance.check_compliance(project_data, Jurisdiction.DUBAI)
        
        assert isinstance(report, ComplianceReport)
        assert report.compliance_percentage > 80
        assert len(report.checks) > 0
        assert len(report.required_permits) > 0
    
    def test_compliance_check_non_compliant(self):
        """Test compliance check for non-compliant project."""
        project_data = {
            'project_name': 'Test Project',
            'pm10_concentration': 200,  # Above UAE limit
            'noise_level': 80,          # Above limit
            'eia_completed': False,
            'waste_management_plan': False,
            'waste_segregation': False,
        }
        
        report = self.compliance.check_compliance(project_data, Jurisdiction.DUBAI)
        
        assert report.overall_status in [ComplianceStatus.NON_COMPLIANT, ComplianceStatus.CONDITIONAL]
        assert report.compliance_percentage < 100
        assert len(report.action_items) > 0
    
    def test_jurisdiction_comparison(self):
        """Test jurisdiction comparison."""
        comparison = self.compliance.compare_jurisdictions([
            Jurisdiction.DUBAI,
            Jurisdiction.ABU_DHABI,
            Jurisdiction.KSA_NATIONAL
        ])
        
        assert len(comparison) > 0
        assert 'Category' in comparison.columns
        assert Jurisdiction.DUBAI.value in comparison.columns
    
    def test_ksa_compliance(self):
        """Test KSA-specific compliance."""
        project_data = {
            'project_name': 'NEOM Project',
            'pm10_concentration': 300,  # Below KSA limit (340)
            'noise_level': 65,          # Below KSA limit (70)
            'water_conservation_plan': True,
        }
        
        report = self.compliance.check_compliance(project_data, Jurisdiction.KSA_NATIONAL)
        
        # Should be more compliant with KSA standards
        assert any(c.status == ComplianceStatus.COMPLIANT 
                  for c in report.checks 
                  if 'Air Quality' in c.regulation_name)


class TestDatabaseModels:
    """Test suite for database models."""
    
    def setup_method(self):
        """Set up test database."""
        # Use in-memory SQLite for tests
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def teardown_method(self):
        """Clean up test database."""
        self.session.close()
    
    def test_create_project(self):
        """Test project creation."""
        project = Project(
            name="Test Project",
            project_type="commercial",
            location="Dubai",
            size=10000,
            duration=12,
            client_name="Test Client"
        )
        
        self.session.add(project)
        self.session.commit()
        
        # Query project
        saved_project = self.session.query(Project).first()
        assert saved_project is not None
        assert saved_project.name == "Test Project"
        assert saved_project.location == "Dubai"
    
    def test_impact_record(self):
        """Test impact record creation."""
        # Create project first
        project = Project(name="Test Project", project_type="industrial", location="Abu Dhabi")
        self.session.add(project)
        self.session.commit()
        
        # Create impact record
        impact = ImpactRecord(
            project_id=project.id,
            pm10_concentration=125,
            pm25_concentration=60,
            peak_noise_level=72,
            carbon_footprint=850,
            biodiversity_score=75
        )
        
        self.session.add(impact)
        self.session.commit()
        
        # Query impact
        saved_impact = self.session.query(ImpactRecord).first()
        assert saved_impact is not None
        assert saved_impact.pm10_concentration == 125
        assert saved_impact.project_id == project.id
    
    def test_project_relationships(self):
        """Test project relationships."""
        project = Project(name="Test Project", project_type="residential", location="Riyadh")
        self.session.add(project)
        self.session.commit()
        
        # Add multiple impact records
        for i in range(3):
            impact = ImpactRecord(
                project_id=project.id,
                pm10_concentration=100 + i * 10,
                assessment_date=datetime.utcnow()
            )
            self.session.add(impact)
        
        self.session.commit()
        
        # Query project with relationships
        project = self.session.query(Project).first()
        assert len(project.impacts) == 3
        assert all(impact.project_id == project.id for impact in project.impacts)


class TestConfiguration:
    """Test suite for configuration management."""
    
    def test_config_initialization(self):
        """Test configuration initialization."""
        config = Config()
        
        assert config.env in ["development", "production", "testing"]
        assert config.database.url is not None
        assert config.api.port > 0
        assert config.regional.uae_pm10_limit == 150
    
    def test_threshold_retrieval(self):
        """Test threshold retrieval."""
        config = Config()
        
        # Test UAE thresholds
        assert config.get_threshold("pm10", "UAE") == 150
        assert config.get_threshold("pm25", "UAE") == 65
        
        # Test KSA thresholds
        assert config.get_threshold("pm10", "KSA") == 340
        assert config.get_threshold("noise_day", "KSA") == 70
    
    def test_config_validation(self):
        """Test configuration validation."""
        config = Config()
        
        # Should validate successfully in development
        if config.env == "development":
            assert config.validate() is True
    
    def test_feature_flags(self):
        """Test feature flags."""
        config = Config()
        
        assert isinstance(config.features, dict)
        assert "satellite_monitoring" in config.features
        assert "ai_predictions" in config.features
        assert all(isinstance(v, bool) for v in config.features.values())


def test_integration_screening_to_compliance():
    """Integration test: screening to compliance check."""
    from src.assessment import EIAScreening
    
    # Step 1: Screening
    screening = EIAScreening("commercial", "Dubai")
    project_data = {
        "project_size": 15000,
        "duration": 18,
        "sensitive_receptors": ["school"],
        "water_usage": 800,
    }
    
    screening_result = screening.assess(project_data)
    assert screening_result.eia_required
    
    # Step 2: Impact calculation
    calculator = ImpactCalculator()
    impact_data = {
        'materials': {'concrete': 800, 'steel': 120},
        'equipment_hours': {'excavator': 150, 'crane': 100},
        'concrete_volume': 800,
        'construction_area': 3000,
        'duration_days': 540,  # 18 months
        'num_workers': 40,
        'area_cleared': 3000,
        'habitat_type': 'urban'
    }
    
    metrics = calculator.calculate_comprehensive_impact(impact_data)
    
    # Step 3: Compliance check
    compliance = RegulatoryCompliance()
    compliance_data = {
        'project_name': 'Test Integration Project',
        'pm10_concentration': 120,
        'noise_level': 68,
        'eia_completed': screening_result.eia_required,
        'waste_management_plan': True,
        'waste_segregation': True,
        'water_conservation_plan': True,
        'water_consumption': metrics.water_consumption
    }
    
    compliance_report = compliance.check_compliance(compliance_data, Jurisdiction.DUBAI)
    
    # Verify integration
    assert screening_result.eia_required
    assert metrics.carbon_footprint > 0
    assert compliance_report.compliance_percentage > 0
    assert len(compliance_report.checks) > 0


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])