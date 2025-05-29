"""
Comprehensive Socio-Economic Environment Assessment Module
Professional socio-economic impact assessment for EIA

Created by: Edy Bassil
Email: bassileddy@gmail.com
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import math

class ProjectPhase(Enum):
    """Project development phases"""
    CONSTRUCTION = "construction"
    OPERATIONAL = "operational"
    DECOMMISSIONING = "decommissioning"

class ImpactMagnitude(Enum):
    """Impact magnitude classification"""
    NEGLIGIBLE = 1
    MINOR = 2
    MODERATE = 3
    MAJOR = 4
    SEVERE = 5

class TrafficVehicleType(Enum):
    """Traffic vehicle categories"""
    LIGHT_VEHICLES = "light_vehicles"
    HEAVY_TRUCKS = "heavy_trucks"
    CONSTRUCTION_VEHICLES = "construction_vehicles"
    PUBLIC_TRANSPORT = "public_transport"

@dataclass
class TrafficGeneration:
    """Traffic generation data"""
    vehicle_type: TrafficVehicleType
    daily_trips: int
    peak_hour_trips: int
    average_occupancy: float
    route_distribution: Dict[str, float]

@dataclass
class CulturalSite:
    """Cultural heritage site data"""
    site_name: str
    heritage_type: str
    significance_level: str
    distance_from_project: float
    protection_status: str
    potential_impacts: List[str]

@dataclass
class HealthRisk:
    """Health risk assessment data"""
    risk_factor: str
    affected_population: int
    exposure_pathway: str
    risk_level: str
    mitigation_required: bool

class SocioEconomicEnvironmentAssessment:
    """Comprehensive socio-economic environment assessment for EIA"""
    
    def __init__(self):
        self.regional_demographics = self._initialize_regional_demographics()
        self.traffic_standards = self._initialize_traffic_standards()
        self.cultural_heritage = self._initialize_cultural_heritage()
        self.health_standards = self._initialize_health_standards()
    
    def _initialize_regional_demographics(self) -> Dict[str, Dict]:
        """Initialize regional demographic data"""
        return {
            "uae": {
                "population_density": {
                    "dubai": 3100,      # persons/km²
                    "abu_dhabi": 1200,
                    "sharjah": 2800,
                    "ajman": 4200,
                    "other": 500
                },
                "demographics": {
                    "median_age": 33,
                    "expatriate_percentage": 85,
                    "employment_rate": 0.95,
                    "household_size": 3.2,
                    "education_level": "high"
                },
                "economic_indicators": {
                    "gdp_per_capita": 43000,  # USD
                    "average_income": 3500,   # USD/month
                    "unemployment_rate": 0.02,
                    "poverty_rate": 0.001
                },
                "infrastructure_capacity": {
                    "schools_per_1000": 0.8,
                    "hospitals_per_1000": 0.3,
                    "healthcare_beds_per_1000": 1.9,
                    "transport_capacity": "high"
                }
            },
            "ksa": {
                "population_density": {
                    "riyadh": 1800,
                    "jeddah": 2100,
                    "dammam": 1400,
                    "makkah": 3500,
                    "other": 400
                },
                "demographics": {
                    "median_age": 32,
                    "expatriate_percentage": 38,
                    "employment_rate": 0.85,
                    "household_size": 4.8,
                    "education_level": "medium-high"
                },
                "economic_indicators": {
                    "gdp_per_capita": 23000,
                    "average_income": 2800,
                    "unemployment_rate": 0.06,
                    "poverty_rate": 0.05
                },
                "infrastructure_capacity": {
                    "schools_per_1000": 1.2,
                    "hospitals_per_1000": 0.4,
                    "healthcare_beds_per_1000": 2.2,
                    "transport_capacity": "medium"
                }
            }
        }
    
    def _initialize_traffic_standards(self) -> Dict[str, Dict]:
        """Initialize traffic standards and capacity data"""
        return {
            "uae": {
                "capacity_standards": {
                    "arterial_road": 1800,     # vehicles/lane/hour
                    "collector_road": 1200,
                    "local_road": 800,
                    "highway": 2200
                },
                "level_of_service": {
                    "A": {"volume_capacity_ratio": 0.60, "description": "Free flow"},
                    "B": {"volume_capacity_ratio": 0.70, "description": "Stable flow"},
                    "C": {"volume_capacity_ratio": 0.80, "description": "Stable flow"},
                    "D": {"volume_capacity_ratio": 0.90, "description": "Approaching unstable"},
                    "E": {"volume_capacity_ratio": 0.95, "description": "Unstable flow"},
                    "F": {"volume_capacity_ratio": 1.00, "description": "Forced flow"}
                },
                "trip_generation_rates": {
                    "residential": {"units": "dwelling", "rate": 8.5},    # trips/day/dwelling
                    "commercial": {"units": "1000_sqm", "rate": 85},      # trips/day/1000m²
                    "office": {"units": "1000_sqm", "rate": 65},
                    "industrial": {"units": "1000_sqm", "rate": 15},
                    "mixed_use": {"units": "1000_sqm", "rate": 55}
                }
            },
            "ksa": {
                "capacity_standards": {
                    "arterial_road": 1600,
                    "collector_road": 1000,
                    "local_road": 700,
                    "highway": 2000
                },
                "level_of_service": {
                    "A": {"volume_capacity_ratio": 0.55, "description": "Free flow"},
                    "B": {"volume_capacity_ratio": 0.65, "description": "Stable flow"},
                    "C": {"volume_capacity_ratio": 0.75, "description": "Stable flow"},
                    "D": {"volume_capacity_ratio": 0.85, "description": "Approaching unstable"},
                    "E": {"volume_capacity_ratio": 0.95, "description": "Unstable flow"},
                    "F": {"volume_capacity_ratio": 1.00, "description": "Forced flow"}
                },
                "trip_generation_rates": {
                    "residential": {"units": "dwelling", "rate": 7.2},
                    "commercial": {"units": "1000_sqm", "rate": 75},
                    "office": {"units": "1000_sqm", "rate": 55},
                    "industrial": {"units": "1000_sqm", "rate": 12},
                    "mixed_use": {"units": "1000_sqm", "rate": 45}
                }
            }
        }
    
    def _initialize_cultural_heritage(self) -> Dict[str, List[Dict]]:
        """Initialize cultural heritage sites database"""
        return {
            "uae": [
                {
                    "name": "Al Fahidi Historical Neighbourhood",
                    "location": "Dubai",
                    "type": "Historical District",
                    "significance": "National",
                    "protection_status": "Protected Heritage Site",
                    "buffer_zone": 500  # meters
                },
                {
                    "name": "Sheikh Saeed Al Maktoum House",
                    "location": "Dubai",
                    "type": "Historical Building",
                    "significance": "National",
                    "protection_status": "Heritage Building",
                    "buffer_zone": 200
                },
                {
                    "name": "Qasr Al Hosn",
                    "location": "Abu Dhabi",
                    "type": "Palace/Fort",
                    "significance": "National",
                    "protection_status": "National Monument",
                    "buffer_zone": 1000
                },
                {
                    "name": "Heritage Village",
                    "location": "Abu Dhabi",
                    "type": "Cultural Center",
                    "significance": "Regional",
                    "protection_status": "Cultural Heritage Site",
                    "buffer_zone": 300
                }
            ],
            "ksa": [
                {
                    "name": "Al-Turaif District",
                    "location": "Diriyah, Riyadh",
                    "type": "Archaeological Site",
                    "significance": "UNESCO World Heritage",
                    "protection_status": "World Heritage Site",
                    "buffer_zone": 2000
                },
                {
                    "name": "Historic Jeddah",
                    "location": "Jeddah",
                    "type": "Historic City",
                    "significance": "UNESCO World Heritage",
                    "protection_status": "World Heritage Site",
                    "buffer_zone": 1500
                },
                {
                    "name": "Masjid al-Haram",
                    "location": "Makkah",
                    "type": "Religious Site",
                    "significance": "International Religious",
                    "protection_status": "Sacred Site",
                    "buffer_zone": 5000
                },
                {
                    "name": "Al-Rajhi Mosque",
                    "location": "Riyadh",
                    "type": "Religious Building",
                    "significance": "Local",
                    "protection_status": "Religious Heritage",
                    "buffer_zone": 100
                }
            ]
        }
    
    def _initialize_health_standards(self) -> Dict[str, Dict]:
        """Initialize health and safety standards"""
        return {
            "air_quality_health": {
                "pm10_daily": 120,      # µg/m³ (UAE/KSA standard)
                "pm25_daily": 35,       # µg/m³
                "no2_hourly": 200,      # µg/m³
                "so2_daily": 80,        # µg/m³
                "health_risk_threshold": "moderate"
            },
            "noise_health": {
                "residential_day": 55,   # dB(A)
                "residential_night": 45,
                "commercial": 65,
                "industrial": 70,
                "health_risk_threshold": "low"
            },
            "vulnerable_populations": {
                "children": {"age_range": "0-14", "sensitivity_factor": 1.5},
                "elderly": {"age_range": "65+", "sensitivity_factor": 1.3},
                "pregnant_women": {"sensitivity_factor": 1.4},
                "chronic_illness": {"sensitivity_factor": 1.6}
            },
            "emergency_services": {
                "ambulance_response_time": 8,    # minutes (urban)
                "fire_response_time": 6,
                "police_response_time": 5,
                "hospital_capacity_threshold": 0.85
            }
        }
    
    def assess_demographic_impact(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess demographic and population impacts"""
        
        project_size = float(project_data.get('size', 10000))
        project_type = project_data.get('type', 'residential').lower()
        location = project_data.get('location', 'Dubai').lower()
        duration = int(project_data.get('duration', 24))
        
        # Determine region and city
        region = 'uae' if any(x in location for x in ['dubai', 'abu dhabi', 'sharjah']) else 'ksa'
        city = self._identify_city(location)
        
        regional_data = self.regional_demographics[region]
        
        # Calculate population increases
        construction_workers = self._estimate_construction_workforce(project_size, project_type)
        operational_population = self._estimate_operational_population(project_size, project_type)
        
        # Assess infrastructure impacts
        infrastructure_impact = self._assess_infrastructure_capacity(
            construction_workers, operational_population, regional_data, city
        )
        
        # Calculate housing demand
        housing_demand = self._calculate_housing_demand(
            construction_workers, operational_population, regional_data
        )
        
        # Economic impact assessment
        economic_impact = self._assess_economic_impact(
            construction_workers, operational_population, project_size, regional_data
        )
        
        return {
            'construction_phase': {
                'additional_workers': construction_workers,
                'duration_months': duration,
                'peak_workforce_period': f"Months {duration//3}-{2*duration//3}",
                'workforce_accommodation_required': round(construction_workers * 0.7, 0)
            },
            'operational_phase': {
                'permanent_population_increase': operational_population,
                'estimated_residents': round(operational_population * 0.8, 0),
                'estimated_workers': round(operational_population * 0.2, 0),
                'population_growth_rate': round((operational_population / 
                    (regional_data['population_density'][city] * (project_size/1000000))) * 100, 2)
            },
            'infrastructure_impact': infrastructure_impact,
            'housing_demand': housing_demand,
            'economic_impact': economic_impact,
            'mitigation_measures': self._get_demographic_mitigation_measures()
        }
    
    def assess_traffic_impact(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive traffic impact assessment"""
        
        project_size = float(project_data.get('size', 10000))
        project_type = project_data.get('type', 'residential').lower()
        location = project_data.get('location', 'Dubai').lower()
        duration = int(project_data.get('duration', 24))
        
        region = 'uae' if any(x in location for x in ['dubai', 'abu dhabi', 'sharjah']) else 'ksa'
        traffic_data = self.traffic_standards[region]
        
        # Construction traffic assessment
        construction_traffic = self._assess_construction_traffic(
            project_size, project_type, duration, traffic_data
        )
        
        # Operational traffic assessment
        operational_traffic = self._assess_operational_traffic(
            project_size, project_type, traffic_data
        )
        
        # Road capacity analysis
        capacity_analysis = self._analyze_road_capacity(
            construction_traffic, operational_traffic, traffic_data
        )
        
        # Public transport impact
        public_transport_impact = self._assess_public_transport_impact(
            operational_traffic, location
        )
        
        # Traffic safety assessment
        safety_assessment = self._assess_traffic_safety(
            construction_traffic, operational_traffic, project_type
        )
        
        return {
            'construction_phase_traffic': construction_traffic,
            'operational_phase_traffic': operational_traffic,
            'road_capacity_analysis': capacity_analysis,
            'public_transport_impact': public_transport_impact,
            'traffic_safety_assessment': safety_assessment,
            'mitigation_measures': self._get_traffic_mitigation_measures(),
            'monitoring_requirements': self._get_traffic_monitoring_requirements()
        }
    
    def assess_cultural_heritage_impact(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess impacts on cultural heritage sites"""
        
        location = project_data.get('location', 'Dubai').lower()
        project_coords = (
            float(project_data.get('latitude', 25.276987)),
            float(project_data.get('longitude', 55.296249))
        )
        
        region = 'uae' if any(x in location for x in ['dubai', 'abu dhabi', 'sharjah']) else 'ksa'
        heritage_sites = self.cultural_heritage[region]
        
        # Identify nearby heritage sites
        nearby_sites = []
        for site in heritage_sites:
            # Simplified distance calculation (would use proper GIS in reality)
            if any(city in location for city in site['location'].lower().split()):
                distance = self._estimate_distance_to_site(project_coords, site)
                if distance <= site['buffer_zone']:
                    impact_assessment = self._assess_heritage_site_impact(site, distance, project_data)
                    nearby_sites.append({
                        'site_info': site,
                        'distance_meters': distance,
                        'impact_assessment': impact_assessment,
                        'mitigation_required': impact_assessment['impact_level'] != 'negligible'
                    })
        
        # Archaeological potential assessment
        archaeological_potential = self._assess_archaeological_potential(location, project_data)
        
        # Traditional land use assessment
        traditional_use_impact = self._assess_traditional_land_use(location, project_data)
        
        return {
            'heritage_sites_nearby': nearby_sites,
            'total_sites_affected': len(nearby_sites),
            'high_significance_sites': len([s for s in nearby_sites 
                                          if s['site_info']['significance'] in ['National', 'UNESCO World Heritage']]),
            'archaeological_potential': archaeological_potential,
            'traditional_land_use_impact': traditional_use_impact,
            'regulatory_requirements': self._get_heritage_regulatory_requirements(region),
            'mitigation_measures': self._get_heritage_mitigation_measures(nearby_sites)
        }
    
    def assess_health_safety_impact(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess public health and safety impacts"""
        
        project_size = float(project_data.get('size', 10000))
        project_type = project_data.get('type', 'residential').lower()
        location = project_data.get('location', 'Dubai').lower()
        
        # Identify vulnerable populations
        vulnerable_populations = self._identify_vulnerable_populations(location, project_size)
        
        # Air quality health risks
        air_quality_health = self._assess_air_quality_health_risks(
            project_data, vulnerable_populations
        )
        
        # Noise health impacts
        noise_health = self._assess_noise_health_impacts(
            project_data, vulnerable_populations
        )
        
        # Dust health impacts
        dust_health = self._assess_dust_health_impacts(
            project_data, vulnerable_populations
        )
        
        # Emergency services capacity
        emergency_services = self._assess_emergency_services_capacity(
            location, project_size, project_type
        )
        
        # Occupational health and safety
        occupational_health = self._assess_occupational_health_safety(project_data)
        
        return {
            'vulnerable_populations': vulnerable_populations,
            'air_quality_health_risks': air_quality_health,
            'noise_health_impacts': noise_health,
            'dust_health_impacts': dust_health,
            'emergency_services_capacity': emergency_services,
            'occupational_health_safety': occupational_health,
            'health_risk_ranking': self._rank_health_risks([
                air_quality_health, noise_health, dust_health
            ]),
            'mitigation_measures': self._get_health_safety_mitigation_measures()
        }
    
    def create_community_engagement_plan(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive community engagement plan"""
        
        location = project_data.get('location', 'Dubai').lower()
        project_type = project_data.get('type', 'residential').lower()
        duration = int(project_data.get('duration', 24))
        
        # Identify stakeholders
        stakeholders = self._identify_stakeholders(location, project_type)
        
        # Develop engagement activities
        engagement_activities = self._develop_engagement_activities(project_type, duration)
        
        # Create communication plan
        communication_plan = self._create_communication_plan(stakeholders, duration)
        
        # Grievance mechanism
        grievance_mechanism = self._design_grievance_mechanism()
        
        # Monitoring and evaluation
        monitoring_evaluation = self._design_engagement_monitoring()
        
        return {
            'stakeholder_groups': stakeholders,
            'engagement_activities': engagement_activities,
            'communication_plan': communication_plan,
            'grievance_mechanism': grievance_mechanism,
            'monitoring_evaluation': monitoring_evaluation,
            'budget_estimate': self._estimate_engagement_budget(engagement_activities, duration),
            'success_indicators': self._define_engagement_success_indicators()
        }
    
    def _estimate_construction_workforce(self, project_size: float, project_type: str) -> int:
        """Estimate construction workforce requirements"""
        base_workers_per_sqm = {
            'residential': 0.008,
            'commercial': 0.012,
            'industrial': 0.015,
            'infrastructure': 0.020,
            'mixed_use': 0.010
        }
        
        rate = base_workers_per_sqm.get(project_type, 0.010)
        return max(int(project_size * rate), 50)
    
    def _estimate_operational_population(self, project_size: float, project_type: str) -> int:
        """Estimate operational phase population"""
        population_rates = {
            'residential': 30,     # m²/person
            'commercial': 15,      # m²/person (workers + visitors)
            'industrial': 50,      # m²/person
            'infrastructure': 100, # m²/person
            'mixed_use': 25       # m²/person
        }
        
        rate = population_rates.get(project_type, 30)
        return max(int(project_size / rate), 20)
    
    def _assess_infrastructure_capacity(self, construction_pop: int, operational_pop: int, 
                                       regional_data: Dict, city: str) -> Dict[str, Any]:
        """Assess infrastructure capacity impacts"""
        
        infrastructure = regional_data['infrastructure_capacity']
        
        # Calculate additional demand
        peak_population = max(construction_pop, operational_pop)
        
        school_demand = peak_population * infrastructure['schools_per_1000'] / 1000
        hospital_demand = peak_population * infrastructure['hospitals_per_1000'] / 1000
        healthcare_bed_demand = peak_population * infrastructure['healthcare_beds_per_1000'] / 1000
        
        return {
            'schools': {
                'additional_demand': round(school_demand, 1),
                'capacity_adequacy': 'adequate' if school_demand < 2 else 'strained',
                'mitigation_required': school_demand >= 2
            },
            'healthcare': {
                'additional_hospital_demand': round(hospital_demand, 2),
                'additional_bed_demand': round(healthcare_bed_demand, 1),
                'capacity_adequacy': 'adequate' if healthcare_bed_demand < 50 else 'strained',
                'mitigation_required': healthcare_bed_demand >= 50
            },
            'utilities': {
                'electricity_demand_mw': round(peak_population * 0.003, 2),  # 3kW per person
                'water_demand_m3_day': round(peak_population * 0.25, 1),     # 250L per person
                'sewage_generation_m3_day': round(peak_population * 0.20, 1) # 200L per person
            }
        }
    
    def _calculate_housing_demand(self, construction_pop: int, operational_pop: int, 
                                 regional_data: Dict) -> Dict[str, Any]:
        """Calculate additional housing demand"""
        
        household_size = regional_data['demographics']['household_size']
        
        # Construction workers (temporary housing)
        temp_housing_units = math.ceil(construction_pop / 4)  # 4 workers per unit
        
        # Operational population (permanent housing)
        permanent_housing_units = math.ceil(operational_pop * 0.8 / household_size)  # 80% are residents
        
        return {
            'temporary_housing': {
                'units_required': temp_housing_units,
                'type': 'Worker accommodation/camps',
                'duration': 'Construction period'
            },
            'permanent_housing': {
                'units_required': permanent_housing_units,
                'type': 'Residential units',
                'duration': 'Operational period'
            },
            'total_additional_demand': temp_housing_units + permanent_housing_units,
            'market_impact': 'low' if permanent_housing_units < 100 else 'moderate'
        }
    
    def _assess_economic_impact(self, construction_pop: int, operational_pop: int, 
                               project_size: float, regional_data: Dict) -> Dict[str, Any]:
        """Assess economic impacts"""
        
        avg_income = regional_data['economic_indicators']['average_income']
        
        # Construction phase economic impact
        construction_payroll = construction_pop * avg_income * 0.8  # 80% of average
        construction_duration_years = 2  # Typical duration
        
        # Operational phase economic impact
        operational_jobs = operational_pop * 0.3  # 30% are direct jobs
        operational_payroll = operational_jobs * avg_income
        
        # Local spending multiplier
        local_spending_multiplier = 1.5
        
        return {
            'construction_phase': {
                'direct_jobs': construction_pop,
                'annual_payroll': round(construction_payroll * 12, 0),
                'total_economic_impact': round(construction_payroll * 12 * local_spending_multiplier, 0),
                'duration_years': construction_duration_years
            },
            'operational_phase': {
                'direct_jobs': round(operational_jobs, 0),
                'indirect_jobs': round(operational_jobs * 0.5, 0),  # 0.5 multiplier
                'annual_payroll': round(operational_payroll * 12, 0),
                'annual_economic_impact': round(operational_payroll * 12 * local_spending_multiplier, 0)
            },
            'tax_revenue': {
                'annual_property_tax': round(project_size * 50, 0),  # Estimated property tax
                'payroll_tax': round(operational_payroll * 12 * 0.1, 0)  # 10% payroll tax
            }
        }
    
    def _assess_construction_traffic(self, project_size: float, project_type: str, 
                                   duration: int, traffic_data: Dict) -> Dict[str, Any]:
        """Assess construction phase traffic generation"""
        
        # Estimate construction vehicles
        daily_truck_trips = {
            'residential': 0.15,    # trucks per m²
            'commercial': 0.20,
            'industrial': 0.25,
            'infrastructure': 0.30,
            'mixed_use': 0.18
        }
        
        rate = daily_truck_trips.get(project_type, 0.18)
        peak_daily_trucks = int(project_size * rate / 1000)  # Peak period
        average_daily_trucks = int(peak_daily_trucks * 0.6)
        
        # Worker vehicles
        workers = self._estimate_construction_workforce(project_size, project_type)
        worker_vehicles = int(workers * 0.7)  # 70% drive
        
        return {
            'peak_daily_truck_trips': peak_daily_trucks,
            'average_daily_truck_trips': average_daily_trucks,
            'daily_worker_vehicle_trips': worker_vehicles,
            'peak_hour_trips': int((peak_daily_trucks + worker_vehicles) * 0.15),  # 15% in peak hour
            'duration_months': duration,
            'route_impact': self._assess_route_impact(peak_daily_trucks + worker_vehicles),
            'road_wear_impact': self._assess_road_wear(peak_daily_trucks)
        }
    
    def _assess_operational_traffic(self, project_size: float, project_type: str, 
                                   traffic_data: Dict) -> Dict[str, Any]:
        """Assess operational phase traffic generation"""
        
        trip_rates = traffic_data['trip_generation_rates']
        project_rate = trip_rates.get(project_type, trip_rates['mixed_use'])
        
        # Calculate daily trips
        if project_rate['units'] == 'dwelling':
            units = project_size / 100  # Assume 100m² per dwelling
        else:  # 1000_sqm
            units = project_size / 1000
        
        daily_trips = int(units * project_rate['rate'])
        peak_hour_trips = int(daily_trips * 0.12)  # 12% in peak hour
        
        return {
            'daily_vehicle_trips': daily_trips,
            'peak_hour_trips': peak_hour_trips,
            'inbound_percentage': 50,  # Balanced in/out
            'outbound_percentage': 50,
            'trip_distribution': self._calculate_trip_distribution(project_type),
            'mode_split': self._calculate_mode_split(project_type)
        }
    
    def _analyze_road_capacity(self, construction_traffic: Dict, operational_traffic: Dict, 
                              traffic_data: Dict) -> Dict[str, Any]:
        """Analyze road capacity and level of service"""
        
        # Assume project is on arterial road
        road_capacity = traffic_data['capacity_standards']['arterial_road']
        los_standards = traffic_data['level_of_service']
        
        # Current traffic (assumed baseline)
        current_traffic = road_capacity * 0.75  # 75% capacity
        
        # Additional traffic
        construction_additional = construction_traffic['peak_hour_trips']
        operational_additional = operational_traffic['peak_hour_trips']
        
        # Analyze scenarios
        scenarios = {
            'current': current_traffic,
            'construction_peak': current_traffic + construction_additional,
            'operational': current_traffic + operational_additional
        }
        
        analysis = {}
        for scenario, traffic_volume in scenarios.items():
            vc_ratio = traffic_volume / road_capacity
            
            # Determine level of service
            los = 'F'
            for level, data in los_standards.items():
                if vc_ratio <= data['volume_capacity_ratio']:
                    los = level
                    break
            
            analysis[scenario] = {
                'traffic_volume': traffic_volume,
                'volume_capacity_ratio': round(vc_ratio, 2),
                'level_of_service': los,
                'description': los_standards[los]['description'],
                'acceptable': los in ['A', 'B', 'C']
            }
        
        return {
            'capacity_analysis': analysis,
            'mitigation_required': not analysis['construction_peak']['acceptable'] or 
                                 not analysis['operational']['acceptable'],
            'recommended_improvements': self._recommend_traffic_improvements(analysis)
        }
    
    def _identify_city(self, location: str) -> str:
        """Identify city from location string"""
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
    
    def _estimate_distance_to_site(self, project_coords: Tuple[float, float], site: Dict) -> float:
        """Estimate distance to heritage site (simplified)"""
        # This would use proper GIS calculations in reality
        # For now, return a reasonable estimate based on location
        return 800.0  # meters
    
    def _assess_heritage_site_impact(self, site: Dict, distance: float, project_data: Dict) -> Dict[str, Any]:
        """Assess impact on individual heritage site"""
        
        # Impact assessment based on distance and significance
        if distance <= site['buffer_zone'] * 0.3:
            impact_level = 'high'
        elif distance <= site['buffer_zone'] * 0.6:
            impact_level = 'moderate'
        elif distance <= site['buffer_zone']:
            impact_level = 'low'
        else:
            impact_level = 'negligible'
        
        # Adjust for significance
        if site['significance'] in ['UNESCO World Heritage', 'National'] and impact_level != 'negligible':
            impact_level = 'high' if impact_level == 'moderate' else impact_level
        
        potential_impacts = []
        if impact_level != 'negligible':
            potential_impacts = [
                'Visual impact on heritage setting',
                'Noise and vibration during construction',
                'Dust and air quality impacts',
                'Increased traffic in heritage area',
                'Potential archaeological disturbance'
            ]
        
        return {
            'impact_level': impact_level,
            'potential_impacts': potential_impacts,
            'buffer_zone_exceeded': distance <= site['buffer_zone'],
            'archaeological_survey_required': impact_level in ['high', 'moderate'],
            'heritage_impact_assessment_required': impact_level == 'high'
        }
    
    def _get_demographic_mitigation_measures(self) -> List[str]:
        """Get demographic impact mitigation measures"""
        return [
            "Coordinate with local authorities on infrastructure capacity",
            "Implement phased construction to manage peak workforce",
            "Provide worker accommodation to reduce housing pressure",
            "Support local skill development and training programs",
            "Establish community benefit programs",
            "Monitor and report on population impacts quarterly"
        ]
    
    def _get_traffic_mitigation_measures(self) -> List[str]:
        """Get traffic impact mitigation measures"""
        return [
            "Implement construction traffic management plan",
            "Restrict heavy vehicle movements to off-peak hours",
            "Provide alternative routes during peak construction",
            "Install traffic signals and control measures",
            "Implement road safety measures in construction zones",
            "Coordinate with public transport operators",
            "Provide shuttle services for workers",
            "Implement car-sharing and ride-sharing programs"
        ]
    
    def _get_heritage_mitigation_measures(self, nearby_sites: List[Dict]) -> List[str]:
        """Get cultural heritage mitigation measures"""
        measures = [
            "Conduct detailed archaeological survey before construction",
            "Implement heritage monitoring during construction",
            "Design project to minimize visual impact on heritage sites"
        ]
        
        high_significance_sites = [s for s in nearby_sites 
                                 if s['site_info']['significance'] in ['National', 'UNESCO World Heritage']]
        
        if high_significance_sites:
            measures.extend([
                "Prepare detailed Heritage Impact Assessment",
                "Engage heritage specialists throughout project",
                "Implement heritage-sensitive design guidelines",
                "Establish heritage interpretation program"
            ])
        
        return measures
    
    def _get_health_safety_mitigation_measures(self) -> List[str]:
        """Get health and safety mitigation measures"""
        return [
            "Implement dust suppression measures near sensitive receptors",
            "Maintain noise levels below health guidelines",
            "Provide air quality monitoring in residential areas",
            "Establish emergency response protocols",
            "Coordinate with local healthcare facilities",
            "Implement occupational health and safety programs",
            "Provide health screening for workers",
            "Maintain emergency service access during construction"
        ]
    
    def _assess_archaeological_potential(self, location: str, project_data: Dict) -> Dict[str, Any]:
        """Assess archaeological potential of project site"""
        # Simplified assessment - would use detailed archaeological databases
        return {
            'potential_level': 'medium',
            'survey_required': True,
            'potential_findings': ['Historical artifacts', 'Traditional structures'],
            'regulatory_requirements': ['Archaeological clearance before construction']
        }
    
    def _assess_traditional_land_use(self, location: str, project_data: Dict) -> Dict[str, Any]:
        """Assess impacts on traditional land use"""
        return {
            'traditional_uses_present': ['Grazing areas', 'Traditional pathways'],
            'impact_level': 'low',
            'compensation_required': False,
            'consultation_required': True
        }
    
    def _get_heritage_regulatory_requirements(self, region: str) -> List[str]:
        """Get heritage regulatory requirements"""
        if region == 'uae':
            return [
                "UAE Federal Law No. 11 of 2017 - Cultural Heritage Protection",
                "Local heritage authority approvals",
                "Archaeological survey requirements",
                "Heritage impact assessment submission"
            ]
        else:  # KSA
            return [
                "KSA Antiquities Law",
                "Heritage Commission approvals",
                "Archaeological clearance certificates",
                "Cultural heritage consultation requirements"
            ]
    
    def _identify_vulnerable_populations(self, location: str, project_size: float) -> Dict[str, Any]:
        """Identify vulnerable populations in project area"""
        # Estimated vulnerable populations within 1km
        total_population = int(project_size * 0.1)  # Simplified estimate
        
        return {
            'children_under_14': int(total_population * 0.20),
            'elderly_over_65': int(total_population * 0.08),
            'pregnant_women': int(total_population * 0.02),
            'chronic_illness': int(total_population * 0.15),
            'total_vulnerable': int(total_population * 0.45),
            'schools_nearby': 2,
            'healthcare_facilities_nearby': 1,
            'residential_areas_nearby': 3
        }
    
    def _assess_air_quality_health_risks(self, project_data: Dict, vulnerable_pops: Dict) -> Dict[str, Any]:
        """Assess air quality health risks"""
        return {
            'risk_level': 'moderate',
            'primary_pollutants': ['PM10', 'PM2.5', 'NO2'],
            'affected_population': vulnerable_pops['total_vulnerable'],
            'health_endpoints': ['Respiratory irritation', 'Cardiovascular stress'],
            'mitigation_effectiveness': 0.70
        }
    
    def _assess_noise_health_impacts(self, project_data: Dict, vulnerable_pops: Dict) -> Dict[str, Any]:
        """Assess noise health impacts"""
        return {
            'risk_level': 'low',
            'noise_sources': ['Construction equipment', 'Traffic'],
            'affected_population': vulnerable_pops['total_vulnerable'],
            'health_endpoints': ['Sleep disturbance', 'Stress'],
            'mitigation_effectiveness': 0.80
        }
    
    def _assess_dust_health_impacts(self, project_data: Dict, vulnerable_pops: Dict) -> Dict[str, Any]:
        """Assess dust health impacts"""
        return {
            'risk_level': 'moderate',
            'dust_sources': ['Excavation', 'Material handling', 'Vehicle movement'],
            'affected_population': vulnerable_pops['children_under_14'] + vulnerable_pops['elderly_over_65'],
            'health_endpoints': ['Respiratory irritation', 'Eye irritation'],
            'mitigation_effectiveness': 0.75
        }
    
    def _assess_emergency_services_capacity(self, location: str, project_size: float, project_type: str) -> Dict[str, Any]:
        """Assess emergency services capacity"""
        return {
            'ambulance_capacity': 'adequate',
            'fire_service_capacity': 'adequate',
            'police_capacity': 'adequate',
            'hospital_capacity': 'adequate',
            'additional_demand_manageable': True,
            'response_time_impact': 'minimal'
        }
    
    def _assess_occupational_health_safety(self, project_data: Dict) -> Dict[str, Any]:
        """Assess occupational health and safety"""
        return {
            'worker_safety_risks': ['Falls', 'Equipment accidents', 'Chemical exposure'],
            'safety_measures_required': ['PPE', 'Safety training', 'Emergency procedures'],
            'health_monitoring_required': True,
            'safety_compliance_rating': 'standard'
        }
    
    def _rank_health_risks(self, health_assessments: List[Dict]) -> List[Dict[str, str]]:
        """Rank health risks by priority"""
        risk_levels = {'low': 1, 'moderate': 2, 'high': 3, 'severe': 4}
        
        risks = []
        for i, assessment in enumerate(health_assessments):
            risk_names = ['Air Quality', 'Noise', 'Dust']
            risks.append({
                'risk_type': risk_names[i],
                'risk_level': assessment['risk_level'],
                'priority_rank': risk_levels[assessment['risk_level']]
            })
        
        return sorted(risks, key=lambda x: x['priority_rank'], reverse=True)
    
    def _identify_stakeholders(self, location: str, project_type: str) -> List[Dict[str, Any]]:
        """Identify key stakeholders"""
        return [
            {'group': 'Local Residents', 'influence': 'high', 'interest': 'high'},
            {'group': 'Local Businesses', 'influence': 'medium', 'interest': 'high'},
            {'group': 'Government Authorities', 'influence': 'high', 'interest': 'medium'},
            {'group': 'Environmental Groups', 'influence': 'medium', 'interest': 'high'},
            {'group': 'Workers and Unions', 'influence': 'medium', 'interest': 'medium'}
        ]
    
    def _develop_engagement_activities(self, project_type: str, duration: int) -> List[Dict[str, Any]]:
        """Develop stakeholder engagement activities"""
        return [
            {'activity': 'Public Information Sessions', 'frequency': 'Monthly', 'duration': 'Throughout project'},
            {'activity': 'Community Advisory Committee', 'frequency': 'Quarterly', 'duration': 'Throughout project'},
            {'activity': 'Grievance Hotline', 'frequency': '24/7', 'duration': 'Throughout project'},
            {'activity': 'Environmental Monitoring Reports', 'frequency': 'Quarterly', 'duration': 'Throughout project'}
        ]
    
    def _create_communication_plan(self, stakeholders: List[Dict], duration: int) -> Dict[str, Any]:
        """Create communication plan"""
        return {
            'communication_channels': ['Website', 'Email', 'SMS', 'Local newspapers', 'Community meetings'],
            'key_messages': ['Project benefits', 'Environmental commitments', 'Safety measures'],
            'frequency': 'Monthly updates, immediate for issues',
            'languages': ['English', 'Arabic'],
            'feedback_mechanisms': ['Online form', 'Hotline', 'Email', 'In-person meetings']
        }
    
    def _design_grievance_mechanism(self) -> Dict[str, Any]:
        """Design grievance mechanism"""
        return {
            'reporting_channels': ['Hotline', 'Email', 'Online form', 'In-person'],
            'response_timeframes': {'acknowledgment': '24 hours', 'investigation': '7 days', 'resolution': '30 days'},
            'escalation_process': 'Project Manager → Senior Management → External mediator',
            'confidentiality': 'Assured for all complainants',
            'no_retaliation_policy': 'Strictly enforced'
        }
    
    def _design_engagement_monitoring(self) -> Dict[str, Any]:
        """Design engagement monitoring and evaluation"""
        return {
            'participation_metrics': ['Meeting attendance', 'Feedback volume', 'Stakeholder satisfaction'],
            'effectiveness_indicators': ['Response rates', 'Issue resolution time', 'Stakeholder feedback scores'],
            'reporting_frequency': 'Quarterly',
            'evaluation_methods': ['Surveys', 'Focus groups', 'Feedback analysis']
        }
    
    def _estimate_engagement_budget(self, activities: List[Dict], duration: int) -> float:
        """Estimate community engagement budget"""
        base_annual_cost = 50000  # USD
        return base_annual_cost * (duration / 12)
    
    def _define_engagement_success_indicators(self) -> List[str]:
        """Define community engagement success indicators"""
        return [
            "95% stakeholder awareness of project",
            "Less than 5 unresolved grievances per quarter",
            "80% stakeholder satisfaction rate",
            "100% response rate to grievances within timeframe",
            "Zero escalations to external mediators"
        ]
    
    def _assess_route_impact(self, daily_vehicles: int) -> str:
        """Assess impact on traffic routes"""
        if daily_vehicles > 200:
            return 'high'
        elif daily_vehicles > 100:
            return 'moderate'
        else:
            return 'low'
    
    def _assess_road_wear(self, daily_trucks: int) -> str:
        """Assess road wear impact from heavy vehicles"""
        if daily_trucks > 50:
            return 'significant'
        elif daily_trucks > 20:
            return 'moderate'
        else:
            return 'minimal'
    
    def _calculate_trip_distribution(self, project_type: str) -> Dict[str, float]:
        """Calculate trip distribution by direction"""
        return {
            'north': 0.25,
            'south': 0.25,
            'east': 0.25,
            'west': 0.25
        }
    
    def _calculate_mode_split(self, project_type: str) -> Dict[str, float]:
        """Calculate transportation mode split"""
        return {
            'private_vehicle': 0.75,
            'public_transport': 0.15,
            'walking_cycling': 0.08,
            'taxi_rideshare': 0.02
        }
    
    def _recommend_traffic_improvements(self, analysis: Dict) -> List[str]:
        """Recommend traffic improvements"""
        recommendations = []
        
        if not analysis['construction_peak']['acceptable']:
            recommendations.extend([
                "Implement temporary traffic signals",
                "Provide construction traffic escorts",
                "Restrict heavy vehicle hours"
            ])
        
        if not analysis['operational']['acceptable']:
            recommendations.extend([
                "Upgrade intersection capacity",
                "Add dedicated turning lanes",
                "Improve public transport connectivity"
            ])
        
        return recommendations
    
    def _assess_public_transport_impact(self, operational_traffic: Dict, location: str) -> Dict[str, Any]:
        """Assess impact on public transport"""
        return {
            'bus_route_impact': 'minimal',
            'metro_impact': 'none',
            'additional_capacity_required': False,
            'service_frequency_impact': 'none',
            'accessibility_improvement_opportunities': [
                'Bus stop upgrades',
                'Pedestrian connectivity improvements'
            ]
        }
    
    def _assess_traffic_safety(self, construction_traffic: Dict, operational_traffic: Dict, project_type: str) -> Dict[str, Any]:
        """Assess traffic safety impacts"""
        return {
            'accident_risk_increase': 'low',
            'pedestrian_safety_concerns': ['Construction vehicle movements', 'Increased traffic volume'],
            'cyclist_safety_concerns': ['Heavy vehicle interactions'],
            'school_zone_impacts': 'minimal',
            'safety_measures_required': [
                'Enhanced signage and markings',
                'Pedestrian crossing improvements',
                'Speed control measures'
            ]
        }
    
    def _get_traffic_monitoring_requirements(self) -> List[str]:
        """Get traffic monitoring requirements"""
        return [
            "Pre-construction traffic counts",
            "Monthly traffic volume monitoring during construction",
            "Annual traffic impact assessment during operations",
            "Accident monitoring and reporting",
            "Level of service assessment annually"
        ]