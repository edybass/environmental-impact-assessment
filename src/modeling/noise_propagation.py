"""
Noise Propagation Modeling
ISO 9613-based outdoor sound propagation model

Author: Edy Bassil
Email: bassileddy@gmail.com
"""

from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import numpy as np
from math import log10, sqrt, atan2, degrees
import pandas as pd
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class NoiseSource:
    """Noise source definition."""
    source_id: str
    source_type: str  # point, line, area
    location: Tuple[float, float]  # (lat, lon)
    height: float  # meters above ground
    sound_power_level: float  # dB re 1pW (Lw)
    directivity: Optional[Dict[float, float]] = None  # angle: correction
    operating_hours: Dict[str, Tuple[int, int]] = None  # period: (start, end)
    frequency_spectrum: Optional[Dict[int, float]] = None  # Hz: dB
    source_dimensions: Optional[Dict[str, float]] = None  # for area/line sources


@dataclass
class NoiseBarrier:
    """Noise barrier or building."""
    barrier_id: str
    start_point: Tuple[float, float]
    end_point: Tuple[float, float]
    height: float  # meters
    transmission_loss: float  # dB


@dataclass
class GroundType:
    """Ground absorption characteristics."""
    ground_type: str  # hard, porous, mixed
    flow_resistivity: float  # kPa.s/m²
    porosity: float  # 0-1


class NoisePropagationModel:
    """ISO 9613-2 compliant outdoor noise propagation model."""
    
    def __init__(self):
        # ISO 9613-2 parameters
        self.reference_conditions = {
            'temperature': 10,  # °C
            'humidity': 70,     # %
            'pressure': 101.325  # kPa
        }
        
        # Octave band center frequencies
        self.octave_bands = [63, 125, 250, 500, 1000, 2000, 4000, 8000]
        
        # A-weighting corrections
        self.a_weighting = {
            63: -26.2,
            125: -16.1,
            250: -8.6,
            500: -3.2,
            1000: 0,
            2000: 1.2,
            4000: 1.0,
            8000: -1.1
        }
        
        # Ground types
        self.ground_types = {
            'hard': {'G': 0, 'description': 'Paving, water, concrete'},
            'porous': {'G': 1, 'description': 'Grass, trees, vegetation'},
            'mixed': {'G': 0.5, 'description': 'Mixed hard and soft'},
            'sand': {'G': 0.7, 'description': 'Desert sand'},
            'very_soft': {'G': 1, 'description': 'Snow, moss'}
        }
        
        # Construction equipment noise levels (Lw in dB)
        self.equipment_noise_levels = {
            'excavator': {'Lw': 105, 'spectrum': 'broadband'},
            'bulldozer': {'Lw': 108, 'spectrum': 'low_frequency'},
            'jackhammer': {'Lw': 110, 'spectrum': 'impact'},
            'crane': {'Lw': 96, 'spectrum': 'broadband'},
            'concrete_mixer': {'Lw': 90, 'spectrum': 'broadband'},
            'pile_driver': {'Lw': 115, 'spectrum': 'impact'},
            'compressor': {'Lw': 98, 'spectrum': 'tonal'},
            'generator': {'Lw': 95, 'spectrum': 'tonal'},
            'truck': {'Lw': 88, 'spectrum': 'low_frequency'},
            'concrete_pump': {'Lw': 106, 'spectrum': 'broadband'}
        }
        
        # Noise limits (LAeq in dBA)
        self.noise_limits = {
            'UAE': {
                'residential': {'day': 55, 'evening': 50, 'night': 45},
                'commercial': {'day': 65, 'evening': 60, 'night': 55},
                'industrial': {'day': 70, 'evening': 70, 'night': 70}
            },
            'KSA': {
                'residential': {'day': 55, 'evening': 50, 'night': 45},
                'commercial': {'day': 60, 'evening': 55, 'night': 50},
                'industrial': {'day': 70, 'evening': 65, 'night': 60}
            }
        }
    
    def calculate_noise_level(
        self,
        source: NoiseSource,
        receiver: Tuple[float, float, float],  # (lat, lon, height)
        met_conditions: Dict[str, float],
        ground_type: str = 'mixed',
        barriers: Optional[List[NoiseBarrier]] = None
    ) -> Dict[str, float]:
        """
        Calculate noise level at receiver location.
        
        Args:
            source: Noise source
            receiver: Receiver location (lat, lon, height)
            met_conditions: Meteorological conditions
            ground_type: Ground type between source and receiver
            barriers: List of barriers
            
        Returns:
            Dictionary with octave band and overall A-weighted levels
        """
        # Calculate distance
        distance = self._calculate_distance_3d(
            (source.location[0], source.location[1], source.height),
            receiver
        )
        
        if distance < 1:
            distance = 1  # Minimum distance
        
        # Get source spectrum
        if source.frequency_spectrum:
            Lw_spectrum = source.frequency_spectrum
        else:
            Lw_spectrum = self._estimate_spectrum(source.sound_power_level, source.source_type)
        
        # Calculate for each octave band
        results = {}
        
        for freq in self.octave_bands:
            Lw = Lw_spectrum.get(freq, source.sound_power_level - 3)
            
            # ISO 9613-2 attenuation terms
            Adiv = self._attenuation_divergence(distance, source.source_type)
            Aatm = self._attenuation_atmospheric(distance, freq, met_conditions)
            Agr = self._attenuation_ground(source.height, receiver[2], distance, freq, ground_type)
            Abar = 0
            
            if barriers:
                Abar = self._attenuation_barrier(source, receiver, barriers, freq)
            
            Amisc = self._attenuation_miscellaneous(distance, met_conditions)
            
            # Calculate sound pressure level
            Lp = Lw - Adiv - Aatm - Agr - Abar - Amisc
            
            results[f'{freq}Hz'] = round(Lp, 1)
        
        # Calculate A-weighted overall level
        Lp_A_total = self._calculate_overall_a_weighted(results)
        results['LAeq'] = round(Lp_A_total, 1)
        
        return results
    
    def calculate_noise_contours(
        self,
        sources: List[NoiseSource],
        area_bounds: Dict[str, float],
        contour_levels: List[float],
        resolution: float = 10,  # meters
        met_conditions: Optional[Dict[str, float]] = None
    ) -> Dict[float, List[Tuple[float, float]]]:
        """
        Calculate noise contours for multiple sources.
        
        Args:
            sources: List of noise sources
            area_bounds: Area boundaries (lat_min, lat_max, lon_min, lon_max)
            contour_levels: Noise levels for contours (dBA)
            resolution: Grid resolution in meters
            met_conditions: Meteorological conditions
            
        Returns:
            Dictionary of contour level: list of (lat, lon) points
        """
        if not met_conditions:
            met_conditions = {
                'temperature': 30,
                'humidity': 50,
                'wind_speed': 3,
                'wind_direction': 0
            }
        
        # Create grid
        lat_min = area_bounds['lat_min']
        lat_max = area_bounds['lat_max']
        lon_min = area_bounds['lon_min']
        lon_max = area_bounds['lon_max']
        
        # Convert resolution to degrees
        lat_step = resolution / 111000
        lon_step = resolution / (111000 * np.cos(np.radians((lat_min + lat_max) / 2)))
        
        lats = np.arange(lat_min, lat_max, lat_step)
        lons = np.arange(lon_min, lon_max, lon_step)
        
        # Calculate noise levels at grid points
        noise_grid = np.zeros((len(lats), len(lons)))
        
        for i, lat in enumerate(lats):
            for j, lon in enumerate(lons):
                receiver = (lat, lon, 1.5)  # 1.5m receiver height
                
                # Sum contributions from all sources
                total_level = 0
                
                for source in sources:
                    levels = self.calculate_noise_level(
                        source, receiver, met_conditions, 'mixed'
                    )
                    # Convert to linear scale, sum, and back to dB
                    total_level += 10 ** (levels['LAeq'] / 10)
                
                noise_grid[i, j] = 10 * log10(total_level) if total_level > 0 else 0
        
        # Extract contours
        contours = {}
        
        for level in contour_levels:
            contour_points = []
            
            # Simple contour extraction (in practice, use matplotlib.contour)
            for i in range(len(lats) - 1):
                for j in range(len(lons) - 1):
                    # Check if contour passes through cell
                    cell_values = [
                        noise_grid[i, j],
                        noise_grid[i+1, j],
                        noise_grid[i+1, j+1],
                        noise_grid[i, j+1]
                    ]
                    
                    if min(cell_values) <= level <= max(cell_values):
                        # Interpolate position (simplified)
                        lat_interp = lats[i] + lat_step * 0.5
                        lon_interp = lons[j] + lon_step * 0.5
                        contour_points.append((lat_interp, lon_interp))
            
            contours[level] = contour_points
        
        return contours
    
    def predict_construction_noise(
        self,
        equipment_list: List[Dict[str, Any]],
        receivers: List[Dict[str, Any]],
        working_hours: Dict[str, Tuple[int, int]],
        project_duration_days: int
    ) -> pd.DataFrame:
        """
        Predict construction noise at sensitive receivers.
        
        Args:
            equipment_list: List of construction equipment
            receivers: List of sensitive receiver locations
            working_hours: Working hours by period
            project_duration_days: Project duration
            
        Returns:
            DataFrame with noise predictions
        """
        results = []
        
        for receiver in receivers:
            receiver_loc = (receiver['lat'], receiver['lon'], receiver.get('height', 1.5))
            
            for period, hours in working_hours.items():
                # Create noise sources from equipment
                sources = []
                
                for equip in equipment_list:
                    if period == 'night' and not equip.get('night_work', False):
                        continue
                    
                    # Get equipment noise level
                    equip_type = equip['type']
                    noise_data = self.equipment_noise_levels.get(
                        equip_type,
                        {'Lw': 100, 'spectrum': 'broadband'}
                    )
                    
                    # Apply usage factor
                    usage_factor = equip.get('usage_factor', 0.5)
                    Lw_adjusted = noise_data['Lw'] + 10 * log10(usage_factor)
                    
                    source = NoiseSource(
                        source_id=f"{equip_type}_{equip.get('id', 1)}",
                        source_type='point',
                        location=(equip['lat'], equip['lon']),
                        height=equip.get('height', 2),
                        sound_power_level=Lw_adjusted
                    )
                    sources.append(source)
                
                # Calculate combined noise level
                if sources:
                    total_level = 0
                    
                    for source in sources:
                        levels = self.calculate_noise_level(
                            source,
                            receiver_loc,
                            {'temperature': 30, 'humidity': 50},
                            'mixed'
                        )
                        total_level += 10 ** (levels['LAeq'] / 10)
                    
                    LAeq = 10 * log10(total_level) if total_level > 0 else 0
                else:
                    LAeq = 0
                
                # Get applicable limit
                location = receiver.get('location', 'UAE')
                zone_type = receiver.get('zone_type', 'residential')
                limit = self.noise_limits.get(location, self.noise_limits['UAE']).get(
                    zone_type, {'day': 55}
                ).get(period, 55)
                
                results.append({
                    'receiver_id': receiver['id'],
                    'receiver_name': receiver['name'],
                    'period': period,
                    'predicted_level': round(LAeq, 1),
                    'limit': limit,
                    'exceedance': round(LAeq - limit, 1),
                    'compliant': LAeq <= limit,
                    'mitigation_required': LAeq > limit
                })
        
        return pd.DataFrame(results)
    
    def recommend_mitigation_measures(
        self,
        predictions: pd.DataFrame,
        budget_level: str = 'medium'
    ) -> List[Dict[str, Any]]:
        """
        Recommend noise mitigation measures.
        
        Args:
            predictions: Noise prediction results
            budget_level: Budget constraint level
            
        Returns:
            List of mitigation recommendations
        """
        recommendations = []
        
        # Get maximum exceedance
        max_exceedance = predictions['exceedance'].max()
        
        if max_exceedance <= 0:
            return [{
                'measure': 'No mitigation required',
                'description': 'Predicted levels comply with limits',
                'cost': 0,
                'effectiveness': 0
            }]
        
        # Mitigation options based on exceedance level
        if max_exceedance <= 5:
            # Minor exceedance
            recommendations.extend([
                {
                    'measure': 'Equipment maintenance',
                    'description': 'Regular maintenance to reduce noise emissions',
                    'cost': 'low',
                    'effectiveness': '2-3 dB reduction',
                    'implementation': 'immediate'
                },
                {
                    'measure': 'Operational restrictions',
                    'description': 'Limit noisy activities during sensitive hours',
                    'cost': 'low',
                    'effectiveness': '3-5 dB reduction',
                    'implementation': 'immediate'
                }
            ])
        
        elif max_exceedance <= 10:
            # Moderate exceedance
            recommendations.extend([
                {
                    'measure': 'Temporary noise barriers',
                    'description': '3-4m high barriers around noisy equipment',
                    'cost': 'medium',
                    'effectiveness': '5-10 dB reduction',
                    'implementation': '1-2 weeks'
                },
                {
                    'measure': 'Equipment silencers',
                    'description': 'Install mufflers and silencers on equipment',
                    'cost': 'medium',
                    'effectiveness': '5-8 dB reduction',
                    'implementation': '1 week'
                },
                {
                    'measure': 'Alternative equipment',
                    'description': 'Use quieter equipment models where available',
                    'cost': 'medium-high',
                    'effectiveness': '5-10 dB reduction',
                    'implementation': '2-4 weeks'
                }
            ])
        
        else:
            # Major exceedance
            recommendations.extend([
                {
                    'measure': 'Acoustic enclosures',
                    'description': 'Full or partial enclosures for stationary equipment',
                    'cost': 'high',
                    'effectiveness': '10-20 dB reduction',
                    'implementation': '2-4 weeks'
                },
                {
                    'measure': 'Permanent noise walls',
                    'description': 'Engineered noise barriers with absorptive treatment',
                    'cost': 'high',
                    'effectiveness': '10-15 dB reduction',
                    'implementation': '4-6 weeks'
                },
                {
                    'measure': 'Relocation of activities',
                    'description': 'Move noisy operations away from receivers',
                    'cost': 'variable',
                    'effectiveness': '10+ dB reduction',
                    'implementation': 'requires planning'
                },
                {
                    'measure': 'Alternative construction methods',
                    'description': 'Use quieter construction techniques',
                    'cost': 'high',
                    'effectiveness': '10-15 dB reduction',
                    'implementation': 'requires redesign'
                }
            ])
        
        # Filter by budget
        if budget_level == 'low':
            recommendations = [r for r in recommendations if r['cost'] in ['low', 'medium']]
        elif budget_level == 'medium':
            recommendations = [r for r in recommendations if r['cost'] != 'high']
        
        # Add monitoring recommendation
        recommendations.append({
            'measure': 'Noise monitoring program',
            'description': 'Continuous monitoring to verify compliance',
            'cost': 'medium',
            'effectiveness': 'verification tool',
            'implementation': 'immediate'
        })
        
        return recommendations
    
    def _calculate_distance_3d(
        self,
        point1: Tuple[float, float, float],
        point2: Tuple[float, float, float]
    ) -> float:
        """Calculate 3D distance between points."""
        lat1, lon1, h1 = point1
        lat2, lon2, h2 = point2
        
        # Horizontal distance (Haversine)
        R = 6371000  # Earth radius in meters
        phi1 = np.radians(lat1)
        phi2 = np.radians(lat2)
        dphi = np.radians(lat2 - lat1)
        dlambda = np.radians(lon2 - lon1)
        
        a = np.sin(dphi/2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlambda/2)**2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
        horizontal_distance = R * c
        
        # 3D distance
        vertical_distance = abs(h2 - h1)
        distance = sqrt(horizontal_distance**2 + vertical_distance**2)
        
        return distance
    
    def _attenuation_divergence(self, distance: float, source_type: str) -> float:
        """Calculate geometric divergence attenuation."""
        if source_type == 'point':
            # Point source
            return 20 * log10(distance) + 11
        elif source_type == 'line':
            # Line source (e.g., road)
            return 10 * log10(distance) + 8
        else:
            # Area source
            if distance < 10:
                return 0
            else:
                return 20 * log10(distance) - 10
    
    def _attenuation_atmospheric(
        self,
        distance: float,
        frequency: int,
        met_conditions: Dict[str, float]
    ) -> float:
        """Calculate atmospheric absorption (ISO 9613-1)."""
        T = met_conditions.get('temperature', 20)
        RH = met_conditions.get('humidity', 70)
        
        # Simplified atmospheric absorption coefficients (dB/km)
        # More accurate calculation would use ISO 9613-1 formulas
        alpha_table = {
            63: 0.1,
            125: 0.4,
            250: 1.0,
            500: 1.9,
            1000: 3.7,
            2000: 9.7,
            4000: 32.8,
            8000: 117.0
        }
        
        # Temperature and humidity corrections (simplified)
        temp_factor = 1 + 0.01 * (T - 20)
        humidity_factor = 1 - 0.01 * (RH - 70)
        
        alpha = alpha_table.get(frequency, 5.0) * temp_factor * humidity_factor
        
        return alpha * distance / 1000
    
    def _attenuation_ground(
        self,
        source_height: float,
        receiver_height: float,
        distance: float,
        frequency: int,
        ground_type: str
    ) -> float:
        """Calculate ground attenuation (ISO 9613-2)."""
        G = self.ground_types.get(ground_type, self.ground_types['mixed'])['G']
        
        # Mean height
        hm = (source_height + receiver_height) / 2
        
        # Ground attenuation regions (ISO 9613-2)
        if distance <= 30 * hm:
            # Source region
            As = -1.5 + G * 2.8 * (1 - distance / (30 * hm))
        else:
            As = -1.5
        
        # Middle region
        Am = -3 * (1 - G)
        
        # Receiver region
        Ar = As  # Symmetrical
        
        # Frequency weighting
        freq_factor = {
            63: 1.5,
            125: 1.5,
            250: 1.5,
            500: 1.5,
            1000: 1.0,
            2000: 0.5,
            4000: 0,
            8000: 0
        }.get(frequency, 1.0)
        
        Agr = (As + Am + Ar) * freq_factor
        
        return max(0, Agr)
    
    def _attenuation_barrier(
        self,
        source: NoiseSource,
        receiver: Tuple[float, float, float],
        barriers: List[NoiseBarrier],
        frequency: int
    ) -> float:
        """Calculate barrier attenuation."""
        # Simplified barrier calculation
        # Full implementation would use path difference method
        
        max_attenuation = 0
        
        for barrier in barriers:
            # Check if barrier is between source and receiver
            # Simplified - assumes barrier blocks if in general area
            
            # Path difference calculation (simplified)
            z = 5  # Simplified path difference
            
            # Barrier attenuation (Maekawa)
            if z > 0:
                Abar = 10 * log10(3 + 20 * z)
                max_attenuation = max(max_attenuation, Abar)
        
        # Frequency correction
        freq_factor = min(1, frequency / 500)
        
        return min(20, max_attenuation * freq_factor)
    
    def _attenuation_miscellaneous(
        self,
        distance: float,
        met_conditions: Dict[str, float]
    ) -> float:
        """Calculate miscellaneous attenuation (vegetation, buildings, etc.)."""
        # Simplified - would include vegetation, industrial sites, etc.
        
        # Vegetation (if present)
        vegetation_attenuation = 0
        if distance > 100:
            vegetation_attenuation = min(10, distance / 100)
        
        # Meteorological correction (simplified)
        wind_speed = met_conditions.get('wind_speed', 0)
        met_correction = 0
        if wind_speed > 5:
            met_correction = -2  # Downwind enhancement
        
        return vegetation_attenuation + met_correction
    
    def _estimate_spectrum(self, overall_level: float, source_type: str) -> Dict[int, float]:
        """Estimate frequency spectrum from overall level."""
        # Standard spectra for different source types
        spectra = {
            'broadband': {
                63: -8, 125: -4, 250: -1, 500: 0,
                1000: 0, 2000: -1, 4000: -4, 8000: -8
            },
            'low_frequency': {
                63: 0, 125: 0, 250: -2, 500: -4,
                1000: -8, 2000: -12, 4000: -16, 8000: -20
            },
            'impact': {
                63: -4, 125: -2, 250: 0, 500: 0,
                1000: -2, 2000: -4, 4000: -8, 8000: -12
            },
            'tonal': {
                63: -10, 125: -8, 250: -4, 500: 0,
                1000: 0, 2000: -4, 4000: -10, 8000: -15
            }
        }
        
        spectrum_corrections = spectra.get(source_type, spectra['broadband'])
        
        spectrum = {}
        for freq, correction in spectrum_corrections.items():
            spectrum[freq] = overall_level + correction
        
        return spectrum
    
    def _calculate_overall_a_weighted(self, octave_levels: Dict[str, float]) -> float:
        """Calculate overall A-weighted level from octave bands."""
        total = 0
        
        for freq in self.octave_bands:
            key = f'{freq}Hz'
            if key in octave_levels:
                Lp = octave_levels[key]
                A_weight = self.a_weighting[freq]
                LpA = Lp + A_weight
                total += 10 ** (LpA / 10)
        
        return 10 * log10(total) if total > 0 else 0
    
    def create_noise_sources_from_project(
        self,
        project_data: Dict[str, Any]
    ) -> List[NoiseSource]:
        """Create noise sources from project data."""
        sources = []
        
        # Construction equipment
        if 'equipment' in project_data:
            for equip in project_data['equipment']:
                noise_data = self.equipment_noise_levels.get(
                    equip['type'],
                    {'Lw': 100, 'spectrum': 'broadband'}
                )
                
                # Apply modifiers
                Lw = noise_data['Lw']
                
                # Multiple units
                if equip.get('quantity', 1) > 1:
                    Lw += 10 * log10(equip['quantity'])
                
                # Usage factor
                usage = equip.get('usage_factor', 0.5)
                Lw += 10 * log10(usage)
                
                source = NoiseSource(
                    source_id=f"equip_{equip['id']}",
                    source_type='point',
                    location=equip.get('location', project_data['center']),
                    height=equip.get('height', 2),
                    sound_power_level=Lw,
                    operating_hours=equip.get('operating_hours', {
                        'day': (7, 19),
                        'evening': (19, 23),
                        'night': None
                    })
                )
                sources.append(source)
        
        # Fixed installations
        if 'installations' in project_data:
            for install in project_data['installations']:
                source = NoiseSource(
                    source_id=f"install_{install['id']}",
                    source_type=install.get('type', 'point'),
                    location=install['location'],
                    height=install.get('height', 3),
                    sound_power_level=install.get('Lw', 95),
                    frequency_spectrum=install.get('spectrum')
                )
                sources.append(source)
        
        # Traffic noise (if applicable)
        if 'traffic' in project_data:
            for route in project_data['traffic']:
                # Line source for roads
                Lw_per_meter = 80 + 10 * log10(route.get('vehicles_per_hour', 100))
                
                source = NoiseSource(
                    source_id=f"traffic_{route['id']}",
                    source_type='line',
                    location=route['center'],  # Simplified
                    height=0.5,
                    sound_power_level=Lw_per_meter,
                    source_dimensions={'length': route.get('length', 100)}
                )
                sources.append(source)
        
        return sources
    
    def generate_noise_report(
        self,
        predictions: pd.DataFrame,
        project_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate noise impact assessment report."""
        report = {
            'project': project_info,
            'assessment_summary': {
                'model_used': 'ISO 9613-2 Outdoor Sound Propagation',
                'standards_applied': 'UAE/KSA Environmental Noise Limits',
                'assessment_date': datetime.now().isoformat()
            },
            'results_summary': {
                'total_receivers': len(predictions['receiver_id'].unique()),
                'compliant_receivers': len(predictions[predictions['compliant']]),
                'non_compliant_receivers': len(predictions[~predictions['compliant']]),
                'max_exceedance': predictions['exceedance'].max(),
                'affected_periods': predictions[~predictions['compliant']]['period'].unique().tolist()
            },
            'detailed_results': predictions.to_dict('records'),
            'mitigation_required': predictions['exceedance'].max() > 0,
            'conclusions': [],
            'recommendations': []
        }
        
        # Generate conclusions
        if report['results_summary']['non_compliant_receivers'] == 0:
            report['conclusions'].append(
                "All sensitive receivers comply with applicable noise limits"
            )
        else:
            report['conclusions'].append(
                f"{report['results_summary']['non_compliant_receivers']} receivers "
                f"exceed noise limits by up to {report['results_summary']['max_exceedance']:.1f} dB"
            )
            
            if 'night' in report['results_summary']['affected_periods']:
                report['conclusions'].append(
                    "Night-time noise limits are exceeded, requiring restrictions on night work"
                )
        
        # Generate recommendations
        if report['mitigation_required']:
            recommendations = self.recommend_mitigation_measures(predictions)
            report['recommendations'] = recommendations
        else:
            report['recommendations'].append({
                'measure': 'Good construction practices',
                'description': 'Maintain equipment and follow noise control procedures',
                'cost': 'low',
                'effectiveness': 'maintains compliance'
            })
        
        return report