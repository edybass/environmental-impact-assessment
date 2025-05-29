"""
Comprehensive Environmental Management Plan (EMP) Module
Professional EMP development integrating all environmental assessments

Created by: Edy Bassil
Email: bassileddy@gmail.com
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import math
from datetime import datetime, timedelta

class ProjectPhase(Enum):
    """Project phases for EMP implementation"""
    PRE_CONSTRUCTION = "pre_construction"
    CONSTRUCTION = "construction"
    OPERATIONAL = "operational"
    DECOMMISSIONING = "decommissioning"

class MitigationHierarchy(Enum):
    """Mitigation hierarchy levels"""
    AVOID = "avoid"
    MINIMIZE = "minimize"
    RESTORE = "restore"
    OFFSET = "offset"

class ImpactSignificance(Enum):
    """Environmental impact significance levels"""
    NEGLIGIBLE = "negligible"
    MINOR = "minor"
    MODERATE = "moderate"
    MAJOR = "major"
    CRITICAL = "critical"

class MonitoringFrequency(Enum):
    """Monitoring frequency options"""
    CONTINUOUS = "continuous"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUALLY = "annually"
    EVENT_BASED = "event_based"

@dataclass
class MitigationMeasure:
    """Individual mitigation measure"""
    measure_id: str
    description: str
    hierarchy_level: MitigationHierarchy
    impact_addressed: str
    implementation_phase: ProjectPhase
    responsible_party: str
    timeline: str
    success_criteria: str
    cost_estimate: float
    effectiveness: float

@dataclass
class MonitoringParameter:
    """Environmental monitoring parameter"""
    parameter_name: str
    monitoring_locations: List[str]
    frequency: MonitoringFrequency
    methodology: str
    regulatory_limit: Optional[float]
    trigger_level: Optional[float]
    reporting_frequency: str
    responsible_party: str

@dataclass
class EMPComponent:
    """EMP component structure"""
    component_name: str
    impacts_addressed: List[str]
    mitigation_measures: List[MitigationMeasure]
    monitoring_parameters: List[MonitoringParameter]
    compliance_requirements: List[str]
    implementation_cost: float

class EnvironmentalManagementPlan:
    """Comprehensive Environmental Management Plan generator"""
    
    def __init__(self):
        self.regulatory_frameworks = self._initialize_regulatory_frameworks()
        self.standard_mitigation_measures = self._initialize_standard_measures()
        self.monitoring_standards = self._initialize_monitoring_standards()
        self.responsibility_matrix = self._initialize_responsibility_matrix()
    
    def _initialize_regulatory_frameworks(self) -> Dict[str, Dict]:
        """Initialize regulatory frameworks for UAE/KSA"""
        return {
            "uae": {
                "federal_laws": [
                    "UAE Federal Law No. 24 of 1999 - Environmental Protection and Development",
                    "UAE Federal Law No. 11 of 2017 - Cultural Heritage Protection",
                    "Cabinet Resolution No. 37 of 2001 - EIA Procedures"
                ],
                "standards": [
                    "UAE.S ESM.01:2019 - Environmental Management Systems",
                    "UAE.S ESM.02:2019 - Environmental Monitoring",
                    "UAE.S ESM.03:2019 - Waste Management"
                ],
                "local_authorities": {
                    "dubai": ["Dubai Municipality", "DEWA", "DDA", "RERA"],
                    "abu_dhabi": ["ADEK", "EAD", "ADWEC", "UPC"],
                    "sharjah": ["Sharjah Municipality", "SEWA", "SPEA"]
                }
            },
            "ksa": {
                "federal_laws": [
                    "KSA Environmental Law (Royal Decree M/34)",
                    "KSA Executive Regulations for Environmental Law",
                    "Waste Management Law",
                    "Water Law"
                ],
                "standards": [
                    "SASO Environmental Management Standards",
                    "GAMEP Guidelines",
                    "NCEC Environmental Assessment Procedures"
                ],
                "authorities": [
                    "Ministry of Environment, Water and Agriculture (MEWA)",
                    "National Center for Environmental Compliance (NCEC)",
                    "General Authority for Meteorology and Environmental Protection (GAMEP)"
                ]
            }
        }
    
    def _initialize_standard_measures(self) -> Dict[str, List[Dict]]:
        """Initialize standard mitigation measures by environmental component"""
        return {
            "air_quality": [
                {
                    "id": "AQ_001",
                    "description": "Install dust suppression systems",
                    "hierarchy": MitigationHierarchy.MINIMIZE,
                    "phase": ProjectPhase.CONSTRUCTION,
                    "effectiveness": 0.75,
                    "cost_factor": 0.02  # % of project cost
                },
                {
                    "id": "AQ_002", 
                    "description": "Implement vehicle emission controls",
                    "hierarchy": MitigationHierarchy.MINIMIZE,
                    "phase": ProjectPhase.CONSTRUCTION,
                    "effectiveness": 0.60,
                    "cost_factor": 0.01
                },
                {
                    "id": "AQ_003",
                    "description": "Schedule activities to avoid adverse weather",
                    "hierarchy": MitigationHierarchy.MINIMIZE,
                    "phase": ProjectPhase.CONSTRUCTION,
                    "effectiveness": 0.40,
                    "cost_factor": 0.005
                }
            ],
            "noise": [
                {
                    "id": "NS_001",
                    "description": "Install noise barriers around construction sites",
                    "hierarchy": MitigationHierarchy.MINIMIZE,
                    "phase": ProjectPhase.CONSTRUCTION,
                    "effectiveness": 0.70,
                    "cost_factor": 0.015
                },
                {
                    "id": "NS_002",
                    "description": "Restrict noisy activities to daytime hours",
                    "hierarchy": MitigationHierarchy.MINIMIZE,
                    "phase": ProjectPhase.CONSTRUCTION,
                    "effectiveness": 0.80,
                    "cost_factor": 0.001
                },
                {
                    "id": "NS_003",
                    "description": "Use quieter construction equipment",
                    "hierarchy": MitigationHierarchy.MINIMIZE,
                    "phase": ProjectPhase.CONSTRUCTION,
                    "effectiveness": 0.50,
                    "cost_factor": 0.01
                }
            ],
            "water_resources": [
                {
                    "id": "WR_001",
                    "description": "Implement water recycling systems",
                    "hierarchy": MitigationHierarchy.MINIMIZE,
                    "phase": ProjectPhase.OPERATIONAL,
                    "effectiveness": 0.80,
                    "cost_factor": 0.03
                },
                {
                    "id": "WR_002",
                    "description": "Install water-efficient fixtures",
                    "hierarchy": MitigationHierarchy.MINIMIZE,
                    "phase": ProjectPhase.OPERATIONAL,
                    "effectiveness": 0.60,
                    "cost_factor": 0.02
                },
                {
                    "id": "WR_003",
                    "description": "Implement stormwater management",
                    "hierarchy": MitigationHierarchy.MINIMIZE,
                    "phase": ProjectPhase.CONSTRUCTION,
                    "effectiveness": 0.85,
                    "cost_factor": 0.025
                }
            ],
            "waste_management": [
                {
                    "id": "WM_001",
                    "description": "Implement waste segregation at source",
                    "hierarchy": MitigationHierarchy.MINIMIZE,
                    "phase": ProjectPhase.CONSTRUCTION,
                    "effectiveness": 0.75,
                    "cost_factor": 0.01
                },
                {
                    "id": "WM_002",
                    "description": "Establish recycling programs",
                    "hierarchy": MitigationHierarchy.MINIMIZE,
                    "phase": ProjectPhase.OPERATIONAL,
                    "effectiveness": 0.65,
                    "cost_factor": 0.015
                },
                {
                    "id": "WM_003",
                    "description": "Partner with certified waste facilities",
                    "hierarchy": MitigationHierarchy.MINIMIZE,
                    "phase": ProjectPhase.CONSTRUCTION,
                    "effectiveness": 0.95,
                    "cost_factor": 0.005
                }
            ],
            "biological_environment": [
                {
                    "id": "BE_001",
                    "description": "Establish construction exclusion zones",
                    "hierarchy": MitigationHierarchy.AVOID,
                    "phase": ProjectPhase.PRE_CONSTRUCTION,
                    "effectiveness": 0.95,
                    "cost_factor": 0.001
                },
                {
                    "id": "BE_002",
                    "description": "Implement seasonal restrictions",
                    "hierarchy": MitigationHierarchy.MINIMIZE,
                    "phase": ProjectPhase.CONSTRUCTION,
                    "effectiveness": 0.80,
                    "cost_factor": 0.002
                },
                {
                    "id": "BE_003",
                    "description": "Restore disturbed habitats",
                    "hierarchy": MitigationHierarchy.RESTORE,
                    "phase": ProjectPhase.OPERATIONAL,
                    "effectiveness": 0.70,
                    "cost_factor": 0.04
                }
            ],
            "soil_geology": [
                {
                    "id": "SG_001",
                    "description": "Implement erosion control measures",
                    "hierarchy": MitigationHierarchy.MINIMIZE,
                    "phase": ProjectPhase.CONSTRUCTION,
                    "effectiveness": 0.85,
                    "cost_factor": 0.02
                },
                {
                    "id": "SG_002",
                    "description": "Conduct soil remediation if contaminated",
                    "hierarchy": MitigationHierarchy.RESTORE,
                    "phase": ProjectPhase.PRE_CONSTRUCTION,
                    "effectiveness": 0.90,
                    "cost_factor": 0.05
                },
                {
                    "id": "SG_003",
                    "description": "Implement ground improvement techniques",
                    "hierarchy": MitigationHierarchy.MINIMIZE,
                    "phase": ProjectPhase.CONSTRUCTION,
                    "effectiveness": 0.80,
                    "cost_factor": 0.03
                }
            ],
            "socio_economic": [
                {
                    "id": "SE_001",
                    "description": "Implement community engagement program",
                    "hierarchy": MitigationHierarchy.MINIMIZE,
                    "phase": ProjectPhase.CONSTRUCTION,
                    "effectiveness": 0.70,
                    "cost_factor": 0.01
                },
                {
                    "id": "SE_002",
                    "description": "Provide local employment opportunities",
                    "hierarchy": MitigationHierarchy.MINIMIZE,
                    "phase": ProjectPhase.CONSTRUCTION,
                    "effectiveness": 0.85,
                    "cost_factor": 0.005
                },
                {
                    "id": "SE_003",
                    "description": "Implement traffic management plan",
                    "hierarchy": MitigationHierarchy.MINIMIZE,
                    "phase": ProjectPhase.CONSTRUCTION,
                    "effectiveness": 0.75,
                    "cost_factor": 0.015
                }
            ]
        }
    
    def _initialize_monitoring_standards(self) -> Dict[str, Dict]:
        """Initialize monitoring standards and methodologies"""
        return {
            "air_quality": {
                "parameters": ["PM10", "PM2.5", "NO2", "SO2", "TSP"],
                "methods": "US EPA Reference Methods / ISO Standards",
                "frequencies": {
                    "construction": MonitoringFrequency.DAILY,
                    "operational": MonitoringFrequency.WEEKLY
                },
                "location_density": "1 station per 2 km radius"
            },
            "noise": {
                "parameters": ["LAeq", "LA10", "LA90", "LAmax"],
                "methods": "IEC 61672 Class 1 Sound Level Meters",
                "frequencies": {
                    "construction": MonitoringFrequency.DAILY,
                    "operational": MonitoringFrequency.MONTHLY
                },
                "location_density": "1 station per sensitive receptor"
            },
            "water_quality": {
                "parameters": ["pH", "BOD", "COD", "TSS", "Heavy metals", "Hydrocarbons"],
                "methods": "Standard Methods for Water and Wastewater Examination",
                "frequencies": {
                    "construction": MonitoringFrequency.WEEKLY,
                    "operational": MonitoringFrequency.MONTHLY
                },
                "location_density": "Upstream and downstream monitoring"
            },
            "soil_quality": {
                "parameters": ["pH", "Heavy metals", "TPH", "Salinity", "Organic matter"],
                "methods": "ISO 18400 series - Soil sampling and analysis",
                "frequencies": {
                    "construction": MonitoringFrequency.QUARTERLY,
                    "operational": MonitoringFrequency.ANNUALLY
                },
                "location_density": "Grid sampling approach"
            },
            "groundwater": {
                "parameters": ["Water level", "pH", "TDS", "Heavy metals", "Hydrocarbons"],
                "methods": "ISO 5667 series - Water sampling",
                "frequencies": {
                    "construction": MonitoringFrequency.MONTHLY,
                    "operational": MonitoringFrequency.QUARTERLY
                },
                "location_density": "Monitoring wells grid"
            },
            "biodiversity": {
                "parameters": ["Species abundance", "Habitat quality", "Vegetation cover"],
                "methods": "Standardized ecological survey protocols",
                "frequencies": {
                    "construction": MonitoringFrequency.QUARTERLY,
                    "operational": MonitoringFrequency.ANNUALLY
                },
                "location_density": "Representative habitat sampling"
            }
        }
    
    def _initialize_responsibility_matrix(self) -> Dict[str, str]:
        """Initialize responsibility matrix for EMP implementation"""
        return {
            "Project Owner": "Overall EMP implementation and compliance",
            "Environmental Manager": "Day-to-day environmental management",
            "Construction Contractor": "Construction phase mitigation implementation",
            "Environmental Consultant": "Monitoring, reporting, and advisory services",
            "Health & Safety Officer": "Worker and public safety measures",
            "Community Relations Officer": "Stakeholder engagement and grievance handling",
            "Waste Management Contractor": "Waste collection, treatment, and disposal",
            "Water Management Contractor": "Water supply and wastewater treatment",
            "Monitoring Laboratory": "Environmental sample analysis",
            "Regulatory Authorities": "Compliance oversight and enforcement"
        }
    
    def generate_comprehensive_emp(self, project_data: Dict[str, Any], 
                                 assessment_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive Environmental Management Plan"""
        
        project_size = float(project_data.get('size', 10000))
        project_type = project_data.get('type', 'residential').lower()
        location = project_data.get('location', 'Dubai').lower()
        duration = int(project_data.get('duration', 24))
        
        # Determine region
        region = 'uae' if any(x in location for x in ['dubai', 'abu dhabi', 'sharjah']) else 'ksa'
        
        # Generate EMP components
        emp_components = {}
        total_implementation_cost = 0
        
        # Air Quality Management Plan
        if 'air_quality' in assessment_results:
            air_component = self._generate_air_quality_emp(
                assessment_results['air_quality'], project_data
            )
            emp_components['air_quality'] = air_component
            total_implementation_cost += air_component.implementation_cost
        
        # Noise Management Plan
        if 'noise' in assessment_results:
            noise_component = self._generate_noise_emp(
                assessment_results['noise'], project_data
            )
            emp_components['noise'] = noise_component
            total_implementation_cost += noise_component.implementation_cost
        
        # Water Resources Management Plan
        if 'water_resources' in assessment_results:
            water_component = self._generate_water_emp(
                assessment_results['water_resources'], project_data
            )
            emp_components['water_resources'] = water_component
            total_implementation_cost += water_component.implementation_cost
        
        # Waste Management Plan
        if 'waste_management' in assessment_results:
            waste_component = self._generate_waste_emp(
                assessment_results['waste_management'], project_data
            )
            emp_components['waste_management'] = waste_component
            total_implementation_cost += waste_component.implementation_cost
        
        # Biodiversity Management Plan
        if 'biological_environment' in assessment_results:
            bio_component = self._generate_biodiversity_emp(
                assessment_results['biological_environment'], project_data
            )
            emp_components['biological_environment'] = bio_component
            total_implementation_cost += bio_component.implementation_cost
        
        # Soil and Geology Management Plan
        if 'soil_geology' in assessment_results:
            soil_component = self._generate_soil_geology_emp(
                assessment_results['soil_geology'], project_data
            )
            emp_components['soil_geology'] = soil_component
            total_implementation_cost += soil_component.implementation_cost
        
        # Socio-Economic Management Plan
        if 'socio_economic' in assessment_results:
            socio_component = self._generate_socio_economic_emp(
                assessment_results['socio_economic'], project_data
            )
            emp_components['socio_economic'] = socio_component
            total_implementation_cost += socio_component.implementation_cost
        
        # Risk Management Plan
        if 'risk_assessment' in assessment_results:
            risk_component = self._generate_risk_management_emp(
                assessment_results['risk_assessment'], project_data
            )
            emp_components['risk_management'] = risk_component
            total_implementation_cost += risk_component.implementation_cost
        
        # Generate implementation timeline
        implementation_timeline = self._generate_implementation_timeline(emp_components, duration)
        
        # Generate monitoring program
        monitoring_program = self._generate_monitoring_program(emp_components, project_data)
        
        # Generate reporting schedule
        reporting_schedule = self._generate_reporting_schedule(region)
        
        # Generate compliance framework
        compliance_framework = self._generate_compliance_framework(region, project_type)
        
        # Generate emergency response plan
        emergency_response = self._generate_emergency_response_plan(emp_components, project_data)
        
        # Generate training requirements
        training_program = self._generate_training_program(emp_components)
        
        # Generate performance indicators
        performance_indicators = self._generate_performance_indicators(emp_components)
        
        # Generate audit and review schedule
        audit_schedule = self._generate_audit_schedule()
        
        return {
            'emp_summary': {
                'total_components': len(emp_components),
                'total_mitigation_measures': sum(len(comp.mitigation_measures) for comp in emp_components.values()),
                'total_monitoring_parameters': sum(len(comp.monitoring_parameters) for comp in emp_components.values()),
                'total_implementation_cost': round(total_implementation_cost, 0),
                'implementation_duration': duration
            },
            'emp_components': emp_components,
            'implementation_timeline': implementation_timeline,
            'monitoring_program': monitoring_program,
            'reporting_schedule': reporting_schedule,
            'compliance_framework': compliance_framework,
            'emergency_response_plan': emergency_response,
            'training_program': training_program,
            'performance_indicators': performance_indicators,
            'audit_and_review_schedule': audit_schedule,
            'management_structure': self._generate_management_structure(),
            'budget_breakdown': self._generate_budget_breakdown(emp_components, total_implementation_cost)
        }
    
    def _generate_air_quality_emp(self, air_assessment: Dict, project_data: Dict) -> EMPComponent:
        """Generate Air Quality Management Plan component"""
        
        project_size = float(project_data.get('size', 10000))
        
        # Select appropriate mitigation measures
        mitigation_measures = []
        for measure_data in self.standard_mitigation_measures['air_quality']:
            cost = project_size * measure_data['cost_factor'] * 100  # Convert to USD
            
            measure = MitigationMeasure(
                measure_id=measure_data['id'],
                description=measure_data['description'],
                hierarchy_level=measure_data['hierarchy'],
                impact_addressed='Air quality deterioration',
                implementation_phase=measure_data['phase'],
                responsible_party=self._get_responsible_party(measure_data['id']),
                timeline=self._get_implementation_timeline(measure_data['phase']),
                success_criteria=self._get_success_criteria(measure_data['id']),
                cost_estimate=cost,
                effectiveness=measure_data['effectiveness']
            )
            mitigation_measures.append(measure)
        
        # Generate monitoring parameters
        monitoring_params = []
        air_standards = self.monitoring_standards['air_quality']
        
        for param in air_standards['parameters']:
            monitoring_param = MonitoringParameter(
                parameter_name=param,
                monitoring_locations=['Site boundary', 'Nearest residential area', 'Downwind location'],
                frequency=air_standards['frequencies']['construction'],
                methodology=air_standards['methods'],
                regulatory_limit=self._get_regulatory_limit(param, 'air'),
                trigger_level=self._get_trigger_level(param, 'air'),
                reporting_frequency='Weekly during construction, Monthly during operation',
                responsible_party='Environmental Consultant'
            )
            monitoring_params.append(monitoring_param)
        
        # Calculate implementation cost
        total_cost = sum(measure.cost_estimate for measure in mitigation_measures)
        monitoring_cost = len(monitoring_params) * 5000  # Annual monitoring cost per parameter
        implementation_cost = total_cost + monitoring_cost
        
        return EMPComponent(
            component_name='Air Quality Management Plan',
            impacts_addressed=['PM10 and PM2.5 emissions', 'Dust generation', 'Vehicle emissions'],
            mitigation_measures=mitigation_measures,
            monitoring_parameters=monitoring_params,
            compliance_requirements=self._get_air_compliance_requirements(),
            implementation_cost=implementation_cost
        )
    
    def _generate_noise_emp(self, noise_assessment: Dict, project_data: Dict) -> EMPComponent:
        """Generate Noise Management Plan component"""
        
        project_size = float(project_data.get('size', 10000))
        
        # Select mitigation measures
        mitigation_measures = []
        for measure_data in self.standard_mitigation_measures['noise']:
            cost = project_size * measure_data['cost_factor'] * 100
            
            measure = MitigationMeasure(
                measure_id=measure_data['id'],
                description=measure_data['description'],
                hierarchy_level=measure_data['hierarchy'],
                impact_addressed='Noise pollution',
                implementation_phase=measure_data['phase'],
                responsible_party=self._get_responsible_party(measure_data['id']),
                timeline=self._get_implementation_timeline(measure_data['phase']),
                success_criteria=self._get_success_criteria(measure_data['id']),
                cost_estimate=cost,
                effectiveness=measure_data['effectiveness']
            )
            mitigation_measures.append(measure)
        
        # Generate monitoring parameters
        monitoring_params = []
        noise_standards = self.monitoring_standards['noise']
        
        for param in noise_standards['parameters']:
            monitoring_param = MonitoringParameter(
                parameter_name=param,
                monitoring_locations=['Site boundary', 'Nearest residential receptor', 'Sensitive locations'],
                frequency=noise_standards['frequencies']['construction'],
                methodology=noise_standards['methods'],
                regulatory_limit=self._get_regulatory_limit(param, 'noise'),
                trigger_level=self._get_trigger_level(param, 'noise'),
                reporting_frequency='Daily during construction, Weekly during operation',
                responsible_party='Environmental Consultant'
            )
            monitoring_params.append(monitoring_param)
        
        total_cost = sum(measure.cost_estimate for measure in mitigation_measures)
        monitoring_cost = len(monitoring_params) * 3000
        implementation_cost = total_cost + monitoring_cost
        
        return EMPComponent(
            component_name='Noise Management Plan',
            impacts_addressed=['Construction noise', 'Traffic noise', 'Equipment noise'],
            mitigation_measures=mitigation_measures,
            monitoring_parameters=monitoring_params,
            compliance_requirements=self._get_noise_compliance_requirements(),
            implementation_cost=implementation_cost
        )
    
    def _generate_water_emp(self, water_assessment: Dict, project_data: Dict) -> EMPComponent:
        """Generate Water Resources Management Plan component"""
        
        project_size = float(project_data.get('size', 10000))
        
        mitigation_measures = []
        for measure_data in self.standard_mitigation_measures['water_resources']:
            cost = project_size * measure_data['cost_factor'] * 100
            
            measure = MitigationMeasure(
                measure_id=measure_data['id'],
                description=measure_data['description'],
                hierarchy_level=measure_data['hierarchy'],
                impact_addressed='Water resource depletion and quality degradation',
                implementation_phase=measure_data['phase'],
                responsible_party=self._get_responsible_party(measure_data['id']),
                timeline=self._get_implementation_timeline(measure_data['phase']),
                success_criteria=self._get_success_criteria(measure_data['id']),
                cost_estimate=cost,
                effectiveness=measure_data['effectiveness']
            )
            mitigation_measures.append(measure)
        
        # Water quality monitoring
        monitoring_params = []
        water_standards = self.monitoring_standards['water_quality']
        
        for param in water_standards['parameters']:
            monitoring_param = MonitoringParameter(
                parameter_name=param,
                monitoring_locations=['Water intake point', 'Discharge point', 'Groundwater wells'],
                frequency=water_standards['frequencies']['construction'],
                methodology=water_standards['methods'],
                regulatory_limit=self._get_regulatory_limit(param, 'water'),
                trigger_level=self._get_trigger_level(param, 'water'),
                reporting_frequency='Monthly',
                responsible_party='Water Management Contractor'
            )
            monitoring_params.append(monitoring_param)
        
        total_cost = sum(measure.cost_estimate for measure in mitigation_measures)
        monitoring_cost = len(monitoring_params) * 4000
        implementation_cost = total_cost + monitoring_cost
        
        return EMPComponent(
            component_name='Water Resources Management Plan',
            impacts_addressed=['Water consumption', 'Wastewater generation', 'Water quality impacts'],
            mitigation_measures=mitigation_measures,
            monitoring_parameters=monitoring_params,
            compliance_requirements=self._get_water_compliance_requirements(),
            implementation_cost=implementation_cost
        )
    
    def _generate_waste_emp(self, waste_assessment: Dict, project_data: Dict) -> EMPComponent:
        """Generate Waste Management Plan component"""
        
        project_size = float(project_data.get('size', 10000))
        
        mitigation_measures = []
        for measure_data in self.standard_mitigation_measures['waste_management']:
            cost = project_size * measure_data['cost_factor'] * 100
            
            measure = MitigationMeasure(
                measure_id=measure_data['id'],
                description=measure_data['description'],
                hierarchy_level=measure_data['hierarchy'],
                impact_addressed='Waste generation and disposal impacts',
                implementation_phase=measure_data['phase'],
                responsible_party=self._get_responsible_party(measure_data['id']),
                timeline=self._get_implementation_timeline(measure_data['phase']),
                success_criteria=self._get_success_criteria(measure_data['id']),
                cost_estimate=cost,
                effectiveness=measure_data['effectiveness']
            )
            mitigation_measures.append(measure)
        
        # Waste monitoring (tracking and reporting)
        monitoring_params = [
            MonitoringParameter(
                parameter_name='Waste generation rates',
                monitoring_locations=['Construction site', 'Operational facilities'],
                frequency=MonitoringFrequency.MONTHLY,
                methodology='Waste tracking and weighing systems',
                regulatory_limit=None,
                trigger_level=None,
                reporting_frequency='Monthly',
                responsible_party='Waste Management Contractor'
            ),
            MonitoringParameter(
                parameter_name='Recycling rates',
                monitoring_locations=['Waste sorting facilities'],
                frequency=MonitoringFrequency.MONTHLY,
                methodology='Material recovery tracking',
                regulatory_limit=None,
                trigger_level=None,
                reporting_frequency='Quarterly',
                responsible_party='Waste Management Contractor'
            )
        ]
        
        total_cost = sum(measure.cost_estimate for measure in mitigation_measures)
        monitoring_cost = 6000  # Annual waste tracking costs
        implementation_cost = total_cost + monitoring_cost
        
        return EMPComponent(
            component_name='Waste Management Plan',
            impacts_addressed=['Construction waste', 'Municipal solid waste', 'Hazardous waste'],
            mitigation_measures=mitigation_measures,
            monitoring_parameters=monitoring_params,
            compliance_requirements=self._get_waste_compliance_requirements(),
            implementation_cost=implementation_cost
        )
    
    def _generate_biodiversity_emp(self, bio_assessment: Dict, project_data: Dict) -> EMPComponent:
        """Generate Biodiversity Management Plan component"""
        
        project_size = float(project_data.get('size', 10000))
        
        mitigation_measures = []
        for measure_data in self.standard_mitigation_measures['biological_environment']:
            cost = project_size * measure_data['cost_factor'] * 100
            
            measure = MitigationMeasure(
                measure_id=measure_data['id'],
                description=measure_data['description'],
                hierarchy_level=measure_data['hierarchy'],
                impact_addressed='Biodiversity and habitat impacts',
                implementation_phase=measure_data['phase'],
                responsible_party=self._get_responsible_party(measure_data['id']),
                timeline=self._get_implementation_timeline(measure_data['phase']),
                success_criteria=self._get_success_criteria(measure_data['id']),
                cost_estimate=cost,
                effectiveness=measure_data['effectiveness']
            )
            mitigation_measures.append(measure)
        
        # Biodiversity monitoring
        monitoring_params = []
        bio_standards = self.monitoring_standards['biodiversity']
        
        for param in bio_standards['parameters']:
            monitoring_param = MonitoringParameter(
                parameter_name=param,
                monitoring_locations=['Project area', 'Reference sites', 'Offset areas'],
                frequency=bio_standards['frequencies']['construction'],
                methodology=bio_standards['methods'],
                regulatory_limit=None,
                trigger_level=None,
                reporting_frequency='Quarterly during construction, Annually during operation',
                responsible_party='Environmental Consultant'
            )
            monitoring_params.append(monitoring_param)
        
        total_cost = sum(measure.cost_estimate for measure in mitigation_measures)
        monitoring_cost = len(monitoring_params) * 8000  # Higher cost for ecological surveys
        implementation_cost = total_cost + monitoring_cost
        
        return EMPComponent(
            component_name='Biodiversity Management Plan',
            impacts_addressed=['Habitat loss', 'Species displacement', 'Ecosystem fragmentation'],
            mitigation_measures=mitigation_measures,
            monitoring_parameters=monitoring_params,
            compliance_requirements=self._get_biodiversity_compliance_requirements(),
            implementation_cost=implementation_cost
        )
    
    def _generate_soil_geology_emp(self, soil_assessment: Dict, project_data: Dict) -> EMPComponent:
        """Generate Soil and Geology Management Plan component"""
        
        project_size = float(project_data.get('size', 10000))
        
        mitigation_measures = []
        for measure_data in self.standard_mitigation_measures['soil_geology']:
            cost = project_size * measure_data['cost_factor'] * 100
            
            measure = MitigationMeasure(
                measure_id=measure_data['id'],
                description=measure_data['description'],
                hierarchy_level=measure_data['hierarchy'],
                impact_addressed='Soil erosion and geological hazards',
                implementation_phase=measure_data['phase'],
                responsible_party=self._get_responsible_party(measure_data['id']),
                timeline=self._get_implementation_timeline(measure_data['phase']),
                success_criteria=self._get_success_criteria(measure_data['id']),
                cost_estimate=cost,
                effectiveness=measure_data['effectiveness']
            )
            mitigation_measures.append(measure)
        
        # Soil monitoring
        monitoring_params = []
        soil_standards = self.monitoring_standards['soil_quality']
        
        for param in soil_standards['parameters']:
            monitoring_param = MonitoringParameter(
                parameter_name=param,
                monitoring_locations=['Disturbed areas', 'Agricultural areas', 'Sensitive locations'],
                frequency=soil_standards['frequencies']['construction'],
                methodology=soil_standards['methods'],
                regulatory_limit=self._get_regulatory_limit(param, 'soil'),
                trigger_level=self._get_trigger_level(param, 'soil'),
                reporting_frequency='Quarterly',
                responsible_party='Environmental Consultant'
            )
            monitoring_params.append(monitoring_param)
        
        total_cost = sum(measure.cost_estimate for measure in mitigation_measures)
        monitoring_cost = len(monitoring_params) * 3500
        implementation_cost = total_cost + monitoring_cost
        
        return EMPComponent(
            component_name='Soil and Geology Management Plan',
            impacts_addressed=['Soil erosion', 'Contamination', 'Geological hazards'],
            mitigation_measures=mitigation_measures,
            monitoring_parameters=monitoring_params,
            compliance_requirements=self._get_soil_compliance_requirements(),
            implementation_cost=implementation_cost
        )
    
    def _generate_socio_economic_emp(self, socio_assessment: Dict, project_data: Dict) -> EMPComponent:
        """Generate Socio-Economic Management Plan component"""
        
        project_size = float(project_data.get('size', 10000))
        
        mitigation_measures = []
        for measure_data in self.standard_mitigation_measures['socio_economic']:
            cost = project_size * measure_data['cost_factor'] * 100
            
            measure = MitigationMeasure(
                measure_id=measure_data['id'],
                description=measure_data['description'],
                hierarchy_level=measure_data['hierarchy'],
                impact_addressed='Socio-economic impacts',
                implementation_phase=measure_data['phase'],
                responsible_party=self._get_responsible_party(measure_data['id']),
                timeline=self._get_implementation_timeline(measure_data['phase']),
                success_criteria=self._get_success_criteria(measure_data['id']),
                cost_estimate=cost,
                effectiveness=measure_data['effectiveness']
            )
            mitigation_measures.append(measure)
        
        # Socio-economic monitoring
        monitoring_params = [
            MonitoringParameter(
                parameter_name='Community satisfaction',
                monitoring_locations=['Local communities'],
                frequency=MonitoringFrequency.QUARTERLY,
                methodology='Community surveys and consultations',
                regulatory_limit=None,
                trigger_level=None,
                reporting_frequency='Quarterly',
                responsible_party='Community Relations Officer'
            ),
            MonitoringParameter(
                parameter_name='Local employment rates',
                monitoring_locations=['Project area'],
                frequency=MonitoringFrequency.MONTHLY,
                methodology='Employment tracking systems',
                regulatory_limit=None,
                trigger_level=None,
                reporting_frequency='Monthly',
                responsible_party='Human Resources'
            )
        ]
        
        total_cost = sum(measure.cost_estimate for measure in mitigation_measures)
        monitoring_cost = 10000  # Community engagement costs
        implementation_cost = total_cost + monitoring_cost
        
        return EMPComponent(
            component_name='Socio-Economic Management Plan',
            impacts_addressed=['Community disruption', 'Traffic impacts', 'Economic effects'],
            mitigation_measures=mitigation_measures,
            monitoring_parameters=monitoring_params,
            compliance_requirements=self._get_socio_compliance_requirements(),
            implementation_cost=implementation_cost
        )
    
    def _generate_risk_management_emp(self, risk_assessment: Dict, project_data: Dict) -> EMPComponent:
        """Generate Risk Management Plan component"""
        
        project_size = float(project_data.get('size', 10000))
        
        # Risk-specific mitigation measures
        mitigation_measures = [
            MitigationMeasure(
                measure_id='RM_001',
                description='Establish emergency response procedures',
                hierarchy_level=MitigationHierarchy.MINIMIZE,
                impact_addressed='Environmental emergency risks',
                implementation_phase=ProjectPhase.PRE_CONSTRUCTION,
                responsible_party='Health & Safety Officer',
                timeline='Before construction commencement',
                success_criteria='Approved emergency response plan',
                cost_estimate=25000,
                effectiveness=0.90
            ),
            MitigationMeasure(
                measure_id='RM_002',
                description='Implement environmental incident reporting system',
                hierarchy_level=MitigationHierarchy.MINIMIZE,
                impact_addressed='Environmental compliance risks',
                implementation_phase=ProjectPhase.CONSTRUCTION,
                responsible_party='Environmental Manager',
                timeline='Throughout construction',
                success_criteria='Zero reportable incidents',
                cost_estimate=15000,
                effectiveness=0.85
            )
        ]
        
        # Risk monitoring
        monitoring_params = [
            MonitoringParameter(
                parameter_name='Environmental incidents',
                monitoring_locations=['Entire project area'],
                frequency=MonitoringFrequency.CONTINUOUS,
                methodology='Incident reporting and tracking system',
                regulatory_limit=None,
                trigger_level=None,
                reporting_frequency='Immediate for incidents, Monthly summary',
                responsible_party='Environmental Manager'
            )
        ]
        
        total_cost = sum(measure.cost_estimate for measure in mitigation_measures)
        monitoring_cost = 8000
        implementation_cost = total_cost + monitoring_cost
        
        return EMPComponent(
            component_name='Risk Management Plan',
            impacts_addressed=['Environmental emergencies', 'Compliance risks', 'Health and safety risks'],
            mitigation_measures=mitigation_measures,
            monitoring_parameters=monitoring_params,
            compliance_requirements=self._get_risk_compliance_requirements(),
            implementation_cost=implementation_cost
        )
    
    def _generate_implementation_timeline(self, emp_components: Dict, duration: int) -> Dict[str, List[str]]:
        """Generate EMP implementation timeline"""
        
        timeline = {
            'pre_construction': [],
            'construction_phase_1': [],
            'construction_phase_2': [],
            'construction_phase_3': [],
            'operational_early': [],
            'operational_ongoing': []
        }
        
        # Organize measures by phase
        for component in emp_components.values():
            for measure in component.mitigation_measures:
                if measure.implementation_phase == ProjectPhase.PRE_CONSTRUCTION:
                    timeline['pre_construction'].append(f"{measure.measure_id}: {measure.description}")
                elif measure.implementation_phase == ProjectPhase.CONSTRUCTION:
                    # Distribute construction measures across phases
                    phase = f"construction_phase_{(len(timeline['construction_phase_1']) % 3) + 1}"
                    timeline[phase].append(f"{measure.measure_id}: {measure.description}")
                elif measure.implementation_phase == ProjectPhase.OPERATIONAL:
                    timeline['operational_early'].append(f"{measure.measure_id}: {measure.description}")
        
        # Add ongoing operational measures
        timeline['operational_ongoing'] = [
            "Continuous environmental monitoring",
            "Regular compliance audits",
            "Stakeholder engagement maintenance",
            "Performance review and updates"
        ]
        
        return timeline
    
    def _generate_monitoring_program(self, emp_components: Dict, project_data: Dict) -> Dict[str, Any]:
        """Generate comprehensive monitoring program"""
        
        all_parameters = []
        for component in emp_components.values():
            all_parameters.extend(component.monitoring_parameters)
        
        # Organize by monitoring type
        monitoring_program = {
            'ambient_monitoring': [],
            'compliance_monitoring': [],
            'biological_monitoring': [],
            'social_monitoring': []
        }
        
        for param in all_parameters:
            if param.parameter_name in ['PM10', 'PM2.5', 'NO2', 'LAeq', 'pH']:
                monitoring_program['ambient_monitoring'].append({
                    'parameter': param.parameter_name,
                    'frequency': param.frequency.value,
                    'locations': param.monitoring_locations,
                    'methodology': param.methodology
                })
            elif 'waste' in param.parameter_name.lower() or 'water' in param.parameter_name.lower():
                monitoring_program['compliance_monitoring'].append({
                    'parameter': param.parameter_name,
                    'frequency': param.frequency.value,
                    'locations': param.monitoring_locations,
                    'methodology': param.methodology
                })
            elif 'species' in param.parameter_name.lower() or 'habitat' in param.parameter_name.lower():
                monitoring_program['biological_monitoring'].append({
                    'parameter': param.parameter_name,
                    'frequency': param.frequency.value,
                    'locations': param.monitoring_locations,
                    'methodology': param.methodology
                })
            else:
                monitoring_program['social_monitoring'].append({
                    'parameter': param.parameter_name,
                    'frequency': param.frequency.value,
                    'locations': param.monitoring_locations,
                    'methodology': param.methodology
                })
        
        # Add monitoring coordination
        monitoring_program['coordination'] = {
            'monitoring_manager': 'Environmental Manager',
            'data_management_system': 'Centralized environmental database',
            'quality_assurance': 'ISO 17025 accredited laboratories',
            'reporting_timeline': 'Monthly progress, Quarterly comprehensive'
        }
        
        return monitoring_program
    
    def _generate_reporting_schedule(self, region: str) -> Dict[str, Any]:
        """Generate reporting schedule"""
        
        return {
            'regulatory_reporting': {
                'monthly_reports': [
                    'Environmental monitoring summary',
                    'Compliance status report',
                    'Incident register'
                ],
                'quarterly_reports': [
                    'Comprehensive environmental report',
                    'EMP implementation progress',
                    'Stakeholder engagement summary'
                ],
                'annual_reports': [
                    'Annual environmental performance report',
                    'EMP effectiveness review',
                    'Environmental audit report'
                ]
            },
            'internal_reporting': {
                'daily': 'Environmental inspection reports',
                'weekly': 'Management summary reports',
                'monthly': 'Board environmental briefing'
            },
            'public_reporting': {
                'quarterly': 'Public environmental disclosure',
                'annually': 'Community environmental report'
            },
            'submission_deadlines': self._get_submission_deadlines(region)
        }
    
    def _generate_compliance_framework(self, region: str, project_type: str) -> Dict[str, Any]:
        """Generate compliance framework"""
        
        regulatory_framework = self.regulatory_frameworks[region]
        
        return {
            'applicable_legislation': regulatory_framework['federal_laws'],
            'regulatory_standards': regulatory_framework.get('standards', []),
            'competent_authorities': regulatory_framework.get('local_authorities', regulatory_framework.get('authorities', [])),
            'permit_requirements': self._get_permit_requirements(region, project_type),
            'compliance_procedures': [
                'Regular self-assessment against requirements',
                'Third-party compliance audits',
                'Regulatory inspection cooperation',
                'Non-compliance incident reporting'
            ],
            'enforcement_mechanisms': [
                'Administrative warnings',
                'Financial penalties',
                'Permit suspension/revocation',
                'Criminal prosecution for severe violations'
            ]
        }
    
    def _generate_emergency_response_plan(self, emp_components: Dict, project_data: Dict) -> Dict[str, Any]:
        """Generate emergency response plan"""
        
        return {
            'emergency_types': [
                'Chemical spill or release',
                'Fire or explosion',
                'Air quality exceedance',
                'Water contamination incident',
                'Waste management emergency',
                'Ecological incident',
                'Worker injury or fatality'
            ],
            'response_procedures': {
                'immediate_response': [
                    'Secure the scene and ensure safety',
                    'Notify emergency services if required',
                    'Implement containment measures',
                    'Notify environmental manager'
                ],
                'short_term_response': [
                    'Assess extent of impact',
                    'Notify regulatory authorities',
                    'Implement mitigation measures',
                    'Document incident details'
                ],
                'long_term_response': [
                    'Conduct detailed investigation',
                    'Implement remediation measures',
                    'Review and update procedures',
                    'Provide stakeholder communications'
                ]
            },
            'notification_requirements': {
                'internal': 'Immediate notification to Environmental Manager',
                'regulatory': 'Within 24 hours to competent authorities',
                'public': 'As required by severity and public impact'
            },
            'emergency_contacts': [
                'Project Environmental Manager: +XXX-XXX-XXXX',
                'Local Emergency Services: 999',
                'Environmental Authority: +XXX-XXX-XXXX',
                'Company Emergency Hotline: +XXX-XXX-XXXX'
            ],
            'emergency_equipment': [
                'Spill response kits',
                'Personal protective equipment',
                'First aid supplies',
                'Communication equipment',
                'Emergency shutdown systems'
            ]
        }
    
    def _generate_training_program(self, emp_components: Dict) -> Dict[str, Any]:
        """Generate training program"""
        
        return {
            'general_environmental_awareness': {
                'target_audience': 'All project personnel',
                'frequency': 'Upon induction and annually',
                'duration': '4 hours',
                'content': [
                    'Project environmental commitments',
                    'Individual environmental responsibilities',
                    'Emergency response procedures',
                    'Incident reporting requirements'
                ]
            },
            'specialized_training': {
                'environmental_management': {
                    'target_audience': 'Environmental staff',
                    'frequency': 'Upon appointment and bi-annually',
                    'duration': '16 hours',
                    'content': ['EMP implementation', 'Monitoring procedures', 'Regulatory requirements']
                },
                'waste_management': {
                    'target_audience': 'Waste handlers',
                    'frequency': 'Upon appointment and annually',
                    'duration': '8 hours',
                    'content': ['Waste segregation', 'Hazardous material handling', 'Storage requirements']
                },
                'spill_response': {
                    'target_audience': 'Emergency response team',
                    'frequency': 'Upon appointment and annually',
                    'duration': '12 hours',
                    'content': ['Spill containment', 'Chemical handling', 'Equipment operation']
                }
            },
            'training_records': {
                'documentation': 'Maintain records of all training provided',
                'competency_assessment': 'Regular assessment of staff competency',
                'refresher_training': 'Based on performance and regulatory changes'
            }
        }
    
    def _generate_performance_indicators(self, emp_components: Dict) -> List[Dict[str, Any]]:
        """Generate environmental performance indicators"""
        
        return [
            {
                'indicator': 'EMP Implementation Rate',
                'target': '100% of mitigation measures implemented on schedule',
                'measurement': 'Percentage of measures implemented vs. planned',
                'reporting_frequency': 'Monthly'
            },
            {
                'indicator': 'Environmental Compliance Rate',
                'target': '100% compliance with regulatory requirements',
                'measurement': 'Number of non-compliance incidents / Total monitoring events',
                'reporting_frequency': 'Monthly'
            },
            {
                'indicator': 'Air Quality Performance',
                'target': 'No exceedances of ambient air quality standards',
                'measurement': 'Number of exceedances / Total monitoring events',
                'reporting_frequency': 'Weekly'
            },
            {
                'indicator': 'Waste Diversion Rate',
                'target': 'Achieve 70% waste diversion from landfill',
                'measurement': 'Weight of waste recycled / Total waste generated',
                'reporting_frequency': 'Monthly'
            },
            {
                'indicator': 'Water Use Efficiency',
                'target': 'Reduce water consumption by 20% from baseline',
                'measurement': 'Water consumption per unit of production',
                'reporting_frequency': 'Monthly'
            },
            {
                'indicator': 'Community Satisfaction',
                'target': 'Maintain >80% community satisfaction rating',
                'measurement': 'Community survey results',
                'reporting_frequency': 'Quarterly'
            },
            {
                'indicator': 'Environmental Training Completion',
                'target': '100% of staff complete required environmental training',
                'measurement': 'Staff trained / Total staff requiring training',
                'reporting_frequency': 'Quarterly'
            }
        ]
    
    def _generate_audit_schedule(self) -> Dict[str, Any]:
        """Generate audit and review schedule"""
        
        return {
            'internal_audits': {
                'frequency': 'Quarterly',
                'scope': 'EMP implementation and effectiveness',
                'auditor': 'Internal environmental team',
                'reporting': 'Audit report within 2 weeks of completion'
            },
            'external_audits': {
                'frequency': 'Annually',
                'scope': 'Comprehensive EMP and regulatory compliance',
                'auditor': 'Third-party environmental consultant',
                'reporting': 'Detailed audit report and recommendations'
            },
            'regulatory_inspections': {
                'frequency': 'As scheduled by authorities',
                'preparation': 'Maintain inspection readiness at all times',
                'cooperation': 'Full cooperation and documentation support'
            },
            'emp_review_and_update': {
                'frequency': 'Annually or as triggered by changes',
                'triggers': [
                    'Regulatory changes',
                    'Project modifications',
                    'Non-compliance incidents',
                    'Effectiveness assessment results'
                ],
                'process': 'Stakeholder consultation and regulatory approval'
            }
        }
    
    def _generate_management_structure(self) -> Dict[str, Any]:
        """Generate environmental management structure"""
        
        return {
            'organizational_structure': {
                'environmental_manager': {
                    'role': 'Overall EMP implementation and compliance',
                    'qualifications': 'Environmental engineering/science degree, 5+ years experience',
                    'reporting': 'Project Director'
                },
                'environmental_officers': {
                    'role': 'Daily environmental monitoring and implementation',
                    'qualifications': 'Environmental science degree, 2+ years experience',
                    'reporting': 'Environmental Manager'
                },
                'environmental_inspectors': {
                    'role': 'Site inspections and monitoring',
                    'qualifications': 'Environmental training certification',
                    'reporting': 'Environmental Officers'
                }
            },
            'environmental_committee': {
                'composition': [
                    'Project Director (Chair)',
                    'Environmental Manager',
                    'Construction Manager',
                    'Health & Safety Manager',
                    'Community Relations Manager'
                ],
                'meeting_frequency': 'Monthly',
                'responsibilities': [
                    'Review environmental performance',
                    'Approve environmental decisions',
                    'Resolve environmental issues',
                    'Ensure resource allocation'
                ]
            },
            'external_support': {
                'environmental_consultant': 'Technical advisory and monitoring support',
                'monitoring_laboratory': 'Sample analysis and reporting',
                'waste_contractor': 'Waste collection and disposal',
                'emergency_response': 'Specialized emergency response services'
            }
        }
    
    def _generate_budget_breakdown(self, emp_components: Dict, total_cost: float) -> Dict[str, Any]:
        """Generate EMP budget breakdown"""
        
        component_costs = {}
        for name, component in emp_components.items():
            component_costs[name] = component.implementation_cost
        
        # Calculate cost categories
        mitigation_costs = sum(
            sum(measure.cost_estimate for measure in component.mitigation_measures)
            for component in emp_components.values()
        )
        
        monitoring_costs = total_cost - mitigation_costs
        
        return {
            'total_emp_budget': round(total_cost, 0),
            'cost_breakdown_by_component': {name: round(cost, 0) for name, cost in component_costs.items()},
            'cost_breakdown_by_category': {
                'mitigation_measures': round(mitigation_costs, 0),
                'monitoring_programs': round(monitoring_costs, 0),
                'management_and_reporting': round(total_cost * 0.1, 0),
                'contingency': round(total_cost * 0.1, 0)
            },
            'annual_operating_costs': {
                'monitoring': round(monitoring_costs * 0.8, 0),  # 80% of monitoring is annual
                'management_staff': 150000,  # Environmental management team
                'reporting_and_compliance': 25000,
                'training_and_capacity_building': 15000
            },
            'capital_costs': {
                'mitigation_infrastructure': round(mitigation_costs, 0),
                'monitoring_equipment': round(monitoring_costs * 0.3, 0),  # 30% for equipment
                'emergency_response_equipment': 25000
            }
        }
    
    # Helper methods for generating specific details
    def _get_responsible_party(self, measure_id: str) -> str:
        """Get responsible party for mitigation measure"""
        responsibility_map = {
            'AQ': 'Construction Contractor',
            'NS': 'Construction Contractor', 
            'WR': 'Water Management Contractor',
            'WM': 'Waste Management Contractor',
            'BE': 'Environmental Consultant',
            'SG': 'Construction Contractor',
            'SE': 'Community Relations Officer',
            'RM': 'Environmental Manager'
        }
        
        prefix = measure_id.split('_')[0]
        return responsibility_map.get(prefix, 'Environmental Manager')
    
    def _get_implementation_timeline(self, phase: ProjectPhase) -> str:
        """Get implementation timeline for phase"""
        timelines = {
            ProjectPhase.PRE_CONSTRUCTION: 'Before construction commencement',
            ProjectPhase.CONSTRUCTION: 'Throughout construction phase',
            ProjectPhase.OPERATIONAL: 'During operational phase',
            ProjectPhase.DECOMMISSIONING: 'During decommissioning'
        }
        return timelines.get(phase, 'To be determined')
    
    def _get_success_criteria(self, measure_id: str) -> str:
        """Get success criteria for mitigation measure"""
        criteria_map = {
            'AQ_001': 'Reduce dust emissions by 75%',
            'AQ_002': 'Vehicle emissions within standards',
            'NS_001': 'Noise levels below regulatory limits',
            'NS_002': 'No noise complaints during restricted hours',
            'WR_001': 'Achieve 80% water recycling rate',
            'WM_001': 'Achieve 75% waste segregation rate',
            'BE_001': 'Zero encroachment into exclusion zones',
            'SG_001': 'Erosion rates within acceptable limits',
            'SE_001': 'Community satisfaction >80%'
        }
        return criteria_map.get(measure_id, 'Meet regulatory requirements')
    
    def _get_regulatory_limit(self, parameter: str, media: str) -> Optional[float]:
        """Get regulatory limit for parameter"""
        limits = {
            'air': {
                'PM10': 150.0,  # µg/m³
                'PM2.5': 35.0,
                'NO2': 200.0
            },
            'noise': {
                'LAeq': 55.0  # dB(A) for residential
            },
            'water': {
                'pH': 8.5,
                'BOD': 30.0  # mg/L
            },
            'soil': {
                'pH': 8.5,
                'Lead': 300.0  # mg/kg
            }
        }
        return limits.get(media, {}).get(parameter)
    
    def _get_trigger_level(self, parameter: str, media: str) -> Optional[float]:
        """Get trigger level for parameter (80% of regulatory limit)"""
        limit = self._get_regulatory_limit(parameter, media)
        return limit * 0.8 if limit else None
    
    def _get_air_compliance_requirements(self) -> List[str]:
        """Get air quality compliance requirements"""
        return [
            "UAE Federal Law No. 24 of 1999 - Air Quality Standards",
            "Local air quality regulations",
            "Ambient air quality monitoring requirements",
            "Emission source registration"
        ]
    
    def _get_noise_compliance_requirements(self) -> List[str]:
        """Get noise compliance requirements"""
        return [
            "Local noise control regulations",
            "Construction noise permits",
            "Noise monitoring and reporting",
            "Community notification requirements"
        ]
    
    def _get_water_compliance_requirements(self) -> List[str]:
        """Get water compliance requirements"""
        return [
            "Water abstraction permits",
            "Wastewater discharge permits",
            "Water quality monitoring",
            "Water conservation targets"
        ]
    
    def _get_waste_compliance_requirements(self) -> List[str]:
        """Get waste compliance requirements"""
        return [
            "Waste management licenses",
            "Hazardous waste permits",
            "Waste tracking and reporting",
            "Recycling target compliance"
        ]
    
    def _get_biodiversity_compliance_requirements(self) -> List[str]:
        """Get biodiversity compliance requirements"""
        return [
            "Environmental clearance certificates",
            "Protected species permits",
            "Habitat compensation requirements",
            "Biodiversity monitoring protocols"
        ]
    
    def _get_soil_compliance_requirements(self) -> List[str]:
        """Get soil compliance requirements"""
        return [
            "Contaminated land assessment",
            "Soil quality standards compliance",
            "Erosion control requirements",
            "Agricultural land protection"
        ]
    
    def _get_socio_compliance_requirements(self) -> List[str]:
        """Get socio-economic compliance requirements"""
        return [
            "Community consultation requirements",
            "Local employment regulations",
            "Cultural heritage protection",
            "Traffic management approvals"
        ]
    
    def _get_risk_compliance_requirements(self) -> List[str]:
        """Get risk management compliance requirements"""
        return [
            "Emergency response plan approval",
            "Health and safety regulations",
            "Environmental incident reporting",
            "Risk assessment updates"
        ]
    
    def _get_submission_deadlines(self, region: str) -> Dict[str, str]:
        """Get regulatory submission deadlines"""
        if region == 'uae':
            return {
                'monthly_reports': '10th of following month',
                'quarterly_reports': '30 days after quarter end',
                'annual_reports': '90 days after year end',
                'incident_reports': 'Within 24 hours'
            }
        else:  # KSA
            return {
                'monthly_reports': '15th of following month',
                'quarterly_reports': '45 days after quarter end', 
                'annual_reports': '120 days after year end',
                'incident_reports': 'Within 24 hours'
            }
    
    def _get_permit_requirements(self, region: str, project_type: str) -> List[str]:
        """Get permit requirements"""
        base_permits = [
            'Environmental Impact Assessment Approval',
            'Construction Environmental Permit',
            'Air Emissions Permit',
            'Wastewater Discharge Permit'
        ]
        
        if project_type in ['industrial', 'infrastructure']:
            base_permits.extend([
                'Hazardous Waste Management Permit',
                'Groundwater Abstraction Permit'
            ])
        
        return base_permits