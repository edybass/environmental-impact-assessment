"""
Comprehensive Risk Assessment Module
Professional environmental and health risk assessment for EIA

Created by: Edy Bassil
Email: bassileddy@gmail.com
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import math

class RiskCategory(Enum):
    """Risk categories for comprehensive assessment"""
    ENVIRONMENTAL = "environmental"
    HEALTH_SAFETY = "health_safety"
    SOCIAL = "social"
    ECONOMIC = "economic"
    TECHNICAL = "technical"
    REGULATORY = "regulatory"

class RiskSeverity(Enum):
    """Risk severity levels"""
    CATASTROPHIC = 5  # Severe environmental damage, multiple fatalities
    MAJOR = 4         # Significant environmental impact, serious injury
    MODERATE = 3      # Moderate environmental impact, minor injury
    MINOR = 2         # Limited environmental impact, near miss
    NEGLIGIBLE = 1    # Minimal environmental impact, no injury

class RiskProbability(Enum):
    """Risk probability levels"""
    ALMOST_CERTAIN = 5  # >90% chance
    LIKELY = 4          # 60-90% chance
    POSSIBLE = 3        # 30-60% chance
    UNLIKELY = 2        # 10-30% chance
    RARE = 1            # <10% chance

@dataclass
class RiskEvent:
    """Individual risk event definition"""
    risk_id: str
    category: RiskCategory
    description: str
    causes: List[str]
    consequences: List[str]
    affected_receptors: List[str]
    severity: RiskSeverity
    probability: RiskProbability
    risk_score: int
    risk_level: str

@dataclass
class RiskMitigation:
    """Risk mitigation measure"""
    measure_id: str
    description: str
    measure_type: str  # Prevention, Reduction, Transfer, Acceptance
    effectiveness: float  # 0-1 scale
    implementation_cost: float
    implementation_time: str
    responsible_party: str

@dataclass
class EmergencyResponse:
    """Emergency response procedure"""
    emergency_type: str
    response_procedures: List[str]
    resources_required: List[str]
    response_time: str
    coordination_authorities: List[str]

class ComprehensiveRiskAssessment:
    """Complete risk assessment for environmental projects"""
    
    def __init__(self):
        self.risk_database = self._initialize_risk_database()
        self.mitigation_measures = self._initialize_mitigation_measures()
        self.emergency_procedures = self._initialize_emergency_procedures()
    
    def _initialize_risk_database(self) -> Dict[str, List[Dict]]:
        """Initialize comprehensive risk database"""
        return {
            "construction_risks": [
                {
                    "risk_id": "ENV_001",
                    "description": "Soil contamination from fuel/chemical spills",
                    "category": RiskCategory.ENVIRONMENTAL,
                    "causes": ["Equipment fuel leaks", "Chemical storage failures", "Improper waste disposal"],
                    "consequences": ["Groundwater contamination", "Soil degradation", "Ecosystem damage"],
                    "receptors": ["Groundwater", "Soil", "Vegetation", "Local community"],
                    "base_severity": RiskSeverity.MAJOR,
                    "base_probability": RiskProbability.POSSIBLE
                },
                {
                    "risk_id": "ENV_002",
                    "description": "Air quality degradation from construction activities",
                    "category": RiskCategory.ENVIRONMENTAL,
                    "causes": ["Dust generation", "Equipment emissions", "Material handling"],
                    "consequences": ["Respiratory health impacts", "Visibility reduction", "Property damage"],
                    "receptors": ["Workers", "Local residents", "Sensitive receptors"],
                    "base_severity": RiskSeverity.MODERATE,
                    "base_probability": RiskProbability.LIKELY
                },
                {
                    "risk_id": "ENV_003",
                    "description": "Noise pollution exceeding regulatory limits",
                    "category": RiskCategory.ENVIRONMENTAL,
                    "causes": ["Heavy machinery operation", "Pile driving", "Material transport"],
                    "consequences": ["Community complaints", "Hearing damage", "Wildlife disturbance"],
                    "receptors": ["Local residents", "Workers", "Wildlife"],
                    "base_severity": RiskSeverity.MINOR,
                    "base_probability": RiskProbability.LIKELY
                },
                {
                    "risk_id": "ENV_004",
                    "description": "Water resource contamination",
                    "category": RiskCategory.ENVIRONMENTAL,
                    "causes": ["Runoff from construction areas", "Chemical wash-off", "Improper drainage"],
                    "consequences": ["Surface water pollution", "Marine ecosystem damage", "Water supply contamination"],
                    "receptors": ["Surface water bodies", "Marine life", "Water users"],
                    "base_severity": RiskSeverity.MAJOR,
                    "base_probability": RiskProbability.POSSIBLE
                },
                {
                    "risk_id": "ENV_005",
                    "description": "Habitat destruction and biodiversity loss",
                    "category": RiskCategory.ENVIRONMENTAL,
                    "causes": ["Vegetation clearance", "Habitat fragmentation", "Species displacement"],
                    "consequences": ["Species population decline", "Ecosystem disruption", "Loss of ecological services"],
                    "receptors": ["Flora and fauna", "Ecosystem services", "Conservation areas"],
                    "base_severity": RiskSeverity.MAJOR,
                    "base_probability": RiskProbability.ALMOST_CERTAIN
                },
                {
                    "risk_id": "HS_001",
                    "description": "Worker injury from construction activities",
                    "category": RiskCategory.HEALTH_SAFETY,
                    "causes": ["Equipment accidents", "Falls from height", "Struck by objects"],
                    "consequences": ["Serious injury", "Fatality", "Project delays"],
                    "receptors": ["Construction workers", "Supervisors", "Visitors"],
                    "base_severity": RiskSeverity.MAJOR,
                    "base_probability": RiskProbability.POSSIBLE
                },
                {
                    "risk_id": "HS_002",
                    "description": "Public safety hazards from construction",
                    "category": RiskCategory.HEALTH_SAFETY,
                    "causes": ["Inadequate site security", "Material transport", "Dust and debris"],
                    "consequences": ["Public injury", "Property damage", "Legal liability"],
                    "receptors": ["General public", "Pedestrians", "Vehicle traffic"],
                    "base_severity": RiskSeverity.MODERATE,
                    "base_probability": RiskProbability.UNLIKELY
                },
                {
                    "risk_id": "SOC_001",
                    "description": "Community disruption from construction",
                    "category": RiskCategory.SOCIAL,
                    "causes": ["Traffic congestion", "Noise and dust", "Access restrictions"],
                    "consequences": ["Business losses", "Quality of life impacts", "Social tensions"],
                    "receptors": ["Local businesses", "Residents", "Community services"],
                    "base_severity": RiskSeverity.MODERATE,
                    "base_probability": RiskProbability.LIKELY
                },
                {
                    "risk_id": "REG_001",
                    "description": "Non-compliance with environmental regulations",
                    "category": RiskCategory.REGULATORY,
                    "causes": ["Inadequate monitoring", "Exceeding permit limits", "Poor documentation"],
                    "consequences": ["Fines and penalties", "Project suspension", "Reputation damage"],
                    "receptors": ["Project owner", "Contractors", "Regulatory authorities"],
                    "base_severity": RiskSeverity.MAJOR,
                    "base_probability": RiskProbability.UNLIKELY
                }
            ],
            "operational_risks": [
                {
                    "risk_id": "OP_ENV_001",
                    "description": "Long-term air quality impacts",
                    "category": RiskCategory.ENVIRONMENTAL,
                    "causes": ["Traffic emissions", "HVAC systems", "Waste management"],
                    "consequences": ["Chronic health effects", "Environmental degradation"],
                    "receptors": ["Building occupants", "Local community", "Environment"],
                    "base_severity": RiskSeverity.MODERATE,
                    "base_probability": RiskProbability.POSSIBLE
                },
                {
                    "risk_id": "OP_ENV_002",
                    "description": "Water resource depletion",
                    "category": RiskCategory.ENVIRONMENTAL,
                    "causes": ["High water consumption", "Inefficient systems", "Lack of recycling"],
                    "consequences": ["Water scarcity", "Ecosystem stress", "Increased costs"],
                    "receptors": ["Local water supply", "Ecosystems", "Community"],
                    "base_severity": RiskSeverity.MODERATE,
                    "base_probability": RiskProbability.LIKELY
                },
                {
                    "risk_id": "OP_ENV_003",
                    "description": "Waste management failures",
                    "category": RiskCategory.ENVIRONMENTAL,
                    "causes": ["Inadequate waste systems", "Poor segregation", "Overflow events"],
                    "consequences": ["Environmental contamination", "Health risks", "Regulatory violations"],
                    "receptors": ["Environment", "Public health", "Regulatory compliance"],
                    "base_severity": RiskSeverity.MAJOR,
                    "base_probability": RiskProbability.UNLIKELY
                }
            ],
            "climate_risks": [
                {
                    "risk_id": "CC_001",
                    "description": "Extreme heat events",
                    "category": RiskCategory.ENVIRONMENTAL,
                    "causes": ["Climate change", "Urban heat island", "Lack of adaptation"],
                    "consequences": ["Heat stress", "Infrastructure failure", "Energy demand spikes"],
                    "receptors": ["Building occupants", "Infrastructure", "Energy systems"],
                    "base_severity": RiskSeverity.MODERATE,
                    "base_probability": RiskProbability.LIKELY
                },
                {
                    "risk_id": "CC_002",
                    "description": "Water scarcity from climate change",
                    "category": RiskCategory.ENVIRONMENTAL,
                    "causes": ["Reduced precipitation", "Increased evaporation", "Temperature rise"],
                    "consequences": ["Water supply shortages", "Ecosystem stress", "Economic impacts"],
                    "receptors": ["Water supply", "Ecosystems", "Economic activities"],
                    "base_severity": RiskSeverity.MAJOR,
                    "base_probability": RiskProbability.POSSIBLE
                },
                {
                    "risk_id": "CC_003",
                    "description": "Coastal impacts from sea level rise",
                    "category": RiskCategory.ENVIRONMENTAL,
                    "causes": ["Global warming", "Thermal expansion", "Ice melt"],
                    "consequences": ["Flooding", "Infrastructure damage", "Ecosystem loss"],
                    "receptors": ["Coastal infrastructure", "Marine ecosystems", "Communities"],
                    "base_severity": RiskSeverity.MAJOR,
                    "base_probability": RiskProbability.POSSIBLE
                }
            ]
        }
    
    def _initialize_mitigation_measures(self) -> Dict[str, List[Dict]]:
        """Initialize mitigation measures database"""
        return {
            "environmental_measures": [
                {
                    "measure_id": "ENV_MIT_001",
                    "description": "Implement spill prevention and response procedures",
                    "type": "Prevention",
                    "effectiveness": 0.85,
                    "cost": 25000,
                    "implementation_time": "1 month",
                    "applicable_risks": ["ENV_001"],
                    "responsible_party": "Environmental Contractor"
                },
                {
                    "measure_id": "ENV_MIT_002",
                    "description": "Install dust suppression systems",
                    "type": "Reduction",
                    "effectiveness": 0.70,
                    "cost": 50000,
                    "implementation_time": "2 weeks",
                    "applicable_risks": ["ENV_002"],
                    "responsible_party": "Construction Contractor"
                },
                {
                    "measure_id": "ENV_MIT_003",
                    "description": "Implement noise control measures",
                    "type": "Reduction",
                    "effectiveness": 0.60,
                    "cost": 75000,
                    "implementation_time": "1 month",
                    "applicable_risks": ["ENV_003"],
                    "responsible_party": "Construction Contractor"
                },
                {
                    "measure_id": "ENV_MIT_004",
                    "description": "Install water treatment and recycling systems",
                    "type": "Prevention",
                    "effectiveness": 0.80,
                    "cost": 150000,
                    "implementation_time": "3 months",
                    "applicable_risks": ["ENV_004", "OP_ENV_002"],
                    "responsible_party": "Project Owner"
                },
                {
                    "measure_id": "ENV_MIT_005",
                    "description": "Implement biodiversity offset program",
                    "type": "Compensation",
                    "effectiveness": 0.75,
                    "cost": 200000,
                    "implementation_time": "6 months",
                    "applicable_risks": ["ENV_005"],
                    "responsible_party": "Environmental Consultant"
                }
            ],
            "health_safety_measures": [
                {
                    "measure_id": "HS_MIT_001",
                    "description": "Implement comprehensive safety training program",
                    "type": "Prevention",
                    "effectiveness": 0.80,
                    "cost": 30000,
                    "implementation_time": "2 weeks",
                    "applicable_risks": ["HS_001"],
                    "responsible_party": "Safety Officer"
                },
                {
                    "measure_id": "HS_MIT_002",
                    "description": "Install safety barriers and signage",
                    "type": "Prevention",
                    "effectiveness": 0.70,
                    "cost": 15000,
                    "implementation_time": "1 week",
                    "applicable_risks": ["HS_002"],
                    "responsible_party": "Construction Contractor"
                }
            ],
            "social_measures": [
                {
                    "measure_id": "SOC_MIT_001",
                    "description": "Implement community engagement program",
                    "type": "Reduction",
                    "effectiveness": 0.65,
                    "cost": 40000,
                    "implementation_time": "Ongoing",
                    "applicable_risks": ["SOC_001"],
                    "responsible_party": "Community Relations Officer"
                }
            ],
            "regulatory_measures": [
                {
                    "measure_id": "REG_MIT_001",
                    "description": "Establish comprehensive monitoring and reporting system",
                    "type": "Prevention",
                    "effectiveness": 0.90,
                    "cost": 60000,
                    "implementation_time": "1 month",
                    "applicable_risks": ["REG_001"],
                    "responsible_party": "Environmental Manager"
                }
            ]
        }
    
    def _initialize_emergency_procedures(self) -> Dict[str, EmergencyResponse]:
        """Initialize emergency response procedures"""
        return {
            "chemical_spill": EmergencyResponse(
                emergency_type="Chemical/Fuel Spill",
                response_procedures=[
                    "Immediately stop the source of spill if safe to do so",
                    "Isolate the spill area and prevent spread",
                    "Notify emergency response team and authorities",
                    "Deploy spill response equipment and materials",
                    "Contain and clean up spilled material",
                    "Document incident and conduct investigation"
                ],
                resources_required=[
                    "Spill response kits", "Absorbent materials", "Personal protective equipment",
                    "Emergency communication equipment", "Containment barriers"
                ],
                response_time="15 minutes",
                coordination_authorities=["Local Emergency Services", "Environmental Authority", "Fire Department"]
            ),
            "air_quality_exceedance": EmergencyResponse(
                emergency_type="Air Quality Exceedance",
                response_procedures=[
                    "Immediately suspend dust-generating activities",
                    "Activate additional dust suppression measures",
                    "Notify affected communities and authorities",
                    "Conduct additional air quality monitoring",
                    "Investigate cause and implement corrective actions",
                    "Resume activities only when levels are acceptable"
                ],
                resources_required=[
                    "Additional dust suppression equipment", "Portable air quality monitors",
                    "Communication systems", "Water trucks"
                ],
                response_time="30 minutes",
                coordination_authorities=["Environmental Authority", "Public Health Department", "Local Municipality"]
            ),
            "worker_injury": EmergencyResponse(
                emergency_type="Worker Injury/Accident",
                response_procedures=[
                    "Provide immediate first aid and medical attention",
                    "Secure the accident scene and prevent further incidents",
                    "Contact emergency medical services if required",
                    "Notify management and safety authorities",
                    "Document incident and preserve evidence",
                    "Conduct incident investigation and implement corrective actions"
                ],
                resources_required=[
                    "First aid equipment", "Emergency medical supplies", "Communication equipment",
                    "Transportation to medical facility"
                ],
                response_time="5 minutes",
                coordination_authorities=["Emergency Medical Services", "Labor Authority", "Police (if required)"]
            ),
            "environmental_incident": EmergencyResponse(
                emergency_type="Environmental Incident",
                response_procedures=[
                    "Assess the nature and extent of environmental impact",
                    "Implement immediate containment measures",
                    "Notify environmental authorities and regulatory bodies",
                    "Deploy environmental response team",
                    "Begin remediation activities as appropriate",
                    "Monitor environmental parameters and recovery"
                ],
                resources_required=[
                    "Environmental monitoring equipment", "Containment and cleanup materials",
                    "Specialist environmental contractors", "Communication systems"
                ],
                response_time="20 minutes",
                coordination_authorities=["Environmental Authority", "Marine Authority (if applicable)", "Wildlife Authority"]
            )
        }
    
    def conduct_risk_assessment(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct comprehensive risk assessment"""
        
        project_type = project_data.get('type', 'residential').lower()
        project_size = float(project_data.get('size', 10000))
        location = project_data.get('location', 'Dubai').lower()
        duration = int(project_data.get('duration', 24))
        
        # Assess construction phase risks
        construction_risks = self._assess_construction_risks(project_data)
        
        # Assess operational phase risks
        operational_risks = self._assess_operational_risks(project_data)
        
        # Assess climate-related risks
        climate_risks = self._assess_climate_risks(project_data)
        
        # Combine all risks
        all_risks = construction_risks + operational_risks + climate_risks
        
        # Calculate risk statistics
        risk_statistics = self._calculate_risk_statistics(all_risks)
        
        # Identify high-priority risks
        high_priority_risks = [risk for risk in all_risks if risk.risk_score >= 15]
        
        return {
            'total_risks_identified': len(all_risks),
            'construction_phase_risks': len(construction_risks),
            'operational_phase_risks': len(operational_risks),
            'climate_related_risks': len(climate_risks),
            'high_priority_risks': len(high_priority_risks),
            'risk_statistics': risk_statistics,
            'detailed_risks': {
                'construction': [self._risk_to_dict(risk) for risk in construction_risks],
                'operational': [self._risk_to_dict(risk) for risk in operational_risks],
                'climate': [self._risk_to_dict(risk) for risk in climate_risks]
            },
            'critical_risks_summary': [self._risk_to_dict(risk) for risk in high_priority_risks]
        }
    
    def develop_risk_management_plan(self, project_data: Dict[str, Any], risk_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Develop comprehensive risk management plan"""
        
        all_risks = []
        for phase_risks in risk_assessment['detailed_risks'].values():
            all_risks.extend(phase_risks)
        
        # Develop mitigation strategies
        mitigation_plan = self._develop_mitigation_strategies(all_risks)
        
        # Calculate implementation costs
        implementation_costs = self._calculate_implementation_costs(mitigation_plan)
        
        # Develop monitoring plan
        monitoring_plan = self._develop_monitoring_plan(all_risks)
        
        # Create emergency response plan
        emergency_response_plan = self._create_emergency_response_plan(all_risks)
        
        # Calculate residual risks
        residual_risks = self._calculate_residual_risks(all_risks, mitigation_plan)
        
        return {
            'mitigation_strategies': mitigation_plan,
            'implementation_costs': implementation_costs,
            'monitoring_plan': monitoring_plan,
            'emergency_response_plan': emergency_response_plan,
            'residual_risk_assessment': residual_risks,
            'risk_management_objectives': [
                "Reduce high and very high risks to acceptable levels",
                "Ensure compliance with all regulatory requirements",
                "Protect worker and public health and safety",
                "Minimize environmental impacts",
                "Maintain project schedule and budget"
            ],
            'implementation_timeline': self._create_implementation_timeline(mitigation_plan),
            'responsible_parties': self._identify_responsible_parties(mitigation_plan)
        }
    
    def _assess_construction_risks(self, project_data: Dict[str, Any]) -> List[RiskEvent]:
        """Assess construction phase risks"""
        risks = []
        project_type = project_data.get('type', 'residential').lower()
        project_size = float(project_data.get('size', 10000))
        location = project_data.get('location', 'Dubai').lower()
        
        for risk_data in self.risk_database['construction_risks']:
            # Adjust risk probability and severity based on project characteristics
            adjusted_severity = self._adjust_severity(risk_data, project_data)
            adjusted_probability = self._adjust_probability(risk_data, project_data)
            
            risk_score = adjusted_severity.value * adjusted_probability.value
            risk_level = self._determine_risk_level(risk_score)
            
            risk_event = RiskEvent(
                risk_id=risk_data['risk_id'],
                category=risk_data['category'],
                description=risk_data['description'],
                causes=risk_data['causes'],
                consequences=risk_data['consequences'],
                affected_receptors=risk_data['receptors'],
                severity=adjusted_severity,
                probability=adjusted_probability,
                risk_score=risk_score,
                risk_level=risk_level
            )
            
            risks.append(risk_event)
        
        return risks
    
    def _assess_operational_risks(self, project_data: Dict[str, Any]) -> List[RiskEvent]:
        """Assess operational phase risks"""
        risks = []
        
        for risk_data in self.risk_database['operational_risks']:
            adjusted_severity = self._adjust_severity(risk_data, project_data)
            adjusted_probability = self._adjust_probability(risk_data, project_data)
            
            risk_score = adjusted_severity.value * adjusted_probability.value
            risk_level = self._determine_risk_level(risk_score)
            
            risk_event = RiskEvent(
                risk_id=risk_data['risk_id'],
                category=risk_data['category'],
                description=risk_data['description'],
                causes=risk_data['causes'],
                consequences=risk_data['consequences'],
                affected_receptors=risk_data['receptors'],
                severity=adjusted_severity,
                probability=adjusted_probability,
                risk_score=risk_score,
                risk_level=risk_level
            )
            
            risks.append(risk_event)
        
        return risks
    
    def _assess_climate_risks(self, project_data: Dict[str, Any]) -> List[RiskEvent]:
        """Assess climate-related risks"""
        risks = []
        location = project_data.get('location', 'Dubai').lower()
        
        # Climate risks are more relevant for certain locations
        climate_factor = 1.2 if any(x in location for x in ['coastal', 'dubai', 'abu dhabi']) else 1.0
        
        for risk_data in self.risk_database['climate_risks']:
            adjusted_severity = self._adjust_severity(risk_data, project_data)
            adjusted_probability = self._adjust_probability(risk_data, project_data)
            
            # Apply climate factor
            if climate_factor > 1.0:
                if adjusted_probability.value < 5:
                    adjusted_probability = RiskProbability(min(adjusted_probability.value + 1, 5))
            
            risk_score = adjusted_severity.value * adjusted_probability.value
            risk_level = self._determine_risk_level(risk_score)
            
            risk_event = RiskEvent(
                risk_id=risk_data['risk_id'],
                category=risk_data['category'],
                description=risk_data['description'],
                causes=risk_data['causes'],
                consequences=risk_data['consequences'],
                affected_receptors=risk_data['receptors'],
                severity=adjusted_severity,
                probability=adjusted_probability,
                risk_score=risk_score,
                risk_level=risk_level
            )
            
            risks.append(risk_event)
        
        return risks
    
    def _adjust_severity(self, risk_data: Dict, project_data: Dict[str, Any]) -> RiskSeverity:
        """Adjust risk severity based on project characteristics"""
        base_severity = risk_data['base_severity']
        project_type = project_data.get('type', 'residential').lower()
        project_size = float(project_data.get('size', 10000))
        location = project_data.get('location', 'Dubai').lower()
        
        # Adjustment factors
        severity_adjustment = 0
        
        # Project type adjustments
        if project_type == 'industrial':
            severity_adjustment += 1
        elif project_type == 'infrastructure':
            severity_adjustment += 0.5
        
        # Project size adjustments
        if project_size > 50000:  # Large projects
            severity_adjustment += 1
        elif project_size > 25000:  # Medium projects
            severity_adjustment += 0.5
        
        # Location sensitivity adjustments
        if any(x in location for x in ['protected', 'reserve', 'coastal']):
            severity_adjustment += 1
        elif any(x in location for x in ['urban', 'city', 'downtown']):
            severity_adjustment += 0.5
        
        # Apply adjustment
        adjusted_value = min(base_severity.value + int(severity_adjustment), 5)
        return RiskSeverity(max(adjusted_value, 1))
    
    def _adjust_probability(self, risk_data: Dict, project_data: Dict[str, Any]) -> RiskProbability:
        """Adjust risk probability based on project characteristics"""
        base_probability = risk_data['base_probability']
        project_type = project_data.get('type', 'residential').lower()
        duration = int(project_data.get('duration', 24))
        
        # Adjustment factors
        probability_adjustment = 0
        
        # Project duration adjustments
        if duration > 36:  # Long projects
            probability_adjustment += 1
        elif duration > 24:  # Medium duration
            probability_adjustment += 0.5
        
        # Project complexity adjustments
        if project_type in ['industrial', 'infrastructure']:
            probability_adjustment += 0.5
        
        # Apply adjustment
        adjusted_value = min(base_probability.value + int(probability_adjustment), 5)
        return RiskProbability(max(adjusted_value, 1))
    
    def _determine_risk_level(self, risk_score: int) -> str:
        """Determine risk level based on score"""
        if risk_score >= 20:
            return "Very High"
        elif risk_score >= 15:
            return "High"
        elif risk_score >= 10:
            return "Medium"
        elif risk_score >= 5:
            return "Low"
        else:
            return "Very Low"
    
    def _calculate_risk_statistics(self, risks: List[RiskEvent]) -> Dict[str, Any]:
        """Calculate risk statistics"""
        stats = {
            'by_category': {},
            'by_risk_level': {},
            'average_risk_score': 0,
            'highest_risk_score': 0
        }
        
        total_score = 0
        max_score = 0
        
        for risk in risks:
            # Count by category
            category = risk.category.value
            stats['by_category'][category] = stats['by_category'].get(category, 0) + 1
            
            # Count by risk level
            level = risk.risk_level
            stats['by_risk_level'][level] = stats['by_risk_level'].get(level, 0) + 1
            
            # Calculate score statistics
            total_score += risk.risk_score
            max_score = max(max_score, risk.risk_score)
        
        stats['average_risk_score'] = round(total_score / len(risks), 1) if risks else 0
        stats['highest_risk_score'] = max_score
        
        return stats
    
    def _develop_mitigation_strategies(self, risks: List[Dict]) -> Dict[str, List[Dict]]:
        """Develop mitigation strategies for identified risks"""
        mitigation_strategies = {
            'environmental': [],
            'health_safety': [],
            'social': [],
            'regulatory': []
        }
        
        # Map risks to mitigation measures
        risk_ids = [risk['risk_id'] for risk in risks if risk['risk_score'] >= 10]  # Focus on medium+ risks
        
        all_measures = []
        for category, measures in self.mitigation_measures.items():
            all_measures.extend(measures)
        
        for measure in all_measures:
            applicable_risks = [risk_id for risk_id in measure.get('applicable_risks', []) if risk_id in risk_ids]
            if applicable_risks:
                measure_info = {
                    'measure_id': measure['measure_id'],
                    'description': measure['description'],
                    'type': measure['type'],
                    'effectiveness': measure['effectiveness'],
                    'cost': measure['cost'],
                    'implementation_time': measure['implementation_time'],
                    'applicable_risks': applicable_risks,
                    'responsible_party': measure['responsible_party']
                }
                
                # Categorize measures
                if 'ENV' in measure['measure_id']:
                    mitigation_strategies['environmental'].append(measure_info)
                elif 'HS' in measure['measure_id']:
                    mitigation_strategies['health_safety'].append(measure_info)
                elif 'SOC' in measure['measure_id']:
                    mitigation_strategies['social'].append(measure_info)
                elif 'REG' in measure['measure_id']:
                    mitigation_strategies['regulatory'].append(measure_info)
        
        return mitigation_strategies
    
    def _calculate_implementation_costs(self, mitigation_plan: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """Calculate mitigation implementation costs"""
        costs = {
            'by_category': {},
            'by_measure_type': {},
            'total_cost': 0,
            'annual_operating_cost': 0
        }
        
        for category, measures in mitigation_plan.items():
            category_cost = sum(measure['cost'] for measure in measures)
            costs['by_category'][category] = category_cost
            costs['total_cost'] += category_cost
            
            for measure in measures:
                measure_type = measure['type']
                costs['by_measure_type'][measure_type] = costs['by_measure_type'].get(measure_type, 0) + measure['cost']
        
        # Estimate annual operating costs (20% of capital costs)
        costs['annual_operating_cost'] = costs['total_cost'] * 0.20
        costs['lifecycle_cost_20_years'] = costs['total_cost'] + (costs['annual_operating_cost'] * 20)
        
        return costs
    
    def _develop_monitoring_plan(self, risks: List[Dict]) -> Dict[str, Any]:
        """Develop risk monitoring plan"""
        monitoring_requirements = {
            'environmental_monitoring': [],
            'health_safety_monitoring': [],
            'performance_indicators': [],
            'reporting_schedule': {}
        }
        
        # Environmental monitoring based on risks
        env_risks = [risk for risk in risks if 'ENV' in risk['risk_id'] and risk['risk_score'] >= 10]
        if env_risks:
            monitoring_requirements['environmental_monitoring'] = [
                "Daily air quality monitoring during construction",
                "Weekly noise level measurements",
                "Monthly water quality testing",
                "Quarterly biodiversity surveys",
                "Continuous dust monitoring systems"
            ]
        
        # Health and safety monitoring
        hs_risks = [risk for risk in risks if 'HS' in risk['risk_id'] and risk['risk_score'] >= 10]
        if hs_risks:
            monitoring_requirements['health_safety_monitoring'] = [
                "Daily safety inspections",
                "Weekly safety training records",
                "Monthly incident reporting",
                "Quarterly emergency drill exercises",
                "Annual safety audit"
            ]
        
        # Key performance indicators
        monitoring_requirements['performance_indicators'] = [
            "Zero environmental incidents target",
            "Zero lost time injuries target",
            "100% compliance with permits and regulations",
            "95% effectiveness of mitigation measures",
            "Community complaint response within 24 hours"
        ]
        
        # Reporting schedule
        monitoring_requirements['reporting_schedule'] = {
            'daily': ['Safety inspections', 'Environmental monitoring'],
            'weekly': ['Progress reports', 'Incident summaries'],
            'monthly': ['Compliance reports', 'KPI dashboards'],
            'quarterly': ['Comprehensive risk assessment updates'],
            'annually': ['Risk management plan review']
        }
        
        return monitoring_requirements
    
    def _create_emergency_response_plan(self, risks: List[Dict]) -> Dict[str, Any]:
        """Create emergency response plan"""
        emergency_plan = {
            'emergency_procedures': {},
            'emergency_contacts': [],
            'resource_requirements': [],
            'training_requirements': []
        }
        
        # Identify relevant emergency types based on risks
        high_risks = [risk for risk in risks if risk['risk_score'] >= 15]
        
        relevant_emergencies = set()
        for risk in high_risks:
            if 'contamination' in risk['description'].lower():
                relevant_emergencies.add('chemical_spill')
            if 'air quality' in risk['description'].lower():
                relevant_emergencies.add('air_quality_exceedance')
            if 'injury' in risk['description'].lower():
                relevant_emergencies.add('worker_injury')
            if 'environmental' in risk['description'].lower():
                relevant_emergencies.add('environmental_incident')
        
        # Add relevant emergency procedures
        for emergency_type in relevant_emergencies:
            if emergency_type in self.emergency_procedures:
                emergency_plan['emergency_procedures'][emergency_type] = {
                    'procedures': self.emergency_procedures[emergency_type].response_procedures,
                    'resources': self.emergency_procedures[emergency_type].resources_required,
                    'response_time': self.emergency_procedures[emergency_type].response_time,
                    'authorities': self.emergency_procedures[emergency_type].coordination_authorities
                }
        
        # Emergency contacts
        emergency_plan['emergency_contacts'] = [
            "Project Manager: +971-XX-XXXXXXX",
            "Environmental Manager: +971-XX-XXXXXXX",
            "Safety Officer: +971-XX-XXXXXXX",
            "Local Emergency Services: 999",
            "Environmental Authority: +971-XX-XXXXXXX"
        ]
        
        # Training requirements
        emergency_plan['training_requirements'] = [
            "Emergency response training for all staff",
            "Spill response training for environmental team",
            "First aid training for supervisors",
            "Regular emergency drill exercises",
            "Annual refresher training"
        ]
        
        return emergency_plan
    
    def _calculate_residual_risks(self, risks: List[Dict], mitigation_plan: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """Calculate residual risks after mitigation"""
        # Create mapping of measures to risks
        measure_effectiveness = {}
        for category, measures in mitigation_plan.items():
            for measure in measures:
                for risk_id in measure['applicable_risks']:
                    if risk_id not in measure_effectiveness:
                        measure_effectiveness[risk_id] = []
                    measure_effectiveness[risk_id].append(measure['effectiveness'])
        
        residual_risks = []
        total_risk_reduction = 0
        
        for risk in risks:
            original_score = risk['risk_score']
            
            # Calculate combined effectiveness of applicable measures
            if risk['risk_id'] in measure_effectiveness:
                effectiveness_values = measure_effectiveness[risk['risk_id']]
                # Combined effectiveness (not simply additive)
                combined_effectiveness = 1 - (1 - max(effectiveness_values)) * (1 - (sum(effectiveness_values) - max(effectiveness_values)) / len(effectiveness_values))
                combined_effectiveness = min(combined_effectiveness, 0.95)  # Maximum 95% reduction
            else:
                combined_effectiveness = 0
            
            # Calculate residual risk score
            residual_score = original_score * (1 - combined_effectiveness)
            risk_reduction = original_score - residual_score
            total_risk_reduction += risk_reduction
            
            residual_risks.append({
                'risk_id': risk['risk_id'],
                'description': risk['description'],
                'original_score': original_score,
                'mitigation_effectiveness': round(combined_effectiveness * 100, 1),
                'residual_score': round(residual_score, 1),
                'residual_level': self._determine_risk_level(int(residual_score)),
                'risk_reduction': round(risk_reduction, 1)
            })
        
        return {
            'residual_risks': residual_risks,
            'total_risk_reduction': round(total_risk_reduction, 1),
            'average_risk_reduction': round(total_risk_reduction / len(risks), 1) if risks else 0,
            'risks_above_acceptable': len([r for r in residual_risks if r['residual_score'] >= 10]),
            'overall_risk_status': 'Acceptable' if all(r['residual_score'] < 10 for r in residual_risks) else 'Requires Additional Measures'
        }
    
    def _create_implementation_timeline(self, mitigation_plan: Dict[str, List[Dict]]) -> Dict[str, List[str]]:
        """Create implementation timeline for mitigation measures"""
        timeline = {
            'immediate': [],  # Within 1 week
            'short_term': [],  # 1 week - 1 month
            'medium_term': [],  # 1-3 months
            'long_term': []  # 3+ months
        }
        
        for category, measures in mitigation_plan.items():
            for measure in measures:
                time_str = measure['implementation_time'].lower()
                if 'week' in time_str and ('1 week' in time_str or 'immediate' in time_str):
                    timeline['immediate'].append(measure['description'])
                elif 'week' in time_str or '1 month' in time_str:
                    timeline['short_term'].append(measure['description'])
                elif '2 month' in time_str or '3 month' in time_str:
                    timeline['medium_term'].append(measure['description'])
                else:
                    timeline['long_term'].append(measure['description'])
        
        return timeline
    
    def _identify_responsible_parties(self, mitigation_plan: Dict[str, List[Dict]]) -> Dict[str, List[str]]:
        """Identify responsible parties for implementation"""
        responsibilities = {}
        
        for category, measures in mitigation_plan.items():
            for measure in measures:
                party = measure['responsible_party']
                if party not in responsibilities:
                    responsibilities[party] = []
                responsibilities[party].append(measure['description'])
        
        return responsibilities
    
    def _risk_to_dict(self, risk: RiskEvent) -> Dict[str, Any]:
        """Convert RiskEvent to dictionary"""
        return {
            'risk_id': risk.risk_id,
            'category': risk.category.value,
            'description': risk.description,
            'causes': risk.causes,
            'consequences': risk.consequences,
            'affected_receptors': risk.affected_receptors,
            'severity': risk.severity.name,
            'probability': risk.probability.name,
            'risk_score': risk.risk_score,
            'risk_level': risk.risk_level
        }