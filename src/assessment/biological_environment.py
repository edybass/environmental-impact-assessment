"""
Comprehensive Biological Environment Assessment Module
Professional flora, fauna, and ecosystem impact assessment

Created by: Edy Bassil
Email: bassileddy@gmail.com
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import math

class ConservationStatus(Enum):
    """Species conservation status according to IUCN/local classifications"""
    CRITICALLY_ENDANGERED = "critically_endangered"
    ENDANGERED = "endangered"
    VULNERABLE = "vulnerable"
    NEAR_THREATENED = "near_threatened"
    LEAST_CONCERN = "least_concern"
    DATA_DEFICIENT = "data_deficient"
    NOT_EVALUATED = "not_evaluated"

class HabitatType(Enum):
    """Habitat types common in UAE/KSA"""
    DESERT = "desert"
    COASTAL = "coastal"
    MARINE = "marine"
    MANGROVE = "mangrove"
    SABKHA = "sabkha"  # Salt flats
    WADI = "wadi"      # Dry riverbeds
    OASIS = "oasis"
    URBAN_GREEN = "urban_green"
    AGRICULTURAL = "agricultural"

@dataclass
class Species:
    """Individual species data"""
    scientific_name: str
    common_name: str
    conservation_status: ConservationStatus
    habitat_preference: List[HabitatType]
    endemic: bool
    protected_by_law: bool
    ecological_importance: str
    threats: List[str]

@dataclass
class Habitat:
    """Habitat area data"""
    habitat_type: HabitatType
    area_hectares: float
    condition: str  # Excellent, Good, Fair, Poor
    connectivity: str
    species_richness: int
    conservation_value: str

@dataclass
class EcosystemService:
    """Ecosystem services provided"""
    service_type: str
    economic_value: float  # USD/hectare/year
    beneficiaries: List[str]
    impact_magnitude: str

class BiologicalEnvironmentAssessment:
    """Comprehensive biological environment assessment for EIA"""
    
    def __init__(self):
        self.regional_species = self._initialize_regional_species()
        self.habitat_database = self._initialize_habitat_database()
        self.ecosystem_services = self._initialize_ecosystem_services()
    
    def _initialize_regional_species(self) -> Dict[str, Dict[str, Species]]:
        """Initialize regional species database"""
        return {
            "uae": {
                "flora": {
                    "ghaf_tree": Species(
                        scientific_name="Prosopis cineraria",
                        common_name="Ghaf Tree",
                        conservation_status=ConservationStatus.NEAR_THREATENED,
                        habitat_preference=[HabitatType.DESERT, HabitatType.WADI],
                        endemic=False,
                        protected_by_law=True,
                        ecological_importance="National tree of UAE, drought tolerance",
                        threats=["Urbanization", "Overgrazing", "Climate change"]
                    ),
                    "date_palm": Species(
                        scientific_name="Phoenix dactylifera",
                        common_name="Date Palm",
                        conservation_status=ConservationStatus.LEAST_CONCERN,
                        habitat_preference=[HabitatType.OASIS, HabitatType.AGRICULTURAL],
                        endemic=False,
                        protected_by_law=False,
                        ecological_importance="Cultural and economic importance",
                        threats=["Red palm weevil", "Urbanization"]
                    ),
                    "mangrove": Species(
                        scientific_name="Avicennia marina",
                        common_name="Grey Mangrove",
                        conservation_status=ConservationStatus.NEAR_THREATENED,
                        habitat_preference=[HabitatType.MANGROVE, HabitatType.COASTAL],
                        endemic=False,
                        protected_by_law=True,
                        ecological_importance="Coastal protection, nursery habitat",
                        threats=["Coastal development", "Pollution", "Sea level rise"]
                    ),
                    "desert_hyacinth": Species(
                        scientific_name="Cistanche tubulosa",
                        common_name="Desert Hyacinth",
                        conservation_status=ConservationStatus.VULNERABLE,
                        habitat_preference=[HabitatType.DESERT],
                        endemic=True,
                        protected_by_law=True,
                        ecological_importance="Endemic species, medicinal value",
                        threats=["Habitat loss", "Over-collection"]
                    )
                },
                "fauna": {
                    "arabian_oryx": Species(
                        scientific_name="Oryx leucoryx",
                        common_name="Arabian Oryx",
                        conservation_status=ConservationStatus.VULNERABLE,
                        habitat_preference=[HabitatType.DESERT],
                        endemic=True,
                        protected_by_law=True,
                        ecological_importance="National animal, ecosystem indicator",
                        threats=["Habitat fragmentation", "Poaching"]
                    ),
                    "houbara_bustard": Species(
                        scientific_name="Chlamydotis undulata",
                        common_name="Houbara Bustard",
                        conservation_status=ConservationStatus.VULNERABLE,
                        habitat_preference=[HabitatType.DESERT],
                        endemic=False,
                        protected_by_law=True,
                        ecological_importance="Migratory species, cultural importance",
                        threats=["Hunting", "Habitat loss", "Power lines"]
                    ),
                    "hawksbill_turtle": Species(
                        scientific_name="Eretmochelys imbricata",
                        common_name="Hawksbill Turtle",
                        conservation_status=ConservationStatus.CRITICALLY_ENDANGERED,
                        habitat_preference=[HabitatType.MARINE, HabitatType.COASTAL],
                        endemic=False,
                        protected_by_law=True,
                        ecological_importance="Marine ecosystem health indicator",
                        threats=["Coastal development", "Marine pollution", "Climate change"]
                    ),
                    "greater_flamingo": Species(
                        scientific_name="Phoenicopterus roseus",
                        common_name="Greater Flamingo",
                        conservation_status=ConservationStatus.LEAST_CONCERN,
                        habitat_preference=[HabitatType.COASTAL, HabitatType.SABKHA],
                        endemic=False,
                        protected_by_law=True,
                        ecological_importance="Indicator of wetland health",
                        threats=["Habitat loss", "Disturbance", "Pollution"]
                    ),
                    "arabian_leopard": Species(
                        scientific_name="Panthera pardus nimr",
                        common_name="Arabian Leopard",
                        conservation_status=ConservationStatus.CRITICALLY_ENDANGERED,
                        habitat_preference=[HabitatType.DESERT],
                        endemic=True,
                        protected_by_law=True,
                        ecological_importance="Top predator, ecosystem health",
                        threats=["Habitat loss", "Prey depletion", "Human conflict"]
                    )
                }
            },
            "ksa": {
                "flora": {
                    "juniper_tree": Species(
                        scientific_name="Juniperus procera",
                        common_name="African Juniper",
                        conservation_status=ConservationStatus.NEAR_THREATENED,
                        habitat_preference=[HabitatType.DESERT],
                        endemic=False,
                        protected_by_law=True,
                        ecological_importance="Forest ecosystem species",
                        threats=["Deforestation", "Overgrazing", "Climate change"]
                    ),
                    "acacia_tree": Species(
                        scientific_name="Acacia tortilis",
                        common_name="Umbrella Acacia",
                        conservation_status=ConservationStatus.LEAST_CONCERN,
                        habitat_preference=[HabitatType.DESERT, HabitatType.WADI],
                        endemic=False,
                        protected_by_law=False,
                        ecological_importance="Shade and fodder provider",
                        threats=["Urbanization", "Overuse"]
                    ),
                    "wild_olive": Species(
                        scientific_name="Olea europaea subsp. cuspidata",
                        common_name="Wild Olive",
                        conservation_status=ConservationStatus.VULNERABLE,
                        habitat_preference=[HabitatType.DESERT],
                        endemic=False,
                        protected_by_law=True,
                        ecological_importance="Relict forest species",
                        threats=["Habitat destruction", "Collection"]
                    )
                },
                "fauna": {
                    "sand_cat": Species(
                        scientific_name="Felis margarita",
                        common_name="Sand Cat",
                        conservation_status=ConservationStatus.NEAR_THREATENED,
                        habitat_preference=[HabitatType.DESERT],
                        endemic=False,
                        protected_by_law=True,
                        ecological_importance="Desert ecosystem predator",
                        threats=["Habitat degradation", "Hunting"]
                    ),
                    "nubian_ibex": Species(
                        scientific_name="Capra nubiana",
                        common_name="Nubian Ibex",
                        conservation_status=ConservationStatus.VULNERABLE,
                        habitat_preference=[HabitatType.DESERT],
                        endemic=False,
                        protected_by_law=True,
                        ecological_importance="Mountain ecosystem species",
                        threats=["Hunting", "Habitat loss", "Competition with livestock"]
                    ),
                    "arabic_oryx": Species(
                        scientific_name="Oryx leucoryx",
                        common_name="Arabian Oryx",
                        conservation_status=ConservationStatus.VULNERABLE,
                        habitat_preference=[HabitatType.DESERT],
                        endemic=True,
                        protected_by_law=True,
                        ecological_importance="Desert flagship species",
                        threats=["Habitat fragmentation", "Poaching"]
                    )
                }
            }
        }
    
    def _initialize_habitat_database(self) -> Dict[str, Dict]:
        """Initialize habitat characteristics database"""
        return {
            HabitatType.DESERT.value: {
                "characteristics": "Arid environment, sparse vegetation, extreme temperatures",
                "typical_species_count": {"flora": 15, "fauna": 25},
                "conservation_priority": "High",
                "ecosystem_services": ["Carbon storage", "Tourism", "Cultural values"],
                "threats": ["Urbanization", "Overgrazing", "Climate change"],
                "restoration_potential": "Moderate"
            },
            HabitatType.COASTAL.value: {
                "characteristics": "Interface between land and sea, high biodiversity",
                "typical_species_count": {"flora": 20, "fauna": 45},
                "conservation_priority": "Very High",
                "ecosystem_services": ["Coastal protection", "Tourism", "Fisheries"],
                "threats": ["Development", "Pollution", "Sea level rise"],
                "restoration_potential": "Good"
            },
            HabitatType.MANGROVE.value: {
                "characteristics": "Salt-tolerant trees in coastal areas",
                "typical_species_count": {"flora": 8, "fauna": 35},
                "conservation_priority": "Critical",
                "ecosystem_services": ["Coastal protection", "Carbon storage", "Nursery habitat"],
                "threats": ["Coastal development", "Pollution", "Climate change"],
                "restoration_potential": "Excellent"
            },
            HabitatType.WADI.value: {
                "characteristics": "Seasonal watercourses, higher vegetation density",
                "typical_species_count": {"flora": 25, "fauna": 30},
                "conservation_priority": "High",
                "ecosystem_services": ["Water regulation", "Biodiversity refuge"],
                "threats": ["Development", "Water extraction", "Pollution"],
                "restoration_potential": "Good"
            },
            HabitatType.SABKHA.value: {
                "characteristics": "Salt flats, specialized halophytic vegetation",
                "typical_species_count": {"flora": 10, "fauna": 20},
                "conservation_priority": "Moderate",
                "ecosystem_services": ["Salt production", "Bird habitat"],
                "threats": ["Development", "Pollution", "Water level changes"],
                "restoration_potential": "Poor"
            }
        }
    
    def _initialize_ecosystem_services(self) -> Dict[str, EcosystemService]:
        """Initialize ecosystem services valuation"""
        return {
            "carbon_sequestration": EcosystemService(
                service_type="Carbon Sequestration",
                economic_value=150,  # USD/hectare/year
                beneficiaries=["Global community", "Climate regulation"],
                impact_magnitude="Global"
            ),
            "coastal_protection": EcosystemService(
                service_type="Coastal Protection",
                economic_value=2500,  # USD/hectare/year
                beneficiaries=["Coastal communities", "Infrastructure"],
                impact_magnitude="Regional"
            ),
            "tourism_recreation": EcosystemService(
                service_type="Tourism and Recreation",
                economic_value=800,   # USD/hectare/year
                beneficiaries=["Tourism industry", "Local communities"],
                impact_magnitude="Local-Regional"
            ),
            "biodiversity_habitat": EcosystemService(
                service_type="Biodiversity Habitat",
                economic_value=300,   # USD/hectare/year
                beneficiaries=["Species conservation", "Research"],
                impact_magnitude="Global"
            ),
            "water_regulation": EcosystemService(
                service_type="Water Regulation",
                economic_value=600,   # USD/hectare/year
                beneficiaries=["Water supply", "Flood control"],
                impact_magnitude="Regional"
            ),
            "cultural_heritage": EcosystemService(
                service_type="Cultural Heritage",
                economic_value=200,   # USD/hectare/year
                beneficiaries=["Local communities", "Cultural preservation"],
                impact_magnitude="Local"
            )
        }
    
    def assess_existing_habitat(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess existing habitat conditions at project site"""
        
        project_size = float(project_data.get('size', 10000))  # m²
        location = project_data.get('location', 'Dubai').lower()
        project_coords = (
            float(project_data.get('latitude', 25.276987)),
            float(project_data.get('longitude', 55.296249))
        )
        
        # Determine region
        region = 'uae' if any(x in location for x in ['dubai', 'abu dhabi', 'sharjah']) else 'ksa'
        
        # Identify probable habitat types based on location
        habitat_assessment = self._identify_habitat_types(location, project_coords)
        
        # Assess habitat quality and condition
        habitat_conditions = {}
        total_conservation_value = 0
        
        for habitat_type, area_percentage in habitat_assessment.items():
            area_hectares = (project_size / 10000) * (area_percentage / 100)
            
            habitat_info = self.habitat_database[habitat_type]
            
            # Assess condition based on location and human pressure
            condition = self._assess_habitat_condition(habitat_type, location)
            
            # Calculate species richness
            expected_flora = habitat_info['typical_species_count']['flora']
            expected_fauna = habitat_info['typical_species_count']['fauna']
            
            # Adjust for condition
            condition_factor = {'Excellent': 1.0, 'Good': 0.8, 'Fair': 0.6, 'Poor': 0.4}[condition]
            actual_flora = int(expected_flora * condition_factor)
            actual_fauna = int(expected_fauna * condition_factor)
            
            # Conservation value scoring
            priority_scores = {'Critical': 5, 'Very High': 4, 'High': 3, 'Moderate': 2, 'Low': 1}
            conservation_score = priority_scores[habitat_info['conservation_priority']]
            
            habitat_conditions[habitat_type] = {
                'area_hectares': round(area_hectares, 2),
                'area_percentage': area_percentage,
                'condition': condition,
                'expected_flora_species': expected_flora,
                'expected_fauna_species': expected_fauna,
                'actual_flora_species': actual_flora,
                'actual_fauna_species': actual_fauna,
                'conservation_priority': habitat_info['conservation_priority'],
                'conservation_score': conservation_score,
                'ecosystem_services': habitat_info['ecosystem_services'],
                'main_threats': habitat_info['threats'],
                'restoration_potential': habitat_info['restoration_potential']
            }
            
            total_conservation_value += conservation_score * area_percentage
        
        # Overall habitat assessment
        overall_score = total_conservation_value / 100
        
        return {
            'project_area_hectares': round(project_size / 10000, 2),
            'habitat_types_present': habitat_conditions,
            'overall_conservation_value': round(overall_score, 1),
            'habitat_connectivity': self._assess_habitat_connectivity(location),
            'endemic_species_potential': self._assess_endemic_species_potential(region, habitat_assessment),
            'protected_areas_nearby': self._identify_nearby_protected_areas(location, project_coords),
            'biodiversity_significance': self._determine_biodiversity_significance(overall_score)
        }
    
    def assess_species_impact(self, project_data: Dict[str, Any], habitat_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Assess potential impacts on flora and fauna species"""
        
        location = project_data.get('location', 'Dubai').lower()
        project_type = project_data.get('type', 'residential').lower()
        
        # Determine region
        region = 'uae' if any(x in location for x in ['dubai', 'abu dhabi', 'sharjah']) else 'ksa'
        
        species_database = self.regional_species[region]
        
        # Identify potentially affected species
        affected_species = {'flora': {}, 'fauna': {}}
        
        for habitat_type in habitat_assessment['habitat_types_present'].keys():
            habitat_enum = HabitatType(habitat_type)
            
            # Check flora
            for species_id, species in species_database['flora'].items():
                if habitat_enum in species.habitat_preference:
                    impact_magnitude = self._calculate_species_impact(
                        species, habitat_type, habitat_assessment, project_type
                    )
                    
                    affected_species['flora'][species_id] = {
                        'scientific_name': species.scientific_name,
                        'common_name': species.common_name,
                        'conservation_status': species.conservation_status.value,
                        'endemic': species.endemic,
                        'protected_by_law': species.protected_by_law,
                        'impact_magnitude': impact_magnitude,
                        'habitat_affected': habitat_type,
                        'mitigation_priority': self._determine_mitigation_priority(species, impact_magnitude)
                    }
            
            # Check fauna
            for species_id, species in species_database['fauna'].items():
                if habitat_enum in species.habitat_preference:
                    impact_magnitude = self._calculate_species_impact(
                        species, habitat_type, habitat_assessment, project_type
                    )
                    
                    affected_species['fauna'][species_id] = {
                        'scientific_name': species.scientific_name,
                        'common_name': species.common_name,
                        'conservation_status': species.conservation_status.value,
                        'endemic': species.endemic,
                        'protected_by_law': species.protected_by_law,
                        'impact_magnitude': impact_magnitude,
                        'habitat_affected': habitat_type,
                        'mitigation_priority': self._determine_mitigation_priority(species, impact_magnitude)
                    }
        
        # Calculate impact statistics
        impact_stats = self._calculate_impact_statistics(affected_species)
        
        return {
            'total_species_assessed': {
                'flora': len(affected_species['flora']),
                'fauna': len(affected_species['fauna'])
            },
            'affected_species': affected_species,
            'impact_statistics': impact_stats,
            'critical_species': self._identify_critical_species(affected_species),
            'legal_protection_requirements': self._assess_legal_requirements(affected_species, region)
        }
    
    def assess_ecosystem_services_impact(self, project_data: Dict[str, Any], habitat_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Assess impact on ecosystem services"""
        
        ecosystem_impact = {}
        total_economic_loss = 0
        
        for habitat_type, habitat_data in habitat_assessment['habitat_types_present'].items():
            area_hectares = habitat_data['area_hectares']
            
            # Determine which ecosystem services are provided by this habitat
            if habitat_type == HabitatType.MANGROVE.value:
                services = ['coastal_protection', 'carbon_sequestration', 'biodiversity_habitat']
            elif habitat_type == HabitatType.COASTAL.value:
                services = ['coastal_protection', 'tourism_recreation', 'biodiversity_habitat']
            elif habitat_type == HabitatType.DESERT.value:
                services = ['carbon_sequestration', 'cultural_heritage', 'biodiversity_habitat']
            elif habitat_type == HabitatType.WADI.value:
                services = ['water_regulation', 'biodiversity_habitat', 'cultural_heritage']
            else:
                services = ['biodiversity_habitat', 'cultural_heritage']
            
            for service_id in services:
                service = self.ecosystem_services[service_id]
                
                # Calculate annual economic value loss
                annual_loss = area_hectares * service.economic_value
                
                if service_id not in ecosystem_impact:
                    ecosystem_impact[service_id] = {
                        'service_type': service.service_type,
                        'affected_area_hectares': 0,
                        'annual_economic_loss': 0,
                        'beneficiaries': service.beneficiaries,
                        'impact_magnitude': service.impact_magnitude
                    }
                
                ecosystem_impact[service_id]['affected_area_hectares'] += area_hectares
                ecosystem_impact[service_id]['annual_economic_loss'] += annual_loss
                total_economic_loss += annual_loss
        
        # Calculate 20-year NPV of ecosystem service loss
        discount_rate = 0.03  # 3% discount rate
        npv_factor = sum(1/(1+discount_rate)**year for year in range(1, 21))
        total_npv_loss = total_economic_loss * npv_factor
        
        return {
            'ecosystem_services_affected': ecosystem_impact,
            'total_annual_economic_loss': round(total_economic_loss, 0),
            'total_npv_loss_20_years': round(total_npv_loss, 0),
            'restoration_cost_estimate': round(total_npv_loss * 0.6, 0),  # Assume restoration costs 60% of service value
            'offset_requirements': self._calculate_offset_requirements(habitat_assessment)
        }
    
    def develop_biodiversity_action_plan(self, project_data: Dict[str, Any], habitat_assessment: Dict[str, Any], species_impact: Dict[str, Any]) -> Dict[str, Any]:
        """Develop comprehensive biodiversity action plan"""
        
        # Avoidance measures
        avoidance_measures = [
            "Conduct detailed pre-construction biological surveys",
            "Implement seasonal restrictions during breeding periods",
            "Establish construction exclusion zones around sensitive habitats",
            "Use wildlife-friendly construction techniques and timing"
        ]
        
        # Minimization measures
        minimization_measures = [
            "Minimize vegetation clearance to essential areas only",
            "Implement progressive revegetation during construction",
            "Use native species for all landscaping",
            "Install wildlife-friendly lighting systems",
            "Create wildlife corridors and connectivity features"
        ]
        
        # Restoration measures
        restoration_area = sum(h['area_hectares'] for h in habitat_assessment['habitat_types_present'].values())
        restoration_measures = [
            f"Restore {restoration_area:.1f} hectares of equivalent habitat",
            "Implement adaptive management monitoring program",
            "Establish 20-year maintenance and monitoring protocol",
            "Partner with local conservation organizations"
        ]
        
        # Offset requirements (if needed)
        offset_requirements = []
        high_value_habitats = [h for h in habitat_assessment['habitat_types_present'].values() 
                              if h['conservation_score'] >= 4]
        
        if high_value_habitats:
            offset_area = sum(h['area_hectares'] for h in high_value_habitats) * 2  # 2:1 ratio
            offset_requirements = [
                f"Secure {offset_area:.1f} hectares of equivalent habitat for conservation",
                "Establish legal protection mechanisms for offset areas",
                "Implement long-term management plans for offset sites"
            ]
        
        # Monitoring requirements
        monitoring_requirements = [
            "Pre-construction baseline surveys (12 months)",
            "Construction phase monitoring (monthly)",
            "Post-construction monitoring (5 years)",
            "Long-term effectiveness monitoring (20 years)",
            "Annual reporting to regulatory authorities"
        ]
        
        # Calculate costs
        total_area = sum(h['area_hectares'] for h in habitat_assessment['habitat_types_present'].values())
        estimated_costs = {
            'surveys_and_planning': 50000,
            'avoidance_measures': 25000,
            'restoration_implementation': total_area * 15000,  # USD per hectare
            'monitoring_program': 30000,  # Annual cost
            'offset_land_acquisition': len(offset_requirements) * 100000 if offset_requirements else 0,
            'total_implementation': 0
        }
        estimated_costs['total_implementation'] = sum(estimated_costs.values()) - estimated_costs['total_implementation']
        
        return {
            'mitigation_hierarchy': {
                'avoidance': avoidance_measures,
                'minimization': minimization_measures,
                'restoration': restoration_measures,
                'offsets': offset_requirements
            },
            'monitoring_requirements': monitoring_requirements,
            'estimated_costs': estimated_costs,
            'implementation_timeline': {
                'pre_construction': '12 months',
                'construction_phase': 'Ongoing during construction',
                'post_construction': '5-20 years'
            },
            'success_criteria': [
                "No net loss of biodiversity",
                "95% survival rate of transplanted/restored vegetation",
                "Stable or increasing wildlife populations in area",
                "Successful establishment of habitat connectivity"
            ],
            'regulatory_approvals_required': self._identify_required_approvals(species_impact, habitat_assessment)
        }
    
    def _identify_habitat_types(self, location: str, coordinates: Tuple[float, float]) -> Dict[str, float]:
        """Identify probable habitat types based on location"""
        lat, lon = coordinates
        
        # Simplified habitat identification based on location
        if 'coastal' in location or 'marina' in location:
            return {
                HabitatType.COASTAL.value: 60,
                HabitatType.DESERT.value: 30,
                HabitatType.URBAN_GREEN.value: 10
            }
        elif 'mangrove' in location or (lat < 25.5 and 'abu dhabi' in location):
            return {
                HabitatType.MANGROVE.value: 40,
                HabitatType.COASTAL.value: 35,
                HabitatType.SABKHA.value: 25
            }
        elif 'desert' in location or 'al ain' in location:
            return {
                HabitatType.DESERT.value: 80,
                HabitatType.WADI.value: 15,
                HabitatType.URBAN_GREEN.value: 5
            }
        elif any(city in location for city in ['dubai', 'sharjah', 'riyadh', 'jeddah']):
            return {
                HabitatType.URBAN_GREEN.value: 50,
                HabitatType.DESERT.value: 40,
                HabitatType.AGRICULTURAL.value: 10
            }
        else:
            # Default desert habitat
            return {
                HabitatType.DESERT.value: 70,
                HabitatType.WADI.value: 20,
                HabitatType.URBAN_GREEN.value: 10
            }
    
    def _assess_habitat_condition(self, habitat_type: str, location: str) -> str:
        """Assess habitat condition based on location and human pressure"""
        urban_areas = ['dubai', 'abu dhabi', 'sharjah', 'riyadh', 'jeddah']
        
        if any(city in location for city in urban_areas):
            if habitat_type in [HabitatType.URBAN_GREEN.value, HabitatType.AGRICULTURAL.value]:
                return 'Fair'
            else:
                return 'Poor'
        else:
            if habitat_type in [HabitatType.MANGROVE.value, HabitatType.COASTAL.value]:
                return 'Good'
            else:
                return 'Fair'
    
    def _assess_habitat_connectivity(self, location: str) -> str:
        """Assess habitat connectivity"""
        if 'protected' in location or 'reserve' in location:
            return 'High'
        elif any(city in location for city in ['dubai', 'abu dhabi', 'riyadh']):
            return 'Low'
        else:
            return 'Moderate'
    
    def _assess_endemic_species_potential(self, region: str, habitat_assessment: Dict[str, float]) -> Dict[str, Any]:
        """Assess potential for endemic species occurrence"""
        species_database = self.regional_species[region]
        
        endemic_potential = {'flora': [], 'fauna': []}
        
        for species_type in ['flora', 'fauna']:
            for species_id, species in species_database[species_type].items():
                if species.endemic:
                    for habitat_type in species.habitat_preference:
                        if habitat_type.value in habitat_assessment:
                            endemic_potential[species_type].append({
                                'species': species.common_name,
                                'scientific_name': species.scientific_name,
                                'conservation_status': species.conservation_status.value,
                                'likelihood': 'High' if habitat_assessment[habitat_type.value] > 30 else 'Moderate'
                            })
        
        return {
            'endemic_flora_potential': endemic_potential['flora'],
            'endemic_fauna_potential': endemic_potential['fauna'],
            'total_endemic_species_potential': len(endemic_potential['flora']) + len(endemic_potential['fauna']),
            'survey_requirements': 'Detailed endemic species surveys required' if endemic_potential['flora'] or endemic_potential['fauna'] else 'Standard surveys adequate'
        }
    
    def _identify_nearby_protected_areas(self, location: str, coordinates: Tuple[float, float]) -> List[Dict[str, Any]]:
        """Identify nearby protected areas (simplified implementation)"""
        # This would normally query a GIS database of protected areas
        protected_areas = []
        
        if 'abu dhabi' in location:
            protected_areas.append({
                'name': 'Eastern Mangroves National Park',
                'distance_km': 25,
                'protection_level': 'National Park',
                'significance': 'Mangrove ecosystem protection'
            })
        elif 'dubai' in location:
            protected_areas.append({
                'name': 'Dubai Desert Conservation Reserve',
                'distance_km': 45,
                'protection_level': 'Conservation Reserve',
                'significance': 'Desert ecosystem and Arabian Oryx protection'
            })
        elif 'riyadh' in location:
            protected_areas.append({
                'name': 'Imam Turki bin Abdullah Royal Nature Reserve',
                'distance_km': 120,
                'protection_level': 'Royal Reserve',
                'significance': 'Arabian Oryx and desert ecosystem'
            })
        
        return protected_areas
    
    def _determine_biodiversity_significance(self, conservation_score: float) -> str:
        """Determine overall biodiversity significance"""
        if conservation_score >= 4.0:
            return "Very High - Critical biodiversity area"
        elif conservation_score >= 3.0:
            return "High - Important biodiversity area"
        elif conservation_score >= 2.0:
            return "Moderate - Biodiversity value present"
        else:
            return "Low - Limited biodiversity value"
    
    def _calculate_species_impact(self, species: Species, habitat_type: str, habitat_assessment: Dict, project_type: str) -> str:
        """Calculate impact magnitude on individual species"""
        # Consider conservation status
        status_weights = {
            ConservationStatus.CRITICALLY_ENDANGERED: 5,
            ConservationStatus.ENDANGERED: 4,
            ConservationStatus.VULNERABLE: 3,
            ConservationStatus.NEAR_THREATENED: 2,
            ConservationStatus.LEAST_CONCERN: 1
        }
        
        status_weight = status_weights[species.conservation_status]
        
        # Consider habitat area affected
        habitat_data = habitat_assessment['habitat_types_present'][habitat_type]
        area_factor = min(habitat_data['area_percentage'] / 100 * 3, 3)  # Max factor of 3
        
        # Consider if species is endemic or protected
        protection_factor = 1.5 if species.endemic else 1.0
        protection_factor *= 1.3 if species.protected_by_law else 1.0
        
        # Consider project type impact
        project_impacts = {
            'industrial': 3.0,
            'infrastructure': 2.5,
            'commercial': 2.0,
            'residential': 1.5,
            'mixed_use': 1.8
        }
        project_factor = project_impacts.get(project_type, 2.0)
        
        # Calculate overall impact score
        impact_score = status_weight * area_factor * protection_factor * project_factor
        
        if impact_score >= 15:
            return "Very High"
        elif impact_score >= 10:
            return "High"
        elif impact_score >= 6:
            return "Moderate"
        elif impact_score >= 3:
            return "Low"
        else:
            return "Very Low"
    
    def _determine_mitigation_priority(self, species: Species, impact_magnitude: str) -> str:
        """Determine mitigation priority for species"""
        if species.conservation_status in [ConservationStatus.CRITICALLY_ENDANGERED, ConservationStatus.ENDANGERED]:
            return "Critical"
        elif species.endemic and impact_magnitude in ["High", "Very High"]:
            return "Critical"
        elif species.protected_by_law and impact_magnitude in ["High", "Very High"]:
            return "High"
        elif impact_magnitude in ["High", "Very High"]:
            return "High"
        elif impact_magnitude == "Moderate":
            return "Medium"
        else:
            return "Low"
    
    def _calculate_impact_statistics(self, affected_species: Dict) -> Dict[str, Any]:
        """Calculate impact statistics"""
        stats = {
            'by_conservation_status': {},
            'by_impact_magnitude': {},
            'protected_species_count': 0,
            'endemic_species_count': 0
        }
        
        all_species = list(affected_species['flora'].values()) + list(affected_species['fauna'].values())
        
        for species in all_species:
            # Count by conservation status
            status = species['conservation_status']
            stats['by_conservation_status'][status] = stats['by_conservation_status'].get(status, 0) + 1
            
            # Count by impact magnitude
            impact = species['impact_magnitude']
            stats['by_impact_magnitude'][impact] = stats['by_impact_magnitude'].get(impact, 0) + 1
            
            # Count protected and endemic species
            if species['protected_by_law']:
                stats['protected_species_count'] += 1
            if species['endemic']:
                stats['endemic_species_count'] += 1
        
        return stats
    
    def _identify_critical_species(self, affected_species: Dict) -> List[Dict]:
        """Identify species requiring special attention"""
        critical_species = []
        
        all_species = list(affected_species['flora'].values()) + list(affected_species['fauna'].values())
        
        for species in all_species:
            if (species['conservation_status'] in ['critically_endangered', 'endangered'] or
                species['endemic'] or
                species['mitigation_priority'] == 'Critical'):
                critical_species.append(species)
        
        return critical_species
    
    def _assess_legal_requirements(self, affected_species: Dict, region: str) -> List[str]:
        """Assess legal protection requirements"""
        requirements = []
        
        protected_count = sum(1 for species in 
                            list(affected_species['flora'].values()) + list(affected_species['fauna'].values())
                            if species['protected_by_law'])
        
        if protected_count > 0:
            if region == 'uae':
                requirements.extend([
                    "UAE Federal Law No. 24 of 1999 - Environmental Protection",
                    "Local environmental authority permits required",
                    "Protected species impact assessment",
                    "Species-specific mitigation plans"
                ])
            else:  # KSA
                requirements.extend([
                    "KSA Environmental Law - Wildlife Protection",
                    "Ministry of Environment, Water and Agriculture permits",
                    "Protected species survey and mitigation requirements"
                ])
        
        return requirements
    
    def _calculate_offset_requirements(self, habitat_assessment: Dict) -> Dict[str, Any]:
        """Calculate biodiversity offset requirements"""
        high_value_area = sum(
            h['area_hectares'] for h in habitat_assessment['habitat_types_present'].values()
            if h['conservation_score'] >= 4
        )
        
        medium_value_area = sum(
            h['area_hectares'] for h in habitat_assessment['habitat_types_present'].values()
            if h['conservation_score'] == 3
        )
        
        # Apply offset multipliers
        offset_area = (high_value_area * 3.0) + (medium_value_area * 2.0)  # 3:1 and 2:1 ratios
        
        return {
            'offset_required': offset_area > 0,
            'offset_area_hectares': round(offset_area, 2),
            'offset_type': 'Like-for-like habitat',
            'offset_location': 'Within 50km of project site',
            'management_period': '20 years minimum'
        }
    
    def _identify_required_approvals(self, species_impact: Dict, habitat_assessment: Dict) -> List[str]:
        """Identify required regulatory approvals"""
        approvals = [
            "Environmental Impact Assessment approval",
            "Biodiversity management plan approval"
        ]
        
        if species_impact['critical_species']:
            approvals.append("Protected species permit")
        
        if any(h['conservation_score'] >= 4 for h in habitat_assessment['habitat_types_present'].values()):
            approvals.append("Habitat compensation plan approval")
        
        if habitat_assessment['protected_areas_nearby']:
            approvals.append("Protected area buffer zone clearance")
        
        return approvals