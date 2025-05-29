"""
Business Logic Services
Service layer for environmental impact assessment

Author: Edy Bassil
Email: bassileddy@gmail.com
"""

from .base_service import (
    BaseService,
    CachedService,
    ServiceException,
    ValidationError,
    NotFoundError,
    UnauthorizedError
)
from .project_service import ProjectService
from .monitoring_service import MonitoringService, Alert, TrendAnalysis
from .auth_service import AuthService, UserRole, Permission
from .report_service import ReportService, ReportType, ReportLanguage, ReportConfig
from .water_service import WaterService

__all__ = [
    # Base classes
    'BaseService',
    'CachedService',
    
    # Exceptions
    'ServiceException',
    'ValidationError',
    'NotFoundError',
    'UnauthorizedError',
    
    # Services
    'ProjectService',
    'MonitoringService',
    'AuthService',
    'ReportService',
    'WaterService',
    
    # Data classes
    'Alert',
    'TrendAnalysis',
    'ReportConfig',
    
    # Enums
    'UserRole',
    'Permission',
    'ReportType',
    'ReportLanguage'
]