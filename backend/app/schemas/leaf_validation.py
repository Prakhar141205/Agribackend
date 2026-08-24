from pydantic import BaseModel, Field


class LeafValidationResponse(BaseModel):
    is_leaf: bool

    confidence: float = Field(
        ge=0,
        le=1,
    )

    reason: str