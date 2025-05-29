"""
Water Resources Impact Analysis
Comprehensive water impact assessment for construction projects

Author: Edy Bassil
Email: bassileddy@gmail.com
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import logging
import numpy as np
from enum import Enum

logger = logging.getLogger(__name__)


class WaterSourceType(Enum):
    """Types of water sources."""
    GROUNDWATER = "groundwater"
    SURFACE_WATER = "surface_water"
    MUNICIPAL = "municipal"
    RECYCLED = "recycled"
    DESALINATED = "desalinated"
    RAINWATER = "rainwater"


class WaterQualityParameter(Enum):
    """Water quality parameters."""
    PH = "ph"
    TDS = "tds"  # Total Dissolved Solids
    TSS = "tss"  # Total Suspended Solids
    BOD = "bod"  # Biological Oxygen Demand
    COD = "cod"  # Chemical Oxygen Demand
    DO = "do"    # Dissolved Oxygen
    TURBIDITY = "turbidity"
    NITRATES = "nitrates"
    PHOSPHATES = "phosphates"
    HEAVY_METALS = "heavy_metals"
    COLIFORM = "coliform"
    TEMPERATURE = "temperature"


@dataclass
class WaterConsumption:
    """Water consumption data."""
    daily_average: float  # m³/day
    peak_demand: float    # m³/day
    total_project: float  # m³
    per_worker: float     # L/person/day
    per_area: float       # L/m²/day
    by_activity: Dict[str, float]
    by_source: Dict[str, float]


@dataclass
class WaterQualityImpact:
    """Water quality impact assessment."""
    parameter: str
    baseline_value: float
    predicted_value: float
    unit: str
    standard_limit: float
    impact_level: str  # Low, Medium, High
    exceeds_standard: bool


@dataclass
class WaterBalance:
    """Project water balance."""
    total_demand: float         # m³
    available_supply: float     # m³
    deficit_surplus: float      # m³
    recycled_water: float       # m³
    discharge_volume: float     # m³
    evaporation_loss: float     # m³
    conservation_potential: float  # m³


@dataclass
class WaterRiskAssessment:
    """Water-related risk assessment."""
    water_scarcity_risk: str    # Low, Medium, High, Extreme
    flooding_risk: str
    quality_degradation_risk: str
    regulatory_compliance_risk: str
    supply_reliability_risk: str
    cost_escalation_risk: str
    overall_risk_level: str
    mitigation_priority: List[str]


class WaterResourcesAnalyzer:
    """Analyzer for water resources impact assessment."""
    
    def __init__(self):
        # Regional water stress indices for UAE/KSA
        self.water_stress_indices = {
            'Dubai': 4.8,      # Extremely high
            'Abu Dhabi': 4.9,  # Extremely high
            'Sharjah': 4.7,    # Extremely high
            'Riyadh': 4.9,     # Extremely high
            'Jeddah': 4.6,     # Extremely high
            'NEOM': 3.5        # High (due to desalination plans)
        }
        
        # Water consumption benchmarks (m³/day)
        self.consumption_benchmarks = {
            'residential': {
                'domestic': 0.25,      # per person
                'irrigation': 0.15,    # per m² landscaping
                'pools': 0.5,         # per m² pool area
                'cooling': 0.1        # per ton cooling
            },
            'commercial': {
                'office': 0.05,       # per person
                'retail': 0.03,       # per m² GFA
                'hotel': 0.5,         # per room
                'restaurant': 0.8     # per seat
            },
            'industrial': {
                'light': 10,          # per facility
                'heavy': 50,          # per facility
                'cooling': 20,        # per MW
                'process': 30         # per production unit
            },
            'infrastructure': {
                'road': 0.02,         # per m² during construction
                'utilities': 0.05,    # per linear meter
                'earthworks': 0.1     # per m³ excavation
            },
            'construction': {
                'concrete': 0.15,     # per m³ concrete
                'dust_control': 0.02, # per m² site area
                'equipment': 0.5,     # per equipment unit
                'workers': 0.1        # per worker
            }
        }
        
        # Water quality standards (UAE/KSA)
        self.quality_standards = {
            'drinking': {
                'ph': (6.5, 8.5),
                'tds': 1000,  # mg/L
                'turbidity': 5,  # NTU
                'nitrates': 50,  # mg/L
                'coliform': 0  # per 100ml
            },
            'irrigation': {
                'ph': (6.0, 9.0),
                'tds': 2000,
                'tss': 100,
                'bod': 100,
                'sodium': 200
            },
            'discharge': {
                'ph': (6.0, 9.0),
                'tss': 50,
                'bod': 30,
                'cod': 100,
                'oil_grease': 10
            }
        }
    
    def calculate_water_consumption(
        self,
        project_type: str,
        project_size: float,
        duration_months: int,
        num_workers: int,
        activities: Dict[str, float],
        water_sources: Optional[Dict[str, float]] = None
    ) -> WaterConsumption:
        """
        Calculate total water consumption for project.
        
        Args:
            project_type: Type of project
            project_size: Project size in m²
            duration_months: Project duration
            num_workers: Number of workers
            activities: Activity quantities
            water_sources: Water source percentages
            
        Returns:
            Water consumption assessment
        """
        try:
            consumption_by_activity = {}
            total_daily = 0
            
            # Construction phase water consumption
            
            # Worker consumption
            worker_daily = num_workers * self.consumption_benchmarks['construction']['workers']
            consumption_by_activity['Workers'] = worker_daily
            total_daily += worker_daily
            
            # Dust control
            dust_control_area = activities.get('site_area', project_size)
            dust_daily = dust_control_area * self.consumption_benchmarks['construction']['dust_control']
            consumption_by_activity['Dust Control'] = dust_daily
            total_daily += dust_daily
            
            # Concrete works
            concrete_volume = activities.get('concrete_volume', 0)
            if concrete_volume > 0:
                concrete_days = activities.get('concrete_days', 90)
                concrete_daily = (concrete_volume * self.consumption_benchmarks['construction']['concrete']) / concrete_days
                consumption_by_activity['Concrete Works'] = concrete_daily
                total_daily += concrete_daily
            
            # Equipment washing
            num_equipment = activities.get('num_equipment', 10)
            equipment_daily = num_equipment * self.consumption_benchmarks['construction']['equipment']
            consumption_by_activity['Equipment'] = equipment_daily
            total_daily += equipment_daily
            
            # Project-specific consumption
            if project_type == 'residential':
                # Landscaping establishment
                landscape_area = activities.get('landscape_area', project_size * 0.2)
                landscape_daily = landscape_area * self.consumption_benchmarks['residential']['irrigation']
                consumption_by_activity['Landscaping'] = landscape_daily
                total_daily += landscape_daily
            
            elif project_type == 'commercial':
                # Testing and commissioning
                gfa = activities.get('gross_floor_area', project_size * 0.8)
                testing_daily = gfa * self.consumption_benchmarks['commercial']['office'] * 0.1
                consumption_by_activity['Testing'] = testing_daily
                total_daily += testing_daily
            
            elif project_type == 'infrastructure':
                # Road construction water
                road_area = activities.get('road_area', project_size * 0.5)
                road_daily = road_area * self.consumption_benchmarks['infrastructure']['road']
                consumption_by_activity['Road Works'] = road_daily
                total_daily += road_daily
            
            # Peak demand (1.5x average during hot months)
            peak_demand = total_daily * 1.5
            
            # Total project consumption
            total_days = duration_months * 30
            total_project = total_daily * total_days
            
            # Per capita and per area metrics
            per_worker = (total_daily / num_workers * 1000) if num_workers > 0 else 0
            per_area = (total_daily / project_size * 1000) if project_size > 0 else 0
            
            # Water sources breakdown
            if not water_sources:
                # Default water sources for UAE/KSA
                water_sources = {
                    'municipal': 0.4,
                    'tanker': 0.3,
                    'groundwater': 0.2,
                    'recycled': 0.1
                }
            
            consumption_by_source = {
                source: total_daily * percentage
                for source, percentage in water_sources.items()
            }
            
            return WaterConsumption(
                daily_average=total_daily,
                peak_demand=peak_demand,
                total_project=total_project,
                per_worker=per_worker,
                per_area=per_area,
                by_activity=consumption_by_activity,
                by_source=consumption_by_source
            )
            
        except Exception as e:
            logger.error(f"Water consumption calculation failed: {e}")
            raise
    
    def assess_water_quality_impact(
        self,
        baseline_quality: Dict[str, float],
        project_activities: List[str],
        discharge_volume: float,
        receiving_water_volume: float
    ) -> List[WaterQualityImpact]:
        """
        Assess impact on water quality.
        
        Args:
            baseline_quality: Baseline water quality parameters
            project_activities: List of project activities
            discharge_volume: Discharge volume (m³/day)
            receiving_water_volume: Receiving water body volume (m³)
            
        Returns:
            List of water quality impacts
        """
        impacts = []
        
        # Activity-specific pollutant loads
        pollutant_loads = {
            'excavation': {'tss': 500, 'turbidity': 100},
            'concrete': {'ph': 12, 'tss': 200, 'alkalinity': 1000},
            'dewatering': {'tss': 150, 'tds': 2000, 'iron': 5},
            'vehicle_washing': {'tss': 300, 'oil_grease': 50, 'cod': 500},
            'camp_domestic': {'bod': 200, 'cod': 400, 'nitrogen': 40, 'phosphorus': 10}
        }
        
        # Calculate dilution factor
        dilution_factor = receiving_water_volume / (receiving_water_volume + discharge_volume)
        
        # Assess each parameter
        for param_name, baseline_value in baseline_quality.items():
            # Calculate pollutant contribution from activities
            added_concentration = 0
            
            for activity in project_activities:
                if activity in pollutant_loads and param_name in pollutant_loads[activity]:
                    # Simple mixing model
                    pollutant_conc = pollutant_loads[activity][param_name]
                    added_concentration += pollutant_conc * discharge_volume / receiving_water_volume
            
            # Predicted concentration after mixing
            predicted_value = baseline_value * dilution_factor + added_concentration
            
            # Get applicable standard
            standard_limit = self._get_water_quality_standard(param_name, 'discharge')
            
            # Determine impact level
            if predicted_value <= baseline_value * 1.1:
                impact_level = "Low"
            elif predicted_value <= baseline_value * 1.5:
                impact_level = "Medium"
            else:
                impact_level = "High"
            
            exceeds_standard = predicted_value > standard_limit if standard_limit else False
            
            impacts.append(WaterQualityImpact(
                parameter=param_name,
                baseline_value=baseline_value,
                predicted_value=predicted_value,
                unit=self._get_parameter_unit(param_name),
                standard_limit=standard_limit or 0,
                impact_level=impact_level,
                exceeds_standard=exceeds_standard
            ))
        
        return impacts
    
    def calculate_water_balance(
        self,
        consumption: WaterConsumption,
        available_water: Dict[str, float],
        recycling_rate: float = 0.3,
        evaporation_rate: float = 0.05
    ) -> WaterBalance:
        """
        Calculate project water balance.
        
        Args:
            consumption: Water consumption data
            available_water: Available water by source (m³/day)
            recycling_rate: Fraction of water that can be recycled
            evaporation_rate: Evaporation loss rate
            
        Returns:
            Water balance assessment
        """
        # Total demand
        total_demand = consumption.daily_average
        
        # Total available supply
        available_supply = sum(available_water.values())
        
        # Recycled water potential
        recyclable_activities = ['dust_control', 'equipment_washing', 'concrete_curing']
        recyclable_volume = sum(
            volume for activity, volume in consumption.by_activity.items()
            if any(r in activity.lower() for r in recyclable_activities)
        )
        recycled_water = recyclable_volume * recycling_rate
        
        # Effective supply with recycling
        effective_supply = available_supply + recycled_water
        
        # Deficit or surplus
        deficit_surplus = effective_supply - total_demand
        
        # Discharge volume (wastewater)
        discharge_volume = total_demand * 0.8  # Assume 80% becomes wastewater
        
        # Evaporation losses
        evaporation_loss = total_demand * evaporation_rate
        
        # Conservation potential
        conservation_measures = {
            'efficient_fixtures': 0.15,
            'rainwater_harvesting': 0.1,
            'greywater_recycling': 0.2,
            'drip_irrigation': 0.3,
            'dust_suppressants': 0.2
        }
        
        conservation_potential = sum(
            consumption.by_activity.get(activity, 0) * reduction
            for activity, reduction in conservation_measures.items()
        )
        
        return WaterBalance(
            total_demand=total_demand,
            available_supply=available_supply,
            deficit_surplus=deficit_surplus,
            recycled_water=recycled_water,
            discharge_volume=discharge_volume,
            evaporation_loss=evaporation_loss,
            conservation_potential=conservation_potential
        )
    
    def assess_water_risks(
        self,
        location: str,
        water_balance: WaterBalance,
        quality_impacts: List[WaterQualityImpact],
        project_duration_months: int
    ) -> WaterRiskAssessment:
        """
        Assess water-related risks.
        
        Args:
            location: Project location
            water_balance: Water balance data
            quality_impacts: Water quality impacts
            project_duration_months: Project duration
            
        Returns:
            Water risk assessment
        """
        # Water scarcity risk based on location and balance
        stress_index = self.water_stress_indices.get(location, 4.5)
        deficit_ratio = abs(water_balance.deficit_surplus) / water_balance.total_demand if water_balance.deficit_surplus < 0 else 0
        
        if stress_index > 4 and deficit_ratio > 0.2:
            scarcity_risk = "Extreme"
        elif stress_index > 4 or deficit_ratio > 0.1:
            scarcity_risk = "High"
        elif stress_index > 3 or deficit_ratio > 0.05:
            scarcity_risk = "Medium"
        else:
            scarcity_risk = "Low"
        
        # Flooding risk (seasonal for UAE/KSA)
        # Higher risk during winter months (Dec-Mar)
        winter_months = [12, 1, 2, 3]
        if location in ['Dubai', 'Sharjah', 'Jeddah']:
            flooding_risk = "Medium"  # Coastal areas
        elif location in ['Riyadh']:
            flooding_risk = "Low"     # Inland desert
        else:
            flooding_risk = "Low"
        
        # Quality degradation risk
        high_impact_params = sum(1 for impact in quality_impacts if impact.impact_level == "High")
        exceedances = sum(1 for impact in quality_impacts if impact.exceeds_standard)
        
        if exceedances > 3 or high_impact_params > 2:
            quality_risk = "High"
        elif exceedances > 1 or high_impact_params > 0:
            quality_risk = "Medium"
        else:
            quality_risk = "Low"
        
        # Regulatory compliance risk
        if exceedances > 0:
            compliance_risk = "High"
        elif quality_risk == "Medium":
            compliance_risk = "Medium"
        else:
            compliance_risk = "Low"
        
        # Supply reliability risk
        if water_balance.deficit_surplus < 0:
            supply_risk = "High"
        elif water_balance.available_supply < water_balance.total_demand * 1.2:
            supply_risk = "Medium"
        else:
            supply_risk = "Low"
        
        # Cost escalation risk
        if scarcity_risk in ["High", "Extreme"]:
            cost_risk = "High"
        elif supply_risk == "High":
            cost_risk = "Medium"
        else:
            cost_risk = "Low"
        
        # Overall risk level
        risk_scores = {
            "Low": 1, "Medium": 2, "High": 3, "Extreme": 4
        }
        
        risks = [scarcity_risk, flooding_risk, quality_risk, compliance_risk, supply_risk, cost_risk]
        avg_score = np.mean([risk_scores.get(r, 2) for r in risks])
        
        if avg_score >= 3:
            overall_risk = "High"
        elif avg_score >= 2:
            overall_risk = "Medium"
        else:
            overall_risk = "Low"
        
        # Mitigation priorities
        priorities = []
        if scarcity_risk in ["High", "Extreme"]:
            priorities.append("Implement water conservation measures")
            priorities.append("Secure alternative water sources")
        if quality_risk in ["Medium", "High"]:
            priorities.append("Install water treatment systems")
            priorities.append("Implement pollution prevention plan")
        if supply_risk in ["Medium", "High"]:
            priorities.append("Increase water storage capacity")
            priorities.append("Develop contingency supply plan")
        if compliance_risk in ["Medium", "High"]:
            priorities.append("Enhance monitoring program")
            priorities.append("Upgrade treatment facilities")
        
        return WaterRiskAssessment(
            water_scarcity_risk=scarcity_risk,
            flooding_risk=flooding_risk,
            quality_degradation_risk=quality_risk,
            regulatory_compliance_risk=compliance_risk,
            supply_reliability_risk=supply_risk,
            cost_escalation_risk=cost_risk,
            overall_risk_level=overall_risk,
            mitigation_priority=priorities[:5]  # Top 5 priorities
        )
    
    def recommend_conservation_measures(
        self,
        consumption: WaterConsumption,
        water_balance: WaterBalance,
        budget_constraint: Optional[float] = None
    ) -> List[Dict[str, any]]:
        """
        Recommend water conservation measures.
        
        Args:
            consumption: Water consumption data
            water_balance: Water balance
            budget_constraint: Budget limit for measures
            
        Returns:
            List of recommended conservation measures
        """
        measures = []
        
        # Conservation measure database
        conservation_options = [
            {
                'name': 'Rainwater Harvesting System',
                'applicable_to': ['residential', 'commercial'],
                'reduction_potential': 0.15,
                'cost_per_m3_saved': 50,
                'implementation_time': 30,
                'description': 'Collect and store rainwater for non-potable uses'
            },
            {
                'name': 'Greywater Recycling',
                'applicable_to': ['residential', 'commercial', 'industrial'],
                'reduction_potential': 0.25,
                'cost_per_m3_saved': 80,
                'implementation_time': 45,
                'description': 'Treat and reuse greywater for irrigation and flushing'
            },
            {
                'name': 'Smart Irrigation System',
                'applicable_to': ['residential', 'commercial'],
                'reduction_potential': 0.3,
                'cost_per_m3_saved': 30,
                'implementation_time': 15,
                'description': 'Weather-based irrigation controllers with drip systems'
            },
            {
                'name': 'Water-Efficient Fixtures',
                'applicable_to': ['all'],
                'reduction_potential': 0.2,
                'cost_per_m3_saved': 20,
                'implementation_time': 7,
                'description': 'Low-flow faucets, dual-flush toilets, and efficient appliances'
            },
            {
                'name': 'Dust Suppression Polymers',
                'applicable_to': ['construction', 'infrastructure'],
                'reduction_potential': 0.5,
                'cost_per_m3_saved': 40,
                'implementation_time': 1,
                'description': 'Chemical dust suppressants reducing water for dust control'
            },
            {
                'name': 'Closed-Loop Equipment Washing',
                'applicable_to': ['construction', 'industrial'],
                'reduction_potential': 0.6,
                'cost_per_m3_saved': 60,
                'implementation_time': 14,
                'description': 'Recirculating wash systems for vehicles and equipment'
            },
            {
                'name': 'Native Landscaping',
                'applicable_to': ['residential', 'commercial'],
                'reduction_potential': 0.7,
                'cost_per_m3_saved': 10,
                'implementation_time': 60,
                'description': 'Replace high-water plants with drought-tolerant native species'
            },
            {
                'name': 'Leak Detection System',
                'applicable_to': ['all'],
                'reduction_potential': 0.1,
                'cost_per_m3_saved': 15,
                'implementation_time': 7,
                'description': 'Smart meters and sensors to detect and prevent leaks'
            }
        ]
        
        # Calculate potential savings for each measure
        for measure in conservation_options:
            # Check applicability
            applicable = False
            for activity, volume in consumption.by_activity.items():
                if volume > 0 and (
                    'all' in measure['applicable_to'] or
                    any(t in activity.lower() for t in measure['applicable_to'])
                ):
                    applicable = True
                    break
            
            if not applicable:
                continue
            
            # Calculate savings
            potential_savings = consumption.daily_average * measure['reduction_potential']
            annual_savings = potential_savings * 365
            implementation_cost = annual_savings * measure['cost_per_m3_saved']
            
            # ROI calculation
            annual_water_cost_savings = annual_savings * 5  # Assume $5/m³ water cost
            payback_period = implementation_cost / annual_water_cost_savings if annual_water_cost_savings > 0 else float('inf')
            
            # Check budget constraint
            if budget_constraint and implementation_cost > budget_constraint:
                continue
            
            measures.append({
                'name': measure['name'],
                'description': measure['description'],
                'water_savings_m3_day': potential_savings,
                'reduction_percentage': measure['reduction_potential'] * 100,
                'implementation_cost': implementation_cost,
                'payback_period_years': payback_period,
                'implementation_time_days': measure['implementation_time'],
                'priority': self._calculate_measure_priority(
                    potential_savings,
                    implementation_cost,
                    payback_period,
                    water_balance.deficit_surplus
                )
            })
        
        # Sort by priority
        measures.sort(key=lambda x: x['priority'], reverse=True)
        
        return measures
    
    def _get_water_quality_standard(self, parameter: str, use_type: str) -> Optional[float]:
        """Get water quality standard for parameter."""
        standards = self.quality_standards.get(use_type, {})
        
        if parameter in standards:
            value = standards[parameter]
            # Handle range values (like pH)
            if isinstance(value, tuple):
                return value[1]  # Return upper limit
            return value
        
        return None
    
    def _get_parameter_unit(self, parameter: str) -> str:
        """Get unit for water quality parameter."""
        units = {
            'ph': 'pH units',
            'tds': 'mg/L',
            'tss': 'mg/L',
            'bod': 'mg/L',
            'cod': 'mg/L',
            'do': 'mg/L',
            'turbidity': 'NTU',
            'nitrates': 'mg/L',
            'phosphates': 'mg/L',
            'temperature': '°C',
            'coliform': 'CFU/100ml'
        }
        return units.get(parameter, 'mg/L')
    
    def _calculate_measure_priority(
        self,
        savings: float,
        cost: float,
        payback: float,
        deficit: float
    ) -> float:
        """Calculate priority score for conservation measure."""
        # Weighted scoring
        savings_score = min(savings / 100, 1) * 30  # Max 30 points
        cost_score = max(0, 1 - cost / 100000) * 20  # Max 20 points
        payback_score = max(0, 1 - payback / 5) * 25  # Max 25 points
        urgency_score = (1 if deficit < 0 else 0.5) * 25  # Max 25 points
        
        return savings_score + cost_score + payback_score + urgency_score
    
    def generate_water_management_plan(
        self,
        project_data: Dict[str, any],
        consumption: WaterConsumption,
        balance: WaterBalance,
        risks: WaterRiskAssessment,
        conservation_measures: List[Dict[str, any]]
    ) -> Dict[str, any]:
        """
        Generate comprehensive water management plan.
        
        Args:
            project_data: Project information
            consumption: Water consumption assessment
            balance: Water balance
            risks: Risk assessment
            conservation_measures: Recommended measures
            
        Returns:
            Water management plan document
        """
        plan = {
            'project_info': {
                'name': project_data.get('name'),
                'location': project_data.get('location'),
                'type': project_data.get('project_type'),
                'duration': project_data.get('duration'),
                'generated_date': datetime.now().isoformat()
            },
            
            'executive_summary': {
                'total_water_demand': consumption.total_project,
                'daily_average_demand': consumption.daily_average,
                'water_deficit_surplus': balance.deficit_surplus,
                'overall_risk_level': risks.overall_risk_level,
                'key_recommendations': conservation_measures[:3] if conservation_measures else []
            },
            
            'water_consumption_analysis': {
                'daily_consumption': consumption.daily_average,
                'peak_demand': consumption.peak_demand,
                'total_project_consumption': consumption.total_project,
                'per_capita_consumption': consumption.per_worker,
                'consumption_by_activity': consumption.by_activity,
                'consumption_by_source': consumption.by_source
            },
            
            'water_balance': {
                'total_demand': balance.total_demand,
                'available_supply': balance.available_supply,
                'deficit_surplus': balance.deficit_surplus,
                'recycled_water_potential': balance.recycled_water,
                'conservation_potential': balance.conservation_potential
            },
            
            'risk_assessment': {
                'water_scarcity_risk': risks.water_scarcity_risk,
                'supply_reliability_risk': risks.supply_reliability_risk,
                'quality_degradation_risk': risks.quality_degradation_risk,
                'regulatory_compliance_risk': risks.regulatory_compliance_risk,
                'overall_risk': risks.overall_risk_level,
                'mitigation_priorities': risks.mitigation_priority
            },
            
            'conservation_strategy': {
                'recommended_measures': conservation_measures,
                'total_savings_potential': sum(m['water_savings_m3_day'] for m in conservation_measures),
                'implementation_schedule': self._create_implementation_schedule(conservation_measures),
                'monitoring_plan': self._create_monitoring_plan()
            },
            
            'implementation_plan': {
                'immediate_actions': [
                    'Establish water management team',
                    'Install water meters at key points',
                    'Implement daily water tracking system',
                    'Train staff on water conservation'
                ],
                'short_term_actions': [
                    m['name'] for m in conservation_measures 
                    if m['implementation_time_days'] <= 30
                ][:3],
                'long_term_actions': [
                    m['name'] for m in conservation_measures 
                    if m['implementation_time_days'] > 30
                ][:3]
            },
            
            'compliance_requirements': {
                'permits_required': [
                    'Water abstraction permit (if using groundwater)',
                    'Discharge permit for wastewater',
                    'NOC from water authority'
                ],
                'monitoring_requirements': [
                    'Daily water consumption recording',
                    'Monthly water quality testing',
                    'Quarterly compliance reporting'
                ],
                'reporting_requirements': [
                    'Monthly water balance report',
                    'Incident reporting within 24 hours',
                    'Annual water audit report'
                ]
            }
        }
        
        return plan
    
    def _create_implementation_schedule(
        self, 
        measures: List[Dict[str, any]]
    ) -> List[Dict[str, any]]:
        """Create implementation schedule for conservation measures."""
        schedule = []
        current_month = 1
        
        # Sort by implementation time
        sorted_measures = sorted(measures, key=lambda x: x['implementation_time_days'])
        
        for measure in sorted_measures[:5]:  # Top 5 measures
            schedule.append({
                'measure': measure['name'],
                'start_month': current_month,
                'duration_days': measure['implementation_time_days'],
                'completion_month': current_month + (measure['implementation_time_days'] // 30),
                'responsible_party': 'Environmental Manager',
                'budget': measure['implementation_cost']
            })
            current_month += max(1, measure['implementation_time_days'] // 30)
        
        return schedule
    
    def _create_monitoring_plan(self) -> Dict[str, any]:
        """Create water monitoring plan."""
        return {
            'consumption_monitoring': {
                'frequency': 'Daily',
                'parameters': ['Total consumption', 'Source-wise consumption', 'Activity-wise usage'],
                'method': 'Digital flow meters with SCADA integration',
                'responsible': 'Site Engineer'
            },
            'quality_monitoring': {
                'frequency': 'Weekly',
                'parameters': ['pH', 'TSS', 'Turbidity', 'Oil & Grease'],
                'sampling_points': ['Inlet', 'Storage tanks', 'Discharge point'],
                'responsible': 'Environmental Officer'
            },
            'compliance_monitoring': {
                'frequency': 'Monthly',
                'parameters': ['Permit compliance', 'Consumption vs allocation', 'Quality standards'],
                'reporting': 'Monthly compliance report to authorities',
                'responsible': 'HSE Manager'
            }
        }