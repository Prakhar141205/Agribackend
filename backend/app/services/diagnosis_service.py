from app.ml.confidence import is_confident
from app.schemas.diagnosis import DiagnosisResponse, Prediction


def build_diagnosis_response(
    class_name: str,
    confidence: float,
) -> DiagnosisResponse:

    confident = is_confident(
        confidence
    )

    if not confident:
        return DiagnosisResponse(
            success=True,
            prediction=Prediction(
                class_name=class_name,
                confidence=confidence,
            ),
            uncertain=True,
            message=(
                "The model is not sufficiently confident. "
                "Please upload a clearer image."
            ),
        )

    return DiagnosisResponse(
        success=True,
        prediction=Prediction(
            class_name=class_name,
            confidence=confidence,
        ),
        uncertain=False,
        message="Disease classified successfully.",
    )