"""
Construction Impact Analysis Module
Analyzes environmental impacts during construction phase
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import math


@dataclass
class NoiseResult:
    """Noise assessment results."""
    peak_noise_level: float  # dB(A)
    average_noise_level: float  # dB(A)
    exceeds_limit: bool
    affected_receptors: List[str]
    mitigation_required: bool
    mitigation_measures: List[str]


@dataclass
class DustResult:
    """Dust assessment results."""
    pm10_concentration: float  # μg/m³
    pm25_concentration: float  # μg/m³
    deposition_rate: float  # mg/m²/day
    exceeds_limit: bool
    affected_area_radius: float  # meters
    mitigation_effectiveness: float  # percentage


class ConstructionImpact:
    """Construction phase environmental impact analyzer."""

    def __init__(self):
        """Initialize impact analyzer with regional standards."""
        self.noise_limits = {
            "residential": {"day": 55, "night": 45},
            "commercial": {"day": 65, "night": 55},
            "industrial": {"day": 70, "night": 60},
            "school": {"day": 50, "night": 45},
            "hospital": {"day": 50, "night": 40}
        }

        self.dust_limits = {
            "pm10_24hr": 150,  # μg/m³ (UAE/KSA standard)
            "pm25_24hr": 75,   # μg/m³
            "pm10_annual": 50,
            "pm25_annual": 25
        }

        # Equipment noise levels (dB at 10m)
        self.equipment_noise = {
            "excavator": 85,
            "bulldozer": 85,
            "pile_driver": 95,
            "concrete_mixer": 85,
            "generator": 75,
            "compressor": 80,
            "jackhammer": 90,
            "crane": 75,
            "truck": 80,
            "concrete_pump": 82
        }

    def assess_noise(self, equipment: List[str], working_hours: str,
                    nearest_receptor_distance: float,
                    receptor_type: str = "residential",
                    barriers: bool = False) -> NoiseResult:
        """
        Assess construction noise impact.

        Args:
            equipment: List of equipment to be used
            working_hours: Working hours (e.g., "07:00-19:00")
            nearest_receptor_distance: Distance to nearest receptor in meters
            receptor_type: Type of receptor
            barriers: Whether noise barriers are installed

        Returns:
            NoiseResult object
        """
        # Calculate combined noise level
        noise_levels = []
        for eq in equipment:
            base_level = self.equipment_noise.get(eq, 80)
            # Apply distance attenuation (20*log10(d2/d1))
            attenuated = base_level - 20 * math.log10(nearest_receptor_distance / 10)
            noise_levels.append(10 ** (attenuated / 10))

        # Combine noise levels (logarithmic addition)
        combined_level = 10 * math.log10(sum(noise_levels))

        # Apply barrier reduction if present
        if barriers:
            combined_level -= 10  # Typical barrier reduction

        # Check time period
        start_hour = int(working_hours.split("-")[0].split(":")[0])
        end_hour = int(working_hours.split("-")[1].split(":")[0])
        is_daytime = 6 <= start_hour <= 22 and end_hour <= 22

        # Get applicable limit
        time_period = "day" if is_daytime else "night"
        limit = self.noise_limits[receptor_type][time_period]

        # Determine mitigation
        exceeds = combined_level > limit
        mitigation_measures = []

        if exceeds:
            mitigation_measures.extend([
                "Install temporary noise barriers",
                "Use quieter equipment where possible",
                "Restrict high-noise activities to daytime",
                "Implement equipment maintenance program"
            ])

            if combined_level > limit + 10:
                mitigation_measures.extend([
                    "Consider alternative construction methods",
                    "Provide temporary relocation for affected residents",
                    "Install double-glazing for affected buildings"
                ])

        # Identify affected receptors
        affected_receptors = []
        if nearest_receptor_distance < 50:
            affected_receptors.append("Immediate neighbors (high impact)")
        elif nearest_receptor_distance < 100:
            affected_receptors.append("Nearby residents (moderate impact)")
        elif nearest_receptor_distance < 200:
            affected_receptors.append("Local community (low impact)")

        return NoiseResult(
            peak_noise_level=combined_level + 5,  # Account for peaks
            average_noise_level=combined_level,
            exceeds_limit=exceeds,
            affected_receptors=affected_receptors,
            mitigation_required=exceeds,
            mitigation_measures=mitigation_measures
        )

    def assess_dust(self, soil_type: str, moisture_content: float,
                   wind_speed: float, area_disturbed: float,
                   mitigation_measures: List[str] = None) -> DustResult:
        """
        Assess construction dust impact.

        Args:
            soil_type: Type of soil (sandy, clay, silt)
            moisture_content: Soil moisture percentage
            wind_speed: Average wind speed in km/h
            area_disturbed: Area of disturbance in m²
            mitigation_measures: List of mitigation measures applied

        Returns:
            DustResult object
        """
        # Emission factors (kg/m²/month) - simplified
        emission_factors = {
            "sandy": 2.0,
            "silt": 1.5,
            "clay": 1.0
        }

        base_emission = emission_factors.get(soil_type, 1.5)

        # Adjust for moisture
        moisture_factor = max(0.1, 1 - moisture_content / 20)

        # Adjust for wind speed (exponential increase)
        wind_factor = 1.0
        if wind_speed > 10:
            wind_factor = 1 + (wind_speed - 10) * 0.1

        # Calculate emission rate
        emission_rate = base_emission * moisture_factor * wind_factor

        # Estimate concentrations (simplified dispersion)
        # PM10 at 50m downwind
        pm10_base = emission_rate * area_disturbed * 0.01
        pm25_base = pm10_base * 0.4  # PM2.5 is typically 40% of PM10

        # Apply mitigation effectiveness
        mitigation_effectiveness = 0
        if mitigation_measures:
            effectiveness_map = {
                "water_spraying": 0.5,
                "barriers": 0.3,
                "covering": 0.7,
                "vegetation": 0.4,
                "dust_suppressants": 0.6,
                "reduced_speed": 0.2
            }

            for measure in mitigation_measures:
                mitigation_effectiveness += effectiveness_map.get(measure, 0)

            mitigation_effectiveness = min(0.85, mitigation_effectiveness)

        # Apply mitigation
        pm10_concentration = pm10_base * (1 - mitigation_effectiveness)
        pm25_concentration = pm25_base * (1 - mitigation_effectiveness)

        # Calculate deposition rate
        deposition_rate = pm10_concentration * 0.1  # Simplified

        # Check limits
        exceeds_limit = (pm10_concentration > self.dust_limits["pm10_24hr"] or
                        pm25_concentration > self.dust_limits["pm25_24hr"])

        # Estimate affected area
        if wind_speed < 10:
            affected_radius = 100
        elif wind_speed < 20:
            affected_radius = 200
        else:
            affected_radius = 500

        return DustResult(
            pm10_concentration=pm10_concentration,
            pm25_concentration=pm25_concentration,
            deposition_rate=deposition_rate,
            exceeds_limit=exceeds_limit,
            affected_area_radius=affected_radius,
            mitigation_effectiveness=mitigation_effectiveness * 100
        )

    def assess_vibration(self, equipment: List[str], distance: float,
                        building_type: str = "residential") -> Dict:
        """Assess ground vibration from construction equipment."""
        # Vibration levels (PPV mm/s at 10m)
        vibration_sources = {
            "pile_driver": 15.0,
            "vibratory_roller": 8.0,
            "bulldozer": 3.0,
            "excavator": 2.0,
            "truck": 1.0
        }

        # Building damage criteria (PPV mm/s)
        damage_criteria = {
            "historical": 2.5,
            "residential": 5.0,
            "commercial": 10.0,
            "industrial": 15.0
        }

        max_vibration = 0
        for eq in equipment:
            base_level = vibration_sources.get(eq, 1.0)
            # Distance attenuation
            attenuated = base_level * (10 / distance) ** 1.5
            max_vibration = max(max_vibration, attenuated)

        limit = damage_criteria.get(building_type, 5.0)

        return {
            "peak_vibration": max_vibration,
            "limit": limit,
            "exceeds_limit": max_vibration > limit,
            "risk_level": "high" if max_vibration > limit else "low",
            "monitoring_required": max_vibration > limit * 0.5
        }

    def calculate_emissions(self, equipment_hours: Dict[str, float],
                           fuel_type: str = "diesel") -> Dict:
        """Calculate air emissions from construction equipment."""
        # Emission factors (g/hour)
        emission_factors = {
            "diesel": {
                "NOx": 10.0,
                "PM": 0.5,
                "SO2": 0.2,
                "CO": 3.0
            },
            "gasoline": {
                "NOx": 5.0,
                "PM": 0.2,
                "SO2": 0.1,
                "CO": 15.0
            }
        }

        factors = emission_factors.get(fuel_type, emission_factors["diesel"])
        total_emissions = {pollutant: 0 for pollutant in factors}

        # Equipment fuel consumption (L/hour) - simplified
        fuel_consumption = {
            "excavator": 15,
            "bulldozer": 20,
            "crane": 10,
            "generator": 5,
            "truck": 8
        }

        for equipment, hours in equipment_hours.items():
            consumption = fuel_consumption.get(equipment, 10)
            for pollutant, factor in factors.items():
                total_emissions[pollutant] += hours * consumption * factor / 1000  # kg

        return total_emissions

    def generate_mitigation_plan(self, noise_result: NoiseResult,
                                dust_result: DustResult) -> Dict:
        """Generate comprehensive mitigation plan."""
        plan = {
            "noise_mitigation": {
                "required": noise_result.mitigation_required,
                "measures": noise_result.mitigation_measures,
                "monitoring": "Daily noise monitoring at receptor locations",
                "complaint_procedure": "24/7 hotline for community complaints"
            },
            "dust_mitigation": {
                "required": dust_result.exceeds_limit,
                "measures": [
                    "Water spraying every 2 hours during dry conditions",
                    "Vehicle wheel washing facilities",
                    "Speed limit 20 km/h on unpaved roads",
                    "Cover stockpiles and trucks",
                    "Progressive restoration of disturbed areas"
                ],
                "monitoring": "PM10/PM2.5 monitoring at site boundary",
                "trigger_levels": {
                    "PM10_1hr": 200,  # μg/m³ - trigger enhanced mitigation
                    "visibility": 1000  # meters
                }
            },
            "general_measures": [
                "Environmental training for all workers",
                "Daily toolbox talks on environmental issues",
                "Regular equipment maintenance",
                "Spill prevention and response plan",
                "Waste segregation and recycling"
            ],
            "emergency_response": {
                "spill_response": "Spill kit locations and trained personnel",
                "dust_storm": "Cease work and secure site procedures",
                "complaint_escalation": "Immediate investigation and response"
            }
        }

        return plan


# Example usage
if __name__ == "__main__":
    analyzer = ConstructionImpact()

    # Assess noise
    noise = analyzer.assess_noise(
        equipment=["excavator", "bulldozer", "truck"],
        working_hours="07:00-19:00",
        nearest_receptor_distance=75,
        receptor_type="residential",
        barriers=True
    )

    print(f"Noise Level: {noise.average_noise_level:.1f} dB(A)")
    print(f"Exceeds Limit: {noise.exceeds_limit}")

    # Assess dust
    dust = analyzer.assess_dust(
        soil_type="sandy",
        moisture_content=5,
        wind_speed=15,
        area_disturbed=5000,
        mitigation_measures=["water_spraying", "barriers"]
    )

    print(f"\nPM10 Concentration: {dust.pm10_concentration:.1f} μg/m³")
    print(f"Mitigation Effectiveness: {dust.mitigation_effectiveness:.0f}%")
