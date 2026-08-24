from app.ai.disease_information_prompts import (
    DISEASE_INFORMATION_PROMPT,
    build_diagnostic_prompt_context,
)
from app.ai.gemini_client import GeminiClient
from app.schemas.disease import (
    DiseaseInformation,
    DiseaseInformationRequest,
)


class DiseaseService:

    def __init__(
        self,
        gemini_client: GeminiClient,
    ):
        self.gemini_client = gemini_client

    async def get_disease_information(
        self,
        diagnostic: DiseaseInformationRequest,
    ) -> DiseaseInformation:

        prompt_variables = build_diagnostic_prompt_context(
            diagnostic=diagnostic,
        )

        return await self.gemini_client.generate_disease_information(
            prompt=DISEASE_INFORMATION_PROMPT,
            prompt_variables=prompt_variables,
        )