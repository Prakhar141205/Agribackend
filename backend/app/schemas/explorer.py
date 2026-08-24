from pydantic import BaseModel, Field

class ExplorerRequest(BaseModel):
    query: str = Field(
        min_length=3,
        max_length=1000,
    )

    crop: str | None = None

    disease: str | None = None


class ExplorerResponse(BaseModel):
    title: str
    summary: str
    overview: str
    symptoms: list[str]
    causes: list[str]
    prevention: list[str]
    management: list[str]
    important_notes: list[str]