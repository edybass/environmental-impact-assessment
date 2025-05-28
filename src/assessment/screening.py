"""
EIA Screening Module
Initial screening to determine if full EIA is required
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
import json
from pathlib import Path


class ProjectType(Enum):
    """Project types requiring EIA."""
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"
    INFRASTRUCTURE = "infrastructure"
    ENERGY = "energy"
    TOURISM = "tourism"
    MIXED_USE = "mixed_use"


class SensitivityLevel(Enum):
    """Environmental sensitivity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ScreeningResult:
    """Results of EIA screening."""
    eia_required: bool
    eia_level: str  # "full", "limited", "none"
    key_concerns: List[str]
    regulatory_requirements: List[str]
    estimated_duration: int  # days
    specialist_studies: List[str]


class EIAScreening:
    """EIA screening tool for UAE/KSA projects."""

    def __init__(self, project_type: str, location: str):
        """
        Initialize screening tool.

        Args:
            project_type: Type of project
            location: Project location (city/emirate)
        """
        self.project_type = ProjectType(project_type)
        self.location = location
        self.thresholds = self._load_thresholds()

    def _load_thresholds(self) -> Dict:
        """Load regulatory thresholds for EIA triggers."""
        # Simplified thresholds - in production, load from database
        return {
            "area_thresholds": {  # in m²
                "residential": 10000,
                "commercial": 5000,
                "industrial": 2000,
                "infrastructure": 1000,
                "energy": 500,
                "tourism": 10000
            },
            "sensitive_distances": {  # in meters
                "protected_area": 1000,
                "water_body": 500,
                "residential_area": 100,
                "school_hospital": 200,
                "cultural_site": 500
            },
            "emission_thresholds": {
                "noise_db": 65,  # dB(A)
                "dust_pm10": 150,  # μg/m³
                "dust_pm25": 75  # μg/m³
            }
        }

    def assess(self, project_data: Dict) -> ScreeningResult:
        """
        Perform EIA screening assessment.

        Args:
            project_data: Dictionary containing project details

        Returns:
            ScreeningResult object
        """
        eia_required = False
        eia_level = "none"
        key_concerns = []
        regulatory_requirements = []
        specialist_studies = []

        # Check project size
        project_size = project_data.get("project_size", 0)
        size_threshold = self.thresholds["area_thresholds"].get(
            self.project_type.value, 10000
        )

        if project_size >= size_threshold:
            eia_required = True
            key_concerns.append(f"Project size ({project_size} m²) exceeds threshold")

        # Check sensitive receptors
        sensitive_receptors = project_data.get("sensitive_receptors", [])
        if sensitive_receptors:
            eia_required = True
            key_concerns.extend([
                f"Near sensitive receptor: {receptor}" 
                for receptor in sensitive_receptors
            ])
            specialist_studies.append("Noise and Air Quality Study")

        # Check water usage (critical in Gulf region)
        water_usage = project_data.get("water_usage", 0)
        if water_usage > 500:  # m³/day
            key_concerns.append(f"High water usage: {water_usage} m³/day")
            specialist_studies.append("Water Resources Assessment")

        # Location-specific requirements
        if self.location in ["Dubai", "Abu Dhabi"]:
            regulatory_requirements.append("EAD/DM Environmental Permit")
        elif self.location in ["Riyadh", "Jeddah", "Dammam"]:
            regulatory_requirements.append("NCEC Environmental License")

        # Protected areas check
        if project_data.get("near_protected_area", False):
            eia_required = True
            eia_level = "full"
            key_concerns.append("Located near protected area")
            specialist_studies.extend([
                "Ecological Impact Assessment",
                "Habitat Compensation Plan"
            ])

        # Determine EIA level
        if eia_required:
            if len(key_concerns) > 3 or "protected area" in str(key_concerns):
                eia_level = "full"
                estimated_duration = 90
            else:
                eia_level = "limited"
                estimated_duration = 45
        else:
            estimated_duration = 0

        # Industrial projects always need air quality
        if self.project_type == ProjectType.INDUSTRIAL:
            specialist_studies.append("Air Dispersion Modeling")
            specialist_studies.append("Hazardous Materials Assessment")

        # Construction phase assessment
        if project_data.get("duration", 0) > 12:  # months
            key_concerns.append("Long construction duration")
            specialist_studies.append("Construction Environmental Management Plan")

        return ScreeningResult(
            eia_required=eia_required,
            eia_level=eia_level,
            key_concerns=key_concerns,
            regulatory_requirements=list(set(regulatory_requirements)),
            estimated_duration=estimated_duration,
            specialist_studies=list(set(specialist_studies))
        )

    def check_regulatory_requirements(self) -> List[str]:
        """Check specific regulatory requirements by location."""
        requirements = []

        # UAE Requirements
        if self.location in ["Dubai", "Abu Dhabi", "Sharjah", "UAE"]:
            requirements.extend([
                "UAE Federal Law No. 24 Compliance",
                "Environmental Permit from Competent Authority",
                "No Objection Certificate (NOC)"
            ])

            if self.location == "Abu Dhabi":
                requirements.append("EAD CEMP Approval")
            elif self.location == "Dubai":
                requirements.append("DM Environmental Section Approval")

        # KSA Requirements
        elif self.location in ["Riyadh", "Jeddah", "Dammam", "NEOM", "KSA"]:
            requirements.extend([
                "NCEC Environmental License",
                "Environmental Compliance Certificate",
                "Environmental Monitoring Plan"
            ])

            if self.project_type == ProjectType.INDUSTRIAL:
                requirements.append("Industrial Environmental Permit")

        return requirements

    def generate_screening_report(self, result: ScreeningResult, 
                                filename: str = "screening_report.json") -> Dict:
        """Generate screening report."""
        report = {
            "project_info": {
                "type": self.project_type.value,
                "location": self.location,
                "screening_date": datetime.now().isoformat()
            },
            "screening_result": {
                "eia_required": result.eia_required,
                "eia_level": result.eia_level,
                "estimated_duration_days": result.estimated_duration
            },
            "findings": {
                "key_concerns": result.key_concerns,
                "regulatory_requirements": result.regulatory_requirements,
                "specialist_studies": result.specialist_studies
            },
            "next_steps": self._get_next_steps(result)
        }

        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)

        return report

    def _get_next_steps(self, result: ScreeningResult) -> List[str]:
        """Get recommended next steps based on screening."""
        steps = []

        if result.eia_required:
            steps.extend([
                "Appoint qualified EIA consultant",
                "Prepare Terms of Reference (ToR)",
                "Conduct baseline environmental surveys",
                "Initiate stakeholder consultation"
            ])

            if result.eia_level == "full":
                steps.append("Schedule scoping meeting with authorities")

            for study in result.specialist_studies:
                steps.append(f"Commission {study}")
        else:
            steps.extend([
                "Prepare Environmental Management Plan",
                "Submit environmental registration",
                "Implement good construction practices"
            ])

        return steps


# Example usage
if __name__ == "__main__":
    # Screen a construction project in Dubai
    screening = EIAScreening("commercial", "Dubai")

    project_data = {
        "project_size": 15000,  # m²
        "duration": 18,  # months
        "sensitive_receptors": ["school", "residential_area"],
        "water_usage": 800,  # m³/day
        "near_protected_area": False
    }

    result = screening.assess(project_data)

    print(f"EIA Required: {result.eia_required}")
    print(f"EIA Level: {result.eia_level}")
    print(f"Key Concerns: {', '.join(result.key_concerns)}")
    print(f"Studies Needed: {', '.join(result.specialist_studies)}")

    # Generate report
    report = screening.generate_screening_report(result)
