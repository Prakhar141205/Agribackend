import json

from app.ai.advisory_prompts import (
    CROP_MANAGEMENT_PROMPT,
    CROP_RECOMMENDATION_PROMPT,
)

from app.ai.gemini_client import GeminiClient

from app.schemas.advisory import (
    CropManagementResponse,
    CropRecommendationResponse,
    FarmAdvisoryRequest,
)


class AdvisoryService:

    def __init__(
        self,
        gemini_client: GeminiClient,
    ):
        self.gemini_client = gemini_client

    def _build_prompt_variables(
        self,
        request: FarmAdvisoryRequest,
    ) -> dict[str, str]:

        return {
            "location": json.dumps(
                request.location.model_dump(),
                ensure_ascii=True,
            ),
            "season": request.season,
            "crop": request.crop or "Not specified",
            "growth_stage": (
                request.growth_stage
                or "Not specified"
            ),
            "soil": json.dumps(
                request.soil.model_dump(),
                ensure_ascii=True,
            ),
            "environment": json.dumps(
                request.environment.model_dump(),
                ensure_ascii=True,
            ),
            "light": json.dumps(
                request.light.model_dump(),
                ensure_ascii=True,
            ),
        }

    async def generate_advisory(
        self,
        request: FarmAdvisoryRequest,
    ) -> (
        CropRecommendationResponse
        | CropManagementResponse
    ):

        prompt_variables = self._build_prompt_variables(
            request
        )

        if request.crop is None:

            return await self.gemini_client.generate_crop_recommendations(
                prompt=CROP_RECOMMENDATION_PROMPT,
                prompt_variables=prompt_variables,
            )

        return await self.gemini_client.generate_crop_management(
            prompt=CROP_MANAGEMENT_PROMPT,
            prompt_variables=prompt_variables,
        )