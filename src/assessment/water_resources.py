"""
Comprehensive Water Resources Assessment Module
Professional water impact assessment for construction and operational phases

Created by: Edy Bassil
Email: bassileddy@gmail.com
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import math

class WaterSource(Enum):
    """Water source types in UAE/KSA"""
    MUNICIPAL_SUPPLY = "municipal_supply"
    DESALINATED = "desalinated"
    GROUNDWATER = "groundwater"
    RECYCLED = "recycled"
    BRACKISH = "brackish"

class WastewaterType(Enum):
    """Wastewater categories"""
    DOMESTIC = "domestic"
    INDUSTRIAL = "industrial"
    STORMWATER = "stormwater"
    CONSTRUCTION = "construction"

@dataclass
class WaterDemand:
    """Water demand calculation"""
    demand_type: str
    daily_demand: float  # m³/day
    peak_demand: float   # m³/day
    annual_demand: float # m³/year
    source_required: WaterSource
    quality_standard: str

@dataclass
class WastewaterGeneration:
    """Wastewater generation data"""
    wastewater_type: WastewaterType
    daily_generation: float  # m³/day
    annual_generation: float # m³/year
    treatment_required: bool
    treatment_level: str
    discharge_method: str

@dataclass
class WaterBalance:
    """Complete water balance"""
    total_demand: float
    total_supply_capacity: float
    wastewater_generation: float
    recycled_water_potential: float
    water_efficiency_ratio: float
    sustainability_score: float

class WaterResourcesAssessment:
    """Comprehensive water resources impact assessment"""
    
    def __init__(self):
        self.regional_standards = self._initialize_regional_standards()
        self.water_consumption_rates = self._initialize_consumption_rates()
        self.treatment_requirements = self._initialize_treatment_requirements()
    
    def _initialize_regional_standards(self) -> Dict[str, Dict]:
        """Initialize regional water standards and regulations"""
        return {
            "uae": {
                "water_consumption_limits": {
                    "residential": 300,    # L/person/day (UAE target)
                    "commercial": 50,      # L/m²/day
                    "industrial": 30,      # L/m²/day
                    "irrigation": 5.0      # L/m²/day
                },
                "wastewater_standards": {
                    "bod_discharge": 20,   # mg/L for treated effluent
                    "tss_discharge": 30,   # mg/L
                    "nitrogen_limit": 10,  # mg/L
                    "phosphorus_limit": 5  # mg/L
                },
                "recycling_targets": {
                    "treated_sewage_effluent": 0.80,  # 80% reuse target
                    "construction_water": 0.60,
                    "cooling_water": 0.90
                },
                "groundwater_protection": {
                    "drawdown_limit": 5.0,  # meters
                    "quality_monitoring": True,
                    "permit_required": True
                }
            },
            "ksa": {
                "water_consumption_limits": {
                    "residential": 250,    # L/person/day (KSA target)
                    "commercial": 40,      # L/m²/day
                    "industrial": 25,      # L/m²/day
                    "irrigation": 4.0      # L/m²/day
                },
                "wastewater_standards": {
                    "bod_discharge": 25,   # mg/L
                    "tss_discharge": 35,   # mg/L
                    "nitrogen_limit": 15,  # mg/L
                    "phosphorus_limit": 8  # mg/L
                },
                "recycling_targets": {
                    "treated_sewage_effluent": 0.70,
                    "construction_water": 0.50,
                    "cooling_water": 0.85
                },
                "groundwater_protection": {
                    "drawdown_limit": 3.0,
                    "quality_monitoring": True,
                    "permit_required": True
                }
            }
        }
    
    def _initialize_consumption_rates(self) -> Dict[str, Dict]:
        """Initialize water consumption rates by project type"""
        return {
            "construction_phase": {
                "concrete_production": 0.15,    # m³/m³ concrete
                "dust_suppression": 2.0,        # L/m²/day
                "equipment_washing": 0.5,       # m³/day per equipment
                "worker_facilities": 150,       # L/person/day
                "curing_concrete": 0.05,        # m³/m² over 28 days
                "compaction": 0.02,             # m³/m²
                "landscaping_establishment": 10  # L/m²/day for first 6 months
            },
            "operational_phase": {
                "domestic_use": {
                    "residential": 250,     # L/person/day
                    "office": 50,          # L/person/day
                    "retail": 30,          # L/person/day
                    "hotel": 400,          # L/person/day
                    "restaurant": 80       # L/person/day
                },
                "non_domestic": {
                    "irrigation": 5.0,     # L/m²/day (landscaped area)
                    "cooling_tower": 2.0,  # L/m²/day (conditioned area)
                    "cleaning": 1.0,       # L/m²/week
                    "fire_protection": 0.1, # m³/m² (storage requirement)
                    "swimming_pool": 50    # L/m²/day (pool area)
                }
            }
        }
    
    def _initialize_treatment_requirements(self) -> Dict[str, Dict]:
        """Initialize wastewater treatment requirements"""
        return {
            "primary_treatment": {
                "removal_efficiency": {
                    "tss": 0.60,
                    "bod": 0.30,
                    "nitrogen": 0.10,
                    "phosphorus": 0.15
                },
                "cost_per_m3": 0.5,  # USD
                "energy_kwh_per_m3": 0.3
            },
            "secondary_treatment": {
                "removal_efficiency": {
                    "tss": 0.85,
                    "bod": 0.85,
                    "nitrogen": 0.30,
                    "phosphorus": 0.30
                },
                "cost_per_m3": 1.2,
                "energy_kwh_per_m3": 0.6
            },
            "tertiary_treatment": {
                "removal_efficiency": {
                    "tss": 0.95,
                    "bod": 0.95,
                    "nitrogen": 0.70,
                    "phosphorus": 0.80
                },
                "cost_per_m3": 2.5,
                "energy_kwh_per_m3": 1.2
            },
            "membrane_treatment": {
                "removal_efficiency": {
                    "tss": 0.99,
                    "bod": 0.98,
                    "nitrogen": 0.85,
                    "phosphorus": 0.95
                },
                "cost_per_m3": 4.0,
                "energy_kwh_per_m3": 2.5
            }
        }
    
    def assess_construction_water_demand(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess construction phase water demand"""
        
        project_size = float(project_data.get('size', 10000))  # m²
        project_type = project_data.get('type', 'residential').lower()
        location = project_data.get('location', 'Dubai').lower()
        duration = int(project_data.get('duration', 24))  # months
        workers = int(project_data.get('workers', project_size / 50))  # Estimate workers
        
        # Get regional standards
        region = 'uae' if any(x in location for x in ['dubai', 'abu dhabi', 'sharjah']) else 'ksa'
        
        construction_rates = self.water_consumption_rates['construction_phase']
        
        # Calculate different water uses
        water_demands = {}
        
        # 1. Concrete production (assume 0.15 m³ concrete per m² floor area)
        concrete_volume = project_size * 0.15
        concrete_water = concrete_volume * construction_rates['concrete_production']
        water_demands['concrete_production'] = {
            'total_demand': concrete_water,
            'daily_average': concrete_water / (duration * 30),
            'peak_demand': concrete_water / (duration * 30) * 1.5,
            'description': 'Water for concrete mixing and production'
        }
        
        # 2. Dust suppression
        dust_suppression_daily = (project_size * construction_rates['dust_suppression']) / 1000
        dust_suppression_total = dust_suppression_daily * duration * 30
        water_demands['dust_suppression'] = {
            'total_demand': dust_suppression_total,
            'daily_average': dust_suppression_daily,
            'peak_demand': dust_suppression_daily * 2.0,  # Hot/windy days
            'description': 'Water for dust control and suppression'
        }
        
        # 3. Worker facilities
        worker_water_daily = (workers * construction_rates['worker_facilities']) / 1000
        worker_water_total = worker_water_daily * duration * 30
        water_demands['worker_facilities'] = {
            'total_demand': worker_water_total,
            'daily_average': worker_water_daily,
            'peak_demand': worker_water_daily * 1.2,
            'description': 'Water for worker toilets, washing, and drinking'
        }
        
        # 4. Equipment washing
        equipment_count = max(int(project_size / 5000), 5)
        equipment_water_daily = equipment_count * construction_rates['equipment_washing']
        equipment_water_total = equipment_water_daily * duration * 30
        water_demands['equipment_washing'] = {
            'total_demand': equipment_water_total,
            'daily_average': equipment_water_daily,
            'peak_demand': equipment_water_daily * 1.5,
            'description': 'Water for cleaning construction equipment'
        }
        
        # 5. Concrete curing
        curing_water = project_size * construction_rates['curing_concrete']
        water_demands['concrete_curing'] = {
            'total_demand': curing_water,
            'daily_average': curing_water / (28 * 3),  # Spread over multiple pours
            'peak_demand': curing_water / (28 * 2),
            'description': 'Water for concrete curing and cooling'
        }
        
        # 6. Landscaping establishment (last 6 months)
        landscape_area = project_size * 0.3  # Assume 30% landscaped
        landscape_daily = (landscape_area * construction_rates['landscaping_establishment']) / 1000
        landscape_total = landscape_daily * 6 * 30  # 6 months
        water_demands['landscaping'] = {
            'total_demand': landscape_total,
            'daily_average': landscape_daily,
            'peak_demand': landscape_daily * 1.8,  # Summer peak
            'description': 'Water for establishing landscaping'
        }
        
        # Calculate totals
        total_demand = sum(demand['total_demand'] for demand in water_demands.values())
        daily_average = sum(demand['daily_average'] for demand in water_demands.values())
        peak_demand = sum(demand['peak_demand'] for demand in water_demands.values())
        
        # Water source recommendations
        water_sources = self._recommend_construction_water_sources(
            daily_average, peak_demand, location
        )
        
        # Calculate costs
        water_costs = self._calculate_construction_water_costs(
            total_demand, water_sources, region
        )
        
        return {
            'phase': 'construction',
            'duration_months': duration,
            'total_demand_m3': round(total_demand, 1),
            'daily_average_m3': round(daily_average, 1),
            'peak_demand_m3': round(peak_demand, 1),
            'water_intensity': round(total_demand / project_size, 3),  # m³/m²
            'detailed_demands': water_demands,
            'recommended_sources': water_sources,
            'estimated_costs': water_costs,
            'water_efficiency_measures': self._get_construction_efficiency_measures()
        }
    
    def assess_operational_water_demand(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess operational phase water demand"""
        
        project_size = float(project_data.get('size', 10000))
        project_type = project_data.get('type', 'residential').lower()
        location = project_data.get('location', 'Dubai').lower()
        
        # Get regional standards
        region = 'uae' if any(x in location for x in ['dubai', 'abu dhabi', 'sharjah']) else 'ksa'
        
        # Calculate occupancy
        occupancy = self._calculate_occupancy(project_size, project_type)
        
        operational_rates = self.water_consumption_rates['operational_phase']
        
        # Calculate water demands
        water_demands = {}
        
        # 1. Domestic water use
        if project_type in operational_rates['domestic_use']:
            domestic_rate = operational_rates['domestic_use'][project_type]
        else:
            domestic_rate = operational_rates['domestic_use']['residential']
        
        domestic_daily = (occupancy * domestic_rate) / 1000  # Convert to m³
        domestic_annual = domestic_daily * 365
        
        water_demands['domestic_use'] = {
            'daily_demand': domestic_daily,
            'annual_demand': domestic_annual,
            'peak_demand': domestic_daily * 1.5,  # Peak day factor
            'source': WaterSource.MUNICIPAL_SUPPLY,
            'description': 'Potable water for drinking, cooking, bathing, etc.'
        }
        
        # 2. Irrigation (landscaped areas)
        landscape_area = project_size * 0.3  # Assume 30% landscaped
        irrigation_daily = (landscape_area * operational_rates['non_domestic']['irrigation']) / 1000
        irrigation_annual = irrigation_daily * 365
        
        water_demands['irrigation'] = {
            'daily_demand': irrigation_daily,
            'annual_demand': irrigation_annual,
            'peak_demand': irrigation_daily * 2.0,  # Summer peak
            'source': WaterSource.RECYCLED,
            'description': 'Water for landscape irrigation and green areas'
        }
        
        # 3. Cooling system (if applicable)
        if project_type in ['commercial', 'industrial', 'mixed_use']:
            cooling_daily = (project_size * operational_rates['non_domestic']['cooling_tower']) / 1000
            cooling_annual = cooling_daily * 365
            
            water_demands['cooling_system'] = {
                'daily_demand': cooling_daily,
                'annual_demand': cooling_annual,
                'peak_demand': cooling_daily * 1.8,  # Summer peak
                'source': WaterSource.RECYCLED,
                'description': 'Water for HVAC cooling towers and systems'
            }
        
        # 4. Cleaning and maintenance
        cleaning_weekly = (project_size * operational_rates['non_domestic']['cleaning']) / 1000
        cleaning_daily = cleaning_weekly / 7
        cleaning_annual = cleaning_daily * 365
        
        water_demands['cleaning'] = {
            'daily_demand': cleaning_daily,
            'annual_demand': cleaning_annual,
            'peak_demand': cleaning_daily * 2.0,
            'source': WaterSource.RECYCLED,
            'description': 'Water for cleaning and maintenance activities'
        }
        
        # 5. Fire protection (storage requirement)
        fire_protection_storage = project_size * operational_rates['non_domestic']['fire_protection']
        
        water_demands['fire_protection'] = {
            'storage_requirement': fire_protection_storage,
            'annual_demand': fire_protection_storage * 0.1,  # 10% annual turnover
            'daily_demand': fire_protection_storage * 0.1 / 365,
            'source': WaterSource.MUNICIPAL_SUPPLY,
            'description': 'Water storage for fire protection systems'
        }
        
        # Calculate totals
        total_daily = sum(
            demand.get('daily_demand', 0) for demand in water_demands.values()
        )
        total_annual = sum(
            demand.get('annual_demand', 0) for demand in water_demands.values()
        )
        peak_daily = sum(
            demand.get('peak_demand', demand.get('daily_demand', 0)) 
            for demand in water_demands.values()
        )
        
        # Water source allocation
        source_allocation = self._allocate_water_sources(water_demands, region)
        
        # Calculate costs
        annual_costs = self._calculate_operational_water_costs(
            water_demands, source_allocation, region
        )
        
        return {
            'phase': 'operational',
            'occupancy': occupancy,
            'daily_total_m3': round(total_daily, 1),
            'annual_total_m3': round(total_annual, 1),
            'peak_daily_m3': round(peak_daily, 1),
            'per_capita_consumption': round((total_daily * 1000) / occupancy, 1),  # L/person/day
            'water_intensity': round(total_annual / project_size, 3),  # m³/m²/year
            'detailed_demands': water_demands,
            'source_allocation': source_allocation,
            'annual_costs': annual_costs,
            'efficiency_measures': self._get_operational_efficiency_measures(region)
        }
    
    def assess_wastewater_generation(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess wastewater generation and treatment requirements"""
        
        project_size = float(project_data.get('size', 10000))
        project_type = project_data.get('type', 'residential').lower()
        location = project_data.get('location', 'Dubai').lower()
        
        # Get regional standards
        region = 'uae' if any(x in location for x in ['dubai', 'abu dhabi', 'sharjah']) else 'ksa'
        
        # Get operational water demand
        water_demand = self.assess_operational_water_demand(project_data)
        
        wastewater_streams = {}
        
        # 1. Domestic wastewater (80% of domestic water consumption)
        domestic_water = water_demand['detailed_demands']['domestic_use']['daily_demand']
        domestic_wastewater = domestic_water * 0.80
        
        wastewater_streams['domestic'] = {
            'daily_generation': domestic_wastewater,
            'annual_generation': domestic_wastewater * 365,
            'wastewater_type': WastewaterType.DOMESTIC,
            'treatment_level': 'secondary',
            'reuse_potential': 0.85,
            'discharge_standard': self.regional_standards[region]['wastewater_standards']
        }
        
        # 2. Cooling tower blowdown (if applicable)
        if 'cooling_system' in water_demand['detailed_demands']:
            cooling_water = water_demand['detailed_demands']['cooling_system']['daily_demand']
            cooling_wastewater = cooling_water * 0.20  # 20% blowdown
            
            wastewater_streams['cooling_blowdown'] = {
                'daily_generation': cooling_wastewater,
                'annual_generation': cooling_wastewater * 365,
                'wastewater_type': WastewaterType.INDUSTRIAL,
                'treatment_level': 'primary',
                'reuse_potential': 0.60,
                'special_considerations': 'High TDS, may require specialized treatment'
            }
        
        # 3. Stormwater runoff
        rainfall_annual = 100 if region == 'uae' else 80  # mm/year average
        runoff_coefficient = 0.85  # For developed areas
        stormwater_annual = (project_size * rainfall_annual * runoff_coefficient) / 1000000  # m³
        
        wastewater_streams['stormwater'] = {
            'daily_generation': stormwater_annual / 365,
            'annual_generation': stormwater_annual,
            'wastewater_type': WastewaterType.STORMWATER,
            'treatment_level': 'primary',
            'reuse_potential': 0.90,
            'seasonal_variation': 'High - concentrated in winter months'
        }
        
        # Calculate totals
        total_daily = sum(stream['daily_generation'] for stream in wastewater_streams.values())
        total_annual = sum(stream['annual_generation'] for stream in wastewater_streams.values())
        
        # Treatment requirements and costs
        treatment_plan = self._develop_treatment_plan(wastewater_streams, region)
        
        # Reuse potential assessment
        reuse_assessment = self._assess_reuse_potential(wastewater_streams, water_demand)
        
        return {
            'daily_total_m3': round(total_daily, 1),
            'annual_total_m3': round(total_annual, 1),
            'wastewater_streams': wastewater_streams,
            'treatment_plan': treatment_plan,
            'reuse_potential': reuse_assessment,
            'regulatory_requirements': self._get_wastewater_regulations(region),
            'environmental_benefits': self._calculate_environmental_benefits(reuse_assessment)
        }
    
    def create_water_balance(self, project_data: Dict[str, Any]) -> WaterBalance:
        """Create comprehensive water balance"""
        
        construction_demand = self.assess_construction_water_demand(project_data)
        operational_demand = self.assess_operational_water_demand(project_data)
        wastewater_assessment = self.assess_wastewater_generation(project_data)
        
        location = project_data.get('location', 'Dubai').lower()
        region = 'uae' if any(x in location for x in ['dubai', 'abu dhabi', 'sharjah']) else 'ksa'
        
        # Calculate annual operational demand
        annual_demand = operational_demand['annual_total_m3']
        
        # Calculate available supply capacity
        municipal_supply_capacity = annual_demand * 1.2  # Assume 20% excess capacity needed
        
        # Calculate wastewater generation
        annual_wastewater = wastewater_assessment['annual_total_m3']
        
        # Calculate recycled water potential
        recycled_potential = sum(
            stream['annual_generation'] * stream.get('reuse_potential', 0)
            for stream in wastewater_assessment['wastewater_streams'].values()
        )
        
        # Calculate water efficiency ratio
        water_efficiency = recycled_potential / annual_demand if annual_demand > 0 else 0
        
        # Calculate sustainability score
        sustainability_score = self._calculate_sustainability_score(
            annual_demand, recycled_potential, region
        )
        
        return WaterBalance(
            total_demand=annual_demand,
            total_supply_capacity=municipal_supply_capacity,
            wastewater_generation=annual_wastewater,
            recycled_water_potential=recycled_potential,
            water_efficiency_ratio=water_efficiency,
            sustainability_score=sustainability_score
        )
    
    def _calculate_occupancy(self, project_size: float, project_type: str) -> int:
        """Calculate project occupancy"""
        occupancy_rates = {
            'residential': 30,      # m²/person
            'commercial': 15,       # m²/person
            'industrial': 50,       # m²/person
            'infrastructure': 100,  # m²/person
            'mixed_use': 25        # m²/person
        }
        
        rate = occupancy_rates.get(project_type, 30)
        return max(int(project_size / rate), 10)
    
    def _recommend_construction_water_sources(self, daily_demand: float, peak_demand: float, location: str) -> List[Dict]:
        """Recommend water sources for construction"""
        sources = []
        
        # Municipal supply for potable needs
        sources.append({
            'source': 'Municipal Supply',
            'allocation_percentage': 40,
            'daily_capacity': daily_demand * 0.4,
            'use_case': 'Worker facilities, concrete mixing (partial)',
            'cost_per_m3': 2.5 if 'uae' in location else 1.8,
            'reliability': 'High'
        })
        
        # Recycled water for non-potable uses
        sources.append({
            'source': 'Recycled/Treated Wastewater',
            'allocation_percentage': 35,
            'daily_capacity': daily_demand * 0.35,
            'use_case': 'Dust suppression, equipment washing, concrete curing',
            'cost_per_m3': 1.2 if 'uae' in location else 0.8,
            'reliability': 'Medium'
        })
        
        # Groundwater (where permitted)
        sources.append({
            'source': 'Groundwater',
            'allocation_percentage': 25,
            'daily_capacity': daily_demand * 0.25,
            'use_case': 'Dust suppression, compaction',
            'cost_per_m3': 1.8 if 'uae' in location else 1.2,
            'reliability': 'Medium',
            'permit_required': True
        })
        
        return sources
    
    def _allocate_water_sources(self, water_demands: Dict, region: str) -> Dict[str, Dict]:
        """Allocate water sources for operational demands"""
        allocation = {}
        
        for demand_type, demand_data in water_demands.items():
            source = demand_data.get('source', WaterSource.MUNICIPAL_SUPPLY)
            
            if source == WaterSource.MUNICIPAL_SUPPLY:
                cost_per_m3 = 2.5 if region == 'uae' else 1.8
            elif source == WaterSource.RECYCLED:
                cost_per_m3 = 1.2 if region == 'uae' else 0.8
            else:
                cost_per_m3 = 2.0
            
            allocation[demand_type] = {
                'source': source.value,
                'annual_volume': demand_data.get('annual_demand', 0),
                'cost_per_m3': cost_per_m3,
                'annual_cost': demand_data.get('annual_demand', 0) * cost_per_m3
            }
        
        return allocation
    
    def _calculate_construction_water_costs(self, total_demand: float, sources: List[Dict], region: str) -> Dict[str, float]:
        """Calculate construction water costs"""
        total_cost = 0
        for source in sources:
            volume = total_demand * (source['allocation_percentage'] / 100)
            cost = volume * source['cost_per_m3']
            total_cost += cost
        
        return {
            'total_water_cost': round(total_cost, 0),
            'cost_per_m3_average': round(total_cost / total_demand, 2) if total_demand > 0 else 0,
            'infrastructure_cost': round(total_cost * 0.15, 0),  # 15% for infrastructure
            'total_cost_including_infrastructure': round(total_cost * 1.15, 0)
        }
    
    def _calculate_operational_water_costs(self, water_demands: Dict, source_allocation: Dict, region: str) -> Dict[str, float]:
        """Calculate annual operational water costs"""
        total_annual_cost = sum(allocation['annual_cost'] for allocation in source_allocation.values())
        total_volume = sum(allocation['annual_volume'] for allocation in source_allocation.values())
        
        return {
            'annual_water_cost': round(total_annual_cost, 0),
            'cost_per_m3_average': round(total_annual_cost / total_volume, 2) if total_volume > 0 else 0,
            'monthly_average': round(total_annual_cost / 12, 0),
            'lifecycle_cost_20_years': round(total_annual_cost * 20, 0)
        }
    
    def _develop_treatment_plan(self, wastewater_streams: Dict, region: str) -> Dict[str, Any]:
        """Develop wastewater treatment plan"""
        treatment_plan = {
            'treatment_systems': [],
            'total_capacity': 0,
            'annual_operating_cost': 0,
            'capital_cost_estimate': 0
        }
        
        for stream_type, stream_data in wastewater_streams.items():
            if stream_data['wastewater_type'] == WastewaterType.DOMESTIC:
                treatment_level = 'secondary_treatment'
            elif stream_data['wastewater_type'] == WastewaterType.STORMWATER:
                treatment_level = 'primary_treatment'
            else:
                treatment_level = 'tertiary_treatment'
            
            treatment_requirements = self.treatment_requirements[treatment_level]
            annual_volume = stream_data['annual_generation']
            
            system = {
                'stream_type': stream_type,
                'treatment_level': treatment_level,
                'annual_volume': annual_volume,
                'annual_cost': annual_volume * treatment_requirements['cost_per_m3'],
                'energy_requirement': annual_volume * treatment_requirements['energy_kwh_per_m3'],
                'removal_efficiency': treatment_requirements['removal_efficiency']
            }
            
            treatment_plan['treatment_systems'].append(system)
            treatment_plan['total_capacity'] += annual_volume
            treatment_plan['annual_operating_cost'] += system['annual_cost']
        
        # Estimate capital cost (10x annual operating cost)
        treatment_plan['capital_cost_estimate'] = treatment_plan['annual_operating_cost'] * 10
        
        return treatment_plan
    
    def _assess_reuse_potential(self, wastewater_streams: Dict, water_demand: Dict) -> Dict[str, Any]:
        """Assess water reuse potential"""
        total_reusable = sum(
            stream['annual_generation'] * stream.get('reuse_potential', 0)
            for stream in wastewater_streams.values()
        )
        
        total_non_potable_demand = 0
        for demand_type, demand_data in water_demand['detailed_demands'].items():
            if demand_data.get('source') == WaterSource.RECYCLED:
                total_non_potable_demand += demand_data.get('annual_demand', 0)
        
        reuse_percentage = min(total_reusable / total_non_potable_demand * 100, 100) if total_non_potable_demand > 0 else 0
        
        return {
            'total_reusable_m3': round(total_reusable, 1),
            'non_potable_demand_m3': round(total_non_potable_demand, 1),
            'reuse_percentage': round(reuse_percentage, 1),
            'water_savings_m3': round(min(total_reusable, total_non_potable_demand), 1),
            'cost_savings_annual': round(min(total_reusable, total_non_potable_demand) * 1.5, 0)  # Savings vs municipal water
        }
    
    def _get_construction_efficiency_measures(self) -> List[str]:
        """Get water efficiency measures for construction"""
        return [
            "Implement closed-loop concrete washing systems",
            "Use recycled water for dust suppression where possible",
            "Install water meters on all major uses",
            "Implement rainwater harvesting for non-potable uses",
            "Use drought-resistant plants for landscaping",
            "Optimize concrete mix designs to reduce water content",
            "Implement leak detection and repair programs",
            "Train workers on water conservation practices"
        ]
    
    def _get_operational_efficiency_measures(self, region: str) -> List[str]:
        """Get water efficiency measures for operations"""
        base_measures = [
            "Install low-flow fixtures and water-efficient appliances",
            "Implement greywater recycling systems",
            "Use drought-resistant landscaping (xeriscaping)",
            "Install smart irrigation systems with weather sensors",
            "Implement cooling tower water management",
            "Regular leak detection and repair programs",
            "Water usage monitoring and reporting systems"
        ]
        
        if region == 'uae':
            base_measures.extend([
                "Achieve ESTIDAMA water efficiency credits",
                "Install desalinated water systems for potable use",
                "Implement district cooling connections where available"
            ])
        else:  # KSA
            base_measures.extend([
                "Comply with KSA Water Efficiency Standards",
                "Install atmospheric water generation systems",
                "Implement solar-powered water heating systems"
            ])
        
        return base_measures
    
    def _get_wastewater_regulations(self, region: str) -> List[str]:
        """Get wastewater regulatory requirements"""
        if region == 'uae':
            return [
                "UAE Federal Law No. 24 of 1999 - Water Pollution Control",
                "Local municipality wastewater discharge standards",
                "ADWEC/DEWA connection and discharge permits",
                "Industrial wastewater pre-treatment requirements",
                "Greywater reuse system approvals"
            ]
        else:  # KSA
            return [
                "KSA Environmental Law - Water Quality Protection",
                "Municipal wastewater connection permits",
                "Industrial discharge permit requirements",
                "Water reuse and recycling approvals",
                "Environmental monitoring and reporting"
            ]
    
    def _calculate_environmental_benefits(self, reuse_assessment: Dict) -> Dict[str, Any]:
        """Calculate environmental benefits of water reuse"""
        water_savings = reuse_assessment['water_savings_m3']
        
        return {
            'freshwater_conservation': f"{water_savings:,.0f} m³/year",
            'equivalent_households': round(water_savings / 150, 0),  # Assuming 150 m³/household/year
            'energy_savings_kwh': round(water_savings * 3.5, 0),  # 3.5 kWh per m³ for treatment/distribution
            'co2_reduction_tons': round(water_savings * 0.002, 1),  # 0.002 tons CO2 per m³
            'ecosystem_protection': "Reduced pressure on groundwater and natural water bodies"
        }
    
    def _calculate_sustainability_score(self, annual_demand: float, recycled_potential: float, region: str) -> float:
        """Calculate water sustainability score (0-100)"""
        # Base score factors
        recycling_ratio = recycled_potential / annual_demand if annual_demand > 0 else 0
        
        # Regional targets
        if region == 'uae':
            target_recycling = 0.50  # 50% target
            efficiency_target = 250   # L/person/day target
        else:  # KSA
            target_recycling = 0.40  # 40% target
            efficiency_target = 200   # L/person/day target
        
        # Calculate score components
        recycling_score = min(recycling_ratio / target_recycling * 50, 50)
        efficiency_score = 30  # Base efficiency score
        technology_score = 20  # Modern technology implementation
        
        total_score = recycling_score + efficiency_score + technology_score
        
        return round(min(total_score, 100), 1)