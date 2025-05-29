"""
GIS Engine for Environmental Assessment
Web-based spatial analysis without expensive GIS software

Author: Edy Bassil
Email: bassileddy@gmail.com
"""

from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field
import json
import numpy as np
from shapely.geometry import Point, Polygon, LineString, MultiPolygon
from shapely.ops import transform, unary_union
import pyproj
import folium
from folium import plugins
import geopandas as gpd
import rasterio
from rasterio.transform import from_bounds
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import io
import base64
from datetime import datetime
import requests
from math import radians, cos, sin, asin, sqrt, atan2, degrees
import logging

logger = logging.getLogger(__name__)


@dataclass
class SensitiveReceptor:
    """Sensitive environmental receptor."""
    receptor_id: str
    name: str
    receptor_type: str  # residential, school, hospital, mosque, park, etc.
    latitude: float
    longitude: float
    population: Optional[int] = None
    sensitivity_level: str = "Medium"  # Low, Medium, High, Critical
    operating_hours: Optional[str] = None
    contact_info: Optional[Dict[str, str]] = None
    photos: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProjectBoundary:
    """Project area boundary."""
    boundary_id: str
    project_id: int
    boundary_type: str  # project_area, construction_zone, buffer_zone
    geometry: Union[Polygon, MultiPolygon]
    area_hectares: float
    perimeter_km: float
    centroid: Point
    created_date: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ImpactContour:
    """Environmental impact contour."""
    contour_id: str
    impact_type: str  # noise, air_quality, visual, vibration
    parameter: str  # specific parameter (e.g., PM10, LAeq)
    contour_levels: List[float]
    geometry: List[Polygon]  # One polygon per contour level
    unit: str
    model_used: str
    created_date: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)


class GISEngine:
    """GIS engine for spatial environmental analysis."""
    
    def __init__(self):
        # Common sensitive receptor types in UAE/KSA
        self.receptor_types = {
            'residential': {'sensitivity': 'High', 'icon': 'home', 'color': 'blue'},
            'school': {'sensitivity': 'Critical', 'icon': 'graduation-cap', 'color': 'red'},
            'hospital': {'sensitivity': 'Critical', 'icon': 'hospital', 'color': 'red'},
            'mosque': {'sensitivity': 'High', 'icon': 'place-of-worship', 'color': 'purple'},
            'park': {'sensitivity': 'Medium', 'icon': 'tree', 'color': 'green'},
            'hotel': {'sensitivity': 'Medium', 'icon': 'bed', 'color': 'orange'},
            'office': {'sensitivity': 'Low', 'icon': 'building', 'color': 'gray'},
            'industrial': {'sensitivity': 'Low', 'icon': 'industry', 'color': 'black'},
            'agricultural': {'sensitivity': 'Medium', 'icon': 'tractor', 'color': 'brown'},
            'archaeological': {'sensitivity': 'Critical', 'icon': 'monument', 'color': 'gold'},
            'wetland': {'sensitivity': 'Critical', 'icon': 'water', 'color': 'cyan'},
            'protected_area': {'sensitivity': 'Critical', 'icon': 'shield', 'color': 'darkgreen'}
        }
        
        # Standard buffer distances (meters)
        self.buffer_distances = {
            'construction_noise': [50, 100, 200, 500, 1000],
            'air_quality': [100, 250, 500, 1000, 2000],
            'vibration': [25, 50, 100, 200],
            'visual': [250, 500, 1000, 2000],
            'traffic': [50, 100, 250, 500],
            'ecological': [100, 250, 500, 1000]
        }
        
        # Initialize coordinate transformer (WGS84 to UTM)
        self.wgs84 = pyproj.CRS('EPSG:4326')
        # UTM zones: UAE (Zone 40N), Western KSA (Zone 37N), Eastern KSA (Zone 38N)
        self.utm_zones = {
            'UAE': pyproj.CRS('EPSG:32640'),
            'KSA_West': pyproj.CRS('EPSG:32637'),
            'KSA_East': pyproj.CRS('EPSG:32638')
        }
    
    def identify_sensitive_receptors(
        self,
        center_point: Tuple[float, float],
        search_radius_km: float = 5.0,
        receptor_types: Optional[List[str]] = None,
        data_source: str = "osm"  # OpenStreetMap
    ) -> List[SensitiveReceptor]:
        """
        Identify sensitive receptors around project location.
        
        Args:
            center_point: (latitude, longitude) of project center
            search_radius_km: Search radius in kilometers
            receptor_types: Types of receptors to search for
            data_source: Data source (osm, google, manual)
            
        Returns:
            List of identified sensitive receptors
        """
        receptors = []
        
        if data_source == "osm":
            # Query OpenStreetMap Overpass API
            receptors.extend(self._query_osm_receptors(
                center_point, 
                search_radius_km,
                receptor_types
            ))
        elif data_source == "manual":
            # Return empty list for manual input
            pass
        
        # Calculate distances and assign IDs
        for i, receptor in enumerate(receptors):
            receptor.receptor_id = f"SR_{i+1:04d}"
            # Calculate distance from project center
            distance = self._calculate_distance(
                center_point[0], center_point[1],
                receptor.latitude, receptor.longitude
            )
            receptor.metadata['distance_km'] = distance
        
        # Sort by distance
        receptors.sort(key=lambda r: r.metadata['distance_km'])
        
        return receptors
    
    def create_project_boundary(
        self,
        project_id: int,
        boundary_points: List[Tuple[float, float]],
        boundary_type: str = "project_area"
    ) -> ProjectBoundary:
        """
        Create project boundary from coordinates.
        
        Args:
            project_id: Project ID
            boundary_points: List of (lat, lon) tuples
            boundary_type: Type of boundary
            
        Returns:
            Project boundary object
        """
        # Create polygon from points
        if len(boundary_points) < 3:
            raise ValueError("At least 3 points required for boundary")
        
        # Ensure polygon is closed
        if boundary_points[0] != boundary_points[-1]:
            boundary_points.append(boundary_points[0])
        
        # Create shapely polygon
        polygon = Polygon([(lon, lat) for lat, lon in boundary_points])
        
        # Calculate area and perimeter in projected coordinates
        utm_crs = self._get_utm_crs(boundary_points[0])
        transformer = pyproj.Transformer.from_crs(self.wgs84, utm_crs, always_xy=True)
        
        polygon_utm = transform(transformer.transform, polygon)
        area_m2 = polygon_utm.area
        perimeter_m = polygon_utm.length
        
        # Get centroid
        centroid = polygon.centroid
        
        boundary = ProjectBoundary(
            boundary_id=f"BOUND_{project_id}_{boundary_type}",
            project_id=project_id,
            boundary_type=boundary_type,
            geometry=polygon,
            area_hectares=area_m2 / 10000,
            perimeter_km=perimeter_m / 1000,
            centroid=Point(centroid.x, centroid.y),
            created_date=datetime.now(),
            metadata={
                'coordinate_count': len(boundary_points),
                'is_valid': polygon.is_valid
            }
        )
        
        return boundary
    
    def create_buffer_zones(
        self,
        source_geometry: Union[Point, LineString, Polygon],
        impact_type: str,
        custom_distances: Optional[List[float]] = None
    ) -> List[Polygon]:
        """
        Create buffer zones around source.
        
        Args:
            source_geometry: Source geometry to buffer
            impact_type: Type of impact for buffer distances
            custom_distances: Custom buffer distances in meters
            
        Returns:
            List of buffer polygons
        """
        # Get buffer distances
        distances = custom_distances or self.buffer_distances.get(
            impact_type, 
            [50, 100, 250, 500, 1000]
        )
        
        # Get appropriate UTM projection
        if hasattr(source_geometry, 'centroid'):
            center = source_geometry.centroid
        else:
            center = source_geometry
        
        utm_crs = self._get_utm_crs((center.y, center.x))
        
        # Transform to UTM for accurate buffering
        transformer_to_utm = pyproj.Transformer.from_crs(
            self.wgs84, utm_crs, always_xy=True
        )
        transformer_to_wgs = pyproj.Transformer.from_crs(
            utm_crs, self.wgs84, always_xy=True
        )
        
        source_utm = transform(transformer_to_utm.transform, source_geometry)
        
        # Create buffers
        buffers = []
        for distance in distances:
            buffer_utm = source_utm.buffer(distance)
            buffer_wgs = transform(transformer_to_wgs.transform, buffer_utm)
            buffers.append(buffer_wgs)
        
        return buffers
    
    def calculate_affected_receptors(
        self,
        impact_zones: List[Polygon],
        receptors: List[SensitiveReceptor],
        impact_levels: List[str]
    ) -> Dict[str, List[SensitiveReceptor]]:
        """
        Calculate which receptors fall within impact zones.
        
        Args:
            impact_zones: List of impact zone polygons
            receptors: List of sensitive receptors
            impact_levels: Impact level for each zone
            
        Returns:
            Dictionary of affected receptors by impact level
        """
        affected = {level: [] for level in impact_levels}
        
        # Check each receptor
        for receptor in receptors:
            receptor_point = Point(receptor.longitude, receptor.latitude)
            
            # Find which zone it falls in (innermost)
            for i, (zone, level) in enumerate(zip(impact_zones, impact_levels)):
                if zone.contains(receptor_point):
                    affected[level].append(receptor)
                    receptor.metadata['impact_level'] = level
                    receptor.metadata['impact_zone'] = i
                    break
        
        return affected
    
    def generate_impact_contours(
        self,
        source_point: Tuple[float, float],
        impact_type: str,
        impact_model: str,
        parameters: Dict[str, Any]
    ) -> ImpactContour:
        """
        Generate impact contours using simplified models.
        
        Args:
            source_point: (lat, lon) of impact source
            impact_type: Type of impact (noise, air_quality)
            impact_model: Model to use
            parameters: Model parameters
            
        Returns:
            Impact contour object
        """
        contours = []
        
        if impact_type == "noise" and impact_model == "simple_distance":
            # Simple distance-based noise attenuation
            source_level = parameters.get('source_level', 85)  # dBA
            background = parameters.get('background', 45)  # dBA
            
            # Calculate distances for different noise levels
            levels = [65, 60, 55, 50, 45]  # dBA
            
            for level in levels:
                if level > background:
                    # Simple geometric spreading: L2 = L1 - 20*log10(r2/r1)
                    # Solving for r2: r2 = r1 * 10^((L1-L2)/20)
                    r1 = parameters.get('reference_distance', 10)  # meters
                    distance = r1 * (10 ** ((source_level - level) / 20))
                    
                    # Create circular contour
                    contour = Point(source_point[1], source_point[0]).buffer(
                        distance / 111000  # Convert meters to degrees (approximate)
                    )
                    contours.append(contour)
        
        elif impact_type == "air_quality" and impact_model == "gaussian_plume":
            # Simplified Gaussian plume model
            emission_rate = parameters.get('emission_rate', 1.0)  # g/s
            wind_speed = parameters.get('wind_speed', 3.0)  # m/s
            stack_height = parameters.get('stack_height', 10)  # m
            
            # Calculate ground-level concentrations
            levels = [100, 50, 25, 10, 5]  # µg/m³
            
            for level in levels:
                # Simplified calculation
                distance = self._calculate_plume_distance(
                    emission_rate, wind_speed, stack_height, level
                )
                
                # Create elliptical contour aligned with wind
                wind_direction = parameters.get('wind_direction', 0)
                contour = self._create_elliptical_contour(
                    source_point, distance, distance * 0.3, wind_direction
                )
                contours.append(contour)
        
        return ImpactContour(
            contour_id=f"CONT_{impact_type}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            impact_type=impact_type,
            parameter=parameters.get('parameter', impact_type),
            contour_levels=levels if 'levels' in locals() else [],
            geometry=contours,
            unit=parameters.get('unit', 'units'),
            model_used=impact_model,
            created_date=datetime.now(),
            metadata=parameters
        )
    
    def create_web_map(
        self,
        project_boundary: ProjectBoundary,
        receptors: List[SensitiveReceptor],
        impact_zones: Optional[List[Polygon]] = None,
        contours: Optional[List[ImpactContour]] = None
    ) -> folium.Map:
        """
        Create interactive web map.
        
        Args:
            project_boundary: Project boundary
            receptors: Sensitive receptors
            impact_zones: Buffer/impact zones
            contours: Impact contours
            
        Returns:
            Folium map object
        """
        # Get map center
        center_lat = project_boundary.centroid.y
        center_lon = project_boundary.centroid.x
        
        # Create base map
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=13,
            tiles=None
        )
        
        # Add base layers
        folium.TileLayer('OpenStreetMap', name='OpenStreetMap').add_to(m)
        folium.TileLayer('Stamen Terrain', name='Terrain').add_to(m)
        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri',
            name='Satellite',
            overlay=False,
            control=True
        ).add_to(m)
        
        # Add project boundary
        boundary_style = {
            'fillColor': '#ff0000',
            'color': '#ff0000',
            'weight': 3,
            'fillOpacity': 0.1
        }
        
        folium.GeoJson(
            project_boundary.geometry.__geo_interface__,
            name='Project Boundary',
            style_function=lambda x: boundary_style,
            tooltip=folium.Tooltip(f"Project Area: {project_boundary.area_hectares:.1f} ha")
        ).add_to(m)
        
        # Add sensitive receptors
        receptor_group = folium.FeatureGroup(name='Sensitive Receptors')
        
        for receptor in receptors:
            # Get icon and color for receptor type
            receptor_info = self.receptor_types.get(
                receptor.receptor_type,
                {'icon': 'info-sign', 'color': 'gray'}
            )
            
            # Create marker
            folium.Marker(
                location=[receptor.latitude, receptor.longitude],
                popup=folium.Popup(
                    f"""
                    <b>{receptor.name}</b><br>
                    Type: {receptor.receptor_type}<br>
                    Sensitivity: {receptor.sensitivity_level}<br>
                    Distance: {receptor.metadata.get('distance_km', 0):.2f} km
                    """,
                    max_width=300
                ),
                tooltip=receptor.name,
                icon=folium.Icon(
                    color=receptor_info['color'],
                    icon=receptor_info['icon'],
                    prefix='fa'
                )
            ).add_to(receptor_group)
        
        receptor_group.add_to(m)
        
        # Add impact zones if provided
        if impact_zones:
            zone_group = folium.FeatureGroup(name='Impact Zones')
            
            colors = ['#ffff00', '#ff9900', '#ff6600', '#ff3300', '#ff0000']
            
            for i, zone in enumerate(impact_zones):
                folium.GeoJson(
                    zone.__geo_interface__,
                    style_function=lambda x, color=colors[i % len(colors)]: {
                        'fillColor': color,
                        'color': color,
                        'weight': 2,
                        'fillOpacity': 0.2
                    },
                    tooltip=f"Impact Zone {i+1}"
                ).add_to(zone_group)
            
            zone_group.add_to(m)
        
        # Add contours if provided
        if contours:
            for contour_set in contours:
                contour_group = folium.FeatureGroup(
                    name=f'{contour_set.impact_type} Contours'
                )
                
                for i, (level, geom) in enumerate(zip(
                    contour_set.contour_levels, 
                    contour_set.geometry
                )):
                    folium.GeoJson(
                        geom.__geo_interface__,
                        style_function=lambda x: {
                            'color': plt.cm.YlOrRd(i / len(contour_set.contour_levels)),
                            'weight': 2,
                            'fillOpacity': 0
                        },
                        tooltip=f"{level} {contour_set.unit}"
                    ).add_to(contour_group)
                
                contour_group.add_to(m)
        
        # Add measurement tool
        plugins.MeasureControl().add_to(m)
        
        # Add drawing tools
        draw = plugins.Draw(
            export=True,
            filename='eia_drawings.geojson',
            position='topleft',
            draw_options={
                'polyline': True,
                'polygon': True,
                'circle': True,
                'marker': True,
                'circlemarker': False,
                'rectangle': True
            }
        )
        draw.add_to(m)
        
        # Add fullscreen button
        plugins.Fullscreen().add_to(m)
        
        # Add layer control
        folium.LayerControl().add_to(m)
        
        # Add scale
        folium.plugins.MiniMap().add_to(m)
        
        return m
    
    def export_to_kml(
        self,
        project_boundary: ProjectBoundary,
        receptors: List[SensitiveReceptor],
        impact_zones: Optional[List[Polygon]] = None,
        output_path: str = "eia_project.kml"
    ) -> str:
        """
        Export spatial data to KML format.
        
        Args:
            project_boundary: Project boundary
            receptors: Sensitive receptors
            impact_zones: Impact zones
            output_path: Output file path
            
        Returns:
            KML file path
        """
        import simplekml
        
        kml = simplekml.Kml()
        
        # Add project boundary
        boundary_folder = kml.newfolder(name="Project Boundary")
        pol = boundary_folder.newpolygon(name="Project Area")
        pol.outerboundaryis = [
            (coord[0], coord[1]) for coord in project_boundary.geometry.exterior.coords
        ]
        pol.style.linestyle.color = simplekml.Color.red
        pol.style.linestyle.width = 3
        pol.style.polystyle.color = simplekml.Color.changealphaint(50, simplekml.Color.red)
        
        # Add sensitive receptors
        receptor_folder = kml.newfolder(name="Sensitive Receptors")
        
        for receptor in receptors:
            pnt = receptor_folder.newpoint(
                name=receptor.name,
                coords=[(receptor.longitude, receptor.latitude)]
            )
            pnt.description = f"""
            Type: {receptor.receptor_type}
            Sensitivity: {receptor.sensitivity_level}
            Distance: {receptor.metadata.get('distance_km', 0):.2f} km
            """
            
            # Set icon based on type
            receptor_info = self.receptor_types.get(receptor.receptor_type, {})
            if receptor_info.get('sensitivity') == 'Critical':
                pnt.style.iconstyle.color = simplekml.Color.red
            elif receptor_info.get('sensitivity') == 'High':
                pnt.style.iconstyle.color = simplekml.Color.orange
            else:
                pnt.style.iconstyle.color = simplekml.Color.yellow
        
        # Add impact zones
        if impact_zones:
            zone_folder = kml.newfolder(name="Impact Zones")
            
            for i, zone in enumerate(impact_zones):
                pol = zone_folder.newpolygon(name=f"Impact Zone {i+1}")
                if zone.geom_type == 'Polygon':
                    pol.outerboundaryis = [
                        (coord[0], coord[1]) for coord in zone.exterior.coords
                    ]
                pol.style.linestyle.color = simplekml.Color.orange
                pol.style.polystyle.color = simplekml.Color.changealphaint(
                    30 + i * 10, simplekml.Color.orange
                )
        
        # Save KML
        kml.save(output_path)
        
        return output_path
    
    def analyze_land_use(
        self,
        project_boundary: ProjectBoundary,
        buffer_distance_km: float = 2.0
    ) -> Dict[str, Any]:
        """
        Analyze land use around project area.
        
        Args:
            project_boundary: Project boundary
            buffer_distance_km: Analysis buffer distance
            
        Returns:
            Land use analysis results
        """
        # Create analysis area
        buffer = project_boundary.geometry.buffer(buffer_distance_km / 111)  # degrees
        
        # In a real implementation, this would query land use data
        # For now, return structured placeholder
        land_use = {
            'analysis_area_km2': buffer.area * 111 * 111,  # Approximate
            'land_use_types': {
                'residential': {'area_km2': 0.5, 'percentage': 25},
                'commercial': {'area_km2': 0.3, 'percentage': 15},
                'industrial': {'area_km2': 0.2, 'percentage': 10},
                'agricultural': {'area_km2': 0.4, 'percentage': 20},
                'open_space': {'area_km2': 0.6, 'percentage': 30}
            },
            'dominant_use': 'open_space',
            'compatibility_assessment': {
                'compatible_uses': ['industrial', 'open_space'],
                'conflicts': ['residential - noise/air quality concerns'],
                'mitigation_needed': True
            }
        }
        
        return land_use
    
    def calculate_viewshed(
        self,
        observer_point: Tuple[float, float],
        observer_height: float,
        target_height: float,
        radius_km: float = 5.0
    ) -> Polygon:
        """
        Calculate simplified viewshed (visibility area).
        
        Args:
            observer_point: Observer location (lat, lon)
            observer_height: Observer height in meters
            target_height: Target structure height in meters
            radius_km: Maximum view distance
            
        Returns:
            Viewshed polygon
        """
        # Simplified viewshed - in reality would use DEM data
        # Calculate theoretical maximum viewing distance
        earth_radius = 6371000  # meters
        
        # Distance to horizon from observer
        d1 = sqrt(2 * earth_radius * observer_height)
        
        # Distance to horizon from target
        d2 = sqrt(2 * earth_radius * target_height)
        
        # Total viewing distance
        max_distance = (d1 + d2) / 1000  # km
        
        # Use smaller of theoretical max or specified radius
        view_radius = min(max_distance, radius_km)
        
        # Create circular viewshed (simplified)
        viewshed = Point(observer_point[1], observer_point[0]).buffer(
            view_radius / 111  # Convert km to degrees
        )
        
        return viewshed
    
    def _query_osm_receptors(
        self,
        center_point: Tuple[float, float],
        radius_km: float,
        receptor_types: Optional[List[str]] = None
    ) -> List[SensitiveReceptor]:
        """Query OpenStreetMap for sensitive receptors."""
        receptors = []
        
        # Build Overpass API query
        lat, lon = center_point
        
        # OSM tags for different receptor types
        osm_tags = {
            'residential': ['building=residential', 'building=apartments', 'landuse=residential'],
            'school': ['amenity=school', 'amenity=university', 'amenity=college', 'amenity=kindergarten'],
            'hospital': ['amenity=hospital', 'amenity=clinic', 'healthcare=*'],
            'mosque': ['amenity=place_of_worship', 'religion=muslim'],
            'park': ['leisure=park', 'leisure=garden', 'landuse=recreation_ground'],
            'hotel': ['tourism=hotel', 'tourism=motel', 'tourism=guest_house']
        }
        
        # Build query
        query_parts = []
        for rtype, tags in osm_tags.items():
            if receptor_types is None or rtype in receptor_types:
                for tag in tags:
                    query_parts.append(f'node[{tag}](around:{radius_km*1000},{lat},{lon});')
                    query_parts.append(f'way[{tag}](around:{radius_km*1000},{lat},{lon});')
        
        query = f"""
        [out:json][timeout:25];
        ({';'.join(query_parts)});
        out center;
        """
        
        # Query Overpass API
        try:
            response = requests.post(
                'https://overpass-api.de/api/interpreter',
                data=query,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Parse results
                for element in data.get('elements', []):
                    tags = element.get('tags', {})
                    
                    # Determine receptor type
                    receptor_type = 'unknown'
                    for rtype, osm_tag_list in osm_tags.items():
                        if any(tag.split('=')[0] in tags for tag in osm_tag_list):
                            receptor_type = rtype
                            break
                    
                    # Get coordinates
                    if element['type'] == 'node':
                        lat = element['lat']
                        lon = element['lon']
                    elif element['type'] == 'way' and 'center' in element:
                        lat = element['center']['lat']
                        lon = element['center']['lon']
                    else:
                        continue
                    
                    # Create receptor
                    receptor = SensitiveReceptor(
                        receptor_id='',  # Will be assigned later
                        name=tags.get('name', f'{receptor_type.title()} {element["id"]}'),
                        receptor_type=receptor_type,
                        latitude=lat,
                        longitude=lon,
                        sensitivity_level=self.receptor_types.get(
                            receptor_type, {}
                        ).get('sensitivity', 'Medium')
                    )
                    
                    receptors.append(receptor)
                    
        except Exception as e:
            logger.warning(f"OSM query failed: {e}")
        
        return receptors
    
    def _calculate_distance(
        self,
        lat1: float, lon1: float,
        lat2: float, lon2: float
    ) -> float:
        """Calculate distance between two points in kilometers."""
        # Haversine formula
        R = 6371  # Earth radius in kilometers
        
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        
        return R * c
    
    def _get_utm_crs(self, point: Tuple[float, float]) -> pyproj.CRS:
        """Get appropriate UTM CRS for a point."""
        lat, lon = point
        
        # Determine UTM zone
        if 22 <= lat <= 32 and 44 <= lon <= 60:
            # UAE
            return self.utm_zones['UAE']
        elif 16 <= lat <= 32 and 34 <= lon <= 44:
            # Western Saudi Arabia
            return self.utm_zones['KSA_West']
        else:
            # Eastern Saudi Arabia
            return self.utm_zones['KSA_East']
    
    def _calculate_plume_distance(
        self,
        emission_rate: float,
        wind_speed: float,
        stack_height: float,
        concentration: float
    ) -> float:
        """Calculate distance for given concentration (simplified Gaussian)."""
        # Very simplified - real implementation would use proper dispersion coefficients
        # Distance where ground-level concentration equals target
        
        # Simplified calculation
        sigma_y = 0.08  # Dispersion coefficient (simplified)
        sigma_z = 0.06
        
        # Solve for distance where C = target concentration
        # This is highly simplified!
        distance = emission_rate / (concentration * wind_speed * sigma_y * sigma_z * 2 * 3.14159)
        distance = distance ** 0.5 * 100  # Scaling factor
        
        return min(distance, 5000)  # Cap at 5km
    
    def _create_elliptical_contour(
        self,
        center: Tuple[float, float],
        major_axis: float,
        minor_axis: float,
        rotation: float
    ) -> Polygon:
        """Create elliptical contour."""
        # Create ellipse points
        theta = np.linspace(0, 2*np.pi, 100)
        
        # Ellipse in local coordinates
        x = major_axis * np.cos(theta) / 111000  # Convert to degrees
        y = minor_axis * np.sin(theta) / 111000
        
        # Rotate
        rotation_rad = radians(rotation)
        x_rot = x * cos(rotation_rad) - y * sin(rotation_rad)
        y_rot = x * sin(rotation_rad) + y * cos(rotation_rad)
        
        # Translate to center
        x_final = x_rot + center[1]
        y_final = y_rot + center[0]
        
        # Create polygon
        coords = [(x_final[i], y_final[i]) for i in range(len(theta))]
        
        return Polygon(coords)
    
    def generate_eia_maps(
        self,
        project_data: Dict[str, Any],
        output_dir: str
    ) -> Dict[str, str]:
        """
        Generate all required EIA maps.
        
        Args:
            project_data: Project information
            output_dir: Output directory for maps
            
        Returns:
            Dictionary of map file paths
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        maps = {}
        
        # 1. Location Map
        location_map = self.create_web_map(
            project_data['boundary'],
            project_data.get('receptors', [])
        )
        location_path = os.path.join(output_dir, 'location_map.html')
        location_map.save(location_path)
        maps['location'] = location_path
        
        # 2. Sensitive Receptors Map
        if 'receptors' in project_data and 'impact_zones' in project_data:
            receptor_map = self.create_web_map(
                project_data['boundary'],
                project_data['receptors'],
                project_data['impact_zones']
            )
            receptor_path = os.path.join(output_dir, 'receptor_map.html')
            receptor_map.save(receptor_path)
            maps['receptors'] = receptor_path
        
        # 3. Impact Contours Map
        if 'contours' in project_data:
            contour_map = self.create_web_map(
                project_data['boundary'],
                project_data.get('receptors', []),
                contours=project_data['contours']
            )
            contour_path = os.path.join(output_dir, 'contour_map.html')
            contour_map.save(contour_path)
            maps['contours'] = contour_path
        
        # 4. Export to KML
        kml_path = os.path.join(output_dir, 'project_spatial.kml')
        self.export_to_kml(
            project_data['boundary'],
            project_data.get('receptors', []),
            project_data.get('impact_zones', []),
            kml_path
        )
        maps['kml'] = kml_path
        
        return maps