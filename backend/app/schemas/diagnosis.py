from pydantic import BaseModel, Field


class Prediction(BaseModel):
    class_name: str
    confidence: float = Field(ge=0.0, le=1.0)


class DiagnosisResponse(BaseModel):
    success: bool
    prediction: Prediction | None
    uncertain: bool
    message: str