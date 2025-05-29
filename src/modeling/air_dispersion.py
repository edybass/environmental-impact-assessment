"""
Air Quality Dispersion Modeling
Simplified Gaussian plume model for air pollutant dispersion

Author: Edy Bassil
Email: bassileddy@gmail.com
"""

from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import numpy as np
from math import exp, sqrt, pi, erf
import pandas as pd
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class EmissionSource:
    """Air pollutant emission source."""
    source_id: str
    source_type: str  # point, area, line, volume
    location: Tuple[float, float]  # (lat, lon)
    height: float  # meters
    diameter: float  # meters (for stacks)
    temperature: float  # K
    velocity: float  # m/s
    emission_rates: Dict[str, float]  # pollutant: g/s


@dataclass
class MetConditions:
    """Meteorological conditions."""
    wind_speed: float  # m/s
    wind_direction: float  # degrees from north
    temperature: float  # °C
    pressure: float  # hPa
    humidity: float  # %
    stability_class: str  # A-F (Pasquill)
    mixing_height: float  # meters
    cloud_cover: float  # fraction


@dataclass
class Receptor:
    """Receptor location for concentration calculation."""
    receptor_id: str
    location: Tuple[float, float]  # (lat, lon)
    height: float  # meters above ground
    receptor_type: str  # residential, school, etc.


class AirDispersionModel:
    """Simplified air dispersion model based on Gaussian plume."""
    
    def __init__(self):
        # Pasquill-Gifford dispersion parameters
        # Rural conditions (UAE/KSA are mostly open terrain)
        self.pg_params = {
            # Stability class: (ay, by, az, bz)
            'A': (0.22, 0.894, 0.20, 0.894),    # Very unstable
            'B': (0.16, 0.894, 0.12, 0.894),    # Unstable
            'C': (0.11, 0.894, 0.08, 0.894),    # Slightly unstable
            'D': (0.08, 0.894, 0.06, 0.894),    # Neutral
            'E': (0.06, 0.894, 0.03, 0.9),      # Slightly stable
            'F': (0.04, 0.894, 0.016, 0.9)      # Stable
        }
        
        # Minimum wind speed (m/s) to prevent division by zero
        self.min_wind_speed = 0.5
        
        # UAE/KSA specific parameters
        self.surface_roughness = 0.01  # Desert terrain (m)
        self.default_mixing_height = {
            'day': 2000,    # Daytime mixing height (m)
            'night': 300    # Nighttime mixing height (m)
        }
        
        # Air quality standards (µg/m³)
        self.standards = {
            'pm10': {'24hr': 150, 'annual': 50},
            'pm25': {'24hr': 65, 'annual': 15},
            'no2': {'1hr': 200, 'annual': 40},
            'so2': {'24hr': 125, 'annual': 60},
            'co': {'8hr': 10000}
        }
    
    def calculate_concentration(
        self,
        source: EmissionSource,
        receptor: Receptor,
        met_conditions: MetConditions,
        pollutant: str
    ) -> float:
        """
        Calculate pollutant concentration at receptor.
        
        Args:
            source: Emission source
            receptor: Receptor location
            met_conditions: Meteorological conditions
            pollutant: Pollutant name
            
        Returns:
            Concentration in µg/m³
        """
        # Get emission rate
        Q = source.emission_rates.get(pollutant, 0)
        if Q == 0:
            return 0
        
        # Calculate distance and direction
        distance, direction = self._calculate_distance_direction(
            source.location, receptor.location
        )
        
        if distance < 1:  # Too close
            distance = 1
        
        # Check if receptor is downwind
        wind_angle = met_conditions.wind_direction
        angle_diff = abs(direction - wind_angle)
        if angle_diff > 180:
            angle_diff = 360 - angle_diff
        
        # Outside 45° cone of influence
        if angle_diff > 45:
            return 0
        
        # Adjust wind speed
        u = max(met_conditions.wind_speed, self.min_wind_speed)
        
        # Get dispersion parameters
        sigma_y, sigma_z = self._calculate_dispersion_coefficients(
            distance, met_conditions.stability_class
        )
        
        # Calculate effective stack height (with plume rise)
        H = self._calculate_effective_height(source, met_conditions)
        
        # Gaussian plume equation
        # Ground-level concentration
        C = (Q / (2 * pi * u * sigma_y * sigma_z)) * \
            exp(-0.5 * ((receptor.height - H) / sigma_z) ** 2) * \
            (exp(-0.5 * ((0) / sigma_y) ** 2))  # Centerline concentration
        
        # Add ground reflection
        C += (Q / (2 * pi * u * sigma_y * sigma_z)) * \
             exp(-0.5 * ((receptor.height + H) / sigma_z) ** 2) * \
             (exp(-0.5 * ((0) / sigma_y) ** 2))
        
        # Account for crosswind distribution
        crosswind_factor = exp(-0.5 * (angle_diff / 22.5) ** 2)
        C *= crosswind_factor
        
        # Convert g/s to µg/m³
        C *= 1e6
        
        # Apply mixing height limitation
        if H > met_conditions.mixing_height * 0.8:
            C *= exp(-(H - 0.8 * met_conditions.mixing_height) / met_conditions.mixing_height)
        
        return C
    
    def calculate_concentration_grid(
        self,
        sources: List[EmissionSource],
        grid_specs: Dict[str, Any],
        met_conditions: MetConditions,
        pollutant: str
    ) -> pd.DataFrame:
        """
        Calculate concentrations over a grid.
        
        Args:
            sources: List of emission sources
            grid_specs: Grid specifications (bounds, resolution)
            met_conditions: Meteorological conditions
            pollutant: Pollutant to model
            
        Returns:
            DataFrame with grid concentrations
        """
        # Create grid
        lat_min = grid_specs['lat_min']
        lat_max = grid_specs['lat_max']
        lon_min = grid_specs['lon_min']
        lon_max = grid_specs['lon_max']
        resolution = grid_specs.get('resolution', 100)  # meters
        
        # Convert resolution to degrees (approximate)
        lat_step = resolution / 111000
        lon_step = resolution / (111000 * np.cos(np.radians((lat_min + lat_max) / 2)))
        
        # Create grid points
        lats = np.arange(lat_min, lat_max, lat_step)
        lons = np.arange(lon_min, lon_max, lon_step)
        
        # Calculate concentrations
        results = []
        
        for lat in lats:
            for lon in lons:
                receptor = Receptor(
                    receptor_id=f"grid_{lat:.6f}_{lon:.6f}",
                    location=(lat, lon),
                    height=1.5,  # Breathing height
                    receptor_type="grid"
                )
                
                # Sum contributions from all sources
                total_conc = 0
                for source in sources:
                    conc = self.calculate_concentration(
                        source, receptor, met_conditions, pollutant
                    )
                    total_conc += conc
                
                results.append({
                    'lat': lat,
                    'lon': lon,
                    'concentration': total_conc,
                    'exceeds_24hr': total_conc > self.standards.get(pollutant, {}).get('24hr', float('inf'))
                })
        
        return pd.DataFrame(results)
    
    def calculate_annual_average(
        self,
        source: EmissionSource,
        receptor: Receptor,
        met_data: pd.DataFrame,
        pollutant: str
    ) -> float:
        """
        Calculate annual average concentration.
        
        Args:
            source: Emission source
            receptor: Receptor location
            met_data: Annual hourly meteorological data
            pollutant: Pollutant name
            
        Returns:
            Annual average concentration
        """
        concentrations = []
        
        # Sample met data if too large (use every nth hour)
        if len(met_data) > 8760:
            met_data = met_data.iloc[::int(len(met_data) / 8760)]
        
        for _, row in met_data.iterrows():
            met = MetConditions(
                wind_speed=row['wind_speed'],
                wind_direction=row['wind_direction'],
                temperature=row['temperature'],
                pressure=row.get('pressure', 1013),
                humidity=row.get('humidity', 50),
                stability_class=self._determine_stability_class(row),
                mixing_height=row.get('mixing_height', 1000),
                cloud_cover=row.get('cloud_cover', 0.5)
            )
            
            conc = self.calculate_concentration(source, receptor, met, pollutant)
            concentrations.append(conc)
        
        return np.mean(concentrations)
    
    def calculate_percentiles(
        self,
        source: EmissionSource,
        receptor: Receptor,
        met_data: pd.DataFrame,
        pollutant: str,
        percentiles: List[float] = [50, 90, 95, 98, 99]
    ) -> Dict[float, float]:
        """
        Calculate concentration percentiles.
        
        Args:
            source: Emission source
            receptor: Receptor location
            met_data: Meteorological data
            pollutant: Pollutant name
            percentiles: Percentiles to calculate
            
        Returns:
            Dictionary of percentile values
        """
        concentrations = []
        
        for _, row in met_data.iterrows():
            met = MetConditions(
                wind_speed=row['wind_speed'],
                wind_direction=row['wind_direction'],
                temperature=row['temperature'],
                pressure=row.get('pressure', 1013),
                humidity=row.get('humidity', 50),
                stability_class=self._determine_stability_class(row),
                mixing_height=row.get('mixing_height', 1000),
                cloud_cover=row.get('cloud_cover', 0.5)
            )
            
            conc = self.calculate_concentration(source, receptor, met, pollutant)
            concentrations.append(conc)
        
        return {
            p: np.percentile(concentrations, p) 
            for p in percentiles
        }
    
    def _calculate_distance_direction(
        self,
        source_loc: Tuple[float, float],
        receptor_loc: Tuple[float, float]
    ) -> Tuple[float, float]:
        """Calculate distance and direction between points."""
        lat1, lon1 = source_loc
        lat2, lon2 = receptor_loc
        
        # Haversine distance
        R = 6371000  # Earth radius in meters
        phi1 = np.radians(lat1)
        phi2 = np.radians(lat2)
        dphi = np.radians(lat2 - lat1)
        dlambda = np.radians(lon2 - lon1)
        
        a = np.sin(dphi/2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlambda/2)**2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
        distance = R * c
        
        # Direction (bearing)
        y = np.sin(dlambda) * np.cos(phi2)
        x = np.cos(phi1) * np.sin(phi2) - np.sin(phi1) * np.cos(phi2) * np.cos(dlambda)
        bearing = np.degrees(np.arctan2(y, x))
        bearing = (bearing + 360) % 360
        
        return distance, bearing
    
    def _calculate_dispersion_coefficients(
        self,
        distance: float,
        stability_class: str
    ) -> Tuple[float, float]:
        """Calculate Pasquill-Gifford dispersion coefficients."""
        params = self.pg_params.get(stability_class, self.pg_params['D'])
        ay, by, az, bz = params
        
        # Convert distance to km for P-G curves
        x_km = distance / 1000
        
        # Rural P-G formulas
        sigma_y = ay * x_km ** by * 1000  # Convert back to meters
        sigma_z = az * x_km ** bz * 1000
        
        # Limit sigma_z to mixing height
        max_sigma_z = 0.8 * self.default_mixing_height['day']
        sigma_z = min(sigma_z, max_sigma_z)
        
        return sigma_y, sigma_z
    
    def _calculate_effective_height(
        self,
        source: EmissionSource,
        met_conditions: MetConditions
    ) -> float:
        """Calculate effective stack height including plume rise."""
        # Holland's formula for plume rise
        u = max(met_conditions.wind_speed, self.min_wind_speed)
        
        # Stack parameters
        Vs = source.velocity  # m/s
        Ds = source.diameter  # m
        Ts = source.temperature  # K
        Ta = met_conditions.temperature + 273.15  # K
        
        # Buoyancy flux
        g = 9.81  # m/s²
        Fb = g * Vs * Ds**2 * (Ts - Ta) / (4 * Ts)
        
        # Momentum flux
        Fm = Vs**2 * Ds**2 * Ta / (4 * Ts)
        
        # Holland formula
        if Fb > 0:  # Buoyant plume
            dH = 1.5 * (Fb / u)**0.33 * (source.height)**(2/3)
        else:  # Momentum dominated
            dH = 3 * Ds * Vs / u
        
        # Limit plume rise
        max_rise = 3 * source.height
        dH = min(dH, max_rise)
        
        return source.height + dH
    
    def _determine_stability_class(self, met_row: pd.Series) -> str:
        """Determine Pasquill stability class from meteorological data."""
        wind_speed = met_row['wind_speed']
        
        # Simplified determination based on wind speed and time
        # In practice, would use solar radiation and cloud cover
        hour = met_row.get('hour', 12)
        
        if 10 <= hour <= 16:  # Daytime
            if wind_speed < 2:
                return 'A'  # Very unstable
            elif wind_speed < 3:
                return 'B'  # Unstable
            elif wind_speed < 5:
                return 'C'  # Slightly unstable
            else:
                return 'D'  # Neutral
        else:  # Nighttime
            if wind_speed < 2:
                return 'F'  # Stable
            elif wind_speed < 3:
                return 'E'  # Slightly stable
            else:
                return 'D'  # Neutral
    
    def create_emission_sources_from_project(
        self,
        project_data: Dict[str, Any]
    ) -> List[EmissionSource]:
        """
        Create emission sources from project data.
        
        Args:
            project_data: Project information
            
        Returns:
            List of emission sources
        """
        sources = []
        
        # Construction equipment sources
        if 'equipment' in project_data:
            for equip in project_data['equipment']:
                # Emission factors (g/hr)
                emission_factors = {
                    'excavator': {'pm10': 0.5, 'pm25': 0.3, 'no2': 2.0, 'co': 5.0},
                    'bulldozer': {'pm10': 0.7, 'pm25': 0.4, 'no2': 2.5, 'co': 6.0},
                    'crane': {'pm10': 0.3, 'pm25': 0.2, 'no2': 1.5, 'co': 3.0},
                    'generator': {'pm10': 0.2, 'pm25': 0.1, 'no2': 3.0, 'so2': 0.5},
                    'truck': {'pm10': 0.4, 'pm25': 0.2, 'no2': 1.8, 'co': 4.0}
                }
                
                factors = emission_factors.get(equip['type'], emission_factors['truck'])
                
                # Convert to g/s
                emission_rates = {
                    poll: rate * equip.get('hours_per_day', 8) / 3600
                    for poll, rate in factors.items()
                }
                
                source = EmissionSource(
                    source_id=f"equip_{equip['id']}",
                    source_type='point',
                    location=equip.get('location', project_data['center']),
                    height=3.0,  # Equipment exhaust height
                    diameter=0.1,
                    temperature=400,  # Exhaust temp (K)
                    velocity=10,  # Exhaust velocity
                    emission_rates=emission_rates
                )
                sources.append(source)
        
        # Dust sources (area sources)
        if 'construction_area' in project_data:
            area = project_data['construction_area']  # m²
            
            # AP-42 emission factors for construction
            # PM10: 0.11 kg/hectare/day
            pm10_rate = 0.11 * (area / 10000) / 86400  # g/s
            pm25_rate = pm10_rate * 0.15  # PM2.5 is ~15% of PM10
            
            dust_source = EmissionSource(
                source_id="dust_area",
                source_type='area',
                location=project_data['center'],
                height=0.5,  # Near ground
                diameter=sqrt(area / pi),  # Equivalent diameter
                temperature=300,  # Ambient
                velocity=0.1,
                emission_rates={'pm10': pm10_rate, 'pm25': pm25_rate}
            )
            sources.append(dust_source)
        
        # Stack sources (if any)
        if 'stacks' in project_data:
            for stack in project_data['stacks']:
                source = EmissionSource(
                    source_id=f"stack_{stack['id']}",
                    source_type='point',
                    location=stack['location'],
                    height=stack['height'],
                    diameter=stack['diameter'],
                    temperature=stack.get('temperature', 400),
                    velocity=stack.get('velocity', 15),
                    emission_rates=stack['emission_rates']
                )
                sources.append(source)
        
        return sources
    
    def generate_met_data(
        self,
        location: str,
        year: int = 2023
    ) -> pd.DataFrame:
        """
        Generate representative meteorological data for location.
        
        Args:
            location: Location name (Dubai, Riyadh, etc.)
            year: Year for data
            
        Returns:
            DataFrame with hourly met data
        """
        # Representative met patterns for UAE/KSA cities
        met_patterns = {
            'Dubai': {
                'wind_speed_mean': 3.5,
                'wind_speed_std': 1.5,
                'prevailing_direction': 315,  # NW
                'temp_summer': 40,
                'temp_winter': 20,
                'mixing_height_day': 2000,
                'mixing_height_night': 300
            },
            'Riyadh': {
                'wind_speed_mean': 4.0,
                'wind_speed_std': 2.0,
                'prevailing_direction': 180,  # S
                'temp_summer': 42,
                'temp_winter': 15,
                'mixing_height_day': 2500,
                'mixing_height_night': 200
            },
            'Jeddah': {
                'wind_speed_mean': 3.0,
                'wind_speed_std': 1.0,
                'prevailing_direction': 270,  # W
                'temp_summer': 38,
                'temp_winter': 22,
                'mixing_height_day': 1500,
                'mixing_height_night': 400
            }
        }
        
        pattern = met_patterns.get(location, met_patterns['Dubai'])
        
        # Generate hourly data
        hours = pd.date_range(start=f'{year}-01-01', end=f'{year}-12-31 23:00', freq='H')
        
        met_data = pd.DataFrame({
            'datetime': hours,
            'hour': hours.hour,
            'month': hours.month,
            'wind_speed': np.random.normal(
                pattern['wind_speed_mean'],
                pattern['wind_speed_std'],
                len(hours)
            ),
            'wind_direction': np.random.normal(
                pattern['prevailing_direction'],
                30,  # Standard deviation
                len(hours)
            ) % 360,
            'temperature': pattern['temp_winter'] + 
                          (pattern['temp_summer'] - pattern['temp_winter']) * 
                          np.sin((hours.dayofyear - 80) * 2 * pi / 365) ** 2 +
                          np.random.normal(0, 3, len(hours)),
            'pressure': np.random.normal(1013, 5, len(hours)),
            'humidity': 50 - 20 * np.sin((hours.dayofyear - 80) * 2 * pi / 365) +
                       np.random.normal(0, 10, len(hours)),
            'mixing_height': np.where(
                (hours.hour >= 10) & (hours.hour <= 16),
                pattern['mixing_height_day'],
                pattern['mixing_height_night']
            )
        })
        
        # Ensure positive values
        met_data['wind_speed'] = met_data['wind_speed'].clip(lower=0.5)
        met_data['temperature'] = met_data['temperature'].clip(lower=10, upper=50)
        met_data['humidity'] = met_data['humidity'].clip(lower=10, upper=90)
        
        return met_data
    
    def create_impact_report(
        self,
        results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create air quality impact assessment report.
        
        Args:
            results: Modeling results
            
        Returns:
            Report dictionary
        """
        report = {
            'summary': {
                'model': 'Gaussian Plume (Simplified AERMOD)',
                'pollutants_modeled': list(results.get('pollutants', [])),
                'number_of_sources': results.get('source_count', 0),
                'number_of_receptors': results.get('receptor_count', 0),
                'modeling_domain': results.get('domain', {}),
                'meteorological_data': results.get('met_summary', {})
            },
            'maximum_impacts': {},
            'compliance_assessment': {},
            'mitigation_recommendations': []
        }
        
        # Analyze maximum impacts
        for pollutant, data in results.get('concentrations', {}).items():
            max_conc = data.get('maximum', 0)
            max_location = data.get('max_location', {})
            
            # Compare with standards
            standards = self.standards.get(pollutant, {})
            
            report['maximum_impacts'][pollutant] = {
                'maximum_concentration': max_conc,
                'location': max_location,
                'percentage_of_standard': {}
            }
            
            for period, standard in standards.items():
                percentage = (max_conc / standard) * 100
                report['maximum_impacts'][pollutant]['percentage_of_standard'][period] = percentage
                
                # Compliance assessment
                if percentage > 100:
                    report['compliance_assessment'][f'{pollutant}_{period}'] = {
                        'compliant': False,
                        'exceedance': percentage - 100,
                        'action_required': True
                    }
                else:
                    report['compliance_assessment'][f'{pollutant}_{period}'] = {
                        'compliant': True,
                        'margin': 100 - percentage,
                        'action_required': False
                    }
        
        # Generate mitigation recommendations
        if any(not v['compliant'] for v in report['compliance_assessment'].values()):
            report['mitigation_recommendations'].extend([
                'Implement dust suppression measures (water spraying, chemical suppressants)',
                'Limit equipment operating hours during high-wind conditions',
                'Use Tier 4 or electric equipment where possible',
                'Install particulate filters on diesel equipment',
                'Establish buffer zones around sensitive receptors',
                'Implement real-time air quality monitoring'
            ])
        
        return report