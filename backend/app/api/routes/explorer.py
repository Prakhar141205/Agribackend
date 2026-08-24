from fastapi import APIRouter, HTTPException

from app.ai.gemini_client import GeminiClient
from app.schemas.explorer import ExplorerRequest
from app.services.explorer_service import ExplorerService


router = APIRouter(
    prefix="/api/v1/explorer",
    tags=["Explorer"],
)


def get_explorer_service() -> ExplorerService:
    return ExplorerService(
        gemini_client=GeminiClient(),
    )


@router.post("/ask")
async def explore(
    request: ExplorerRequest,
):
    try:
        service = get_explorer_service()

        result = await service.explore(
            request=request,
            knowledge_context={},
        )

        return {
            "success": True,
            "result": result.model_dump(),
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
            detail=f"Explorer request failed: {exc}",
        ) from exc