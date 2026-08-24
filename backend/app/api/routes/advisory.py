from fastapi import APIRouter, HTTPException

from app.ai.gemini_client import GeminiClient
from app.schemas.advisory import FarmAdvisoryRequest
from app.services.advisory_service import AdvisoryService


router = APIRouter(
    prefix="/api/v1/advisory",
    tags=["Farm Advisory"],
)


def get_advisory_service() -> AdvisoryService:
    return AdvisoryService(
        gemini_client=GeminiClient(),
    )


@router.post("/recommend")
async def generate_farm_advisory(
    request: FarmAdvisoryRequest,
):

    try:

        service = get_advisory_service()

        result = await service.generate_advisory(
            request=request,
        )

        return {
            "success": True,
            "mode": (
                "crop_recommendation"
                if request.crop is None
                else "crop_management"
            ),
            "advisory": result.model_dump(),
        }

    except RuntimeError as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

    except ValueError as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail="Farm advisory generation failed.",
        ) from exc