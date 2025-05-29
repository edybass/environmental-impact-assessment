"""
Configuration Management
Central configuration for the EIA application

Author: Edy Bassil
Email: bassileddy@gmail.com
"""

import os
from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass
import json
import logging

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent


@dataclass
class DatabaseConfig:
    """Database configuration."""
    url: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/eia_database.db")
    echo: bool = os.getenv("DB_ECHO", "false").lower() == "true"
    pool_size: int = int(os.getenv("DB_POOL_SIZE", "5"))
    max_overflow: int = int(os.getenv("DB_MAX_OVERFLOW", "10"))


@dataclass
class APIConfig:
    """API configuration."""
    host: str = os.getenv("API_HOST", "0.0.0.0")
    port: int = int(os.getenv("API_PORT", "8000"))
    debug: bool = os.getenv("API_DEBUG", "false").lower() == "true"
    cors_origins: list = json.loads(os.getenv("CORS_ORIGINS", '["*"]'))
    api_key: str = os.getenv("API_KEY", "development-key")


@dataclass
class RegionalConfig:
    """Regional settings and thresholds."""
    # UAE Standards
    uae_pm10_limit: float = 150  # μg/m³ (24-hour)
    uae_pm25_limit: float = 65   # μg/m³ (24-hour)
    uae_noise_residential_day: float = 65  # dB(A)
    uae_noise_residential_night: float = 55  # dB(A)
    uae_noise_commercial_day: float = 70  # dB(A)
    uae_noise_commercial_night: float = 60  # dB(A)
    
    # KSA Standards
    ksa_pm10_limit: float = 340  # μg/m³ (24-hour)
    ksa_pm25_limit: float = 75   # μg/m³ (24-hour)
    ksa_noise_day: float = 70    # dB(A)
    ksa_noise_night: float = 60  # dB(A)
    
    # Water scarcity thresholds
    water_scarcity_threshold: float = 1000  # m³/day
    high_water_usage: float = 5000  # m³/day


@dataclass
class ReportConfig:
    """Report generation configuration."""
    reports_dir: Path = BASE_DIR / "reports"
    templates_dir: Path = BASE_DIR / "templates"
    logo_path: Path = BASE_DIR / "static" / "logo.png"
    default_language: str = "en"
    languages: list = None
    
    def __post_init__(self):
        if self.languages is None:
            self.languages = ["en", "ar"]
        # Create directories if they don't exist
        self.reports_dir.mkdir(exist_ok=True)
        self.templates_dir.mkdir(exist_ok=True)


@dataclass
class LoggingConfig:
    """Logging configuration."""
    level: str = os.getenv("LOG_LEVEL", "INFO")
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file: Path = BASE_DIR / "logs" / "eia.log"
    max_bytes: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    
    def __post_init__(self):
        # Create logs directory if it doesn't exist
        self.file.parent.mkdir(exist_ok=True)


@dataclass
class EmailConfig:
    """Email notification configuration."""
    smtp_host: str = os.getenv("SMTP_HOST", "localhost")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_user: str = os.getenv("SMTP_USER", "")
    smtp_password: str = os.getenv("SMTP_PASSWORD", "")
    from_email: str = os.getenv("FROM_EMAIL", "eia@example.com")
    admin_emails: list = json.loads(os.getenv("ADMIN_EMAILS", '["admin@example.com"]'))


@dataclass
class MonitoringConfig:
    """Environmental monitoring configuration."""
    monitoring_interval: int = int(os.getenv("MONITORING_INTERVAL", "3600"))  # seconds
    alert_thresholds: Dict[str, float] = None
    data_retention_days: int = int(os.getenv("DATA_RETENTION_DAYS", "365"))
    
    def __post_init__(self):
        if self.alert_thresholds is None:
            self.alert_thresholds = {
                "pm10": 200,  # μg/m³
                "pm25": 100,  # μg/m³
                "noise": 75,  # dB(A)
                "temperature": 50,  # °C (relevant for Gulf region)
            }


@dataclass
class SecurityConfig:
    """Security configuration."""
    secret_key: str = os.getenv("SECRET_KEY", "development-secret-key-change-in-production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = int(os.getenv("TOKEN_EXPIRE_MINUTES", "30"))
    password_min_length: int = 8
    password_require_special: bool = True
    max_login_attempts: int = 5
    lockout_duration: int = 300  # seconds


class Config:
    """Main configuration class."""
    
    def __init__(self):
        self.env = os.getenv("ENVIRONMENT", "development")
        self.debug = self.env == "development"
        
        # Sub-configurations
        self.database = DatabaseConfig()
        self.api = APIConfig()
        self.regional = RegionalConfig()
        self.report = ReportConfig()
        self.logging = LoggingConfig()
        self.email = EmailConfig()
        self.monitoring = MonitoringConfig()
        self.security = SecurityConfig()
        
        # Application settings
        self.app_name = "Environmental Impact Assessment Tool"
        self.app_version = "2.0.0"
        self.app_author = "Edy Bassil"
        self.app_email = "bassileddy@gmail.com"
        
        # Feature flags
        self.features = {
            "satellite_monitoring": os.getenv("FEATURE_SATELLITE", "false").lower() == "true",
            "ai_predictions": os.getenv("FEATURE_AI", "false").lower() == "true",
            "blockchain_tracking": os.getenv("FEATURE_BLOCKCHAIN", "false").lower() == "true",
            "mobile_app": os.getenv("FEATURE_MOBILE", "false").lower() == "true",
        }
        
        # Initialize logging
        self._setup_logging()
    
    def _setup_logging(self):
        """Set up logging configuration."""
        logging.basicConfig(
            level=getattr(logging, self.logging.level.upper()),
            format=self.logging.format
        )
        
        # Add file handler if not in development
        if self.env != "development":
            from logging.handlers import RotatingFileHandler
            
            file_handler = RotatingFileHandler(
                self.logging.file,
                maxBytes=self.logging.max_bytes,
                backupCount=self.logging.backup_count
            )
            file_handler.setFormatter(logging.Formatter(self.logging.format))
            logging.getLogger().addHandler(file_handler)
    
    def get_threshold(self, parameter: str, jurisdiction: str = "UAE") -> float:
        """
        Get environmental threshold for a parameter and jurisdiction.
        
        Args:
            parameter: Environmental parameter (e.g., 'pm10', 'noise')
            jurisdiction: Jurisdiction (UAE or KSA)
            
        Returns:
            Threshold value
        """
        thresholds = {
            "UAE": {
                "pm10": self.regional.uae_pm10_limit,
                "pm25": self.regional.uae_pm25_limit,
                "noise_residential_day": self.regional.uae_noise_residential_day,
                "noise_residential_night": self.regional.uae_noise_residential_night,
                "noise_commercial_day": self.regional.uae_noise_commercial_day,
                "noise_commercial_night": self.regional.uae_noise_commercial_night,
            },
            "KSA": {
                "pm10": self.regional.ksa_pm10_limit,
                "pm25": self.regional.ksa_pm25_limit,
                "noise_day": self.regional.ksa_noise_day,
                "noise_night": self.regional.ksa_noise_night,
            }
        }
        
        return thresholds.get(jurisdiction, {}).get(parameter, 0)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "environment": self.env,
            "debug": self.debug,
            "app": {
                "name": self.app_name,
                "version": self.app_version,
                "author": self.app_author,
                "email": self.app_email,
            },
            "features": self.features,
            "database": {
                "url": self.database.url.replace(self.database.url.split("://")[1].split("@")[0], "***")
                if "@" in self.database.url else self.database.url,
                "pool_size": self.database.pool_size,
            },
            "api": {
                "host": self.api.host,
                "port": self.api.port,
                "debug": self.api.debug,
            },
            "regional": {
                "uae_pm10_limit": self.regional.uae_pm10_limit,
                "uae_noise_limits": {
                    "residential_day": self.regional.uae_noise_residential_day,
                    "residential_night": self.regional.uae_noise_residential_night,
                },
                "ksa_pm10_limit": self.regional.ksa_pm10_limit,
                "ksa_noise_limits": {
                    "day": self.regional.ksa_noise_day,
                    "night": self.regional.ksa_noise_night,
                },
            },
        }
    
    def validate(self):
        """Validate configuration settings."""
        errors = []
        
        # Check critical settings
        if self.env == "production":
            if self.security.secret_key == "development-secret-key-change-in-production":
                errors.append("SECRET_KEY must be changed for production")
            if self.api.api_key == "development-key":
                errors.append("API_KEY must be changed for production")
            if self.api.debug:
                errors.append("Debug mode should be disabled in production")
        
        # Check paths
        if not self.report.reports_dir.exists():
            try:
                self.report.reports_dir.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                errors.append(f"Cannot create reports directory: {e}")
        
        if errors:
            raise ValueError(f"Configuration errors: {'; '.join(errors)}")
        
        return True


# Global configuration instance
config = Config()


def get_config() -> Config:
    """Get configuration instance."""
    return config


def reload_config():
    """Reload configuration from environment."""
    global config
    config = Config()
    return config


if __name__ == "__main__":
    # Test configuration
    cfg = get_config()
    
    print("EIA Tool Configuration")
    print("=" * 50)
    print(f"Environment: {cfg.env}")
    print(f"Database: {cfg.database.url}")
    print(f"API Port: {cfg.api.port}")
    print(f"Log Level: {cfg.logging.level}")
    
    print("\nRegional Thresholds:")
    print(f"UAE PM10 Limit: {cfg.regional.uae_pm10_limit} μg/m³")
    print(f"KSA PM10 Limit: {cfg.regional.ksa_pm10_limit} μg/m³")
    
    print("\nFeature Flags:")
    for feature, enabled in cfg.features.items():
        print(f"{feature}: {'Enabled' if enabled else 'Disabled'}")
    
    # Validate configuration
    try:
        cfg.validate()
        print("\n✅ Configuration is valid")
    except ValueError as e:
        print(f"\n❌ Configuration error: {e}")