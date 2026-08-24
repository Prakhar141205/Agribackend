import json

from app.ai.explorer_prompts import EXPLORER_PROMPT
from app.ai.gemini_client import GeminiClient
from app.schemas.explorer import (
    ExplorerRequest,
    ExplorerResponse,
)


class ExplorerService:

    def __init__(
        self,
        gemini_client: GeminiClient,
    ):
        self.gemini_client = gemini_client

    async def explore(
        self,
        request: ExplorerRequest,
        knowledge_context: dict,
    ) -> ExplorerResponse:

        prompt_variables = {
            "query": request.query,
            "crop": request.crop or "Not specified",
            "disease": request.disease or "Not specified",
            "knowledge_context": json.dumps(
                knowledge_context,
                ensure_ascii=True,
            ),
        }

        return await self.gemini_client.generate_explorer_information(
            prompt=EXPLORER_PROMPT,
            prompt_variables=prompt_variables,
        )