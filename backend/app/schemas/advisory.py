from pydantic import BaseModel, Field


class LocationContext(BaseModel):
    state: str
    district: str


class SoilContext(BaseModel):
    moisture_percent: float = Field(
        ge=0,
        le=100,
    )
    ph: float = Field(
        ge=0,
        le=14,
    )
    temperature_c: float


class EnvironmentContext(BaseModel):
    temperature_c: float
    humidity_percent: float = Field(
        ge=0,
        le=100,
    )


class LightContext(BaseModel):
    lux: float = Field(
        ge=0,
    )


class FarmAdvisoryRequest(BaseModel):
    location: LocationContext
    season: str

    crop: str | None = None
    growth_stage: str | None = None

    soil: SoilContext
    environment: EnvironmentContext
    light: LightContext


class CropRecommendation(BaseModel):
    crop: str
    suitability: str
    reason: str
    limitations: list[str]


class CropRecommendationResponse(BaseModel):
    title: str
    summary: str
    field_assessment: str
    recommended_crops: list[CropRecommendation]
    irrigation_guidance: list[str]
    fertilizer_guidance: list[str]
    risk_factors: list[str]
    safety_measures: list[str]
    next_actions: list[str]


class CropManagementResponse(BaseModel):
    title: str
    summary: str
    crop_assessment: str
    irrigation_guidance: list[str]
    fertilizer_guidance: list[str]
    risk_factors: list[str]
    safety_measures: list[str]
    next_actions: list[str]