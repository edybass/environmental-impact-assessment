"""
Tests for EIA Tool
"""

import pytest
from src.assessment import EIAScreening
from src.analysis import ConstructionImpact


class TestEIAScreening:
    """Test EIA screening functionality."""

    def test_screening_small_project(self):
        """Test screening for small project."""
        screening = EIAScreening("residential", "Dubai")

        result = screening.assess({
            "project_size": 5000,
            "duration": 6,
            "sensitive_receptors": [],
            "water_usage": 100
        })

        assert not result.eia_required
        assert result.eia_level == "none"

    def test_screening_large_project(self):
        """Test screening for large project."""
        screening = EIAScreening("industrial", "Riyadh")

        result = screening.assess({
            "project_size": 50000,
            "duration": 36,
            "sensitive_receptors": ["hospital", "school"],
            "water_usage": 2000,
            "near_protected_area": True
        })

        assert result.eia_required
        assert result.eia_level == "full"
        assert len(result.specialist_studies) > 3


class TestConstructionImpact:
    """Test construction impact analysis."""

    def test_noise_assessment(self):
        """Test noise impact assessment."""
        analyzer = ConstructionImpact()

        result = analyzer.assess_noise(
            equipment=["excavator", "truck"],
            working_hours="08:00-17:00",
            nearest_receptor_distance=50,
            receptor_type="residential"
        )

        assert result.average_noise_level > 0
        assert len(result.mitigation_measures) > 0

    def test_dust_assessment(self):
        """Test dust impact assessment."""
        analyzer = ConstructionImpact()

        result = analyzer.assess_dust(
            soil_type="sandy",
            moisture_content=5,
            wind_speed=15,
            area_disturbed=1000,
            mitigation_measures=["water_spraying"]
        )

        assert result.pm10_concentration > 0
        assert result.mitigation_effectiveness > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
