"""
Risk Matrix Module
Environmental risk assessment and management for construction projects

Author: Edy Bassil
Email: bassileddy@gmail.com
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import logging

# Configure logging
logger = logging.getLogger(__name__)


class Likelihood(Enum):
    """Risk likelihood categories."""
    RARE = 1
    UNLIKELY = 2
    POSSIBLE = 3
    LIKELY = 4
    ALMOST_CERTAIN = 5


class Consequence(Enum):
    """Risk consequence categories."""
    INSIGNIFICANT = 1
    MINOR = 2
    MODERATE = 3
    MAJOR = 4
    CATASTROPHIC = 5


class RiskLevel(Enum):
    """Overall risk levels."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    EXTREME = "Extreme"


@dataclass
class Risk:
    """Environmental risk definition."""
    id: str
    category: str
    description: str
    likelihood: Likelihood
    consequence: Consequence
    existing_controls: List[str]
    risk_level: Optional[RiskLevel] = None
    residual_likelihood: Optional[Likelihood] = None
    residual_consequence: Optional[Consequence] = None
    residual_risk_level: Optional[RiskLevel] = None
    mitigation_measures: Optional[List[str]] = None


class RiskMatrix:
    """
    Environmental risk assessment matrix for construction projects.
    Implements AS/NZS ISO 31000:2018 risk management principles.
    """

    def __init__(self):
        """Initialize risk matrix with standard 5x5 configuration."""
        # Risk matrix mapping (likelihood x consequence)
        self.matrix = {
            (1, 1): RiskLevel.LOW,      (1, 2): RiskLevel.LOW,      (1, 3): RiskLevel.MEDIUM,   (1, 4): RiskLevel.HIGH,     (1, 5): RiskLevel.HIGH,
            (2, 1): RiskLevel.LOW,      (2, 2): RiskLevel.LOW,      (2, 3): RiskLevel.MEDIUM,   (2, 4): RiskLevel.HIGH,     (2, 5): RiskLevel.EXTREME,
            (3, 1): RiskLevel.LOW,      (3, 2): RiskLevel.MEDIUM,   (3, 3): RiskLevel.HIGH,     (3, 4): RiskLevel.EXTREME,  (3, 5): RiskLevel.EXTREME,
            (4, 1): RiskLevel.MEDIUM,   (4, 2): RiskLevel.HIGH,     (4, 3): RiskLevel.HIGH,     (4, 4): RiskLevel.EXTREME,  (4, 5): RiskLevel.EXTREME,
            (5, 1): RiskLevel.MEDIUM,   (5, 2): RiskLevel.HIGH,     (5, 3): RiskLevel.EXTREME,  (5, 4): RiskLevel.EXTREME,  (5, 5): RiskLevel.EXTREME,
        }
        
        # Standard environmental risk categories
        self.risk_categories = [
            "Air Quality",
            "Noise & Vibration",
            "Water Resources",
            "Soil & Land",
            "Biodiversity",
            "Waste Management",
            "Climate Change",
            "Community",
            "Cultural Heritage",
            "Health & Safety"
        ]
        
        # Risk register
        self.risks: List[Risk] = []

    def assess_risk(self, likelihood: Likelihood, consequence: Consequence) -> RiskLevel:
        """
        Assess risk level based on likelihood and consequence.
        
        Args:
            likelihood: Risk likelihood
            consequence: Risk consequence
            
        Returns:
            Overall risk level
        """
        return self.matrix[(likelihood.value, consequence.value)]

    def add_risk(self, risk: Risk) -> None:
        """
        Add a risk to the risk register.
        
        Args:
            risk: Risk to add
        """
        # Calculate initial risk level
        risk.risk_level = self.assess_risk(risk.likelihood, risk.consequence)
        
        # Calculate residual risk if mitigation measures provided
        if risk.mitigation_measures:
            # Assume mitigation reduces likelihood and/or consequence
            risk.residual_likelihood = risk.residual_likelihood or Likelihood(max(1, risk.likelihood.value - 1))
            risk.residual_consequence = risk.residual_consequence or risk.consequence
            risk.residual_risk_level = self.assess_risk(risk.residual_likelihood, risk.residual_consequence)
        
        self.risks.append(risk)
        logger.info(f"Added risk: {risk.id} - {risk.description} (Level: {risk.risk_level.value})")

    def get_construction_risks(self, project_type: str, location: str) -> List[Risk]:
        """
        Generate standard construction risks based on project type and location.
        
        Args:
            project_type: Type of construction project
            location: Project location (affects environmental sensitivities)
            
        Returns:
            List of identified risks
        """
        risks = []
        
        # Air Quality Risks
        risks.append(Risk(
            id="AQ001",
            category="Air Quality",
            description="Dust generation from excavation and earthworks",
            likelihood=Likelihood.LIKELY,
            consequence=Consequence.MODERATE,
            existing_controls=["Water spraying", "Site hoarding"],
            mitigation_measures=["Dust suppressants", "Real-time monitoring", "Covered stockpiles"]
        ))
        
        risks.append(Risk(
            id="AQ002",
            category="Air Quality",
            description="Equipment emissions affecting local air quality",
            likelihood=Likelihood.POSSIBLE,
            consequence=Consequence.MINOR,
            existing_controls=["Equipment maintenance"],
            mitigation_measures=["Use Tier 4 engines", "Electric equipment where possible"]
        ))
        
        # Noise Risks
        risks.append(Risk(
            id="NV001",
            category="Noise & Vibration",
            description="Construction noise disturbing nearby receptors",
            likelihood=Likelihood.LIKELY,
            consequence=Consequence.MODERATE if location in ["Dubai", "Abu Dhabi"] else Consequence.MINOR,
            existing_controls=["Working hours restrictions"],
            mitigation_measures=["Noise barriers", "Equipment enclosures", "Community liaison"]
        ))
        
        # Water Resources Risks
        risks.append(Risk(
            id="WR001",
            category="Water Resources",
            description="Groundwater contamination from spills",
            likelihood=Likelihood.UNLIKELY,
            consequence=Consequence.MAJOR,
            existing_controls=["Spill kits on site"],
            mitigation_measures=["Bunded storage", "Impermeable surfaces", "Spill response training"]
        ))
        
        risks.append(Risk(
            id="WR002",
            category="Water Resources",
            description="Excessive water consumption in water-scarce region",
            likelihood=Likelihood.POSSIBLE,
            consequence=Consequence.MODERATE,
            existing_controls=["Metered water use"],
            mitigation_measures=["Water recycling", "Greywater reuse", "Efficient fixtures"]
        ))
        
        # Biodiversity Risks
        if location in ["NEOM", "coastal"]:
            risks.append(Risk(
                id="BD001",
                category="Biodiversity",
                description="Impact on marine ecosystems",
                likelihood=Likelihood.POSSIBLE,
                consequence=Consequence.MAJOR,
                existing_controls=["Environmental surveys"],
                mitigation_measures=["Silt curtains", "Timing restrictions", "Marine monitoring"]
            ))
        
        # Waste Management Risks
        risks.append(Risk(
            id="WM001",
            category="Waste Management",
            description="Improper disposal of construction waste",
            likelihood=Likelihood.POSSIBLE,
            consequence=Consequence.MODERATE,
            existing_controls=["Waste segregation"],
            mitigation_measures=["Waste tracking system", "Recycling targets", "Authorized disposal"]
        ))
        
        # Climate Change Risks
        risks.append(Risk(
            id="CC001",
            category="Climate Change",
            description="High carbon emissions from construction activities",
            likelihood=Likelihood.LIKELY,
            consequence=Consequence.MODERATE,
            existing_controls=["Fuel monitoring"],
            mitigation_measures=["Low-carbon materials", "Renewable energy", "Carbon offsetting"]
        ))
        
        # Community Risks
        risks.append(Risk(
            id="CM001",
            category="Community",
            description="Traffic disruption affecting local community",
            likelihood=Likelihood.LIKELY,
            consequence=Consequence.MODERATE,
            existing_controls=["Traffic management plan"],
            mitigation_measures=["Alternative routes", "Off-peak deliveries", "Community notifications"]
        ))
        
        return risks

    def prioritize_risks(self, risks: Optional[List[Risk]] = None) -> List[Risk]:
        """
        Prioritize risks based on their risk level.
        
        Args:
            risks: List of risks to prioritize (uses internal register if None)
            
        Returns:
            Prioritized list of risks
        """
        risks_to_sort = risks or self.risks
        
        # Define priority order
        priority_map = {
            RiskLevel.EXTREME: 4,
            RiskLevel.HIGH: 3,
            RiskLevel.MEDIUM: 2,
            RiskLevel.LOW: 1
        }
        
        # Sort by risk level (descending) and consequence (descending)
        return sorted(
            risks_to_sort,
            key=lambda r: (priority_map[r.risk_level], r.consequence.value),
            reverse=True
        )

    def generate_risk_register(self, project_name: str) -> pd.DataFrame:
        """
        Generate risk register as a DataFrame.
        
        Args:
            project_name: Name of the project
            
        Returns:
            Risk register DataFrame
        """
        register_data = []
        
        for risk in self.risks:
            register_data.append({
                'Risk ID': risk.id,
                'Category': risk.category,
                'Description': risk.description,
                'Likelihood': risk.likelihood.name,
                'Consequence': risk.consequence.name,
                'Initial Risk Level': risk.risk_level.value,
                'Existing Controls': ', '.join(risk.existing_controls),
                'Mitigation Measures': ', '.join(risk.mitigation_measures) if risk.mitigation_measures else '',
                'Residual Likelihood': risk.residual_likelihood.name if risk.residual_likelihood else '',
                'Residual Consequence': risk.residual_consequence.name if risk.residual_consequence else '',
                'Residual Risk Level': risk.residual_risk_level.value if risk.residual_risk_level else ''
            })
        
        df = pd.DataFrame(register_data)
        df.attrs['project_name'] = project_name
        df.attrs['assessment_date'] = datetime.now().strftime('%Y-%m-%d')
        
        return df

    def generate_risk_matrix_visual(self) -> str:
        """
        Generate ASCII visualization of risk matrix.
        
        Returns:
            ASCII representation of risk matrix
        """
        visual = """
        ENVIRONMENTAL RISK MATRIX
        ========================
        
        Likelihood ↑
        
        5 | M | H | E | E | E |
        4 | M | H | H | E | E |
        3 | L | M | H | E | E |
        2 | L | L | M | H | E |
        1 | L | L | M | H | H |
          +---+---+---+---+---+
            1   2   3   4   5  → Consequence
            
        L = Low, M = Medium, H = High, E = Extreme
        """
        return visual

    def get_risk_treatment_plan(self, risk_level: RiskLevel) -> Dict[str, any]:
        """
        Get standard risk treatment plan based on risk level.
        
        Args:
            risk_level: Level of risk
            
        Returns:
            Treatment plan with actions and timeframes
        """
        treatment_plans = {
            RiskLevel.EXTREME: {
                'action': 'Immediate action required',
                'approval': 'Senior management',
                'monitoring': 'Daily',
                'review': 'Weekly',
                'documentation': 'Detailed risk assessment and treatment plan'
            },
            RiskLevel.HIGH: {
                'action': 'Urgent action required',
                'approval': 'Project manager',
                'monitoring': 'Weekly',
                'review': 'Monthly',
                'documentation': 'Risk assessment and mitigation measures'
            },
            RiskLevel.MEDIUM: {
                'action': 'Scheduled action required',
                'approval': 'Site supervisor',
                'monitoring': 'Monthly',
                'review': 'Quarterly',
                'documentation': 'Risk register entry'
            },
            RiskLevel.LOW: {
                'action': 'Monitor and review',
                'approval': 'Team leader',
                'monitoring': 'Quarterly',
                'review': 'Annually',
                'documentation': 'Standard procedures'
            }
        }
        
        return treatment_plans.get(risk_level, treatment_plans[RiskLevel.MEDIUM])

    def export_risk_summary(self) -> Dict:
        """
        Export risk assessment summary.
        
        Returns:
            Dictionary containing risk summary statistics
        """
        summary = {
            'total_risks': len(self.risks),
            'by_level': {},
            'by_category': {},
            'high_priority_risks': [],
            'assessment_date': datetime.now().isoformat()
        }
        
        # Count by risk level
        for level in RiskLevel:
            count = sum(1 for r in self.risks if r.risk_level == level)
            summary['by_level'][level.value] = count
        
        # Count by category
        for category in self.risk_categories:
            count = sum(1 for r in self.risks if r.category == category)
            if count > 0:
                summary['by_category'][category] = count
        
        # High priority risks (HIGH and EXTREME)
        high_priority = [r for r in self.risks if r.risk_level in [RiskLevel.HIGH, RiskLevel.EXTREME]]
        summary['high_priority_risks'] = [
            {
                'id': r.id,
                'description': r.description,
                'level': r.risk_level.value,
                'mitigation': r.mitigation_measures
            }
            for r in high_priority
        ]
        
        return summary


def main():
    """Example usage of RiskMatrix."""
    # Initialize risk matrix
    risk_matrix = RiskMatrix()
    
    # Generate construction risks for a Dubai project
    construction_risks = risk_matrix.get_construction_risks("commercial", "Dubai")
    
    # Add risks to register
    for risk in construction_risks:
        risk_matrix.add_risk(risk)
    
    # Add a custom risk
    custom_risk = Risk(
        id="CU001",
        category="Cultural Heritage",
        description="Potential damage to archaeological sites",
        likelihood=Likelihood.RARE,
        consequence=Consequence.CATASTROPHIC,
        existing_controls=["Pre-construction survey"],
        mitigation_measures=["Archaeological monitoring", "Chance find procedure"]
    )
    risk_matrix.add_risk(custom_risk)
    
    # Prioritize risks
    prioritized = risk_matrix.prioritize_risks()
    
    # Display results
    print("Environmental Risk Assessment")
    print("=" * 40)
    print(f"Total risks identified: {len(risk_matrix.risks)}")
    print("\nTop 5 Priority Risks:")
    for i, risk in enumerate(prioritized[:5], 1):
        print(f"{i}. [{risk.risk_level.value}] {risk.description}")
    
    # Generate risk register
    register = risk_matrix.generate_risk_register("Dubai Marina Tower")
    print(f"\nRisk register generated with {len(register)} entries")
    
    # Display risk matrix
    print(risk_matrix.generate_risk_matrix_visual())
    
    # Export summary
    summary = risk_matrix.export_risk_summary()
    print(f"\nRisk Summary:")
    print(f"- Total Risks: {summary['total_risks']}")
    print(f"- Risk Levels: {summary['by_level']}")
    print(f"- High Priority Risks: {len(summary['high_priority_risks'])}")


if __name__ == "__main__":
    main()