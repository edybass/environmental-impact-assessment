"""
EIA Pro Platform - Assessment Modules Package
Professional environmental assessment modules for comprehensive EIA

Created by: Edy Bassil
Email: bassileddy@gmail.com
"""

# Import all assessment modules for easy access
try:
    from .screening import EIAScreening, ScreeningResult
except ImportError:
    pass

try:
    from .waste_management import WasteManagementAssessment, WasteStream, WasteManagementPlan
except ImportError:
    pass

try:
    from .water_resources import WaterResourcesAssessment, WaterDemand, WastewaterGeneration, WaterBalance
except ImportError:
    pass

try:
    from .biological_environment import BiologicalEnvironmentAssessment, Species, Habitat, EcosystemService
except ImportError:
    pass

try:
    from .comprehensive_risk_assessment import ComprehensiveRiskAssessment, RiskEvent, RiskMitigation, EmergencyResponse
except ImportError:
    pass

try:
    from .socio_economic_environment import SocioEconomicEnvironmentAssessment, TrafficGeneration, CulturalSite, HealthRisk
except ImportError:
    pass

try:
    from .soil_geology import SoilGeologyAssessment, SoilProfile, ContaminationData, GeotechnicalData
except ImportError:
    pass

try:
    from .environmental_management_plan import EnvironmentalManagementPlan, MitigationMeasure, MonitoringParameter, EMPComponent
except ImportError:
    pass

__all__ = [
    # Original screening
    'EIAScreening',
    'ScreeningResult',
    
    # Waste Management
    'WasteManagementAssessment',
    'WasteStream',
    'WasteManagementPlan',
    
    # Water Resources
    'WaterResourcesAssessment',
    'WaterDemand',
    'WastewaterGeneration',
    'WaterBalance',
    
    # Biological Environment
    'BiologicalEnvironmentAssessment',
    'Species',
    'Habitat',
    'EcosystemService',
    
    # Risk Assessment
    'ComprehensiveRiskAssessment',
    'RiskEvent',
    'RiskMitigation',
    'EmergencyResponse',
    
    # Socio-Economic
    'SocioEconomicEnvironmentAssessment',
    'TrafficGeneration',
    'CulturalSite',
    'HealthRisk',
    
    # Soil & Geology
    'SoilGeologyAssessment',
    'SoilProfile',
    'ContaminationData',
    'GeotechnicalData',
    
    # Environmental Management Plan
    'EnvironmentalManagementPlan',
    'MitigationMeasure',
    'MonitoringParameter',
    'EMPComponent'
]

# Module version
__version__ = '2.0.0'

# Module information
__author__ = 'Edy Bassil'
__email__ = 'bassileddy@gmail.com'
__description__ = 'Comprehensive environmental assessment modules for EIA Pro Platform'