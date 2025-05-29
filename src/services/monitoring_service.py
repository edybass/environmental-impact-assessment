"""
Environmental Monitoring Service
Real-time monitoring, alerts, and data analysis

Author: Edy Bassil
Email: bassileddy@gmail.com
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
import numpy as np
from dataclasses import dataclass
import logging

from src.services.base_service import BaseService, ValidationError, ServiceException
from src.models import Project, MonitoringData, MitigationMeasure
from src.config import get_config

logger = logging.getLogger(__name__)
config = get_config()


@dataclass
class Alert:
    """Environmental alert."""
    project_id: int
    parameter: str
    value: float
    threshold: float
    severity: str  # low, medium, high, critical
    message: str
    timestamp: datetime
    location: Optional[str] = None


@dataclass
class TrendAnalysis:
    """Trend analysis results."""
    parameter: str
    trend: str  # increasing, decreasing, stable
    change_percentage: float
    forecast_value: float
    confidence: float


class MonitoringService(BaseService[MonitoringData]):
    """
    Service for environmental monitoring and alerting.
    Handles real-time data, trends, and compliance alerts.
    """
    
    def __init__(self, session: Session):
        super().__init__(MonitoringData, session)
        self.alert_thresholds = config.monitoring.alert_thresholds
        self.alerts: List[Alert] = []
    
    def _validate_create_data(self, data: Dict[str, Any]) -> None:
        """Validate monitoring data."""
        required_fields = ['project_id', 'parameter', 'value', 'unit']
        
        for field in required_fields:
            if field not in data or data[field] is None:
                raise ValidationError(f"{field} is required", field)
        
        # Validate parameter
        valid_parameters = [
            'pm10', 'pm25', 'noise', 'temperature', 'humidity',
            'wind_speed', 'voc', 'co', 'no2', 'so2', 'vibration'
        ]
        
        if data['parameter'] not in valid_parameters:
            raise ValidationError(
                f"Invalid parameter. Must be one of: {valid_parameters}", 
                'parameter'
            )
        
        # Validate value is numeric and positive
        if not isinstance(data['value'], (int, float)) or data['value'] < 0:
            raise ValidationError("Value must be a positive number", 'value')
        
        # Validate unit based on parameter
        unit_map = {
            'pm10': 'μg/m³',
            'pm25': 'μg/m³',
            'noise': 'dB(A)',
            'temperature': '°C',
            'humidity': '%',
            'wind_speed': 'km/h',
            'voc': 'ppm',
            'co': 'ppm',
            'no2': 'ppm',
            'so2': 'ppm',
            'vibration': 'mm/s'
        }
        
        expected_unit = unit_map.get(data['parameter'])
        if expected_unit and data['unit'] != expected_unit:
            raise ValidationError(
                f"Unit for {data['parameter']} should be {expected_unit}", 
                'unit'
            )
        
        # Validate coordinates if provided
        if 'latitude' in data and data['latitude'] is not None:
            if not (-90 <= data['latitude'] <= 90):
                raise ValidationError("Invalid latitude", 'latitude')
        
        if 'longitude' in data and data['longitude'] is not None:
            if not (-180 <= data['longitude'] <= 180):
                raise ValidationError("Invalid longitude", 'longitude')
    
    def _validate_update_data(self, data: Dict[str, Any], entity: MonitoringData) -> None:
        """Validate monitoring data update."""
        # Can't change fundamental fields
        immutable_fields = ['project_id', 'parameter', 'measurement_date']
        
        for field in immutable_fields:
            if field in data and data[field] != getattr(entity, field):
                raise ValidationError(f"{field} cannot be changed", field)
        
        # Validate other fields
        if data:
            self._validate_create_data({**entity.__dict__, **data})
    
    def record_measurement(self, 
                          project_id: int,
                          parameter: str,
                          value: float,
                          monitoring_point: str = None,
                          coordinates: Tuple[float, float] = None,
                          weather_conditions: str = None,
                          equipment_used: str = None) -> MonitoringData:
        """
        Record environmental measurement with automatic alerts.
        
        Args:
            project_id: Project ID
            parameter: Parameter being measured
            value: Measured value
            monitoring_point: Location identifier
            coordinates: (latitude, longitude) tuple
            weather_conditions: Current weather
            equipment_used: Monitoring equipment
            
        Returns:
            MonitoringData record
        """
        # Get unit for parameter
        unit_map = {
            'pm10': 'μg/m³', 'pm25': 'μg/m³', 'noise': 'dB(A)',
            'temperature': '°C', 'humidity': '%', 'wind_speed': 'km/h'
        }
        unit = unit_map.get(parameter, 'unit')
        
        # Get threshold for parameter
        threshold = self._get_threshold(project_id, parameter)
        
        # Create monitoring record
        data = {
            'project_id': project_id,
            'parameter': parameter,
            'value': value,
            'unit': unit,
            'monitoring_point': monitoring_point,
            'measurement_time': datetime.utcnow().strftime('%H:%M'),
            'weather_conditions': weather_conditions,
            'equipment_used': equipment_used,
            'limit_value': threshold,
            'exceeds_limit': value > threshold if threshold else False
        }
        
        if coordinates:
            data['latitude'] = coordinates[0]
            data['longitude'] = coordinates[1]
        
        monitoring_record = self.create(data)
        
        # Check for alerts
        if monitoring_record.exceeds_limit:
            self._create_alert(project_id, parameter, value, threshold, monitoring_point)
        
        return monitoring_record
    
    def bulk_record_measurements(self, measurements: List[Dict[str, Any]]) -> List[MonitoringData]:
        """
        Record multiple measurements in bulk.
        
        Args:
            measurements: List of measurement data
            
        Returns:
            List of MonitoringData records
        """
        records = []
        alerts_to_create = []
        
        for measurement in measurements:
            # Process each measurement
            threshold = self._get_threshold(
                measurement['project_id'], 
                measurement['parameter']
            )
            
            measurement['limit_value'] = threshold
            measurement['exceeds_limit'] = measurement['value'] > threshold if threshold else False
            
            if measurement['exceeds_limit']:
                alerts_to_create.append(measurement)
        
        # Bulk create records
        records = self.bulk_create(measurements)
        
        # Create alerts
        for alert_data in alerts_to_create:
            self._create_alert(
                alert_data['project_id'],
                alert_data['parameter'],
                alert_data['value'],
                alert_data['limit_value'],
                alert_data.get('monitoring_point')
            )
        
        return records
    
    def get_latest_readings(self, 
                           project_id: int,
                           parameters: List[str] = None) -> Dict[str, Any]:
        """
        Get latest readings for all or specified parameters.
        
        Args:
            project_id: Project ID
            parameters: List of parameters to retrieve
            
        Returns:
            Dictionary of latest readings by parameter
        """
        query = self.session.query(MonitoringData).filter_by(project_id=project_id)
        
        if parameters:
            query = query.filter(MonitoringData.parameter.in_(parameters))
        
        # Get latest reading for each parameter
        subquery = query.distinct(MonitoringData.parameter).subquery()
        
        latest_readings = {}
        
        for param in parameters or ['pm10', 'pm25', 'noise', 'temperature']:
            reading = query.filter_by(parameter=param).order_by(
                MonitoringData.measurement_date.desc()
            ).first()
            
            if reading:
                latest_readings[param] = {
                    'value': reading.value,
                    'unit': reading.unit,
                    'timestamp': reading.measurement_date.isoformat(),
                    'exceeds_limit': reading.exceeds_limit,
                    'monitoring_point': reading.monitoring_point
                }
        
        return latest_readings
    
    def analyze_trends(self,
                      project_id: int,
                      parameter: str,
                      days: int = 30) -> TrendAnalysis:
        """
        Analyze trends for a parameter over time.
        
        Args:
            project_id: Project ID
            parameter: Parameter to analyze
            days: Number of days to analyze
            
        Returns:
            TrendAnalysis with results
        """
        # Get historical data
        since_date = datetime.utcnow() - timedelta(days=days)
        
        readings = self.session.query(
            MonitoringData.measurement_date,
            MonitoringData.value
        ).filter(
            and_(
                MonitoringData.project_id == project_id,
                MonitoringData.parameter == parameter,
                MonitoringData.measurement_date >= since_date
            )
        ).order_by(MonitoringData.measurement_date).all()
        
        if len(readings) < 3:
            return TrendAnalysis(
                parameter=parameter,
                trend='insufficient_data',
                change_percentage=0,
                forecast_value=readings[-1].value if readings else 0,
                confidence=0
            )
        
        # Extract values and timestamps
        timestamps = np.array([(r.measurement_date - since_date).days for r in readings])
        values = np.array([r.value for r in readings])
        
        # Calculate linear regression
        coefficients = np.polyfit(timestamps, values, 1)
        slope = coefficients[0]
        
        # Determine trend
        avg_value = np.mean(values)
        if abs(slope) < 0.01 * avg_value:  # Less than 1% change per day
            trend = 'stable'
        elif slope > 0:
            trend = 'increasing'
        else:
            trend = 'decreasing'
        
        # Calculate change percentage
        first_value = values[0]
        last_value = values[-1]
        change_percentage = ((last_value - first_value) / first_value) * 100 if first_value != 0 else 0
        
        # Forecast next value (simple linear extrapolation)
        next_day = timestamps[-1] + 1
        forecast_value = coefficients[0] * next_day + coefficients[1]
        forecast_value = max(0, forecast_value)  # Ensure non-negative
        
        # Calculate confidence (R-squared)
        y_pred = np.polyval(coefficients, timestamps)
        ss_res = np.sum((values - y_pred) ** 2)
        ss_tot = np.sum((values - np.mean(values)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        confidence = max(0, min(100, r_squared * 100))
        
        return TrendAnalysis(
            parameter=parameter,
            trend=trend,
            change_percentage=change_percentage,
            forecast_value=forecast_value,
            confidence=confidence
        )
    
    def get_exceedances(self,
                       project_id: int,
                       start_date: datetime = None,
                       end_date: datetime = None) -> List[Dict[str, Any]]:
        """
        Get all threshold exceedances for a project.
        
        Args:
            project_id: Project ID
            start_date: Start date filter
            end_date: End date filter
            
        Returns:
            List of exceedance records
        """
        query = self.session.query(MonitoringData).filter(
            and_(
                MonitoringData.project_id == project_id,
                MonitoringData.exceeds_limit == True
            )
        )
        
        if start_date:
            query = query.filter(MonitoringData.measurement_date >= start_date)
        
        if end_date:
            query = query.filter(MonitoringData.measurement_date <= end_date)
        
        exceedances = query.order_by(MonitoringData.measurement_date.desc()).all()
        
        return [
            {
                'parameter': e.parameter,
                'value': e.value,
                'limit': e.limit_value,
                'exceedance_percentage': ((e.value - e.limit_value) / e.limit_value * 100) if e.limit_value else 0,
                'timestamp': e.measurement_date.isoformat(),
                'location': e.monitoring_point,
                'duration': self._calculate_exceedance_duration(e)
            }
            for e in exceedances
        ]
    
    def generate_monitoring_report(self, 
                                 project_id: int,
                                 start_date: datetime,
                                 end_date: datetime) -> Dict[str, Any]:
        """
        Generate comprehensive monitoring report.
        
        Args:
            project_id: Project ID
            start_date: Report start date
            end_date: Report end date
            
        Returns:
            Dictionary with monitoring statistics
        """
        # Get all parameters monitored
        parameters = self.session.query(MonitoringData.parameter).filter(
            and_(
                MonitoringData.project_id == project_id,
                MonitoringData.measurement_date.between(start_date, end_date)
            )
        ).distinct().all()
        
        report = {
            'project_id': project_id,
            'period': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat(),
                'days': (end_date - start_date).days
            },
            'parameters': {}
        }
        
        for (param,) in parameters:
            # Get statistics for each parameter
            stats = self.session.query(
                func.count(MonitoringData.id).label('count'),
                func.avg(MonitoringData.value).label('average'),
                func.min(MonitoringData.value).label('minimum'),
                func.max(MonitoringData.value).label('maximum'),
                func.stddev(MonitoringData.value).label('std_dev'),
                func.sum(func.cast(MonitoringData.exceeds_limit, Integer)).label('exceedances')
            ).filter(
                and_(
                    MonitoringData.project_id == project_id,
                    MonitoringData.parameter == param,
                    MonitoringData.measurement_date.between(start_date, end_date)
                )
            ).first()
            
            # Get trend
            trend = self.analyze_trends(project_id, param, (end_date - start_date).days)
            
            report['parameters'][param] = {
                'measurements': stats.count,
                'average': float(stats.average) if stats.average else 0,
                'minimum': float(stats.minimum) if stats.minimum else 0,
                'maximum': float(stats.maximum) if stats.maximum else 0,
                'std_deviation': float(stats.std_dev) if stats.std_dev else 0,
                'exceedances': stats.exceedances or 0,
                'compliance_rate': ((stats.count - (stats.exceedances or 0)) / stats.count * 100) if stats.count else 100,
                'trend': {
                    'direction': trend.trend,
                    'change_percentage': trend.change_percentage,
                    'forecast': trend.forecast_value
                }
            }
        
        # Overall compliance
        total_measurements = sum(p['measurements'] for p in report['parameters'].values())
        total_exceedances = sum(p['exceedances'] for p in report['parameters'].values())
        
        report['overall'] = {
            'total_measurements': total_measurements,
            'total_exceedances': total_exceedances,
            'compliance_rate': ((total_measurements - total_exceedances) / total_measurements * 100) if total_measurements else 100
        }
        
        return report
    
    def get_monitoring_alerts(self, 
                            project_id: int = None,
                            severity: str = None,
                            hours: int = 24) -> List[Alert]:
        """
        Get recent monitoring alerts.
        
        Args:
            project_id: Filter by project
            severity: Filter by severity
            hours: Hours to look back
            
        Returns:
            List of alerts
        """
        since = datetime.utcnow() - timedelta(hours=hours)
        
        alerts = [a for a in self.alerts if a.timestamp >= since]
        
        if project_id:
            alerts = [a for a in alerts if a.project_id == project_id]
        
        if severity:
            alerts = [a for a in alerts if a.severity == severity]
        
        return sorted(alerts, key=lambda a: a.timestamp, reverse=True)
    
    def _get_threshold(self, project_id: int, parameter: str) -> float:
        """Get threshold for parameter based on project location."""
        # Get project location
        project = self.session.query(Project).filter_by(id=project_id).first()
        if not project:
            return self.alert_thresholds.get(parameter, float('inf'))
        
        # Use regional thresholds
        if project.location in ['Dubai', 'Abu Dhabi', 'Sharjah']:
            if parameter == 'pm10':
                return config.regional.uae_pm10_limit
            elif parameter == 'pm25':
                return config.regional.uae_pm25_limit
            elif parameter == 'noise':
                return config.regional.uae_noise_residential_day
        elif project.location in ['Riyadh', 'Jeddah']:
            if parameter == 'pm10':
                return config.regional.ksa_pm10_limit
            elif parameter == 'pm25':
                return config.regional.ksa_pm25_limit
            elif parameter == 'noise':
                return config.regional.ksa_noise_day
        
        return self.alert_thresholds.get(parameter, float('inf'))
    
    def _create_alert(self, 
                     project_id: int,
                     parameter: str,
                     value: float,
                     threshold: float,
                     location: str = None):
        """Create and store alert."""
        # Determine severity
        exceedance = (value - threshold) / threshold * 100 if threshold else 0
        
        if exceedance > 100:
            severity = 'critical'
        elif exceedance > 50:
            severity = 'high'
        elif exceedance > 20:
            severity = 'medium'
        else:
            severity = 'low'
        
        # Create alert message
        message = f"{parameter.upper()} level of {value} exceeds limit of {threshold} by {exceedance:.1f}%"
        
        alert = Alert(
            project_id=project_id,
            parameter=parameter,
            value=value,
            threshold=threshold,
            severity=severity,
            message=message,
            timestamp=datetime.utcnow(),
            location=location
        )
        
        self.alerts.append(alert)
        
        # Log alert
        logger.warning(f"Alert created for project {project_id}: {message}")
        
        # In production, send notifications here
        # self._send_notifications(alert)
    
    def _calculate_exceedance_duration(self, exceedance: MonitoringData) -> str:
        """Calculate how long parameter has been exceeding limit."""
        # Find when exceedance started
        previous_readings = self.session.query(MonitoringData).filter(
            and_(
                MonitoringData.project_id == exceedance.project_id,
                MonitoringData.parameter == exceedance.parameter,
                MonitoringData.monitoring_point == exceedance.monitoring_point,
                MonitoringData.measurement_date < exceedance.measurement_date
            )
        ).order_by(MonitoringData.measurement_date.desc()).limit(10).all()
        
        duration = timedelta(0)
        for reading in previous_readings:
            if reading.exceeds_limit:
                duration = exceedance.measurement_date - reading.measurement_date
            else:
                break
        
        if duration.days > 0:
            return f"{duration.days} days"
        elif duration.seconds > 3600:
            return f"{duration.seconds // 3600} hours"
        else:
            return "< 1 hour"