"""
Impact Calculator Module
Comprehensive environmental impact calculations for construction projects

Author: Edy Bassil
Email: bassileddy@gmail.com
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
import logging

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class ImpactMetrics:
    """Container for environmental impact metrics."""
    carbon_footprint: float  # tonnes CO2e
    water_consumption: float  # m³
    waste_generation: float  # tonnes
    energy_usage: float  # MWh
    land_disturbance: float  # m²
    biodiversity_score: float  # 0-100 scale


class ImpactCalculator:
    """
    Advanced environmental impact calculator for construction projects.
    Implements various calculation methodologies for different impact categories.
    """

    def __init__(self):
        """Initialize the impact calculator with default emission factors."""
        self.emission_factors = {
            # Construction materials (kg CO2e per unit)
            'concrete': 410,  # per m³
            'steel': 1850,  # per tonne
            'cement': 900,  # per tonne
            'asphalt': 140,  # per tonne
            'timber': -1600,  # per m³ (carbon negative)
            'aluminum': 11890,  # per tonne
            'glass': 1200,  # per tonne
            'bricks': 240,  # per 1000 units
        }
        
        self.equipment_emissions = {
            # Equipment emissions (kg CO2e per hour)
            'excavator': 25.5,
            'bulldozer': 30.2,
            'crane': 18.7,
            'concrete_mixer': 15.3,
            'generator': 12.8,
            'truck': 22.4,
            'compressor': 8.5,
        }
        
        self.water_factors = {
            # Water consumption factors (L per unit)
            'concrete_mixing': 150,  # per m³
            'dust_suppression': 2.5,  # per m² per day
            'equipment_washing': 200,  # per equipment per day
            'worker_facilities': 50,  # per worker per day
        }

    def calculate_carbon_footprint(self, 
                                 materials: Dict[str, float],
                                 equipment_hours: Dict[str, float],
                                 transport_km: float = 0) -> float:
        """
        Calculate total carbon footprint of construction project.
        
        Args:
            materials: Dictionary of material quantities
            equipment_hours: Dictionary of equipment usage hours
            transport_km: Total transport distance for materials
            
        Returns:
            Total carbon footprint in tonnes CO2e
        """
        # Material emissions
        material_emissions = sum(
            self.emission_factors.get(material, 0) * quantity
            for material, quantity in materials.items()
        )
        
        # Equipment emissions
        equipment_emissions = sum(
            self.equipment_emissions.get(equipment, 0) * hours
            for equipment, hours in equipment_hours.items()
        )
        
        # Transport emissions (assuming 0.1 kg CO2e per tonne-km)
        transport_emissions = transport_km * 0.1 * sum(materials.values())
        
        total_emissions = (material_emissions + equipment_emissions + transport_emissions) / 1000
        
        logger.info(f"Calculated carbon footprint: {total_emissions:.2f} tonnes CO2e")
        return total_emissions

    def calculate_water_consumption(self,
                                  concrete_volume: float,
                                  construction_area: float,
                                  duration_days: int,
                                  num_workers: int) -> float:
        """
        Calculate total water consumption during construction.
        
        Args:
            concrete_volume: Total concrete volume in m³
            construction_area: Construction area in m²
            duration_days: Construction duration in days
            num_workers: Average number of workers on site
            
        Returns:
            Total water consumption in m³
        """
        concrete_water = concrete_volume * self.water_factors['concrete_mixing']
        dust_water = construction_area * duration_days * self.water_factors['dust_suppression']
        equipment_water = 10 * duration_days * self.water_factors['equipment_washing']  # Assume 10 equipment
        worker_water = num_workers * duration_days * self.water_factors['worker_facilities']
        
        total_water = (concrete_water + dust_water + equipment_water + worker_water) / 1000
        
        logger.info(f"Calculated water consumption: {total_water:.2f} m³")
        return total_water

    def calculate_waste_generation(self,
                                 materials: Dict[str, float],
                                 waste_factors: Optional[Dict[str, float]] = None) -> float:
        """
        Calculate construction waste generation.
        
        Args:
            materials: Dictionary of material quantities
            waste_factors: Custom waste generation factors (optional)
            
        Returns:
            Total waste generation in tonnes
        """
        if waste_factors is None:
            waste_factors = {
                'concrete': 0.05,  # 5% waste
                'steel': 0.02,     # 2% waste
                'timber': 0.10,    # 10% waste
                'general': 0.07,   # 7% average waste
            }
        
        total_waste = sum(
            quantity * waste_factors.get(material, waste_factors['general'])
            for material, quantity in materials.items()
        )
        
        logger.info(f"Calculated waste generation: {total_waste:.2f} tonnes")
        return total_waste

    def calculate_energy_usage(self,
                             equipment_hours: Dict[str, float],
                             facility_area: float = 0,
                             duration_days: int = 0) -> float:
        """
        Calculate total energy usage during construction.
        
        Args:
            equipment_hours: Dictionary of equipment usage hours
            facility_area: Temporary facility area in m²
            duration_days: Construction duration in days
            
        Returns:
            Total energy usage in MWh
        """
        # Equipment energy (assuming average 50 kW per equipment)
        equipment_energy = sum(equipment_hours.values()) * 50 / 1000
        
        # Facility energy (lighting, HVAC, etc.) - 100 W/m² for 12 hours/day
        facility_energy = facility_area * 0.1 * 12 * duration_days / 1000
        
        total_energy = equipment_energy + facility_energy
        
        logger.info(f"Calculated energy usage: {total_energy:.2f} MWh")
        return total_energy

    def calculate_biodiversity_impact(self,
                                    area_cleared: float,
                                    habitat_type: str,
                                    mitigation_measures: List[str] = None) -> float:
        """
        Calculate biodiversity impact score.
        
        Args:
            area_cleared: Area of habitat cleared in m²
            habitat_type: Type of habitat affected
            mitigation_measures: List of mitigation measures implemented
            
        Returns:
            Biodiversity score (0-100, higher is better)
        """
        # Base impact scores by habitat type
        habitat_impacts = {
            'desert': 20,
            'urban': 10,
            'agricultural': 30,
            'coastal': 50,
            'wetland': 70,
            'forest': 80,
        }
        
        base_impact = habitat_impacts.get(habitat_type, 40)
        
        # Area factor (larger areas have more impact)
        area_factor = min(1.0, area_cleared / 10000)  # Normalize to 1 hectare
        
        # Mitigation effectiveness
        mitigation_score = 0
        if mitigation_measures:
            mitigation_effects = {
                'habitat_restoration': 0.3,
                'wildlife_corridors': 0.2,
                'transplantation': 0.15,
                'timing_restrictions': 0.1,
                'noise_barriers': 0.05,
            }
            mitigation_score = sum(
                mitigation_effects.get(measure, 0.05)
                for measure in mitigation_measures
            )
        
        # Calculate final score (100 = no impact, 0 = maximum impact)
        impact_score = 100 - (base_impact * area_factor * (1 - min(0.7, mitigation_score)))
        
        logger.info(f"Calculated biodiversity score: {impact_score:.1f}")
        return impact_score

    def calculate_comprehensive_impact(self,
                                     project_data: Dict) -> ImpactMetrics:
        """
        Calculate comprehensive environmental impact metrics.
        
        Args:
            project_data: Dictionary containing all project parameters
            
        Returns:
            ImpactMetrics object with all calculated impacts
        """
        # Extract data
        materials = project_data.get('materials', {})
        equipment_hours = project_data.get('equipment_hours', {})
        
        # Calculate individual impacts
        carbon = self.calculate_carbon_footprint(
            materials, 
            equipment_hours,
            project_data.get('transport_km', 0)
        )
        
        water = self.calculate_water_consumption(
            project_data.get('concrete_volume', 0),
            project_data.get('construction_area', 0),
            project_data.get('duration_days', 0),
            project_data.get('num_workers', 0)
        )
        
        waste = self.calculate_waste_generation(materials)
        
        energy = self.calculate_energy_usage(
            equipment_hours,
            project_data.get('facility_area', 0),
            project_data.get('duration_days', 0)
        )
        
        biodiversity = self.calculate_biodiversity_impact(
            project_data.get('area_cleared', 0),
            project_data.get('habitat_type', 'urban'),
            project_data.get('mitigation_measures', [])
        )
        
        return ImpactMetrics(
            carbon_footprint=carbon,
            water_consumption=water,
            waste_generation=waste,
            energy_usage=energy,
            land_disturbance=project_data.get('area_cleared', 0),
            biodiversity_score=biodiversity
        )

    def generate_impact_summary(self, metrics: ImpactMetrics) -> Dict:
        """
        Generate a summary report of environmental impacts.
        
        Args:
            metrics: Calculated impact metrics
            
        Returns:
            Dictionary containing impact summary and recommendations
        """
        summary = {
            'timestamp': datetime.now().isoformat(),
            'impacts': {
                'carbon_footprint': {
                    'value': metrics.carbon_footprint,
                    'unit': 'tonnes CO2e',
                    'severity': self._assess_severity(metrics.carbon_footprint, 'carbon')
                },
                'water_consumption': {
                    'value': metrics.water_consumption,
                    'unit': 'm³',
                    'severity': self._assess_severity(metrics.water_consumption, 'water')
                },
                'waste_generation': {
                    'value': metrics.waste_generation,
                    'unit': 'tonnes',
                    'severity': self._assess_severity(metrics.waste_generation, 'waste')
                },
                'energy_usage': {
                    'value': metrics.energy_usage,
                    'unit': 'MWh',
                    'severity': self._assess_severity(metrics.energy_usage, 'energy')
                },
                'biodiversity_score': {
                    'value': metrics.biodiversity_score,
                    'unit': 'score',
                    'severity': 'low' if metrics.biodiversity_score > 70 else 'medium' if metrics.biodiversity_score > 40 else 'high'
                }
            },
            'recommendations': self._generate_recommendations(metrics)
        }
        
        return summary

    def _assess_severity(self, value: float, impact_type: str) -> str:
        """Assess severity level of an impact."""
        thresholds = {
            'carbon': {'low': 100, 'medium': 500},
            'water': {'low': 1000, 'medium': 5000},
            'waste': {'low': 50, 'medium': 200},
            'energy': {'low': 100, 'medium': 500}
        }
        
        limits = thresholds.get(impact_type, {'low': 100, 'medium': 500})
        
        if value < limits['low']:
            return 'low'
        elif value < limits['medium']:
            return 'medium'
        else:
            return 'high'

    def _generate_recommendations(self, metrics: ImpactMetrics) -> List[str]:
        """Generate recommendations based on impact metrics."""
        recommendations = []
        
        if metrics.carbon_footprint > 500:
            recommendations.append("Consider using low-carbon concrete alternatives")
            recommendations.append("Optimize equipment usage to reduce idle time")
        
        if metrics.water_consumption > 5000:
            recommendations.append("Implement water recycling system for concrete mixing")
            recommendations.append("Use dust suppressants instead of water spraying")
        
        if metrics.waste_generation > 200:
            recommendations.append("Implement waste segregation at source")
            recommendations.append("Partner with recycling facilities for construction waste")
        
        if metrics.biodiversity_score < 50:
            recommendations.append("Develop and implement a Biodiversity Action Plan")
            recommendations.append("Consider habitat restoration post-construction")
        
        return recommendations


def main():
    """Example usage of the ImpactCalculator."""
    calculator = ImpactCalculator()
    
    # Example project data
    project_data = {
        'materials': {
            'concrete': 1000,  # m³
            'steel': 150,      # tonnes
            'cement': 200,     # tonnes
        },
        'equipment_hours': {
            'excavator': 200,
            'crane': 150,
            'concrete_mixer': 100,
        },
        'transport_km': 500,
        'concrete_volume': 1000,
        'construction_area': 5000,
        'duration_days': 180,
        'num_workers': 50,
        'facility_area': 500,
        'area_cleared': 8000,
        'habitat_type': 'desert',
        'mitigation_measures': ['habitat_restoration', 'timing_restrictions']
    }
    
    # Calculate impacts
    metrics = calculator.calculate_comprehensive_impact(project_data)
    summary = calculator.generate_impact_summary(metrics)
    
    # Display results
    print("Environmental Impact Assessment Results")
    print("=" * 40)
    for impact, details in summary['impacts'].items():
        print(f"{impact}: {details['value']:.2f} {details['unit']} (Severity: {details['severity']})")
    
    print("\nRecommendations:")
    for rec in summary['recommendations']:
        print(f"- {rec}")


if __name__ == "__main__":
    main()