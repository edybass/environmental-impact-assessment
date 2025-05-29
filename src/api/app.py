"""
EIA Tool API
Professional Environmental Impact Assessment API for UAE/KSA

Author: Edy Bassil
Email: bassileddy@gmail.com
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
import time
from contextlib import asynccontextmanager
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.models import init_database
from src.config import get_config
from src.api.endpoints import all_routers
from src.services import ServiceException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load configuration
config = get_config()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting EIA Tool API...")
    
    # Initialize database
    try:
        init_database()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
    
    # Validate configuration
    try:
        config.validate()
        logger.info("Configuration validated successfully")
    except Exception as e:
        logger.error(f"Configuration validation failed: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down EIA Tool API...")


# Create FastAPI application
app = FastAPI(
    title="Environmental Impact Assessment API",
    description="""
    ## Professional EIA Tool for UAE & Saudi Arabia 🌿
    
    Comprehensive environmental impact assessment and monitoring system designed 
    specifically for construction projects in the Gulf region.
    
    ### Features:
    - 📋 **Project Management**: Create and track construction projects
    - 🔍 **Environmental Screening**: Automated EIA requirement assessment
    - 📊 **Impact Analysis**: Carbon footprint, water, waste, and biodiversity
    - ⚠️ **Risk Assessment**: ISO 31000 compliant risk management
    - 📏 **Compliance Checking**: UAE/KSA regulatory compliance
    - 📈 **Real-time Monitoring**: Environmental parameter tracking
    - 📑 **Reporting**: Comprehensive reports and dashboards
    
    ### Supported Jurisdictions:
    - 🇦🇪 UAE (Federal, Dubai, Abu Dhabi, Sharjah)
    - 🇸🇦 Saudi Arabia (National, NEOM)
    
    ### API Authentication:
    All endpoints (except registration and login) require Bearer token authentication.
    
    ### Contact:
    - **Developer**: Edy Bassil
    - **Email**: bassileddy@gmail.com
    - **GitHub**: [Environmental Impact Assessment](https://github.com/edybass/environmental-impact-assessment)
    """,
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.api.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware for security
if config.env == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*.environmental-assessment.com", "localhost"]
    )


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all API requests."""
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url.path}")
    
    # Process request
    response = await call_next(request)
    
    # Calculate duration
    duration = time.time() - start_time
    
    # Log response
    logger.info(
        f"Response: {request.method} {request.url.path} "
        f"- Status: {response.status_code} - Duration: {duration:.3f}s"
    )
    
    # Add custom headers
    response.headers["X-Process-Time"] = str(duration)
    response.headers["X-API-Version"] = app.version
    
    return response


# Exception handlers
@app.exception_handler(ServiceException)
async def service_exception_handler(request: Request, exc: ServiceException):
    """Handle service layer exceptions."""
    logger.error(f"Service exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": str(exc),
            "code": exc.code,
            "type": "service_error"
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors."""
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "type": "validation_error"
        }
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "type": "http_error"
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    
    # Don't expose internal errors in production
    if config.env == "production":
        detail = "An unexpected error occurred"
    else:
        detail = str(exc)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": detail,
            "type": "internal_error"
        }
    )


# Register routers
for router in all_routers:
    app.include_router(router)


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """API root endpoint with system information."""
    return {
        "name": config.app_name,
        "version": config.app_version,
        "environment": config.env,
        "author": config.app_author,
        "documentation": "/api/docs",
        "health": "/health",
        "features": config.features
    }


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring."""
    try:
        # Check database connection
        from src.models import get_session
        db = get_session()
        db.execute("SELECT 1")
        db.close()
        db_status = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "unhealthy"
    
    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "timestamp": time.time(),
        "services": {
            "database": db_status,
            "api": "healthy"
        },
        "version": app.version,
        "environment": config.env
    }


# API Information endpoint
@app.get("/api/info", tags=["Information"])
async def api_info():
    """Get API configuration and capabilities."""
    return {
        "version": app.version,
        "environment": config.env,
        "features": config.features,
        "jurisdictions": [
            "UAE Federal", "Dubai", "Abu Dhabi", "Sharjah",
            "KSA National", "Riyadh", "Jeddah", "NEOM"
        ],
        "parameters": {
            "air_quality": ["pm10", "pm25", "nox", "so2", "co", "voc"],
            "noise": ["peak_level", "average_level"],
            "water": ["consumption", "quality", "discharge"],
            "waste": ["generation", "recycling", "disposal"]
        },
        "thresholds": {
            "UAE": {
                "pm10_24hr": config.regional.uae_pm10_limit,
                "pm25_24hr": config.regional.uae_pm25_limit,
                "noise_residential_day": config.regional.uae_noise_residential_day
            },
            "KSA": {
                "pm10_24hr": config.regional.ksa_pm10_limit,
                "pm25_24hr": config.regional.ksa_pm25_limit,
                "noise_day": config.regional.ksa_noise_day
            }
        }
    }


# Custom OpenAPI schema
def custom_openapi():
    """Customize OpenAPI schema."""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = app.openapi()
    
    # Add security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT token obtained from /api/auth/login endpoint"
        }
    }
    
    # Add tags description
    openapi_schema["tags"] = [
        {
            "name": "Authentication",
            "description": "User registration, login, and authentication"
        },
        {
            "name": "Projects",
            "description": "Project management and lifecycle"
        },
        {
            "name": "Assessments",
            "description": "Environmental impact assessments"
        },
        {
            "name": "Monitoring",
            "description": "Real-time environmental monitoring"
        },
        {
            "name": "Compliance",
            "description": "Regulatory compliance checking"
        },
        {
            "name": "Reports",
            "description": "Report generation and export"
        }
    ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    uvicorn.run(
        "app:app",
        host=config.api.host,
        port=config.api.port,
        reload=config.api.debug,
        log_level="info" if config.debug else "warning"
    )