from fastapi import APIRouter, File, HTTPException, UploadFile
from app.ai.gemini_client import GeminiClient
from app.core.config import settings
from app.ml.inference import ViTInference
from app.schemas.disease import DiseaseInformationRequest
from app.services.disease_service import DiseaseService
from app.utils.image import load_and_validate_image


router = APIRouter(
    prefix="/api/v1/diseases",
    tags=["Disease Classification"],
)


inference_engine = ViTInference(
    model_path=settings.MODEL_PATH,
    confidence_threshold=settings.CONFIDENCE_THRESHOLD,
    margin_threshold=settings.TOP2_MARGIN_THRESHOLD,
    top_k=settings.TOP_K,
)


def get_disease_service() -> DiseaseService:
    return DiseaseService(
        gemini_client=GeminiClient(),
    )

@router.post("/predict")
async def predict_disease(
    file: UploadFile = File(...),
):

    try:

        image_bytes = await file.read()

        image = load_and_validate_image(
            image_bytes=image_bytes,
            content_type=file.content_type,
        )

        gemini_client = GeminiClient()

        leaf_validation = (
            await gemini_client.validate_leaf_image(
                image_bytes=image_bytes,
                mime_type=file.content_type,
            )
        )

        leaf_accepted = (
            leaf_validation.is_leaf
            and leaf_validation.confidence
            >= settings.LEAF_VALIDATION_THRESHOLD
        )

        if not leaf_accepted:

            return {
                "success": False,
                "filename": file.filename,
                "leaf_validation": (
                    leaf_validation.model_dump()
                ),
                "prediction": None,
                "message": (
                    "The uploaded image does not appear "
                    "to contain a sufficiently clear plant leaf."
                ),
            }

        result = inference_engine.predict(
            image
        )

        return {
            "success": True,
            "filename": file.filename,
            "leaf_validation": (
                leaf_validation.model_dump()
            ),
            **result,
        }

    except ValueError as exc:
        raise HTTPException(status_code=400,detail=str(exc))

    except RuntimeError as exc:
        raise HTTPException(status_code=500,detail=str(exc))

    except Exception as exc:
        raise HTTPException(status_code=500,detail=str(exc))
        