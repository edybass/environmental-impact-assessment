"""
Comprehensive Soil & Geology Assessment Module
Professional soil and geological impact assessment for EIA

Created by: Edy Bassil
Email: bassileddy@gmail.com
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import math

class SoilType(Enum):
    """Soil classification types common in UAE/KSA"""
    SANDY_SOIL = "sandy_soil"
    CLAYEY_SOIL = "clayey_soil"
    SILTY_SOIL = "silty_soil"
    CALCAREOUS_SOIL = "calcareous_soil"
    SABKHA = "sabkha"  # Salt-affected soil
    ROCK_OUTCROP = "rock_outcrop"
    WADI_DEPOSITS = "wadi_deposits"

class ContaminationLevel(Enum):
    """Soil contamination levels"""
    CLEAN = "clean"
    SLIGHTLY_CONTAMINATED = "slightly_contaminated"
    MODERATELY_CONTAMINATED = "moderately_contaminated"
    HEAVILY_CONTAMINATED = "heavily_contaminated"
    SEVERELY_CONTAMINATED = "severely_contaminated"

class SeismicZone(Enum):
    """Seismic hazard zones"""
    ZONE_1 = "zone_1"  # Very Low
    ZONE_2 = "zone_2"  # Low
    ZONE_3 = "zone_3"  # Moderate
    ZONE_4 = "zone_4"  # High
    ZONE_5 = "zone_5"  # Very High

@dataclass
class SoilProfile:
    """Soil profile data"""
    depth_from: float  # meters
    depth_to: float    # meters
    soil_type: SoilType
    description: str
    bearing_capacity: float  # kPa
    permeability: float      # m/s
    plasticity_index: float
    organic_content: float   # %

@dataclass
class ContaminationData:
    """Soil contamination assessment data"""
    contaminant: str
    concentration: float
    unit: str
    regulatory_limit: float
    contamination_level: ContaminationLevel
    remediation_required: bool

@dataclass
class GeotechnicalData:
    """Geotechnical investigation data"""
    soil_profiles: List[SoilProfile]
    groundwater_depth: float
    foundation_recommendation: str
    settlement_potential: str
    liquefaction_potential: str

class SoilGeologyAssessment:
    """Comprehensive soil and geology assessment for EIA"""
    
    def __init__(self):
        self.regional_geology = self._initialize_regional_geology()
        self.soil_standards = self._initialize_soil_standards()
        self.seismic_data = self._initialize_seismic_data()
        self.contamination_standards = self._initialize_contamination_standards()
    
    def _initialize_regional_geology(self) -> Dict[str, Dict]:
        """Initialize regional geological data"""
        return {
            "uae": {
                "geological_formations": {
                    "quaternary_deposits": {
                        "description": "Recent alluvial and coastal deposits",
                        "thickness": "0-50m",
                        "characteristics": "Sand, gravel, clay, sabkha",
                        "occurrence": "Coastal areas, wadis, inland basins"
                    },
                    "tertiary_rocks": {
                        "description": "Limestone, sandstone, conglomerate",
                        "thickness": "100-500m",
                        "characteristics": "Well-bedded, sometimes fractured",
                        "occurrence": "Inland areas, Hajar Mountains"
                    },
                    "mesozoic_rocks": {
                        "description": "Limestone, dolomite, evaporites",
                        "thickness": "500-2000m",
                        "characteristics": "Carbonate rocks, solution features",
                        "occurrence": "Deep subsurface, mountain areas"
                    },
                    "ophiolite_complex": {
                        "description": "Igneous and metamorphic rocks",
                        "thickness": "Variable",
                        "characteristics": "Very hard, fractured, weathered surface",
                        "occurrence": "Hajar Mountains, UAE-Oman border"
                    }
                },
                "typical_soil_conditions": {
                    "coastal": {
                        "dominant_type": SoilType.SANDY_SOIL,
                        "characteristics": "Medium to fine sand, some silt",
                        "bearing_capacity": "150-300 kPa",
                        "challenges": ["Wind erosion", "Salt intrusion", "Low bearing capacity"]
                    },
                    "inland_plains": {
                        "dominant_type": SoilType.CALCAREOUS_SOIL,
                        "characteristics": "Calcareous sand and gravel",
                        "bearing_capacity": "200-400 kPa",
                        "challenges": ["Cementation variability", "Settlement"]
                    },
                    "sabkha_areas": {
                        "dominant_type": SoilType.SABKHA,
                        "characteristics": "Salt-affected clayey soil",
                        "bearing_capacity": "50-150 kPa",
                        "challenges": ["Expansive soils", "Corrosion", "Poor drainage"]
                    },
                    "mountain_foothills": {
                        "dominant_type": SoilType.ROCK_OUTCROP,
                        "characteristics": "Shallow soil over rock",
                        "bearing_capacity": "500-1000 kPa",
                        "challenges": ["Shallow soil", "Rock excavation", "Slope stability"]
                    }
                }
            },
            "ksa": {
                "geological_formations": {
                    "quaternary_deposits": {
                        "description": "Alluvial and aeolian deposits",
                        "thickness": "0-100m",
                        "characteristics": "Sand dunes, wadi deposits, sabkha",
                        "occurrence": "Eastern Province, coastal areas"
                    },
                    "tertiary_sediments": {
                        "description": "Sandstone, limestone, shale",
                        "thickness": "200-1000m",
                        "characteristics": "Well-stratified sedimentary rocks",
                        "occurrence": "Eastern and central regions"
                    },
                    "mesozoic_formations": {
                        "description": "Limestone, dolomite, sandstone",
                        "thickness": "1000-3000m",
                        "characteristics": "Massive carbonate and clastic rocks",
                        "occurrence": "Widespread in eastern regions"
                    },
                    "arabian_shield": {
                        "description": "Precambrian crystalline rocks",
                        "thickness": "Basement",
                        "characteristics": "Granite, gneiss, volcanic rocks",
                        "occurrence": "Western Saudi Arabia"
                    }
                },
                "typical_soil_conditions": {
                    "eastern_coastal": {
                        "dominant_type": SoilType.SANDY_SOIL,
                        "characteristics": "Fine to coarse sand",
                        "bearing_capacity": "100-250 kPa",
                        "challenges": ["Liquefaction", "Low bearing capacity", "Salt intrusion"]
                    },
                    "central_plateau": {
                        "dominant_type": SoilType.CALCAREOUS_SOIL,
                        "characteristics": "Calcareous gravelly soil",
                        "bearing_capacity": "250-500 kPa",
                        "challenges": ["Variable cementation", "Cavernous limestone"]
                    },
                    "western_mountains": {
                        "dominant_type": SoilType.ROCK_OUTCROP,
                        "characteristics": "Thin soil over crystalline rock",
                        "bearing_capacity": "800-1500 kPa",
                        "challenges": ["Very shallow soil", "Hard rock excavation", "Steep slopes"]
                    },
                    "sabkha_areas": {
                        "dominant_type": SoilType.SABKHA,
                        "characteristics": "Highly saline clayey soil",
                        "bearing_capacity": "30-120 kPa",
                        "challenges": ["Extreme salinity", "Expansive clays", "Corrosion risk"]
                    }
                }
            }
        }
    
    def _initialize_soil_standards(self) -> Dict[str, Dict]:
        """Initialize soil quality standards"""
        return {
            "uae": {
                "agricultural_standards": {
                    "ph_range": [6.5, 8.5],
                    "salinity_ec_max": 4.0,  # dS/m
                    "organic_matter_min": 1.0,  # %
                    "heavy_metals": {
                        "lead": 300,     # mg/kg
                        "cadmium": 10,   # mg/kg
                        "mercury": 5,    # mg/kg
                        "chromium": 250, # mg/kg
                        "zinc": 300     # mg/kg
                    }
                },
                "residential_standards": {
                    "total_petroleum_hydrocarbons": 100,  # mg/kg
                    "benzene": 1,     # mg/kg
                    "toluene": 30,    # mg/kg
                    "heavy_metals": {
                        "lead": 400,
                        "cadmium": 20,
                        "mercury": 10,
                        "arsenic": 20
                    }
                },
                "industrial_standards": {
                    "total_petroleum_hydrocarbons": 500,
                    "benzene": 5,
                    "toluene": 100,
                    "heavy_metals": {
                        "lead": 800,
                        "cadmium": 50,
                        "mercury": 20,
                        "arsenic": 50
                    }
                }
            },
            "ksa": {
                "agricultural_standards": {
                    "ph_range": [6.0, 8.5],
                    "salinity_ec_max": 4.0,
                    "organic_matter_min": 0.8,
                    "heavy_metals": {
                        "lead": 250,
                        "cadmium": 8,
                        "mercury": 3,
                        "chromium": 200,
                        "zinc": 250
                    }
                },
                "residential_standards": {
                    "total_petroleum_hydrocarbons": 80,
                    "benzene": 0.8,
                    "toluene": 25,
                    "heavy_metals": {
                        "lead": 350,
                        "cadmium": 15,
                        "mercury": 8,
                        "arsenic": 15
                    }
                },
                "industrial_standards": {
                    "total_petroleum_hydrocarbons": 400,
                    "benzene": 4,
                    "toluene": 80,
                    "heavy_metals": {
                        "lead": 600,
                        "cadmium": 40,
                        "mercury": 15,
                        "arsenic": 40
                    }
                }
            }
        }
    
    def _initialize_seismic_data(self) -> Dict[str, Dict]:
        """Initialize seismic hazard data"""
        return {
            "uae": {
                "seismic_zones": {
                    "dubai": {"zone": SeismicZone.ZONE_2, "pga": 0.10},        # Peak Ground Acceleration (g)
                    "abu_dhabi": {"zone": SeismicZone.ZONE_2, "pga": 0.08},
                    "sharjah": {"zone": SeismicZone.ZONE_2, "pga": 0.10},
                    "northern_emirates": {"zone": SeismicZone.ZONE_3, "pga": 0.15},
                    "eastern_region": {"zone": SeismicZone.ZONE_3, "pga": 0.18}
                },
                "fault_systems": [
                    {"name": "Dibba Fault Zone", "type": "Active", "distance_factor": "High risk if within 50km"},
                    {"name": "Hatta Fault", "type": "Potentially Active", "distance_factor": "Moderate risk if within 30km"}
                ],
                "building_code": "UAE Building Code - Seismic Design Requirements"
            },
            "ksa": {
                "seismic_zones": {
                    "riyadh": {"zone": SeismicZone.ZONE_1, "pga": 0.05},
                    "jeddah": {"zone": SeismicZone.ZONE_2, "pga": 0.12},
                    "dammam": {"zone": SeismicZone.ZONE_2, "pga": 0.10},
                    "tabuk": {"zone": SeismicZone.ZONE_3, "pga": 0.20},
                    "jazan": {"zone": SeismicZone.ZONE_3, "pga": 0.25}
                },
                "fault_systems": [
                    {"name": "Red Sea Rift", "type": "Active", "distance_factor": "High risk if within 100km"},
                    {"name": "Najd Fault System", "type": "Potentially Active", "distance_factor": "Moderate risk if within 50km"}
                ],
                "building_code": "Saudi Building Code - Seismic Load Requirements"
            }
        }
    
    def _initialize_contamination_standards(self) -> Dict[str, Dict]:
        """Initialize contamination assessment standards"""
        return {
            "screening_criteria": {
                "petroleum_hydrocarbons": {
                    "low": 50,      # mg/kg
                    "moderate": 200,
                    "high": 500,
                    "severe": 1000
                },
                "heavy_metals": {
                    "lead": {"low": 100, "moderate": 300, "high": 600, "severe": 1000},
                    "cadmium": {"low": 5, "moderate": 15, "high": 30, "severe": 50},
                    "mercury": {"low": 2, "moderate": 8, "high": 15, "severe": 25}
                },
                "volatile_organic_compounds": {
                    "benzene": {"low": 0.5, "moderate": 2, "high": 5, "severe": 10},
                    "toluene": {"low": 10, "moderate": 40, "high": 80, "severe": 150}
                }
            },
            "remediation_methods": {
                "excavation_disposal": {
                    "applicability": "All contamination types",
                    "effectiveness": 0.99,
                    "cost_per_m3": 150,  # USD
                    "timeframe": "Immediate"
                },
                "soil_washing": {
                    "applicability": "Heavy metals, some organics",
                    "effectiveness": 0.85,
                    "cost_per_m3": 80,
                    "timeframe": "3-6 months"
                },
                "bioremediation": {
                    "applicability": "Petroleum hydrocarbons",
                    "effectiveness": 0.75,
                    "cost_per_m3": 40,
                    "timeframe": "6-18 months"
                },
                "stabilization": {
                    "applicability": "Heavy metals",
                    "effectiveness": 0.70,
                    "cost_per_m3": 60,
                    "timeframe": "1-3 months"
                }
            }
        }
    
    def assess_soil_conditions(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess existing soil conditions at project site"""
        
        location = project_data.get('location', 'Dubai').lower()
        project_size = float(project_data.get('size', 10000))
        project_type = project_data.get('type', 'residential').lower()
        project_coords = (
            float(project_data.get('latitude', 25.276987)),
            float(project_data.get('longitude', 55.296249))
        )
        
        # Determine region and geological setting
        region = 'uae' if any(x in location for x in ['dubai', 'abu dhabi', 'sharjah']) else 'ksa'
        geological_setting = self._determine_geological_setting(location, project_coords)
        
        regional_geology = self.regional_geology[region]
        
        # Assess soil profile
        soil_profile = self._assess_soil_profile(geological_setting, regional_geology)
        
        # Agricultural impact assessment
        agricultural_impact = self._assess_agricultural_impact(project_data, soil_profile)
        
        # Erosion potential assessment
        erosion_assessment = self._assess_erosion_potential(location, soil_profile, project_data)
        
        # Soil suitability for construction
        construction_suitability = self._assess_construction_suitability(soil_profile, project_type)
        
        return {
            'geological_setting': geological_setting,
            'soil_profile': soil_profile,
            'agricultural_impact': agricultural_impact,
            'erosion_assessment': erosion_assessment,
            'construction_suitability': construction_suitability,
            'investigation_requirements': self._get_soil_investigation_requirements(project_size, project_type),
            'mitigation_measures': self._get_soil_mitigation_measures(erosion_assessment, construction_suitability)
        }
    
    def assess_contamination_risk(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess soil contamination risks"""
        
        location = project_data.get('location', 'Dubai').lower()
        project_type = project_data.get('type', 'residential').lower()
        project_size = float(project_data.get('size', 10000))
        
        # Determine region
        region = 'uae' if any(x in location for x in ['dubai', 'abu dhabi', 'sharjah']) else 'ksa'
        
        # Historical land use assessment
        historical_assessment = self._assess_historical_land_use(location, project_data)
        
        # Contamination risk screening
        contamination_risk = self._screen_contamination_risk(historical_assessment, project_type)
        
        # Sampling requirements
        sampling_plan = self._develop_sampling_plan(contamination_risk, project_size)
        
        # Standards assessment
        applicable_standards = self._get_applicable_standards(region, project_type)
        
        # Remediation planning
        remediation_planning = self._assess_remediation_requirements(contamination_risk)
        
        return {
            'historical_land_use': historical_assessment,
            'contamination_risk_level': contamination_risk,
            'sampling_requirements': sampling_plan,
            'applicable_standards': applicable_standards,
            'remediation_planning': remediation_planning,
            'regulatory_requirements': self._get_contamination_regulatory_requirements(region),
            'cost_estimates': self._estimate_contamination_costs(contamination_risk, project_size)
        }
    
    def assess_geological_hazards(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess geological and seismic hazards"""
        
        location = project_data.get('location', 'Dubai').lower()
        project_type = project_data.get('type', 'residential').lower()
        project_coords = (
            float(project_data.get('latitude', 25.276987)),
            float(project_data.get('longitude', 55.296249))
        )
        
        # Determine region
        region = 'uae' if any(x in location for x in ['dubai', 'abu dhabi', 'sharjah']) else 'ksa'
        
        # Seismic hazard assessment
        seismic_assessment = self._assess_seismic_hazards(location, region, project_coords)
        
        # Ground stability assessment
        ground_stability = self._assess_ground_stability(location, project_data)
        
        # Slope stability assessment
        slope_stability = self._assess_slope_stability(location, project_coords)
        
        # Liquefaction potential
        liquefaction_assessment = self._assess_liquefaction_potential(location, project_data)
        
        # Subsidence potential
        subsidence_assessment = self._assess_subsidence_potential(location, project_data)
        
        return {
            'seismic_hazards': seismic_assessment,
            'ground_stability': ground_stability,
            'slope_stability': slope_stability,
            'liquefaction_potential': liquefaction_assessment,
            'subsidence_potential': subsidence_assessment,
            'design_parameters': self._get_geotechnical_design_parameters(seismic_assessment),
            'mitigation_measures': self._get_geological_mitigation_measures(
                seismic_assessment, ground_stability, slope_stability
            )
        }
    
    def conduct_geotechnical_assessment(self, project_data: Dict[str, Any]) -> GeotechnicalData:
        """Conduct comprehensive geotechnical assessment"""
        
        location = project_data.get('location', 'Dubai').lower()
        project_type = project_data.get('type', 'residential').lower()
        project_size = float(project_data.get('size', 10000))
        
        # Geological setting
        geological_setting = self._determine_geological_setting(location, (25.0, 55.0))
        
        # Develop soil profiles based on location
        soil_profiles = self._develop_soil_profiles(geological_setting, project_size)
        
        # Groundwater assessment
        groundwater_depth = self._estimate_groundwater_depth(location, geological_setting)
        
        # Foundation recommendations
        foundation_recommendation = self._assess_foundation_requirements(
            soil_profiles, groundwater_depth, project_type
        )
        
        # Settlement analysis
        settlement_potential = self._assess_settlement_potential(soil_profiles, project_type)
        
        # Liquefaction analysis
        liquefaction_potential = self._assess_detailed_liquefaction(soil_profiles, location)
        
        return GeotechnicalData(
            soil_profiles=soil_profiles,
            groundwater_depth=groundwater_depth,
            foundation_recommendation=foundation_recommendation,
            settlement_potential=settlement_potential,
            liquefaction_potential=liquefaction_potential
        )
    
    def _determine_geological_setting(self, location: str, coords: Tuple[float, float]) -> str:
        """Determine geological setting based on location"""
        if any(term in location for term in ['coastal', 'marina', 'beach']):
            return 'coastal'
        elif any(term in location for term in ['mountain', 'hill', 'jebel']):
            return 'mountain_foothills'
        elif 'sabkha' in location or 'salt' in location:
            return 'sabkha_areas'
        else:
            return 'inland_plains'
    
    def _assess_soil_profile(self, geological_setting: str, regional_geology: Dict) -> Dict[str, Any]:
        """Assess soil profile based on geological setting"""
        
        if geological_setting in regional_geology['typical_soil_conditions']:
            soil_data = regional_geology['typical_soil_conditions'][geological_setting]
            
            return {
                'dominant_soil_type': soil_data['dominant_type'].value,
                'characteristics': soil_data['characteristics'],
                'bearing_capacity_range': soil_data['bearing_capacity'],
                'engineering_challenges': soil_data['challenges'],
                'profile_description': self._generate_soil_profile_description(soil_data['dominant_type']),
                'thickness_estimate': self._estimate_soil_thickness(geological_setting)
            }
        else:
            return {
                'dominant_soil_type': SoilType.SANDY_SOIL.value,
                'characteristics': 'Variable soil conditions',
                'bearing_capacity_range': '100-300 kPa',
                'engineering_challenges': ['Unknown soil conditions'],
                'profile_description': 'Detailed investigation required',
                'thickness_estimate': 'Variable'
            }
    
    def _assess_agricultural_impact(self, project_data: Dict, soil_profile: Dict) -> Dict[str, Any]:
        """Assess impact on agricultural land"""
        
        project_size = float(project_data.get('size', 10000))
        
        # Estimate agricultural land loss
        agricultural_area_affected = project_size * 1.2  # Include buffer area
        
        # Soil quality assessment for agriculture
        soil_type = soil_profile['dominant_soil_type']
        
        if soil_type in ['sandy_soil', 'calcareous_soil']:
            agricultural_suitability = 'moderate'
            productivity_loss = 'medium'
        elif soil_type == 'sabkha':
            agricultural_suitability = 'poor'
            productivity_loss = 'low'
        else:
            agricultural_suitability = 'good'
            productivity_loss = 'high'
        
        return {
            'agricultural_area_affected_m2': agricultural_area_affected,
            'agricultural_suitability': agricultural_suitability,
            'productivity_loss_level': productivity_loss,
            'topsoil_salvage_potential': 'high' if soil_type != 'sabkha' else 'low',
            'compensation_requirements': agricultural_area_affected > 5000,
            'restoration_potential': 'good' if productivity_loss != 'low' else 'poor'
        }
    
    def _assess_erosion_potential(self, location: str, soil_profile: Dict, project_data: Dict) -> Dict[str, Any]:
        """Assess soil erosion potential"""
        
        project_size = float(project_data.get('size', 10000))
        soil_type = soil_profile['dominant_soil_type']
        
        # Erosion susceptibility by soil type
        erosion_susceptibility = {
            'sandy_soil': 'high',
            'clayey_soil': 'medium',
            'silty_soil': 'high',
            'calcareous_soil': 'medium',
            'sabkha': 'low',
            'rock_outcrop': 'very_low'
        }
        
        susceptibility = erosion_susceptibility.get(soil_type, 'medium')
        
        # Wind erosion assessment
        if 'coastal' in location or 'desert' in location:
            wind_erosion_risk = 'high'
        else:
            wind_erosion_risk = 'medium'
        
        # Water erosion assessment
        if any(term in location for term in ['wadi', 'valley', 'slope']):
            water_erosion_risk = 'high'
        else:
            water_erosion_risk = 'low'
        
        # Calculate erosion rate
        if susceptibility == 'high':
            estimated_erosion_rate = 15  # tons/hectare/year
        elif susceptibility == 'medium':
            estimated_erosion_rate = 8
        else:
            estimated_erosion_rate = 2
        
        return {
            'erosion_susceptibility': susceptibility,
            'wind_erosion_risk': wind_erosion_risk,
            'water_erosion_risk': water_erosion_risk,
            'estimated_erosion_rate_tons_ha_year': estimated_erosion_rate,
            'total_soil_loss_potential_tons': round((project_size / 10000) * estimated_erosion_rate, 1),
            'erosion_control_priority': 'high' if susceptibility in ['high', 'medium'] else 'low',
            'monitoring_required': susceptibility in ['high', 'medium']
        }
    
    def _assess_construction_suitability(self, soil_profile: Dict, project_type: str) -> Dict[str, Any]:
        """Assess soil suitability for construction"""
        
        soil_type = soil_profile['dominant_soil_type']
        bearing_capacity = soil_profile['bearing_capacity_range']
        
        # Construction suitability matrix
        suitability_matrix = {
            'sandy_soil': {'foundation': 'suitable_with_treatment', 'excavation': 'easy', 'stability': 'moderate'},
            'clayey_soil': {'foundation': 'requires_assessment', 'excavation': 'difficult', 'stability': 'good'},
            'calcareous_soil': {'foundation': 'good', 'excavation': 'moderate', 'stability': 'good'},
            'sabkha': {'foundation': 'poor', 'excavation': 'difficult', 'stability': 'poor'},
            'rock_outcrop': {'foundation': 'excellent', 'excavation': 'very_difficult', 'stability': 'excellent'}
        }
        
        suitability = suitability_matrix.get(soil_type, suitability_matrix['sandy_soil'])
        
        # Project-specific requirements
        if project_type in ['commercial', 'industrial', 'infrastructure']:
            required_bearing_capacity = 300  # kPa
        else:
            required_bearing_capacity = 150  # kPa
        
        # Extract bearing capacity value (simplified)
        if 'kPa' in bearing_capacity:
            capacity_range = bearing_capacity.replace(' kPa', '').split('-')
            max_capacity = float(capacity_range[-1])
        else:
            max_capacity = 200  # Default
        
        bearing_adequate = max_capacity >= required_bearing_capacity
        
        return {
            'foundation_suitability': suitability['foundation'],
            'excavation_difficulty': suitability['excavation'],
            'slope_stability': suitability['stability'],
            'bearing_capacity_adequate': bearing_adequate,
            'ground_improvement_required': not bearing_adequate or suitability['foundation'] == 'poor',
            'special_foundation_design': soil_type in ['sabkha', 'clayey_soil'],
            'dewatering_required': 'likely' if soil_type == 'clayey_soil' else 'unlikely',
            'construction_challenges': soil_profile['engineering_challenges']
        }
    
    def _assess_historical_land_use(self, location: str, project_data: Dict) -> Dict[str, Any]:
        """Assess historical land use for contamination risk"""
        
        # Simplified historical assessment (would use detailed records in practice)
        potential_contamination_sources = []
        risk_level = 'low'
        
        if any(term in location.lower() for term in ['industrial', 'port', 'airport']):
            potential_contamination_sources.extend([
                'Industrial activities', 'Fuel storage', 'Chemical handling'
            ])
            risk_level = 'high'
        elif any(term in location.lower() for term in ['gas station', 'petrol', 'fuel']):
            potential_contamination_sources.extend([
                'Fuel storage tanks', 'Hydrocarbon spills'
            ])
            risk_level = 'moderate'
        elif any(term in location.lower() for term in ['urban', 'commercial']):
            potential_contamination_sources.extend([
                'Urban activities', 'Small-scale contamination'
            ])
            risk_level = 'low'
        
        return {
            'historical_activities': potential_contamination_sources,
            'contamination_risk_level': risk_level,
            'investigation_priority': 'high' if risk_level == 'high' else 'medium',
            'likely_contaminants': self._identify_likely_contaminants(potential_contamination_sources)
        }
    
    def _screen_contamination_risk(self, historical_assessment: Dict, project_type: str) -> str:
        """Screen contamination risk level"""
        
        historical_risk = historical_assessment['contamination_risk_level']
        
        # Adjust for project sensitivity
        if project_type in ['residential', 'mixed_use']:
            if historical_risk == 'moderate':
                return 'high'
            elif historical_risk == 'low':
                return 'moderate'
        
        return historical_risk
    
    def _develop_sampling_plan(self, contamination_risk: str, project_size: float) -> Dict[str, Any]:
        """Develop soil sampling plan"""
        
        # Sampling density based on risk and size
        if contamination_risk == 'high':
            sampling_density = 1  # samples per 1000 m²
        elif contamination_risk == 'moderate':
            sampling_density = 0.5
        else:
            sampling_density = 0.2
        
        total_samples = max(int((project_size / 1000) * sampling_density), 5)
        
        return {
            'total_samples_required': total_samples,
            'sampling_depth': '0-3m below ground surface',
            'sample_locations': 'Grid pattern with additional targeted sampling',
            'analytical_parameters': self._get_analytical_parameters(contamination_risk),
            'sampling_standards': 'ISO 18400 series - Soil sampling',
            'estimated_cost': total_samples * 150  # USD per sample
        }
    
    def _assess_seismic_hazards(self, location: str, region: str, coords: Tuple[float, float]) -> Dict[str, Any]:
        """Assess seismic hazards"""
        
        seismic_data = self.seismic_data[region]
        
        # Determine city/area
        city = self._identify_seismic_zone(location)
        
        if city in seismic_data['seismic_zones']:
            zone_data = seismic_data['seismic_zones'][city]
            seismic_zone = zone_data['zone']
            pga = zone_data['pga']
        else:
            # Default values
            seismic_zone = SeismicZone.ZONE_2
            pga = 0.10
        
        # Assess fault proximity
        fault_risk = self._assess_fault_proximity(coords, seismic_data['fault_systems'])
        
        return {
            'seismic_zone': seismic_zone.value,
            'peak_ground_acceleration': pga,
            'seismic_hazard_level': self._determine_seismic_hazard_level(pga),
            'fault_proximity_risk': fault_risk,
            'building_code_requirements': seismic_data['building_code'],
            'design_response_spectrum': self._get_design_response_spectrum(pga),
            'site_class_assessment_required': True
        }
    
    def _assess_ground_stability(self, location: str, project_data: Dict) -> Dict[str, Any]:
        """Assess ground stability conditions"""
        
        geological_setting = self._determine_geological_setting(location, (25.0, 55.0))
        
        if geological_setting == 'mountain_foothills':
            stability_rating = 'moderate'
            stability_concerns = ['Rock fall', 'Slope instability']
        elif geological_setting == 'sabkha_areas':
            stability_rating = 'poor'
            stability_concerns = ['Expansive soils', 'Settlement', 'Bearing capacity']
        elif geological_setting == 'coastal':
            stability_rating = 'moderate'
            stability_concerns = ['Settlement', 'Liquefaction potential']
        else:
            stability_rating = 'good'
            stability_concerns = ['Minor settlement']
        
        return {
            'overall_stability_rating': stability_rating,
            'stability_concerns': stability_concerns,
            'detailed_investigation_required': stability_rating in ['poor', 'moderate'],
            'geotechnical_monitoring_required': stability_rating == 'poor',
            'foundation_design_implications': self._get_foundation_implications(stability_rating)
        }
    
    def _assess_slope_stability(self, location: str, coords: Tuple[float, float]) -> Dict[str, Any]:
        """Assess slope stability"""
        
        # Simplified slope assessment
        if any(term in location for term in ['mountain', 'hill', 'slope', 'wadi']):
            slope_risk = 'high'
            slope_angle_estimate = '>15 degrees'
            stability_measures_required = True
        elif 'coastal' in location:
            slope_risk = 'moderate'
            slope_angle_estimate = '5-15 degrees'
            stability_measures_required = False
        else:
            slope_risk = 'low'
            slope_angle_estimate = '<5 degrees'
            stability_measures_required = False
        
        return {
            'slope_stability_risk': slope_risk,
            'estimated_slope_angle': slope_angle_estimate,
            'stability_measures_required': stability_measures_required,
            'slope_monitoring_required': slope_risk == 'high',
            'recommendations': self._get_slope_stability_recommendations(slope_risk)
        }
    
    def _assess_liquefaction_potential(self, location: str, project_data: Dict) -> Dict[str, Any]:
        """Assess liquefaction potential"""
        
        # Liquefaction assessment factors
        if 'coastal' in location or 'beach' in location:
            soil_susceptibility = 'high'
        elif any(term in location for term in ['wadi', 'valley']):
            soil_susceptibility = 'moderate'
        else:
            soil_susceptibility = 'low'
        
        # Groundwater depth factor
        if 'coastal' in location:
            groundwater_factor = 'high_risk'  # Shallow groundwater
        else:
            groundwater_factor = 'low_risk'   # Deep groundwater
        
        # Combined assessment
        if soil_susceptibility == 'high' and groundwater_factor == 'high_risk':
            liquefaction_potential = 'high'
        elif soil_susceptibility == 'moderate' or groundwater_factor == 'high_risk':
            liquefaction_potential = 'moderate'
        else:
            liquefaction_potential = 'low'
        
        return {
            'liquefaction_potential': liquefaction_potential,
            'soil_susceptibility': soil_susceptibility,
            'groundwater_influence': groundwater_factor,
            'detailed_analysis_required': liquefaction_potential in ['high', 'moderate'],
            'mitigation_measures_required': liquefaction_potential == 'high',
            'design_considerations': self._get_liquefaction_design_considerations(liquefaction_potential)
        }
    
    def _assess_subsidence_potential(self, location: str, project_data: Dict) -> Dict[str, Any]:
        """Assess subsidence potential"""
        
        # Subsidence risk factors
        if 'sabkha' in location or 'salt' in location:
            subsidence_risk = 'high'
            causes = ['Salt dissolution', 'Clay compression']
        elif any(term in location for term in ['limestone', 'carbonate']):
            subsidence_risk = 'moderate'
            causes = ['Limestone dissolution', 'Karst formation']
        else:
            subsidence_risk = 'low'
            causes = ['Natural settlement only']
        
        return {
            'subsidence_risk': subsidence_risk,
            'potential_causes': causes,
            'monitoring_required': subsidence_risk in ['high', 'moderate'],
            'settlement_magnitude': self._estimate_settlement_magnitude(subsidence_risk),
            'timeframe': self._estimate_subsidence_timeframe(subsidence_risk)
        }
    
    def _get_soil_investigation_requirements(self, project_size: float, project_type: str) -> List[str]:
        """Get soil investigation requirements"""
        requirements = [
            "Geotechnical site investigation with borehole drilling",
            "Standard Penetration Test (SPT) at regular intervals",
            "Laboratory testing for soil classification and properties",
            "Groundwater level monitoring"
        ]
        
        if project_size > 10000:  # Large projects
            requirements.extend([
                "Cone Penetration Test (CPT) for detailed profiling",
                "Plate load tests for bearing capacity verification",
                "Permeability testing for drainage design"
            ])
        
        if project_type in ['industrial', 'infrastructure']:
            requirements.extend([
                "Dynamic loading tests",
                "Consolidation testing for settlement analysis",
                "Triaxial strength testing"
            ])
        
        return requirements
    
    def _get_soil_mitigation_measures(self, erosion_assessment: Dict, construction_suitability: Dict) -> List[str]:
        """Get soil protection and mitigation measures"""
        measures = []
        
        # Erosion control measures
        if erosion_assessment['erosion_susceptibility'] in ['high', 'medium']:
            measures.extend([
                "Implement erosion and sediment control plan",
                "Install temporary erosion barriers during construction",
                "Establish permanent vegetation cover",
                "Design proper drainage systems"
            ])
        
        # Construction measures
        if construction_suitability['ground_improvement_required']:
            measures.extend([
                "Ground improvement techniques (compaction, stabilization)",
                "Specialized foundation design",
                "Soil replacement in critical areas"
            ])
        
        if construction_suitability['dewatering_required'] == 'likely':
            measures.extend([
                "Implement dewatering system during construction",
                "Monitor groundwater levels and quality",
                "Implement groundwater protection measures"
            ])
        
        # General measures
        measures.extend([
            "Topsoil stripping and stockpiling for reuse",
            "Implement dust control measures",
            "Soil contamination prevention protocols"
        ])
        
        return measures
    
    def _identify_likely_contaminants(self, contamination_sources: List[str]) -> List[str]:
        """Identify likely contaminants based on sources"""
        contaminants = []
        
        for source in contamination_sources:
            if 'fuel' in source.lower() or 'hydrocarbon' in source.lower():
                contaminants.extend(['Total Petroleum Hydrocarbons', 'BTEX compounds'])
            elif 'industrial' in source.lower():
                contaminants.extend(['Heavy metals', 'Volatile organic compounds'])
            elif 'chemical' in source.lower():
                contaminants.extend(['Various chemicals', 'Solvents'])
        
        return list(set(contaminants))  # Remove duplicates
    
    def _get_analytical_parameters(self, contamination_risk: str) -> List[str]:
        """Get analytical parameters for soil testing"""
        base_parameters = [
            'Total Petroleum Hydrocarbons (TPH)',
            'Heavy metals (Pb, Cd, Hg, As, Cr, Zn)',
            'pH and electrical conductivity'
        ]
        
        if contamination_risk in ['high', 'moderate']:
            base_parameters.extend([
                'BTEX (Benzene, Toluene, Ethylbenzene, Xylenes)',
                'Polycyclic Aromatic Hydrocarbons (PAHs)',
                'Volatile Organic Compounds (VOCs)'
            ])
        
        return base_parameters
    
    def _get_applicable_standards(self, region: str, project_type: str) -> Dict[str, Any]:
        """Get applicable soil quality standards"""
        standards = self.soil_standards[region]
        
        if project_type == 'agricultural':
            return standards['agricultural_standards']
        elif project_type in ['residential', 'mixed_use']:
            return standards['residential_standards']
        else:
            return standards['industrial_standards']
    
    def _assess_remediation_requirements(self, contamination_risk: str) -> Dict[str, Any]:
        """Assess remediation requirements"""
        
        if contamination_risk == 'high':
            remediation_likelihood = 'high'
            recommended_methods = ['Excavation and disposal', 'Soil washing', 'Bioremediation']
            estimated_timeframe = '6-12 months'
        elif contamination_risk == 'moderate':
            remediation_likelihood = 'moderate'
            recommended_methods = ['Bioremediation', 'Stabilization', 'Monitored natural attenuation']
            estimated_timeframe = '3-9 months'
        else:
            remediation_likelihood = 'low'
            recommended_methods = ['Monitoring only', 'Minor soil replacement']
            estimated_timeframe = '1-3 months'
        
        return {
            'remediation_likelihood': remediation_likelihood,
            'recommended_methods': recommended_methods,
            'estimated_timeframe': estimated_timeframe,
            'regulatory_oversight_required': contamination_risk == 'high',
            'waste_classification_required': contamination_risk in ['high', 'moderate']
        }
    
    def _get_contamination_regulatory_requirements(self, region: str) -> List[str]:
        """Get contamination regulatory requirements"""
        if region == 'uae':
            return [
                "UAE Federal Law No. 24 of 1999 - Environmental Protection",
                "Contaminated land assessment guidelines",
                "Waste classification and disposal regulations",
                "Environmental clearance for remediation activities"
            ]
        else:  # KSA
            return [
                "KSA Environmental Law - Soil Protection Provisions",
                "Contaminated site investigation requirements",
                "Waste management and disposal regulations",
                "Environmental permit for remediation works"
            ]
    
    def _estimate_contamination_costs(self, contamination_risk: str, project_size: float) -> Dict[str, Any]:
        """Estimate contamination assessment and remediation costs"""
        
        # Investigation costs
        investigation_cost = project_size * 0.5  # USD per m²
        
        # Remediation costs (if required)
        if contamination_risk == 'high':
            remediation_cost_per_m2 = 100
        elif contamination_risk == 'moderate':
            remediation_cost_per_m2 = 40
        else:
            remediation_cost_per_m2 = 5
        
        remediation_cost = project_size * remediation_cost_per_m2
        
        return {
            'investigation_cost': round(investigation_cost, 0),
            'potential_remediation_cost': round(remediation_cost, 0),
            'total_potential_cost': round(investigation_cost + remediation_cost, 0),
            'cost_per_m2': round((investigation_cost + remediation_cost) / project_size, 2)
        }
    
    def _generate_soil_profile_description(self, soil_type: SoilType) -> str:
        """Generate detailed soil profile description"""
        descriptions = {
            SoilType.SANDY_SOIL: "Medium to fine sand with trace silt, loose to medium dense",
            SoilType.CLAYEY_SOIL: "Clay with sand and silt, firm to stiff consistency",
            SoilType.CALCAREOUS_SOIL: "Calcareous sand and gravel, cemented to loose",
            SoilType.SABKHA: "Highly saline clay and silt, soft to firm",
            SoilType.ROCK_OUTCROP: "Weathered rock with thin soil cover",
            SoilType.WADI_DEPOSITS: "Alluvial sand, gravel and silt deposits"
        }
        
        return descriptions.get(soil_type, "Variable soil conditions")
    
    def _estimate_soil_thickness(self, geological_setting: str) -> str:
        """Estimate soil thickness"""
        thickness_estimates = {
            'coastal': '5-20 meters',
            'inland_plains': '2-10 meters',
            'sabkha_areas': '1-5 meters',
            'mountain_foothills': '0.5-3 meters'
        }
        
        return thickness_estimates.get(geological_setting, 'Variable')
    
    def _identify_seismic_zone(self, location: str) -> str:
        """Identify seismic zone from location"""
        if 'dubai' in location:
            return 'dubai'
        elif 'abu dhabi' in location:
            return 'abu_dhabi'
        elif 'sharjah' in location:
            return 'sharjah'
        elif 'riyadh' in location:
            return 'riyadh'
        elif 'jeddah' in location:
            return 'jeddah'
        else:
            return 'other'
    
    def _determine_seismic_hazard_level(self, pga: float) -> str:
        """Determine seismic hazard level from PGA"""
        if pga >= 0.20:
            return 'high'
        elif pga >= 0.10:
            return 'moderate'
        else:
            return 'low'
    
    def _assess_fault_proximity(self, coords: Tuple[float, float], fault_systems: List[Dict]) -> str:
        """Assess proximity to active faults"""
        # Simplified assessment - would use GIS analysis in practice
        return 'moderate'  # Default assessment
    
    def _get_design_response_spectrum(self, pga: float) -> Dict[str, float]:
        """Get design response spectrum parameters"""
        return {
            'short_period_acceleration': pga * 1.2,
            '1_second_acceleration': pga * 0.8,
            'site_class': 'D',  # Default site class
            'importance_factor': 1.0
        }
    
    def _get_foundation_implications(self, stability_rating: str) -> List[str]:
        """Get foundation design implications"""
        if stability_rating == 'poor':
            return [
                "Deep foundation system required",
                "Ground improvement necessary",
                "Specialized foundation design",
                "Continuous monitoring required"
            ]
        elif stability_rating == 'moderate':
            return [
                "Careful foundation design required",
                "Possible ground improvement",
                "Regular monitoring recommended"
            ]
        else:
            return [
                "Standard foundation design adequate",
                "Routine geotechnical design approach"
            ]
    
    def _get_slope_stability_recommendations(self, slope_risk: str) -> List[str]:
        """Get slope stability recommendations"""
        if slope_risk == 'high':
            return [
                "Detailed slope stability analysis required",
                "Install slope stabilization measures",
                "Implement comprehensive monitoring system",
                "Design appropriate drainage systems"
            ]
        elif slope_risk == 'moderate':
            return [
                "Basic slope stability assessment",
                "Install standard slope protection",
                "Regular visual inspections"
            ]
        else:
            return [
                "Standard grading and drainage adequate",
                "Periodic maintenance required"
            ]
    
    def _get_liquefaction_design_considerations(self, potential: str) -> List[str]:
        """Get liquefaction design considerations"""
        if potential == 'high':
            return [
                "Liquefaction analysis required",
                "Ground improvement to mitigate liquefaction",
                "Special foundation design for liquefaction",
                "Post-earthquake inspection protocols"
            ]
        elif potential == 'moderate':
            return [
                "Simplified liquefaction assessment",
                "Consider liquefaction in foundation design",
                "Monitor performance during earthquakes"
            ]
        else:
            return [
                "Standard seismic design adequate",
                "No special liquefaction measures required"
            ]
    
    def _estimate_settlement_magnitude(self, subsidence_risk: str) -> str:
        """Estimate settlement magnitude"""
        if subsidence_risk == 'high':
            return '10-50 cm over 5-10 years'
        elif subsidence_risk == 'moderate':
            return '2-10 cm over 10-20 years'
        else:
            return '<2 cm over project lifetime'
    
    def _estimate_subsidence_timeframe(self, subsidence_risk: str) -> str:
        """Estimate subsidence timeframe"""
        if subsidence_risk == 'high':
            return 'Immediate to 10 years'
        elif subsidence_risk == 'moderate':
            return '5-20 years'
        else:
            return 'Long-term (>20 years)'
    
    def _develop_soil_profiles(self, geological_setting: str, project_size: float) -> List[SoilProfile]:
        """Develop representative soil profiles"""
        profiles = []
        
        if geological_setting == 'coastal':
            profiles.extend([
                SoilProfile(0, 2, SoilType.SANDY_SOIL, "Fine to medium sand, loose", 150, 1e-4, 5, 0.5),
                SoilProfile(2, 8, SoilType.SANDY_SOIL, "Medium sand with shells, medium dense", 250, 1e-3, 8, 0.3),
                SoilProfile(8, 15, SoilType.CLAYEY_SOIL, "Marine clay, firm", 120, 1e-8, 25, 2.0)
            ])
        elif geological_setting == 'sabkha_areas':
            profiles.extend([
                SoilProfile(0, 1, SoilType.SABKHA, "Saline crust, very stiff", 80, 1e-9, 45, 1.0),
                SoilProfile(1, 5, SoilType.SABKHA, "Saline clay, soft to firm", 60, 1e-8, 35, 3.0),
                SoilProfile(5, 12, SoilType.CLAYEY_SOIL, "Silty clay, firm", 150, 1e-7, 20, 1.5)
            ])
        else:  # inland_plains default
            profiles.extend([
                SoilProfile(0, 3, SoilType.SANDY_SOIL, "Calcareous sand, loose to medium", 200, 1e-3, 10, 0.8),
                SoilProfile(3, 10, SoilType.CALCAREOUS_SOIL, "Cemented calcareous soil", 400, 1e-5, 15, 0.5),
                SoilProfile(10, 20, SoilType.ROCK_OUTCROP, "Weathered limestone", 800, 1e-6, 5, 0.2)
            ])
        
        return profiles
    
    def _estimate_groundwater_depth(self, location: str, geological_setting: str) -> float:
        """Estimate groundwater depth"""
        if geological_setting == 'coastal':
            return 2.0  # meters below surface
        elif geological_setting == 'sabkha_areas':
            return 1.0
        elif 'wadi' in location:
            return 5.0
        else:
            return 15.0  # Deep groundwater in inland areas
    
    def _assess_foundation_requirements(self, soil_profiles: List[SoilProfile], 
                                      groundwater_depth: float, project_type: str) -> str:
        """Assess foundation requirements"""
        
        # Find bearing capacity at shallow depth
        shallow_bearing = min([profile.bearing_capacity for profile in soil_profiles[:2]])
        
        if project_type in ['commercial', 'industrial']:
            required_capacity = 300  # kPa
        else:
            required_capacity = 150  # kPa
        
        if shallow_bearing >= required_capacity:
            return "Shallow foundations (spread footings) adequate"
        elif any(profile.bearing_capacity >= required_capacity for profile in soil_profiles):
            return "Deep foundations (piles) recommended to competent layer"
        else:
            return "Ground improvement required before foundation construction"
    
    def _assess_settlement_potential(self, soil_profiles: List[SoilProfile], project_type: str) -> str:
        """Assess settlement potential"""
        
        # Check for compressible layers
        compressible_layers = [p for p in soil_profiles if p.soil_type == SoilType.CLAYEY_SOIL and p.bearing_capacity < 200]
        
        if compressible_layers:
            total_thickness = sum(layer.depth_to - layer.depth_from for layer in compressible_layers)
            if total_thickness > 5:
                return "High settlement potential - detailed analysis required"
            else:
                return "Moderate settlement potential - design considerations needed"
        else:
            return "Low settlement potential - standard design adequate"
    
    def _assess_detailed_liquefaction(self, soil_profiles: List[SoilProfile], location: str) -> str:
        """Assess liquefaction potential in detail"""
        
        # Check for sandy layers below groundwater
        sandy_layers = [p for p in soil_profiles if p.soil_type == SoilType.SANDY_SOIL]
        
        if 'coastal' in location and sandy_layers:
            return "Moderate to high liquefaction potential - detailed analysis required"
        elif sandy_layers:
            return "Low to moderate liquefaction potential - consider in design"
        else:
            return "Low liquefaction potential - no special measures required"
    
    def _get_geotechnical_design_parameters(self, seismic_assessment: Dict) -> Dict[str, Any]:
        """Get geotechnical design parameters"""
        
        pga = seismic_assessment['peak_ground_acceleration']
        
        return {
            'design_ground_acceleration': pga,
            'site_class': 'D',  # Default for UAE/KSA conditions
            'soil_factor': 1.2,
            'foundation_factor': 1.0,
            'liquefaction_factor': 1.1 if 'coastal' in str(seismic_assessment) else 1.0,
            'dynamic_analysis_required': pga > 0.15
        }
    
    def _get_geological_mitigation_measures(self, seismic_assessment: Dict, 
                                          ground_stability: Dict, slope_stability: Dict) -> List[str]:
        """Get geological hazard mitigation measures"""
        measures = []
        
        # Seismic measures
        if seismic_assessment['seismic_hazard_level'] in ['moderate', 'high']:
            measures.extend([
                "Implement seismic design code requirements",
                "Conduct site-specific seismic analysis",
                "Design for appropriate ground acceleration"
            ])
        
        # Ground stability measures
        if ground_stability['overall_stability_rating'] == 'poor':
            measures.extend([
                "Implement ground improvement techniques",
                "Install monitoring systems",
                "Design specialized foundation systems"
            ])
        
        # Slope stability measures
        if slope_stability['slope_stability_risk'] == 'high':
            measures.extend([
                "Install slope stabilization systems",
                "Implement proper drainage design",
                "Establish slope monitoring program"
            ])
        
        # General measures
        measures.extend([
            "Regular geotechnical monitoring during construction",
            "Implement proper site drainage",
            "Follow geotechnical design recommendations"
        ])
        
        return measures