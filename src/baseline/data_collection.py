"""
Baseline Data Collection Framework
Comprehensive system for environmental baseline studies

Author: Edy Bassil
Email: bassileddy@gmail.com
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class SamplingFrequency(Enum):
    """Sampling frequency standards."""
    CONTINUOUS = "continuous"
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    SEASONAL = "seasonal"
    ANNUAL = "annual"


class DataQuality(Enum):
    """Data quality indicators."""
    VALIDATED = "validated"
    PRELIMINARY = "preliminary"
    ESTIMATED = "estimated"
    MISSING = "missing"
    REJECTED = "rejected"


@dataclass
class SamplingLocation:
    """Environmental sampling location."""
    location_id: str
    name: str
    latitude: float
    longitude: float
    elevation: float
    location_type: str  # air, water, soil, noise, ecology
    description: str
    access_notes: Optional[str] = None
    photos: List[str] = field(default_factory=list)
    established_date: datetime = field(default_factory=datetime.now)
    active: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FieldMeasurement:
    """Field measurement record."""
    measurement_id: str
    location_id: str
    parameter: str
    value: float
    unit: str
    measurement_date: datetime
    measurement_time: str
    operator: str
    equipment_id: str
    weather_conditions: Dict[str, Any]
    quality_flag: DataQuality
    notes: Optional[str] = None
    qc_status: str = "pending"
    lab_id: Optional[str] = None


@dataclass
class BaselineDataset:
    """Baseline monitoring dataset."""
    dataset_id: str
    project_id: int
    parameter_group: str  # air, water, noise, ecology, social
    start_date: datetime
    end_date: datetime
    locations: List[SamplingLocation]
    measurements: List[FieldMeasurement]
    sampling_frequency: SamplingFrequency
    completeness_percent: float
    validation_status: str
    summary_statistics: Dict[str, Any]


class BaselineDataCollector:
    """Manages baseline environmental data collection."""
    
    def __init__(self):
        # Sampling requirements by parameter type
        self.sampling_requirements = {
            'air_quality': {
                'parameters': ['pm10', 'pm25', 'no2', 'so2', 'co', 'o3', 'voc', 'h2s', 'nh3'],
                'frequency': SamplingFrequency.CONTINUOUS,
                'duration_days': 365,
                'locations_min': 3,
                'equipment': ['Beta attenuation monitor', 'Chemiluminescence analyzer', 'UV analyzer'],
                'standards': {'pm10_24hr': 150, 'pm25_24hr': 65, 'no2_annual': 100}
            },
            'meteorology': {
                'parameters': ['wind_speed', 'wind_direction', 'temperature', 'humidity', 
                              'pressure', 'rainfall', 'solar_radiation'],
                'frequency': SamplingFrequency.HOURLY,
                'duration_days': 365,
                'locations_min': 1,
                'equipment': ['Automatic weather station', 'Data logger'],
                'data_recovery': 0.9  # 90% minimum
            },
            'noise': {
                'parameters': ['laeq', 'la90', 'la10', 'lamax', 'lamin'],
                'frequency': SamplingFrequency.CONTINUOUS,
                'duration_days': 7,  # Per location
                'locations_min': 5,
                'equipment': ['Type 1 sound level meter', 'Acoustic calibrator'],
                'measurement_periods': ['day', 'evening', 'night']
            },
            'water_quality': {
                'parameters': ['ph', 'do', 'bod', 'cod', 'tss', 'tds', 'turbidity', 
                              'nutrients', 'heavy_metals', 'hydrocarbons'],
                'frequency': SamplingFrequency.MONTHLY,
                'duration_days': 365,
                'locations_min': 3,
                'equipment': ['Multi-parameter probe', 'Sample bottles', 'Cooler'],
                'preservation': {'heavy_metals': 'HNO3', 'nutrients': 'H2SO4'}
            },
            'groundwater': {
                'parameters': ['depth', 'ph', 'tds', 'hardness', 'chlorides', 'sulfates', 
                              'nitrates', 'heavy_metals', 'tph'],
                'frequency': SamplingFrequency.QUARTERLY,
                'duration_days': 365,
                'locations_min': 3,
                'equipment': ['Water level meter', 'Bailer', 'Peristaltic pump'],
                'well_development': True
            },
            'soil': {
                'parameters': ['texture', 'ph', 'organic_matter', 'nutrients', 'salinity', 
                              'heavy_metals', 'tph', 'pesticides'],
                'frequency': SamplingFrequency.SEASONAL,
                'duration_days': 365,
                'locations_min': 5,
                'depths': [0.0, 0.3, 1.0],  # meters
                'equipment': ['Soil auger', 'GPS unit', 'Sample bags']
            },
            'ecology': {
                'parameters': ['flora_species', 'fauna_species', 'habitat_types', 
                              'vegetation_cover', 'species_abundance'],
                'frequency': SamplingFrequency.SEASONAL,
                'duration_days': 365,
                'locations_min': 10,
                'survey_methods': ['Quadrat', 'Transect', 'Point count', 'Camera trap'],
                'timing': {'birds': 'dawn/dusk', 'mammals': 'night', 'reptiles': 'morning'}
            },
            'marine': {
                'parameters': ['coral_cover', 'fish_abundance', 'seagrass_density', 
                              'benthic_fauna', 'water_quality'],
                'frequency': SamplingFrequency.SEASONAL,
                'duration_days': 365,
                'locations_min': 5,
                'survey_methods': ['SCUBA transect', 'Drop camera', 'Grab sampling'],
                'tide_consideration': True
            },
            'social': {
                'parameters': ['population', 'employment', 'land_use', 'infrastructure', 
                              'health_facilities', 'schools', 'cultural_sites'],
                'frequency': SamplingFrequency.ANNUAL,
                'duration_days': 30,
                'survey_size': 200,  # households
                'methods': ['Questionnaire', 'Focus groups', 'Key informant interviews'],
                'stratification': ['age', 'gender', 'occupation', 'location']
            }
        }
        
        # Quality control requirements
        self.qc_requirements = {
            'field_duplicates': 0.1,  # 10% of samples
            'field_blanks': 0.05,     # 5% of samples
            'lab_duplicates': 0.1,
            'spike_recovery': (0.8, 1.2),  # 80-120%
            'calibration_frequency': {
                'daily': ['ph', 'do', 'turbidity'],
                'weekly': ['sound_level_meter'],
                'monthly': ['air_monitors']
            }
        }
    
    def create_sampling_plan(
        self,
        project_area: Dict[str, Any],
        parameter_groups: List[str],
        project_duration_months: int,
        sensitive_receptors: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Create comprehensive baseline sampling plan.
        
        Args:
            project_area: Project boundary and characteristics
            parameter_groups: Required baseline parameters
            project_duration_months: Project duration
            sensitive_receptors: Nearby sensitive locations
            
        Returns:
            Detailed sampling plan
        """
        sampling_plan = {
            'project_info': project_area,
            'duration': self._calculate_baseline_duration(project_duration_months),
            'parameter_groups': {},
            'locations': [],
            'schedule': [],
            'qc_plan': {},
            'budget_estimate': 0
        }
        
        # Plan for each parameter group
        for group in parameter_groups:
            if group not in self.sampling_requirements:
                logger.warning(f"Unknown parameter group: {group}")
                continue
            
            requirements = self.sampling_requirements[group]
            
            # Determine sampling locations
            locations = self._determine_sampling_locations(
                project_area,
                sensitive_receptors,
                group,
                requirements['locations_min']
            )
            
            # Create sampling schedule
            schedule = self._create_sampling_schedule(
                requirements['frequency'],
                requirements['duration_days'],
                group
            )
            
            # Estimate costs
            cost = self._estimate_sampling_cost(
                group,
                len(locations),
                requirements['duration_days'],
                requirements['frequency']
            )
            
            sampling_plan['parameter_groups'][group] = {
                'parameters': requirements['parameters'],
                'locations': locations,
                'frequency': requirements['frequency'].value,
                'duration_days': requirements['duration_days'],
                'equipment': requirements.get('equipment', []),
                'schedule': schedule,
                'estimated_cost': cost
            }
            
            sampling_plan['locations'].extend(locations)
            sampling_plan['budget_estimate'] += cost
        
        # Add QC plan
        sampling_plan['qc_plan'] = self._create_qc_plan(parameter_groups)
        
        # Create integrated schedule
        sampling_plan['schedule'] = self._integrate_schedules(
            sampling_plan['parameter_groups']
        )
        
        return sampling_plan
    
    def validate_baseline_data(
        self,
        dataset: BaselineDataset,
        parameter_group: str
    ) -> Dict[str, Any]:
        """
        Validate baseline dataset completeness and quality.
        
        Args:
            dataset: Baseline dataset
            parameter_group: Parameter group type
            
        Returns:
            Validation report
        """
        validation_report = {
            'dataset_id': dataset.dataset_id,
            'valid': True,
            'completeness': {},
            'quality_issues': [],
            'statistical_validity': {},
            'recommendations': []
        }
        
        requirements = self.sampling_requirements.get(parameter_group, {})
        
        # Check temporal coverage
        expected_duration = requirements.get('duration_days', 365)
        actual_duration = (dataset.end_date - dataset.start_date).days
        
        if actual_duration < expected_duration * 0.9:  # Allow 10% tolerance
            validation_report['valid'] = False
            validation_report['quality_issues'].append(
                f"Insufficient temporal coverage: {actual_duration} days vs {expected_duration} required"
            )
        
        # Check spatial coverage
        min_locations = requirements.get('locations_min', 1)
        if len(dataset.locations) < min_locations:
            validation_report['valid'] = False
            validation_report['quality_issues'].append(
                f"Insufficient sampling locations: {len(dataset.locations)} vs {min_locations} required"
            )
        
        # Check data completeness by parameter
        for param in requirements.get('parameters', []):
            param_data = [m for m in dataset.measurements if m.parameter == param]
            expected_measurements = self._calculate_expected_measurements(
                requirements['frequency'],
                expected_duration,
                len(dataset.locations)
            )
            
            completeness = len(param_data) / expected_measurements if expected_measurements > 0 else 0
            validation_report['completeness'][param] = completeness
            
            if completeness < 0.8:  # 80% minimum
                validation_report['quality_issues'].append(
                    f"Low data completeness for {param}: {completeness:.1%}"
                )
        
        # Statistical validity checks
        validation_report['statistical_validity'] = self._check_statistical_validity(
            dataset.measurements,
            parameter_group
        )
        
        # Generate recommendations
        if validation_report['quality_issues']:
            validation_report['recommendations'] = self._generate_data_recommendations(
                validation_report['quality_issues'],
                parameter_group
            )
        
        return validation_report
    
    def analyze_baseline_variability(
        self,
        measurements: List[FieldMeasurement],
        parameter: str
    ) -> Dict[str, Any]:
        """
        Analyze temporal and spatial variability in baseline data.
        
        Args:
            measurements: Field measurements
            parameter: Parameter to analyze
            
        Returns:
            Variability analysis
        """
        # Filter measurements for parameter
        param_data = [m for m in measurements if m.parameter == parameter]
        
        if not param_data:
            return {'error': 'No data for parameter'}
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame([
            {
                'date': m.measurement_date,
                'location': m.location_id,
                'value': m.value,
                'month': m.measurement_date.month,
                'season': self._get_season(m.measurement_date),
                'weekday': m.measurement_date.weekday()
            }
            for m in param_data
        ])
        
        analysis = {
            'parameter': parameter,
            'n_measurements': len(df),
            'temporal_variability': {},
            'spatial_variability': {},
            'patterns': {}
        }
        
        # Temporal variability
        analysis['temporal_variability'] = {
            'daily': self._analyze_daily_variation(df),
            'weekly': self._analyze_weekly_variation(df),
            'monthly': df.groupby('month')['value'].agg(['mean', 'std']).to_dict(),
            'seasonal': df.groupby('season')['value'].agg(['mean', 'std']).to_dict()
        }
        
        # Spatial variability
        location_stats = df.groupby('location')['value'].agg(['mean', 'std', 'min', 'max'])
        analysis['spatial_variability'] = {
            'by_location': location_stats.to_dict(),
            'coefficient_of_variation': location_stats['std'].mean() / location_stats['mean'].mean()
        }
        
        # Identify patterns
        analysis['patterns'] = {
            'trend': self._detect_trend(df),
            'seasonality': self._detect_seasonality(df),
            'outliers': self._detect_outliers(df)
        }
        
        return analysis
    
    def generate_baseline_report(
        self,
        datasets: List[BaselineDataset],
        project_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate comprehensive baseline conditions report.
        
        Args:
            datasets: All baseline datasets
            project_info: Project information
            
        Returns:
            Baseline report structure
        """
        report = {
            'project': project_info,
            'executive_summary': {},
            'methodology': {},
            'baseline_conditions': {},
            'data_quality': {},
            'limitations': [],
            'conclusions': []
        }
        
        # Methodology section
        report['methodology'] = {
            'sampling_locations': self._summarize_locations(datasets),
            'parameters_monitored': self._list_all_parameters(datasets),
            'sampling_periods': self._summarize_periods(datasets),
            'analytical_methods': self._get_analytical_methods(datasets),
            'qaqc_procedures': self.qc_requirements
        }
        
        # Baseline conditions by parameter group
        for dataset in datasets:
            group = dataset.parameter_group
            
            # Statistical summary
            stats = self._calculate_baseline_statistics(dataset.measurements)
            
            # Comparison with standards
            exceedances = self._check_standard_exceedances(
                dataset.measurements,
                group
            )
            
            # Variability analysis
            variability = {}
            for param in self._get_unique_parameters(dataset.measurements):
                variability[param] = self.analyze_baseline_variability(
                    dataset.measurements,
                    param
                )
            
            report['baseline_conditions'][group] = {
                'summary_statistics': stats,
                'exceedances': exceedances,
                'variability': variability,
                'data_quality': {
                    'completeness': dataset.completeness_percent,
                    'validation_status': dataset.validation_status
                }
            }
        
        # Data quality summary
        report['data_quality'] = self._summarize_data_quality(datasets)
        
        # Limitations
        report['limitations'] = self._identify_limitations(datasets)
        
        # Executive summary
        report['executive_summary'] = self._create_executive_summary(
            report['baseline_conditions']
        )
        
        return report
    
    def _calculate_baseline_duration(self, project_months: int) -> int:
        """Calculate required baseline monitoring duration."""
        if project_months <= 12:
            return 365  # 1 year minimum
        elif project_months <= 36:
            return 365  # 1 year
        else:
            return 730  # 2 years for major projects
    
    def _determine_sampling_locations(
        self,
        project_area: Dict[str, Any],
        receptors: List[Dict[str, Any]],
        parameter_group: str,
        min_locations: int
    ) -> List[SamplingLocation]:
        """Determine optimal sampling locations."""
        locations = []
        
        # Add receptor-based locations
        for receptor in receptors[:min_locations]:
            locations.append(SamplingLocation(
                location_id=f"{parameter_group}_{len(locations)+1}",
                name=f"{receptor['name']} - {parameter_group}",
                latitude=receptor['lat'],
                longitude=receptor['lon'],
                elevation=receptor.get('elevation', 0),
                location_type=parameter_group,
                description=f"Near {receptor['type']}"
            ))
        
        # Add boundary locations if needed
        if len(locations) < min_locations:
            # Add locations at project boundaries
            bounds = project_area.get('boundaries', {})
            locations.extend(self._create_boundary_locations(
                bounds,
                parameter_group,
                min_locations - len(locations)
            ))
        
        return locations
    
    def _create_sampling_schedule(
        self,
        frequency: SamplingFrequency,
        duration_days: int,
        parameter_group: str
    ) -> List[Dict[str, Any]]:
        """Create detailed sampling schedule."""
        schedule = []
        start_date = datetime.now()
        
        if frequency == SamplingFrequency.CONTINUOUS:
            # Continuous monitoring
            schedule.append({
                'start': start_date,
                'end': start_date + timedelta(days=duration_days),
                'frequency': 'Continuous',
                'type': parameter_group
            })
        
        elif frequency == SamplingFrequency.HOURLY:
            # Hourly measurements
            for day in range(duration_days):
                date = start_date + timedelta(days=day)
                schedule.append({
                    'date': date,
                    'times': [f"{h:02d}:00" for h in range(24)],
                    'type': parameter_group
                })
        
        elif frequency == SamplingFrequency.DAILY:
            # Daily measurements
            for day in range(duration_days):
                schedule.append({
                    'date': start_date + timedelta(days=day),
                    'time': '09:00',
                    'type': parameter_group
                })
        
        elif frequency == SamplingFrequency.WEEKLY:
            # Weekly measurements
            weeks = duration_days // 7
            for week in range(weeks):
                schedule.append({
                    'date': start_date + timedelta(weeks=week),
                    'type': parameter_group
                })
        
        elif frequency == SamplingFrequency.MONTHLY:
            # Monthly measurements
            months = duration_days // 30
            for month in range(months):
                schedule.append({
                    'date': start_date + timedelta(days=month*30),
                    'type': parameter_group
                })
        
        elif frequency == SamplingFrequency.SEASONAL:
            # Seasonal measurements (4 per year)
            seasons = ['Winter', 'Spring', 'Summer', 'Fall']
            for i in range(4):
                schedule.append({
                    'date': start_date + timedelta(days=i*90),
                    'season': seasons[i],
                    'type': parameter_group
                })
        
        return schedule
    
    def _estimate_sampling_cost(
        self,
        parameter_group: str,
        n_locations: int,
        duration_days: int,
        frequency: SamplingFrequency
    ) -> float:
        """Estimate sampling program cost."""
        # Base costs per parameter group (USD)
        base_costs = {
            'air_quality': {
                'equipment': 50000,
                'per_sample': 200,
                'per_day': 500
            },
            'meteorology': {
                'equipment': 20000,
                'per_day': 100
            },
            'noise': {
                'equipment': 15000,
                'per_location_day': 300
            },
            'water_quality': {
                'per_sample': 500,
                'per_location': 200
            },
            'groundwater': {
                'well_installation': 5000,
                'per_sample': 600
            },
            'soil': {
                'per_sample': 400,
                'per_location': 150
            },
            'ecology': {
                'per_survey_day': 2000,
                'equipment': 10000
            },
            'marine': {
                'per_survey_day': 5000,
                'equipment': 30000
            },
            'social': {
                'per_household': 50,
                'analysis': 10000
            }
        }
        
        costs = base_costs.get(parameter_group, {'per_sample': 300})
        total_cost = 0
        
        # Equipment costs
        total_cost += costs.get('equipment', 0)
        
        # Sampling costs
        if frequency == SamplingFrequency.CONTINUOUS:
            total_cost += costs.get('per_day', 300) * duration_days * n_locations
        else:
            # Calculate number of sampling events
            n_samples = self._calculate_expected_measurements(
                frequency,
                duration_days,
                n_locations
            )
            total_cost += costs.get('per_sample', 300) * n_samples
        
        # Add location-specific costs
        total_cost += costs.get('per_location', 0) * n_locations
        
        # Add 20% for QA/QC and reporting
        total_cost *= 1.2
        
        return total_cost
    
    def _calculate_expected_measurements(
        self,
        frequency: SamplingFrequency,
        duration_days: int,
        n_locations: int
    ) -> int:
        """Calculate expected number of measurements."""
        frequency_multipliers = {
            SamplingFrequency.CONTINUOUS: duration_days * 24,  # Hourly data
            SamplingFrequency.HOURLY: duration_days * 24,
            SamplingFrequency.DAILY: duration_days,
            SamplingFrequency.WEEKLY: duration_days // 7,
            SamplingFrequency.MONTHLY: duration_days // 30,
            SamplingFrequency.QUARTERLY: duration_days // 90,
            SamplingFrequency.SEASONAL: 4,
            SamplingFrequency.ANNUAL: 1
        }
        
        multiplier = frequency_multipliers.get(frequency, 1)
        return int(multiplier * n_locations)
    
    def _create_qc_plan(self, parameter_groups: List[str]) -> Dict[str, Any]:
        """Create quality control plan."""
        qc_plan = {
            'field_qc': {
                'duplicates': self.qc_requirements['field_duplicates'],
                'blanks': self.qc_requirements['field_blanks'],
                'calibration': {}
            },
            'laboratory_qc': {
                'duplicates': self.qc_requirements['lab_duplicates'],
                'spike_recovery': self.qc_requirements['spike_recovery'],
                'detection_limits': {}
            },
            'data_validation': {
                'levels': ['Level 1 - Completeness', 'Level 2 - QC checks', 
                          'Level 3 - Statistical', 'Level 4 - Expert review'],
                'criteria': {}
            }
        }
        
        # Add parameter-specific QC
        for group in parameter_groups:
            if group == 'air_quality':
                qc_plan['field_qc']['calibration']['air_monitors'] = 'Monthly'
                qc_plan['laboratory_qc']['detection_limits']['pm10'] = '10 µg/m³'
            elif group == 'water_quality':
                qc_plan['field_qc']['calibration']['ph_meter'] = 'Daily'
                qc_plan['laboratory_qc']['preservation'] = 'As per EPA methods'
        
        return qc_plan
    
    def _get_season(self, date: datetime) -> str:
        """Get season for date (Northern Hemisphere)."""
        month = date.month
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Fall'
    
    def _check_statistical_validity(
        self,
        measurements: List[FieldMeasurement],
        parameter_group: str
    ) -> Dict[str, Any]:
        """Check statistical validity of dataset."""
        validity = {
            'sample_size_adequate': True,
            'temporal_coverage': True,
            'spatial_coverage': True,
            'data_distribution': {}
        }
        
        # Check sample sizes
        min_samples = {
            'air_quality': 8760,  # Hourly for 1 year
            'water_quality': 12,  # Monthly for 1 year
            'noise': 168,  # Hourly for 1 week
            'ecology': 4  # Seasonal
        }
        
        n_samples = len(measurements)
        min_required = min_samples.get(parameter_group, 10)
        
        if n_samples < min_required * 0.8:
            validity['sample_size_adequate'] = False
        
        return validity
    
    def _calculate_baseline_statistics(
        self,
        measurements: List[FieldMeasurement]
    ) -> Dict[str, Any]:
        """Calculate comprehensive baseline statistics."""
        if not measurements:
            return {}
        
        # Group by parameter
        param_groups = {}
        for m in measurements:
            if m.parameter not in param_groups:
                param_groups[m.parameter] = []
            param_groups[m.parameter].append(m.value)
        
        statistics = {}
        for param, values in param_groups.items():
            values_array = np.array(values)
            statistics[param] = {
                'n': len(values),
                'mean': np.mean(values_array),
                'std': np.std(values_array),
                'min': np.min(values_array),
                'max': np.max(values_array),
                'p25': np.percentile(values_array, 25),
                'p50': np.percentile(values_array, 50),
                'p75': np.percentile(values_array, 75),
                'p95': np.percentile(values_array, 95),
                'cv': np.std(values_array) / np.mean(values_array) if np.mean(values_array) > 0 else 0
            }
        
        return statistics