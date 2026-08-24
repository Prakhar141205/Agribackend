from fastapi import APIRouter, Depends, HTTPException

from app.ai.gemini_client import GeminiClient
from app.schemas.disease import (
    DiseaseInformation,
    DiseaseInformationRequest,
)
from app.services.disease_service import DiseaseService


router = APIRouter(
    prefix="/api/v1/diseases",
    tags=["Disease Information"],
)


def get_disease_service() -> DiseaseService:
    return DiseaseService(
        gemini_client=GeminiClient(),
    )


@router.post(
    "/information",
    response_model=DiseaseInformation,
)
async def get_disease_information(
    diagnostic: DiseaseInformationRequest,
    disease_service: DiseaseService = Depends(
        get_disease_service
    ),
) -> DiseaseInformation:

    if diagnostic.uncertain:
        raise HTTPException(
            status_code=400,
            detail=(
                "Detailed disease information is unavailable "
                "for an uncertain diagnosis."
            ),
        )

    if not diagnostic.confidence_analysis.accepted:
        raise HTTPException(
            status_code=400,
            detail=(
                "Detailed disease information is available "
                "only for accepted diagnoses."
            ),
        )

    if not diagnostic.more_information_available:
        raise HTTPException(
            status_code=400,
            detail=(
                "Additional information is not available "
                "for this diagnosis."
            ),
        )

    try:
        return await disease_service.get_disease_information(
            diagnostic=diagnostic,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc