"""
Field Data Collection System
Mobile-friendly forms and data collection interface

Author: Edy Bassil
Email: bassileddy@gmail.com
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import json
import uuid
from enum import Enum
import base64
import hashlib

@dataclass
class FieldForm:
    """Digital field data collection form."""
    form_id: str
    form_type: str  # air, water, noise, ecology, soil
    version: str
    fields: List[Dict[str, Any]]
    validation_rules: Dict[str, Any]
    required_equipment: List[str]
    instructions: Dict[str, str]
    created_date: datetime
    created_by: str


@dataclass
class FieldSession:
    """Field data collection session."""
    session_id: str
    project_id: int
    form_id: str
    location_id: str
    operator_name: str
    operator_id: str
    start_time: datetime
    end_time: Optional[datetime]
    weather_conditions: Dict[str, Any]
    equipment_used: List[Dict[str, str]]
    photos: List[str]  # Base64 encoded
    measurements: List[Dict[str, Any]]
    qc_checks: Dict[str, bool]
    notes: str
    gps_track: List[Tuple[float, float, datetime]]
    status: str  # draft, completed, validated


class FieldDataCollector:
    """Manages field data collection with mobile-friendly interface."""
    
    def __init__(self):
        # Pre-built form templates
        self.form_templates = {
            'air_quality': self._create_air_quality_form(),
            'water_quality': self._create_water_quality_form(),
            'noise_monitoring': self._create_noise_form(),
            'ecological_survey': self._create_ecology_form(),
            'soil_sampling': self._create_soil_form(),
            'groundwater': self._create_groundwater_form(),
            'social_survey': self._create_social_form()
        }
        
        # Equipment calibration requirements
        self.calibration_requirements = {
            'ph_meter': {'frequency': 'daily', 'method': 'buffer_solutions'},
            'do_meter': {'frequency': 'daily', 'method': 'air_saturation'},
            'sound_level_meter': {'frequency': 'before_use', 'method': 'calibrator_94db'},
            'air_monitor': {'frequency': 'monthly', 'method': 'zero_span'},
            'gps': {'frequency': 'before_use', 'method': 'known_point'}
        }
    
    def _create_air_quality_form(self) -> FieldForm:
        """Create air quality monitoring form."""
        return FieldForm(
            form_id="AQ001",
            form_type="air_quality",
            version="2.0",
            fields=[
                {
                    'name': 'station_id',
                    'label': 'Monitoring Station ID',
                    'type': 'select',
                    'required': True,
                    'options': 'dynamic:stations'
                },
                {
                    'name': 'date',
                    'label': 'Date',
                    'type': 'date',
                    'required': True,
                    'default': 'today'
                },
                {
                    'name': 'time',
                    'label': 'Time',
                    'type': 'time',
                    'required': True,
                    'default': 'now'
                },
                {
                    'name': 'pm10',
                    'label': 'PM10 (µg/m³)',
                    'type': 'number',
                    'required': True,
                    'min': 0,
                    'max': 999,
                    'decimal': 1,
                    'unit': 'µg/m³'
                },
                {
                    'name': 'pm25',
                    'label': 'PM2.5 (µg/m³)',
                    'type': 'number',
                    'required': True,
                    'min': 0,
                    'max': 999,
                    'decimal': 1,
                    'unit': 'µg/m³'
                },
                {
                    'name': 'no2',
                    'label': 'NO₂ (µg/m³)',
                    'type': 'number',
                    'required': False,
                    'min': 0,
                    'max': 999,
                    'decimal': 1,
                    'unit': 'µg/m³'
                },
                {
                    'name': 'so2',
                    'label': 'SO₂ (µg/m³)',
                    'type': 'number',
                    'required': False,
                    'min': 0,
                    'max': 999,
                    'decimal': 1,
                    'unit': 'µg/m³'
                },
                {
                    'name': 'co',
                    'label': 'CO (mg/m³)',
                    'type': 'number',
                    'required': False,
                    'min': 0,
                    'max': 99,
                    'decimal': 1,
                    'unit': 'mg/m³'
                },
                {
                    'name': 'wind_speed',
                    'label': 'Wind Speed (m/s)',
                    'type': 'number',
                    'required': True,
                    'min': 0,
                    'max': 50,
                    'decimal': 1,
                    'unit': 'm/s'
                },
                {
                    'name': 'wind_direction',
                    'label': 'Wind Direction (degrees)',
                    'type': 'number',
                    'required': True,
                    'min': 0,
                    'max': 360,
                    'decimal': 0,
                    'unit': 'degrees'
                },
                {
                    'name': 'temperature',
                    'label': 'Temperature (°C)',
                    'type': 'number',
                    'required': True,
                    'min': -10,
                    'max': 60,
                    'decimal': 1,
                    'unit': '°C'
                },
                {
                    'name': 'humidity',
                    'label': 'Relative Humidity (%)',
                    'type': 'number',
                    'required': True,
                    'min': 0,
                    'max': 100,
                    'decimal': 0,
                    'unit': '%'
                },
                {
                    'name': 'pressure',
                    'label': 'Atmospheric Pressure (hPa)',
                    'type': 'number',
                    'required': False,
                    'min': 900,
                    'max': 1100,
                    'decimal': 1,
                    'unit': 'hPa'
                },
                {
                    'name': 'visibility',
                    'label': 'Visibility',
                    'type': 'select',
                    'required': True,
                    'options': ['Clear >10km', 'Good 5-10km', 'Moderate 2-5km', 'Poor 1-2km', 'Very Poor <1km']
                },
                {
                    'name': 'photos',
                    'label': 'Site Photos',
                    'type': 'photo',
                    'required': True,
                    'multiple': True,
                    'max_files': 5
                },
                {
                    'name': 'calibration_check',
                    'label': 'Equipment Calibrated?',
                    'type': 'checkbox',
                    'required': True
                },
                {
                    'name': 'notes',
                    'label': 'Field Notes',
                    'type': 'textarea',
                    'required': False,
                    'max_length': 500
                }
            ],
            validation_rules={
                'pm10_pm25_ratio': 'pm10 >= pm25',
                'wind_calm': 'if wind_speed < 0.5 then wind_direction = null',
                'photo_required': 'len(photos) >= 1'
            },
            required_equipment=[
                'PM Monitor (Beta Attenuation or equivalent)',
                'Gas Analyzers (if measuring gases)',
                'Weather Station',
                'Camera',
                'GPS Device'
            ],
            instructions={
                'setup': 'Set up monitoring equipment at least 30 minutes before measurements',
                'calibration': 'Perform zero/span check on all analyzers',
                'recording': 'Record 1-hour average values',
                'weather': 'Note any unusual weather conditions',
                'photos': 'Take photos of site in 4 cardinal directions'
            },
            created_date=datetime.now(),
            created_by='System'
        )
    
    def _create_water_quality_form(self) -> FieldForm:
        """Create water quality sampling form."""
        return FieldForm(
            form_id="WQ001",
            form_type="water_quality",
            version="2.0",
            fields=[
                {
                    'name': 'sample_id',
                    'label': 'Sample ID',
                    'type': 'text',
                    'required': True,
                    'pattern': 'WQ-[0-9]{6}',
                    'auto_generate': True
                },
                {
                    'name': 'location_id',
                    'label': 'Sampling Location',
                    'type': 'select',
                    'required': True,
                    'options': 'dynamic:water_locations'
                },
                {
                    'name': 'sample_type',
                    'label': 'Sample Type',
                    'type': 'select',
                    'required': True,
                    'options': ['Surface Water', 'Groundwater', 'Wastewater', 'Drinking Water', 'Marine']
                },
                {
                    'name': 'sample_depth',
                    'label': 'Sample Depth (m)',
                    'type': 'number',
                    'required': True,
                    'min': 0,
                    'max': 100,
                    'decimal': 1,
                    'unit': 'm'
                },
                {
                    'name': 'water_temp',
                    'label': 'Water Temperature (°C)',
                    'type': 'number',
                    'required': True,
                    'min': 0,
                    'max': 50,
                    'decimal': 1,
                    'unit': '°C',
                    'field_measurement': True
                },
                {
                    'name': 'ph',
                    'label': 'pH',
                    'type': 'number',
                    'required': True,
                    'min': 0,
                    'max': 14,
                    'decimal': 2,
                    'unit': 'pH units',
                    'field_measurement': True
                },
                {
                    'name': 'do',
                    'label': 'Dissolved Oxygen (mg/L)',
                    'type': 'number',
                    'required': True,
                    'min': 0,
                    'max': 20,
                    'decimal': 1,
                    'unit': 'mg/L',
                    'field_measurement': True
                },
                {
                    'name': 'conductivity',
                    'label': 'Conductivity (µS/cm)',
                    'type': 'number',
                    'required': True,
                    'min': 0,
                    'max': 99999,
                    'decimal': 0,
                    'unit': 'µS/cm',
                    'field_measurement': True
                },
                {
                    'name': 'turbidity',
                    'label': 'Turbidity (NTU)',
                    'type': 'number',
                    'required': True,
                    'min': 0,
                    'max': 9999,
                    'decimal': 1,
                    'unit': 'NTU',
                    'field_measurement': True
                },
                {
                    'name': 'appearance',
                    'label': 'Water Appearance',
                    'type': 'select',
                    'required': True,
                    'options': ['Clear', 'Slightly Turbid', 'Turbid', 'Very Turbid', 'Colored']
                },
                {
                    'name': 'odor',
                    'label': 'Odor',
                    'type': 'select',
                    'required': True,
                    'options': ['None', 'Slight', 'Moderate', 'Strong', 'Chemical', 'Sewage', 'Other']
                },
                {
                    'name': 'flow_condition',
                    'label': 'Flow Condition',
                    'type': 'select',
                    'required': False,
                    'options': ['Stagnant', 'Low Flow', 'Normal Flow', 'High Flow', 'Flooding']
                },
                {
                    'name': 'weather_24hr',
                    'label': 'Weather Last 24 Hours',
                    'type': 'select',
                    'required': True,
                    'options': ['Dry', 'Light Rain', 'Heavy Rain', 'Intermittent Rain']
                },
                {
                    'name': 'lab_parameters',
                    'label': 'Parameters for Lab Analysis',
                    'type': 'multiselect',
                    'required': True,
                    'options': ['BOD', 'COD', 'TSS', 'TDS', 'Nutrients', 'Heavy Metals', 
                               'Hydrocarbons', 'Pesticides', 'Bacteria']
                },
                {
                    'name': 'bottles_filled',
                    'label': 'Sample Bottles',
                    'type': 'checklist',
                    'required': True,
                    'options': [
                        {'id': 'plastic_1L', 'label': 'Plastic 1L (General)'},
                        {'id': 'glass_1L', 'label': 'Glass 1L (Organics)'},
                        {'id': 'plastic_250ml_preserved', 'label': 'Plastic 250ml (Metals, preserved)'},
                        {'id': 'sterile_100ml', 'label': 'Sterile 100ml (Bacteria)'}
                    ]
                },
                {
                    'name': 'preservation',
                    'label': 'Preservation Applied',
                    'type': 'checklist',
                    'required': True,
                    'options': [
                        {'id': 'ice', 'label': 'Cooled on Ice'},
                        {'id': 'hno3', 'label': 'HNO₃ for Metals'},
                        {'id': 'h2so4', 'label': 'H₂SO₄ for Nutrients'},
                        {'id': 'na2s2o3', 'label': 'Na₂S₂O₃ for Chlorine'}
                    ]
                },
                {
                    'name': 'photos',
                    'label': 'Sampling Photos',
                    'type': 'photo',
                    'required': True,
                    'multiple': True,
                    'instructions': 'Include upstream, downstream, and sampling point'
                },
                {
                    'name': 'chain_custody',
                    'label': 'Chain of Custody Number',
                    'type': 'text',
                    'required': True,
                    'auto_generate': True
                }
            ],
            validation_rules={
                'do_temperature': 'do < (14.6 - 0.4 * water_temp)',  # DO saturation check
                'preservation_metals': 'if "Heavy Metals" in lab_parameters then "hno3" in preservation',
                'bottle_check': 'bottles_filled matches lab_parameters'
            },
            required_equipment=[
                'Multi-parameter probe (calibrated)',
                'Sample bottles (appropriate types)',
                'Cooler with ice',
                'Preservation chemicals',
                'Labels and markers',
                'Chain of custody forms',
                'PPE (gloves, safety glasses)',
                'Bailer or sampling pole'
            ],
            instructions={
                'pre_sampling': 'Calibrate all meters before leaving office',
                'sampling': 'Rinse bottles 3x with sample water (except sterile)',
                'field_measurements': 'Allow probe to stabilize for 2 minutes',
                'preservation': 'Add preservatives immediately after collection',
                'transport': 'Keep samples at 4°C, deliver to lab within 24 hours'
            },
            created_date=datetime.now(),
            created_by='System'
        )
    
    def _create_noise_form(self) -> FieldForm:
        """Create noise monitoring form."""
        return FieldForm(
            form_id="NM001",
            form_type="noise_monitoring",
            version="2.0",
            fields=[
                {
                    'name': 'location_id',
                    'label': 'Monitoring Location',
                    'type': 'select',
                    'required': True,
                    'options': 'dynamic:noise_locations'
                },
                {
                    'name': 'measurement_type',
                    'label': 'Measurement Type',
                    'type': 'select',
                    'required': True,
                    'options': ['Baseline', 'Construction', 'Operational', 'Compliance']
                },
                {
                    'name': 'period',
                    'label': 'Measurement Period',
                    'type': 'select',
                    'required': True,
                    'options': ['Day (07:00-19:00)', 'Evening (19:00-23:00)', 'Night (23:00-07:00)', '24-Hour']
                },
                {
                    'name': 'start_time',
                    'label': 'Start Time',
                    'type': 'datetime',
                    'required': True
                },
                {
                    'name': 'duration_minutes',
                    'label': 'Duration (minutes)',
                    'type': 'select',
                    'required': True,
                    'options': ['15', '30', '60', '480', '1440'],
                    'default': '60'
                },
                {
                    'name': 'laeq',
                    'label': 'LAeq (dBA)',
                    'type': 'number',
                    'required': True,
                    'min': 20,
                    'max': 140,
                    'decimal': 1,
                    'unit': 'dBA'
                },
                {
                    'name': 'la90',
                    'label': 'LA90 (Background) (dBA)',
                    'type': 'number',
                    'required': True,
                    'min': 20,
                    'max': 140,
                    'decimal': 1,
                    'unit': 'dBA'
                },
                {
                    'name': 'la10',
                    'label': 'LA10 (dBA)',
                    'type': 'number',
                    'required': True,
                    'min': 20,
                    'max': 140,
                    'decimal': 1,
                    'unit': 'dBA'
                },
                {
                    'name': 'lamax',
                    'label': 'LAmax (dBA)',
                    'type': 'number',
                    'required': True,
                    'min': 20,
                    'max': 140,
                    'decimal': 1,
                    'unit': 'dBA'
                },
                {
                    'name': 'dominant_sources',
                    'label': 'Dominant Noise Sources',
                    'type': 'multiselect',
                    'required': True,
                    'options': ['Traffic', 'Construction', 'Industrial', 'Aircraft', 
                               'Birds/Insects', 'Wind', 'Human Activity', 'Other']
                },
                {
                    'name': 'weather_conditions',
                    'label': 'Weather Conditions',
                    'type': 'group',
                    'fields': [
                        {
                            'name': 'wind_speed',
                            'label': 'Wind Speed (m/s)',
                            'type': 'number',
                            'required': True,
                            'min': 0,
                            'max': 20,
                            'decimal': 1
                        },
                        {
                            'name': 'wind_direction',
                            'label': 'Wind Direction',
                            'type': 'select',
                            'required': True,
                            'options': ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
                        },
                        {
                            'name': 'temperature',
                            'label': 'Temperature (°C)',
                            'type': 'number',
                            'required': True,
                            'min': -10,
                            'max': 60,
                            'decimal': 1
                        },
                        {
                            'name': 'humidity',
                            'label': 'Humidity (%)',
                            'type': 'number',
                            'required': True,
                            'min': 0,
                            'max': 100,
                            'decimal': 0
                        },
                        {
                            'name': 'precipitation',
                            'label': 'Precipitation',
                            'type': 'select',
                            'required': True,
                            'options': ['None', 'Light Rain', 'Rain', 'Heavy Rain']
                        }
                    ]
                },
                {
                    'name': 'meter_settings',
                    'label': 'Sound Level Meter Settings',
                    'type': 'group',
                    'fields': [
                        {
                            'name': 'meter_model',
                            'label': 'Meter Model',
                            'type': 'text',
                            'required': True
                        },
                        {
                            'name': 'calibration_before',
                            'label': 'Calibration Before (dB)',
                            'type': 'number',
                            'required': True,
                            'default': 94.0,
                            'decimal': 1
                        },
                        {
                            'name': 'calibration_after',
                            'label': 'Calibration After (dB)',
                            'type': 'number',
                            'required': True,
                            'decimal': 1
                        },
                        {
                            'name': 'microphone_height',
                            'label': 'Microphone Height (m)',
                            'type': 'number',
                            'required': True,
                            'default': 1.5,
                            'decimal': 1
                        }
                    ]
                },
                {
                    'name': 'photos',
                    'label': 'Measurement Photos',
                    'type': 'photo',
                    'required': True,
                    'multiple': True,
                    'instructions': 'Include meter setup and surrounding area'
                },
                {
                    'name': 'audio_recording',
                    'label': 'Audio Sample',
                    'type': 'audio',
                    'required': False,
                    'max_duration': 60,
                    'instructions': 'Record 1-minute sample if unusual sounds'
                },
                {
                    'name': 'notes',
                    'label': 'Observations',
                    'type': 'textarea',
                    'required': False
                }
            ],
            validation_rules={
                'statistical_check': 'la90 <= laeq <= la10 <= lamax',
                'wind_limit': 'wind_speed <= 5',  # m/s limit for valid measurement
                'calibration_drift': 'abs(calibration_after - calibration_before) <= 0.5',
                'rain_check': 'precipitation == "None"'  # No measurement in rain
            },
            required_equipment=[
                'Type 1 Sound Level Meter (IEC 61672)',
                'Acoustic Calibrator (94 dB)',
                'Windscreen',
                'Tripod',
                'Weather meter',
                'Camera',
                'Data logging equipment'
            ],
            instructions={
                'setup': 'Set up meter 1.5m high, away from reflecting surfaces (>3.5m)',
                'calibration': 'Calibrate before AND after measurement',
                'weather': 'Do not measure if wind >5m/s or during precipitation',
                'documentation': 'Photo of setup from 4 directions',
                'data': 'Log data at minimum 1-second intervals'
            },
            created_date=datetime.now(),
            created_by='System'
        )
    
    def _create_ecology_form(self) -> FieldForm:
        """Create ecological survey form."""
        return FieldForm(
            form_id="ECO001",
            form_type="ecological_survey",
            version="2.0",
            fields=[
                {
                    'name': 'survey_type',
                    'label': 'Survey Type',
                    'type': 'select',
                    'required': True,
                    'options': ['Flora', 'Fauna', 'Habitat', 'Combined']
                },
                {
                    'name': 'survey_method',
                    'label': 'Survey Method',
                    'type': 'select',
                    'required': True,
                    'options': ['Quadrat', 'Transect', 'Point Count', 'Camera Trap', 
                               'Mist Net', 'Pitfall Trap', 'Visual Encounter']
                },
                {
                    'name': 'habitat_type',
                    'label': 'Habitat Type',
                    'type': 'select',
                    'required': True,
                    'options': ['Desert', 'Coastal', 'Mangrove', 'Sabkha', 'Rocky', 
                               'Agricultural', 'Urban', 'Wadi', 'Mountain']
                },
                {
                    'name': 'transect_info',
                    'label': 'Transect/Plot Information',
                    'type': 'group',
                    'show_if': 'survey_method in ["Quadrat", "Transect"]',
                    'fields': [
                        {
                            'name': 'transect_id',
                            'label': 'Transect/Plot ID',
                            'type': 'text',
                            'required': True
                        },
                        {
                            'name': 'start_gps',
                            'label': 'Start GPS',
                            'type': 'gps',
                            'required': True
                        },
                        {
                            'name': 'end_gps',
                            'label': 'End GPS',
                            'type': 'gps',
                            'required': True,
                            'show_if': 'survey_method == "Transect"'
                        },
                        {
                            'name': 'length_m',
                            'label': 'Length (m)',
                            'type': 'number',
                            'required': True,
                            'min': 1,
                            'max': 1000
                        }
                    ]
                },
                {
                    'name': 'species_records',
                    'label': 'Species Observations',
                    'type': 'repeating_group',
                    'required': True,
                    'fields': [
                        {
                            'name': 'species_name',
                            'label': 'Species Name',
                            'type': 'text',
                            'required': True,
                            'autocomplete': 'species_database'
                        },
                        {
                            'name': 'common_name',
                            'label': 'Common Name',
                            'type': 'text',
                            'required': False
                        },
                        {
                            'name': 'count',
                            'label': 'Count/Abundance',
                            'type': 'number',
                            'required': True,
                            'min': 0
                        },
                        {
                            'name': 'life_stage',
                            'label': 'Life Stage',
                            'type': 'select',
                            'required': False,
                            'options': ['Adult', 'Juvenile', 'Seedling', 'Egg', 'Larva', 'Mixed']
                        },
                        {
                            'name': 'behavior',
                            'label': 'Behavior/Activity',
                            'type': 'multiselect',
                            'required': False,
                            'options': ['Feeding', 'Resting', 'Breeding', 'Nesting', 
                                       'Flying', 'Calling', 'Territorial']
                        },
                        {
                            'name': 'photo',
                            'label': 'Species Photo',
                            'type': 'photo',
                            'required': False
                        },
                        {
                            'name': 'conservation_status',
                            'label': 'Conservation Status',
                            'type': 'select',
                            'required': False,
                            'options': ['Not Evaluated', 'Least Concern', 'Near Threatened', 
                                       'Vulnerable', 'Endangered', 'Critically Endangered']
                        }
                    ]
                },
                {
                    'name': 'vegetation_cover',
                    'label': 'Vegetation Cover (%)',
                    'type': 'number',
                    'required': True,
                    'min': 0,
                    'max': 100,
                    'show_if': 'survey_type in ["Flora", "Habitat", "Combined"]'
                },
                {
                    'name': 'canopy_height',
                    'label': 'Average Canopy Height (m)',
                    'type': 'number',
                    'required': False,
                    'min': 0,
                    'max': 50,
                    'decimal': 1,
                    'show_if': 'survey_type in ["Flora", "Habitat", "Combined"]'
                },
                {
                    'name': 'disturbance_signs',
                    'label': 'Signs of Disturbance',
                    'type': 'multiselect',
                    'required': True,
                    'options': ['None', 'Grazing', 'Vehicle Tracks', 'Litter', 'Fire', 
                               'Construction', 'Invasive Species', 'Erosion']
                },
                {
                    'name': 'habitat_quality',
                    'label': 'Habitat Quality',
                    'type': 'select',
                    'required': True,
                    'options': ['Pristine', 'Good', 'Moderate', 'Degraded', 'Severely Degraded']
                },
                {
                    'name': 'weather',
                    'label': 'Weather Conditions',
                    'type': 'select',
                    'required': True,
                    'options': ['Sunny', 'Partly Cloudy', 'Cloudy', 'Light Rain', 'Windy', 'Foggy']
                },
                {
                    'name': 'survey_effort',
                    'label': 'Survey Effort',
                    'type': 'group',
                    'fields': [
                        {
                            'name': 'start_time',
                            'label': 'Start Time',
                            'type': 'time',
                            'required': True
                        },
                        {
                            'name': 'end_time',
                            'label': 'End Time',
                            'type': 'time',
                            'required': True
                        },
                        {
                            'name': 'num_observers',
                            'label': 'Number of Observers',
                            'type': 'number',
                            'required': True,
                            'min': 1,
                            'max': 10
                        }
                    ]
                },
                {
                    'name': 'habitat_photos',
                    'label': 'Habitat Photos',
                    'type': 'photo',
                    'required': True,
                    'multiple': True,
                    'min_files': 4,
                    'instructions': 'North, South, East, West views'
                }
            ],
            validation_rules={
                'species_count': 'len(species_records) >= 1',
                'time_check': 'end_time > start_time',
                'cover_total': 'vegetation_cover <= 100'
            },
            required_equipment=[
                'GPS device',
                'Camera with macro lens',
                'Binoculars',
                'Field guides',
                'Measuring tape (50m)',
                'Quadrat frame (1m²)',
                'Data sheets',
                'Plant press (if collecting)',
                'Collection permits'
            ],
            instructions={
                'timing': 'Best survey times: Dawn (birds), Morning (reptiles), Dusk (mammals)',
                'approach': 'Walk slowly, stop frequently, scan all vegetation layers',
                'recording': 'Record all species seen/heard within survey area',
                'photography': 'Photograph unknown species for later identification',
                'permits': 'Ensure all necessary permits before collecting specimens'
            },
            created_date=datetime.now(),
            created_by='System'
        )
    
    def create_field_session(
        self,
        project_id: int,
        form_type: str,
        location_id: str,
        operator_name: str,
        operator_id: str
    ) -> FieldSession:
        """
        Create new field data collection session.
        
        Args:
            project_id: Project ID
            form_type: Type of form to use
            location_id: Sampling location ID
            operator_name: Field operator name
            operator_id: Operator ID
            
        Returns:
            New field session
        """
        if form_type not in self.form_templates:
            raise ValueError(f"Unknown form type: {form_type}")
        
        session = FieldSession(
            session_id=str(uuid.uuid4()),
            project_id=project_id,
            form_id=self.form_templates[form_type].form_id,
            location_id=location_id,
            operator_name=operator_name,
            operator_id=operator_id,
            start_time=datetime.now(),
            end_time=None,
            weather_conditions={},
            equipment_used=[],
            photos=[],
            measurements=[],
            qc_checks={},
            notes="",
            gps_track=[],
            status="draft"
        )
        
        return session
    
    def validate_field_data(
        self,
        session: FieldSession,
        form_type: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate field data against form rules.
        
        Args:
            session: Field session
            form_type: Form type
            data: Field data to validate
            
        Returns:
            Validation results
        """
        form = self.form_templates.get(form_type)
        if not form:
            return {'valid': False, 'errors': ['Invalid form type']}
        
        errors = []
        warnings = []
        
        # Check required fields
        for field in form.fields:
            if field.get('required') and field['name'] not in data:
                errors.append(f"Required field missing: {field['label']}")
        
        # Validate field values
        for field in form.fields:
            field_name = field['name']
            if field_name in data:
                value = data[field_name]
                
                # Type validation
                if field['type'] == 'number':
                    try:
                        num_value = float(value)
                        # Range validation
                        if 'min' in field and num_value < field['min']:
                            errors.append(f"{field['label']} below minimum: {field['min']}")
                        if 'max' in field and num_value > field['max']:
                            errors.append(f"{field['label']} above maximum: {field['max']}")
                    except:
                        errors.append(f"{field['label']} must be a number")
                
                elif field['type'] == 'select' and value not in field.get('options', []):
                    errors.append(f"Invalid option for {field['label']}: {value}")
        
        # Apply validation rules
        for rule_name, rule_expr in form.validation_rules.items():
            # Simple rule evaluation (in production, use safe expression parser)
            try:
                # This is simplified - implement proper expression evaluation
                if not self._evaluate_rule(rule_expr, data):
                    errors.append(f"Validation failed: {rule_name}")
            except:
                warnings.append(f"Could not evaluate rule: {rule_name}")
        
        # Check QC requirements
        if form_type == 'noise_monitoring':
            if 'calibration_before' in data and 'calibration_after' in data:
                drift = abs(float(data['calibration_after']) - float(data['calibration_before']))
                if drift > 0.5:
                    errors.append(f"Calibration drift too high: {drift:.1f} dB")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'completeness': self._calculate_completeness(data, form.fields)
        }
    
    def save_field_session(
        self,
        session: FieldSession,
        data: Dict[str, Any],
        photos: List[str],
        finalize: bool = False
    ) -> FieldSession:
        """
        Save field session data.
        
        Args:
            session: Field session
            data: Field measurements
            photos: Base64 encoded photos
            finalize: Whether to finalize session
            
        Returns:
            Updated session
        """
        # Add measurement data
        measurement = {
            'timestamp': datetime.now().isoformat(),
            'data': data,
            'data_hash': self._calculate_data_hash(data)
        }
        session.measurements.append(measurement)
        
        # Add photos
        for photo in photos:
            session.photos.append({
                'photo_id': str(uuid.uuid4()),
                'timestamp': datetime.now().isoformat(),
                'data': photo,  # Base64 encoded
                'location': data.get('gps_location')
            })
        
        # Update weather if provided
        if 'weather_conditions' in data:
            session.weather_conditions = data['weather_conditions']
        
        # Update status
        if finalize:
            session.end_time = datetime.now()
            session.status = 'completed'
            
            # Calculate QC checks
            session.qc_checks = {
                'data_complete': self._check_data_completeness(session),
                'photos_taken': len(session.photos) > 0,
                'duration_valid': (session.end_time - session.start_time).seconds > 300,
                'gps_recorded': len(session.gps_track) > 0
            }
        
        return session
    
    def generate_field_report(
        self,
        sessions: List[FieldSession],
        output_format: str = 'pdf'
    ) -> bytes:
        """
        Generate field data collection report.
        
        Args:
            sessions: List of field sessions
            output_format: Output format (pdf, excel)
            
        Returns:
            Report file bytes
        """
        # Group sessions by type
        sessions_by_type = {}
        for session in sessions:
            form_type = self._get_form_type_from_id(session.form_id)
            if form_type not in sessions_by_type:
                sessions_by_type[form_type] = []
            sessions_by_type[form_type].append(session)
        
        # Create report structure
        report_data = {
            'title': 'Field Data Collection Report',
            'generated_date': datetime.now(),
            'total_sessions': len(sessions),
            'data_by_type': {}
        }
        
        # Summarize data by type
        for form_type, type_sessions in sessions_by_type.items():
            summary = {
                'session_count': len(type_sessions),
                'locations': list(set(s.location_id for s in type_sessions)),
                'operators': list(set(s.operator_name for s in type_sessions)),
                'date_range': {
                    'start': min(s.start_time for s in type_sessions),
                    'end': max(s.end_time or s.start_time for s in type_sessions)
                },
                'measurements': [],
                'qc_summary': self._summarize_qc_checks(type_sessions)
            }
            
            # Extract measurements
            for session in type_sessions:
                for measurement in session.measurements:
                    summary['measurements'].append({
                        'session_id': session.session_id,
                        'location': session.location_id,
                        'timestamp': measurement['timestamp'],
                        'data': measurement['data']
                    })
            
            report_data['data_by_type'][form_type] = summary
        
        # Generate output
        if output_format == 'pdf':
            # Use ReportLab to generate PDF
            # This is simplified - integrate with report_service.py
            return b"PDF report content"
        else:
            # Generate Excel
            import pandas as pd
            import io
            
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                # Summary sheet
                summary_df = pd.DataFrame([{
                    'Form Type': ft,
                    'Sessions': data['session_count'],
                    'Locations': len(data['locations']),
                    'Start Date': data['date_range']['start'],
                    'End Date': data['date_range']['end']
                } for ft, data in report_data['data_by_type'].items()])
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                # Data sheets by type
                for form_type, data in report_data['data_by_type'].items():
                    if data['measurements']:
                        # Flatten measurement data
                        rows = []
                        for m in data['measurements']:
                            row = {
                                'Session ID': m['session_id'],
                                'Location': m['location'],
                                'Timestamp': m['timestamp']
                            }
                            row.update(m['data'])
                            rows.append(row)
                        
                        df = pd.DataFrame(rows)
                        sheet_name = form_type.replace('_', ' ').title()[:31]  # Excel limit
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            buffer.seek(0)
            return buffer.getvalue()
    
    def _evaluate_rule(self, rule: str, data: Dict[str, Any]) -> bool:
        """Evaluate validation rule (simplified)."""
        # In production, use a safe expression parser
        # This is a basic implementation
        if 'pm10 >= pm25' in rule:
            return float(data.get('pm10', 0)) >= float(data.get('pm25', 0))
        return True
    
    def _calculate_completeness(self, data: Dict[str, Any], fields: List[Dict]) -> float:
        """Calculate data completeness percentage."""
        required_fields = [f['name'] for f in fields if f.get('required')]
        if not required_fields:
            return 100.0
        
        filled = sum(1 for f in required_fields if f in data and data[f])
        return (filled / len(required_fields)) * 100
    
    def _calculate_data_hash(self, data: Dict[str, Any]) -> str:
        """Calculate hash of data for integrity checking."""
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()[:16]
    
    def _get_form_type_from_id(self, form_id: str) -> str:
        """Get form type from form ID."""
        for form_type, form in self.form_templates.items():
            if form.form_id == form_id:
                return form_type
        return 'unknown'
    
    def _check_data_completeness(self, session: FieldSession) -> bool:
        """Check if session data is complete."""
        if not session.measurements:
            return False
        
        # Get form to check required fields
        form_type = self._get_form_type_from_id(session.form_id)
        form = self.form_templates.get(form_type)
        
        if not form:
            return False
        
        # Check last measurement
        if session.measurements:
            last_data = session.measurements[-1]['data']
            validation = self.validate_field_data(session, form_type, last_data)
            return validation['valid']
        
        return False
    
    def _summarize_qc_checks(self, sessions: List[FieldSession]) -> Dict[str, Any]:
        """Summarize QC checks across sessions."""
        total = len(sessions)
        if total == 0:
            return {}
        
        qc_summary = {
            'data_complete': sum(1 for s in sessions if s.qc_checks.get('data_complete', False)) / total * 100,
            'photos_taken': sum(1 for s in sessions if s.qc_checks.get('photos_taken', False)) / total * 100,
            'duration_valid': sum(1 for s in sessions if s.qc_checks.get('duration_valid', False)) / total * 100,
            'overall_pass_rate': sum(1 for s in sessions if all(s.qc_checks.values())) / total * 100
        }
        
        return qc_summary
    
    def _create_soil_form(self) -> FieldForm:
        """Create soil sampling form."""
        # Similar structure to other forms
        # Implementation abbreviated for space
        return FieldForm(
            form_id="SS001",
            form_type="soil_sampling",
            version="2.0",
            fields=[
                {'name': 'sample_id', 'label': 'Sample ID', 'type': 'text', 'required': True},
                {'name': 'depth_cm', 'label': 'Depth (cm)', 'type': 'number', 'required': True},
                {'name': 'soil_type', 'label': 'Soil Type', 'type': 'select', 
                 'options': ['Sand', 'Silt', 'Clay', 'Loam', 'Rocky'], 'required': True},
                # Additional fields...
            ],
            validation_rules={},
            required_equipment=['Soil auger', 'Sample bags', 'Labels'],
            instructions={'sampling': 'Collect from multiple points'},
            created_date=datetime.now(),
            created_by='System'
        )
    
    def _create_groundwater_form(self) -> FieldForm:
        """Create groundwater monitoring form."""
        # Implementation abbreviated
        return self._create_water_quality_form()  # Similar to water quality
    
    def _create_social_form(self) -> FieldForm:
        """Create social survey form."""
        return FieldForm(
            form_id="SOC001",
            form_type="social_survey",
            version="2.0",
            fields=[
                {'name': 'household_id', 'label': 'Household ID', 'type': 'text', 'required': True},
                {'name': 'respondent_age', 'label': 'Age Group', 'type': 'select',
                 'options': ['18-25', '26-40', '41-60', '60+'], 'required': True},
                {'name': 'occupation', 'label': 'Occupation', 'type': 'text', 'required': True},
                # Additional demographic and impact questions...
            ],
            validation_rules={},
            required_equipment=['Tablet/Phone', 'Consent forms'],
            instructions={'approach': 'Introduce yourself and explain purpose'},
            created_date=datetime.now(),
            created_by='System'
        )