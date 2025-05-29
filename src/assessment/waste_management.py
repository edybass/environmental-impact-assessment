"""
Comprehensive Waste Management Assessment Module
Professional waste assessment for construction and operational phases

Created by: Edy Bassil
Email: bassileddy@gmail.com
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import math

class WasteCategory(Enum):
    """Waste categories according to UAE/KSA regulations"""
    MUNICIPAL_SOLID = "municipal_solid"
    CONSTRUCTION_DEMOLITION = "construction_demolition"
    HAZARDOUS = "hazardous"
    INDUSTRIAL = "industrial"
    MEDICAL = "medical"
    ELECTRONIC = "electronic"

@dataclass
class WasteStream:
    """Individual waste stream data"""
    category: WasteCategory
    type: str
    generation_rate: float  # kg/unit/day
    unit: str  # m², person, etc.
    recyclable_percentage: float
    hazardous: bool
    disposal_method: str
    treatment_required: bool

@dataclass
class WasteManagementPlan:
    """Complete waste management plan"""
    total_generation: Dict[str, float]
    recycling_rate: float
    disposal_facilities: List[Dict]
    mitigation_measures: List[str]
    cost_estimate: float
    compliance_status: str

class WasteManagementAssessment:
    """Comprehensive waste management assessment for EIA"""
    
    def __init__(self):
        self.waste_streams = self._initialize_waste_streams()
        self.disposal_facilities = self._initialize_disposal_facilities()
        self.recycling_rates = self._initialize_recycling_rates()
    
    def _initialize_waste_streams(self) -> Dict[str, WasteStream]:
        """Initialize standard waste streams for different project types"""
        return {
            # Construction & Demolition Waste
            "concrete_waste": WasteStream(
                category=WasteCategory.CONSTRUCTION_DEMOLITION,
                type="Concrete and masonry",
                generation_rate=85.0,  # kg/m² of construction
                unit="m²",
                recyclable_percentage=0.85,
                hazardous=False,
                disposal_method="recycling_facility",
                treatment_required=False
            ),
            "steel_waste": WasteStream(
                category=WasteCategory.CONSTRUCTION_DEMOLITION,
                type="Steel and metal",
                generation_rate=12.5,  # kg/m²
                unit="m²",
                recyclable_percentage=0.95,
                hazardous=False,
                disposal_method="metal_recycling",
                treatment_required=False
            ),
            "wood_waste": WasteStream(
                category=WasteCategory.CONSTRUCTION_DEMOLITION,
                type="Wood and timber",
                generation_rate=8.3,  # kg/m²
                unit="m²",
                recyclable_percentage=0.70,
                hazardous=False,
                disposal_method="biomass_facility",
                treatment_required=False
            ),
            "excavated_soil": WasteStream(
                category=WasteCategory.CONSTRUCTION_DEMOLITION,
                type="Excavated soil and rock",
                generation_rate=150.0,  # kg/m² for basement levels
                unit="m²_basement",
                recyclable_percentage=0.60,
                hazardous=False,
                disposal_method="land_reclamation",
                treatment_required=True  # Testing required
            ),
            "construction_mixed": WasteStream(
                category=WasteCategory.CONSTRUCTION_DEMOLITION,
                type="Mixed construction waste",
                generation_rate=25.0,  # kg/m²
                unit="m²",
                recyclable_percentage=0.45,
                hazardous=False,
                disposal_method="sorting_facility",
                treatment_required=False
            ),
            
            # Operational Waste
            "municipal_solid": WasteStream(
                category=WasteCategory.MUNICIPAL_SOLID,
                type="Municipal solid waste",
                generation_rate=1.2,  # kg/person/day (UAE average)
                unit="person",
                recyclable_percentage=0.30,
                hazardous=False,
                disposal_method="municipal_landfill",
                treatment_required=False
            ),
            "organic_waste": WasteStream(
                category=WasteCategory.MUNICIPAL_SOLID,
                type="Organic/food waste",
                generation_rate=0.5,  # kg/person/day
                unit="person",
                recyclable_percentage=0.90,  # Composting
                hazardous=False,
                disposal_method="composting_facility",
                treatment_required=False
            ),
            "plastic_waste": WasteStream(
                category=WasteCategory.MUNICIPAL_SOLID,
                type="Plastic waste",
                generation_rate=0.2,  # kg/person/day
                unit="person",
                recyclable_percentage=0.75,
                hazardous=False,
                disposal_method="plastic_recycling",
                treatment_required=False
            ),
            
            # Hazardous Waste
            "hazardous_chemicals": WasteStream(
                category=WasteCategory.HAZARDOUS,
                type="Hazardous chemicals",
                generation_rate=0.05,  # kg/m²/year
                unit="m²",
                recyclable_percentage=0.10,
                hazardous=True,
                disposal_method="hazardous_facility",
                treatment_required=True
            ),
            "electronic_waste": WasteStream(
                category=WasteCategory.ELECTRONIC,
                type="Electronic waste",
                generation_rate=0.02,  # kg/person/day
                unit="person",
                recyclable_percentage=0.80,
                hazardous=True,
                disposal_method="e_waste_facility",
                treatment_required=True
            )
        }
    
    def _initialize_disposal_facilities(self) -> Dict[str, Dict]:
        """Initialize disposal facilities database for UAE/KSA"""
        return {
            "uae_facilities": {
                "bee_ah_sharjah": {
                    "name": "Bee'ah Waste-to-Energy Facility",
                    "location": "Sharjah",
                    "capacity": 1000000,  # tons/year
                    "waste_types": ["municipal_solid", "construction_mixed"],
                    "distance_dubai": 45,  # km
                    "cost_per_ton": 120,  # AED
                    "environmental_rating": "A+"
                },
                "emirates_environmental": {
                    "name": "Emirates Environmental Technologies",
                    "location": "Dubai",
                    "capacity": 500000,
                    "waste_types": ["construction_demolition", "hazardous"],
                    "distance_dubai": 25,
                    "cost_per_ton": 150,
                    "environmental_rating": "A"
                },
                "dulsco_landfill": {
                    "name": "DULSCO Landfill",
                    "location": "Al Qusais, Dubai",
                    "capacity": 800000,
                    "waste_types": ["municipal_solid", "construction_mixed"],
                    "distance_dubai": 15,
                    "cost_per_ton": 80,
                    "environmental_rating": "B+"
                }
            },
            "ksa_facilities": {
                "madinah_wte": {
                    "name": "Madinah Waste-to-Energy Plant",
                    "location": "Madinah",
                    "capacity": 300000,
                    "waste_types": ["municipal_solid"],
                    "distance_riyadh": 420,
                    "cost_per_ton": 100,
                    "environmental_rating": "A"
                },
                "riyadh_landfill": {
                    "name": "Riyadh Municipality Landfill",
                    "location": "Riyadh",
                    "capacity": 600000,
                    "waste_types": ["municipal_solid", "construction_mixed"],
                    "distance_riyadh": 35,
                    "cost_per_ton": 70,
                    "environmental_rating": "B"
                }
            }
        }
    
    def _initialize_recycling_rates(self) -> Dict[str, float]:
        """Regional recycling rates and targets"""
        return {
            "uae_current": {
                "construction_demolition": 0.65,
                "municipal_solid": 0.30,
                "plastic": 0.25,
                "metal": 0.85,
                "paper": 0.40
            },
            "uae_target_2030": {
                "construction_demolition": 0.85,
                "municipal_solid": 0.75,
                "plastic": 0.70,
                "metal": 0.95,
                "paper": 0.80
            },
            "ksa_current": {
                "construction_demolition": 0.45,
                "municipal_solid": 0.15,
                "plastic": 0.20,
                "metal": 0.70,
                "paper": 0.25
            },
            "ksa_target_2030": {
                "construction_demolition": 0.70,
                "municipal_solid": 0.60,
                "plastic": 0.50,
                "metal": 0.90,
                "paper": 0.65
            }
        }
    
    def assess_construction_waste(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess construction phase waste generation"""
        
        project_size = float(project_data.get('size', 10000))  # m²
        project_type = project_data.get('type', 'residential').lower()
        location = project_data.get('location', 'Dubai').lower()
        duration = int(project_data.get('duration', 24))  # months
        
        # Calculate basement area if applicable
        basement_area = 0
        if project_type in ['commercial', 'mixed_use', 'industrial']:
            basement_area = project_size * 0.8  # Assume 80% has basement
        elif project_type == 'residential':
            basement_area = project_size * 0.3  # 30% has basement
        
        # Calculate waste generation
        waste_generation = {}
        total_weight = 0
        
        # Construction waste streams
        construction_streams = [
            'concrete_waste', 'steel_waste', 'wood_waste', 
            'construction_mixed'
        ]
        
        for stream_id in construction_streams:
            stream = self.waste_streams[stream_id]
            if stream.unit == "m²":
                volume = project_size
            elif stream.unit == "m²_basement":
                volume = basement_area
            else:
                volume = project_size
            
            total_waste = stream.generation_rate * volume
            recyclable = total_waste * stream.recyclable_percentage
            disposal = total_waste - recyclable
            
            waste_generation[stream_id] = {
                'type': stream.type,
                'total_generation': total_waste,
                'recyclable': recyclable,
                'disposal': disposal,
                'generation_rate': stream.generation_rate,
                'hazardous': stream.hazardous
            }
            
            total_weight += total_waste
        
        # Add excavated soil if basement exists
        if basement_area > 0:
            stream = self.waste_streams['excavated_soil']
            total_soil = stream.generation_rate * basement_area
            reusable_soil = total_soil * stream.recyclable_percentage
            disposal_soil = total_soil - reusable_soil
            
            waste_generation['excavated_soil'] = {
                'type': stream.type,
                'total_generation': total_soil,
                'recyclable': reusable_soil,
                'disposal': disposal_soil,
                'generation_rate': stream.generation_rate,
                'hazardous': stream.hazardous,
                'testing_required': True
            }
            
            total_weight += total_soil
        
        # Calculate recycling potential
        total_recyclable = sum(w['recyclable'] for w in waste_generation.values())
        recycling_rate = total_recyclable / total_weight if total_weight > 0 else 0
        
        # Estimate costs
        disposal_cost = self._calculate_disposal_costs(waste_generation, location)
        
        return {
            'phase': 'construction',
            'total_weight': round(total_weight, 1),
            'total_recyclable': round(total_recyclable, 1),
            'recycling_rate': round(recycling_rate * 100, 1),
            'waste_streams': waste_generation,
            'disposal_cost': disposal_cost,
            'duration_months': duration,
            'daily_average': round(total_weight / (duration * 30), 1),
            'compliance_requirements': self._get_construction_compliance(location)
        }
    
    def assess_operational_waste(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess operational phase waste generation"""
        
        project_size = float(project_data.get('size', 10000))
        project_type = project_data.get('type', 'residential').lower()
        location = project_data.get('location', 'Dubai').lower()
        
        # Estimate occupancy
        occupancy = self._calculate_occupancy(project_size, project_type)
        
        # Calculate operational waste
        waste_generation = {}
        total_daily = 0
        
        operational_streams = [
            'municipal_solid', 'organic_waste', 'plastic_waste'
        ]
        
        for stream_id in operational_streams:
            stream = self.waste_streams[stream_id]
            if stream.unit == "person":
                daily_generation = stream.generation_rate * occupancy
            else:
                daily_generation = stream.generation_rate * project_size / 365
            
            annual_generation = daily_generation * 365
            recyclable = annual_generation * stream.recyclable_percentage
            disposal = annual_generation - recyclable
            
            waste_generation[stream_id] = {
                'type': stream.type,
                'daily_generation': round(daily_generation, 2),
                'annual_generation': round(annual_generation, 1),
                'recyclable': round(recyclable, 1),
                'disposal': round(disposal, 1),
                'hazardous': stream.hazardous
            }
            
            total_daily += daily_generation
        
        # Add project-specific waste
        if project_type in ['industrial', 'commercial']:
            # Add electronic waste
            stream = self.waste_streams['electronic_waste']
            e_waste_daily = stream.generation_rate * occupancy
            e_waste_annual = e_waste_daily * 365
            
            waste_generation['electronic_waste'] = {
                'type': stream.type,
                'daily_generation': round(e_waste_daily, 3),
                'annual_generation': round(e_waste_annual, 1),
                'recyclable': round(e_waste_annual * stream.recyclable_percentage, 1),
                'disposal': round(e_waste_annual * (1 - stream.recyclable_percentage), 1),
                'hazardous': stream.hazardous,
                'special_handling': True
            }
            
            total_daily += e_waste_daily
        
        # Calculate annual totals
        annual_total = total_daily * 365
        annual_recyclable = sum(w['recyclable'] for w in waste_generation.values())
        recycling_rate = annual_recyclable / annual_total if annual_total > 0 else 0
        
        # Estimate costs
        annual_disposal_cost = self._calculate_operational_disposal_costs(
            waste_generation, location
        )
        
        return {
            'phase': 'operational',
            'occupancy': occupancy,
            'daily_total': round(total_daily, 1),
            'annual_total': round(annual_total, 1),
            'annual_recyclable': round(annual_recyclable, 1),
            'recycling_rate': round(recycling_rate * 100, 1),
            'waste_streams': waste_generation,
            'annual_disposal_cost': annual_disposal_cost,
            'per_capita_generation': round(total_daily / occupancy, 2) if occupancy > 0 else 0,
            'compliance_requirements': self._get_operational_compliance(location)
        }
    
    def create_waste_management_plan(self, project_data: Dict[str, Any]) -> WasteManagementPlan:
        """Create comprehensive waste management plan"""
        
        construction_assessment = self.assess_construction_waste(project_data)
        operational_assessment = self.assess_operational_waste(project_data)
        location = project_data.get('location', 'Dubai').lower()
        
        # Combine assessments
        total_generation = {
            'construction_phase': construction_assessment['total_weight'],
            'operational_annual': operational_assessment['annual_total'],
            'construction_duration': construction_assessment['duration_months']
        }
        
        # Calculate overall recycling rate
        const_recyclable = construction_assessment['total_recyclable']
        const_total = construction_assessment['total_weight']
        op_recyclable = operational_assessment['annual_recyclable']
        op_total = operational_assessment['annual_total']
        
        # Weight by significance (construction is one-time, operations ongoing)
        overall_recycling = (const_recyclable + op_recyclable * 5) / (const_total + op_total * 5)
        
        # Identify suitable disposal facilities
        disposal_facilities = self._recommend_disposal_facilities(location, {
            **construction_assessment['waste_streams'],
            **operational_assessment['waste_streams']
        })
        
        # Develop mitigation measures
        mitigation_measures = self._develop_mitigation_measures(
            construction_assessment, operational_assessment
        )
        
        # Estimate total costs
        construction_cost = construction_assessment['disposal_cost']
        operational_cost = operational_assessment['annual_disposal_cost']
        total_cost = construction_cost + (operational_cost * 20)  # 20-year lifecycle
        
        # Determine compliance status
        compliance_status = self._assess_waste_compliance(
            construction_assessment, operational_assessment, location
        )
        
        return WasteManagementPlan(
            total_generation=total_generation,
            recycling_rate=round(overall_recycling * 100, 1),
            disposal_facilities=disposal_facilities,
            mitigation_measures=mitigation_measures,
            cost_estimate=total_cost,
            compliance_status=compliance_status
        )
    
    def _calculate_occupancy(self, project_size: float, project_type: str) -> int:
        """Calculate project occupancy based on type and size"""
        occupancy_rates = {
            'residential': 30,      # m²/person
            'commercial': 15,       # m²/person
            'industrial': 50,       # m²/person
            'infrastructure': 100,  # m²/person
            'mixed_use': 25        # m²/person
        }
        
        rate = occupancy_rates.get(project_type, 30)
        return max(int(project_size / rate), 10)
    
    def _calculate_disposal_costs(self, waste_streams: Dict, location: str) -> float:
        """Calculate construction waste disposal costs"""
        location_key = 'uae_facilities' if 'uae' in location or any(
            city in location for city in ['dubai', 'abu dhabi', 'sharjah']
        ) else 'ksa_facilities'
        
        facilities = self.disposal_facilities[location_key]
        total_cost = 0
        
        for stream_data in waste_streams.values():
            disposal_weight = stream_data['disposal'] / 1000  # Convert to tons
            # Use average facility cost
            avg_cost = sum(f['cost_per_ton'] for f in facilities.values()) / len(facilities)
            total_cost += disposal_weight * avg_cost
        
        return round(total_cost, 0)
    
    def _calculate_operational_disposal_costs(self, waste_streams: Dict, location: str) -> float:
        """Calculate annual operational waste disposal costs"""
        location_key = 'uae_facilities' if 'uae' in location or any(
            city in location for city in ['dubai', 'abu dhabi', 'sharjah']
        ) else 'ksa_facilities'
        
        facilities = self.disposal_facilities[location_key]
        annual_cost = 0
        
        for stream_data in waste_streams.values():
            disposal_weight = stream_data['disposal'] / 1000  # Convert to tons
            # Use average facility cost
            avg_cost = sum(f['cost_per_ton'] for f in facilities.values()) / len(facilities)
            annual_cost += disposal_weight * avg_cost
        
        return round(annual_cost, 0)
    
    def _recommend_disposal_facilities(self, location: str, waste_streams: Dict) -> List[Dict]:
        """Recommend appropriate disposal facilities"""
        location_key = 'uae_facilities' if 'uae' in location or any(
            city in location for city in ['dubai', 'abu dhabi', 'sharjah']
        ) else 'ksa_facilities'
        
        facilities = self.disposal_facilities[location_key]
        recommendations = []
        
        for facility_id, facility in facilities.items():
            # Check if facility handles required waste types
            applicable_streams = []
            for stream_id, stream_data in waste_streams.items():
                if any(wt in stream_id for wt in facility['waste_types']):
                    applicable_streams.append(stream_data['type'])
            
            if applicable_streams:
                recommendations.append({
                    'facility_name': facility['name'],
                    'location': facility['location'],
                    'applicable_waste_types': applicable_streams,
                    'capacity': facility['capacity'],
                    'cost_per_ton': facility['cost_per_ton'],
                    'environmental_rating': facility['environmental_rating'],
                    'recommended': len(applicable_streams) > 2
                })
        
        return recommendations
    
    def _develop_mitigation_measures(self, construction: Dict, operational: Dict) -> List[str]:
        """Develop waste minimization and management measures"""
        measures = [
            "Implement waste segregation at source",
            "Establish recycling targets: Construction (70%), Operations (50%)",
            "Conduct waste audits quarterly",
            "Train staff on waste management procedures"
        ]
        
        # Construction-specific measures
        if construction['recycling_rate'] < 60:
            measures.extend([
                "Implement construction waste sorting areas",
                "Partner with certified recycling facilities",
                "Use modular construction to reduce waste generation"
            ])
        
        # Operational-specific measures
        if operational['recycling_rate'] < 40:
            measures.extend([
                "Install comprehensive recycling bins",
                "Implement organic waste composting program",
                "Establish waste reduction awareness campaigns"
            ])
        
        # Hazardous waste measures
        measures.extend([
            "Implement hazardous waste tracking system",
            "Ensure proper storage and labeling of hazardous materials",
            "Use licensed hazardous waste disposal contractors"
        ])
        
        return measures
    
    def _get_construction_compliance(self, location: str) -> List[str]:
        """Get construction waste compliance requirements"""
        if 'uae' in location or any(city in location for city in ['dubai', 'abu dhabi']):
            return [
                "UAE Federal Law No. 24 of 1999 - Environmental Protection",
                "Dubai Municipality Waste Management Regulations",
                "Construction & Demolition Waste Management Guidelines",
                "Waste tracking and reporting requirements",
                "Licensed contractor requirements"
            ]
        else:  # KSA
            return [
                "KSA Environmental Law - Waste Management Provisions",
                "Municipal waste management regulations",
                "Construction waste disposal permits",
                "Environmental compliance reporting",
                "Waste facility licensing requirements"
            ]
    
    def _get_operational_compliance(self, location: str) -> List[str]:
        """Get operational waste compliance requirements"""
        if 'uae' in location or any(city in location for city in ['dubai', 'abu dhabi']):
            return [
                "Municipal solid waste collection agreements",
                "Recycling program implementation",
                "Waste generation reporting",
                "Hazardous waste manifesting",
                "Annual waste audit requirements"
            ]
        else:  # KSA
            return [
                "Municipal waste service agreements",
                "Waste segregation compliance",
                "Recycling target achievement",
                "Environmental monitoring and reporting",
                "Waste minimization plan implementation"
            ]
    
    def _assess_waste_compliance(self, construction: Dict, operational: Dict, location: str) -> str:
        """Assess overall waste management compliance"""
        
        # Check recycling rates against regional targets
        if 'uae' in location:
            const_target = 65  # UAE current target for C&D waste
            op_target = 30     # UAE current target for MSW
        else:  # KSA
            const_target = 45  # KSA current target
            op_target = 15     # KSA current target
        
        const_compliant = construction['recycling_rate'] >= const_target
        op_compliant = operational['recycling_rate'] >= op_target
        
        if const_compliant and op_compliant:
            return "Fully Compliant"
        elif const_compliant or op_compliant:
            return "Partially Compliant - Improvements Required"
        else:
            return "Non-Compliant - Significant Improvements Required"