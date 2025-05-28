"""
EIA Tool API
RESTful API for Environmental Impact Assessment
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.assessment import EIAScreening
from src.analysis import ConstructionImpact

app = FastAPI(
    title="EIA Tool API",
    description="Environmental Impact Assessment API for UAE/KSA",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ScreeningRequest(BaseModel):
    project_type: str
    location: str
    project_size: float
    duration: int
    sensitive_receptors: List[str] = []
    water_usage: float = 0
    near_protected_area: bool = False


class NoiseRequest(BaseModel):
    equipment: List[str]
    working_hours: str
    nearest_receptor_distance: float
    receptor_type: str = "residential"
    barriers: bool = False


class DustRequest(BaseModel):
    soil_type: str
    moisture_content: float
    wind_speed: float
    area_disturbed: float
    mitigation_measures: List[str] = []


@app.get("/")
async def root():
    return {
        "message": "EIA Tool API",
        "endpoints": {
            "/screening": "EIA screening assessment",
            "/impact/noise": "Construction noise assessment",
            "/impact/dust": "Construction dust assessment",
            "/docs": "API documentation"
        }
    }


@app.post("/api/screening")
async def screening_assessment(request: ScreeningRequest):
    """Perform EIA screening assessment."""
    try:
        screening = EIAScreening(request.project_type, request.location)

        project_data = {
            "project_size": request.project_size,
            "duration": request.duration,
            "sensitive_receptors": request.sensitive_receptors,
            "water_usage": request.water_usage,
            "near_protected_area": request.near_protected_area
        }

        result = screening.assess(project_data)

        return {
            "eia_required": result.eia_required,
            "eia_level": result.eia_level,
            "key_concerns": result.key_concerns,
            "regulatory_requirements": result.regulatory_requirements,
            "specialist_studies": result.specialist_studies,
            "estimated_duration": result.estimated_duration
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/impact/noise")
async def noise_assessment(request: NoiseRequest):
    """Assess construction noise impact."""
    try:
        analyzer = ConstructionImpact()
        result = analyzer.assess_noise(
            equipment=request.equipment,
            working_hours=request.working_hours,
            nearest_receptor_distance=request.nearest_receptor_distance,
            receptor_type=request.receptor_type,
            barriers=request.barriers
        )

        return {
            "peak_noise_level": result.peak_noise_level,
            "average_noise_level": result.average_noise_level,
            "exceeds_limit": result.exceeds_limit,
            "affected_receptors": result.affected_receptors,
            "mitigation_required": result.mitigation_required,
            "mitigation_measures": result.mitigation_measures
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/impact/dust")
async def dust_assessment(request: DustRequest):
    """Assess construction dust impact."""
    try:
        analyzer = ConstructionImpact()
        result = analyzer.assess_dust(
            soil_type=request.soil_type,
            moisture_content=request.moisture_content,
            wind_speed=request.wind_speed,
            area_disturbed=request.area_disturbed,
            mitigation_measures=request.mitigation_measures
        )

        return {
            "pm10_concentration": result.pm10_concentration,
            "pm25_concentration": result.pm25_concentration,
            "deposition_rate": result.deposition_rate,
            "exceeds_limit": result.exceeds_limit,
            "affected_area_radius": result.affected_area_radius,
            "mitigation_effectiveness": result.mitigation_effectiveness
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
