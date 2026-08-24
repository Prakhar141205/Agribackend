from pydantic import BaseModel, Field


class ViTPrediction(BaseModel):
    class_name: str
    confidence: float = Field(ge=0.0, le=1.0)
    class_index: int


class ConfidenceAnalysis(BaseModel):
    accepted: bool
    top1_confidence: float = Field(ge=0.0, le=1.0)
    top2_confidence: float = Field(ge=0.0, le=1.0)
    confidence_margin: float
    confidence_threshold_passed: bool
    margin_threshold_passed: bool


class DiseaseInformationRequest(BaseModel):
    prediction: ViTPrediction
    top_k: list[ViTPrediction] = Field(default_factory=list)
    uncertain: bool
    confidence_analysis: ConfidenceAnalysis
    more_information_available: bool


class DiseaseInformation(BaseModel):
    disease: str
    overview: str
    symptoms: list[str] = Field(default_factory=list)
    causes: list[str] = Field(default_factory=list)
    spread: list[str] = Field(default_factory=list)
    favorable_conditions: list[str] = Field(default_factory=list)
    prevention: list[str] = Field(default_factory=list)
    management: list[str] = Field(default_factory=list)
    treatment: list[str] = Field(default_factory=list)
    affected_parts: list[str] = Field(default_factory=list)
    severity: str
    immediate_actions: list[str] = Field(default_factory=list)
    things_to_avoid: list[str] = Field(default_factory=list)